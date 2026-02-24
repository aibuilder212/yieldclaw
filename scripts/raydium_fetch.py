"""
raydium_fetch.py - YieldClaw Raydium LP Scanner
Fetches top pools from Raydium API v3 and filters by APY/TVL thresholds.

Usage:
    python raydium_fetch.py          # Full scan, print results
    python raydium_fetch.py --test   # Single test scan, verbose output
"""

import os
import sys
import json
import math
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Config from .env
RAYDIUM_API_BASE = os.getenv("RAYDIUM_API_BASE", "https://api.raydium.io/v3")
MIN_APY = float(os.getenv("MIN_APY_THRESHOLD", 5))
MIN_TVL = float(os.getenv("MIN_TVL_USD", 10000))
IL_THRESHOLD = float(os.getenv("IL_WARNING_THRESHOLD", 3))


def fetch_pools(page_size=50, sort_field="apr", sort_type="desc"):
    """Fetch top pools from Raydium API v3"""
    url = f"{RAYDIUM_API_BASE}/pools/info/list"
    params = {
        "poolType": "all",
        "sortField": sort_field,
        "sortType": sort_type,
        "pageSize": page_size,
        "page": 1
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("data", [])
    except requests.RequestException as e:
        print(f"[ERROR] Raydium API fetch failed: {e}")
        return []


def calculate_il(price_ratio):
    """
    Calculate impermanent loss given a price ratio change.
    price_ratio = current_price / entry_price
    Returns IL as a percentage (negative = loss)
    """
    if price_ratio <= 0:
        return -100.0
    il = (2 * math.sqrt(price_ratio) / (1 + price_ratio)) - 1
    return round(il * 100, 2)


def filter_pools(pools):
    """Filter pools by APY and TVL thresholds"""
    filtered = []
    for pool in pools:
        try:
            apy = float(pool.get("apr", {}).get("apr", 0) or 0)
            tvl = float(pool.get("tvl", 0) or 0)
            if apy >= MIN_APY and tvl >= MIN_TVL:
                filtered.append({
                    "pool_id": pool.get("id", ""),
                    "token_a": pool.get("mintA", {}).get("symbol", "?"),
                    "token_b": pool.get("mintB", {}).get("symbol", "?"),
                    "apy": round(apy, 2),
                    "tvl": round(tvl, 2),
                    "fee_24h": pool.get("feeApr", 0),
                    "volume_24h": pool.get("day", {}).get("volume", 0),
                    "pool_type": pool.get("type", "unknown"),
                    "scanned_at": datetime.utcnow().isoformat()
                })
        except (ValueError, TypeError, AttributeError):
            continue
    return filtered


def format_output(pools):
    """Print a clean summary of filtered pools"""
    print(f"\n{'='*60}")
    print(f"YieldClaw Scan | {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*60}")
    print(f"Pools scanned: passing APY>{MIN_APY}% + TVL>${MIN_TVL:,.0f}")
    print(f"Results: {len(pools)} pools found")
    print(f"{'-'*60}")
    for i, p in enumerate(pools[:10], 1):  # Top 10
        print(f"{i:2}. {p['token_a']}/{p['token_b']}")
        print(f"    APY: {p['apy']}% | TVL: ${p['tvl']:,.0f} | Type: {p['pool_type']}")
    print(f"{'='*60}\n")


def main():
    test_mode = "--test" in sys.argv
    if test_mode:
        print("[YieldClaw] Running in TEST mode...")

    print(f"[YieldClaw] Fetching Raydium pools from {RAYDIUM_API_BASE}...")
    raw_pools = fetch_pools(page_size=100 if not test_mode else 20)

    if not raw_pools:
        print("[YieldClaw] No pools returned. Check API or network.")
        sys.exit(1)

    print(f"[YieldClaw] Fetched {len(raw_pools)} raw pools. Filtering...")
    filtered = filter_pools(raw_pools)

    format_output(filtered)

    # Output JSON for n8n to consume (stdout)
    print(json.dumps(filtered, indent=2))


if __name__ == "__main__":
    main()
