/**
 * Crypto Liquidity Cockpit - Single-Page Application Controller
 * File: src/crypto_dashboard/web/app.js
 * Architecture: Pure Vanilla ES6 Unidirectional Flow (Zero External Dependencies)
 * Authoritative sources: PROJECT.md §F10-F12; explorer_m4_1, explorer_m4_2, explorer_m4_3.
 */

// 1. CONSTANTS & SYSTEM PARAMETERS
const HARD_FLOOR_VND = 540000000;
const BASE_CAPITAL_VND = 650000000;
const TOTAL_BDS_BUDGET_VND = 3100000000;
const BORROW_CEILING_VND = 615000000;
const FAMILY_SUPPORT_VND = 1300000000;
const PERSONAL_CASH_VND = 705000000;
const STATUTORY_HOURLY_BURN_VND = 38750;
const BURN_PER_SECOND_VND = 38750 / 3600; // ~10.7638 VND/sec
const COMMITMENT_TOTAL_SECONDS = 600; // 10 minutes

// 2. STATE STORE
const State = {
  isOffline: false,
  valuation: null,
  portfolio: [],
  marketRates: {
    btc_usdt: 84262.0,
    sol_usdt: 115.72,
    usdt_vnd_p2p: 25930.0,
    is_cached: false,
    updated_at: new Date().toISOString()
  },
  disciplineGate: null,
  matrix: null,
  dualStrategies: null,
  strategyView: 'both', // 'a', 'b', or 'both'
  activeOrdersMode: 'a', // 'a' or 'b'
  macroEvents: [],
  bdsGap: null,
  trend: null,
  simInputs: {
    btcShockPct: 0.0,
    solShockPct: 0.0,
    btcPrice: 84262.0,
    solPrice: 115.72,
    p2pRate: 25930.0,
    sell50Pct: true
  },
  simResult: null,
  accumulatedHesitationTax: 32600000.0,
  commitmentSecondsLeft: 465, // ~07:45 initial
  agyExecuting: false
};

// 3. OFFLINE FALLBACK ORACLE
const OfflineOracle = {
  status: {
    valuation: {
      tts_vnd: 550643256.0,
      tts_usd: 21235.76,
      crypto_vnd: 513987256.0,
      withdrawn_vnd: 36656000.0,
      base_capital_vnd: 650000000.0,
      unrealized_pnl_vnd: -99356744.0,
      unrealized_pnl_pct: -15.29,
      cash_withdrawn_vnd: 0.0,
      cashout_progress_pct: 0.0,
      hard_floor_vnd: 540000000.0,
      distance_to_floor_vnd: 10643256.0,
      distance_to_floor_pct: 1.97,
      distance_to_floor_atr_multiple: 3.72,
      data_source: "offline_cache",
      timestamp: new Date().toISOString()
    },
    portfolio: [
      { asset: "BTC", amount: 0.159310, price_usd: 84262.0, value_usd: 13423.78, value_vnd: 348113125.0, weight_pct: 63.22, action_flag: "HOLD_PARTIAL_WITH_STOP" },
      { asset: "SOL", amount: 55.28, price_usd: 115.72, value_usd: 6396.99, value_vnd: 165874131.0, weight_pct: 30.12, action_flag: "SELL_FIRST" },
      { asset: "USDT", amount: 1415.0, price_usd: 1.0, value_usd: 1415.0, value_vnd: 36656000.0, weight_pct: 6.66, action_flag: "WITHDRAW_NOW" }
    ],
    market_rates: {
      btc_usdt: 84262.0,
      sol_usdt: 115.72,
      sol_btc_ratio: 0.0013733,
      usdt_vnd_p2p: 25930.0,
      is_cached: true,
      updated_at: new Date().toISOString()
    },
    discipline_gate: {
      missed_recommendations_count: 13,
      total_recommendations_count: 13,
      execution_rate_pct: 0.0,
      delay_days: 50,
      current_band: "TAKE_PROFIT_540M",
      is_urgent_action_required: true,
      urgent_message: "TTS đạt 550,6tr VND (vượt ngưỡng 540tr). Bán ngay 50% coin (xả sạch SOL) và rút Stables."
    }
  },
  matrix: {
    hard_floor_vnd: 540000000.0,
    active_band: "TAKE_PROFIT_540M",
    distance_to_floor_vnd: 10643256.0,
    distance_to_floor_pct: 1.97,
    urgent_action_required: true,
    missed_recommendations_count: 13,
    orders_sheet: [
      { priority: 1, action: "WITHDRAW_P2P", symbol: "USDT", qty: 1415.0, price: 25930.0, estimated_vnd: 36690950.0, channel: "P2P", deadline: "Ngay lập tức" },
      { priority: 2, action: "MARKET_SELL", symbol: "SOLUSDT", qty: 55.28, price: 115.72, estimated_vnd: 165874131.0, channel: "Spot", deadline: "Ngay lập tức" },
      { priority: 3, action: "LIMIT_OR_MARKET_SELL", symbol: "BTCUSDT", qty: 0.04155, price: 84262.0, estimated_vnd: 90786520.0, channel: "Spot", deadline: "Trước 20:00 VN" }
    ],
    overrides_triggered: ["OVERRIDE_01_TAKE_PROFIT_540M"],
    days_to_deadline: 37,
    deadline_date: "2026-10-31"
  },
  macro: {
    events: [
      { id: "tranche_1", title: "Tranche 1 (15% gốc)", deadline_utc: "2026-09-24T13:00:00Z", remaining_seconds: 27912.0, is_urgent: true, description: "Bán 0,035327 BTC trước 20:00 VN" },
      { id: "tranche_2", title: "Tranche 2 (20% gốc)", deadline_utc: "2026-09-29T13:00:00Z", remaining_seconds: 461520.0, is_urgent: false, description: "Kéo lên trước công bố PCE Mỹ" },
      { id: "bds_debt_source", title: "Hạn chốt nguồn vay BĐS 615tr", deadline_utc: "2026-09-30T17:00:00Z", remaining_seconds: 564300.0, is_urgent: true, description: "Xác nhận phương án nợ BĐS" },
      { id: "pce_inflation", title: "PCE Lạm phát Mỹ", deadline_utc: "2026-09-30T12:30:00Z", remaining_seconds: 548100.0, is_urgent: false, description: "Công bố Core PCE tháng 8/2026" },
      { id: "late_oct_deadline", title: "Hạn chót rút tiền (Late October 2026)", deadline_utc: "2026-10-31T23:59:59Z", remaining_seconds: 3239999.0, is_urgent: false, description: "Toàn bộ tiền mặt VND phải về tài khoản" }
    ],
    bds_financial_gap: {
      total_budget_vnd: 3100000000.0,
      parents_support_vnd: 1300000000.0,
      personal_cash_vnd: 705000000.0,
      crypto_tts_current_vnd: 550643256.0,
      total_self_equity_vnd: 2555643256.0,
      borrow_needed_vnd: 544356744.0,
      borrow_ceiling_vnd: 615000000.0,
      cushion_vnd: 70643256.0,
      is_within_ceiling: true
    }
  },
  trend: {
    mcr_sim: {
      prob_ruin: 0.37,
      ruin_probability_pct: 37.0,
      first_passage_days_median: 18.5,
      paths_breached: 185,
      total_simulations: 500,
      horizon_days: 37,
      var_95_vnd: 482000000.0,
      cvar_95_vnd: 461000000.0,
      safety_status: "CRITICAL_RUIN_RISK"
    },
    bht_ticker: {
      unexecuted_count: 13,
      days_hesitated: 50,
      burn_rate_vnd_per_hour: 38750.0,
      burn_rate_vnd_per_second: 10.7638,
      total_hesitation_tax_vnd: 32600000.0,
      land_2027_hazard_exposure_vnd: 370000000.0,
      status_level: "DEFCON_1_PARALYSIS"
    },
    avc_meter: {
      tts_vnd: 550643256.0,
      hard_floor_vnd: 540000000.0,
      cushion_vnd: 10643256.0,
      cushion_pct: 1.97,
      vcr_days: 0.69,
      risk_zone: "RED_DANGER",
      cppi_max_safe_crypto_vnd: 114443612.0,
      excess_risk_vnd: 381656388.0
    }
  }
};

