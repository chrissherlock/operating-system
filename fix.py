#!/usr/bin/env python3
import os

AGING_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>8. Simulating LRU: The Aging Algorithm — COSC240</title>
  <script>
    window.MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']]
      }
    };
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
      --border-dark: #94a3b8;
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --text: #0f172a;
      --text-muted: #475569;
      --hit-color: #16a34a;
      --hit-bg: #dcfce7;
      --fault-color: #dc2626;
      --fault-bg: #fee2e2;
      --warn-color: #d97706;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 18px;
    }

    .nav-back {
      width: 100%;
      max-width: 1100px;
      display: flex;
    }
    .nav-back a {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      font-family: var(--font-mono);
      text-decoration: none;
      color: var(--accent);
      background-color: #f0f9ff;
      border: 1px solid #bae6fd;
      padding: 6px 12px;
      border-radius: 6px;
      transition: background-color 0.15s ease, color 0.15s ease;
    }
    .nav-back a:hover { background-color: var(--accent); color: #fff; }

    header { text-align: center; max-width: 900px; }
    h1 { font-size: 1.85rem; color: var(--accent); margin-bottom: 6px; }
    p.subtitle { color: var(--text-muted); font-size: 0.95rem; }

    .main-container {
      display: flex;
      flex-direction: column;
      gap: 20px;
      width: 100%;
      max-width: 1100px;
    }

    .card {
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    .theory-section {
      line-height: 1.7;
      font-size: 0.95rem;
      color: #334155;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .theory-section h2 {
      font-size: 1.25rem;
      color: var(--text);
      margin-bottom: 4px;
      border-bottom: 1px solid #f1f5f9;
      padding-bottom: 4px;
    }
    .theory-callout {
      background-color: #f0f9ff;
      border-left: 4px solid var(--accent);
      padding: 12px 16px;
      border-radius: 0 6px 6px 0;
      font-size: 0.9rem;
      color: #0369a1;
      font-family: var(--font-mono);
      line-height: 1.5;
    }

    .figure-container {
      width: 100%;
      max-width: 820px;
      margin: 10px auto;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      overflow-x: auto;
    }

    .tutorial-panel {
      border-left: 4px solid var(--accent);
      background: #f0f9ff;
    }
    .tutorial-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .tutorial-title {
      font-size: 1.25rem;
      font-weight: 700;
      color: #075985;
    }
    .tutorial-body {
      font-size: 0.95rem;
      line-height: 1.6;
      color: #0c4a6e;
      min-height: 75px;
    }

    .tour-nav {
      display: flex;
      gap: 10px;
      align-items: center;
      margin-top: 8px;
    }

    button {
      background-color: var(--accent);
      color: #fff;
      border: none;
      padding: 8px 14px;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.85rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: background-color 0.15s ease;
    }
    button:hover { background-color: var(--accent-hover); }
    button:disabled { opacity: 0.4; cursor: not-allowed; }
    button.btn-sec {
      background-color: #f1f5f9;
      color: var(--text);
      border: 1px solid var(--border);
    }
    button.btn-sec:hover { background-color: #e2e8f0; }

    .split-grid {
      display: grid;
      grid-template-columns: 400px 1fr;
      gap: 20px;
      align-items: start; /* Prevents vertical collision/overlap */
      margin-top: 10px;
    }
    @media (max-width: 860px) {
      .split-grid { grid-template-columns: 1fr; }
    }

    .register-visual-box {
      display: flex;
      flex-direction: column;
      gap: 8px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
    }

    .bit-cell-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
      font-size: 0.8rem;
      padding: 4px 6px;
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 4px;
    }
    .bit-boxes {
      display: flex;
      gap: 2px;
    }
    .bit-box {
      width: 20px;
      height: 22px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      font-weight: 700;
      font-size: 0.75rem;
      color: #0f172a;
    }
    .bit-box.msb-highlight {
      background: #dcfce7;
      border-color: #16a34a;
      color: #15803d;
      transform: scale(1.08);
      box-shadow: 0 0 6px rgba(22, 163, 74, 0.4);
    }

    .table-spec {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.82rem;
      font-family: var(--font-mono);
    }
    .table-spec th, .table-spec td {
      border: 1px solid var(--border);
      padding: 6px 8px;
      text-align: center;
    }
    .table-spec th { background: #f8fafc; font-weight: 700; color: var(--text-muted); }
    .table-spec tr.victim-row { background-color: #fee2e2; font-weight: 700; }

    .telemetry-box {
      background: #0f172a;
      color: #f8fafc;
      border-radius: 6px;
      padding: 12px 16px;
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 0.85rem;
    }

    .terminal-box {
      background: #0f172a;
      color: #f8fafc;
      border-radius: 6px;
      padding: 12px;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      height: 220px;
      overflow-y: auto;
      display: flex;
      flex-direction: column-reverse;
      gap: 4px;
    }
    .log-row { line-height: 1.4; }
    .log-hit { color: #4ade80; font-weight: 700; }
    .log-fault { color: #f87171; font-weight: 700; }
    .log-clear { color: #facc15; }
    .log-info { color: #38bdf8; }

    .guide-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 10px;
      margin-top: 6px;
      margin-bottom: 12px;
    }
    .guide-box {
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 2px;
      font-size: 0.85rem;
    }
    .guide-box strong {
      color: var(--accent);
      font-size: 0.88rem;
    }
  </style>
</head>
<body>

  <div class="nav-back">
    <a href="index.html">&larr; Back to Week Overview</a>
  </div>

  <header>
    <h1>8. Simulating LRU: The Aging Algorithm</h1>
    <p class="subtitle">Tanenbaum Section 3.4.5 (Fig. 3-17): Right-shift history registers, MSB insertion of R-bits, and multi-tick LRU approximation.</p>
  </header>

  <div class="main-container">

    <!-- 1. THEORETICAL EXPLANATION -->
    <div class="card">
      <div class="theory-section">
        <h2>1. The Limitation of Simple Second-Chance</h2>
        <p>
          While the Clock algorithm (second-chance) avoids the heavy overhead of strict LRU, it is relatively coarse-grained. It only remembers whether a page was referenced during the <em>current</em> sweep cycle ($R = 1$ or $R = 0$). It cannot distinguish between a page referenced 10 instructions ago versus one referenced 10,000 instructions ago.
        </p>

        <h2>2. The Aging Algorithm Solution &amp; The Referenced ($R$) Bit</h2>
        <p>
          To capture more precise access history without full LRU matrix overhead, operating systems use the <strong>Aging Algorithm</strong>. Each physical page frame is assigned a fixed-width binary history register (typically 8 bits wide, corresponding to 8 consecutive clock ticks).
        </p>
        <p>
          The foundation of aging relies on the hardware <strong>Referenced ($R$) bit</strong>. Whenever the CPU accesses a virtual address, the memory management unit (MMU) automatically sets the page's $R$ bit to $1$. Because the MMU never clears this bit on its own, the OS uses periodic clock ticks to read, shift, and reset it.
        </p>
        <ul style="padding-left: 20px; display: flex; flex-direction: column; gap: 6px;">
          <li><strong>Clock Tick Interception:</strong> At regular hardware clock intervals, the OS interrupts execution and performs a right-shift operation on every page's counter: $R_i \to R_i \gg 1$.</li>
          <li><strong>MSB Injection ($R \to \text{MSB}$):</strong> During the shift, the current hardware Referenced ($R$) bit is inserted into the most significant bit (MSB, position 7) of the register: $R_7 = R$.</li>
          <li><strong>Eviction Policy:</strong> When a page fault occurs, the kernel scans all frame registers as unsigned integers. The page with the <strong>lowest numerical value</strong> is chosen as the victim (indicating it has not been referenced for the longest sequence of ticks).</li>
        </ul>
        <div class="theory-callout">
          <strong>Tanenbaum's Aging Principle (Fig. 3-17):</strong><br>
          An 8-bit history register records access over the last 8 clock ticks. For example, a register value of `10001000` (136 decimal) means the page was referenced 8 ticks ago and 4 ticks ago. A value of `00000001` (1 decimal) means it was only referenced 1 tick ago. Aging provides an exceptional approximation of true LRU.
        </div>
      </div>
    </div>

    <!-- 2. GUIDED WALKTHROUGH -->
    <div class="card tutorial-panel">
      <div class="tutorial-header">
        <span id="wtCounter">Step 1 of 4</span>
        <span>Interactive Aging Stepper</span>
      </div>
      <div id="wtTitle" class="tutorial-title">1. Initial State across 4 Frames</div>

      <div class="split-grid">
        <div class="register-visual-box" id="wtRegisterBox"></div>
        <div style="display:flex; flex-direction:column; justify-content:space-between; height:100%; gap:12px;">
          <div id="wtText" class="tutorial-body"></div>
          <div class="tour-nav">
            <button id="wtPrevBtn" class="btn-sec" onclick="stepWtBackward()">Previous</button>
            <button id="wtNextBtn" onclick="stepWtForward()">Next Step &rarr;</button>
            <button class="btn-sec" style="margin-left:auto;" onclick="document.getElementById('sandboxSection').scrollIntoView({behavior:'smooth'})">Jump to Sandbox &darr;</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. SANDBOX -->
    <div class="card" id="sandboxSection">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
          <h2 style="font-size:1.25rem; font-weight:700;">Part 3: Interactive Aging Algorithm Sandbox</h2>
          <p style="font-size:0.85rem; color:var(--text-muted); margin-top:2px;">
            Trigger clock ticks, shift history registers, and observe victim selection based on lowest unsigned integer values.
          </p>
        </div>
        <div style="display:flex; gap:8px;">
          <button class="btn-sec" onclick="resetAgingState()">Reset Frames</button>
        </div>
      </div>

      <!-- Controls -->
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
        <label style="font-size:0.85rem; font-weight:600;">Reference Page:</label>
        <input type="text" id="refPageInput" value="X" maxlength="2" style="width:45px; text-align:center; padding:4px; font-family:var(--font-mono); text-transform:uppercase;">
        <button onclick="executeAgingAccess()">Access Page</button>
        <button class="btn-sec" onclick="triggerClockTick()">Clock Tick (Shift &gt;&gt; 1)</button>
      </div>

      <!-- Telemetry Banner -->
      <div class="telemetry-box">
        <span>Total Accesses: <strong id="statAccesses">0</strong></span>
        <span>Hits: <strong id="statHits" style="color:#4ade80;">0</strong></span>
        <span>Faults: <strong id="statFaults" style="color:#f87171;">0</strong></span>
        <span>Clock Ticks: <strong id="statTicks" style="color:#38bdf8;">0</strong></span>
      </div>

      <div class="split-grid">
        <div>
          <span style="font-weight:700; font-size:0.85rem; color:var(--text-muted); text-transform:uppercase;">Physical Frame Registers (8-bit)</span>
          <table class="table-spec" style="margin-top:6px;">
            <thead>
              <tr><th>Frame</th><th>Page</th><th>Hardware R</th><th>8-Bit Register (Binary Cells)</th><th>Decimal</th></tr>
            </thead>
            <tbody id="agingTableBody"></tbody>
          </table>
        </div>

        <div style="display:flex; flex-direction:column; gap:6px;">
          <span style="font-weight:700; font-size:0.85rem; color:var(--text-muted); text-transform:uppercase;">Kernel Aging Log</span>
          <div id="agingLog" class="terminal-box"></div>
        </div>
      </div>
    </div>

  </div>

  <script>
    let wtStep = 0;
    const wtSteps = [
      {
        title: "1. Initial State: Current Hardware R-Bits",
        text: "Consider 4 physical frames holding pages A, B, C, and D. Each frame has a live hardware <strong>Referenced ($R$) bit</strong> set by the MMU during recent CPU execution, alongside its 8-bit history register.",
        showR: true,
        frames: [
          { page: "A", r: 1, reg: 0b10001000, dec: 136 },
          { page: "B", r: 0, reg: 0b01110000, dec: 112 },
          { page: "C", r: 0, reg: 0b10000000, dec: 128 },
          { page: "D", r: 1, reg: 0b00110011, dec: 51 }
        ]
      },
      {
        title: "2. Clock Tick: R-Bit Injection & Right Shift",
        text: "During a clock tick, the OS reads each page's current hardware $R$ bit, shifts the 8-bit register right by 1 ($\gg 1$), and injects $R$ directly into Bit 7 (MSB, highlighted in green). Then $R$ resets to 0.",
        showR: true,
        highlightMsb: true,
        frames: [
          { page: "A", r: 0, reg: 0b11000100, dec: 196 },
          { page: "B", r: 0, reg: 0b00111000, dec: 56 },
          { page: "C", r: 0, reg: 0b01000000, dec: 64 },
          { page: "D", r: 0, reg: 0b10011001, dec: 153 }
        ]
      },
      {
        title: "3. Evaluating Eviction Candidates",
        text: "When a page fault occurs, the kernel evaluates unsigned decimal counter values: Page B (56), Page C (64), Page D (153), Page A (196).",
        showR: false,
        frames: [
          { page: "A", r: 0, reg: 0b11000100, dec: 196 },
          { page: "B", r: 0, reg: 0b00111000, dec: 56, victim: true },
          { page: "C", r: 0, reg: 0b01000000, dec: 64 },
          { page: "D", r: 0, reg: 0b10011001, dec: 153 }
        ]
      },
      {
        title: "4. Victim Selected: Page B Evicted",
        text: "Page B has the lowest numerical counter value (56), proving it has gone the longest without being referenced. Page B is evicted.",
        showR: false,
        frames: [
          { page: "A", r: 0, reg: 0b11000100, dec: 196 },
          { page: "X", r: 1, reg: 0b10000000, dec: 128, new: true },
          { page: "C", r: 0, reg: 0b01000000, dec: 64 },
          { page: "D", r: 0, reg: 0b10011001, dec: 153 }
        ]
      }
    ];

    function renderBitBoxes(val, highlightMsb) {
      const binStr = (val >>> 0).toString(2).padStart(8, '0');
      let html = '<div class="bit-boxes">';
      for (let i = 0; i < 8; i++) {
        const bit = binStr[i];
        const isMsb = (i === 0 && highlightMsb);
        html += `<div class="bit-box ${isMsb ? 'msb-highlight' : ''}" title="Bit ${7-i}">${bit}</div>`;
      }
      html += '</div>';
      return html;
    }

    function renderWt() {
      const s = wtSteps[wtStep];
      document.getElementById("wtCounter").textContent = `Step ${wtStep + 1} of ${wtSteps.length}`;
      document.getElementById("wtTitle").textContent = s.title;
      document.getElementById("wtText").innerHTML = s.text;

      const box = document.getElementById("wtRegisterBox");
      box.innerHTML = "";
      s.frames.forEach(f => {
        const row = document.createElement("div");
        row.className = "bit-cell-row";
        if (f.victim) row.style.background = "#fee2e2";
        if (f.new) row.style.background = "#dcfce7";

        const rBadge = s.showR ? `<span style="background:${f.r ? '#dcfce7' : '#fee2e2'}; color:${f.r ? '#15803d' : '#b91c1c'}; padding:2px 6px; border-radius:3px; font-weight:700; font-size:0.72rem;">R=${f.r}</span>` : '';

        row.innerHTML = `
          <div style="display:flex; align-items:center; gap:8px;">
            <span><strong>Page ${f.page}</strong></span>
            ${rBadge}
          </div>
          ${renderBitBoxes(f.reg, s.highlightMsb)}
          <span style="font-size:0.75rem; color:var(--text-muted);">${f.dec}</span>
        `;
        box.appendChild(row);
      });

      if (window.MathJax && window.MathJax.typeset) {
        MathJax.typeset();
      }

      document.getElementById("wtPrevBtn").disabled = (wtStep === 0);
      document.getElementById("wtNextBtn").disabled = (wtStep === wtSteps.length - 1);
    }

    function stepWtForward() {
      if (wtStep < wtSteps.length - 1) { wtStep++; renderWt(); }
      document.activeElement.blur();
    }
    function stepWtBackward() {
      if (wtStep > 0) { wtStep--; renderWt(); }
      document.activeElement.blur();
    }
    renderWt();

    let agingFrames = [
      { id: 0, page: "A", r: 1, reg: 0b10001000 },
      { id: 1, page: "B", r: 0, reg: 0b01110000 },
      { id: 2, page: "C", r: 0, reg: 0b10000000 },
      { id: 3, page: "D", r: 1, reg: 0b00110011 }
    ];
    let statTotal = 0;
    let statHits = 0;
    let statFaults = 0;
    let statTicks = 0;

    function renderAgingSandbox() {
      const tbody = document.getElementById("agingTableBody");
      tbody.innerHTML = "";

      let minVal = 999999;
      let victimIdx = -1;
      agingFrames.forEach((f, idx) => {
        if (f.reg < minVal) {
          minVal = f.reg;
          victimIdx = idx;
        }
      });

      agingFrames.forEach((f, idx) => {
        const tr = document.createElement("tr");
        if (idx === victimIdx) tr.className = "victim-row";
        tr.innerHTML = `
          <td>Frame ${f.id}</td>
          <td><strong>${f.page}</strong></td>
          <td><span style="background:${f.r ? '#dcfce7' : '#fee2e2'}; color:${f.r ? '#15803d' : '#b91c1c'}; padding:2px 6px; border-radius:3px; font-weight:700;">R=${f.r}</span></td>
          <td><div style="display:flex; justify-content:center;">${renderBitBoxes(f.reg, false)}</div></td>
          <td>${f.reg} ${idx === victimIdx ? ' &larr; [Victim]' : ''}</td>
        `;
        tbody.appendChild(tr);
      });

      document.getElementById("statAccesses").textContent = statTotal;
      document.getElementById("statHits").textContent = statHits;
      document.getElementById("statFaults").textContent = statFaults;
      document.getElementById("statTicks").textContent = statTicks;
    }

    function logAging(msg, type = "log-row") {
      const term = document.getElementById("agingLog");
      const row = document.createElement("div");
      row.className = `log-row ${type}`;
      row.textContent = `> ${msg}`;
      term.prepend(row);
    }

    function triggerClockTick() {
      statTicks++;
      agingFrames.forEach(f => {
        f.reg = (f.reg >>> 1) | (f.r << 7);
        f.r = 0;
      });
      logAging(`Clock Tick #${statTicks}: Injected hardware R-bits into MSB, shifted registers right by 1, and cleared R &rarr; 0.`, "log-clear");
      renderAgingSandbox();
    }

    function executeAgingAccess() {
      const input = document.getElementById("refPageInput");
      const p = input.value.trim().toUpperCase();
      if (!p) return;

      statTotal++;
      logAging(`--------------------------------------------------`);
      logAging(`Instruction references virtual Page '${p}'...`, "log-info");

      const hitIdx = agingFrames.findIndex(f => f.page === p);
      if (hitIdx !== -1) {
        statHits++;
        agingFrames[hitIdx].r = 1;
        logAging(`PAGE HIT: Page '${p}' is resident in Frame ${hitIdx}. Hardware set R=1.`, "log-hit");
        renderAgingSandbox();
        return;
      }

      statFaults++;
      logAging(`PAGE FAULT: Page '${p}' is absent from RAM! Finding victim with lowest counter...`, "log-fault");

      let minVal = 999999;
      let victimIdx = -1;
      agingFrames.executeAgingAccess = function() {} // placeholder
      agingFrames.forEach((f, idx) => {
        if (f.reg < minVal) {
          minVal = f.reg;
          victimIdx = idx;
        }
      });

      let evicted = agingFrames[victimIdx].page;
      agingFrames[victimIdx].page = p;
      agingFrames[victimIdx].r = 1;
      agingFrames[victimIdx].reg = 0b10000000;

      logAging(`EVICTION: Frame ${victimIdx} had lowest counter (${minVal}). Evicted '${evicted}' &rarr; Loaded '${p}' (R=1).`, "log-fault");
      renderAgingSandbox();
    }

    function resetAgingState() {
      agingFrames = [
        { id: 0, page: "A", r: 1, reg: 0b10001000 },
        { id: 1, page: "B", r: 0, reg: 0b01110000 },
        { id: 2, page: "C", r: 0, reg: 0b10000000 },
        { id: 3, page: "D", r: 1, reg: 0b00110011 }
      ];
      statTotal = 0;
      statHits = 0;
      statFaults = 0;
      statTicks = 0;
      document.getElementById("agingLog").innerHTML = "";
      logAging("Aging simulation reset to initial state.");
      renderAgingSandbox();
    }

    renderAgingSandbox();
    logAging("Aging algorithm sandbox initialized with 4 physical frames.");
  </script>
</body>
</html>
"""

def main():
    target_file = "week09-memory-management/08-aging-algorithm.html"
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(AGING_HTML)
    print(f"Successfully generated and updated active path: {target_file}")

if __name__ == "__main__":
    main()
