#!/usr/bin/env python3
"""Word-frequency / signal analysis over newly listed entries.

Writes reports/YYYY-MM-DD.md, reports/YYYY-MM-DD.json (machine summary), reports/latest.md,
and refreshes the README block between <!-- LATEST:START --> and <!-- LATEST:END -->.
"""
from __future__ import annotations

import argparse
import html
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

from radar.common import REPO_URL, domain_of
from radar import llm
from radar.parsers import NOISE_DOMAINS

ROOT = Path(__file__).parent
DATA, REPORTS = ROOT / "data", ROOT / "reports"

STOP = set("""a an the and or but if then else for of to in on at by with from as is are was were be been being it its this that
these those i you he she we they me my your our their his her them us not no nor so too very can could will would should may might
must do does did done have has had having just only also than more most much many some any all each every other another such own same
into over under out up down off about above below between through during before after again further once here there when where why how
what which who whom whose while until because via per vs etc yet both either neither one two get gets got use uses used using make makes
made making let lets want wants need needs like likes help helps helping take takes lets across within without among around""".split())
NOISE = set("""free online tool tools app apps best new simple easy fast quick powered based platform website site web page pages
open source built build builds create creates created creating generate generates generator generation turn turns helps
smart modern next real instant daily better good great top ultimate complete powerful minimal lightweight beta alpha
launch launches launched product products project projects software service services solution solutions company
other general misc various ready your yours everything anything things thing way ways time
http https www com org net html read more rated rating ratings pricing freemium paid trial offer offers provide provides
provided providing information home edit visit view click link links contact copyright rights reserved privacy policy terms
login sign signup subscribe newsletter learn discover explore find share join start today feature features benefit benefits
review reviews detail details listing listings directory submit submitted alternative alternatives pick editor featured
sponsor sponsored sponsorsed top latest recent popular trending add added ago day days week weeks month hour hours
people user users team teams work works working world business businesses service company companies solution
betting bets bet casino escort escorts porn sex slot slots gambling bikini swimwear lingerie
accurate half fits fit adds add score professional quality high higher coverage support supports allows allow enables enable
provides application applications
first include includes including combine combines combined wide range discover discovering driving measurable written
visited particularly suggest suggests enhance enhances enhancing understanding known fee fees across unforgettable
viral growth results result especially ensure ensures ensuring various variety offering offered along""".split())
KEEP_SHORT = {"3d", "qr", "vr", "ar", "ui", "ux", "ml", "ai", "pdf", "seo", "api", "llm", "gpt", "cli", "sql", "nft"}
CJK = re.compile(r"[\u4e00-\u9fff]+")
CJK_STOP = set("的了和是在有与及或为你我他她它们这那个一不也都就而及并被把对从到用让将可能请")
WORD = re.compile(r"[a-z0-9][a-z0-9\-\+\.]*[a-z0-9]|[a-z0-9]")


def tokens(text: str):
    """Yield token list per field with None markers for stopword/noise positions."""
    text = re.sub(r"https?://\S+|www\.\S+|\b[\w-]+\.(com|org|net|io|ai|dev|app|co|xyz)\b", " ", text.lower())
    seq = []
    pos = 0
    for m in re.finditer(r"[\u4e00-\u9fff]+|[a-z0-9][a-z0-9'’\+\.]*", text):
        t = m.group(0)
        if CJK.fullmatch(t):
            chars = [c for c in t if c not in CJK_STOP]
            seq += [a + b for a, b in zip(chars, chars[1:])] or chars
            seq.append(None)
            continue
        t = t.strip("-.'’+") if not t.endswith("+") else t
        t = re.sub(r"['’]s$", "", t)
        if re.fullmatch(r"[\d\.\-]+", t) or "." in t and re.search(r"\.[a-z]{2,}$", t):
            seq.append(None)  # numbers and domain-like tokens are not keywords
            continue
        if (len(t) < 3 and t not in KEEP_SHORT) or t in STOP or t in NOISE:
            seq.append(None)
        else:
            seq.append(t)
    return seq


def stem(t: str) -> str:
    if t.isascii() and len(t) > 4:
        if t.endswith("ies"):
            return t[:-3] + "y"
        if t.endswith("s") and not t.endswith(("ss", "us", "is")):
            return t[:-1]
    return t