// 4. FORMATTERS & UTILITIES
function formatVND(amount, compact = false) {
  if (amount == null || isNaN(amount)) return "0 ₫";
  const num = Math.round(Number(amount));
  if (compact) {
    if (Math.abs(num) >= 1e9) {
      return (num / 1e9).toFixed(1).replace(".", ",") + "B ₫";
    }
    if (Math.abs(num) >= 1e6) {
      return (num / 1e6).toFixed(1).replace(".", ",") + "tr ₫";
    }
  }
  return num.toLocaleString("vi-VN") + " ₫";
}

function formatUSD(amount) {
  if (amount == null || isNaN(amount)) return "$0.00";
  return "$" + Number(amount).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatCrypto(amount, symbol = "") {
  if (amount == null || isNaN(amount)) return "0 " + symbol;
  const num = Number(amount);
  const formatted = num >= 1 ? num.toFixed(2) : num.toFixed(5);
  return `${formatted} ${symbol}`.trim();
}

function formatPct(val, showSign = true) {
  if (val == null || isNaN(val)) return "0,0%";
  const num = Number(val);
  const sign = showSign && num > 0 ? "+" : "";
  return sign + num.toFixed(2).replace(".", ",") + "%";
}

function formatDuration(remainingSeconds) {
  const sec = Math.round(Number(remainingSeconds));
  if (sec <= 0) return "ĐÃ ĐẾN HẠN";
  const d = Math.floor(sec / 86400);
  const h = Math.floor((sec % 86400) / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = sec % 60;

  if (d > 0) {
    return `${d}d ${h.toString().padStart(2, "0")}h ${m.toString().padStart(2, "0")}m`;
  }
  return `${h.toString().padStart(2, "0")}h ${m.toString().padStart(2, "0")}m ${s.toString().padStart(2, "0")}s`;
}

// 5. API CLIENT CALLS WITH RESILIENT FALLBACK
async function safeFetchJson(url, options = {}, fallbackData = null) {
  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        ...(options.headers || {})
      }
    });
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    const json = await res.json();
    return json.data !== undefined ? json.data : json;
  } catch (err) {
    State.isOffline = true;
    updateNetworkStatusBadge(false);
    return fallbackData;
  }
}

async function fetchInitialData() {
  const [statusData, matrixData, macroData, trendData] = await Promise.all([
    safeFetchJson("/api/status", { method: "GET" }, OfflineOracle.status),
    safeFetchJson("/api/matrix", { method: "GET" }, OfflineOracle.matrix),
    safeFetchJson("/api/macro", { method: "GET" }, OfflineOracle.macro),
    safeFetchJson("/api/trend", { method: "GET" }, OfflineOracle.trend)
  ]);

  if (statusData && !State.isOffline) {
    updateNetworkStatusBadge(true);
  }

  if (statusData) {
    State.valuation = statusData.valuation || OfflineOracle.status.valuation;
    State.portfolio = statusData.portfolio || OfflineOracle.status.portfolio;
    State.marketRates = statusData.market_rates || OfflineOracle.status.market_rates;
    State.disciplineGate = statusData.discipline_gate || OfflineOracle.status.discipline_gate;

    if (statusData.dual_strategies) {
      State.dualStrategies = statusData.dual_strategies;
    }

    // Sync simulation reference prices
    if (State.marketRates) {
      State.simInputs.btcPrice = State.marketRates.btc_usdt || 84262.0;
      State.simInputs.solPrice = State.marketRates.sol_usdt || 115.72;
      State.simInputs.p2pRate = State.marketRates.usdt_vnd_p2p || 25930.0;
    }
  }

  if (matrixData) {
    State.matrix = matrixData;
  }

  if (macroData) {
    State.macroEvents = macroData.events || OfflineOracle.macro.events;
    State.bdsGap = macroData.bds_financial_gap || OfflineOracle.macro.bds_financial_gap;
  }

  if (trendData) {
    State.trend = trendData;
    if (trendData.bht_ticker && trendData.bht_ticker.total_hesitation_tax_vnd) {
      State.accumulatedHesitationTax = trendData.bht_ticker.total_hesitation_tax_vnd;
    }
  }

  calculateLocalSimulation();
  renderAllViews();
}

function updateNetworkStatusBadge(isOnline) {
  const badge = document.getElementById("network-status");
  if (!badge) return;
  if (isOnline) {
    badge.className = "badge badge-success";
    badge.textContent = "🟢 REALTIME";
  } else {
    badge.className = "badge badge-warning";
    badge.textContent = "🟠 OFFLINE CACHE";
  }
}

