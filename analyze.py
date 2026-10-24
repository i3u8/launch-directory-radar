#!/usr/bin/env python3
"""Word-frequency / signal analysis over newly listed entries.

Writes reports/YYYY-MM-DD.md, reports/YYYY-MM-DD.json (machine summary), reports/latest.md,
and refreshes the README block between <!-- LATEST:START --> and <!-- LATEST:END -->.
"""
from __future__ import annotations

import argparse
import json
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
provides application applications""".split())
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
    """Return (unigram set, bigram set) for an entry."""
    uni, bi = set(), set()
    for field in (e.get("name", ""), e.get("tagline", ""), e.get("category", "")):
        seq = tokens(field)
        seq = [stem(t) if t else None for t in seq]
        for t in seq:
            if t and t != "ai":
                uni.add(t)
        for a, b in zip(seq, seq[1:]):
            if a and b and a != b:
                bi.add(f"{a} {b}")
    return uni, bi


def has_ai(e):
    t = " ".join([e.get("name", ""), e.get("tagline", ""), e.get("category", "")]).lower()
    return bool(re.search(r"\bai\b|\bllm\b|\bgpt\b|人工智能|\bagent", t))


def pid(e, src_domains):
    d = domain_of(e["url"])
    if d and d != src_domains.get(e["source"]):
        return d
    return e["source"] + "|" + (e.get("name") or e["url"]).lower()


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


def count(entries, srcmap=None):
    """Document frequency of unigrams/bigrams; optionally record which sources contain each term."""
    uc, bc = Counter(), Counter()
    for e in entries:
        u, b = terms_of(e)
        uc.update(u)
        bc.update(b)
        if srcmap is not None:
            for t in u | b:
                srcmap[t].add(e["source"])
    return uc, bc


def rank(today_c, n_today, b7, n7, b30, n30, min_count, top=15, srcmap=None, min_src=1):
    rows = []
    for t, c in today_c.items():
        if c < min_count or (srcmap is not None and len(srcmap[t]) < min_src):
            continue
        r7 = (c / n_today) / ((b7.get(t, 0) + 0.5) / (n7 + 1)) if n7 else None
        r30 = (c / n_today) / ((b30.get(t, 0) + 0.5) / (n30 + 1)) if n30 else None
        rows.append(dict(term=t, today=c, b7=b7.get(t, 0), b30=b30.get(t, 0), r7=r7, r30=r30,
                         new=(b30.get(t, 0) == 0 and n30 >= 30)))
    top_rows = sorted(rows, key=lambda r: (-r["today"], r["term"]))[:top]
    rising = [r for r in rows if r["today"] >= min_count and ((r["r7"] or 0) >= 2.0 and (r["r30"] or 0) >= 2.0 or r["new"])]
    rising.sort(key=lambda r: (-(r["r30"] or 0) * r["today"] ** 0.5, r["term"]))
    return top_rows, rising[:top]


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
    srcmap = defaultdict(set)
    tu, tb = count(new_today, srcmap)
    n_active = len({e["source"] for e in new_today})
    min_src = 3 if n_active >= 10 else 1
    u7, b7 = count(w7)
    u30, b30 = count(w30)
    min_c = 3 if n_t >= 60 else 2
    top_u, rise_u = rank(tu, max(n_t, 1), u7, n7, u30, n30, min_c, srcmap=srcmap, min_src=min_src)
    top_b, rise_b = rank(tb, max(n_t, 1), b7, n7, b30, n30, min_c, srcmap=srcmap, min_src=min_src)
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

    # clusters: bigram shared by >=3 different products today
    clusters = []
    by_bi = defaultdict(list)
    for e in new_today:
        for b in terms_of(e)[1]:
            by_bi[b].append(e)
    used = set()
    for b, es in sorted(by_bi.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        if len(es) < 3:
            break
        if len({e["source"] for e in es}) < min(min_src, 2):
            continue
        key = frozenset(pid(e, src_dom) for e in es)
        if len(key & used) > 0.6 * len(key):
            continue
        used |= key
        clusters.append(dict(term=b, size=len(es), examples=[f"{e['name']} ({domain_of(e['url'])})" for e in es[:4]]))
        if len(clusters) >= 6:
            break
    signals = []
    for c in clusters[:3]:
        signals.append(f"同日聚类「{c['term']}」{c['size']} 个产品：" + "、".join(x.split(" (")[0] for x in c["examples"][:3]))
    for e in ours_today[:2]:
        signals.append(f"我们的站点上线：{domain_of(e['url'])} @ {src_dom.get(e['source'], e['source'])}")
    for d, s in overlap_today[:2]:
        signals.append(f"跨目录同时出现：{d}（{len(s)} 个目录）")
    for r in rise_b[:2] + rise_u[:2]:
        signals.append(f"升温词「{r['term']}」今日 {r['today']} 条" + ("（近30天首次出现）" if r["new"] else f"，较30天基线 {fmt_ratio(r['r30'])}"))

    enabled = [s for s in srcs.values() if s["enabled"]]
    h_ok = sum(1 for s in enabled if health.get(s["id"], {}).get("last_run") == today and not health[s["id"]].get("last_error"))
    h_fail = [s["id"] for s in enabled if health.get(s["id"], {}).get("last_error")]
    h_flag = [s["id"] for s in enabled if health.get(s["id"], {}).get("flagged")]
    n_dirs = len(srcs)

    summary = dict(date=today, sources_total=n_dirs, sources_enabled=len(enabled), sources_ok=h_ok,
                   sources_failed=len(h_fail), failed_ids=h_fail[:20], flagged_ids=h_flag,
                   new_today=n_raw_today, new_today_unique=n_t, ai_share_today=round(ai_today / n_t, 2) if n_t else None,
                   ai_share_30d=round(ai_30 / n30, 2) if n30 else None,
                   top_terms=[(r["term"], r["today"], r["new"] or ((r["r30"] or 0) >= 2 and (r["r7"] or 0) >= 2)) for r in top_u[:10]],
                   top_bigrams=[(r["term"], r["today"]) for r in top_b[:10]],
                   rising=[(r["term"], r["today"], None if r["r30"] is None else round(r["r30"], 1)) for r in (rise_u + rise_b)[:8]],
                   signals=signals[:7], repo=REPO_URL, report_url=f"{REPO_URL}/blob/main/reports/{today}.md", digest="")

    # LLM digest (best effort)
    if not a.no_llm and n_t >= 5:
        sample = [f"{e['name']}｜{e['tagline'][:80]}｜{e.get('category','')}" for e in new_today[:40]]
        ctx = (f"日期 {today}；今日新增 {n_t} 个产品。\n高频词：" + "、".join(f"{t}({c})" for t, c, _ in summary["top_terms"]) +
               "\n高频双词：" + "、".join(f"{t}({c})" for t, c in summary["top_bigrams"]) +
               "\n升温词：" + "、".join(f"{t}({c})" for t, c, _ in summary["rising"]) + "\n样例条目：\n" + "\n".join(sample))
        summary["digest"] = llm.digest(ctx)

    # ---------------- markdown
    L = [f"# 每日目录雷达 {today}", "",
         f"- 监控目录 {len(enabled)} / 筛查目录 {n_dirs}；今日成功 {h_ok}，失败 {len(h_fail)}" + (f"；连续失败预警：{', '.join(h_flag)}" if h_flag else ""),
         f"- 今日新增条目 **{n_raw_today}**（去重后 {n_t}）；7 天基线 {n7}，30 天基线 {n30}"
         + ("（基线样本偏少，升温判断仅供参考）" if n30 < 100 else ""),
         f"- AI 相关占比：今日 {summary['ai_share_today']}，30天 {summary['ai_share_30d']}", ""]
    if summary["digest"]:
        L += ["## LLM 摘要", "", summary["digest"], ""]
    if signals:
        L += ["## 信号 Signals", ""] + [f"- {s}" for s in signals] + [""]
    L += ["## 高频词 Top terms（按条目数）", "", "| 词 | 今日 | 来源数 | 7天基线 | 30天基线 | vs7d | vs30d |", "|---|---|---|---|---|---|---|"]
    for r in top_u:
        L.append(f"| {r['term']} | {r['today']} | {len(srcmap[r['term']])} | {r['b7']} | {r['b30']} | {fmt_ratio(r['r7'])} | {fmt_ratio(r['r30'])}{' 🆕' if r['new'] else ''} |")
    L += ["", "## 高频双词 Top bigrams", "", "| 双词 | 今日 | 7天基线 | 30天基线 | vs30d |", "|---|---|---|---|---|"]
    for r in top_b:
        L.append(f"| {r['term']} | {r['today']} | {r['b7']} | {r['b30']} | {fmt_ratio(r['r30'])}{' 🆕' if r['new'] else ''} |")
    L += ["", "## 升温词 Rising（今日占比 ≥2× 7天且 ≥2× 30天，或30天内首次出现）", ""]
    L += [f"- **{r['term']}** 今日 {r['today']}，vs7d {fmt_ratio(r['r7'])}，vs30d {fmt_ratio(r['r30'])}{' 🆕' if r['new'] else ''}" for r in (rise_u + rise_b)[:12]] or ["- （暂无）"]
    L += ["", "## 同日产品聚类 Clusters", ""]
    L += [f"- **{c['term']}** × {c['size']}：" + "；".join(c["examples"]) for c in clusters] or ["- （暂无）"]
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
        block = [f"**{today}** · 新增 {n_raw_today} · 监控 {len(enabled)} 个目录（今日成功 {h_ok}）", "",
                 "Top 关键词: " + "、".join(f"`{t}`({c})" for t, c, _ in summary["top_terms"]), "",
                 "Top 双词: " + "、".join(f"`{t}`({c})" for t, c in summary["top_bigrams"]), ""]
        if summary["rising"]:
            block += ["升温: " + "、".join(f"`{t}`" for t, _, _ in summary["rising"]), ""]
        if summary["digest"]:
            block += [f"> {summary['digest']}", ""]
        block += [f"完整报告: [reports/{today}.md](reports/{today}.md)", ""]
        txt = rp.read_text()
        txt = re.sub(r"<!-- LATEST:START -->.*<!-- LATEST:END -->", "<!-- LATEST:START -->\n" + "\n".join(block) + "<!-- LATEST:END -->", txt, flags=re.S)
        rp.write_text(txt)
    # prune old per-day reports (keep 90 days)
    cut = (d0 - timedelta(days=90)).strftime("%Y-%m-%d")
    for f in REPORTS.glob("20*"):
        if f.stem < cut:
            f.unlink()
    print(f"analyzed {today}: new={n_raw_today} unique={n_t} top={[t for t,_,_ in summary['top_terms'][:5]]}")


if __name__ == "__main__":
    main()
