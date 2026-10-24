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

import requests

ROOT = Path(__file__).parent
REPO = "https://github.com/i3u8/launch-directory-radar"


def build(s: dict) -> str:
    L = [f"📡 每日目录雷达 {s['date']}",
         f"监控目录 {s['sources_enabled']}/{s['sources_total']}｜今日成功 {s['sources_ok']}｜失败 {s['sources_failed']}"
         + (f"｜连续失败预警 {len(s['flagged_ids'])}" if s.get("flagged_ids") else ""),
         f"今日新增 {s['new_today']} 条（去重 {s['new_today_unique']}）｜AI 占比 {s.get('ai_share_today')}", ""]
    if s["top_terms"]:
        L.append("🔥 Top10 热词：" + "、".join(f"{t}({c}){'↑' if up else ''}" for t, c, up in s["top_terms"]))
    if s["top_bigrams"]:
        L.append("🔤 热门双词：" + "、".join(f"{t}({c})" for t, c in s["top_bigrams"][:6]))
    if s["rising"]:
        L.append("📈 升温：" + "、".join(f"{t}({c})" for t, c, _ in s["rising"][:6]))
    if s["signals"]:
        L.append("")
        L.append("🎯 信号：")
        L += [f"{i}. {x}" for i, x in enumerate(s["signals"][:5], 1)]
    if s.get("digest"):
        L += ["", f"🤖 摘要：{s['digest']}"]
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