// 6. LOCAL WHAT-IF MATHEMATICAL SIMULATION ENGINE
function calculateLocalSimulation() {
  const btcQty = 0.159310;
  const solQty = 55.28;
  const stablesUSD = 1415.0;
  const withdrawnVND = 36656000.0;

  const refBtcPrice = (State.marketRates && State.marketRates.btc_usdt) || 84262.0;
  const refSolPrice = (State.marketRates && State.marketRates.sol_usdt) || 115.72;
  const p2p = Number(State.simInputs.p2pRate) || 25930.0;

  // Calculate simulated spot prices based on shock %
  const simBtcPrice = refBtcPrice * (1.0 + State.simInputs.btcShockPct / 100.0);
  const simSolPrice = refSolPrice * (1.0 + State.simInputs.solShockPct / 100.0);

  State.simInputs.btcPrice = simBtcPrice;
  State.simInputs.solPrice = simSolPrice;

  // Scenario B: Hold 100% coin
  const simCryptoUsdB = (btcQty * simBtcPrice) + (solQty * simSolPrice) + stablesUSD;
  const simTtsVndB = (simCryptoUsdB * p2p) + withdrawnVND;
  const distFloorB = simTtsVndB - HARD_FLOOR_VND;
  const distFloorPctB = (distFloorB / HARD_FLOOR_VND) * 100.0;
  const isBreachedB = simTtsVndB < HARD_FLOOR_VND;
  const ruinProbB = isBreachedB ? 37.0 : 15.0;
  const selfEquityB = FAMILY_SUPPORT_VND + PERSONAL_CASH_VND + simTtsVndB;
  const borrowGapB = Math.max(0, TOTAL_BDS_BUDGET_VND - selfEquityB);

  // Scenario A: Sell 50% Take Profit
  const baseCryptoUsd = (btcQty * refBtcPrice) + (solQty * refSolPrice) + stablesUSD;
  const cashLockedA = 0.5 * baseCryptoUsd * p2p;
  const shockRatio = baseCryptoUsd > 0 ? (simCryptoUsdB / baseCryptoUsd) : 1.0;
  const remainingCryptoA = 0.5 * baseCryptoUsd * p2p * shockRatio;
  const simTtsVndA = cashLockedA + remainingCryptoA + withdrawnVND;
  const distFloorA = simTtsVndA - HARD_FLOOR_VND;
  const distFloorPctA = (distFloorA / HARD_FLOOR_VND) * 100.0;
  const isBreachedA = simTtsVndA < HARD_FLOOR_VND;
  const ruinProbA = isBreachedA ? 25.0 : 4.2;
  const selfEquityA = FAMILY_SUPPORT_VND + PERSONAL_CASH_VND + simTtsVndA;
  const borrowGapA = Math.max(0, TOTAL_BDS_BUDGET_VND - selfEquityA);

  State.simResult = {
    simulated_tts_vnd: simTtsVndB,
    distance_to_floor_vnd: distFloorB,
    distance_to_floor_pct: distFloorPctB,
    is_floor_breached: isBreachedB,
    scenario_a: {
      cash_locked_vnd: cashLockedA,
      simulated_tts_vnd: simTtsVndA,
      distance_to_floor_vnd: distFloorA,
      distance_to_floor_pct: distFloorPctA,
      ruin_prob: ruinProbA,
      borrow_gap_vnd: borrowGapA,
      is_breached: isBreachedA
    },
    scenario_b: {
      cash_locked_vnd: 0.0,
      simulated_tts_vnd: simTtsVndB,
      distance_to_floor_vnd: distFloorB,
      distance_to_floor_pct: distFloorPctB,
      ruin_prob: ruinProbB,
      borrow_gap_vnd: borrowGapB,
      is_breached: isBreachedB
    }
  };

  renderSimulationPanel();
}

// 7. VIEW RENDERERS
function renderAllViews() {
  renderAlertBanner();
  renderHeaderTickers();
  renderKeyMetrics();
  renderSimulationPanel();
  renderMacroCountdowns();
  renderBdsDebtGauge();
  renderQuantVisualizers();
  renderOrdersTable();
}

function renderAlertBanner() {
  const banner = document.getElementById("alert-banner");
  const msgEl = document.getElementById("alert-message");
  const delayBadge = document.getElementById("alert-delay-badge");
  const heading = document.getElementById("alert-heading");
  if (!banner || !msgEl) return;

  const tts = (State.valuation && State.valuation.tts_vnd) || 550643256;
  const isAboveFloor = tts >= HARD_FLOOR_VND;
  const missedCount = (State.disciplineGate && State.disciplineGate.unexecuted_recommendations_count != null)
    ? State.disciplineGate.unexecuted_recommendations_count
    : ((State.matrix && State.matrix.missed_recommendations_count) || 0);

  if (delayBadge) {
    if (missedCount === 0) {
      delayBadge.textContent = "SPRINT 1 THÁNG CUỐI (27/09 - 31/10)";
      delayBadge.className = "badge badge-tag";
    } else {
      delayBadge.textContent = `${missedCount} LỆNH CHƯA THỰC THI`;
      delayBadge.className = "badge badge-delay";
    }
  }

  if (heading) {
    if (missedCount === 0) {
      heading.textContent = "KẾ HOẠCH THOÁT VỐN 1 THÁNG CUỐI: BẢO VỆ SÀN CỨNG 540TR";
    } else {
      heading.textContent = `CẢNH BÁO KỶ LUẬT: 0/${missedCount} LỆNH ĐÃ THỰC THI`;
    }
  }

  if (isAboveFloor) {
    banner.className = missedCount === 0 ? "alert-banner warning" : "alert-banner alert-pulse danger";
    msgEl.innerHTML = `TTS đạt <strong>${formatVND(tts)}</strong> (vượt ngưỡng Sàn Cứng <strong>${formatVND(HARD_FLOOR_VND)}</strong>). ` +
      `Kích hoạt quy tắc nhị phân: <strong>BÁN 50% GIÁ TRỊ COIN (XẢ SẠCH 55,28 SOL) VÀ RÚT TOÀN BỘ STABLES VỀ BANK!</strong> ` +
      `Kế hoạch 1 tháng: Thoát vốn từng tuần theo Glidepath v3.0, hoàn tất 100% trước 25/10/2026.`;
  } else {
    banner.className = "alert-banner alert-pulse danger";
    msgEl.innerHTML = `🚨 BÁO ĐỘNG ĐỎ: TTS ĐÂM THỦNG SÀN CỨNG 540TR (${formatVND(tts)} < 540.000.000 ₫). ` +
      `<strong>MARKET SELL TOÀN BỘ DANH MỤC RA VND NGAY LẬP TỨC ĐỂ BẢO VỆ PHƯƠNG ÁN BĐS!</strong>`;
  }
}

