#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand 04-realtime-multiprocessor.html in Week 3
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week03-process-scheduling", "04-realtime-multiprocessor.html")

MODULE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>04. Real-Time &amp; Multiprocessor Scheduling | Week 3: Process Scheduling</title>
  <style>
    :root {
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
      --text: #1e293b;
      --text-muted: #475569;
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --success: #059669;
      --warning: #d97706;
      --danger: #dc2626;
    }
    * { box-sizing: border-box; }
    body {
      font-family: var(--font-sans);
      color: var(--text);
      background: var(--bg);
      margin: 0;
      padding: 32px 16px;
      line-height: 1.6;
    }
    .container {
      max-width: 960px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    h1, h2, h3, h4, h5 { color: #0f172a; }
    h2 { border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 28px; }
    h3 { margin-top: 24px; margin-bottom: 8px; color: var(--accent); font-size: 1.2rem; }
    h4 { margin-top: 18px; margin-bottom: 6px; color: #334155; font-size: 1.02rem; }
    h5 { margin-top: 14px; margin-bottom: 4px; color: #475569; font-size: 0.92rem; text-transform: uppercase; letter-spacing: 0.04em; }
    p { color: var(--text-muted); margin-bottom: 12px; }
    ul, ol { margin-left: 20px; color: var(--text-muted); margin-bottom: 12px; }
    li { margin-bottom: 6px; }
    code { font-family: var(--font-mono); background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.88rem; color: #0369a1; }
    pre {
      background: #0f172a;
      color: #e2e8f0;
      padding: 16px;
      border-radius: 6px;
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      margin: 16px 0;
    }
    pre code {
      background: transparent !important;
      color: inherit !important;
      padding: 0 !important;
      border-radius: 0 !important;
      font-size: inherit !important;
    }

    .math-callout {
      background: #f8fafc;
      border-left: 4px solid var(--accent);
      padding: 14px 18px;
      margin: 16px 0;
      border-radius: 0 6px 6px 0;
      font-size: 0.9rem;
      color: #1e293b;
    }
    .math-callout strong { color: #0f172a; }

    .nav-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
    }
    .nav-bar a {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #334155;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.85rem;
      transition: background-color 0.15s ease, color 0.15s ease;
    }
    .nav-bar a:hover {
      background-color: #0f172a;
      color: #ffffff;
    }

    /* Directed Narrative Stepper Layout */
    .aid-wrapper {
      margin: 32px 0;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #ffffff;
      box-shadow: 0 2px 4px rgba(0,0,0,0.03);
      overflow: hidden;
    }
    .aid-header {
      background: #f1f5f9;
      padding: 12px 18px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }
    .aid-header h4 {
      margin: 0;
      font-size: 0.96rem;
      font-weight: 700;
      color: #0f172a;
    }
    .dimension-toggles {
      display: flex;
      gap: 6px;
    }
    .dim-btn {
      padding: 4px 12px;
      font-size: 0.78rem;
      font-weight: 600;
      border-radius: 4px;
      border: 1px solid var(--border);
      background: #ffffff;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .dim-btn.active {
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
    }
    .scenario-banner {
      background: #f8fafc;
      padding: 10px 18px;
      border-bottom: 1px solid var(--border);
      font-size: 0.85rem;
      color: #334155;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .scenario-tag {
      background: #e0f2fe;
      color: #0369a1;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }
    .telemetry-strip {
      background: #0f172a;
      color: #f8fafc;
      padding: 12px 18px;
      font-family: var(--font-mono);
      font-size: 0.8rem;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 10px 16px;
      border-bottom: 1px solid #1e293b;
    }
    .telemetry-cell {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .telemetry-label {
      color: #94a3b8;
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .telemetry-val {
      color: #38bdf8;
      font-weight: 600;
    }
    .telemetry-val.highlight { color: #4ade80; }
    .telemetry-val.alert { color: #f87171; }

    .canvas-container {
      background: #ffffff;
      padding: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      border-bottom: 1px solid var(--border);
    }
    svg.rt-canvas {
      width: 100%;
      max-width: 760px;
      height: auto;
      overflow: visible;
    }

    .controls-narrative-strip {
      padding: 14px 18px;
      background: #f8fafc;
      border-bottom: 1px solid var(--border);
      display: grid;
      grid-template-columns: auto 1fr;
      align-items: center;
      gap: 18px;
    }
    @media (max-width: 720px) {
      .controls-narrative-strip {
        grid-template-columns: 1fr;
      }
    }
    .stepper-btn-group {
      display: flex;
      gap: 8px;
      align-self: center;
    }
    .btn-step {
      padding: 7px 14px;
      font-size: 0.82rem;
      font-weight: 600;
      border-radius: 6px;
      border: 1px solid var(--border);
      background: #ffffff;
      color: #334155;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
    }
    .btn-step:hover:not(:disabled) {
      background: #0f172a;
      color: #ffffff;
    }
    .btn-step:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }
    .narrative-preview-panel {
      font-size: 0.84rem;
      line-height: 1.5;
      color: #334155;
      background: #ffffff;
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent);
      border-radius: 4px;
      padding: 10px 14px;
    }
    .narrative-preview-panel strong {
      color: #0f172a;
      display: block;
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 2px;
    }

    .analytical-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      background: var(--border);
      gap: 1px;
    }
    @media (max-width: 720px) {
      .analytical-grid { grid-template-columns: 1fr; }
    }
    .pane-card {
      background: #ffffff;
      padding: 18px;
    }
    .pane-title {
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .pane-title.what { color: var(--accent); }
    .pane-title.why { color: var(--success); }
    .pane-content {
      font-size: 0.88rem;
      line-height: 1.55;
      color: #334155;
      margin: 0;
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="03-interactive-scheduling.html">&larr; 03. Interactive Scheduling</a>
      <a href="index.html">&#127968; Week 3 Index</a>
      <span style="font-size: 0.85rem; font-weight: 700; color: #64748b;">Module 04 (Final)</span>
    </nav>

    <h2>04. Real-Time &amp; Multiprocessor Scheduling</h2>
    <p>
      In batch and interactive systems, scheduling algorithms optimize for statistical averages: mean turnaround time, maximum throughput, or average interactive response time. However, two specialized computing domains introduce physical and temporal constraints that break standard general-purpose queuing models:
    </p>
    <ul>
      <li><strong>Real-Time Systems:</strong> The correctness of a computation depends not only on its logical output, but on the <em>exact physical instant</em> that output is delivered. Missing a deadline can result in catastrophic physical failure.</li>
      <li><strong>Multiprocessor / Multicore Systems (SMP):</strong> Distributing runnable threads across multiple physical execution units creates hardware cache affinity bottlenecks, interconnect memory traffic (NUMA), and inter-core lock contention.</li>
    </ul>

    <h3>1. Real-Time Scheduling Foundations</h3>
    <p>
      Real-time systems are categorized by the operational consequence of missing a deadline:
    </p>
    <ul>
      <li><strong>Hard Real-Time:</strong> Absolute, deterministic timing constraints. Missing a single deadline by 1 microsecond represents a total system catastrophe (e.g., flight control fly-by-wire surfaces, automotive Anti-lock Braking Systems [ABS], cardiac pacemakers, nuclear reactor protection rods). Over-provisioning hardware and mathematical schedulability proofs are mandatory.</li>
      <li><strong>Soft Real-Time:</strong> Deadlines are critical for quality of service, but an occasional miss causes degraded user experience rather than destruction (e.g., 60 FPS video streaming, video game rendering, VoIP voice packet decoding). Missing a deadline drops a frame; the system continues operating.</li>
    </ul>

    <h4>The Periodic Task Formal Model</h4>
    <p>
      A classic real-time system executes a set of <i>n</i> periodic tasks, denoted &Tau; = {&tau;<sub>1</sub>, &tau;<sub>2</sub>, ..., &tau;<sub><i>n</i></sub>}. Each task &tau;<sub><i>i</i></sub> is characterized by three deterministic physical parameters:
    </p>
    <ul>
      <li><strong>Period (<i>P</i><sub><i>i</i></sub>):</strong> The time interval between successive releases or arrivals of the task.</li>
      <li><strong>Worst-Case Execution Time (<i>C</i><sub><i>i</i></sub>):</strong> The maximum continuous computation time required by the task on the target CPU core.</li>
      <li><strong>Deadline (<i>D</i><sub><i>i</i></sub>):</strong> The time relative to task arrival by which computation must complete. In standard synchronous models, the deadline equals the period: <code><i>D</i><sub><i>i</i></sub> = <i>P</i><sub><i>i</i></sub></code>.</li>
    </ul>

    <div class="math-callout">
      <strong>Total CPU Utilization (Load Factor, <i>U</i>):</strong>
      <br>
      The fraction of CPU execution bandwidth demanded by the periodic task set is the sum of their individual utilization ratios:
      <pre><code><i>U</i> = &sum;<sub><i>i</i>=1</sub><sup><i>n</i></sup> (<i>C</i><sub><i>i</i></sub> / <i>P</i><sub><i>i</i></sub>)</code></pre>
      <strong>Necessary Condition for Schedulability:</strong>
      <br>
      For any single-core hardware architecture, the task set cannot possibly be scheduled without missing deadlines if total utilization exceeds 100%:
      <pre><code><i>U</i> &le; 1.0</code></pre>
      If <i>U</i> &gt; 1.0, the task set is mathematically unschedulable under <em>any</em> algorithm.
    </div>

    <h3>2. Rate-Monotonic Scheduling (RMS)</h3>
    <p>
      Developed by C. L. Liu and James Layland (1973), <strong>Rate-Monotonic Scheduling (RMS)</strong> is the canonical static-priority scheduling algorithm for periodic real-time tasks:
    </p>
    <ul>
      <li><strong>Static Assignment Rule:</strong> Priorities are assigned to tasks prior to system execution based strictly on their <strong>rate</strong> (frequency of occurrence, <code>1 / <i>P</i><sub><i>i</i></sub></code>).</li>
      <li><strong>The Monotonic Priority Principle:</strong> <em>Tasks with shorter periods (higher rates) receive higher static priority.</em> Tasks with longer periods receive lower priority.</li>
      <li><strong>Preemption:</strong> If a high-priority task with a short period arrives while a low-priority task is running, the running task is immediately preempted.</li>
    </ul>

    <h4>The Liu &amp; Layland Schedulability Bound</h4>
    <p>
      Is a task set with <i>U</i> &le; 1.0 guaranteed to meet all deadlines under RMS? <strong>No.</strong> Because priorities are fixed statically, a long-period task can be repeatedly preempted by short-period tasks, missing its deadline even when spare CPU capacity exists.
    </p>
    <p>
      Liu and Layland proved that a set of <i>n</i> independent periodic tasks is <strong>guaranteed to be schedulable</strong> under Rate-Monotonic Scheduling if its total CPU utilization satisfies the following inequality:
    </p>
    <div class="math-callout">
      <pre><code><i>U</i> = &sum;<sub><i>i</i>=1</sub><sup><i>n</i></sup> (<i>C</i><sub><i>i</i></sub> / <i>P</i><sub><i>i</i></sub>) &le; <i>n</i>(2<sup>1/<i>n</i></sup> &minus; 1)</code></pre>
      Evaluating the bound across increasing task counts:
      <ul>
        <li><code><i>n</i> = 1:</code> <i>U</i> &le; 1(2<sup>1</sup> &minus; 1) = <strong>100%</strong></li>
        <li><code><i>n</i> = 2:</code> <i>U</i> &le; 2(2<sup>1/2</sup> &minus; 1) &approx; 2(1.414 &minus; 1) = <strong>82.8%</strong></li>
        <li><code><i>n</i> = 3:</code> <i>U</i> &le; 3(2<sup>1/3</sup> &minus; 1) &approx; 3(1.260 &minus; 1) = <strong>77.9%</strong></li>
        <li><code>As <i>n</i> &rarr; &infin;:</code> <code>lim<sub><i>n</i>&rarr;&infin;</sub> <i>n</i>(2<sup>1/<i>n</i></sup> &minus; 1) = ln(2) &approx; <strong>69.3%</strong></code></li>
      </ul>
      <strong>The 69.3% Invariant:</strong> If total utilization of any arbitrary periodic task set is below <strong>69.3%</strong>, Rate-Monotonic scheduling guarantees that <em>no deadline will ever be missed</em>. If utilization falls between 69.3% and 100%, the set may still be schedulable, but requires exact <strong>Response-Time Analysis (RTA)</strong> recurrence testing.
    </div>

    <h3>3. Earliest Deadline First (EDF)</h3>
    <p>
      To overcome the 69.3% static priority ceiling and achieve up to 100% CPU utilization, operating systems turn to <strong>Earliest Deadline First (EDF)</strong>.
    </p>
    <ul>
      <li><strong>Dynamic Priority Assignment:</strong> Unlike RMS, priorities under EDF are not fixed at compile time. Priorities are assigned dynamically at runtime.</li>
      <li><strong>The Dynamic Selection Rule:</strong> Whenever the scheduler evaluates runnable tasks, it selects the task whose <strong>absolute deadline (<i>d</i><sub><i>i</i></sub>)</strong> is closest to the current physical clock.</li>
      <li><strong>Preemption:</strong> If task &tau;<sub>2</sub> arrives with a deadline at <i>T</i> = 14 ms while task &tau;<sub>1</sub> is executing with a deadline at <i>T</i> = 18 ms, &tau;<sub>1</sub> is immediately preempted because 14 &lt; 18.</li>
    </ul>

    <h4>The Optimality of EDF</h4>
    <p>
      <strong>Theorem:</strong> Earliest Deadline First is an <em>optimal</em> dynamic uniprocessor scheduling algorithm. A set of periodic tasks with deadlines equal to periods is schedulable under EDF <strong>if and only if</strong>:
    </p>
    <pre><code><i>U</i> = &sum;<sub><i>i</i>=1</sub><sup><i>n</i></sup> (<i>C</i><sub><i>i</i></sub> / <i>P</i><sub><i>i</i></sub>) &le; 1.0 (100%)</code></pre>
    <p>
      EDF can fully saturate a processor execution core up to 100% capacity without missing a single deadline.
    </p>

    <h4>The Fatal Flaw of EDF: Domino Effect under Overload</h4>
    <p>
      Despite its theoretical optimality, EDF exhibits a dangerous vulnerability in mission-critical environments: <strong>the cascading domino effect during transient overloads</strong>.
    </p>
    <ul>
      <li><strong>RMS Under Overload:</strong> Under static Rate-Monotonic priorities, if a system experiences a spike where <i>U</i> = 1.20, high-priority tasks (short periods) continue running perfectly without missing deadlines. Only the lowest-priority background tasks miss deadlines. System failure is contained predictably.</li>
      <li><strong>EDF Under Overload:</strong> If <i>U</i> &gt; 1.0, EDF constantly prioritizes the task closest to failing its deadline. That task executes, misses its deadline anyway, and by doing so, delays the next upcoming task, causing it to miss its deadline as well. A single transient spike can cause <em>every task in the entire system to miss its deadline consecutively</em>.</li>
    </ul>

    <!-- Directed Narrative Stepper: RMS vs EDF Execution -->
    <div class="aid-wrapper">
      <div class="aid-header">
        <h4>Interactive Stepper: Static RMS vs. Dynamic EDF under High Utilization</h4>
        <div class="dimension-toggles">
          <button class="dim-btn active" id="dim-rms" onclick="setRtDim('rms')">Rate-Monotonic (RMS: Static)</button>
          <button class="dim-btn" id="dim-edf" onclick="setRtDim('edf')">Earliest Deadline First (EDF: Dynamic)</button>
        </div>
      </div>

      <div class="scenario-banner">
        <span class="scenario-tag">Workload Arc</span>
        <span id="rt-scenario-text">Task 1 (C1=2, P1=5; U1=0.40) and Task 2 (C2=4, P2=7; U2=0.57). Total U = 0.97 (97%). Testing schedulability against the Liu &amp; Layland bound (82.8%).</span>
      </div>

      <div class="telemetry-strip">
        <div class="telemetry-cell">
          <span class="telemetry-label">Timeline Clock</span>
          <span class="telemetry-val highlight" id="rt-telem-time">T = 0 ms</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Active Core Task</span>
          <span class="telemetry-val" id="rt-telem-task">Task 1 (C=2, P=5)</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Next Urgent Deadline</span>
          <span class="telemetry-val" id="rt-telem-deadline">Task 1 (d = 5 ms)</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Schedulability Status</span>
          <span class="telemetry-val highlight" id="rt-telem-status">Nominal (Zero Misses)</span>
        </div>
      </div>

      <div class="canvas-container">
        <svg class="rt-canvas" viewBox="0 0 760 260">
          <defs>
            <marker id="rt-arr-deadline" viewBox="0 0 10 10" refX="5" refY="8" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 2 0 L 5 8 L 8 0 z" fill="#dc2626" />
            </marker>
          </defs>

          <!-- Timeline Grid (0 to 14 ms, scale: 50px per ms, x=30 to 730) -->
          <!-- Track 1: Task 1 (Period = 5ms, Execution = 2ms) -->
          <g transform="translate(15, 20)">
            <rect width="730" height="48" rx="4" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="12" y="18" font-size="10" font-weight="700" fill="#0284c7">TASK 1 [C1=2ms, P1=5ms | Priority: High / Period: 5ms]</text>
            <g id="gantt-t1-bars"></g>
          </g>

          <!-- Track 2: Task 2 (Period = 7ms, Execution = 4ms) -->
          <g transform="translate(15, 85)">
            <rect width="730" height="48" rx="4" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="12" y="18" font-size="10" font-weight="700" fill="#d97706">TASK 2 [C2=4ms, P2=7ms | Priority: Low / Period: 7ms]</text>
            <g id="gantt-t2-bars"></g>
          </g>

          <!-- Track 3: CPU Core 0 Composite Execution -->
          <g transform="translate(15, 150)">
            <rect width="730" height="44" rx="4" fill="#ffffff" stroke="#059669" stroke-width="2"/>
            <text x="12" y="18" font-size="10" font-weight="700" fill="#166534">CPU CORE 0 (Combined Dispatch Timeline)</text>
            <g id="gantt-core-bars"></g>
          </g>

          <!-- Time Axis at y = 215 -->
          <line x1="30" y1="215" x2="730" y2="215" stroke="#94a3b8" stroke-width="2"/>
          <!-- Scale: 50px per ms; 0=30, 2=130, 4=230, 5=280, 7=380, 10=530, 14=730 -->
          <line x1="30" y1="215" x2="30" y2="223" stroke="#475569" stroke-width="1.5"/>
          <text x="30" y="238" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#475569">0</text>

          <line x1="130" y1="215" x2="130" y2="223" stroke="#475569" stroke-width="1.5"/>
          <text x="130" y="238" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#475569">2</text>

          <line x1="280" y1="215" x2="280" y2="223" stroke="#0284c7" stroke-width="2"/>
          <text x="280" y="238" text-anchor="middle" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#0284c7">T=5 (T1)</text>

          <line x1="380" y1="215" x2="380" y2="223" stroke="#d97706" stroke-width="2"/>
          <text x="380" y="238" text-anchor="middle" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#d97706">T=7 (T2)</text>

          <line x1="530" y1="215" x2="530" y2="223" stroke="#0284c7" stroke-width="2"/>
          <text x="530" y="238" text-anchor="middle" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#0284c7">T=10 (T1)</text>

          <line x1="730" y1="215" x2="730" y2="223" stroke="#d97706" stroke-width="2"/>
          <text x="730" y="238" text-anchor="middle" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#d97706">T=14 (T2)</text>
        </svg>
      </div>

      <!-- Stepper Controls & Current Step Summary Panel -->
      <div class="controls-narrative-strip">
        <div class="stepper-btn-group">
          <button class="btn-step" id="rt-btn-prev" onclick="stepRt(-1)" disabled>&larr; Previous</button>
          <button class="btn-step" id="rt-btn-next" onclick="stepRt(1)">Next Step &rarr;</button>
          <button class="btn-step" id="rt-btn-reset" onclick="resetRt()">Reset</button>
        </div>
        <div class="narrative-preview-panel">
          <strong>Current Step Summary</strong>
          <span id="rt-txt-narrative">At T=0, both Task 1 and Task 2 release instances. Under RMS, Task 1 (period 5) has shorter period than Task 2 (period 7), so Task 1 takes top static priority.</span>
        </div>
      </div>

      <div class="analytical-grid">
        <div class="pane-card">
          <div class="pane-title what">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            What Is Happening
          </div>
          <p class="pane-content" id="rt-txt-what">Task 1 runs on Core 0 from T=0 to T=2 ms. Task 2 waits in the Ready list.</p>
        </div>
        <div class="pane-card">
          <div class="pane-title why">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
            Why The System Does This
          </div>
          <p class="pane-content" id="rt-txt-why">RMS assigns highest priority to the shortest period task (P1=5 &lt; P2=7) to ensure high-frequency events complete ahead of longer deadlines.</p>
        </div>
      </div>
    </div>

    <h3>4. Multiprocessor Scheduling (SMP Architectures)</h3>
    <p>
      Modern processors do not scale through raw clock frequency increases; they scale horizontally through multiple physical CPU cores. Symmetric Multiprocessing (SMP) architectures share a unified physical address space across all cores, but introduce complex hardware topology and memory latency bottlenecks.
    </p>

    <h4>Single-Queue vs. Multi-Queue Topologies</h4>
    <p>
      Operating system architects face a foundational design fork when structuring multiprocessor runqueues:
    </p>

    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 20px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 4.1: Single-Queue (SQMS) vs. Multi-Queue (MQMS) Topologies</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">Comparing global lock contention against per-core cache affinity and work-stealing load balancing.</div>

      <svg viewBox="0 0 760 210" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <!-- Left: SQMS (Single Global Queue) -->
        <g transform="translate(20, 10)">
          <rect width="340" height="185" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
          <text x="14" y="24" font-size="11" font-weight="700" fill="#dc2626">Single-Queue Multiprocessor (SQMS)</text>

          <rect x="25" y="40" width="290" height="34" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
          <text x="170" y="58" text-anchor="middle" font-size="9.5" font-weight="700" fill="#991b1b">Global Runqueue [Spinlock Protected]</text>
          <text x="170" y="68" text-anchor="middle" font-size="7.5" fill="#dc2626">Extreme lock contention beyond 4 cores</text>

          <!-- Cores 0, 1, 2 -->
          <rect x="25" y="105" width="80" height="42" rx="4" fill="#ffffff" stroke="#94a3b8"/>
          <text x="65" y="125" text-anchor="middle" font-size="9" font-weight="700" fill="#334155">Core 0</text>
          <text x="65" y="138" text-anchor="middle" font-size="7.5" fill="#64748b">Cold Cache</text>

          <rect x="130" y="105" width="80" height="42" rx="4" fill="#ffffff" stroke="#94a3b8"/>
          <text x="170" y="125" text-anchor="middle" font-size="9" font-weight="700" fill="#334155">Core 1</text>
          <text x="170" y="138" text-anchor="middle" font-size="7.5" fill="#64748b">Cold Cache</text>

          <rect x="235" y="105" width="80" height="42" rx="4" fill="#ffffff" stroke="#94a3b8"/>
          <text x="275" y="125" text-anchor="middle" font-size="9" font-weight="700" fill="#334155">Core 2</text>
          <text x="275" y="138" text-anchor="middle" font-size="7.5" fill="#64748b">Cold Cache</text>

          <line x1="170" y1="74" x2="65" y2="105" stroke="#dc2626" stroke-width="1.5"/>
          <line x1="170" y1="74" x2="170" y2="105" stroke="#dc2626" stroke-width="1.5"/>
          <line x1="170" y1="74" x2="275" y2="105" stroke="#dc2626" stroke-width="1.5"/>

          <text x="14" y="172" font-size="8.5" fill="#475569">&bull; Tasks bounce across cores, destroying hardware caches.</text>
        </g>

        <!-- Right: MQMS (Per-Core Queues) -->
        <g transform="translate(390, 10)">
          <rect width="350" height="185" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
          <text x="14" y="24" font-size="11" font-weight="700" fill="#059669">Multi-Queue Multiprocessor (MQMS)</text>

          <!-- Core 0 Stack -->
          <rect x="25" y="40" width="135" height="30" rx="3" fill="#dcfce7" stroke="#16a34a"/>
          <text x="92" y="58" text-anchor="middle" font-size="8.5" font-weight="700" fill="#166534">Runqueue 0 (Local Lock)</text>
          <rect x="25" y="85" width="135" height="40" rx="4" fill="#ffffff" stroke="#059669" stroke-width="2"/>
          <text x="92" y="105" text-anchor="middle" font-size="9" font-weight="700" fill="#166534">Core 0 (L1/L2 Warm)</text>

          <!-- Core 1 Stack -->
          <rect x="190" y="40" width="135" height="30" rx="3" fill="#dcfce7" stroke="#16a34a"/>
          <text x="257" y="58" text-anchor="middle" font-size="8.5" font-weight="700" fill="#166534">Runqueue 1 (Local Lock)</text>
          <rect x="190" y="85" width="135" height="40" rx="4" fill="#ffffff" stroke="#059669" stroke-width="2"/>
          <text x="257" y="105" text-anchor="middle" font-size="9" font-weight="700" fill="#166534">Core 1 (L1/L2 Warm)</text>

          <!-- Work Stealing Arrow -->
          <path d="M 190 55 L 165 55" stroke="#d97706" stroke-width="2" stroke-dasharray="3 2"/>
          <text x="177" y="48" text-anchor="middle" font-size="8" font-weight="700" fill="#d97706">Steal</text>

          <text x="14" y="152" font-size="8.5" fill="#475569">&bull; Zero lock contention; exceptional cache affinity.</text>
          <text x="14" y="168" font-size="8.5" fill="#475569">&bull; Requires <strong>Work Stealing</strong> to balance idle cores.</text>
        </g>
      </svg>
    </div>

    <h4>Hardware Cache Affinity &amp; Invalidation Overhead</h4>
    <p>
      When a process runs on Core 0, its instructions and working data are fetched into Core 0's private L1 and L2 silicon caches. The task runs at peak hardware speed.
    </p>
    <p>
      If the scheduler preempts the task and subsequently dispatches it onto Core 1:
    </p>
    <ul>
      <li><strong>Cold Cache Penalties:</strong> Core 1's L1/L2 caches contain none of the process's working set. The CPU stalls on memory read requests, waiting tens of nanoseconds for data from shared L3 cache or DRAM.</li>
      <li><strong>Cache Invalidation Traffic:</strong> Hardware cache coherence protocols (such as MESI or MOESI) must broadcast bus invalidation signals across the interconnect fabric to invalidate the stale dirty lines sitting in Core 0's cache, creating cross-core bandwidth saturation.</li>
    </ul>
    <p>
      To prevent this, production schedulers enforce <strong>Processor Affinity</strong>:
    </p>
    <ul>
      <li><strong>Soft Affinity:</strong> The scheduler attempts to re-dispatch a process on the exact CPU core where it previously executed, but will migrate it to an idle core if queue imbalances become severe.</li>
      <li><strong>Hard Affinity (<code>sched_setaffinity(2)</code>):</strong> The application explicitly pins a thread to a specified bitmask of physical CPU cores, strictly prohibiting inter-core migration.</li>
    </ul>

    <h4>NUMA-Aware Scheduling (Non-Uniform Memory Access)</h4>
    <p>
      On modern multi-socket enterprise servers and high-core-count processors (such as AMD EPYC and Intel Xeon), memory controllers are partitioned across distinct physical silicon dies called <strong>NUMA Nodes</strong>.
    </p>
    <ul>
      <li>Accessing local memory directly wired to the core's own node takes &approx; <strong>60&ndash;80 ns</strong>.</li>
      <li>Accessing remote memory attached to another socket via high-speed interconnects (Ultra Path Interconnect [UPI] or Infinity Fabric) takes &approx; <strong>130&ndash;180 ns</strong> (a 2&times; to 3&times; latency penalty).</li>
      <li><strong>NUMA Scheduling Invariant:</strong> Schedulers must be NUMA-aware. A thread must be scheduled on the CPU node where its memory pages physically reside (following the operating system's <em>first-touch memory allocation policy</em>). Migration between NUMA sockets is treated as an expensive last resort.</li>
    </ul>

    <h4>Work Stealing Algorithms</h4>
    <p>
      To maintain near-perfect load balance in MQMS without global lock contention, modern schedulers implement <strong>Work Stealing</strong>:
    </p>
    <ol>
      <li>Each CPU core maintains its own double-ended queue (deque) of runnable tasks.</li>
      <li>A core pushes and pops tasks from the <strong>head of its own deque in LIFO order</strong>, maximizing hardware L1 cache locality for recently paused sub-tasks.</li>
      <li>When a core exhausts its own runqueue and becomes idle, it randomly chooses a peer core (the "victim") and attempts to <strong>steal work from the tail of the victim's deque in FIFO order</strong>.</li>
      <li>Stealing from the tail minimizes lock conflicts with the victim core (which accesses the head), while simultaneously grabbing the oldest queued task—the task whose cache footprint on the victim core is already cold, making cross-core migration practically free.</li>
    </ol>

    <nav class="nav-bar" style="margin-top: 36px; border-bottom: none; border-top: 1px solid var(--border); padding-top: 16px;">
      <a href="03-interactive-scheduling.html">&larr; 03. Interactive Scheduling</a>
      <a href="index.html">&#127968; Week 3 Index</a>
      <span style="font-size: 0.85rem; font-weight: 700; color: #64748b;">Module 04 (Final)</span>
    </nav>
  </div>

  <script>
    const rtSteps = {
      rms: [
        {
          time: "T = 0 ms",
          task: "Task 1 (Period 5, Run 2ms)",
          deadline: "Task 1 (d = 5ms)",
          status: "Nominal (T1 Running)",
          t1Bars: `
            <rect x="30" y="24" width="100" height="18" rx="2" fill="#0284c7"/>
            <text x="80" y="37" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">T1 (Exec 0-2ms)</text>
          `,
          t2Bars: `
            <rect x="30" y="24" width="100" height="18" rx="2" fill="#fef3c7" stroke="#d97706" stroke-dasharray="2 2"/>
            <text x="80" y="37" text-anchor="middle" font-size="8.5" fill="#b45309">T2 Waiting (P=7)</text>
          `,
          coreBars: `
            <rect x="30" y="22" width="100" height="16" rx="2" fill="#0284c7"/>
            <text x="80" y="34" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">Task 1 (High Priority)</text>
          `,
          narrative: "At T=0, both Task 1 (P1=5, C1=2) and Task 2 (P2=7, C2=4) arrive. Under Rate-Monotonic Scheduling, Task 1 has shorter period (5 < 7), granting it highest static priority. Task 1 runs immediately.",
          what: "Task 1 runs on Core 0 from T=0 to T=2 ms. Task 2 waits in the Ready list.",
          why: "RMS assigns highest priority to the shortest period task to ensure high-frequency events complete ahead of longer deadlines."
        },
        {
          time: "T = 2 ms",
          task: "Task 2 (Period 7, Needs 4ms)",
          deadline: "Task 2 (d = 7ms)",
          status: "Nominal (T2 Running)",
          t1Bars: `
            <rect x="30" y="24" width="100" height="18" rx="2" fill="#0284c7"/>
            <text x="80" y="37" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">T1 (Done)</text>
          `,
          t2Bars: `
            <rect x="130" y="24" width="150" height="18" rx="2" fill="#d97706"/>
            <text x="205" y="37" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">T2 Executing (2-5ms)</text>
          `,
          coreBars: `
            <rect x="30" y="22" width="100" height="16" rx="2" fill="#0284c7"/>
            <rect x="130" y="22" width="150" height="16" rx="2" fill="#d97706"/>
            <text x="205" y="34" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">Task 2</text>
          `,
          narrative: "Task 1 completes its 2ms computation at T=2. Core 0 switches to Task 2. Task 2 requires 4ms of computation and has a deadline at T=7.",
          what: "Task 2 executes from T=2 to T=5 ms. Task 2 completes 3ms of its required 4ms computation.",
          why: "When high-priority tasks finish or block, lower-priority tasks run until the next high-priority arrival."
        },
        {
          time: "T = 5 ms",
          task: "Task 1 PREEMPTS Task 2!",
          deadline: "T1 (d = 10ms), T2 (d = 7ms)",
          status: "T2 PREEMPTED (1ms left)",
          t1Bars: `
            <rect x="30" y="24" width="100" height="18" rx="2" fill="#0284c7"/>
            <rect x="280" y="24" width="100" height="18" rx="2" fill="#0284c7"/>
            <text x="330" y="37" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">T1 (Exec 5-7ms)</text>
          `,
          t2Bars: `
            <rect x="130" y="24" width="150" height="18" rx="2" fill="#d97706"/>
            <rect x="280" y="24" width="100" height="18" rx="2" fill="#fee2e2" stroke="#dc2626" stroke-dasharray="2 2"/>
            <text x="330" y="37" text-anchor="middle" font-size="8" fill="#dc2626">T2 Preempted!</text>
          `,
          coreBars: `
            <rect x="30" y="22" width="100" height="16" rx="2" fill="#0284c7"/>
            <rect x="130" y="22" width="150" height="16" rx="2" fill="#d97706"/>
            <rect x="280" y="22" width="100" height="16" rx="2" fill="#0284c7"/>
            <text x="330" y="34" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">Task 1 (Preempts T2)</text>
          `,
          narrative: "At T=5, Task 1 releases its second periodic instance. Because RMS is static, Task 1 retains higher priority than Task 2, PREEMPTING Task 2 even though Task 2's deadline is right at T=7!",
          what: "Task 2 is forcibly preempted at T=5 with 1ms remaining. Task 1 executes from T=5 to T=7.",
          why: "Rate-Monotonic priority is static. The scheduler cannot recognize that Task 2 has a more urgent upcoming deadline (T=7 vs T=10)."
        },
        {
          time: "T = 7 ms",
          task: "CRITICAL FAILURE: Task 2 Misses Deadline!",
          deadline: "Task 2 Deadline PASSED",
          status: "DEADLINE MISSED (RMS Failure)",
          t1Bars: `
            <rect x="30" y="24" width="100" height="18" rx="2" fill="#0284c7"/>
            <rect x="280" y="24" width="100" height="18" rx="2" fill="#0284c7"/>
          `,
          t2Bars: `
            <rect x="130" y="24" width="150" height="18" rx="2" fill="#d97706"/>
            <!-- Failure Indicator Marker -->
            <rect x="380" y="20" width="120" height="24" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
            <text x="440" y="36" text-anchor="middle" font-size="9" font-weight="700" fill="#b91c1c">&times; T2 MISSED DEADLINE!</text>
          `,
          coreBars: `
            <rect x="30" y="22" width="100" height="16" rx="2" fill="#0284c7"/>
            <rect x="130" y="22" width="150" height="16" rx="2" fill="#d97706"/>
            <rect x="280" y="22" width="100" height="16" rx="2" fill="#0284c7"/>
            <rect x="380" y="22" width="50" height="16" rx="2" fill="#fee2e2" stroke="#dc2626"/>
            <text x="405" y="34" text-anchor="middle" font-size="8" font-weight="700" fill="#dc2626">T2 Miss</text>
          `,
          narrative: "At T=7, Task 1 finishes. Task 2 resumes to execute its final 1ms—but T=7 was Task 2's deadline! Task 2 MISSED ITS DEADLINE. Total U = 0.97 exceeded Liu & Layland's 82.8% bound.",
          what: "Task 2 completes at T=8 ms, 1 ms past its hard deadline. In a safety-critical system, this represents complete system failure.",
          why: "Static RMS priority cannot adapt dynamically, demonstrating why Liu & Layland bounds must be strictly enforced."
        }
      ],
      edf: [
        {
          time: "T = 0 ms",
          task: "Task 1 (Deadline d = 5ms)",
          deadline: "T1 (d = 5ms) < T2 (d = 7ms)",
          status: "Nominal (T1 Running)",
          t1Bars: `
            <rect x="30" y="24" width="100" height="18" rx="2" fill="#0284c7"/>
            <text x="80" y="37" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">T1 (Exec 0-2ms)</text>
          `,
          t2Bars: `
            <rect x="30" y="24" width="100" height="18" rx="2" fill="#fef3c7" stroke="#d97706" stroke-dasharray="2 2"/>
            <text x="80" y="37" text-anchor="middle" font-size="8.5" fill="#b45309">T2 (Deadline 7ms)</text>
          `,
          coreBars: `
            <rect x="30" y="22" width="100" height="16" rx="2" fill="#0284c7"/>
            <text x="80" y="34" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">Task 1 (Earliest Deadline)</text>
          `,
          narrative: "Under Earliest Deadline First (EDF), the scheduler inspects absolute deadlines. Task 1 deadline = 5ms. Task 2 deadline = 7ms. Since 5 < 7, Task 1 is assigned higher dynamic priority and runs first.",
          what: "Task 1 runs from T=0 to T=2 ms.",
          why: "EDF prioritizes whichever task is closest to its deadline to prevent starvation."
        },
        {
          time: "T = 2 ms",
          task: "Task 2 (Deadline d = 7ms)",
          deadline: "Task 2 (d = 7ms)",
          status: "Nominal (T2 Running)",
          t1Bars: `
            <rect x="30" y="24" width="100" height="18" rx="2" fill="#0284c7"/>
            <text x="80" y="37" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">T1 (Done)</text>
          `,
          t2Bars: `
            <rect x="130" y="24" width="150" height="18" rx="2" fill="#d97706"/>
            <text x="205" y="37" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">T2 Executing (2-5ms)</text>
          `,
          coreBars: `
            <rect x="30" y="22" width="100" height="16" rx="2" fill="#0284c7"/>
            <rect x="130" y="22" width="150" height="16" rx="2" fill="#d97706"/>
            <text x="205" y="34" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">Task 2</text>
          `,
          narrative: "Task 1 finishes at T=2. Task 2 runs from T=2 to T=5. Task 2 has executed 3ms of its required 4ms.",
          what: "Task 2 is actively computing on Core 0.",
          why: "The CPU executes runnable tasks according to closest upcoming deadline."
        },
        {
          time: "T = 5 ms",
          task: "Task 2 CONTINUES! (Dynamic Priority)",
          deadline: "T2 (d = 7ms) < T1 (d = 10ms)!",
          status: "NO PREEMPTION! (T2 Priority Higher)",
          t1Bars: `
            <rect x="30" y="24" width="100" height="18" rx="2" fill="#0284c7"/>
            <rect x="280" y="24" width="50" height="18" rx="2" fill="#f8fafc" stroke="#0284c7" stroke-dasharray="2 2"/>
            <text x="305" y="37" text-anchor="middle" font-size="8" fill="#0284c7">T1 Waits</text>
          `,
          t2Bars: `
            <rect x="130" y="24" width="200" height="18" rx="2" fill="#d97706"/>
            <text x="230" y="37" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">T2 Finishes (2-6ms)!</text>
          `,
          coreBars: `
            <rect x="30" y="22" width="100" height="16" rx="2" fill="#0284c7"/>
            <rect x="130" y="22" width="200" height="16" rx="2" fill="#d97706"/>
            <text x="230" y="34" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">Task 2 Retains CPU</text>
          `,
          narrative: "CRITICAL DIFFERENCE: At T=5, Task 1 arrives with deadline d=10ms. But Task 2's deadline is d=7ms! Since 7 < 10, Task 2 has EARLIER DEADLINE than Task 1. Task 2 is NOT preempted and finishes successfully at T=6!",
          what: "Task 2 continues executing, completing its full 4ms burst at T=6 ms, easily beating its T=7 ms deadline.",
          why: "Dynamic priority assignment in EDF evaluates actual upcoming deadlines rather than static periods, achieving 100% schedulability."
        },
        {
          time: "T = 6 ms",
          task: "Task 1 Dispatched &amp; Meets Deadline",
          deadline: "All Deadlines Met (100% Schedulable)",
          status: "OPTIMAL (Zero Deadline Misses!)",
          t1Bars: `
            <rect x="30" y="24" width="100" height="18" rx="2" fill="#0284c7"/>
            <rect x="330" y="24" width="100" height="18" rx="2" fill="#0284c7"/>
            <text x="380" y="37" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">T1 Runs (6-8ms)</text>
          `,
          t2Bars: `
            <rect x="130" y="24" width="200" height="18" rx="2" fill="#d97706"/>
          `,
          coreBars: `
            <rect x="30" y="22" width="100" height="16" rx="2" fill="#0284c7"/>
            <rect x="130" y="22" width="200" height="16" rx="2" fill="#d97706"/>
            <rect x="330" y="22" width="100" height="16" rx="2" fill="#0284c7"/>
            <text x="380" y="34" text-anchor="middle" font-size="8.5" font-weight="700" fill="#ffffff">Task 1 (Meets d=10ms)</text>
          `,
          narrative: "At T=6, Task 1 executes its 2ms burst, finishing at T=8 ms (well ahead of its d=10 ms deadline). Both tasks meet every single deadline under EDF with 97% CPU utilization!",
          what: "Both tasks successfully complete their cycles. Zero deadlines were missed.",
          why: "EDF is mathematically optimal: any task set with U <= 1.0 is guaranteed schedulable."
        }
      ]
    };

    let activeRtDim = "rms";
    let activeRtStep = 0;

    function renderRtStepper() {
      const steps = rtSteps[activeRtDim];
      const step = steps[activeRtStep];

      // Update Telemetry
      document.getElementById("rt-telem-time").textContent = step.time;
      document.getElementById("rt-telem-task").textContent = step.task;
      document.getElementById("rt-telem-deadline").textContent = step.deadline;
      document.getElementById("rt-telem-status").textContent = step.status;

      const isAlert = step.status.includes("DEADLINE MISSED");
      document.getElementById("rt-telem-status").classList.toggle("alert", isAlert);
      document.getElementById("rt-telem-status").classList.toggle("highlight", !isAlert);

      // Update Gantt Bars
      document.getElementById("gantt-t1-bars").innerHTML = step.t1Bars;
      document.getElementById("gantt-t2-bars").innerHTML = step.t2Bars;
      document.getElementById("gantt-core-bars").innerHTML = step.coreBars;

      // Update Narrative Panel
      document.getElementById("rt-txt-narrative").innerHTML = step.narrative;
      document.getElementById("rt-btn-prev").disabled = (activeRtStep === 0);
      document.getElementById("rt-btn-next").disabled = (activeRtStep === steps.length - 1);

      // Update Analytical Panes
      document.getElementById("rt-txt-what").innerHTML = step.what;
      document.getElementById("rt-txt-why").innerHTML = step.why;
    }

    function stepRt(delta) {
      const steps = rtSteps[activeRtDim];
      activeRtStep = Math.max(0, Math.min(steps.length - 1, activeRtStep + delta));
      renderRtStepper();
    }

    function resetRt() {
      activeRtStep = 0;
      renderRtStepper();
    }

    function setRtDim(dim) {
      activeRtDim = dim;
      activeRtStep = 0;
      document.getElementById("dim-rms").classList.toggle("active", dim === "rms");
      document.getElementById("dim-edf").classList.toggle("active", dim === "edf");

      const scenarioText = dim === "rms"
        ? "Task 1 (C1=2, P1=5; U1=0.40) and Task 2 (C2=4, P2=7; U2=0.57). Total U = 0.97 (97%). Demonstrating how static RMS priorities cause Task 2 to miss its deadline at T=7ms."
        : "Task 1 (C1=2, P1=5; U1=0.40) and Task 2 (C2=4, P2=7; U2=0.57). Total U = 0.97 (97%). Demonstrating how dynamic EDF priorities prevent preemption at T=5ms and satisfy all deadlines.";
      document.getElementById("rt-scenario-text").innerHTML = scenarioText;

      renderRtStepper();
    }

    document.addEventListener("DOMContentLoaded", () => {
      renderRtStepper();
    });
  </script>
</body>
</html>
"""

def execute_expansion():
    os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(MODULE_HTML.strip() + "\n")

    print(f"--> Successfully expanded {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand 04-realtime-multiprocessor.html with RMS, EDF, and SMP topologies\n\n"
            "Add Liu & Layland bound proof, EDF overload domino analysis, SQMS/MQMS\n"
            "work stealing, NUMA node topology, and an RMS vs. EDF Gantt stepper."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    execute_expansion()
