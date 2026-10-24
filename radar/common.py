"""Shared helpers: HTTP session with retries, URL normalisation, date parsing."""
from __future__ import annotations

import html
import re
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode, urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

REPO_URL = "https://github.com/i3u8/launch-directory-radar"
UA = f"Mozilla/5.0 (compatible; LaunchDirectoryRadar/1.0; +{REPO_URL})"
TIMEOUT = (6, 15)
MAX_BYTES = 6_000_000

TRACKING = re.compile(r"^(utm_.*|ref|ref_src|source|fbclid|gclid|mc_.*|via)$", re.I)


def make_session(retries: int = 2) -> requests.Session:
    s = requests.Session()
    retry = Retry(
        total=retries, connect=retries, read=retries, status=retries,
        backoff_factor=1.0, status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET", "HEAD"), respect_retry_after_header=True,
    )
    ad = HTTPAdapter(max_retries=retry, pool_connections=8, pool_maxsize=8)
    s.mount("https://", ad)
    s.mount("http://", ad)
    s.headers.update({"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en,zh;q=0.8"})
    return s


def fetch(s: requests.Session, url: str, timeout=TIMEOUT, max_bytes: int = MAX_BYTES):
    """GET with a size cap. Returns (response, bytes) ; raises on network error."""
    r = s.get(url, timeout=timeout, stream=True, allow_redirects=True)
    buf = bytearray()
    try:
        for chunk in r.iter_content(65536):
            buf.extend(chunk)
            if len(buf) > max_bytes:
                break
    finally:
        r.close()
    return r, bytes(buf)


def text_of(r, body: bytes) -> str:
    enc = r.encoding if (r.encoding and "charset" in r.headers.get("content-type", "").lower()) else "utf-8"
    try:
        return body.decode(enc, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


def norm_host(host: str) -> str:
    host = (host or "").lower().strip().rstrip(".")
    return host[4:] if host.startswith("www.") else host


def norm_url(url: str) -> str:
    """Canonical form: https scheme kept as-is, host lowercased w/o www, no fragment,
    no tracking params, no trailing slash on bare paths."""
    if not url:
        return ""
    url = url.strip()
    if not re.match(r"^[a-z][a-z0-9+.-]*://", url, re.I):
        url = "https://" + url.lstrip("/")
    p = urlparse(url)
    if p.scheme not in ("http", "https") or not p.netloc:
        return ""
    q = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True) if not TRACKING.match(k)]
    path = p.path or "/"
    if path != "/":
        path = path.rstrip("/") or "/"
    return urlunparse(("https", norm_host(p.hostname or "") + (f":{p.port}" if p.port else ""),
                       path, "", urlencode(q), ""))


def domain_of(url: str) -> str:
    try:
        return norm_host(urlparse(url).hostname or "")
    except Exception:
        return ""


def to_iso(v) -> str | None:
    """Parse many date formats into ISO-8601 UTC string, or None."""
    if v is None or v == "":
        return None
    try:
        if isinstance(v, (int, float)):
            if v > 1e12:
                v /= 1000.0
            if v < 1e8:
                return None
            return datetime.fromtimestamp(v, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if isinstance(v, time.struct_time):
            return datetime(*v[:6], tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        s = str(v).strip()
        if re.fullmatch(r"\d{9,13}", s):
            return to_iso(int(s))
        try:
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            dt = parsedate_to_datetime(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None


def clean(s, n: int = 300) -> str:
    if s is None:
        return ""
    if isinstance(s, (list, tuple)):
        s = ", ".join(str(x.get("name", x)) if isinstance(x, dict) else str(x) for x in s)
    s = re.sub(r"<[^>]+>", " ", str(s))
    s = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", " ", s)  # never store third-party emails
    s = html.unescape(s).replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s[:n]


def absolutize(base: str, href: str) -> str:
    return urljoin(base, href)