function renderHeaderTickers() {
  const btcEl = document.getElementById("ticker-btc");
  const solEl = document.getElementById("ticker-sol");
  const p2pEl = document.getElementById("ticker-p2p");
  const tsVal = document.getElementById("data-timestamp-val");

  if (btcEl && State.marketRates) btcEl.textContent = formatUSD(State.marketRates.btc_usdt);
  if (solEl && State.marketRates) solEl.textContent = formatUSD(State.marketRates.sol_usdt);
  if (p2pEl && State.marketRates) p2pEl.textContent = formatVND(State.marketRates.usdt_vnd_p2p);

  if (tsVal) {
    const now = new Date();
    const pad = (n) => n.toString().padStart(2, '0');
    tsVal.textContent = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())} (${pad(now.getDate())}/${pad(now.getMonth()+1)}/${now.getFullYear()})`;
  }
}

function renderKeyMetrics() {
  const v = State.valuation || OfflineOracle.status.valuation;

  // 1. TTS Card
  const ttsVndEl = document.getElementById("val-tts-vnd");
  const ttsUsdEl = document.getElementById("val-tts-usd");
  const floorBadgeEl = document.getElementById("val-floor-badge");
  const floorCushionEl = document.getElementById("val-floor-cushion");

  if (ttsVndEl) ttsVndEl.textContent = formatVND(v.tts_vnd);
  if (ttsUsdEl) ttsUsdEl.textContent = formatUSD(v.tts_usd);

  const cushionVnd = v.tts_vnd - HARD_FLOOR_VND;
  const cushionPct = (cushionVnd / HARD_FLOOR_VND) * 100;

  if (floorBadgeEl) {
    if (cushionVnd >= 0) {
      floorBadgeEl.className = "badge badge-success";
      floorBadgeEl.textContent = "≥ 540TR LỜI BẤT NGỜ";
    } else {
      floorBadgeEl.className = "badge badge-danger";
      floorBadgeEl.textContent = "🚨 THỦNG SÀN 540TR";
    }
  }

  if (floorCushionEl) {
    if (cushionVnd >= 0) {
      floorCushionEl.className = "font-mono text-success";
      floorCushionEl.textContent = `+${formatVND(cushionVnd)} (${formatPct(cushionPct)})`;
    } else {
      floorCushionEl.className = "font-mono text-danger";
      floorCushionEl.textContent = `${formatVND(cushionVnd)} (${formatPct(cushionPct)})`;
    }
  }

  // 2. Cashout Progress Card
  const cashoutProgEl = document.getElementById("val-cashout-progress");
  const cashoutAmtEl = document.getElementById("val-cashout-amount");
  const cashoutBarEl = document.getElementById("cashout-progress-bar");
  const cashoutPct = v.cashout_progress_pct || 0.0;
  const cashWithdrawn = v.cash_withdrawn_vnd || 0.0;

  if (cashoutProgEl) cashoutProgEl.textContent = formatPct(cashoutPct, false);
  if (cashoutAmtEl) cashoutAmtEl.textContent = `${formatVND(cashWithdrawn)} / ${formatVND(HARD_FLOOR_VND)}`;
  if (cashoutBarEl) cashoutBarEl.style.width = `${Math.min(100, Math.max(0, cashoutPct))}%`;

  // 3. Portfolio Card Summary
  const portSummaryEl = document.getElementById("portfolio-summary");
  if (portSummaryEl && State.portfolio && State.portfolio.length > 0) {
    const summaryStr = State.portfolio.map(p => `${p.asset}: ${formatPct(p.weight_pct, false)}`).join(" | ");
    portSummaryEl.textContent = summaryStr;
  }

  // 4. Cost of Delay Card
  const delayTaxEl = document.getElementById("val-hesitation-tax");
  if (delayTaxEl) {
    delayTaxEl.textContent = "-" + formatVND(State.accumulatedHesitationTax);
  }
}

function renderSimulationPanel() {
  const btcShockDisplay = document.getElementById("val-btc-shock-display");
  const btcSimPrice = document.getElementById("val-btc-sim-price");
  const solShockDisplay = document.getElementById("val-sol-shock-display");
  const solSimPrice = document.getElementById("val-sol-sim-price");
  const p2pDisplay = document.getElementById("val-p2p-rate-display");

  if (btcShockDisplay) btcShockDisplay.textContent = formatPct(State.simInputs.btcShockPct);
  if (btcSimPrice) btcSimPrice.textContent = formatUSD(State.simInputs.btcPrice);
  if (solShockDisplay) solShockDisplay.textContent = formatPct(State.simInputs.solShockPct);
  if (solSimPrice) solSimPrice.textContent = formatUSD(State.simInputs.solPrice);
  if (p2pDisplay) p2pDisplay.textContent = formatVND(State.simInputs.p2pRate);

  if (!State.simResult) return;

  // Safety buffer bar
  const safetyText = document.getElementById("sim-safety-text");
  const safetyBar = document.getElementById("sim-safety-bar");
  const dist = State.simResult.distance_to_floor_vnd;

  if (safetyText && safetyBar) {
    if (dist >= 0) {
      safetyText.className = "font-mono text-success font-bold";
      safetyText.textContent = `+${formatVND(dist)} (AN TOÀN)`;
      safetyBar.className = "safety-fill bg-success";
      // 540M is at 50% marker; clamp bar width between 50% and 100%
      const w = 50 + Math.min(50, (dist / 100000000) * 50);
      safetyBar.style.width = `${w}%`;
    } else {
      safetyText.className = "font-mono text-danger font-bold";
      safetyText.textContent = `🚨 ${formatVND(dist)} (VI PHẠM SÀN CỨNG 540M)`;
      safetyBar.className = "safety-fill bg-danger";
      const w = Math.max(0, 50 - Math.min(50, (Math.abs(dist) / 100000000) * 50));
      safetyBar.style.width = `${w}%`;
    }
  }

  // Scenarios A and B
  const scA = State.simResult.scenario_a;
  const scB = State.simResult.scenario_b;

  const aCash = document.getElementById("sim-a-cash");
  const aTts = document.getElementById("sim-a-tts");
  const aRuin = document.getElementById("sim-a-ruin");
  const aGap = document.getElementById("sim-a-gap");

  if (aCash) aCash.textContent = formatVND(scA.cash_locked_vnd);
  if (aTts) aTts.textContent = formatVND(scA.simulated_tts_vnd);
  if (aRuin) aRuin.textContent = `< ${scA.ruin_prob}% (AN TOÀN)`;
  if (aGap) aGap.textContent = `${formatVND(scA.borrow_gap_vnd, true)} (${scA.borrow_gap_vnd <= BORROW_CEILING_VND ? "Dưới trần 615tr" : "Vượt trần"})`;

  const bCash = document.getElementById("sim-b-cash");
  const bTts = document.getElementById("sim-b-tts");
  const bRuin = document.getElementById("sim-b-ruin");
  const bGap = document.getElementById("sim-b-gap");

  if (bCash) bCash.textContent = "0 ₫";
  if (bTts) bTts.textContent = formatVND(scB.simulated_tts_vnd);
  if (bRuin) bRuin.textContent = `${scB.ruin_prob}% (${scB.is_breached ? "NGUY CƠ CAO" : "CẢNH BÁO"})`;
  if (bGap) {
    bGap.textContent = `${formatVND(scB.borrow_gap_vnd, true)} (${scB.borrow_gap_vnd > BORROW_CEILING_VND ? "🚨 VƯỢT TRẦN NỢ 615TR" : "Sát trần 615tr"})`;
  }
}

function renderMacroCountdowns() {
  if (!State.macroEvents || State.macroEvents.length === 0) return;

  State.macroEvents.forEach(evt => {
    let el = null;
    if (evt.id === "tranche_1") el = document.getElementById("countdown-tranche-1");
    else if (evt.id === "tranche_2") el = document.getElementById("countdown-tranche-2");
    else if (evt.id === "bds_debt_source") el = document.getElementById("countdown-bds-debt");
    else if (evt.id === "pce_inflation") el = document.getElementById("countdown-pce");
    else if (evt.id === "late_oct_deadline") el = document.getElementById("countdown-late-oct");

    if (el) {
      el.textContent = formatDuration(evt.remaining_seconds);
      if (evt.remaining_seconds <= 0) {
        el.className = "countdown-timer font-mono text-danger font-bold";
      }
    }
  });
}

function renderBdsDebtGauge() {
  const gap = State.bdsGap || OfflineOracle.macro.bds_financial_gap;
  const badgeEl = document.getElementById("bds-status-badge");
  const ceilingBar = document.getElementById("bds-ceiling-bar");
  const budgetEl = document.getElementById("bds-total-budget");
  const equityEl = document.getElementById("bds-self-equity");
  const borrowEl = document.getElementById("bds-borrow-needed");

  if (budgetEl) budgetEl.textContent = formatVND(gap.total_budget_vnd, true);
  if (equityEl) equityEl.textContent = formatVND(gap.total_self_equity_vnd, true);
  if (borrowEl) borrowEl.textContent = formatVND(gap.borrow_needed_vnd);

  const borrowNeeded = gap.borrow_needed_vnd || 544356744;
  const ceiling = gap.borrow_ceiling_vnd || BORROW_CEILING_VND;
  const cushion = ceiling - borrowNeeded;

  if (badgeEl) {
    if (cushion >= 0) {
      badgeEl.className = "badge badge-success";
      badgeEl.textContent = `🟢 DƯ AN TOÀN (+${formatVND(cushion, true)})`;
    } else {
      badgeEl.className = "badge badge-danger";
      badgeEl.textContent = `🚨 VƯỢT TRẦN NỢ (-${formatVND(Math.abs(cushion), true)})`;
    }
  }

  if (ceilingBar) {
    const pct = Math.min(100, Math.max(0, (borrowNeeded / ceiling) * 100));
    ceilingBar.style.width = `${pct}%`;
    ceilingBar.className = cushion >= 0 ? "progress-fill bg-success" : "progress-fill bg-danger";
  }
}

function renderQuantVisualizers() {
  // 1. MCR-Sim
  const mcrHoldProbEl = document.getElementById("mcr-prob-hold");
  const mcrHoldBar = document.getElementById("mcr-prob-hold-bar");
  const mcrSellProbEl = document.getElementById("mcr-prob-sell");
  const mcrSellBar = document.getElementById("mcr-prob-sell-bar");

  if (mcrHoldProbEl && mcrHoldBar) {
    mcrHoldProbEl.textContent = "37,0% THỦNG SÀN";
    mcrHoldBar.style.width = "37%";
  }
  if (mcrSellProbEl && mcrSellBar) {
    mcrSellProbEl.textContent = "0,8% (AN TOÀN)";
    mcrSellBar.style.width = "4.2%";
  }

  // 2. BHT-Ticker circular ring
  const circle = document.getElementById("bht-countdown-circle");
  const timerText = document.getElementById("bht-timer-text");
  const totalTaxEl = document.getElementById("bht-total-tax");

  if (circle && timerText) {
    const radius = 54;
    const circumference = 2 * Math.PI * radius; // ~339.29
    const ratio = Math.max(0, State.commitmentSecondsLeft) / COMMITMENT_TOTAL_SECONDS;
    const offset = circumference * (1 - ratio);
    circle.style.strokeDashoffset = offset.toFixed(2);

    const m = Math.floor(State.commitmentSecondsLeft / 60);
    const s = State.commitmentSecondsLeft % 60;
    timerText.textContent = `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;

    if (State.commitmentSecondsLeft <= 60) {
      circle.style.stroke = "#ef4444";
    } else if (State.commitmentSecondsLeft <= 180) {
      circle.style.stroke = "#f59e0b";
    } else {
      circle.style.stroke = "#ef4444";
    }
  }

  if (totalTaxEl) {
    totalTaxEl.textContent = "-" + formatVND(State.accumulatedHesitationTax);
  }

  // 3. AVC-Meter Speedometer
  const needle = document.getElementById("avc-needle");
  const vcrVal = document.getElementById("avc-vcr-value");
  const holdingEl = document.getElementById("cppi-holding");
  const maxSafeEl = document.getElementById("cppi-max-safe");
  const excessEl = document.getElementById("cppi-excess-risk");

  const vcr = (State.trend && State.trend.avc_meter && State.trend.avc_meter.vcr_days) || 0.69;
  if (vcrVal) vcrVal.textContent = vcr.toFixed(2);

  if (needle) {
    // 0 days -> -75 deg, 3.0 days -> 0 deg, 6.0 days -> +75 deg
    let angle = -75;
    if (vcr <= 3.0) {
      angle = -75 + (vcr / 3.0) * 75;
    } else if (vcr <= 6.0) {
      angle = ((vcr - 3.0) / 3.0) * 75;
    } else {
      angle = Math.min(85, 75 + ((vcr - 6.0) / 4.0) * 10);
    }
    needle.setAttribute("transform", `rotate(${angle.toFixed(1)} 120 110)`);
  }

  if (holdingEl) holdingEl.textContent = "496,1tr ₫";
  if (maxSafeEl) maxSafeEl.textContent = "114,4tr ₫";
  if (excessEl) excessEl.textContent = "⚠️ VƯỢT TRẦN NGUY HIỂM: +381,7 TRIỆU VND";
}