def terms_of(e):
    """Return the set of unigrams, bigrams and trigrams of an entry (contiguous non-stopword tokens
    within one field; 'ai' is kept only inside n-grams)."""
    out = set()
    for field in (e.get("name", ""), e.get("tagline", ""), e.get("category", "")):
        seq = [stem(t) if t else None for t in tokens(field)]
        for i, a in enumerate(seq):
            if not a:
                continue
            if a != "ai":
                out.add(a)
            b = seq[i + 1] if i + 1 < len(seq) else None
            if b and b != a:
                out.add(f"{a} {b}")
                c = seq[i + 2] if i + 2 < len(seq) else None
                if c and c != b and c != a:
                    out.add(f"{a} {b} {c}")
    return out


def load_generic():
    """generic_terms.txt -> (explicit term set, generic single words)."""
    terms = set()
    p = ROOT / "generic_terms.txt"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip().lower()
            if line:
                terms.add(" ".join(stem(w) for w in line.split()))
    words = {t for t in terms if " " not in t} | {"ai"}
    return terms, words


# data-driven suppression: a term that appears in more than this share of the whole corpus is "head"
CORPUS_SHARE = {1: 0.015, 2: 0.007, 3: 0.004}
CORPUS_MIN_DF = 25
NGRAM_BONUS = {1: 1.0, 2: 1.5, 3: 1.9}
NICHE_MIN, NICHE_MAX, NICHE_MIN_SRC = 2, 15, 2


def is_generic(term, generic, gwords, df, n_corpus):
    n = len(term.split())
    if term in generic or all(w in gwords for w in term.split()):
        return True
    d = df.get(term, 0)
    return d >= CORPUS_MIN_DF and d / max(n_corpus, 1) > CORPUS_SHARE[n]


def pick_examples(es, k=3):
    """Up to k example entries, one per distinct product (prefer the real product site over a directory page)."""
    out, seen = [], set()
    for e in sorted(es, key=lambda e: (-len(e.get("tagline", "")), e.get("name", ""))):
        key = re.sub(r"[^a-z0-9]+", " ", (e.get("name") or "").lower()).strip()
        if key in seen:
            continue
        seen.add(key)
        out.append(dict(name=html.unescape(e.get("name") or "")[:60], url=e["url"]))
        if len(out) >= k:
            break
    return out


def niche_terms(raw_today, hist30, corpus, src_dom, n_corpus_df):
    """Rank focused terms. Returns list of dict(term,count,sources,df,b30,ratio,new,score,entries,examples)."""
    generic, gwords = load_generic()
    df = n_corpus_df
    n_corpus = df.get("__N__", 1)
    by_term = defaultdict(list)
    for e in raw_today:  # raw: the same product listed in N directories contributes N sources, 1 product
        for t in terms_of(e):
            by_term[t].append(e)
    new_today = dedupe(raw_today, src_dom)
    b30 = Counter()
    for e in hist30:
        b30.update(terms_of(e))
    n_t, n30 = max(len(new_today), 1), len(hist30)
    rows = []
    for t, es in by_term.items():
        doms = {pid(e, src_dom) for e in es}
        c = len(doms)  # distinct products
        if c < NICHE_MIN or c > NICHE_MAX:
            continue
        n = len(t.split())
        if n == 1 and (len(t) < 4 or t in STOP):
            continue
        srcs = {e["source"] for e in es}
        if len(srcs) < NICHE_MIN_SRC:
            continue
        if n > 1 and "ai" in t.split():  # "first ai", "include ai": need the other words to be rare
            others = [w for w in t.split() if w != "ai"]
            if any(df.get(w, 0) / n_corpus > 0.005 for w in others):
                continue
        if is_generic(t, generic, gwords, df, n_corpus):
            continue
        d = df.get(t, c)
        idf = math.log(n_corpus / (d + 1)) if n_corpus > d else 0.1
        ratio = (c / n_t) / ((b30[t] + 0.5) / (n30 + 1)) if n30 else None
        new = b30[t] == 0 and n30 >= 30
        score = idf * math.log2(1 + c) * NGRAM_BONUS[n] * (min(ratio, 25) ** 0.35 if ratio else 1) * (1.3 if new else 1)
        rows.append(dict(term=t, count=c, sources=len(srcs), df=d, b30=b30[t], ratio=ratio, new=new, score=score,
                         ids={pid(e, src_dom) for e in es}, examples=pick_examples(es)))
    rows.sort(key=lambda r: (-r["score"], r["term"]))
    return rows


