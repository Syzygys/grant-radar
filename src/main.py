#!/usr/bin/env python3
"""Grant Radar —— 聚合多个 Web3 grant/bounty/quest 平台的今日机会。

可作为 hackathon BUIDL / bounty 的交付物。零必需依赖（仅可选 requests）。
用法:
    python src/main.py            # 抓取并打印表格
    python src/main.py --json     # 输出 JSON
    GITHUB_TOKEN=xxx python src/main.py   # 提高 GitHub API 限额
"""
from __future__ import annotations
import json
import os
import sys

try:
    import requests
except ImportError:
    requests = None

TIMEOUT = 12
UA = {"User-Agent": "grant-radar/1.0", "Accept": "application/json"}


def fetch_ton():
    if requests is None:
        return []
    token = os.environ.get("GITHUB_TOKEN")
    h = dict(UA)
    if token:
        h["Authorization"] = f"Bearer {token}"
    try:
        repo = "ton-society/grants-and-bounties"
        meta = requests.get(f"https://api.github.com/repos/{repo}", headers=h, timeout=TIMEOUT)
        if meta.ok and meta.json().get("archived"):
            return []
        r = requests.get(f"https://api.github.com/repos/{repo}/issues",
                         params={"state": "open", "labels": "Footstep", "per_page": 10},
                         headers=h, timeout=TIMEOUT)
        r.raise_for_status()
        return [{"platform": "TON Footsteps", "name": i["title"],
                 "reward": "USDT+SBT", "url": i["html_url"]}
                for i in r.json() if "pull_request" not in i]
    except Exception:
        return []


def fetch_superteam():
    if requests is None:
        return []
    try:
        r = requests.get("https://earn.superteam.fun/api/listings",
                         params={"status": "open", "type": "bounty"},
                         headers=UA, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        items = data if isinstance(data, list) else data.get("listings", data.get("data", []))
        out = []
        for it in items[:10]:
            out.append({"platform": "Superteam", "name": it.get("title", "?"),
                        "reward": f"{it.get('rewardAmount','')} {it.get('token','USDC')}",
                        "url": it.get("url", "https://superteam.fun/earn")})
        return out
    except Exception:
        return []


SOURCES = {"TON Footsteps": fetch_ton, "Superteam Earn": fetch_superteam}


def collect():
    rows = []
    for fn in SOURCES.values():
        rows.extend(fn())
    return rows


def print_table(rows):
    if not rows:
        print("（未抓到机会：可能离线、被限流，或当前各源无开放机会）")
        return
    w = {"platform": 16, "name": 46, "reward": 18}
    print(f"{'PLATFORM':<16} {'OPPORTUNITY':<46} {'REWARD':<18} LINK")
    print("-" * 110)
    for r in rows:
        print(f"{r['platform'][:15]:<16} {r['name'][:45]:<46} "
              f"{str(r['reward'])[:17]:<18} {r['url']}")
    print(f"\n共 {len(rows)} 条机会。")


def main():
    rows = collect()
    if "--json" in sys.argv:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print_table(rows)


if __name__ == "__main__":
    main()