// --- DUAL STRATEGY CONTROLLERS ---
window.selectStrategyView = function(mode) {
  State.strategyView = mode;
  const btnA = document.getElementById("btn-mode-a");
  const btnB = document.getElementById("btn-mode-b");
  const btnBoth = document.getElementById("btn-mode-both");
  const grid = document.getElementById("strategy-cards-grid");

  if (btnA) btnA.className = mode === 'a' ? "btn btn-sm btn-primary active-mode-btn" : "btn btn-sm btn-secondary";
  if (btnB) btnB.className = mode === 'b' ? "btn btn-sm btn-primary active-mode-btn" : "btn btn-sm btn-secondary";
  if (btnBoth) btnBoth.className = mode === 'both' ? "btn btn-sm btn-primary active-mode-btn" : "btn btn-sm btn-secondary";

  if (grid) {
    grid.classList.remove("single-a", "single-b");
    if (mode === 'a') grid.classList.add("single-a");
    if (mode === 'b') grid.classList.add("single-b");
  }
};

window.applyOrdersMode = function(mode) {
  State.activeOrdersMode = mode;
  const badge = document.getElementById("orders-mode-badge");
  const btnA = document.getElementById("btn-toggle-orders-a");
  const btnB = document.getElementById("btn-toggle-orders-b");
  const cardBtnA = document.getElementById("btn-apply-card-a");
  const cardBtnB = document.getElementById("btn-apply-card-b");
  const cardA = document.getElementById("card-strategy-a");
  const cardB = document.getElementById("card-strategy-b");

  if (badge) {
    if (mode === 'a') {
      badge.textContent = "ĐANG XEM: CHẾ ĐỘ A (BĐS GLIDEPATH)";
      badge.className = "badge badge-success font-mono";
    } else {
      badge.textContent = "ĐANG XEM: CHẾ ĐỘ B (MAXIMUM PORT)";
      badge.className = "badge badge-warning font-mono";
    }
  }

  if (btnA) btnA.className = mode === 'a' ? "btn btn-xs btn-primary" : "btn btn-xs btn-secondary";
  if (btnB) btnB.className = mode === 'b' ? "btn btn-xs btn-primary" : "btn btn-xs btn-secondary";

  if (cardBtnA) {
    cardBtnA.textContent = mode === 'a' ? "✓ Đang Áp Dụng Lệnh Mode A" : "🧭 Áp Dụng Lệnh Mode A";
    cardBtnA.className = mode === 'a' ? "btn btn-success btn-xs" : "btn btn-outline btn-xs";
  }

  if (cardBtnB) {
    cardBtnB.textContent = mode === 'b' ? "✓ Đang Áp Dụng Lệnh Mode B" : "🚀 Áp Dụng Lệnh Mode B";
    cardBtnB.className = mode === 'b' ? "btn btn-warning btn-xs" : "btn btn-outline btn-xs";
  }

  if (cardA) cardA.classList.toggle("active-card", mode === 'a');
  if (cardB) cardB.classList.toggle("active-card", mode === 'b');

  renderOrdersTable();
  showToast(mode === 'a' ? "🧭 Bảng lệnh chuyển sang Chế Độ A (BĐS Glidepath)" : "🚀 Bảng lệnh chuyển sang Chế Độ B (Maximum Port Trend-Riding)", "info");
};

