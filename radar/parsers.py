"""Parsers turn a fetched source into normalised entries.

Every parser returns a list of dicts:
  {name, url, tagline, category, listed_at (ISO UTC or None), permalink}
`params` is the per-source dict from sources.yaml (parser specific).
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from urllib.parse import urlparse, unquote

import feedparser
from bs4 import BeautifulSoup

from .common import (absolutize, clean, domain_of, fetch, norm_host, norm_url,
                     text_of, to_iso)

# --------------------------------------------------------------------------- RSS / Atom


def _find_external(host: str, entry) -> str:
    blobs = [entry.get("summary", "") or "", entry.get("description", "") or ""]
    for c in entry.get("content", []) or []:
        blobs.append(c.get("value", ""))
    for b in blobs:
        for m in re.finditer(r"""href=["'](https?://[^"']+)""", b):
            if domain_of(m.group(1)) not in ("", host):
                return m.group(1)
        for m in re.finditer(r"\((https?://[^\s)]+)\)\s*$", clean(b, 2000)):
            if domain_of(m.group(1)) != host:
                return m.group(1)
    return ""


def parse_feed(body: bytes, base_url: str, params: dict | None = None):
    params = params or {}
    d = feedparser.parse(body)
    host = domain_of(base_url)
    out = []
    for e in d.entries:
        link = e.get("link", "") or ""
        title = clean(e.get("title", ""), 200)
        cat = ""
        sep = params.get("title_split")
        if sep and sep in title:
            title, cat = [x.strip() for x in title.rsplit(sep, 1)]
        if not cat:
            cat = clean([t.get("term", "") for t in e.get("tags", []) or []], 120)
        desc = clean(e.get("summary", "") or e.get("description", ""), 400)
        desc = re.sub(r"\s*\(https?://[^\s)]+\)\s*$", "", desc)
        ext = _find_external(host, e)
        if not ext and link and domain_of(link) != host:
            ext = link
        listed = to_iso(e.get("published_parsed") or e.get("updated_parsed")
                        or e.get("published") or e.get("updated"))
        if not title or not (ext or link):
            continue
        out.append(dict(name=title, url=ext or link, tagline=desc, category=cat,
                        listed_at=listed, permalink=link))
    return out, (d.feed.get("title", "") if d.get("feed") else "")


# --------------------------------------------------------------------------- JSON

NAME_K = ["name", "title", "tool_name", "toolName", "product_name", "productName", "site_name",
          "siteName", "app_name", "label", "project_name"]
URL_K = ["url", "website", "website_url", "websiteUrl", "site_url", "siteUrl", "link", "homepage",
         "external_url", "externalUrl", "tool_url", "toolUrl", "product_url", "href", "domain"]
PERMA_K = ["permalink", "detail_url", "detailUrl", "page_url", "pageUrl", "canonical_url"]
TAG_K = ["tagline", "description", "short_description", "shortDescription", "summary", "desc",
         "excerpt", "subtitle", "slogan", "one_liner", "oneLiner", "overview"]
CAT_K = ["category", "categories", "category_name", "categoryName", "type", "tags", "kind", "niche"]
DATE_K = ["createdAt", "created_at", "publishedAt", "published_at", "date", "addedAt", "added_at",
          "submittedAt", "submitted_at", "created", "timestamp", "pubDate", "updatedAt",
          "updated_at", "launchDate", "launch_date", "launchedAt", "dateAdded", "date_added", "time"]


def _pick(d: dict, keys):
    for k in keys:
        if k in d and d[k] not in (None, "", [], {}):
            v = d[k]
            if isinstance(v, dict) and "rendered" in v:  # WordPress REST
                v = v["rendered"]
            return v
    return None


def _find_lists(obj, depth=0, path=""):
    if isinstance(obj, list):
        if len(obj) >= 3 and sum(isinstance(x, dict) for x in obj) >= 0.8 * len(obj):
            yield path, obj
    if depth >= 3:
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                yield from _find_lists(v, depth + 1, f"{path}.{k}" if path else k)


def parse_json(body: bytes, base_url: str, params: dict | None = None):
    params = params or {}
    data = json.loads(body.decode("utf-8", errors="replace"))
    lists = list(_find_lists(data))
    if params.get("list_path"):
        lists = [(p, l) for p, l in lists if p == params["list_path"]] or lists
    best, bestscore = None, -1
    for path, lst in lists:
        score = 0
        for x in lst[:20]:
            if isinstance(x, dict) and _pick(x, NAME_K) and (_pick(x, URL_K) or _pick(x, PERMA_K)):
                score += 1
        if score > bestscore or (score == bestscore and best and len(lst) > len(best)):
            best, bestscore = lst, score
    if not best or bestscore < 3:
        return []
    fm = params.get("fields", {})
    out = []
    for x in best:
        if not isinstance(x, dict):
            continue
        g = lambda key, keys: x.get(fm[key]) if key in fm else _pick(x, keys)
        name, url, perma = g("name", NAME_K), g("url", URL_K), g("permalink", PERMA_K)
        if isinstance(name, dict):
            name = name.get("rendered") or name.get("en") or next(iter(name.values()), "")
        if not name or not (url or perma):
            continue
        url = str(url) if url else ""
        if url and not url.startswith("http") and "." in url and " " not in url:
            url = "https://" + url
        if url and not url.startswith("http"):
            url = ""
        perma = absolutize(base_url, str(perma)) if perma else ""
        tag = g("tagline", TAG_K)
        if isinstance(tag, dict):
            tag = tag.get("en") or next(iter(tag.values()), "")
        out.append(dict(name=clean(name, 200), url=url or perma, tagline=clean(tag, 400),
                        category=clean(g("category", CAT_K), 120),
                        listed_at=to_iso(g("date", DATE_K)), permalink=perma))
    return out


# --------------------------------------------------------------------------- sitemap

LISTING_SEGS = ("tool", "tools", "site", "sites", "website", "websites", "listing", "listings",
                "product", "products", "startup", "startups", "launch", "launches", "software",
                "app", "apps", "project", "projects", "detail", "item", "items", "agent", "agents",
                "company", "companies", "directory", "ai", "ai-tools", "business", "resource",
                "resources", "t", "s", "p", "r", "review", "reviews", "alternatives", "mcp",
                "server", "servers", "model", "models", "game", "games", "prompt", "prompts")
BAD_SEGS = ("blog", "blogs", "news", "category", "categories", "cat", "tag", "tags", "page", "author",
            "authors", "topic", "topics", "search", "about", "contact", "privacy", "terms", "login",
            "signup", "register", "submit", "pricing", "faq", "help", "docs", "legal", "feed",
            "sitemap", "wp-content", "wp-json", "cdn-cgi", "collections", "collection", "guides",
            "guide", "article", "articles", "post", "posts", "learn", "changelog", "press",
            "stories", "story", "podcast", "events", "jobs", "user", "users", "profile", "u",
            "compare", "comparison", "vs", "best", "top", "lists", "list", "country", "countries",
            "city", "cities", "location", "locations", "region", "regions", "languages", "language")
SKIP_EXT = re.compile(r"\.(jpe?g|png|gif|svg|webp|pdf|css|js|xml|txt|zip|mp4|ico)(\?|$)", re.I)


def _loc_children(root, ns):
    return [(clean(e.findtext(f"{ns}loc") or ""), e.findtext(f"{ns}lastmod")) for e in root]


def _slug_name(url: str) -> str:
    seg = unquote(urlparse(url).path.rstrip("/").split("/")[-1])
    seg = re.sub(r"\.(html?|php|aspx?)$", "", seg)
    return re.sub(r"[-_+]+", " ", seg).strip().title()[:120]


def _sm_root(body: bytes):
    root = ET.fromstring(body)
    ns = re.match(r"\{.*\}", root.tag)
    return root, (ns.group(0) if ns else ""), root.tag.split("}")[-1]


def sitemap_urls(session, url, max_children=3, max_bytes=8_000_000, _depth=0, hint_re=None):
    """Return list of (loc, lastmod_iso) from a sitemap or sitemap index."""
    r, body = fetch(session, url, max_bytes=max_bytes)
    if r.status_code != 200:
        raise RuntimeError(f"sitemap http {r.status_code}")
    if url.endswith(".gz") or body[:2] == b"\x1f\x8b":
        import gzip
        body = gzip.decompress(body)
    root, ns, kind = _sm_root(body)
    items = _loc_children(root, ns)
    if kind == "sitemapindex":
        if _depth >= 1:
            return []
        cand = [(loc, to_iso(lm)) for loc, lm in items if loc]
        def rank(c):
            loc = c[0].lower()
            bad = any(b in loc for b in ("blog", "post", "news", "page", "category", "tag", "author", "article", "image", "video"))
            good = any(g in loc for g in ("tool", "site", "listing", "product", "startup", "launch", "software", "app", "project", "item", "dir", "agent", "compan"))
            return (bad, not good, "" if not c[1] else "".join(chr(255 - ord(ch)) for ch in c[1]))
        cand.sort(key=rank)
        out = []
        for loc, _ in cand[:max_children]:
            try:
                out += sitemap_urls(session, loc, max_children, max_bytes, _depth + 1)
            except Exception:
                continue
        return out
    return [(loc, to_iso(lm)) for loc, lm in items if loc]


def pick_listing_prefix(urls, fallback=True):
    """Choose the path prefix that best looks like individual listing pages.
    Pass 1: well-known listing segments (tool/site/product...). Pass 2 (fallback): the biggest
    non-blog group with >=30 urls, mostly dated, with a recent lastmod (heuristic prefix)."""
    groups = defaultdict(list)
    for loc, lm in urls:
        p = urlparse(loc)
        segs = [s for s in p.path.split("/") if s]
        if SKIP_EXT.search(p.path) or len(segs) < 2:
            continue
        groups[segs[0].lower()].append((loc, lm, len(segs)))
    best, fb = None, None
    cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    for seg, lst in groups.items():
        if seg in BAD_SEGS or len(lst) < 10:
            continue
        depth = Counter(x[2] for x in lst).most_common(1)[0][0]
        if seg in LISTING_SEGS:
            key = len(lst)
            if best is None or key > best[0]:
                best = (key, seg, depth, len(lst))
        elif len(lst) >= 30:
            dated = [x[1] for x in lst if x[1]]
            if len(dated) >= 0.5 * len(lst) and max(dated) >= cutoff and len(re.findall(r"\d", seg)) == 0:
                if fb is None or len(lst) > fb[0]:
                    fb = (len(lst), seg, depth, len(lst))
    if best:
        return best[1:]
    if fallback and fb:
        return fb[1:]
    return None


def parse_sitemap(session, url, params=None):
    params = params or {}
    urls = sitemap_urls(session, url, max_children=params.get("max_children", 3))
    prefix = params.get("prefix")
    depth = params.get("depth")
    if not prefix:
        pp = pick_listing_prefix(urls)
        if not pp:
            return []
        prefix, depth = pp[0], pp[1]
    out = []
    for loc, lm in urls:
        p = urlparse(loc)
        segs = [s for s in p.path.split("/") if s]
        if not segs or segs[0].lower() != prefix or (depth and len(segs) != depth) or SKIP_EXT.search(p.path):
            continue
        out.append(dict(name=_slug_name(loc), url=loc, tagline="", category=prefix, listed_at=lm,
                        permalink=loc))
    out.sort(key=lambda e: e["listed_at"] or "", reverse=True)
    dated = sum(1 for e in out if e["listed_at"])
    cap = params.get("cap", 300) if dated >= 0.5 * len(out) else params.get("cap_undated", 1000)
    return out[:cap]


# --------------------------------------------------------------------------- HTML list

NOISE_DOMAINS = {
    "twitter.com", "x.com", "facebook.com", "linkedin.com", "instagram.com", "youtube.com", "t.me",
    "github.com", "discord.com", "discord.gg", "reddit.com", "pinterest.com", "tiktok.com",
    "google.com", "apple.com", "play.google.com", "apps.apple.com", "producthunt.com", "medium.com",
    "wikipedia.org", "cloudflare.com", "wordpress.org", "wordpress.com", "mailto", "bit.ly",
    "buymeacoffee.com", "ko-fi.com", "paypal.com", "stripe.com", "gmpg.org", "w3.org", "schema.org",
    "fonts.googleapis.com", "creativecommons.org", "trustpilot.com", "whatsapp.com", "weibo.com",
    "bsky.app", "threads.net", "mastodon.social", "vercel.com", "netlify.com", "dmca.com",
}
GENERIC_TEXT = re.compile(r"^(visit|visit site|visit website|website|read more|more|view|view more|"
                          r"details|learn more|link|click here|here|open|go|home|next|prev|previous|"
                          r"submit|login|sign in|sign up|register|contact|about|privacy|terms)\b", re.I)
SKIP_SEG_HTML = set(BAD_SEGS) | {"tools-by", "deals", "sponsor", "advertise", "ads", "api", "static", "assets"}


def _block_text(a):
    node = a
    for _ in range(4):
        node = node.parent
        if node is None or node.name in ("body", "html", "ul", "ol", "main", "section", "table", "tbody"):
            return ""
        if node.name in ("li", "article", "tr", "div", "p"):
            txt = clean(node.get_text(" ", strip=True), 600)
            if len(txt) > len(clean(a.get_text(" ", strip=True))) + 15:
                return txt
    return ""


def analyze_html_list(html: str, page_url: str, min_links: int = 10):
    """Find the dominant repeated link pattern on a page.
    Returns dict(pattern=..., external=bool, count=n) or None."""
    soup = BeautifulSoup(html, "html.parser")
    host = domain_of(page_url)
    internal = defaultdict(dict)
    external = {}
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        full = absolutize(page_url, href)
        p = urlparse(full)
        if p.scheme not in ("http", "https"):
            continue
        d = norm_host(p.hostname or "")
        text = clean(a.get_text(" ", strip=True) or a.get("title") or a.get("aria-label") or "", 200)
        if d == host:
            segs = [s for s in p.path.split("/") if s]
            if len(segs) < 2 or SKIP_EXT.search(p.path) or segs[0].lower() in SKIP_SEG_HTML:
                continue
            internal[(segs[0], len(segs))][full] = text
        elif d and not any(d == n or d.endswith("." + n) for n in NOISE_DOMAINS) and text \
                and not GENERIC_TEXT.match(text) and len(text) <= 120:
            external.setdefault(d, (full, text))
    best = None
    for (seg, depth), links in internal.items():
        n = len(links)
        if n >= min_links:
            named = sum(1 for t in links.values() if t)
            score = n + (5 if seg.lower() in LISTING_SEGS else 0) + named * 0.1
            if not best or score > best[0]:
                best = (score, dict(pattern=f"^https?://(www\\.)?{re.escape(host)}/{re.escape(seg)}/[^/]+(/[^/]+){{{depth - 2}}}/?$"
                                    if depth > 2 else
                                    f"^https?://(www\\.)?{re.escape(host)}/{re.escape(seg)}/[^/?#]+/?$",
                                    external=False, count=n, seg=seg))
    if len(external) >= max(min_links, 12) and (not best or len(external) > best[1]["count"]):
        return dict(pattern="", external=True, count=len(external))
    return best[1] if best else None


def _container(a):
    node = a
    for _ in range(4):
        node = node.parent
        if node is None or node.name in ("body", "html", "ul", "ol", "main", "section", "table", "tbody"):
            return None
        if node.name in ("li", "article", "tr", "div", "p"):
            if len(clean(node.get_text(" ", strip=True))) > len(clean(a.get_text(" ", strip=True))) + 15:
                return node
    return None


def _better_name(a):
    c = _container(a)
    if c is None:
        return ""
    for h in c.find_all(["h1", "h2", "h3", "h4", "h5", "strong", "b"]):
        t = clean(h.get_text(" ", strip=True), 120)
        if t and not GENERIC_TEXT.match(t):
            return t
    for x in c.find_all("a"):
        t = clean(x.get_text(" ", strip=True), 120)
        if t and not GENERIC_TEXT.match(t) and len(t) >= 3:
            return t
    return ""


def html_quality(entries):
    """Reject pages that are navigation/category menus or lists of generic labels.
    Returns (ok, reason)."""
    if len(entries) < 10:
        return False, "too few entries"
    names = [e["name"].strip().lower() for e in entries]
    if len(set(names)) < 0.8 * len(names):
        return False, "duplicate/generic anchor names"
    sample = [n for n in set(names) if len(n) >= 4][:120]
    navlike = 0
    for e in entries:
        t = e["tagline"].lower()
        me = e["name"].strip().lower()
        if sum(1 for n in sample if n != me and n in t) >= 3:
            navlike += 1
    if navlike >= 0.5 * len(entries):
        return False, "looks like a navigation/category menu"
    if sum(1 for n in names if GENERIC_TEXT.match(n) or re.fullmatch(r"[\d,\s\-–]+", n)) >= 0.3 * len(names):
        return False, "generic labels"
    return True, ""


def parse_html_list(html: str, page_url: str, params: dict | None = None):
    params = params or {}
    soup = BeautifulSoup(html, "html.parser")
    host = domain_of(page_url)
    pat = re.compile(params["pattern"]) if params.get("pattern") else None
    ext = bool(params.get("external"))
    seen, out = set(), []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        full = absolutize(page_url, href)
        p = urlparse(full)
        if p.scheme not in ("http", "https"):
            continue
        d = norm_host(p.hostname or "")
        text = clean(a.get_text(" ", strip=True) or a.get("title") or a.get("aria-label") or "", 200)
        if ext:
            if d == host or not d or any(d == n or d.endswith("." + n) for n in NOISE_DOMAINS):
                continue
            if not text or GENERIC_TEXT.match(text):
                text = _better_name(a)
            if not text or GENERIC_TEXT.match(text) or len(text) > 120:
                continue
            key = d
            perma = page_url
        else:
            if not pat or not pat.search(full):
                continue
            key = norm_url(full)
            perma = full
            if not text or GENERIC_TEXT.match(text):
                text = _better_name(a) or ""
            if not text or GENERIC_TEXT.match(text):
                continue
        if key in seen:
            continue
        seen.add(key)
        blk = _block_text(a)
        tag = re.sub(r"https?://\S+|www\.\S+", " ", blk.replace(text, "", 1)) if blk else ""
        tag = re.sub(r"(?i)\b(read more|visit website|visit|view details|edit|save|latest websites added:?)\b", " ", tag)
        tag = re.sub(r"\s+", " ", tag).strip(" -–—|:")
        out.append(dict(name=text[:200], url=full, tagline=tag[:400], category="", listed_at=None,
                        permalink=perma))
    return out


# --------------------------------------------------------------------------- dispatch

def run_source(session, src: dict):
    """Fetch & parse one source (sources.yaml row). Returns entries list. Raises on failure."""
    kind, url, params = src["parser"], src["url"], src.get("params") or {}
    if kind == "sitemap":
        return parse_sitemap(session, url, params)
    r, body = fetch(session, url)
    if r.status_code != 200:
        raise RuntimeError(f"http {r.status_code}")
    if kind in ("rss", "atom"):
        return parse_feed(body, url, params)[0]
    if kind == "json_api":
        return parse_json(body, url, params)
    if kind == "html_list":
        return parse_html_list(text_of(r, body), url, params)
    raise RuntimeError(f"unknown parser {kind}")
