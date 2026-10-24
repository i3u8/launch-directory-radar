#!/usr/bin/env python3
"""Post the daily summary to a Feishu custom-bot webhook (FEISHU_WEBHOOK_URL env / secret).

Optional FEISHU_SECRET enables signature verification. Exit code 1 if Feishu does not answer code 0.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

ROOT = Path(__file__).parent
REPO = "https://github.com/i3u8/launch-directory-radar"


def _ex(examples, k=2):
    out = []
    for x in examples[:k]:
        try:
            dom = urlparse(x["url"]).hostname or ""
        except Exception:
            dom = ""
        out.append(f"{x['name'][:32].strip()}（{dom.removeprefix('www.')}）")
    return "、".join(out)


def build(s: dict) -> str:
    L = [f"📡 每日目录雷达 {s['date']}（聚焦小词）",
         f"监控目录 {s['sources_enabled']}/{s['sources_total']}｜今日成功 {s['sources_ok']}｜失败 {s['sources_failed']}"
         + (f"｜连续失败预警 {len(s['flagged_ids'])}" if s.get("flagged_ids") else "")
         + f"｜今日新增 {s['new_today']} 条（去重 {s['new_today_unique']}）", ""]
    nt = s.get("niche_terms") or []
    if nt:
        L.append("🎯 聚焦小词 Top 10（产品数/目录数）：")
        for i, r in enumerate(nt[:10], 1):
            L.append(f"{i}. {r['term']} ×{r['count']}/{r['sources']}{' 🆕' if r.get('new') else ''} — {_ex(r['examples'])}")
    if s.get("new_terms"):
        L += ["", "🆕 新出现：" + "、".join(f"{r['term']}({r['count']})" for r in s["new_terms"][:8])]
    if s.get("clusters"):
        L += ["", "🧩 同日小簇（相似产品）："]
        L += [f"- {c['term']} ×{c['size']}：{_ex(c['examples'], 3)}" for c in s["clusters"][:3]]
    if s.get("niche_groups"):
        L += ["", "🤖 微赛道归纳：", s["niche_groups"]]
    extra = [x for x in s.get("signals", []) if x.startswith(("我们的站点", "跨目录"))]
    if extra:
        L += ["", "📌 " + "；".join(extra[:3])]
    L += ["", f"📄 日报：{s['report_url']}", f"🔗 GitHub 仓库：{s.get('repo', REPO)}"]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    ap.add_argument("--text", default="", help="send custom text instead of the day summary")
    a = ap.parse_args()
    url = os.environ.get("FEISHU_WEBHOOK_URL", "").strip()
    if not url:
        print("FEISHU_WEBHOOK_URL not set; skipping notification")
        return 0
    text = a.text or build(json.loads((ROOT / "reports" / f"{a.date}.json").read_text()))
    if REPO not in text:
        text += f"\n🔗 GitHub 仓库：{REPO}"
    body = {"msg_type": "text", "content": {"text": text}}
    secret = os.environ.get("FEISHU_SECRET", "")
    if secret:
        ts = str(int(time.time()))
        sign = base64.b64encode(hmac.new(f"{ts}\n{secret}".encode(), digestmod=hashlib.sha256).digest()).decode()
        body.update(timestamp=ts, sign=sign)
    last = None
    for attempt in range(3):
        try:
            r = requests.post(url, json=body, timeout=20)
            last = r
            j = r.json()
            if j.get("code", j.get("StatusCode")) == 0:
                print("feishu ok: code 0")
                return 0
            print(f"feishu rejected: http {r.status_code} body={r.text[:300]}")
            break  # a rejection will not fix itself
        except Exception as e:
            print(f"feishu error: {type(e).__name__}")
            time.sleep(3)
    return 1


if __name__ == "__main__":
    sys.exit(main())