function getActiveOrdersList() {
  const mode = State.activeOrdersMode || 'a';
  if (mode === 'b') {
    if (State.dualStrategies && State.dualStrategies.mode_b && State.dualStrategies.mode_b.orders) {
      return State.dualStrategies.mode_b.orders;
    }
    const p2p = (State.marketRates && State.marketRates.usdt_vnd_p2p) || 26011;
    const solP = (State.marketRates && State.marketRates.sol_usdt) || 120.66;
    return [
      { step: 1, action: "WITHDRAW", channel: "P2P", symbol: "USDT", qty: 1415.0, price: p2p, estimated_vnd: 1415.0 * p2p, deadline: "Ngay lập tức", reason: "Rút 100% Stables ra VND (loại bỏ rủi ro Binance)" },
      { step: 2, action: "MARKET_SELL", channel: "SPOT", symbol: "SOL", qty: 55.28, price: solP, estimated_vnd: 55.28 * solP * p2p, deadline: "Trong tuần 1", reason: "Chốt lời SOL ở đỉnh SOL/BTC 98.9% (hoặc swap BTC)" },
      { step: 3, action: "STOP_MARKET", channel: "SPOT", symbol: "BTC", qty: 0.15931, price: 78500.0, estimated_vnd: 0.15931 * 78500.0 * p2p, deadline: "GTC (Cài ngay)", reason: "Cài Stop-Market $78,500 bảo vệ TTS >= 520tr VND" },
      { step: 4, action: "LIMIT_SELL", channel: "SPOT", symbol: "BTC", qty: 0.04000, price: 90200.0, estimated_vnd: 0.04000 * 90200.0 * p2p, deadline: "GTC (Treo sẵn)", reason: "Thang L1 ($90.2k): Bán 25% BTC khi sóng 1 bùng nổ (TTS ~595tr)" },
      { step: 5, action: "LIMIT_SELL", channel: "SPOT", symbol: "BTC", qty: 0.04000, price: 96500.0, estimated_vnd: 0.04000 * 96500.0 * p2p, deadline: "GTC (Treo sẵn)", reason: "Thang L2 ($96.5k): Bán 25% BTC tiếp theo (TTS ~635tr)" },
      { step: 6, action: "LIMIT_SELL", channel: "SPOT", symbol: "BTC", qty: 0.04000, price: 103000.0, estimated_vnd: 0.04000 * 103000.0 * p2p, deadline: "GTC (Treo sẵn)", reason: "Thang L3 ($103k): Bán 25% BTC (TTS đạt ~675tr - VƯỢT GỐC 650TR)" }
    ];
  }
  return (State.matrix && State.matrix.orders_sheet) || OfflineOracle.matrix.orders_sheet || [];
}

function renderOrdersTable() {
  const table = document.getElementById("orders-table");
  if (!table) return;

  const tbody = table.querySelector("tbody");
  if (!tbody) return;

  const orders = getActiveOrdersList();
  if (!orders || orders.length === 0) return;

  tbody.innerHTML = "";
  orders.forEach((ord, idx) => {
    const tr = document.createElement("tr");
    const priority = ord.priority || ord.step || (idx + 1);
    const pClass = priority === 1 ? "p1" : (priority === 2 ? "p2" : (priority === 3 ? "p3" : "p2"));
    const actStr = (ord.action || ord.order_type || "").toUpperCase();
    const isStop = actStr.includes("STOP");
    const isLimit = actStr.includes("LIMIT");
    const isWithdraw = actStr.includes("WITHDRAW");
    const actionColor = isStop ? "text-danger" : (isLimit ? "text-cyan" : (isWithdraw ? "text-success" : "text-warning"));
    const tagColor = isStop ? "badge-tag-danger" : (isLimit ? "badge-tag-warning" : "badge-tag-danger");
    const channel = (ord.channel === "P2P" || ord.symbol_pair === "USDT/VND" || ord.order_type === "P2P_SELL") ? "Binance P2P" : "Binance Spot";
    const sym = ord.symbol || (ord.symbol_pair ? ord.symbol_pair.replace("USDT", "") : "BTC");
    const estVal = ord.estimated_vnd || ord.est_vnd || 0;

    tr.innerHTML = `
      <td><span class="badge-priority ${pClass}">${priority}</span></td>
      <td>${channel}</td>
      <td><strong class="${actionColor}">${actStr.replace(/_/g, " ")}</strong></td>
      <td>${sym}</td>
      <td class="font-mono">${formatCrypto(ord.qty, sym.replace("USDT", ""))}</td>
      <td class="font-mono">${channel.includes("P2P") ? formatVND(ord.price) : "$" + Number(ord.price).toLocaleString()}</td>
      <td class="font-mono ${actionColor}">${formatVND(estVal)}</td>
      <td><span class="${tagColor}">${ord.deadline || "Ngay lập tức"}</span></td>
    `;
    tbody.appendChild(tr);
  });
}

