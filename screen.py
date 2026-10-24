#!/usr/bin/env python3
"""Screen every directory in directories.csv for monitorability.

Usage: python screen.py [--only domain1,domain2] [--workers 24] [--limit N]
Writes: sources.yaml (merged, `locked: true` rows are preserved), SCREENING.md, data/screen_raw.json
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import yaml
from bs4 import BeautifulSoup

from radar.common import absolutize, domain_of, fetch, make_session, norm_host, text_of
from radar.parsers import (analyze_html_list, html_quality, parse_feed, parse_html_list, parse_json,
                           parse_sitemap, pick_listing_prefix, sitemap_urls)

ROOT = Path(__file__).parent
FEED_PATHS = ["/feed", "/feed/", "/feed.xml", "/rss", "/rss.xml", "/atom.xml", "/launches.xml",
              "/index.xml", "/latest.xml", "/new.xml", "/feeds/latest", "/rss/latest", "/rss/new"]
API_PATHS = ["/api/launches", "/api/tools", "/api/products", "/api/listings", "/api/sites",
             "/api/projects", "/api/startups", "/api/latest", "/api/new", "/api/directory",
             "/api/items", "/api/apps", "/api/websites", "/api/entries", "/api/feed",
             "/api/v1/tools", "/api/v1/listings", "/api/tools/latest", "/api/products/latest"]
HTML_PATHS = ["/new", "/latest", "/recent", "/newest", "/new-tools", "/latest-sites", "/recently-added",
              "/newly-added", "/whats-new", "/new-listings", "/new-sites", "/new-websites", "/latest-tools",
              "/latest-submissions", "/recent-submissions", "/new-arrivals", "/tools/new", "/sites/new",
              "/latest-listings", "/new-products", "/latest-ai-tools", "/new-ai-tools", "/recent-listings"]
NEW_TEXT = re.compile(r"^\s*(new|latest|recent|newest|just added|recently added|newly added|new arrivals|"
                      r"new listings|latest sites|latest tools|latest listings|new sites|new tools|"
                      r"what'?s new|latest additions|latest submissions)\b", re.I)
API_SKIP = re.compile(r"submit|login|logout|auth|contact|subscribe|checkout|stripe|upload|payment|"
                      r"webhook|session|user|account|track|analytics|vote|comment|newsletter|csrf|token|"
                      r"verify|password|register|signup|oauth|cron|revalidate|click|report|admin", re.I)
BLOG_TOK = re.compile(r"/(blog|news|posts?|articles?|press|stories|story|insights|journal|magazine)(/|$)", re.I)
LIST_TOK = re.compile(r"/(tools?|sites?|websites?|listings?|products?|startups?|launch(es)?|software|apps?|"
                      r"projects?|detail|items?|agents?|compan(y|ies)|directory|submissions?|mcp|servers?)(/|$)", re.I)
PARK = re.compile(r"domain is for sale|buy this domain|sedoparking|hugedomains|this domain may be for sale|"
                  r"parked (free|domain)|domain has expired|afternic|dan\.com/buy", re.I)
CF = re.compile(r"just a moment|attention required|cf-browser-verification|enable javascript and cookies|"
                r"checking your browser|ddos protection by|captcha|are you human|access denied|"
                r"request rejected|incapsula|sucuri", re.I)
NEW_URL = re.compile(r"(new|latest|recent|newest|added|fresh)", re.I)
LOGIN = re.compile(r"log ?in to (continue|view|see)|sign ?in to (continue|view|see)|please (log|sign) ?in", re.I)


def stats_of(entries):
    n = len(entries)
    dated = sorted(e["listed_at"] for e in entries if e.get("listed_at"))
    host_ext = sum(1 for e in entries if e["url"] and domain_of(e["url"]) != domain_of(e.get("permalink") or e["url"]))
    words = [len(e["name"].split()) for e in entries]
    return dict(n=n, dated=len(dated), newest=dated[-1] if dated else None, oldest=dated[0] if dated else None,
                ext_ratio=round(host_ext / n, 2) if n else 0, median_words=statistics.median(words) if words else 0)


def looks_like_listing(entries, url, feed_title=""):
    st = stats_of(entries)
    perm = [urlparse(e.get("permalink") or e["url"]).path for e in entries[:30]]
    blog = sum(1 for p in perm if BLOG_TOK.search(p + "/"))
    lst = sum(1 for p in perm if LIST_TOK.search(p + "/"))
    if blog >= 0.5 * len(perm) and st["ext_ratio"] < 0.3:
        return False, "entries are blog/news posts"
    if BLOG_TOK.search(urlparse(url).path + "/") and lst == 0 and st["ext_ratio"] < 0.3:
        return False, "blog/news feed"
    if lst or st["ext_ratio"] >= 0.3:
        return True, ""
    if st["median_words"] <= 4:
        return True, "short titles (name-like)"
    return False, "feed content looks like articles, not listings"


def get(s, url, **kw):
    try:
        r, body = fetch(s, url, **kw)
        return r, body
    except Exception:
        return None, b""


def _screen_domain(row, session):
    dom = row["domain"]
    res = dict(domain=dom, submit_url=row["submit_url"], kind=row["kind"], ledger_dir_status=row["ledger_dir_status"],
               class_="not_monitorable", reason="", url="", parser="", params={}, stats={}, notes=[], alt=[])
    if dom.startswith("form:"):
        res.update(reason="form_only", notes=["ledger entry is a hosted form (Google Form/Tally), no directory domain"])
        return res
    # ---- homepage
    home = None
    for base in (f"https://{dom}/", f"https://www.{dom}/", f"http://{dom}/"):
        r, body = get(session, base)
        if r is not None:
            home = (r, body)
            break
    if home is None:
        res.update(reason="dead", notes=["no connection / DNS failure on https+http, apex+www"])
        return res
    r, body = home
    base = f"{urlparse(r.url).scheme}://{urlparse(r.url).netloc}"
    html = text_of(r, body)
    res["home_status"] = r.status_code
    final_dom = domain_of(r.url)
    if final_dom and final_dom != dom and not final_dom.endswith("." + dom):
        res["notes"].append(f"home redirects to {final_dom}")
    blocked = r.status_code in (401, 403, 429, 503) or (len(html) < 200_000 and CF.search(html[:4000] or "") and r.status_code != 200)
    if r.status_code >= 500 and not blocked:
        res.update(reason="dead", notes=res["notes"] + [f"home http {r.status_code}"])
        return res
    if r.status_code in (404, 410):
        res.update(reason="dead", notes=res["notes"] + [f"home http {r.status_code}"])
        return res
    if PARK.search(html[:20000]):
        res.update(reason="dead", notes=res["notes"] + ["parked / for-sale domain"])
        return res
    soup = BeautifulSoup(html, "html.parser") if html else None
    cands = {"json": [], "feed": [], "sitemap": [], "html": []}

    def sleep():
        time.sleep(0.15)

    # ---- link discovery from homepage
    if soup is not None:
        for l in soup.find_all("link", rel=True, href=True):
            rel = " ".join(l["rel"]).lower()
            typ = (l.get("type") or "").lower()
            if "alternate" in rel and ("rss" in typ or "atom" in typ or "xml" in typ):
                cands["feed"].append(absolutize(base + "/", l["href"]))
        for a in soup.find_all("a", href=True):
            t = a.get_text(" ", strip=True)
            if NEW_TEXT.match(t or "") and domain_of(absolutize(base + "/", a["href"])) == norm_host(urlparse(base).hostname):
                cands["html"].append(absolutize(base + "/", a["href"]))
            if re.search(r"(^|/)(rss|feed|atom)(\.xml)?/?$", a["href"], re.I):
                cands["feed"].append(absolutize(base + "/", a["href"]))
        # API endpoints mentioned in inline html / first scripts
        blobs = [html]
        for sc in soup.find_all("script", src=True)[:4]:
            su = absolutize(base + "/", sc["src"])
            if domain_of(su) == domain_of(base):
                rr, bb = get(session, su, max_bytes=1_500_000)
                if rr is not None and rr.status_code == 200:
                    blobs.append(text_of(rr, bb))
                sleep()
        found = []
        for b in blobs:
            for m in re.finditer(r"""["'`](/api/[A-Za-z0-9_\-/]{3,60})["'`]""", b):
                pth = m.group(1)
                if not API_SKIP.search(pth) and pth not in found:
                    found.append(pth)
        cands["json"] += [base + p_ for p_ in found[:8]]
        wp = "wp-content" in html or "wp-json" in html
    else:
        wp = False
    for u in filter(None, (row.get("live_urls") or "").split("|")):
        if domain_of(u) == dom and u.rstrip("/") != base and NEW_URL.search(u):
            cands["html"].append(u)
    # robots sitemaps
    rr, bb = get(session, base + "/robots.txt", max_bytes=200_000)
    if rr is not None and rr.status_code == 200 and b"<html" not in bb[:500].lower():
        for m in re.finditer(r"(?im)^\s*sitemap:\s*(\S+)", text_of(rr, bb)):
            cands["sitemap"].append(m.group(1))
    sleep()
    if blocked:
        res["notes"].append(f"home http {r.status_code}" + (" (anti-bot challenge)" if CF.search(html[:4000] or "") else ""))

    def uniq(l):
        seen = set()
        return [x for x in l if not (x in seen or seen.add(x))]

    # ---- 1. JSON (WordPress REST + /api guesses)
    json_cands = []
    if wp:
        rr, bb = get(session, base + "/wp-json/wp/v2/types", max_bytes=500_000)
        if rr is not None and rr.status_code == 200:
            try:
                types = json.loads(bb)
                for k, v in types.items():
                    if k not in ("post", "page", "attachment", "wp_block", "wp_template", "wp_template_part",
                                 "wp_navigation", "nav_menu_item", "wp_global_styles", "wp_font_family",
                                 "wp_font_face", "elementor_library", "e-floating-buttons", "product", "shop_order",
                                 "portfolio", "testimonial", "team", "faq") and v.get("rest_base"):
                        json_cands.append(f"{base}/wp-json/wp/v2/{v['rest_base']}?per_page=40&orderby=date&order=desc")
            except Exception:
                pass
        sleep()
    json_cands += uniq(cands["json"]) + [base + p_ for p_ in API_PATHS]
    if not blocked:
        for u in uniq(json_cands)[:30]:
            rr, bb = get(session, u, max_bytes=3_000_000)
            sleep()
            if rr is None or rr.status_code != 200 or not bb[:1].strip() in (b"{", b"["):
                continue
            try:
                ents = parse_json(bb, u, {})
            except Exception:
                continue
            if len(ents) >= 3:
                ok, why = looks_like_listing(ents, u)
                st = stats_of(ents)
                if ok or (st["ext_ratio"] == 0 and st["median_words"] <= 4):
                    res.update(**{"class_": "json_api", "url": u, "parser": "json_api", "stats": st})
                    return res
                res["notes"].append(f"json {urlparse(u).path} rejected: {why}")
    # ---- 2. feeds
    feed_urls = uniq(cands["feed"] + [base + p_ for p_ in FEED_PATHS])
    rejected_feed = None
    for u in feed_urls[:18]:
        rr, bb = get(session, u, max_bytes=3_000_000)
        sleep()
        if rr is None or rr.status_code != 200:
            continue
        head = bb[:600].lower()
        if b"<rss" not in head and b"<feed" not in head and b"<?xml" not in head and b"<rdf" not in head:
            continue
        try:
            ents, title = parse_feed(bb, u, {})
        except Exception:
            continue
        if len(ents) >= 3:
            ok, why = looks_like_listing(ents, u, title)
            st = stats_of(ents)
            kind = "atom" if b"<feed" in head else "rss"
            if ok:
                res.update(class_=kind, url=u, parser=kind, stats=st)
                if why:
                    res["notes"].append(why)
                return res
            rejected_feed = (u, why, st, kind)
    if rejected_feed:
        res["notes"].append(f"feed {urlparse(rejected_feed[0]).path} found but {rejected_feed[1]}")
        res["alt"].append(dict(kind=rejected_feed[3], url=rejected_feed[0], why=rejected_feed[1]))
    # ---- 3. sitemap
    sm_urls = uniq(cands["sitemap"] + [base + p_ for p_ in ("/sitemap.xml", "/sitemap_index.xml", "/sitemap-index.xml", "/wp-sitemap.xml")])
    for u in sm_urls[:5]:
        try:
            urls = sitemap_urls(session, u, max_children=3)
        except Exception:
            sleep()
            continue
        sleep()
        if not urls:
            continue
        pp = pick_listing_prefix(urls)
        if not pp:
            res["notes"].append(f"sitemap {urlparse(u).path} has {len(urls)} urls but no recognisable listing path")
            continue
        prefix, depth, cnt = pp
        ents = parse_sitemap(session, u, {"prefix": prefix, "depth": depth, "max_children": 3})
        st = stats_of(ents)
        if len(ents) >= 10:
            res.update(class_="sitemap", url=u, parser="sitemap", params={"prefix": prefix, "depth": depth, "cap": 300}, stats=st)
            if not st["dated"]:
                res["notes"].append("sitemap has no lastmod; first-seen dates only")
            return res
    # ---- 4. HTML list pages
    html_urls = uniq(cands["html"][:4] + [base + p_ for p_ in HTML_PATHS])
    if not blocked:
        for u in html_urls[:20]:
            rr, bb = get(session, u, max_bytes=2_500_000)
            sleep()
            if rr is None or rr.status_code != 200 or "html" not in rr.headers.get("content-type", "html"):
                continue
            if domain_of(rr.url) != domain_of(base) and not domain_of(rr.url).endswith(dom):
                continue
            if urlparse(rr.url).path in ("", "/") or not NEW_URL.search(rr.url):
                continue
            h = text_of(rr, bb)
            if CF.search(h[:3000]) and len(h) < 8000:
                continue
            a = analyze_html_list(h, rr.url)
            if a:
                ents = parse_html_list(h, rr.url, {"pattern": a["pattern"], "external": a["external"]})
                ok_q, why_q = html_quality(ents)
                if not ok_q:
                    res["notes"].append(f"html {urlparse(rr.url).path or '/'}: {why_q}")
                    continue
                if len(ents) >= 10:
                    res.update(class_="html_list", url=rr.url, parser="html_list",
                               params={"pattern": a["pattern"], "external": a["external"]}, stats=stats_of(ents))
                    return res
    # ---- nothing found: why?
    if blocked:
        res["reason"] = "blocked"
        res["notes"].append("anti-bot / forbidden; no probe path accessible")
        return res
    n_a = len(soup.find_all("a")) if soup is not None else 0
    visible = len(re.sub(r"\s+", " ", soup.get_text(" ", strip=True))) if soup is not None else 0
    if LOGIN.search(html[:30000]) and n_a < 15:
        res["reason"] = "login_wall"
    elif re.search(r"/(log-?in|sign-?in|auth)\b", urlparse(r.url).path, re.I):
        res["reason"] = "login_wall"
    elif n_a < 6 and visible < 400 and re.search(r'id="(root|__next|app|__nuxt)"|<noscript', html, re.I):
        res["reason"] = "js_only"
    elif row["ledger_dir_status"] in ("dead",):
        res["reason"] = "dead"
    else:
        res["reason"] = "no_public_list"
    return res


def screen_domain(row, session):
    res = _screen_domain(row, session)
    newest = (res.get("stats") or {}).get("newest")
    if res["class_"] != "not_monitorable" and newest:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(newest.replace("Z", "+00:00"))).days
        if age > 120:
            res["notes"].append(f"newest entry is {age}d old; source looks stale")
            res.update(reason="stale", stale_kind=res["class_"], class_="not_monitorable")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(ROOT / "directories.csv")))
    if a.only:
        keep = set(a.only.split(","))
        rows = [r for r in rows if r["domain"] in keep]
    if a.limit:
        rows = rows[: a.limit]
    sessions = [make_session(retries=1) for _ in range(a.workers)]
    results = {}

    def work(i, row):
        try:
            return screen_domain(row, sessions[i % a.workers])
        except Exception as e:  # never lose a domain
            return dict(domain=row["domain"], submit_url=row["submit_url"], kind=row["kind"],
                        ledger_dir_status=row["ledger_dir_status"], class_="not_monitorable",
                        reason="error", url="", parser="", params={}, stats={}, notes=[f"screen error: {e!r}"[:200]], alt=[])
    t0 = time.time()
    with ThreadPoolExecutor(a.workers) as ex:
        futs = {ex.submit(work, i, r): r["domain"] for i, r in enumerate(rows)}
        for n, f in enumerate(as_completed(futs), 1):
            res = f.result()
            results[res["domain"]] = res
            if n % 25 == 0:
                print(f"{n}/{len(rows)} {time.time()-t0:.0f}s", file=sys.stderr, flush=True)
    write_outputs(rows, results)


