#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand 01-scheduling-introduction.html in Week 3
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week03-process-scheduling", "01-scheduling-introduction.html")

MODULE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>01. Introduction to CPU Scheduling | Week 3: Process Scheduling</title>
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

    /* High-contrast Syntax Tokens */
    .syn-kwd { color: #f43f5e; font-weight: 700; }
    .syn-fn  { color: #38bdf8; font-weight: 600; }
    .syn-cmt { color: #94a3b8; font-style: italic; }
    .syn-var { color: #f8fafc; font-weight: 500; }
    .syn-punc{ color: #cbd5e1; }
    .syn-type{ color: #4ade80; font-weight: 600; }

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
    svg.scheduler-canvas {
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

    /* Diagram Nodes & Shapes */
    .task-node {
      fill: #ffffff;
      stroke: #cbd5e1;
      stroke-width: 2;
      transition: all 0.3s ease;
    }
    .task-node.running {
      fill: #f0fdf4;
      stroke: #059669;
      stroke-width: 2.5;
    }
    .task-node.ready {
      fill: #f0f9ff;
      stroke: #0284c7;
      stroke-width: 2;
    }
    .task-node.waiting {
      fill: #fef3c7;
      stroke: #d97706;
      stroke-width: 2;
    }
    .task-node.preempted {
      fill: #fef2f2;
      stroke: #dc2626;
      stroke-width: 2;
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <span></span>
      <a href="index.html">&#127968; Week 3 Index</a>
      <a href="02-batch-scheduling.html">Next: 02. Batch Scheduling &rarr;</a>
    </nav>

    <h2>01. Introduction to CPU Scheduling</h2>
    <p>
      In any multiprogrammed system, multiple processes and execution threads reside simultaneously in main memory. While modern hardware platforms provide multi-core processors, the number of active, runnable tasks almost always exceeds the number of physical execution units.
    </p>
    <p>
      The operating system must decide: <em>which process runs next, on which CPU core, for how long, and when it must be forced to yield?</em> This critical allocation policy is governed by the <strong>CPU scheduler</strong>, while the low-level mechanism that enacts the switch is executed by the <strong>dispatcher</strong>.
    </p>

    <h3>1. Process Behavior: The CPU-I/O Burst Cycle</h3>
    <p>
      Nearly all processes alternate between two distinct execution phases in an unending cycle:
    </p>
    <ul>
      <li><strong>CPU Burst:</strong> The processor actively executes machine instructions, arithmetic calculations, memory loads, and data transformations without waiting for external hardware.</li>
      <li><strong>I/O Burst:</strong> The process issues a synchronous request to an external device (e.g., secondary storage, network socket, user keyboard, or system timer) and transitions into the Blocked/Waiting state until the hardware device completes the transfer.</li>
    </ul>

    <h4>The Empirical Burst Distribution</h4>
    <p>
      Decades of empirical measurements across production systems demonstrate that CPU burst durations follow a heavy-tailed, hyperexponential frequency distribution:
    </p>
    <ul>
      <li><strong>The Vast Majority of Bursts are Extremely Short:</strong> Over 80% of all CPU bursts in general-purpose workloads last under 4 to 8 milliseconds. These correspond to interactive events, GUI updates, system call parameter validation, and short message passing.</li>
      <li><strong>A Small Minority of Bursts are Very Long:</strong> A tiny fraction of CPU bursts last tens, hundreds, or thousands of milliseconds. These belong to compute-heavy workloads such as video rendering, scientific matrix inversion, data compression, or cryptographic hashing.</li>
    </ul>

    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 20px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 1.1: Empirical Frequency Distribution of CPU Burst Durations</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">High frequency of sub-10ms bursts versus rare, long-running compute bursts.</div>

      <svg viewBox="0 0 760 220" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <linearGradient id="burstGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#0284c7" stop-opacity="0.6"/>
            <stop offset="100%" stop-color="#0284c7" stop-opacity="0.05"/>
          </linearGradient>
        </defs>

        <!-- Axes -->
        <line x1="60" y1="180" x2="720" y2="180" stroke="#94a3b8" stroke-width="2"/>
        <line x1="60" y1="20" x2="60" y2="180" stroke="#94a3b8" stroke-width="2"/>

        <text x="60" y="15" text-anchor="middle" font-size="10" font-weight="700" fill="#475569">Frequency (%)</text>
        <text x="720" y="202" text-anchor="end" font-size="10" font-weight="700" fill="#475569">CPU Burst Duration (Milliseconds) &rarr;</text>

        <!-- Axis Labels -->
        <text x="50" y="184" text-anchor="end" font-family="var(--font-mono)" font-size="9" fill="#64748b">0</text>
        <text x="50" y="105" text-anchor="end" font-family="var(--font-mono)" font-size="9" fill="#64748b">50%</text>
        <text x="50" y="30" text-anchor="end" font-family="var(--font-mono)" font-size="9" fill="#64748b">100%</text>

        <text x="120" y="196" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#64748b">2ms</text>
        <text x="200" y="196" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#64748b">8ms</text>
        <text x="320" y="196" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#64748b">20ms</text>
        <text x="500" y="196" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#64748b">50ms</text>
        <text x="680" y="196" text-anchor="middle" font-family="var(--font-mono)" font-size="9" fill="#64748b">100ms+</text>

        <!-- Curve Area -->
        <path d="M 60 25 Q 90 28, 120 70 Q 160 130, 220 160 Q 350 176, 700 179 L 700 180 L 60 180 Z" fill="url(#burstGrad)" />
        <path d="M 60 25 Q 90 28, 120 70 Q 160 130, 220 160 Q 350 176, 700 179" fill="none" stroke="#0284c7" stroke-width="3" />

        <!-- Annotations -->
        <rect x="140" y="40" width="220" height="52" rx="4" fill="#ffffff" stroke="#bae6fd" filter="drop-shadow(0 1px 2px rgba(0,0,0,0.05))"/>
        <text x="150" y="58" font-size="10" font-weight="700" fill="#0369a1">I/O-Bound Cluster (&gt;80% of Bursts)</text>
        <text x="150" y="74" font-size="9" fill="#475569">Interactive, text editors, GUI events,</text>
        <text x="150" y="86" font-size="9" fill="#475569">short-lived system calls.</text>

        <rect x="460" y="105" width="220" height="52" rx="4" fill="#ffffff" stroke="#cbd5e1" filter="drop-shadow(0 1px 2px rgba(0,0,0,0.05))"/>
        <text x="470" y="123" font-size="10" font-weight="700" fill="#0f172a">CPU-Bound Tail (&lt;20% of Bursts)</text>
        <text x="470" y="139" font-size="9" fill="#475569">Simulations, matrix multiplication,</text>
        <text x="470" y="151" font-size="9" fill="#475569">long uninterrupted compilation.</text>
      </svg>
    </div>

    <h4>Compute-Bound vs. I/O-Bound Workloads</h4>
    <p>
      An operating system exploits this asymmetry to achieve balanced system utilization:
    </p>
    <ul>
      <li>
        <strong>I/O-Bound Processes:</strong> Spend the majority of their lifespan waiting for I/O operations. They run for mere fractions of a millisecond before issuing a system call and yielding the core. If the scheduler prioritizes I/O-bound tasks immediately upon unblocking, they can issue hardware disk/network requests rapidly and step aside, keeping peripheral hardware pipelines saturated while consuming minimal CPU time.
      </li>
      <li>
        <strong>Compute-Bound (CPU-Bound) Processes:</strong> Spend virtually all their time performing continuous calculations. If an unconstrained compute-bound process is allowed to run indefinitely, it will monopolize the physical CPU core, starving all interactive processes and causing severe system lag.
      </li>
    </ul>

    <h3>2. The Scheduler vs. The Dispatcher</h3>
    <p>
      A common point of confusion is the division of responsibility between the <em>scheduler</em> and the <em>dispatcher</em>:
    </p>
    <div style="overflow-x: auto; margin: 18px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 14px; width: 30%;">Component</th>
            <th style="padding: 10px 14px; width: 35%;">Primary Role</th>
            <th style="padding: 10px 14px; width: 35%;">Mechanisms &amp; Overhead</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700; color: #0284c7;">The CPU Scheduler</td>
            <td style="padding: 10px 14px;"><strong>Policy Engine:</strong> Selects <em>which</em> process from the Ready queue should be allocated the CPU core, applying priority algorithms and accounting rules.</td>
            <td style="padding: 10px 14px;">Algorithmic logic (e.g., traversing priority trees, computing remaining quantum, sorting runqueues).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700; color: #059669;">The Dispatcher</td>
            <td style="padding: 10px 14px;"><strong>Mechanism Engine:</strong> Low-level hardware routine that actually gives control of the physical CPU core to the process selected by the scheduler.</td>
            <td style="padding: 10px 14px;">Context switching, saving/restoring hardware registers, switching virtual memory page tables (CR3), dropping from Ring 0 to Ring 3, and jumping to the program counter.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h4>Dispatch Latency</h4>
    <p>
      The time required for the dispatcher to stop one process, perform a full context switch, and start another process running is called the <strong>dispatch latency</strong>:
    </p>
    <pre><code>Dispatch Latency = Interrupt Trapping + State Saving (Registers/Stack) +
                   Scheduler Selection + MMU Context Switch (CR3/Page Tables) +
                   State Restoration + User Mode Transition (Ring 0 &rarr; Ring 3)</code></pre>
    <p>
      Beyond the immediate assembly instructions (typically 1 to 5 microseconds), dispatch latency incurs an invisible <strong>cache warm-up penalty</strong>: the newly scheduled process encounters cold L1/L2 hardware caches and Translation Lookaside Buffer (TLB) misses, stalling CPU pipelines until its memory working set is fetched back into on-chip SRAM.
    </p>

    <h3>3. When to Schedule: Trigger Points &amp; Preemption</h3>
    <p>
      CPU scheduling decisions arise under four distinct operational events:
    </p>
    <ol>
      <li><strong>Running &rarr; Waiting (Blocked):</strong> The process initiates a blocking operation (e.g., synchronous file I/O, network packet wait, <code>sleep()</code>, or waiting on a semaphore/mutex).</li>
      <li><strong>Running &rarr; Ready:</strong> The process is forcibly interrupted while actively executing instructions (e.g., an APIC hardware timer interrupt indicates its time slice has expired, or an external device interrupt unblocks a higher-priority task).</li>
      <li><strong>Waiting &rarr; Ready:</strong> An asynchronous hardware event occurs (e.g., disk controller finishes DMA transfer, network packet arrives at the NIC), moving a previously blocked process into the Ready queue.</li>
      <li><strong>Terminated:</strong> The running process completes execution by calling <code>exit()</code> or is aborted by the kernel due to an unhandled exception (e.g., segmentation fault <code>SIGSEGV</code>).</li>
    </ol>

    <h4>Preemptive vs. Non-Preemptive (Cooperative) Scheduling</h4>
    <ul>
      <li>
        <strong>Non-Preemptive (Cooperative) Multitasking:</strong>
        Scheduling occurs <em>only</em> under conditions 1 and 4. Once a process is allocated the CPU, it retains exclusive ownership of the core until it voluntarily yields control—either by blocking on an I/O request or terminating.
        <br>
        <em>The Fatal Vulnerability:</em> If an application enters a buggy infinite loop (<code>while(1);</code>) or a developer refuses to call cooperative yield routines, the entire operating system and all other applications freeze permanently. Early personal computer operating systems (such as Windows 3.1 and classic Mac OS System 7) relied on cooperative multitasking, leading to frequent system-wide lockups.
      </li>
      <li>
        <strong>Preemptive Multitasking:</strong>
        Scheduling occurs across all four conditions (1, 2, 3, and 4). The operating system programs a hardware timer interrupt (e.g., the local APIC timer on x86-64) to fire periodically at a fixed frequency (e.g., every 1 ms to 10 ms).
        <br>
        When the timer interrupt fires, the CPU hardware forcefully suspends user execution, vectors into the kernel interrupt handler in Ring 0, saves the interrupted task's state, and invokes the scheduler. If a task has exhausted its allocated quantum, it is preempted immediately and moved back to the Ready queue. Preemption prevents any single process from monopolizing the hardware.
      </li>
    </ul>

    <!-- Directed Narrative Stepper Standard: CPU Scheduling Mechanics -->
    <div class="aid-wrapper">
      <div class="aid-header">
        <h4>Interactive Stepper: Preemptive vs. Cooperative Execution Models</h4>
        <div class="dimension-toggles">
          <button class="dim-btn active" id="dim-preempt" onclick="setSchedDim('preempt')">Preemptive Scheduling (Timer Interrupt)</button>
          <button class="dim-btn" id="dim-coop" onclick="setSchedDim('coop')">Non-Preemptive (Cooperative Mode)</button>
        </div>
      </div>

      <div class="scenario-banner">
        <span class="scenario-tag">Scenario Arc</span>
        <span id="sched-scenario-text">Process A (Compute-Bound Matrix Math) is executing. Process B (Interactive User Input) arrives in the Ready queue. Tracking how the scheduler handles CPU allocation.</span>
      </div>

      <div class="telemetry-strip">
        <div class="telemetry-cell">
          <span class="telemetry-label">Active CPU Entity</span>
          <span class="telemetry-val highlight" id="s-telem-entity">Process A (Compute-Bound)</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Quantum Status</span>
          <span class="telemetry-val" id="s-telem-quantum">Timer: 8ms Remaining</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">CPU Core Mode</span>
          <span class="telemetry-val" id="s-telem-mode">User Mode (Ring 3)</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Interactive Latency</span>
          <span class="telemetry-val highlight" id="s-telem-lat">0 ms (Process B Buffered)</span>
        </div>
      </div>

      <div class="canvas-container">
        <svg class="scheduler-canvas" viewBox="0 0 760 260">
          <defs>
            <marker id="s-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 0 2 L 8 5 L 0 8 z" fill="#0284c7" />
            </marker>
            <marker id="s-arr-alert" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 0 2 L 8 5 L 0 8 z" fill="#dc2626" />
            </marker>
          </defs>

          <!-- Ready Queue Area -->
          <rect x="30" y="30" width="220" height="200" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
          <text x="45" y="55" font-size="12" font-weight="700" fill="#0f172a">READY QUEUE (FIFO / Priority)</text>

          <g id="box-task-b" transform="translate(45, 75)">
            <rect class="task-node ready" width="190" height="60" rx="6"/>
            <text x="14" y="24" font-size="11" font-weight="700" fill="#0284c7">Process B (Interactive)</text>
            <text id="txt-task-b-state" x="14" y="44" font-family="var(--font-mono)" font-size="10" fill="#475569">State: Ready (Key Waiting)</text>
          </g>

          <g id="box-task-c" transform="translate(45, 150)">
            <rect class="task-node" width="190" height="60" rx="6"/>
            <text x="14" y="24" font-size="11" font-weight="700" fill="#334155">Process C (Background)</text>
            <text x="14" y="44" font-family="var(--font-mono)" font-size="10" fill="#64748b">State: Ready (Queued)</text>
          </g>

          <!-- Hardware CPU Execution Core -->
          <g transform="translate(320, 30)">
            <rect id="rect-cpu-core" x="0" y="0" width="230" height="200" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2.5"/>
            <text x="20" y="30" font-size="13" font-weight="700" fill="#059669">PHYSICAL CPU CORE 0</text>
            <text id="txt-core-mode" x="20" y="50" font-family="var(--font-mono)" font-size="10" fill="#15803d">Status: Executing Ring 3</text>

            <rect id="rect-active-task" x="15" y="70" width="200" height="110" rx="6" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
            <text id="txt-active-name" x="30" y="98" font-size="12" font-weight="700" fill="#166534">Process A (Compute)</text>
            <text id="txt-active-details" x="30" y="120" font-family="var(--font-mono)" font-size="10" fill="#334155">Burst: Infinite Math Loop</text>
            <text id="txt-active-quantum" x="30" y="142" font-family="var(--font-mono)" font-size="10" fill="#059669">Quantum: 8ms Remaining</text>
          </g>

          <!-- Flow Connectors -->
          <!-- Ready Queue to CPU -->
          <path id="path-dispatch" d="M 250 105 L 320 105" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#s-arr)"/>
          <!-- Preemption Return Arc -->
          <path id="path-preempt" d="M 435 30 C 435 10, 140 10, 140 30" fill="none" stroke="#dc2626" stroke-width="2" stroke-dasharray="4 3" marker-end="url(#s-arr-alert)" style="display: none;"/>
          <text id="txt-preempt-label" x="280" y="18" text-anchor="middle" font-size="9" font-weight="700" fill="#dc2626" style="display: none;">Hardware Timer Preemption</text>

          <!-- I/O Wait State / Blocked Area -->
          <g transform="translate(590, 30)">
            <rect x="0" y="0" width="140" height="200" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="14" y="30" font-size="11" font-weight="700" fill="#475569">BLOCKED QUEUE</text>
            <text x="14" y="50" font-size="9" fill="#64748b">Awaiting Hardware</text>
            <rect x="12" y="70" width="116" height="40" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="20" y="94" font-family="var(--font-mono)" font-size="9" fill="#64748b">Disk Read (FD 4)</text>
          </g>
        </svg>
      </div>

      <!-- Stepper Controls & Current Step Summary Panel -->
      <div class="controls-narrative-strip">
        <div class="stepper-btn-group">
          <button class="btn-step" id="s-btn-prev" onclick="stepSched(-1)" disabled>&larr; Previous</button>
          <button class="btn-step" id="s-btn-next" onclick="stepSched(1)">Next Step &rarr;</button>
          <button class="btn-step" id="s-btn-reset" onclick="resetSched()">Reset</button>
        </div>
        <div class="narrative-preview-panel">
          <strong>Current Step Summary</strong>
          <span id="s-txt-narrative">Process A runs uninterrupted on CPU Core 0, performing intensive matrix calculations. Process B enters the Ready queue awaiting interactive input processing.</span>
        </div>
      </div>

      <div class="analytical-grid">
        <div class="pane-card">
          <div class="pane-title what">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            What Is Happening
          </div>
          <p class="pane-content" id="s-txt-what">Process A executes unconstrained in User Mode. Process B arrives in the Ready queue after a keyboard keystroke triggers an asynchronous interrupt.</p>
        </div>
        <div class="pane-card">
          <div class="pane-title why">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
            Why The System Does This
          </div>
          <p class="pane-content" id="s-txt-why">The CPU maintains maximum instruction throughput by keeping the execution pipeline full with Process A until an interrupt forces an intervention.</p>
        </div>
      </div>
    </div>

    <h3>4. Conflicting Optimization Goals &amp; Metrics</h3>
    <p>
      An ideal CPU scheduler would simultaneously maximize throughput, eliminate user latency, execute tasks instantaneously, and consume zero CPU overhead. In physical reality, these goals directly contradict one another.
    </p>

    <h4>Formal Scheduling Performance Metrics</h4>
    <ul>
      <li>
        <strong>Turnaround Time ($T_{\text{turnaround}}$):</strong> The total elapsed time between a job's submission/arrival and its final completion:
        <pre><code>T_turnaround = T_completion - T_arrival</code></pre>
        This metric includes time spent waiting in the ready queue, context switching overhead, executing on the CPU, and waiting on I/O. Minimizing turnaround time is the primary goal of batch systems.
      </li>
      <li>
        <strong>Waiting Time ($T_{\text{wait}}$):</strong> The total time a process spends waiting in the Ready queue ready to execute, but unable to acquire a physical core:
        <pre><code>T_wait = T_turnaround - T_burst</code></pre>
        (where $T_{\text{burst}}$ is the actual time spent running CPU instructions).
      </li>
      <li>
        <strong>Response Time ($T_{\text{response}}$):</strong> The elapsed duration from when a process becomes runnable to when it produces its very first observable execution response:
        <pre><code>T_response = T_first_execution - T_arrival</code></pre>
        In interactive systems, response time is far more important than turnaround time; users expect immediate tactile feedback (within 16 to 50 ms) even if the underlying background task requires several minutes to complete.
      </li>
      <li>
        <strong>Throughput:</strong> The number of complete processes finished per unit of time (e.g., 50 jobs per minute). Maximizing throughput requires minimizing context switch overhead and keeping the CPU saturated with long bursts.
      </li>
      <li>
        <strong>CPU Utilization:</strong> The percentage of time the physical CPU execution units are actively executing non-idle user or kernel instructions (typically 40% in lightly loaded systems to 95% in heavily loaded batch clusters).
      </li>
    </ul>

    <h4>The Core Architectural Dilemma: Interactive Responsiveness vs. Batch Throughput</h4>
    <div style="overflow-x: auto; margin: 18px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 14px; width: 25%;">System Environment</th>
            <th style="padding: 10px 14px; width: 35%;">Primary Optimization Goals</th>
            <th style="padding: 10px 14px; width: 40%;">Tolerated Trade-offs</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700;">Batch Systems</td>
            <td style="padding: 10px 14px; color: #0f172a;">Maximize throughput, minimize turnaround time, maximize CPU utilization.</td>
            <td style="padding: 10px 14px; color: var(--text-muted);">High response latency is completely acceptable; human users are not waiting interactively.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700;">Interactive Systems</td>
            <td style="padding: 10px 14px; color: #0284c7;">Minimize response time, enforce proportionality, prevent starvation.</td>
            <td style="padding: 10px 14px; color: var(--text-muted);">Frequent context switches waste 2% to 5% of raw CPU capacity to preserve user responsiveness.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700;">Real-Time Systems</td>
            <td style="padding: 10px 14px; color: #059669;">Guarantee hard/soft deadlines, deterministic execution predictability.</td>
            <td style="padding: 10px 14px; color: var(--text-muted);">Sacrifices average throughput and hardware utilization to ensure worst-case timing bounds are met.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <nav class="nav-bar" style="margin-top: 36px; border-bottom: none; border-top: 1px solid var(--border); padding-top: 16px;">
      <span></span>
      <a href="index.html">&#127968; Week 3 Index</a>
      <a href="02-batch-scheduling.html">Next: 02. Batch Scheduling &rarr;</a>
    </nav>
  </div>

  <script>
    const schedSteps = {
      preempt: [
        {
          entity: "Process A (Compute-Bound)",
          quantum: "Timer: 8ms Remaining",
          mode: "User Mode (Ring 3)",
          lat: "0 ms (Process B Queued)",
          activeName: "Process A (Compute)",
          activeDetails: "Burst: Infinite Math Loop",
          activeQuantum: "Quantum: 8ms Remaining",
          coreMode: "Status: Executing Ring 3",
          taskBState: "State: Ready (Key Waiting)",
          showPreempt: false,
          narrative: "Process A runs uninterrupted on CPU Core 0, performing intensive matrix calculations. Process B enters the Ready queue awaiting interactive input processing.",
          what: "Process A executes unconstrained in User Mode. Process B arrives in the Ready queue after a keyboard keystroke triggers an asynchronous interrupt.",
          why: "The CPU maintains maximum instruction throughput by keeping the execution pipeline full with Process A until an interrupt forces an intervention."
        },
        {
          entity: "Hardware APIC Timer Interrupt",
          quantum: "Timer Expired: 0ms (TRAP)",
          mode: "Kernel Mode (Ring 0)",
          lat: "Interrupt Vector 0x20",
          activeName: "Kernel APIC Handler",
          activeDetails: "Saving Process A Context",
          activeQuantum: "Preempting Process A",
          coreMode: "Status: Supervisor Mode (Ring 0)",
          taskBState: "State: High Priority Ready",
          showPreempt: true,
          narrative: "The local APIC hardware timer interrupt fires as Process A's 10ms quantum expires. The CPU drops into Ring 0, saves Process A's registers to its PCB, and marks it preempted.",
          what: "A hardware timer interrupt vectors execution into the kernel. The dispatcher stops Process A and enqueues it at the tail of the Ready list.",
          why: "Preemptive multitasking guarantees that compute-bound tasks cannot monopolize the hardware or starve interactive user applications."
        },
        {
          entity: "Process B (Interactive Scheduled)",
          quantum: "Dispatched: 10ms Quantum",
          mode: "User Mode (Ring 3)",
          lat: "Response Latency: 1.2 ms",
          activeName: "Process B (Interactive)",
          activeDetails: "Handling Keypress Event",
          activeQuantum: "Yields after 0.8ms (I/O)",
          coreMode: "Status: Executing Ring 3",
          taskBState: "State: Process A Ready",
          showPreempt: false,
          narrative: "The scheduler selects Process B from the Ready queue. The dispatcher loads Process B's registers and virtual memory map. The keystroke is rendered on screen within 1.2ms.",
          what: "Process B runs immediately, executes its brief 0.8ms burst to render the character glyph, and voluntarily blocks on the next keystroke.",
          why: "Prioritizing interactive I/O bursts ensures near-zero user perceptible lag while allowing background compute jobs to resume immediately afterward."
        }
      ],
      coop: [
        {
          entity: "Process A (Compute-Bound)",
          quantum: "Cooperative: No Timer",
          mode: "User Mode (Ring 3)",
          lat: "0 ms (Process B Arrives)",
          activeName: "Process A (Compute)",
          activeDetails: "Burst: Infinite Math Loop",
          activeQuantum: "No Preemption Mechanism",
          coreMode: "Status: Executing Ring 3",
          taskBState: "State: Starving in Ready",
          showPreempt: false,
          narrative: "Process A executes a compute-bound loop under cooperative multitasking. Process B arrives in the Ready queue with a user keystroke.",
          what: "Process A owns the CPU core. There are no hardware timer interrupts configured to forcibly preempt user code.",
          why: "Cooperative systems avoid timer interrupt overhead and kernel context switching costs, assuming all applications yield voluntarily."
        },
        {
          entity: "Process A Continues Monopolizing",
          quantum: "No Voluntary Yield Called",
          mode: "User Mode (Infinite Loop)",
          lat: "ALERT: 500 ms Latency",
          activeName: "Process A (Compute)",
          activeDetails: "Ignoring Yield Calls",
          activeQuantum: "Never Blocks on I/O",
          coreMode: "Status: Locked to Process A",
          taskBState: "State: Starved (Frozen UI)",
          showPreempt: false,
          narrative: "Process A never invokes a voluntary yield system call. Process B waits indefinitely in the Ready queue. The desktop user interface stutters and becomes completely unresponsive.",
          what: "Process A continues running arithmetic instructions. Because it does not issue I/O requests, the operating system kernel is never invoked.",
          why: "Without preemption, the operating system is entirely at the mercy of application software correctness. A single bug or malicious loop freezes the entire system."
        },
        {
          entity: "System Frozen / Failure State",
          quantum: "System Latency: &infin; ms",
          mode: "User Stalled / Hard Hang",
          lat: "CRITICAL: System Deadlock",
          activeName: "Process A (Monopolized)",
          activeDetails: "Operating System Powerless",
          activeQuantum: "Requires Hardware Reset",
          coreMode: "Status: Completely Stalled",
          taskBState: "State: Starvation Hang",
          showPreempt: false,
          narrative: "Process B and all other system processes are completely starved of CPU cycles. The entire system is frozen, requiring a manual hardware power cycle or hard reboot.",
          what: "The cooperative model fails catastrophically under non-yielding or compute-bound workloads.",
          why: "This historical failure mode led all modern general-purpose operating systems to mandate hardware-enforced preemptive scheduling."
        }
      ]
    };

    let activeSchedDim = "preempt";
    let activeSchedStep = 0;

    function renderSchedStepper() {
      const steps = schedSteps[activeSchedDim];
      const step = steps[activeSchedStep];

      // Update Live Telemetry
      document.getElementById("s-telem-entity").textContent = step.entity;
      document.getElementById("s-telem-quantum").textContent = step.quantum;
      document.getElementById("s-telem-mode").textContent = step.mode;
      document.getElementById("s-telem-lat").textContent = step.lat;

      // Update Canvas Nodes
      document.getElementById("txt-active-name").textContent = step.activeName;
      document.getElementById("txt-active-details").textContent = step.activeDetails;
      document.getElementById("txt-active-quantum").textContent = step.activeQuantum;
      document.getElementById("txt-core-mode").textContent = step.coreMode;
      document.getElementById("txt-task-b-state").textContent = step.taskBState;

      // Preemption Visual Path
      const preemptPath = document.getElementById("path-preempt");
      const preemptLabel = document.getElementById("txt-preempt-label");
      if (step.showPreempt) {
        preemptPath.style.display = "block";
        preemptLabel.style.display = "block";
      } else {
        preemptPath.style.display = "none";
        preemptLabel.style.display = "none";
      }

      // Update Narrative Panel
      document.getElementById("s-txt-narrative").textContent = step.narrative;
      document.getElementById("s-btn-prev").disabled = (activeSchedStep === 0);
      document.getElementById("s-btn-next").disabled = (activeSchedStep === steps.length - 1);

      // Update Analytical Panes
      document.getElementById("s-txt-what").textContent = step.what;
      document.getElementById("s-txt-why").textContent = step.why;
    }

    function stepSched(delta) {
      const steps = schedSteps[activeSchedDim];
      activeSchedStep = Math.max(0, Math.min(steps.length - 1, activeSchedStep + delta));
      renderSchedStepper();
    }

    function resetSched() {
      activeSchedStep = 0;
      renderSchedStepper();
    }

    function setSchedDim(dim) {
      activeSchedDim = dim;
      activeSchedStep = 0;
      document.getElementById("dim-preempt").classList.toggle("active", dim === "preempt");
      document.getElementById("dim-coop").classList.toggle("active", dim === "coop");

      const scenarioText = dim === "preempt"
        ? "Process A (Compute-Bound Matrix Math) is executing. Process B (Interactive User Input) arrives in the Ready queue. Tracking how preemptive timer interrupts ensure responsive scheduling."
        : "Process A executes under cooperative multitasking without hardware timer interrupts. Observing the starvation hazard when a compute-bound task refuses to yield.";
      document.getElementById("sched-scenario-text").innerHTML = scenarioText;

      renderSchedStepper();
    }

    document.addEventListener("DOMContentLoaded", () => {
      renderSchedStepper();
    });
  </script>
</body>
</html>
"""

def execute_module_expansion():
    os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(MODULE_HTML.strip() + "\n")

    print(f"--> Successfully expanded {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Module 01 in week03-process-scheduling with interactive stepper\n\n"
            "Add deep technical analysis of the CPU-I/O burst cycle, dispatch latency,\n"
            "scheduling triggers, optimization trade-offs, and a dual-mode stepper."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    execute_module_expansion()
