# amazon-product-due-diligence

English | [简体中文](README.zh-CN.md)

An AI skill (plus a unit-economics calculator) that runs due diligence on a candidate Amazon FBA product before you spend money on samples and inventory — and ends with a plain **GO / THINK AGAIN / DON'T**.

Works with Claude (as a Skill) and any agent that can read a Markdown instruction file. The calculator runs on its own.

## What it does

1. **Defines the product** at listing level and checks the competitors are really the same thing.
2. **Hard-stop check** — price band, platform, heavy regulation (FDA/FCC/children's products), IP and licensing risk.
3. **Scores four dimensions** with explicit thresholds:
   - **Market demand** — BSR, estimated sales, 12-month trend, return rates
   - **Competition** — review moats, concentration, price spread, 1–3-star pain points, room to differentiate
   - **Unit economics** — referral and FBA fees, COGS, freight, returns, ads, margin, markup, break-even
   - **Execution** — MOQ, weight/size tier, compliance, seasonality
4. **Flags red signals** — Amazon's own brand in the niche, patents, suspiciously cheap quotes, a flood of new listings.
5. **Gives a verdict** with the reasons, a launch checklist or the blockers to solve.
6. **Ends with a data-honesty section** — what's verified, what's estimated, what's unavailable and what it would cost to find out.

## The two rules that matter most

- **Neutral.** It says yes to a good product and no to a bad one — no manufactured doubt, no polite optimism.
- **No invented numbers.** Every figure is labeled `[verified — source @ date]`, `[est. ±N% — basis]` or `[unavailable — how to get it]`. Fees are always checked against Amazon's current schedule, never quoted from memory.

## Calculator

```bash
python3 skills/amazon-product-due-diligence/scripts/unit_economics.py \
  --price 45 --cogs 8 --fba 9.5 --referral-pct 15 \
  --freight 3 --packaging 1 --return-pct 5 --acos 25 --budget 3000
```

Prints a per-unit P&L, margin, markup (price ÷ COGS) and break-even units, rated against the skill's thresholds. Add `--json` for machine-readable output.

## Defaults you can change

The hard stops assume a lean "test small" approach: **$15–100 price band, ~$3,000 first batch, Amazon US**. Edit section 1 of `SKILL.md` (and the calculator's `--budget`) to match your strategy.

See an abridged [sample report](examples/sample-report.md).

## Install

**Claude:** copy `skills/amazon-product-due-diligence/` into `~/.claude/skills/` (or your project's `.claude/skills/`), then share the candidate with competitor links and supplier quotes:

> Is this worth selling on Amazon? Target price $45, here are 3 competitors and 2 supplier quotes.

**Other agents:** use `SKILL.md` as the instructions.

## Files

```
skills/amazon-product-due-diligence/
├── SKILL.md                   # Principles, hard stops, 9-section report, verdict rules
└── scripts/
    └── unit_economics.py      # Per-unit P&L, markup and break-even
examples/
└── sample-report.md           # Abridged example (illustrative numbers)
```

Not financial advice — a structured way to make a better-informed call.

## License

[MIT](LICENSE)
