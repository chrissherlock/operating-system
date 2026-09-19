#!/usr/bin/env python3
import os
import subprocess
import sys

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>10. The WSClock Algorithm — COSC240</title>
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
      --warn-bg: #fef3c7;
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
      display: block;
    }
    .theory-section h2 {
      font-size: 1.25rem;
      color: var(--text);
      margin-top: 16px;
      margin-bottom: 4px;
      border-bottom: 1px solid #f1f5f9;
      padding-bottom: 4px;
    }
    .theory-section p {
      margin-bottom: 10px;
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
      margin-bottom: 12px;
    }

    /* Floating Bio Sidebar */
    .bio-sidebar {
      float: right;
      width: 300px;
      background: #f8fafc;
      border: 1px solid var(--border);
      border-top: 4px solid var(--accent);
      border-radius: 6px;
      padding: 16px;
      margin-left: 24px;
      margin-right: 0px;
      margin-bottom: 16px;
      margin-top: 4px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      font-size: 0.88rem;
      shape-outside: margin-box;
    }
    .bio-sidebar h3 {
      font-size: 1rem;
      color: var(--accent);
      margin-bottom: 2px;
    }
    .bio-sidebar p {
      color: var(--text-muted);
      line-height: 1.5;
      font-size: 0.85rem;
      margin-bottom: 6px;
    }
    .bio-sidebar a {
      color: var(--accent);
      text-decoration: underline;
      font-weight: 600;
    }

    .figure-container {
      width: 100%;
      max-width: 860px;
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
      clear: both;
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

    .split-grid {
      display: grid;
      grid-template-columns: 460px 1fr;
      gap: 24px;
      align-items: start;
      margin-top: 10px;
    }
    @media (max-width: 860px) {
      .split-grid { grid-template-columns: 1fr; }
      .bio-sidebar { float: none; width: 100%; margin-left: 0; }
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
    .table-spec tr.hand-active { background: #e0f2fe; font-weight: 700; }
    .table-spec tr.victim-row { background: #fee2e2; font-weight: 700; }

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
      padding: 12px 16px;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      height: 240px;
      overflow-y: auto;
      display: flex;
      flex-direction: column-reverse;
      gap: 4px;
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
    }
    button:hover { background-color: var(--accent-hover); }
    button.btn-sec { background-color: #f1f5f9; color: var(--text); border: 1px solid var(--border); }
    button.btn-sec:hover { background-color: #e2e8f0; }
  </style>
</head>
<body>

  <div class="nav-back">
    <a href="index.html">&larr; Back to Week Overview</a>
  </div>

  <header>
    <h1>10. The WSClock Page Replacement Algorithm</h1>
    <p class="subtitle">Tanenbaum Section 3.4.6 (Fig. 3-20): Combining the simplicity of Clock with the thrashing-resistance of the Working Set model.</p>
  </header>

  <div class="main-container">

    <!-- 1. THEORY SECTION WITH PIONEER PROFILE -->
    <div class="card">
      <div class="theory-section">
        <!-- Bio Sidebar on Right -->
        <aside class="bio-sidebar">
          <h3>Pioneer Profile</h3>
          <p>
            <strong>Richard W. Carr</strong> and <strong>John L. Hennessy</strong> formulated the <strong>WSClock</strong> algorithm in their seminal 1981 paper, <em>"WSCLOCK—A Simple and Effective Algorithm for Virtual Memory Management"</em>, presented at the 8th ACM Symposium on Operating Systems Principles (SOSP).
          </p>
          <p>
            Recognizing that Denning's pure working set algorithm suffered from an expensive \(O(N)\) linear scan on every page fault, they married the low-overhead circular pointer of the Clock algorithm with working set age thresholds (\(\tau\)).
          </p>
          <p>
            <strong>Dr. John L. Hennessy</strong> later co-developed the MIPS RISC architecture, co-authored the definitive computer architecture textbooks with David Patterson, served as the 10th President of Stanford University, and was awarded the ACM A.M. Turing Award in 2017.
          </p>
        </aside>

        <h2>1. Why Simple Working Set Is Too Expensive</h2>
        <p>
          While the theoretical Working Set model prevents thrashing by ensuring a process's active pages ($w(k, t)$) remain resident in RAM, implementing it naively is impractical. In a basic working set algorithm, every single page fault triggers a linear scan across <strong>all</strong> allocated page table entries to evaluate whether their age exceeds $\tau$. On systems with gigabytes of RAM and hundreds of thousands of frames, this $O(N)$ traversal consumes an unacceptable number of CPU cycles.
        </p>

        <h2>2. The WSClock Innovation: Circular List with Asynchronous Flushing</h2>
        <p>
          To solve this problem, Carr and Hennessy formulated <strong>WSClock</strong>. Like the standard Clock algorithm, all allocated page frames are linked in a circular ring traversed by a single moving hand. When a page fault occurs, the hand examines the page pointed to and evaluates four specific criteria:
        </p>
        <div class="theory-callout">
          <strong>WSClock Decision Logic per Frame:</strong><br>
          Let $T_{\text{current}}$ be the process's current virtual execution time, and let $\tau$ be the working set age threshold.<br>
          1. <strong>If $R = 1$:</strong> The page was referenced recently. Clear $R \leftarrow 0$, update $\text{Time of Last Use} \leftarrow T_{\text{current}}$, and advance the hand.<br>
          2. <strong>If $R = 0$ and $(T_{\text{current}} - \text{Time}) \le \tau$:</strong> The page is still within the active working set window. Do not evict; advance the hand.<br>
          3. <strong>If $R = 0$ and $(T_{\text{current}} - \text{Time}) > \tau$ and $M = 0$:</strong> The page is cold and clean. <strong>Immediate Victim!</strong> Evict this page, claim the frame, and finish.<br>
          4. <strong>If $R = 0$ and $(T_{\text{current}} - \text{Time}) > \tau$ and $M = 1$:</strong> The page is cold but dirty. To avoid blocking the CPU, schedule an <strong>asynchronous disk write</strong> and keep advancing the hand in search of a clean candidate.
        </div>

        <h2>3. Handling Full Hand Sweeps</h2>
        <p>
          If the clock hand completes a full 360-degree rotation without finding an evicted clean page:
        </p>
        <ul style="padding-left: 20px; display: flex; flex-direction: column; gap: 6px; margin-bottom: 10px;">
          <li><strong>If at least one write was scheduled:</strong> The hand continues advancing until the first scheduled write completes, allowing that newly clean frame to be reclaimed.</li>
          <li><strong>If no writes were scheduled:</strong> All resident pages have $R=1$ or are within the working set $\tau$. The process is genuinely thrashing under severe memory pressure, so the OS picks the first clean page it encounters or falls back to standard Clock.</li>
        </ul>
      </div>

      <!-- Embedded SVG Diagram for WSClock -->
      <div class="figure-container">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure 3-20: The WSClock Ring Architecture (Tanenbaum)</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 340" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #ffffff;">
          <defs>
            <marker id="arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
            </marker>
          </defs>

          <!-- Title -->
          <text x="380" y="26" font-size="14" font-weight="700" fill="#0f172a" text-anchor="middle">WSClock Circular Frame Ring Structure</text>
          <text x="380" y="44" font-size="11" fill="#64748b" text-anchor="middle">Circular buffer of physical frames evaluating R-bit, Modified-bit, and Age delta (Current Time - Last Use)</text>

          <!-- Circular Ring Path -->
          <circle cx="380" cy="190" r="115" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="6"/>

          <!-- Frame Node 0 (Top) -->
          <g transform="translate(380, 75)">
            <rect x="-65" y="-22" width="130" height="44" rx="5" fill="#f8fafc" stroke="#334155" stroke-width="1.5"/>
            <text x="0" y="-4" font-size="11" font-weight="700" fill="#0369a1" text-anchor="middle">Frame 0 (Page A)</text>
            <text x="0" y="12" font-size="9.5" font-family="monospace" fill="#334155" text-anchor="middle">R=1 | M=0 | T=2184</text>
          </g>

          <!-- Frame Node 1 (Right) -->
          <g transform="translate(495, 190)">
            <rect x="-65" y="-22" width="130" height="44" rx="5" fill="#f8fafc" stroke="#334155" stroke-width="1.5"/>
            <text x="0" y="-4" font-size="11" font-weight="700" fill="#0369a1" text-anchor="middle">Frame 1 (Page B)</text>
            <text x="0" y="12" font-size="9.5" font-family="monospace" fill="#334155" text-anchor="middle">R=0 | M=1 | T=1020</text>
          </g>

          <!-- Frame Node 2 (Bottom) -->
          <g transform="translate(380, 305)">
            <rect x="-65" y="-22" width="130" height="44" rx="5" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
            <text x="0" y="-4" font-size="11" font-weight="700" fill="#b91c1c" text-anchor="middle">Frame 2 (Page C)</text>
            <text x="0" y="12" font-size="9.5" font-family="monospace" fill="#991b1b" text-anchor="middle">R=0 | M=0 | T=850</text>
          </g>

          <!-- Frame Node 3 (Left) -->
          <g transform="translate(265, 190)">
            <rect x="-65" y="-22" width="130" height="44" rx="5" fill="#f8fafc" stroke="#334155" stroke-width="1.5"/>
            <text x="0" y="-4" font-size="11" font-weight="700" fill="#0369a1" text-anchor="middle">Frame 3 (Page D)</text>
            <text x="0" y="12" font-size="9.5" font-family="monospace" fill="#334155" text-anchor="middle">R=0 | M=0 | T=2140</text>
          </g>

          <!-- Clock Center & Moving Hand -->
          <circle cx="380" cy="190" r="16" fill="#0284c7"/>
          <line x1="380" y1="190" x2="380" y2="280" stroke="#0284c7" stroke-width="3" marker-end="url(#arr)"/>
          <text x="380" y="194" font-size="9" font-weight="700" fill="#ffffff" text-anchor="middle">HAND</text>

          <!-- Annotation pointing to Frame 2 victim -->
          <path d="M 450 305 L 530 305" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="3"/>
          <text x="540" y="302" font-size="10.5" font-weight="700" fill="#dc2626">Victim Evicted!</text>
          <text x="540" y="316" font-size="9" fill="#475569">R=0, Age > tau (1350 > 400), M=0</text>
        </svg>
      </div>
    </div>

    <!-- 2. INTERACTIVE GUIDED WALKTHROUGH -->
    <div class="card tutorial-panel">
      <div class="tutorial-header">
        <span id="wtCounter">Step 1 of 4</span>
        <span>Guided Walkthrough: Hand Evaluation Cases</span>
      </div>
      <div id="wtTitle" class="tutorial-title">1. The R = 1 Case (Recently Active)</div>

      <div class="split-grid">
        <div style="background:#fff; border:1px solid var(--border); border-radius:8px; padding:14px; display:flex; flex-direction:column; gap:10px;">
          <span style="font-family:var(--font-mono); font-size:0.8rem; font-weight:700; color:var(--text-muted); text-transform:uppercase;">Hand Inspector (Current Frame)</span>
          <div id="wtFrameBox" style="font-family:var(--font-mono); font-size:0.85rem; padding:10px; border-radius:6px; background:#f8fafc; border:1px solid var(--border);"></div>
          <div id="wtMathSummary" style="font-family:var(--font-mono); font-size:0.85rem; color:var(--accent); font-weight:700;"></div>
        </div>

        <div style="display:flex; flex-direction:column; justify-content:space-between; height:100%; gap:12px;">
          <div id="wtText" class="tutorial-body"></div>
          <div class="tour-nav">
            <button id="wtPrevBtn" class="btn-sec" onclick="stepWtBackward()">Previous</button>
            <button id="wtNextBtn" onclick="stepWtForward()">Next Case &rarr;</button>
            <button class="btn-sec" style="margin-left:auto;" onclick="document.getElementById('sandboxSection').scrollIntoView({behavior:'smooth'})">Jump to Simulator &darr;</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. INTERACTIVE WSCLOCK SANDBOX -->
    <div class="card" id="sandboxSection">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
          <h2 style="font-size:1.25rem; font-weight:700;">Part 3: Interactive WSClock Ring Simulator</h2>
          <p style="font-size:0.85rem; color:var(--text-muted); margin-top:2px;">
            Advance the clock hand, trigger page faults, and observe age thresholds and dirty write flushes.
          </p>
        </div>
        <div style="display:flex; gap:8px;">
          <button class="btn-sec" onclick="resetSimulator()">Reset Ring</button>
        </div>
      </div>

      <!-- Controls -->
      <div style="display:flex; gap:14px; align-items:center; flex-wrap:wrap; background:#f8fafc; padding:12px 14px; border:1px solid var(--border); border-radius:6px;">
        <button onclick="triggerFault()">Trigger Page Fault (Advance Hand)</button>
        <label style="font-size:0.85rem; font-weight:600;">Working Set Threshold ($\tau$):</label>
        <input type="range" id="tauSlider" min="100" max="800" value="400" oninput="updateTau(this.value)">
        <span id="tauVal" style="font-family:var(--font-mono); font-weight:700; color:var(--accent);">400 ticks</span>
        <span style="margin-left:auto; font-size:0.85rem; font-family:var(--font-mono); font-weight:700;">Virtual Time: <span id="virtTimeDisplay" style="color:#0284c7;">2200</span></span>
      </div>

      <!-- Telemetry Banner -->
      <div class="telemetry-box">
        <span>Clock Hand Index: <strong id="handIdxDisplay" style="color:#38bdf8;">Frame 0</strong></span>
        <span>Total Faults: <strong id="statFaults" style="color:#f87171;">0</strong></span>
        <span>Dirty Writes Queued: <strong id="statWrites" style="color:#facc15;">0</strong></span>
        <span>Clean Evictions: <strong id="statEvictions" style="color:#4ade80;">0</strong></span>
      </div>

      <div class="split-grid">
        <!-- Circular Buffer Table -->
        <div>
          <span style="font-weight:700; font-size:0.85rem; color:var(--text-muted); text-transform:uppercase;">Circular Buffer Frames</span>
          <table class="table-spec" style="margin-top:6px;">
            <thead>
              <tr><th>Frame</th><th>Page</th><th>R</th><th>M</th><th>Last Used</th><th>Age</th><th>Status</th></tr>
            </thead>
            <tbody id="ringTableBody"></tbody>
          </table>
        </div>

        <!-- Kernel Log -->
        <div style="display:flex; flex-direction:column; gap:6px;">
          <span style="font-weight:700; font-size:0.85rem; color:var(--text-muted); text-transform:uppercase;">Kernel WSClock Execution Trace</span>
          <div id="wsLog" class="terminal-box"></div>
        </div>
      </div>
    </div>

  </div>

  <script>
    /* =========================================================================
       PART 2: GUIDED WALKTHROUGH LOGIC
       ========================================================================= */
    let wtStep = 0;
    const wtCases = [
      {
        title: "1. The R = 1 Case (Recently Active)",
        text: "The hand inspects a frame where the hardware Referenced bit $R = 1$. The process has touched this page recently. Evicting it would risk thrashing. The algorithm clears $R \leftarrow 0$, updates its timestamp to current virtual time, and advances to the next frame.",
        frame: { name: "Page A (Frame 0)", r: 1, m: 0, time: 2180, currTime: 2200, tau: 400 },
        math: "R = 1 &rarr; Set R=0, Last_Use = 2200. Advance hand without evicting."
      },
      {
        title: "2. The R = 0, Age <= tau Case (Resident in Working Set)",
        text: "The hand inspects a frame with $R = 0$, but its age $(2200 - 1950 = 250)$ is less than or equal to threshold $\tau = 400$. Even though it wasn't touched in the latest slice, it still belongs to the process's working set. The hand steps over it.",
        frame: { name: "Page B (Frame 1)", r: 0, m: 0, time: 1950, currTime: 2200, tau: 400 },
        math: "Age = (2200 - 1950) = 250 <= tau (400) &rarr; Keep page in RAM."
      },
      {
        title: "3. The R = 0, Age > tau, M = 0 Case (Clean Eviction!)",
        text: "The hand inspects a frame with $R = 0$, an age $(2200 - 1600 = 600)$ greater than $\tau$, and a clean Modified bit $M = 0$. This page is officially out of the working set and requires no disk flush. It is evicted immediately!",
        frame: { name: "Page C (Frame 2)", r: 0, m: 0, time: 1600, currTime: 2200, tau: 400 },
        math: "Age = 600 > tau, M = 0 &rarr; EVICTED IMMEDIATELY (Zero I/O penalty)."
      },
      {
        title: "4. The R = 0, Age > tau, M = 1 Case (Asynchronous Dirty Flush)",
        text: "The hand inspects a frame whose age exceeds $\tau$, but $M = 1$ (dirty). The data must be preserved on disk before the frame can be claimed. Instead of stalling the CPU, WSClock issues an asynchronous disk write and keeps advancing.",
        frame: { name: "Page D (Frame 3)", r: 0, m: 1, time: 1500, currTime: 2200, tau: 400 },
        math: "Age = 700 > tau, M = 1 &rarr; Schedule Async Disk Write. Keep advancing hand."
      }
    ];

    function renderWt() {
      const c = wtCases[wtStep];
      document.getElementById("wtCounter").textContent = `Case ${wtStep + 1} of ${wtCases.length}`;
      document.getElementById("wtTitle").textContent = c.title;
      document.getElementById("wtText").innerHTML = c.text;

      const f = c.frame;
      const age = f.currTime - f.time;
      document.getElementById("wtFrameBox").innerHTML = `
        <strong>${f.name}</strong><br>
        Referenced (R): <strong>${f.r}</strong> | Modified (M): <strong>${f.m}</strong><br>
        Last Used: <strong>${f.time}</strong> | Current Time: <strong>${f.currTime}</strong> | Age: <strong>${age}</strong> (Threshold &tau;=${f.tau})
      `;
      document.getElementById("wtMathSummary").innerHTML = c.math;

      document.getElementById("wtPrevBtn").disabled = (wtStep === 0);
      document.getElementById("wtNextBtn").disabled = (wtStep === wtCases.length - 1);
    }

    function stepWtForward() {
      if (wtStep < wtCases.length - 1) { wtStep++; renderWt(); }
      document.activeElement.blur();
    }
    function stepWtBackward() {
      if (wtStep > 0) { wtStep--; renderWt(); }
      document.activeElement.blur();
    }
    renderWt();

    /* =========================================================================
       PART 3: LIVE SIMULATOR LOGIC
       ========================================================================= */
    let tau = 400;
    let virtualTime = 2200;
    let handIdx = 0;
    let statFaults = 0;
    let statWrites = 0;
    let statEvictions = 0;

    let frames = [
      { id: 0, page: "A", r: 1, m: 0, lastUse: 2184 },
      { id: 1, page: "B", r: 0, m: 1, lastUse: 1200 },
      { id: 2, page: "C", r: 0, m: 0, lastUse: 850 },
      { id: 3, page: "D", r: 0, m: 0, lastUse: 2140 },
      { id: 4, page: "E", r: 1, m: 1, lastUse: 2190 },
      { id: 5, page: "F", r: 0, m: 1, lastUse: 1500 }
    ];

    function logSim(msg) {
      const term = document.getElementById("wsLog");
      const row = document.createElement("div");
      row.className = "log-row";
      row.textContent = `> ${msg}`;
      term.prepend(row);
    }

    function renderRingTable(victimIdx = -1) {
      const tbody = document.getElementById("ringTableBody");
      tbody.innerHTML = "";

      frames.forEach((f, idx) => {
        const tr = document.createElement("tr");
        const age = virtualTime - f.lastUse;
        const isHand = (idx === handIdx);
        const isVictim = (idx === victimIdx);

        if (isVictim) tr.className = "victim-row";
        else if (isHand) tr.className = "hand-active";

        tr.innerHTML = `
          <td>Frame ${f.id} ${isHand ? '👉 [HAND]' : ''}</td>
          <td><strong>${f.page}</strong></td>
          <td>${f.r}</td>
          <td>${f.m}</td>
          <td>${f.lastUse}</td>
          <td>${age}</td>
          <td>${isVictim ? '<span style="color:#b91c1c;font-weight:700;">CLAIMED</span>' : (age <= tau ? 'Active WS' : (f.m ? 'Dirty' : 'Clean Candidate'))}</td>
        `;
        tbody.appendChild(tr);
      });

      document.getElementById("handIdxDisplay").textContent = `Frame ${handIdx}`;
      document.getElementById("virtTimeDisplay").textContent = virtualTime;
      document.getElementById("statFaults").textContent = statFaults;
      document.getElementById("statWrites").textContent = statWrites;
      document.getElementById("statEvictions").textContent = statEvictions;
    }

    function updateTau(val) {
      tau = parseInt(val, 10);
      document.getElementById("tauVal").textContent = `${tau} ticks`;
      renderRingTable();
    }

    function triggerFault() {
      statFaults++;
      virtualTime += 50;
      logSim(`--------------------------------------------------`);
      logSim(`Page fault at Virtual Time = ${virtualTime}. Scanning from Frame ${handIdx}...`);

      let evicted = false;

      for (let i = 0; i < frames.length * 2; i++) {
        let f = frames[handIdx];
        let age = virtualTime - f.lastUse;

        // Case 1: R = 1
        if (f.r === 1) {
          f.r = 0;
          f.lastUse = virtualTime;
          logSim(`Frame ${f.id} (${f.page}): R=1. Reset R=0, updated lastUse=${virtualTime}. Hand advances.`);
          handIdx = (handIdx + 1) % frames.length;
          continue;
        }

        // Case 2: R = 0, Age <= tau
        if (age <= tau) {
          logSim(`Frame ${f.id} (${f.page}): R=0, but Age=${age} <= tau(${tau}). In Working Set. Hand advances.`);
          handIdx = (handIdx + 1) % frames.length;
          continue;
        }

        // Case 3: R = 0, Age > tau, M = 0 (Clean eviction)
        if (f.m === 0) {
          logSim(`Frame ${f.id} (${f.page}): R=0, Age=${age} > tau(${tau}), Clean (M=0). EVICTED!`);
          statEvictions++;
          let oldPage = f.page;
          f.page = String.fromCharCode(65 + Math.floor(Math.random() * 26));
          f.r = 1;
          f.m = 0;
          f.lastUse = virtualTime;
          renderRingTable(f.id);
          handIdx = (handIdx + 1) % frames.length;
          evicted = true;
          logSim(`Loaded new Page '${f.page}' into Frame ${f.id}. Next Hand -> Frame ${handIdx}.`);
          break;
        }

        // Case 4: R = 0, Age > tau, M = 1 (Dirty write scheduled)
        if (f.m === 1) {
          statWrites++;
          f.m = 0;
          logSim(`Frame ${f.id} (${f.page}): R=0, Age=${age} > tau(${tau}), Dirty (M=1). Scheduled Async Disk Write. Cleared M.`);
          handIdx = (handIdx + 1) % frames.length;
        }
      }

      if (!evicted) {
        logSim(`Full ring scan completed. Evicting first available clean candidate.`);
        renderRingTable();
      }
    }

    function resetSimulator() {
      tau = 400;
      virtualTime = 2200;
      handIdx = 0;
      statFaults = 0;
      statWrites = 0;
      statEvictions = 0;
      frames = [
        { id: 0, page: "A", r: 1, m: 0, lastUse: 2184 },
        { id: 1, page: "B", r: 0, m: 1, lastUse: 1200 },
        { id: 2, page: "C", r: 0, m: 0, lastUse: 850 },
        { id: 3, page: "D", r: 0, m: 0, lastUse: 2140 },
        { id: 4, page: "E", r: 1, m: 1, lastUse: 2190 },
        { id: 5, page: "F", r: 0, m: 1, lastUse: 1500 }
      ];
      document.getElementById("tauSlider").value = 400;
      document.getElementById("tauVal").textContent = "400 ticks";
      document.getElementById("wsLog").innerHTML = "";
      logSim("WSClock simulator reset to default state.");
      renderRingTable();
    }

    renderRingTable();
    logSim("WSClock simulator initialized with 6 physical frames.");
  </script>
</body>
</html>
"""

COMMIT_MSG = """Add Carr and Hennessy pioneer sidebar to 10-wsclock.html

Introduce a floating bio sidebar in 10-wsclock.html honoring Richard W.
Carr and John L. Hennessy for formulating the WSClock algorithm in
1981. Format the sidebar to float on the right with prose wrapping,
matching the layout established in the working set module."""

def run_git_step(cmd, step_desc):
    print(f"--> {step_desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout.strip():
        print(res.stdout.strip())
    if res.stderr.strip():
        print(f"[{step_desc} stderr]\n{res.stderr.strip()}")
    if res.returncode != 0:
        print(f"Error during {step_desc} (exit code {res.returncode})", file=sys.stderr)
        sys.exit(res.returncode)

def sync_module():
    target_module = "week09-memory-management/10-wsclock.html"
    os.makedirs(os.path.dirname(target_module), exist_ok=True)
    with open(target_module, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Wrote updated module to {target_module}")

    run_git_step(["git", "add", target_module], "Staging updated 10-wsclock.html")
    run_git_step(["git", "commit", "-a", "-m", COMMIT_MSG], "Committing with -a -m")
    run_git_step(["git", "push", "origin", "main"], "Pushing main to origin")
    print("--> Successfully updated, committed, and pushed to origin/main.")

if __name__ == "__main__":
    sync_module()
