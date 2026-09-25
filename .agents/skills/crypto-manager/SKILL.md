---
name: crypto-manager
description: >-
  Automated review and discipline manager for personal crypto portfolio following
  crypto-plan.md and AGENTS.md rules. Activates when user asks to review crypto portfolio,
  evaluate 540tr hard floor, calculate Total Net Worth (TTS), check missed recommendations,
  run daily or weekly portfolio review, or generate Binance 10-minute exit order sheets.
allowed-tools: Bash(python3 *), Bash(curl *), view_file, write_to_file, replace_file_content
metadata:
  author: Teamwork Crypto Dashboard
  version: "1.1.0"
  requires:
    runtime: "Python 3.10+, curl, agy CLI 1.2.9+"
  permissions:
    - "Network read access for Binance Spot and P2P ticker APIs"
    - "Filesystem read access to /Users/thien.tm/Documents/me/crypto/"
    - "Filesystem append-only write access to /Users/thien.tm/Documents/me/crypto/logs/"
---

# Crypto Portfolio Manager (`crypto-manager`)

Automates portfolio valuation, binary matrix evaluation (540tr hard floor), execution audit (0/13 missed orders warning), and standardized Section 7.5 reviews for the personal crypto portfolio.

## Inviolable Rules (AGENTS.md & crypto-plan.md)

1. **Append-Only Logs (`AGENTS.md`)**:
   - NEVER modify or delete existing entries in `/Users/thien.tm/Documents/me/crypto/logs/*.md`.
   - All reviews must be appended with an ISO date header (`## YYYY-MM-DD: ...`).
2. **Three Inviolable Principles**:
   - NEVER recommend injecting new capital (tuyệt đối không nạp thêm vốn) into crypto.
   - NEVER recommend buying back / DCA to recover losses.
   - NEVER extend the exit deadline beyond Late October 2026 (2026-10-31).
3. **Three Agent Prohibitions**:
   - DO NOT use price forecasts to reduce tranche size or delay selling.
   - DO NOT repeat unexecuted recommendations without highlighting them at the very top (0/13 missed orders audit).
   - DO NOT propose new thresholds or rules when existing rules remain unexecuted.

## Authoritative Parameters (2026-09-24 Critical Update)
- **Hard Floor (Sàn cứng)**: `540,000,000 VND`
- **Take-Profit Trigger**: `TTS >= 540,000,000 VND`
- **Cash-out Deadline**: Late October 2026 (`2026-10-31`)
- **Measured Holdings** (from `crypto-plan.md`):
  * BTC: `0.15931`
  * SOL: `55.28`
  * Stables: `$1,415.00`
- **BĐS Target**:
  * Total Land Sổ Đỏ Cost: `3,100,000,000 VND`
  * Planned Loan Gap: `615,000,000 VND`
  * Self-funded Cash: Parents (`1,300,000,000 VND`) + Personal (`705,000,000 VND`)

## Execution Procedure

### Method A: Automated Execution via Helper Script (Recommended)
Run the bundled helper script to compute live rates, evaluate the binary matrix, and optionally append the review log:

```bash
# 1. Quick review preview in terminal
python3 skills/crypto-manager/scripts/run_review.py

# 2. Output structured JSON for downstream tools
python3 skills/crypto-manager/scripts/run_review.py --json

# 3. Append standardized review directly to the active log file
python3 skills/crypto-manager/scripts/run_review.py --append
```

### Method B: Autonomous Agent Execution (Manual Step-by-Step)

If running in pure reasoning mode without executing scripts:

#### Step 1: Read Portfolio State
- Read `/Users/thien.tm/Documents/me/crypto/crypto-plan.md` Section 2 for holdings.
- Read `/Users/thien.tm/Documents/me/crypto/logs/{YYYY-MM}.md` to audit unexecuted orders and cashout progress.

#### Step 2: Fetch Live Market Rates
Execute curl to fetch live Binance spot and P2P SELL prices:
```bash
# Binance Spot
curl -s "https://api.binance.com/api/v3/ticker/price?symbols=%5B%22BTCUSDT%22,%22SOLUSDT%22%5D"

# Binance P2P USDT/VND SELL rate
curl -s -X POST -H "Content-Type: application/json" -H "User-Agent: Mozilla/5.0" \
  -d '{"page":1,"rows":5,"payTypes":[],"asset":"USDT","tradeType":"SELL","fiat":"VND","transAmount":"50000000"}' \
  https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search
```

#### Step 3: Compute Valuation & Distance to Floor
- `TTS (VND) = VND_withdrawn + (BTC_qty * BTC_price + SOL_qty * SOL_price + Stables_USD) * P2P_rate`
- `Distance to Floor (VND) = TTS - 540,000,000`

#### Step 4: Binary Decision Matrix Evaluation
1. **If TTS >= 540,000,000 VND**:
   - Status: `TAKE_PROFIT_540M` ("Lời bất ngờ")
   - Action: Kích hoạt Take-profit 50% NGAY LẬP TỨC ngoài lịch.
   - Priority Execution:
     1. Rút 100% Stables ra VND qua P2P.
     2. Bán SẠCH 100% SOL (55.28 SOL) ra USDT rồi rút VND (SOL rủi ro cao, SOL/BTC đỉnh).
     3. Bán thêm BTC ra USDT để tổng giá trị bán đạt đúng 50% coin.
     4. Đặt lệnh Stop-Market GTC cho lượng BTC còn lại.
2. **If TTS < 540,000,000 VND**:
   - Status: `HARD_FLOOR_BREACH` ("EMERGENCY THỦNG SÀN")
   - Action: EMERGENCY! Market Sell ALL ra VND ngay lập tức! Bán toàn bộ BTC, SOL, rút toàn bộ Stables ra VND trong 24 giờ.

#### Step 5: Format Section 7.5 Review & Append to Log
Write or append to `/Users/thien.tm/Documents/me/crypto/logs/{YYYY-MM}.md` following Section 7.5 standard format.