def sid(domain):
    return re.sub(r"[^a-z0-9]+", "-", domain.lower()).strip("-")


def write_outputs(rows, results):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    sp = ROOT / "sources.yaml"
    old = {}
    if sp.exists():
        for s in yaml.safe_load(sp.read_text()).get("sources", []):
            old[s["domain"]] = s
    sources = dict(old)
    raw_path = ROOT / "data" / "screen_raw.json"
    raw = json.loads(raw_path.read_text()) if raw_path.exists() else {}
    ovr = yaml.safe_load((ROOT / "overrides.yaml").read_text()) if (ROOT / "overrides.yaml").exists() else {}
    for d, res in results.items():
        raw[d] = res
        if old.get(d, {}).get("locked"):
            continue
        enabled = res["class_"] != "not_monitorable"
        kind = res["class_"] if enabled else "not_monitorable"
        note = "; ".join(res["notes"])[:300]
        if not enabled:
            note = (res["reason"] + ("; " if note else "") + note)[:300]
        sources[d] = dict(id=sid(d), domain=d, kind=kind, url=res["url"], parser=res["parser"] or None,
                          enabled=enabled, params=res["params"] or {}, notes=note, last_screened=today,
                          directory_kind=res["kind"], submit_url=res["submit_url"],
                          reason=None if enabled else res["reason"])
    for d, o in (ovr or {}).items():
        if d in sources and not sources[d].get("locked"):
            s_ = sources[d]
            if o.get("enabled") is False:
                s_.update(enabled=False, kind="not_monitorable", reason=o.get("reason", "manual"),
                          notes=f"{o.get('reason', 'manual')}; manual override: {o.get('notes', '')}"[:300])
    order = sorted(sources.values(), key=lambda s: (not s["enabled"], s["kind"], s["domain"]))
    sp.write_text("# Generated by screen.py (rows with `locked: true` are kept as-is on re-screen).\n" +
                  yaml.safe_dump({"sources": order}, allow_unicode=True, sort_keys=False, width=200))
    raw_path.parent.mkdir(exist_ok=True)
    raw_path.write_text(json.dumps(raw, ensure_ascii=False, indent=0))
    write_md(order, raw)