def dedupe_terms(rows, limit, exclude=()):
    """Greedy pick by score; skip a term whose products are (>=75%) already covered by a chosen one
    (singular/plural, bigram containing its unigram, trigram containing its bigram...)."""
    chosen = []
    for r in rows:
        if r["term"] in exclude:
            continue
        dup = False
        for c in chosen:
            inter = len(r["ids"] & c["ids"])
            if inter >= 0.75 * min(len(r["ids"]), len(c["ids"])) or r["term"] in c["term"].split() and inter >= 0.5 * len(r["ids"]):
                dup = True
                break
        if not dup:
            chosen.append(r)
            if len(chosen) >= limit:
                break
    return chosen


def has_ai(e):
    t = " ".join([e.get("name", ""), e.get("tagline", ""), e.get("category", "")]).lower()
    return bool(re.search(r"\bai\b|\bllm\b|\bgpt\b|人工智能|\bagent", t))


def pid(e, src_domains):
    """Product identity: normalised name (the same product listed on several directories, or on its own
    site, counts once). Falls back to the url's domain/path when there is no name."""
    name = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", html.unescape(e.get("name") or "").lower()).strip()
    if name:
        return "n|" + name
    return domain_of(e["url"]) or e["url"]


def load(today):
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text())
    srcs = {s["id"]: s for s in yaml.safe_load((ROOT / "sources.yaml").read_text())["sources"]}
    src_dom = {i: s["domain"] for i, s in srcs.items()}
    entries = []
    p = DATA / "entries.jsonl"
    if p.exists():
        for line in p.open(encoding="utf-8"):
            try:
                entries.append(json.loads(line))
            except Exception:
                pass
    dp = DATA / "daily" / f"{today}.json"
    daily = json.loads(dp.read_text()) if dp.exists() else {"new": [], "sources": {}}
    health = json.loads((DATA / "health.json").read_text()) if (DATA / "health.json").exists() else {}
    return cfg, srcs, src_dom, entries, daily, health


def dedupe(entries, src_dom):
    seen, out = set(), []
    for e in entries:
        k = pid(e, src_dom)
        if k not in seen:
            seen.add(k)
            out.append(e)
    return out


def corpus_df(entries, src_dom):
    """Document frequency of every term over the whole corpus (entries with text, one per product)."""
    df = Counter()
    n = 0
    for e in dedupe([e for e in entries if not e.get("baseline")], src_dom):
        df.update(terms_of(e))
        n += 1
    df["__N__"] = max(n, 1)
    return df


