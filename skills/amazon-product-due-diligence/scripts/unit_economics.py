#!/usr/bin/env python3
"""unit_economics.py — per-unit P&L, markup and break-even for an Amazon FBA candidate.

Usage:
    python3 unit_economics.py --price 45 --cogs 8 --fba 9.5 --referral-pct 15 \
        --freight 3 --packaging 1 --return-pct 5 --acos 25 --budget 3000

All money in USD. Fees change every year: take --fba from Amazon's current
FBA revenue calculator and --referral-pct from the current fee schedule.
Prints a table plus GO/caution/stop ratings against the skill's thresholds.
Python 3.8+, standard library only.
"""
import argparse
import json


def calc(a):
    referral = a.price * a.referral_pct / 100
    returns = a.price * a.return_pct / 100       # simple proxy: lost revenue on returned units
    ads = a.price * a.acos / 100 * a.ad_share    # ad spend per unit across all sales
    costs = {
        "Referral fee": referral,
        "FBA fulfillment fee": a.fba,
        "COGS": a.cogs,
        "Freight + inbound": a.freight,
        "Packaging / labels / inspection": a.packaging,
        "Returns and write-offs": returns,
        "Advertising": ads,
    }
    profit = a.price - sum(costs.values())
    margin = profit / a.price * 100
    markup = a.price / a.cogs if a.cogs else float("inf")
    breakeven = a.budget / profit if profit > 0 else None
    return costs, profit, margin, markup, breakeven


def rate_margin(margin, markup):
    if markup < 3:
        return "❌ markup below 3× — financially not viable"
    if margin >= 40 and markup >= 5:
        return "✅ strong"
    if margin >= 30:
        return "✅/⚠️ acceptable — depends on the other dimensions"
    if margin >= 20:
        return "⚠️ thin"
    return "❌ margin below 20%"


def main():
    ap = argparse.ArgumentParser(description="Per-unit economics for an Amazon FBA product.")
    ap.add_argument("--price", type=float, required=True, help="selling price")
    ap.add_argument("--cogs", type=float, required=True, help="unit cost from supplier (FOB)")
    ap.add_argument("--fba", type=float, required=True, help="FBA fulfillment fee per unit")
    ap.add_argument("--referral-pct", type=float, default=15, help="referral fee %% (default 15)")
    ap.add_argument("--freight", type=float, default=3, help="freight + inbound per unit (default 3)")
    ap.add_argument("--packaging", type=float, default=1, help="packaging/labels/inspection per unit (default 1)")
    ap.add_argument("--return-pct", type=float, default=5, help="return/write-off %% of price (default 5)")
    ap.add_argument("--acos", type=float, default=25, help="assumed ACoS %% on ad-driven sales (default 25)")
    ap.add_argument("--ad-share", type=float, default=1.0,
                    help="share of units sold through ads, 0–1 (default 1.0 = conservative)")
    ap.add_argument("--budget", type=float, default=3000, help="initial investment for break-even (default 3000)")
    ap.add_argument("--json", action="store_true", help="print JSON")
    a = ap.parse_args()

    costs, profit, margin, markup, breakeven = calc(a)
    if a.json:
        print(json.dumps({"costs": costs, "profit": profit, "margin_pct": margin,
                          "markup": markup, "breakeven_units": breakeven}, indent=2))
        return

    print(f"{'Line':<34}{'$':>9}{'% of price':>12}")
    print(f"{'Selling price':<34}{a.price:>9.2f}{100:>11.1f}%")
    for name, v in costs.items():
        print(f"{name:<34}{-v:>9.2f}{v / a.price * 100:>11.1f}%")
    print("-" * 55)
    print(f"{'Profit per unit':<34}{profit:>9.2f}{margin:>11.1f}%")
    print(f"\nMarkup (price ÷ COGS): {markup:.1f}×  (≥3× minimum, ≥5× ideal)")
    print("Break-even units: " + (f"{breakeven:,.0f} on a ${a.budget:,.0f} budget" if breakeven
                                  else "never — profit per unit is zero or negative"))
    print(f"Rating: {rate_margin(margin, markup)}")
    print("\nReminder: fees and ACoS are inputs, not facts. Label them verified or estimated in the report.")


if __name__ == "__main__":
    main()
