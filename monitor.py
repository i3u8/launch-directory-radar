#!/usr/bin/env python3
"""Collect new entries from every enabled source in sources.yaml.

Writes: data/entries.jsonl (append-only, dedup by (source, url)), data/daily/YYYY-MM-DD.json,
        data/health.json (per-source health). Each source fails independently.
"""
from __future__ import annotations

import argparse
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

from radar.common import domain_of, make_session, norm_url
from radar.parsers import run_source

ROOT = Path(__file__).parent
DATA = ROOT / "data"
FRESH_HOURS = 36        # first run of a source: entries newer than this count as "new today"
BACKFILL_DAYS = 30      # first run: dated entries within this window seed the trailing baselines
BULK_SITEMAP = 100      # a sitemap yielding more new URLs than this in one run = bulk lastmod change
DAILY_KEEP_DAYS = 60
FAIL_FLAG_DAYS = 3
local = threading.local()


def session():
    if not hasattr(local, "s"):
        local.s = make_session(retries=2)
    return local.s


def load_seen():
    seen = set()
    p = DATA / "entries.jsonl"
    if p.exists():
        for line in p.open(encoding="utf-8"):
            try:
                e = json.loads(line)
                seen.add((e["source"], e["url"]))
            except Exception:
                continue
    return seen


def baseline(e):
    """Compact record: only enough to dedupe future runs."""
    return dict(source=e["source"], url=e["url"], first_seen=e["first_seen"], baseline=True)


def collect(src):
    t0 = time.time()
    try:
        entries = run_source(session(), src)
        if not entries:
            raise RuntimeError("0 entries parsed")
        return src, entries, None, time.time() - t0
    except Exception as e:
        return src, [], f"{type(e).__name__}: {e}"[:200], time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    today = a.date
    now = datetime.now(timezone.utc)
    DATA.mkdir(exist_ok=True)
    (DATA / "daily").mkdir(exist_ok=True)
    sources = [s for s in yaml.safe_load((ROOT / "sources.yaml").read_text())["sources"] if s.get("enabled")]
    if a.only:
        sources = [s for s in sources if s["id"] in a.only.split(",")]
    health_p = DATA / "health.json"
    health = json.loads(health_p.read_text()) if health_p.exists() else {}
    seen = load_seen()
    daily_p = DATA / "daily" / f"{today}.json"
    daily = json.loads(daily_p.read_text()) if daily_p.exists() else {"date": today, "new": [], "sources": {}}
    new_out, run_stats = [], {}

    with ThreadPoolExecutor(a.workers) as ex:
        futs = [ex.submit(collect, s) for s in sources]
        results = [f.result() for f in as_completed(futs)]
    results.sort(key=lambda r: r[0]["id"])

    fresh_cut = (now - timedelta(hours=FRESH_HOURS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    back_cut = (now - timedelta(days=BACKFILL_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    for src, entries, err, dt in results:
        sid = src["id"]
        h = health.setdefault(sid, dict(domain=src["domain"], kind=src["kind"], seeded=False,
                                        consecutive_failures=0, last_ok=None, last_run=None))
        h.update(domain=src["domain"], kind=src["kind"], url=src["url"])
        if err is None:
            h["consecutive_failures"] = 0
        elif h.get("last_run") != today:  # count one failure per calendar day
            h["consecutive_failures"] += 1
        h["last_run"] = today
        h["last_error"] = err
        h["elapsed_s"] = round(dt, 1)
        h["flagged"] = h["consecutive_failures"] >= FAIL_FLAG_DAYS
        if err is not None:
            print(f"[FAIL] {sid}: {err}", file=sys.stderr)
            h["last_count"] = 0
            continue
        h["last_ok"] = today
        h["last_count"] = len(entries)
        first_run = not h.get("seeded")
        fresh = []
        for e in entries:
            key = norm_url(e["url"]) if src["parser"] != "sitemap" else e["url"]
            if not key or (sid, key) in seen:
                continue
            la = e["listed_at"]
            if la and la > now.strftime("%Y-%m-%dT%H:%M:%SZ"):
                la = None  # future-dated lastmod: ignore
            rec = dict(source=sid, name=e["name"], url=key, tagline=e["tagline"], category=e["category"],
                       listed_at=la, first_seen=today)
            if e["permalink"] and norm_url(e["permalink"]) != key:
                rec["permalink"] = e["permalink"]
            e = rec
            fresh.append(e)
        for e in fresh:
            seen.add((sid, e["url"]))
        n_fresh = sum(1 for e in fresh if e["listed_at"] and e["listed_at"] >= fresh_cut) if first_run else len(fresh)
        if src["parser"] == "sitemap" and n_fresh > BULK_SITEMAP:
            hist = [baseline(e) for e in fresh]
            new_today = []
            print(f"[bulk] {sid}: {n_fresh} new sitemap urls in one run (bulk lastmod) -> baseline", file=sys.stderr)
        elif first_run:
            new_today, hist = [], []
            for e in fresh:
                la = e["listed_at"]
                if la and la >= fresh_cut:
                    new_today.append(e)
                elif la and la >= back_cut:
                    e["day"] = la[:10]
                    e["backfill"] = True
                    hist.append(e)
                else:
                    hist.append(baseline(e))
        else:
            new_today, hist = fresh, []
        h["seeded"] = True
        for e in new_today:
            e["day"] = today
        new_out += new_today
        run_stats[sid] = dict(new=len(new_today), total=len(entries))
        with (DATA / "entries.jsonl").open("a", encoding="utf-8") as f:
            for e in new_today + hist:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")

    # merge into the day's file (idempotent for same-day reruns)
    daily["new"] += new_out
    for sid, st in run_stats.items():
        prev = daily["sources"].get(sid, {"new": 0})
        daily["sources"][sid] = dict(new=prev["new"] + st["new"], total=st["total"])
    for sid in {r[0]["id"] for r in results if r[2]}:
        daily["sources"].setdefault(sid, dict(new=0, total=0, failed=True))
    daily_p.write_text(json.dumps(daily, ensure_ascii=False, indent=0))
    health_p.write_text(json.dumps(health, ensure_ascii=False, indent=1, sort_keys=True))
    # trim old daily files
    cut = (now - timedelta(days=DAILY_KEEP_DAYS)).strftime("%Y-%m-%d")
    for f in (DATA / "daily").glob("*.json"):
        if f.stem < cut:
            f.unlink()
    ok = sum(1 for r in results if r[2] is None)
    print(f"sources={len(results)} ok={ok} failed={len(results)-ok} new_today={len(new_out)}")


if __name__ == "__main__":
    main()