def fmt_ratio(x):
    return "–" if x is None else f"{x:.1f}x"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    ap.add_argument("--no-llm", action="store_true")
    a = ap.parse_args()
    today = a.date
    cfg, srcs, src_dom, entries, daily, health = load(today)
    ours = set(cfg["our_domains"])
    d0 = datetime.strptime(today, "%Y-%m-%d")
    day = lambda e: e.get("day") or e["first_seen"]
    new_today = dedupe(daily["new"], src_dom)
    n_raw_today = len(daily["new"])
    hist = [e for e in entries if not e.get("baseline") and day(e) < today]
    w7 = dedupe([e for e in hist if day(e) >= (d0 - timedelta(days=7)).strftime("%Y-%m-%d")], src_dom)
    w30 = dedupe([e for e in hist if day(e) >= (d0 - timedelta(days=30)).strftime("%Y-%m-%d")], src_dom)

    n_t, n7, n30 = len(new_today), len(w7), len(w30)
    df = corpus_df(entries, src_dom)
    cand = niche_terms(daily["new"], w30, entries, src_dom, df)
    top15 = dedupe_terms(cand, 15)
    top_set = {r["term"] for r in top15}
    new_terms = dedupe_terms([r for r in cand if r["new"]], 10, exclude=top_set)
    ai_today = sum(1 for e in new_today if has_ai(e))
    ai_30 = sum(1 for e in w30 if has_ai(e))

    # categories per source
    cat_src = defaultdict(Counter)
    for e in new_today:
        if e.get("category"):
            cat_src[e["source"]][e["category"]] += 1
    src_vol = Counter(e["source"] for e in daily["new"])

    # cross-source overlap (all history, external product domains only)
    dom_src = defaultdict(set)
    dom_name = {}
    for e in entries:
        d = domain_of(e["url"])
        if d and d != src_dom.get(e["source"]):
            dom_src[d].add(e["source"])
            dom_name.setdefault(d, e.get("name", ""))
    today_doms = {domain_of(e["url"]) for e in daily["new"]}
    overlap = sorted(((d, s) for d, s in dom_src.items() if len(s) >= 2 and not any(d == n or d.endswith('.' + n) for n in NOISE_DOMAINS | {'openai.com', 'anthropic.com', 'microsoft.com', 'notion.so', 'figma.com'})), key=lambda x: (-len(x[1]), x[0]))
    overlap_today = [(d, s) for d, s in overlap if d in today_doms][:10]
    ours_seen = {d: sorted(s) for d, s in dom_src.items() if d in ours}
    ours_today = [e for e in daily["new"] if domain_of(e["url"]) in ours]

    # micro-clusters: 3-10 similar products sharing a specific n-gram, from >=2 sources
    by_id = {pid(e, src_dom): e for e in new_today}  # one representative per product
    cl_rows = [r for r in cand if 3 <= r["count"] <= 10 and len(r["term"].split()) >= 2]
    clusters = []
    for r in dedupe_terms(cl_rows, 8):
        clusters.append(dict(term=r["term"], size=r["count"], sources=r["sources"],
                             examples=[dict(name=html.unescape(by_id[i].get("name", ""))[:60], url=by_id[i]["url"]) for i in sorted(r["ids"]) if i in by_id][:4]))
    signals = []
    for r in top15[:3]:
        ex = "、".join(x["name"] for x in r["examples"][:2])
        signals.append(f"小词「{r['term']}」今日 {r['count']} 个产品/{r['sources']} 个目录：{ex}")
    for c in clusters[:2]:
        signals.append(f"同日小簇「{c['term']}」{c['size']} 个相似产品：" + "、".join(x["name"] for x in c["examples"][:3]))
    for e in ours_today[:2]:
        signals.append(f"我们的站点上线：{domain_of(e['url'])} @ {src_dom.get(e['source'], e['source'])}")
    for d, s in overlap_today[:2]:
        signals.append(f"跨目录同时出现：{d}（{len(s)} 个目录）")

    enabled = [s for s in srcs.values() if s["enabled"]]
    h_ok = sum(1 for s in enabled if health.get(s["id"], {}).get("last_run") == today and not health[s["id"]].get("last_error"))
    h_fail = [s["id"] for s in enabled if health.get(s["id"], {}).get("last_error")]
    h_flag = [s["id"] for s in enabled if health.get(s["id"], {}).get("flagged")]
    n_dirs = len(srcs)

    def pack(r):
        return dict(term=r["term"], count=r["count"], sources=r["sources"], ratio=None if r["ratio"] is None else round(r["ratio"], 1),
                    new=r["new"], examples=r["examples"])

    summary = dict(date=today, sources_total=n_dirs, sources_enabled=len(enabled), sources_ok=h_ok,
                   sources_failed=len(h_fail), failed_ids=h_fail[:20], flagged_ids=h_flag,
                   new_today=n_raw_today, new_today_unique=n_t, ai_share_today=round(ai_today / n_t, 2) if n_t else None,
                   ai_share_30d=round(ai_30 / n30, 2) if n30 else None,
                   niche_terms=[pack(r) for r in top15], new_terms=[pack(r) for r in new_terms], clusters=clusters,
                   signals=signals[:7], repo=REPO_URL, report_url=f"{REPO_URL}/blob/main/reports/{today}.md", niche_groups="")

    # LLM: group niche terms into micro-niches (best effort, never fatal)
    if not a.no_llm and top15:
        lines = [f"{r['term']}（{r['count']}个，例：" + "；".join(x["name"] for x in r["examples"][:2]) + "）" for r in top15 + new_terms[:6]]
        summary["niche_groups"] = llm.niche_groups(f"日期 {today}，今日新增 {n_t} 个产品。聚焦小词及样例产品：\n" + "\n".join(lines))

    # ---------------- markdown
    mdex = lambda exs: "；".join(f"[{x['name']}]({x['url']})" for x in exs)
    L = [f"# 每日目录雷达 {today}", "",
         f"- 监控目录 {len(enabled)} / 筛查目录 {n_dirs}；今日成功 {h_ok}，失败 {len(h_fail)}" + (f"；连续失败预警：{', '.join(h_flag)}" if h_flag else ""),
         f"- 今日新增条目 **{n_raw_today}**（去重后 {n_t}）；7 天基线 {n7}，30 天基线 {n30}"
         + ("（基线样本偏少，“新出现”判断仅供参考）" if n30 < 100 else ""),
         f"- 语料 {df['__N__']} 个产品；出现率超过阈值的泛词与 `generic_terms.txt` 中的大词已被抑制。AI 相关占比：今日 {summary['ai_share_today']}，30天 {summary['ai_share_30d']}", ""]
    if summary["niche_groups"]:
        L += ["## 微赛道归纳（LLM）", "", summary["niche_groups"], ""]
    if signals:
        L += ["## 信号 Signals", ""] + [f"- {s}" for s in signals] + [""]
    L += ["## 聚焦小词 Top 15", "", "每个词：今日出现在 2–15 个产品、至少 2 个目录；按稀有度（IDF）× 今日/30天基线比 × n-gram 加权排序。", "",
          "| # | 词 | 今日 | 目录数 | vs30d | 示例产品 |", "|---|---|---|---|---|---|"]
    for i, r in enumerate(top15, 1):
        L.append(f"| {i} | **{r['term']}** | {r['count']} | {r['sources']} | {'🆕' if r['new'] else fmt_ratio(r['ratio'])} | {mdex(r['examples'])} |")
    L += ["", "## 新出现的词 New terms（30 天基线中从未出现）", ""]
    L += [f"- **{r['term']}** × {r['count']}（{r['sources']} 个目录）：{mdex(r['examples'])}" for r in new_terms] or ["- （暂无）"]
    L += ["", "## 同日小簇（3-10 个相似产品）", ""]
    L += [f"- **{c['term']}** × {c['size']}（{c['sources']} 个目录）：{mdex(c['examples'])}" for c in clusters] or ["- （暂无）"]
    L += ["", "## 各目录今日新增与热门分类", "", "| 目录 | 新增 | 热门分类 |", "|---|---|---|"]
    for sid, n in src_vol.most_common(12):
        cats = "、".join(f"{c}({k})" for c, k in cat_src[sid].most_common(3))
        L.append(f"| {src_dom.get(sid, sid)} | {n} | {cats} |")
    L += ["", "## 跨目录重复 Cross-listing（历史累计，同一产品域名出现在 ≥2 个目录）", ""]
    L += [f"- {d}（{dom_name.get(d, '')}）：{', '.join(src_dom.get(x, x) for x in sorted(s))}" for d, s in (overlap_today or overlap[:8])] or ["- （暂无）"]
    if ours_seen:
        L += ["", "## 我们的站点已被目录公开展示", ""] + [f"- {d}：{', '.join(src_dom.get(x, x) for x in s)}" for d, s in sorted(ours_seen.items())]
    if h_fail:
        L += ["", "## 今日失败的来源", ""] + [f"- {i}: {health[i].get('last_error')}（连续 {health[i].get('consecutive_failures')} 天）" for i in h_fail[:30]]
    L += ["", f"仓库 Repo: {REPO_URL}", ""]
    md = "\n".join(L)
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / f"{today}.md").write_text(md)
    (REPORTS / "latest.md").write_text(md)
    (REPORTS / f"{today}.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))

    # README block
    rp = ROOT / "README.md"
    if rp.exists():
        block = [f"**{today}** · 新增 {n_raw_today} · 监控 {len(enabled)} 个目录（今日成功 {h_ok}）", "", "聚焦小词 Top 15:", ""]
        for r in top15:
            block.append(f"- `{r['term']}` ×{r['count']}（{r['sources']} 目录）" + (" 🆕" if r["new"] else "") + "：" + "；".join(x["name"] for x in r["examples"][:2]))
        block.append("")
        if summary["niche_groups"]:
            block += ["微赛道归纳:", "", summary["niche_groups"], ""]
        block += [f"完整报告: [reports/{today}.md](reports/{today}.md)", ""]
        txt = rp.read_text()
        txt = re.sub(r"<!-- LATEST:START -->.*<!-- LATEST:END -->", "<!-- LATEST:START -->\n" + "\n".join(block) + "<!-- LATEST:END -->", txt, flags=re.S)
        rp.write_text(txt)
    # prune old per-day reports (keep 90 days)
    cut = (d0 - timedelta(days=90)).strftime("%Y-%m-%d")
    for f in REPORTS.glob("20*"):
        if f.stem < cut:
            f.unlink()
    print(f"analyzed {today}: new={n_raw_today} unique={n_t} niche={[r['term'] for r in top15[:6]]}")


if __name__ == "__main__":
    main()