def write_md(sources, raw):
    from collections import Counter
    total = len(sources)
    en = [s for s in sources if s["enabled"]]
    by_kind = Counter(s["kind"] for s in en)
    by_reason = Counter(s["reason"] for s in sources if not s["enabled"])
    lines = ["# SCREENING — 目录可监控性筛查 / Directory monitorability screening", "",
             f"- 目录总数 total directories: **{total}**",
             f"- 已启用 enabled: **{len(en)}** (" + ", ".join(f"{k}: {v}" for k, v in by_kind.most_common()) + ")",
             f"- 不可监控 not monitorable: **{total - len(en)}** (" + ", ".join(f"{k}: {v}" for k, v in by_reason.most_common()) + ")",
             f"- 最近筛查 last screened: {max((s['last_screened'] for s in sources), default='')}", "",
             "Reasons: `dead` 无法连接/404/5xx/停放; `blocked` 反爬/403/Cloudflare; `login_wall` 需登录; `js_only` 纯前端渲染无 SSR 内容/无 feed; "
             "`no_public_list` 站点正常但无公开可抓的“最新”列表/feed/sitemap; `form_only` 仅表单入口。", "",
             "| # | domain | kind | enabled | why / notes | sample size | newest entry (UTC) |", "|---|---|---|---|---|---|---|"]
    for i, s in enumerate(sources, 1):
        st = (raw.get(s["domain"]) or {}).get("stats") or {}
        why = s["notes"] if s["enabled"] else (s["reason"] or "") + ((": " + s["notes"].split("; ", 1)[1]) if "; " in (s["notes"] or "") else "")
        why = (why or "").replace("|", "/")[:140]
        u = f" [{urlparse(s['url']).path or '/'}]({s['url']})" if s["url"] else ""
        lines.append(f"| {i} | {s['domain']} | {s['kind']}{u if s['enabled'] else ''} | {'✅' if s['enabled'] else '❌'} | {why} | {st.get('n', '')} | {(st.get('newest') or '')[:10]} |")
    (ROOT / "SCREENING.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
