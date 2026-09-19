#!/usr/bin/env python3
import os
import re
import subprocess
import sys

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>11. Local vs. Global Allocation Policies — COSC240</title>
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
      --proc-a: #0284c7;
      --proc-b: #7c3aed;
      --proc-c: #16a34a;
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
      outline: none;
    }
    .tutorial-body {
      font-size: 0.93rem;
      line-height: 1.65;
      color: #0c4a6e;
      min-height: 90px;
    }

    .tour-nav {
      display: flex;
      gap: 10px;
      align-items: center;
      margin-top: 8px;
    }

    .split-grid {
      display: grid;
      grid-template-columns: 500px 1fr;
      gap: 20px;
      align-items: start;
      margin-top: 10px;
    }
    @media (max-width: 900px) {
      .split-grid { grid-template-columns: 1fr; }
    }

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
      height: 220px;
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
      user-select: none;
      transition: background-color 0.15s ease, opacity 0.15s ease;
    }
    button:hover:not(:disabled) { background-color: var(--accent-hover); }
    button:disabled {
      opacity: 0.45;
      cursor: not-allowed;
      pointer-events: none;
    }
    button.btn-sec {
      background-color: #f1f5f9;
      color: var(--text);
      border: 1px solid var(--border);
    }
    button.btn-sec:hover:not(:disabled) { background-color: #e2e8f0; }

    /* Sandbox Ram Slots */
    .ram-pool-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      margin-top: 8px;
    }
    .ram-slot {
      background: #f1f5f9;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 10px;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 0.8rem;
      display: flex;
      flex-direction: column;
      gap: 4px;
      min-height: 65px;
      justify-content: center;
    }
    .ram-slot.slot-a { background: #e0f2fe; border-color: #0284c7; color: #0369a1; font-weight: 700; }
    .ram-slot.slot-b { background: #ede9fe; border-color: #7c3aed; color: #6d28d9; font-weight: 700; }
    .ram-slot.slot-c { background: #dcfce7; border-color: #16a34a; color: #15803d; font-weight: 700; }
  </style>
</head>
<body>

  <div class="nav-back">
    <a href="index.html">&larr; Back to Week Overview</a>
  </div>

  <header>
    <h1>11. Local vs. Global Allocation Policies</h1>
    <p class="subtitle">Tanenbaum Section 3.5.1 (Fig. 3-22): Process-local replacement quotas versus system-wide global frame allocation under memory pressure.</p>
  </header>

  <div class="main-container">

    <!-- 1. THEORY SECTION -->
    <div class="card">
      <div class="theory-section">
        <h2>1. The Core Allocation Dilemma in Multiprogramming</h2>
        <p>
          When multiple processes run concurrently in a virtual memory operating system, physical RAM must be divided among them. If a running process suffers a page fault and all physical frames are occupied, the kernel must select a resident page to evict. The foundational policy question is: <strong>Should the victim be chosen exclusively from the faulting process's own allocated frames, or from any frame in the entire machine?</strong>
        </p>

        <h2>2. Local Allocation Policies</h2>
        <p>
          A <strong>local replacement policy</strong> assigns each active process a fixed quota of physical page frames (e.g., determined at process startup based on executable size or dynamic working set estimation). When a page fault occurs, the kernel chooses a replacement victim strictly from the pages owned by that specific process.
        </p>
        <ul style="padding-left: 20px; display: flex; flex-direction: column; gap: 6px; margin-bottom: 10px;">
          <li><strong>Pros (Isolation):</strong> Processes are isolated from one another. A poorly written, thrashing program cannot steal frames from other well-behaved applications.</li>
          <li><strong>Cons (Inflexibility):</strong> If a process enters a heavy compute phase requiring more memory, it cannot borrow idle frames from an inactive process, leading to artificial page faults and suboptimal performance.</li>
        </ul>

        <h2>3. Global Allocation Policies</h2>
        <p>
          A <strong>global replacement policy</strong> treats all physical memory frames in the machine as a unified, shared pool. When any process incurs a page fault, the kernel selects a replacement victim from the entire system-wide population of resident pages, regardless of which process owns them.
        </p>
        <ul style="padding-left: 20px; display: flex; flex-direction: column; gap: 6px; margin-bottom: 10px;">
          <li><strong>Pros (Adaptability):</strong> Highly efficient. If Process A is idle, its resident frames naturally migrate to Process B if B's working set is expanding. Overall system throughput is maximized.</li>
          <li><strong>Cons (Vulnerability):</strong> Lack of isolation. A runaway or thrashing program can continuously steal frames from other processes, dragging down system-wide responsiveness.</li>
        </ul>

        <!-- Embedded SVG Diagram: Tanenbaum Figure 3-22 -->
        <div class="figure-container">
          <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure 3-22: Local vs. Global Page Replacement (Tanenbaum)</span>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 260" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #ffffff;">
            <defs>
              <marker id="arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#334155" />
              </marker>
            </defs>

            <!-- (a) Original Configuration -->
            <rect x="30" y="30" width="200" height="190" fill="#f8fafc" stroke="#334155" stroke-width="1.5" rx="6"/>
            <text x="130" y="52" font-size="11" font-weight="700" fill="#0f172a" text-anchor="middle">(a) Original Configuration</text>
            <rect x="50" y="70" width="160" height="60" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.2" rx="4"/>
            <text x="130" y="95" font-size="10" font-weight="700" fill="#0369a1" text-anchor="middle">Process A (5 Frames)</text>
            <rect x="50" y="145" width="160" height="60" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.2" rx="4"/>
            <text x="130" y="170" font-size="10" font-weight="700" fill="#6d28d9" text-anchor="middle">Process B (5 Frames)</text>

            <!-- Arrow 1 -->
            <line x1="240" y1="125" x2="275" y2="125" stroke="#334155" stroke-width="1.5" marker-end="url(#arr)"/>

            <!-- (b) Local Replacement -->
            <rect x="285" y="30" width="200" height="190" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5" rx="6"/>
            <text x="385" y="52" font-size="11" font-weight="700" fill="#15803d" text-anchor="middle">(b) Local Replacement</text>
            <rect x="305" y="70" width="160" height="60" fill="#ffffff" stroke="#16a34a" stroke-width="1.2" rx="4"/>
            <text x="385" y="95" font-size="10" font-weight="700" fill="#15803d" text-anchor="middle">Process A faults:</text>
            <text x="385" y="112" font-size="9" fill="#166534" text-anchor="middle">Evicts only from A's quota</text>
            <rect x="305" y="145" width="160" height="60" fill="#ffffff" stroke="#16a34a" stroke-width="1.2" rx="4"/>
            <text x="385" y="170" font-size="10" font-weight="700" fill="#15803d" text-anchor="middle">Process B unaffected</text>
            <text x="385" y="187" font-size="9" fill="#166534" text-anchor="middle">Quotas remain strictly 5/5</text>

            <!-- Arrow 2 -->
            <line x1="495" y1="125" x2="530" y2="125" stroke="#334155" stroke-width="1.5" marker-end="url(#arr)"/>

            <!-- (c) Global Replacement -->
            <rect x="540" y="30" width="190" height="190" fill="#fef3c7" stroke="#d97706" stroke-width="1.5" rx="6"/>
            <text x="635" y="52" font-size="11" font-weight="700" fill="#b45309" text-anchor="middle">(c) Global Replacement</text>
            <rect x="555" y="70" width="160" height="60" fill="#ffffff" stroke="#d97706" stroke-width="1.2" rx="4"/>
            <text x="635" y="95" font-size="10" font-weight="700" fill="#92400e" text-anchor="middle">Process A faults:</text>
            <text x="635" y="112" font-size="9" fill="#b45309" text-anchor="middle">Can steal frame from B!</text>
            <rect x="555" y="145" width="160" height="60" fill="#ffffff" stroke="#d97706" stroke-width="1.2" rx="4"/>
            <text x="635" y="170" font-size="10" font-weight="700" fill="#92400e" text-anchor="middle">Dynamic Quotas:</text>
            <text x="635" y="187" font-size="9" fill="#b45309" text-anchor="middle">A grows (6), B shrinks (4)</text>
          </svg>
        </div>
      </div>
    </div>

    <!-- 2. INTERACTIVE GUIDED WALKTHROUGH -->
    <div class="card tutorial-panel">
      <div class="tutorial-header">
        <span id="wtCounter">Step 1 of 4</span>
        <span>Guided Walkthrough: Allocation Mechanics</span>
      </div>
      <div id="wtTitle" class="tutorial-title" tabindex="-1">1. The Baseline Multiprogramming State</div>
      <div class="tutorial-body" id="wtText"></div>
      <div class="tour-nav">
        <button type="button" id="wtPrevBtn" class="btn-sec" onclick="stepWtBackward()">Previous</button>
        <button type="button" id="wtNextBtn" onclick="stepWtForward()">Next Step &rarr;</button>
        <button type="button" class="btn-sec" style="margin-left:auto;" onclick="document.getElementById('sandboxSection').scrollIntoView({behavior:'smooth'})">Jump to Sandbox &darr;</button>
      </div>
    </div>

    <!-- 3. INTERACTIVE ALLOCATION SANDBOX -->
    <div class="card" id="sandboxSection">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
          <h2 style="font-size:1.25rem; font-weight:700;">Part 3: Interactive Multi-Process Allocation Sandbox</h2>
          <p style="font-size:0.85rem; color:var(--text-muted); margin-top:2px;">
            Trigger page faults for Process A or Process B under Local vs. Global allocation policies and observe frame ownership.
          </p>
        </div>
        <div style="display:flex; gap:8px;">
          <button type="button" class="btn-sec" onclick="resetSandbox()">Reset Sandbox</button>
        </div>
      </div>

      <!-- Controls -->
      <div style="display:flex; gap:14px; align-items:center; flex-wrap:wrap; background:#f8fafc; padding:12px 14px; border:1px solid var(--border); border-radius:6px;">
        <label style="font-size:0.85rem; font-weight:600;">Policy Mode:</label>
        <select id="policySelect" onchange="switchPolicy(this.value)" style="padding:5px 10px; font-family:var(--font-mono); font-size:0.85rem; border:1px solid var(--border); border-radius:4px;">
          <option value="local">Local Allocation (Fixed Quotas)</option>
          <option value="global">Global Allocation (Shared Pool)</option>
        </select>

        <div style="display:flex; gap:8px; margin-left:auto;">
          <button type="button" onclick="faultProcess('A')" style="background:#0284c7;">Fault Process A</button>
          <button type="button" onclick="faultProcess('B')" style="background:#7c3aed;">Fault Process B</button>
        </div>
      </div>

      <!-- Telemetry Banner -->
      <div class="telemetry-box">
        <span>Active Policy: <strong id="statPolicy" style="color:#38bdf8;">Local Allocation</strong></span>
        <span>Process A Frames: <strong id="statFramesA" style="color:#38bdf8;">4</strong></span>
        <span>Process B Frames: <strong id="statFramesB" style="color:#a78bfa;">4</strong></span>
      </div>

      <div class="split-grid">
        <!-- Physical RAM Pool (8 Frames) -->
        <div>
          <span style="font-weight:700; font-size:0.85rem; color:var(--text-muted); text-transform:uppercase;">Physical RAM Pool (8 Total Frames)</span>
          <div id="ramPoolGrid" class="ram-pool-grid"></div>
        </div>

        <!-- Kernel Event Log -->
        <div style="display:flex; flex-direction:column; gap:6px;">
          <span style="font-weight:700; font-size:0.85rem; color:var(--text-muted); text-transform:uppercase;">Kernel Allocation Event Log</span>
          <div id="sandboxLog" class="terminal-box"></div>
        </div>
      </div>
    </div>

  </div>

  <script>
    /* =========================================================================
       PART 2: GUIDED WALKTHROUGH LOGIC
       ========================================================================= */
    let wtStep = 0;
    const wtSteps = [
      {
        title: "1. The Baseline Multiprogramming State",
        text: "Consider a computer with 8 physical frames shared between two active processes, Process A and Process B. In the initial baseline state, each process is allocated an equal quota of 4 frames."
      },
      {
        title: "2. Page Fault Under Local Allocation",
        text: "Process A incurs a page fault. Under a <strong>Local Allocation</strong> policy, the operating system is restricted to choosing a victim page exclusively from Process A's own 4 frames. Even if Process B is completely idle and has cold pages, Process A cannot touch them."
      },
      {
        title: "3. Page Fault Under Global Allocation",
        text: "Now consider the same page fault under a <strong>Global Allocation</strong> policy. The kernel scans all 8 frames across the entire machine. If Process B's page was accessed less recently than Process A's candidate, Process B's frame is seized and reassigned to Process A. Process A's quota grows to 5 while Process B shrinks to 3."
      },
      {
        title: "4. Trade-Offs: Protection vs. Efficiency",
        text: "Local allocation provides rigid isolation, ensuring processes cannot starve each other, but it wastes memory when workloads fluctuate. Global allocation maximizes RAM utilization across active tasks, but exposes well-behaved applications to memory hogging by runaway threads."
      }
    ];

    function renderWt() {
      const s = wtSteps[wtStep];
      document.getElementById("wtCounter").textContent = `Step ${wtStep + 1} of ${wtSteps.length}`;
      document.getElementById("wtTitle").textContent = s.title;
      document.getElementById("wtText").innerHTML = s.text;

      document.getElementById("wtPrevBtn").disabled = (wtStep === 0);
      document.getElementById("wtNextBtn").disabled = (wtStep === wtSteps.length - 1);
      document.getElementById("wtTitle").focus();
    }

    function stepWtForward() {
      if (wtStep < wtSteps.length - 1) {
        wtStep++;
        renderWt();
      }
    }

    function stepWtBackward() {
      if (wtStep > 0) {
        wtStep--;
        renderWt();
      }
    }

    renderWt();

    /* =========================================================================
       PART 3: LIVE SANDBOX LOGIC
       ========================================================================= */
    let policy = "local";
    let ramFrames = [
      { id: 0, owner: "A", age: 10 },
      { id: 1, owner: "A", age: 20 },
      { id: 2, owner: "A", age: 30 },
      { id: 3, owner: "A", age: 40 },
      { id: 4, owner: "B", age: 5 },
      { id: 5, owner: "B", age: 15 },
      { id: 6, owner: "B", age: 25 },
      { id: 7, owner: "B", age: 35 }
    ];

    function logSandbox(msg) {
      const term = document.getElementById("sandboxLog");
      const row = document.createElement("div");
      row.className = "log-row";
      row.textContent = `> ${msg}`;
      term.prepend(row);
    }

    function renderSandbox() {
      const grid = document.getElementById("ramPoolGrid");
      grid.innerHTML = "";

      let countA = 0;
      let countB = 0;

      ramFrames.forEach(f => {
        if (f.owner === "A") countA++;
        if (f.owner === "B") countB++;

        const div = document.createElement("div");
        div.className = `ram-slot slot-${f.owner.toLowerCase()}`;
        div.innerHTML = `
          <span>Frame #${f.id}</span>
          <strong>Proc ${f.owner}</strong>
          <span style="font-size:0.72rem; opacity:0.8;">Age: ${f.age}</span>
        `;
        grid.appendChild(div);
      });

      document.getElementById("statPolicy").textContent = (policy === "local" ? "Local Allocation (Fixed Quotas)" : "Global Allocation (Shared Pool)");
      document.getElementById("statFramesA").textContent = countA;
      document.getElementById("statFramesB").textContent = countB;
    }

    function switchPolicy(val) {
      policy = val;
      logSandbox(`Allocation policy switched to: ${policy.toUpperCase()}.`);
      renderSandbox();
    }

    function faultProcess(proc) {
      const targetProc = proc;
      const victimProc = (targetProc === "A" ? "B" : "A");

      logSandbox(`--------------------------------------------------`);
      logSandbox(`Page fault triggered by Process ${targetProc}!`);

      if (policy === "local") {
        // Local: find oldest frame owned by targetProc
        let oldestAge = -1;
        let victimIdx = -1;

        ramFrames.forEach((f, idx) => {
          if (f.owner === targetProc && f.age > oldestAge) {
            oldestAge = f.age;
            victimIdx = idx;
          }
        });

        if (victimIdx !== -1) {
          ramFrames[victimIdx].age = 0;
          // Age others
          ramFrames.forEach(f => f.age += 5);
          logSandbox(`LOCAL POLICY: Evicted Process ${targetProc}'s oldest frame (#${victimIdx}). Quotas strictly maintained.`);
        }
      } else {
        // Global: find oldest frame in the entire machine
        let oldestAge = -1;
        let victimIdx = -1;

        ramFrames.forEach((f, idx) => {
          if (f.age > oldestAge) {
            oldestAge = f.age;
            victimIdx = idx;
          }
        });

        if (victimIdx !== -1) {
          const stolenFrom = ramFrames[victimIdx].owner;
          ramFrames[victimIdx].owner = targetProc;
          ramFrames[victimIdx].age = 0;
          ramFrames.forEach(f => f.age += 5);
          logSandbox(`GLOBAL POLICY: Stole Frame #${victimIdx} from Process ${stolenFrom} and assigned to Process ${targetProc}!`);
        }
      }

      renderSandbox();
    }

    function resetSandbox() {
      policy = "local";
      document.getElementById("policySelect").value = "local";
      ramFrames = [
        { id: 0, owner: "A", age: 10 },
        { id: 1, owner: "A", age: 20 },
        { id: 2, owner: "A", age: 30 },
        { id: 3, owner: "A", age: 40 },
        { id: 4, owner: "B", age: 5 },
        { id: 5, owner: "B", age: 15 },
        { id: 6, owner: "B", age: 25 },
        { id: 7, owner: "B", age: 35 }
      ];
      document.getElementById("sandboxLog").innerHTML = "";
      logSandbox("Sandbox reset to baseline 4/4 frame distribution.");
      renderSandbox();
    }

    renderSandbox();
    logSandbox("Sandbox initialized with Local Allocation policy.");
  </script>
</body>
</html>
"""

COMMIT_MSG = """Add Local vs Global Allocation Policies module and update index

Implement 11-local-vs-global.html covering Tanenbaum Section 3.5.1
(Figure 3-22). Provide theoretical breakdown of process-local fixed
allocations versus system-wide global frame allocation under
multiprogrammed memory pressure.

Include a comparative SVG diagram, 4-step guided walkthrough, and an
interactive multi-process allocation sandbox. Update index.html to link
to 11-local-vs-global.html and mark it as published."""

def run_git_step(cmd, desc):
    print(f"--> {desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout.strip():
        print(res.stdout.strip())
    if res.stderr.strip():
        print(f"[{desc} stderr]\n{res.stderr.strip()}")
    if res.returncode != 0:
        print(f"Error during {desc} (code {res.returncode})", file=sys.stderr)
        sys.exit(res.returncode)

def sync_module_and_index():
    target_module = "week09-memory-management/11-local-vs-global.html"
    index_file = "week09-memory-management/index.html"

    # 1. Write 11-local-vs-global.html
    os.makedirs(os.path.dirname(target_module), exist_ok=True)
    with open(target_module, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Wrote module to {target_module}")

    # 2. Update index.html to point to 11-local-vs-global.html and mark published
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            idx_content = f.read()

        # Update link href and badge status for topic 11
        idx_content = re.sub(
            r'href=["\']11-local-vs-global\.html["\']',
            'href="11-local-vs-global.html"',
            idx_content
        )

        # Mark badge as published if draft
        idx_content = re.sub(
            r'(<a[^>]*href=["\']11-local-vs-global\.html["\'][^>]*>[\s\S]*?<span[^>]*class=["\'])badge\s+draft(["\']>)Draft(</span>)',
            r'\1badge completed published\2Published\3',
            idx_content
        )

        with open(index_file, "w", encoding="utf-8") as f:
            f.write(idx_content)
        print(f"Updated link and published badge in {index_file}")

    # 3. Git add, commit -a -m, and push
    run_git_step(["git", "add", target_module, index_file], "Staging files")
    run_git_step(["git", "commit", "-a", "-m", COMMIT_MSG], "Committing with -a -m")
    run_git_step(["git", "push", "origin", "main"], "Pushing main to origin")
    print("--> Local vs Global module created and index published successfully!")

if __name__ == "__main__":
    sync_module_and_index()