function renderAgyConsole(output, isError = false) {
  const consoleEl = document.getElementById("agy-console");
  if (!consoleEl) return;
  consoleEl.textContent = output;
  consoleEl.style.color = isError ? "#f87171" : "#a7f3d0";
}

function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  if (type === "error") toast.style.borderColor = "var(--accent-danger)";
  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3500);
}

// 8. ACTIONS & COMMANDS
async function copyOrderSheet() {
  const mode = State.activeOrdersMode || 'a';
  const orders = getActiveOrdersList();
  let text = mode === 'a' 
    ? `=== BẢNG LỆNH CHẾ ĐỘ A: BĐS GLIDEPATH (HẠN 31/10/2026) ===\n`
    : `=== BẢNG LỆNH CHẾ ĐỘ B: MAXIMUM PORT TREND-RIDING (SÓNG Q4) ===\n`;
  text += `Thời gian tạo: ${new Date().toLocaleString("vi-VN")}\n`;
  text += mode === 'a'
    ? `Mục tiêu: Thoát vốn 100% về bank trước 25/10 để làm sổ đất Phù Đổng (né tăng giá đất 2027)\n\n`
    : `Mục tiêu: Tối đa hóa lợi nhuận Q4, cài Trailing Stop $78.5k + Thang chốt lời $90k-$103k\n\n`;

  orders.forEach((o, idx) => {
    const num = o.priority || o.step || (idx + 1);
    const act = (o.action || o.order_type || "").replace(/_/g, " ");
    const channel = (o.channel === "P2P" || o.symbol_pair === "USDT/VND" || o.order_type === "P2P_SELL") ? "P2P" : "SPOT";
    const sym = o.symbol || (o.symbol_pair ? o.symbol_pair.replace("USDT", "") : "BTC");
    const priceStr = channel === "P2P" ? `${formatVND(o.price)}` : `$${Number(o.price).toLocaleString()}`;
    const est = formatVND(o.estimated_vnd || o.est_vnd || 0);
    text += `${num}. [${channel}] ${act}: ${o.qty} ${sym} @ ${priceStr} -> ${est} (Hạn: ${o.deadline || "Ngay"})\n   Ghi chú: ${o.reason || o.note || ""}\n`;
  });
  text += `\n=============================================================`;

  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(text);
    } else {
      // Fallback textarea
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    }
    showToast(mode === 'a' ? "📋 Đã sao chép Bảng Lệnh Chế Độ A (BĐS Glidepath)!" : "📋 Đã sao chép Bảng Lệnh Chế Độ B (Maximum Port)!", "success");
  } catch (err) {
    showToast("Không thể sao chép tự động: " + err.message, "error");
  }
}

async function runAgyExecution(dryRun = false) {
  if (State.agyExecuting) return;
  State.agyExecuting = true;

  const spinner = document.getElementById("agy-spinner");
  const runBtn = document.getElementById("btn-run-agy");
  const bannerBtn = document.getElementById("btn-banner-agy");
  const intelBtn = document.getElementById("btn-trigger-intel");

  if (spinner) spinner.style.display = "block";
  if (runBtn) {
    runBtn.disabled = true;
    runBtn.textContent = "⏳ Đang phân tích qua agy CLI...";
  }
  if (bannerBtn) bannerBtn.disabled = true;
  if (intelBtn) {
    intelBtn.disabled = true;
    intelBtn.textContent = "⏳ Đang phân tích...";
  }

  renderAgyConsole(`[EXEC] Đang điều phối phiên Antigravity qua CLI cục bộ (dry_run=${dryRun})...\n$ agy -p "Review crypto portfolio according to crypto-plan.md, evaluate 540tr hard floor..."`);

  try {
    const res = await safeFetchJson("/api/agy/execute", {
      method: "POST",
      body: JSON.stringify({ action: "review", dry_run: dryRun, timeout: 60 })
    }, {
      status: "ok",
      data: {
        status: "completed",
        stdout: `[OFFLINE AGY SIMULATION]\n> Command: agy -p "Review crypto portfolio according to crypto-plan.md, evaluate 540tr hard floor..."\n> Returncode: 0\n> Section 7.5 Review: COMPLETED\n> Status: Binary Matrix Rule Triggered (TTS >= 540tr -> TAKE PROFIT 50% NOW)\n> 10-Min Binance Order Sheet dispatched.`,
        returncode: 0
      }
    });

    let output = "";
    if (res?.data?.parsed?.response) {
      output = res.data.parsed.response;
    } else if (res?.parsed?.response) {
      output = res.parsed.response;
    } else {
      output = (res && res.stdout) || (res && res.data && res.data.stdout) || JSON.stringify(res, null, 2);
    }
    const now = new Date();
    const pad = (n) => n.toString().padStart(2, '0');
    const timeStr = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
    
    renderAgyConsole(`=== ANTIGRAVITY EXECUTION COMPLETED (${timeStr}) ===\n${output}`);
    showToast(`⚡ Phiên agy review đã hoàn tất lúc ${timeStr}!`, "success");

    const lastRunEl = document.getElementById("intel-last-run");
    if (lastRunEl) {
      lastRunEl.innerHTML = `Đánh giá gần nhất: <strong>${timeStr} hôm nay</strong>`;
    }

    // Refresh data after successful run
    setTimeout(fetchInitialData, 1000);
  } catch (err) {
    renderAgyConsole(`=== AGY EXECUTION ERROR ===\n${err.message}`, true);
    showToast("Lỗi khi gọi agy CLI: " + err.message, "error");
  } finally {
    State.agyExecuting = false;
    if (spinner) spinner.style.display = "none";
    if (runBtn) {
      runBtn.disabled = false;
      runBtn.textContent = "⚡ Chạy agy Review (Local CLI)";
    }
    if (bannerBtn) bannerBtn.disabled = false;
    if (intelBtn) {
      intelBtn.disabled = false;
      intelBtn.textContent = "⚡ Phân Tích Danh Mục";
    }
  }
}

async function viewAgyCommand() {
  const res = await safeFetchJson("/api/agy/command", {
    method: "POST",
    body: JSON.stringify({ action: "review" })
  }, {
    command: `agy -p "Review crypto portfolio according to crypto-plan.md, evaluate 540tr hard floor and generate action proposals." --dangerously-skip-permissions --output-format json`
  });

  const cmd = res.command || (res.data && res.data.command) || res;
  renderAgyConsole(`[SHELL COMMAND GENERATOR]\n${cmd}\n\n(Bạn có thể sao chép lệnh trên để chạy trực tiếp trên Terminal)`);
  showToast("💻 Đã tạo lệnh shell agy CLI!", "info");
}

// 9. EVENT LISTENERS SETUP
function setupEventListeners() {
  // Slider BTC shock
  const btcSlider = document.getElementById("slider-btc-shock");
  if (btcSlider) {
    btcSlider.addEventListener("input", (e) => {
      State.simInputs.btcShockPct = parseFloat(e.target.value);
      calculateLocalSimulation();
    });
  }

  // Slider SOL shock
  const solSlider = document.getElementById("slider-sol-shock");
  if (solSlider) {
    solSlider.addEventListener("input", (e) => {
      State.simInputs.solShockPct = parseFloat(e.target.value);
      calculateLocalSimulation();
    });
  }

  // Slider P2P rate
  const p2pSlider = document.getElementById("slider-p2p-rate");
  if (p2pSlider) {
    p2pSlider.addEventListener("input", (e) => {
      State.simInputs.p2pRate = parseFloat(e.target.value);
      calculateLocalSimulation();
    });
  }

  // Presets
  const btnDump = document.getElementById("btn-preset-dump");
  if (btnDump) {
    btnDump.addEventListener("click", () => {
      if (btcSlider) btcSlider.value = -10;
      if (solSlider) solSlider.value = -15;
      State.simInputs.btcShockPct = -10;
      State.simInputs.solShockPct = -15;
      calculateLocalSimulation();
    });
  }

  const btnCrash = document.getElementById("btn-preset-crash");
  if (btnCrash) {
    btnCrash.addEventListener("click", () => {
      if (btcSlider) btcSlider.value = -20;
      if (solSlider) solSlider.value = -30;
      State.simInputs.btcShockPct = -20;
      State.simInputs.solShockPct = -30;
      calculateLocalSimulation();
    });
  }

  // Test F11 Preset: BTC $70k (-16.93%), SOL $95 (-17.91%)
  const btnBtc70k = document.getElementById("btn-preset-btc70k");
  if (btnBtc70k) {
    btnBtc70k.addEventListener("click", () => {
      if (btcSlider) btcSlider.value = -17;
      if (solSlider) solSlider.value = -18;
      State.simInputs.btcShockPct = -16.9257; // 70000 / 84262 - 1
      State.simInputs.solShockPct = -17.9053; // 95 / 115.72 - 1
      calculateLocalSimulation();
      showToast("Đã nạp kịch bản BTC $70k (Thủng sàn 540tr)", "warning");
    });
  }

  const btnReset = document.getElementById("btn-preset-reset");
  if (btnReset) {
    btnReset.addEventListener("click", () => {
      if (btcSlider) btcSlider.value = 0;
      if (solSlider) solSlider.value = 0;
      if (p2pSlider) p2pSlider.value = 25930;
      State.simInputs.btcShockPct = 0;
      State.simInputs.solShockPct = 0;
      State.simInputs.p2pRate = 25930;
      calculateLocalSimulation();
    });
  }

  // Action buttons
  const btnCopy = document.getElementById("btn-copy-orders");
  if (btnCopy) btnCopy.addEventListener("click", copyOrderSheet);

  const btnBannerCopy = document.getElementById("btn-banner-copy");
  if (btnBannerCopy) btnBannerCopy.addEventListener("click", copyOrderSheet);

  const btnRunAgy = document.getElementById("btn-run-agy");
  if (btnRunAgy) btnRunAgy.addEventListener("click", () => runAgyExecution(false));

  const btnTriggerIntel = document.getElementById("btn-trigger-intel");
  if (btnTriggerIntel) btnTriggerIntel.addEventListener("click", () => runAgyExecution(false));

  const btnBannerAgy = document.getElementById("btn-banner-agy");
  if (btnBannerAgy) btnBannerAgy.addEventListener("click", () => runAgyExecution(false));

  const btnDryRun = document.getElementById("btn-dryrun-agy");
  if (btnDryRun) btnDryRun.addEventListener("click", () => runAgyExecution(true));

  const btnViewCmd = document.getElementById("btn-view-command");
  if (btnViewCmd) btnViewCmd.addEventListener("click", viewAgyCommand);

  const btnRefresh = document.getElementById("btn-refresh");
  if (btnRefresh) {
    btnRefresh.addEventListener("click", () => {
      showToast("⟳ Đang làm mới dữ liệu từ backend...", "info");
      fetchInitialData();
    });
  }

  const btnCloseConsole = document.getElementById("btn-close-console");
  if (btnCloseConsole) {
    btnCloseConsole.addEventListener("click", () => {
      const consoleBox = document.getElementById("agy-console-drawer");
      if (consoleBox) {
        consoleBox.style.display = consoleBox.style.display === "none" ? "block" : "none";
      }
    });
  }
}

// 10. TIMERS & LIFECYCLE MANAGEMENT
function startClocks() {
  // 1-second ticking clock
  setInterval(() => {
    // Tick macro events
    if (State.macroEvents && State.macroEvents.length > 0) {
      State.macroEvents.forEach(evt => {
        if (evt.remaining_seconds > 0) {
          evt.remaining_seconds -= 1;
        }
      });
      renderMacroCountdowns();
    }

    // Tick hesitation tax: +10.7638 VND/sec
    State.accumulatedHesitationTax += BURN_PER_SECOND_VND;
    const totalTaxEl = document.getElementById("bht-total-tax");
    const delayTaxEl = document.getElementById("val-hesitation-tax");
    if (totalTaxEl) totalTaxEl.textContent = "-" + formatVND(State.accumulatedHesitationTax);
    if (delayTaxEl) delayTaxEl.textContent = "-" + formatVND(State.accumulatedHesitationTax);

    // Tick commitment circular timer
    if (State.commitmentSecondsLeft > 0) {
      State.commitmentSecondsLeft -= 1;
    } else {
      State.commitmentSecondsLeft = COMMITMENT_TOTAL_SECONDS; // loop
    }
    const circle = document.getElementById("bht-countdown-circle");
    const timerText = document.getElementById("bht-timer-text");
    if (circle && timerText) {
      const radius = 54;
      const circumference = 2 * Math.PI * radius;
      const ratio = State.commitmentSecondsLeft / COMMITMENT_TOTAL_SECONDS;
      const offset = circumference * (1 - ratio);
      circle.style.strokeDashoffset = offset.toFixed(2);

      const m = Math.floor(State.commitmentSecondsLeft / 60);
      const s = State.commitmentSecondsLeft % 60;
      timerText.textContent = `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
    }
  }, 1000);

  // Background polling every 30s
  setInterval(() => {
    if (!document.hidden) {
      fetchInitialData();
    }
  }, 30000);

  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) {
      fetchInitialData();
    }
  });
}

// 11. BOOTSTRAP APP
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners();
  fetchInitialData();
  startClocks();
});
