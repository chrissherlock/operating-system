#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand NPTL and clone(2) in 04-thread-implementation.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "04-thread-implementation.html")

MODULE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>04. Thread Implementation &amp; APIs | Week 2: Processes &amp; Concurrency</title>
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

    /* Code Syntax Highlighting Tokens */
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
    svg.thread-canvas {
      width: 100%;
      max-width: 720px;
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
    .boundary-line {
      stroke: #94a3b8;
      stroke-dasharray: 6 4;
      stroke-width: 1.5;
    }
    .node-box {
      fill: #ffffff;
      stroke: #cbd5e1;
      stroke-width: 2;
      transition: all 0.3s ease;
    }
    .node-box.active {
      stroke: #0284c7;
      stroke-width: 2.5;
      fill: #f0f9ff;
    }
    .node-box.blocked {
      stroke: #d97706;
      stroke-width: 2.5;
      fill: #fef3c7;
    }
    .flow-edge {
      stroke: #cbd5e1;
      stroke-width: 2;
      fill: none;
      transition: all 0.3s ease;
    }
    .flow-edge.active {
      stroke: #0284c7;
      stroke-width: 3;
      filter: drop-shadow(0 0 3px rgba(2, 132, 199, 0.4));
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="03-classical-threads.html">&larr; Previous: 03. Classical Threads</a>
      <a href="index.html">&#127968; Week 2 Index</a>
      <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">Module 04 (End of Week 2)</span>
    </nav>

    <h2>04. Thread Implementation &amp; APIs</h2>
    <p>
      While the abstract thread model establishes threads as lightweight units of execution sharing an address space, operating systems differ substantially in how they implement, schedule, and expose threads to user programs. The two dominant modern computing platforms—<strong>Windows NT</strong> and <strong>UNIX/Linux</strong>—solve this fundamental engineering challenge through contrasting architectural philosophies.
    </p>

    <h3>1. Architectural Implementation Models: ULT vs. KLT</h3>
    <p>
      Operating system threads are categorized based on whether execution states are tracked in <strong>user space</strong>, directly within the <strong>operating system kernel</strong>, or through a hybrid combination:
    </p>

    <h4>User-Level Threads (ULT: Many-to-One Model)</h4>
    <p>
      In a pure user-level thread implementation, the operating system kernel is completely oblivious to multithreading. The kernel manages only the parent process container as a single scheduling entity with one Process Control Block (PCB).
    </p>
    <ul>
      <li><strong>User-Space Runtime Library:</strong> All thread creation, destruction, and scheduling decisions are handled by a user-space library (such as historical Green Threads, GNU Pth, or modern language coroutines).</li>
      <li><strong>Thread Switching Speed:</strong> Switching between user threads requires only swapping CPU registers and the stack pointer using unprivileged assembly instructions (analogous to <code>setjmp</code> and <code>longjmp</code>). It incurs zero supervisor trap overhead, completing in nanoseconds.</li>
      <li><strong>The Inherent Flaws:</strong>
        <ol>
          <li><em>The Blocking Call Vulnerability:</em> If any user thread invokes a synchronous, blocking system call (such as reading a disk sector), the kernel halts the entire process because it only sees one kernel thread. All sibling user threads are frozen.</li>
          <li><em>Lack of Hardware Multiprocessing:</em> Because the kernel assigns at most one physical CPU core to the process, a user-level multithreaded application can never execute across multiple cores simultaneously, regardless of how many cores the machine possesses.</li>
        </ol>
      </li>
    </ul>

    <h4>Kernel-Level Threads (KLT: One-to-One Model)</h4>
    <p>
      In a 1:1 kernel-level thread model, every user-level thread is backed directly by an official kernel scheduling entity. Both modern <strong>Windows</strong> and <strong>Linux</strong> utilize this model as their primary threading architecture.
    </p>
    <ul>
      <li><strong>True Multicore Execution:</strong> The kernel scheduler assigns independent threads of the same process to separate physical CPU cores, achieving true simultaneous hardware execution in silicon.</li>
      <li><strong>Isolated I/O Blocking:</strong> When one thread blocks on disk or network I/O, the kernel puts only that specific thread to sleep, keeping sibling threads executing unimpeded.</li>
      <li><strong>Context Switch Overhead:</strong> Thread creation, destruction, and context switching require entering supervisor mode (Ring 0) via a system call trap, incurring higher CPU overhead than user-space switches.</li>
    </ul>

    <!-- Directed Narrative Stepper Standard: Thread Implementation Models -->
    <div class="aid-wrapper">
      <div class="aid-header">
        <h4>Interactive Stepper: Thread Implementation Architectures in Action</h4>
        <div class="dimension-toggles">
          <button class="dim-btn active" id="dim-klt" onclick="setImplDim('klt')">Kernel Threads (1:1 Model - Windows &amp; Linux)</button>
          <button class="dim-btn" id="dim-ult" onclick="setImplDim('ult')">User Threads (Many-to-One - Green Threads / Fibers)</button>
        </div>
      </div>

      <div class="scenario-banner">
        <span class="scenario-tag">Scenario Arc</span>
        <span id="impl-scenario-text">Thread 1 runs compute, Thread 2 blocks on a disk read(), and Thread 3 handles background tasks. Observing how kernel-level versus user-level thread managers react to blocking I/O.</span>
      </div>

      <div class="telemetry-strip">
        <div class="telemetry-cell">
          <span class="telemetry-label">Active Phase</span>
          <span class="telemetry-val highlight" id="m-telem-phase">1. Multi-Core Execution</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Scheduling Entity</span>
          <span class="telemetry-val" id="m-telem-sched">OS Kernel Scheduler</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Kernel Privilege Level</span>
          <span class="telemetry-val" id="m-telem-ring">Ring 0 Supervised</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Core Saturation</span>
          <span class="telemetry-val" id="m-telem-cores">3 Cores Saturated</span>
        </div>
      </div>

      <div class="canvas-container">
        <svg class="thread-canvas" viewBox="0 0 720 260">
          <defs>
            <marker id="arrhead" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#64748b" />
            </marker>
            <marker id="arrhead-act" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
            </marker>
          </defs>

          <!-- User Space vs Kernel Space Boundary -->
          <line class="boundary-line" x1="20" y1="130" x2="700" y2="130" />
          <text x="30" y="24" font-family="system-ui" font-size="11" font-weight="700" fill="#64748b">USER SPACE (Ring 3)</text>
          <text x="30" y="148" font-family="system-ui" font-size="11" font-weight="700" fill="#64748b">KERNEL SPACE (Ring 0)</text>

          <!-- User Space Threads -->
          <g id="box-ut1" transform="translate(60, 40)">
            <rect class="node-box active" width="130" height="65" rx="6"/>
            <text x="15" y="26" font-family="system-ui" font-size="11" font-weight="700" fill="#0f172a">Thread / Fiber 1</text>
            <text id="ut1-sub" x="15" y="44" font-family="var(--font-mono)" font-size="10" fill="#0284c7">Compute Burst</text>
          </g>

          <g id="box-ut2" transform="translate(295, 40)">
            <rect class="node-box" width="130" height="65" rx="6"/>
            <text x="15" y="26" font-family="system-ui" font-size="11" font-weight="700" fill="#0f172a">Thread / Fiber 2</text>
            <text id="ut2-sub" x="15" y="44" font-family="var(--font-mono)" font-size="10" fill="#64748b">Ready to Read</text>
          </g>

          <g id="box-ut3" transform="translate(530, 40)">
            <rect class="node-box" width="130" height="65" rx="6"/>
            <text x="15" y="26" font-family="system-ui" font-size="11" font-weight="700" fill="#0f172a">Thread / Fiber 3</text>
            <text id="ut3-sub" x="15" y="44" font-family="var(--font-mono)" font-size="10" fill="#64748b">Ready Queue</text>
          </g>

          <!-- Mapping Edges -->
          <path id="map-edge-1" class="flow-edge active" d="M 125 105 L 125 170" marker-end="url(#arrhead-act)" />
          <path id="map-edge-2" class="flow-edge active" d="M 360 105 L 360 170" marker-end="url(#arrhead-act)" />
          <path id="map-edge-3" class="flow-edge active" d="M 595 105 L 595 170" marker-end="url(#arrhead-act)" />

          <!-- Kernel Space Entities -->
          <g id="box-kt-1" transform="translate(60, 170)">
            <rect class="node-box active" width="130" height="65" rx="6"/>
            <text id="txt-kt1-title" x="15" y="26" font-family="system-ui" font-size="11" font-weight="700" fill="#0f172a">Kernel TCB 1</text>
            <text id="txt-kt1-status" x="15" y="44" font-family="var(--font-mono)" font-size="10" fill="#0284c7">Core 0: RUNNING</text>
          </g>

          <g id="box-kt-2" transform="translate(295, 170)">
            <rect class="node-box" width="130" height="65" rx="6"/>
            <text id="txt-kt2-title" x="15" y="26" font-family="system-ui" font-size="11" font-weight="700" fill="#0f172a">Kernel TCB 2</text>
            <text id="txt-kt2-status" x="15" y="44" font-family="var(--font-mono)" font-size="10" fill="#64748b">Core 1: RUNNING</text>
          </g>

          <g id="box-kt-3" transform="translate(530, 170)">
            <rect class="node-box" width="130" height="65" rx="6"/>
            <text id="txt-kt3-title" x="15" y="26" font-family="system-ui" font-size="11" font-weight="700" fill="#0f172a">Kernel TCB 3</text>
            <text id="txt-kt3-status" x="15" y="44" font-family="var(--font-mono)" font-size="10" fill="#64748b">Core 2: RUNNING</text>
          </g>
        </svg>
      </div>

      <!-- Stepper Controls & Current Step Summary Panel -->
      <div class="controls-narrative-strip">
        <div class="stepper-btn-group">
          <button class="btn-step" id="m-btn-prev" onclick="stepImpl(-1)" disabled>&larr; Previous</button>
          <button class="btn-step" id="m-btn-next" onclick="stepImpl(1)">Next Step &rarr;</button>
          <button class="btn-step" id="m-btn-reset" onclick="resetImpl()">Reset</button>
        </div>
        <div class="narrative-preview-panel">
          <strong>Current Step Summary</strong>
          <span id="m-txt-narrative">In a 1:1 kernel thread model, each user thread maps to an independent kernel scheduling object (ETHREAD on Windows, task_struct on Linux). All three physical CPU cores execute instructions concurrently.</span>
        </div>
      </div>

      <div class="analytical-grid">
        <div class="pane-card">
          <div class="pane-title what">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            What Is Happening
          </div>
          <p class="pane-content" id="m-txt-what">Each thread has a dedicated kernel TCB. The operating system dispatcher maps each thread to a separate hardware core simultaneously.</p>
        </div>
        <div class="pane-card">
          <div class="pane-title why">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
            Why The System Does This
          </div>
          <p class="pane-content" id="m-txt-why">Kernel-level threads enable true symmetric multiprocessing (SMP) parallelism, allowing compute-bound applications to scale linearly with physical core counts.</p>
        </div>
      </div>
    </div>

    <h3>2. The Windows NT Threading Architecture</h3>
    <p>
      Windows was architected from its inception as a native, multithreaded operating system. Unlike early UNIX implementations where threads were bolted onto existing process models, Windows treats the <strong>thread as the fundamental unit of CPU execution</strong> and the <strong>process as a passive resource container</strong>.
    </p>

    <h4>The Kernel Representation: ETHREAD and KTHREAD</h4>
    <p>
      Within the Windows NT kernel, every thread is represented by a two-tiered data structure:
    </p>
    <ul>
      <li><strong>ETHREAD (Executive Thread Block):</strong> Resides in the Windows Executive layer (upper kernel mode). It encapsulates higher-level management data: the thread's access token, process ownership pointer (to <code>EPROCESS</code>), thread impersonation security contexts, I/O request lists (IRP list), and cross-thread communication endpoints.</li>
      <li><strong>KTHREAD (Kernel Thread Block):</strong> Embedded directly within the <code>ETHREAD</code> structure, it resides in the Windows Microkernel layer. It contains hardware-critical execution state: the kernel execution stack, machine register context, hardware scheduling priority (0 to 31), processor affinity masks, dispatching state (Ready, Running, Standby, Waiting), and quantum counters.</li>
    </ul>

    <h4>The Win32 Thread Management API</h4>
    <p>
      Windows exposes thread lifecycle and synchronization management via the Win32 subsystem API:
    </p>
    <pre><code><span class="syn-kwd">#include</span> <span class="syn-var">&lt;windows.h&gt;</span>
<span class="syn-kwd">#include</span> <span class="syn-var">&lt;stdio.h&gt;</span>

<span class="syn-type">CRITICAL_SECTION</span> <span class="syn-var">cs</span><span class="syn-punc">;</span>
<span class="syn-type">LONG</span> <span class="syn-var">shared_val</span> <span class="syn-punc">=</span> <span class="syn-var">0</span><span class="syn-punc">;</span>

<span class="syn-type">DWORD</span> <span class="syn-var">WINAPI</span> <span class="syn-fn">WorkerRoutine</span><span class="syn-punc">(</span><span class="syn-type">LPVOID</span> <span class="syn-var">lpParam</span><span class="syn-punc">) {</span>
    <span class="syn-type">LONG</span> <span class="syn-var">iterations</span> <span class="syn-punc">= *(</span><span class="syn-type">LONG</span><span class="syn-punc">*)</span><span class="syn-var">lpParam</span><span class="syn-punc">;</span>
    <span class="syn-kwd">for</span> <span class="syn-punc">(</span><span class="syn-type">LONG</span> <span class="syn-var">i</span> <span class="syn-punc">=</span> <span class="syn-var">0</span><span class="syn-punc">;</span> <span class="syn-var">i</span> <span class="syn-punc">&lt;</span> <span class="syn-var">iterations</span><span class="syn-punc">;</span> <span class="syn-var">i</span><span class="syn-punc">++) {</span>
        <span class="syn-fn">EnterCriticalSection</span><span class="syn-punc">(&amp;</span><span class="syn-var">cs</span><span class="syn-punc">);</span>
        <span class="syn-var">shared_val</span><span class="syn-punc">++;</span>  <span class="syn-cmt">/* Fast user-mode mutual exclusion */</span>
        <span class="syn-fn">LeaveCriticalSection</span><span class="syn-punc">(&amp;</span><span class="syn-var">cs</span><span class="syn-punc">);</span>
    <span class="syn-punc">}</span>
    <span class="syn-kwd">return</span> <span class="syn-var">0</span><span class="syn-punc">;</span>
<span class="syn-punc">}</span>

<span class="syn-type">int</span> <span class="syn-fn">main</span><span class="syn-punc">() {</span>
    <span class="syn-type">HANDLE</span> <span class="syn-var">hThreads</span><span class="syn-punc">[</span><span class="syn-var">2</span><span class="syn-punc">];</span>
    <span class="syn-type">LONG</span> <span class="syn-var">loop_count</span> <span class="syn-punc">=</span> <span class="syn-var">500000</span><span class="syn-punc">;</span>

    <span class="syn-fn">InitializeCriticalSection</span><span class="syn-punc">(&amp;</span><span class="syn-var">cs</span><span class="syn-punc">);</span>

    <span class="syn-var">hThreads</span><span class="syn-punc">[</span><span class="syn-var">0</span><span class="syn-punc">] =</span> <span class="syn-fn">CreateThread</span><span class="syn-punc">(</span><span class="syn-var">NULL</span><span class="syn-punc">,</span> <span class="syn-var">0</span><span class="syn-punc">,</span> <span class="syn-var">WorkerRoutine</span><span class="syn-punc">, &amp;</span><span class="syn-var">loop_count</span><span class="syn-punc">,</span> <span class="syn-var">0</span><span class="syn-punc">,</span> <span class="syn-var">NULL</span><span class="syn-punc">);</span>
    <span class="syn-var">hThreads</span><span class="syn-punc">[</span><span class="syn-var">1</span><span class="syn-punc">] =</span> <span class="syn-fn">CreateThread</span><span class="syn-punc">(</span><span class="syn-var">NULL</span><span class="syn-punc">,</span> <span class="syn-var">0</span><span class="syn-punc">,</span> <span class="syn-var">WorkerRoutine</span><span class="syn-punc">, &amp;</span><span class="syn-var">loop_count</span><span class="syn-punc">,</span> <span class="syn-var">0</span><span class="syn-punc">,</span> <span class="syn-var">NULL</span><span class="syn-punc">);</span>

    <span class="syn-cmt">/* Synchronize with all worker threads simultaneously */</span>
    <span class="syn-fn">WaitForMultipleObjects</span><span class="syn-punc">(</span><span class="syn-var">2</span><span class="syn-punc">,</span> <span class="syn-var">hThreads</span><span class="syn-punc">,</span> <span class="syn-var">TRUE</span><span class="syn-punc">,</span> <span class="syn-var">INFINITE</span><span class="syn-punc">);</span>

    <span class="syn-fn">CloseHandle</span><span class="syn-punc">(</span><span class="syn-var">hThreads</span><span class="syn-punc">[</span><span class="syn-var">0</span><span class="syn-punc">]);</span>
    <span class="syn-fn">CloseHandle</span><span class="syn-punc">(</span><span class="syn-var">hThreads</span><span class="syn-punc">[</span><span class="syn-var">1</span><span class="syn-punc">]);</span>
    <span class="syn-fn">DeleteCriticalSection</span><span class="syn-punc">(&amp;</span><span class="syn-var">cs</span><span class="syn-punc">);</span>
    <span class="syn-kwd">return</span> <span class="syn-var">0</span><span class="syn-punc">;</span>
<span class="syn-punc">}</span></code></pre>

    <h4>Windows Fibers: Cooperative User-Mode Scheduling</h4>
    <p>
      In addition to native kernel threads, Windows natively implements <strong>Fibers</strong>—a pure user-level, cooperative threading mechanism (Many-to-One / Many-to-Many):
    </p>
    <ul>
      <li>A thread converts itself to a fiber by calling <code>ConvertThreadToFiber()</code>.</li>
      <li>Additional fibers are created in user space via <code>CreateFiber()</code>. Each fiber possesses its own private execution stack and user-mode context, but shares the underlying kernel thread.</li>
      <li>Fibers yield control explicitly using <code>SwitchToFiber(lpFiber)</code>. The switch executes entirely in User Mode (Ring 3) without kernel intervention.</li>
      <li><em>Engineering Context:</em> Microsoft originally introduced Fibers to simplify porting existing UNIX database engines (such as early Microsoft SQL Server architectures based on Sybase) that relied heavily on user-space thread schedulers.</li>
    </ul>

    <h3>3. The Linux NPTL Architecture &amp; clone(2)</h3>
    <p>
      Linux approaches threading from an entirely unique conceptual angle. Rather than distinguishing sharply between a "process" container and a "thread" object, the Linux kernel manages all execution contexts uniformly as <strong>tasks</strong>, each represented internally by a <code>struct task_struct</code>.
    </p>
    <p>
      Whether a task behaves as an independent, fully isolated process or as a cooperative thread sharing memory is simply a matter of configuration flags supplied to the <strong><code>clone(2)</code></strong> system call.
    </p>

    <h4>1. Historical Evolution: From LinuxThreads to NPTL</h4>
    <p>
      Early Linux threading relied on the <strong>LinuxThreads</strong> library, which suffered from severe architectural flaws that violated the POSIX specification:
    </p>
    <ul>
      <li><strong>The Manager Thread Bottleneck:</strong> A dedicated "manager thread" had to handle all thread creation, teardown, and signal handling in user space, creating severe scalability bottlenecks on multi-socket systems.</li>
      <li><strong>Divergent Process IDs:</strong> Each thread had a distinct Process ID (PID) visible in <code>getpid()</code>. Two threads in the same application saw different PIDs, breaking POSIX compliance.</li>
      <li><strong>Broken Signal Handling:</strong> Signals sent to the process (such as <code>SIGTERM</code> or <code>SIGKILL</code>) were delivered to only one specific thread rather than the entire thread group. Signal dispositions could not be synchronized reliably across threads.</li>
      <li><strong>User/Group ID Discrepancies:</strong> Changing credentials (e.g., via <code>setuid()</code>) in one thread did not propagate to sibling threads, creating dangerous security vulnerabilities.</li>
    </ul>
    <p>
      To resolve these structural defects, the Linux kernel was fundamentally enhanced with the release of kernel 2.6. Ingo Molnar and Ulrich Drepper developed the <strong>Native POSIX Thread Library (NPTL)</strong>, enabled by three major kernel-level innovations:
    </p>
    <ol>
      <li><strong>Thread Group ID (TGID) Architecture:</strong> Unifying all threads under a shared process identity in <code>struct task_struct</code>.</li>
      <li><strong>Fast Userspace Mutexes (<code>futex</code>):</strong> Allowing synchronization locks to be acquired and released in user space without entering the kernel unless contention occurs.</li>
      <li><strong>Enhanced <code>clone()</code> Flags:</strong> Providing fine-grained kernel mechanisms to synchronize thread credentials, signal queues, and lifecycle notifications.</li>
    </ol>

    <h4>2. The Unified Task Abstraction: PID vs. TGID</h4>
    <p>
      In modern Linux, every schedulable entity is an instance of <code>struct task_struct</code>. The kernel reconciles thread grouping through a dual-identity model:
    </p>
    <ul>
      <li><strong>The Thread ID (<code>task-&gt;pid</code>):</strong> Every task receives a globally unique integer ID assigned by the kernel allocator. Within kernel space, this is called the task's <strong>PID</strong>, but to user-space applications, it is exposed as the <strong>Thread ID (TID)</strong>, queried via the <code>gettid()</code> system call.</li>
      <li><strong>The Thread Group ID (<code>task-&gt;tgid</code>):</strong> When the first thread of a program (the main thread) is spawned via <code>fork()</code> or <code>execve()</code>, its <code>tgid</code> is set equal to its <code>pid</code>. This main thread becomes the <strong>Thread Group Leader</strong>.</li>
      <li>When subsequent threads are spawned using <code>clone()</code> with the <code>CLONE_THREAD</code> flag, the kernel sets the child's <code>tgid</code> to match the parent's <code>tgid</code>:
        <pre><code><span class="syn-cmt">/* Kernel representation inside task_struct: */</span>
<span class="syn-type">pid_t</span> <span class="syn-var">pid</span><span class="syn-punc">;</span>   <span class="syn-cmt">/* Unique to this specific thread (TID) */</span>
<span class="syn-type">pid_t</span> <span class="syn-var">tgid</span><span class="syn-punc">;</span>  <span class="syn-cmt">/* Shared across all threads in process (POSIX PID) */</span></code></pre>
      </li>
      <li>The standard POSIX <code>getpid()</code> system call returns <code>task-&gt;tgid</code>, ensuring that every thread in the application observes the exact same Process ID, fully satisfying POSIX compliance.</li>
    </ul>

    <h4>3. Deep Breakdown of clone(2) and clone3(2)</h4>
    <p>
      The core mechanism behind thread creation in NPTL is the <code>clone(2)</code> system call (and the modern 64-bit extensible <code>clone3(2)</code> system call). Unlike <code>fork()</code> which duplicates all resources, <code>clone()</code> accepts bitmask flags specifying exactly which resources should be <em>shared by reference</em> versus <em>copied</em>:
    </p>

    <div style="overflow-x: auto; margin: 16px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 14px; width: 30%;">Clone Flag</th>
            <th style="padding: 10px 14px; width: 70%;">Kernel Mechanism &amp; Resource Sharing Behavior</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;"><code>CLONE_VM</code></td>
            <td style="padding: 10px 14px;">The child task shares the caller's memory descriptor (<code>task-&gt;mm</code>). Both tasks point to the same page table directory root (CR3). Any memory allocation, deallocation, or page modification by one task is immediately visible to the other.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;"><code>CLONE_FILES</code></td>
            <td style="padding: 10px 14px;">The child shares the open file descriptor table (<code>task-&gt;files</code>). File descriptors opened or closed by one thread are instantly updated across all threads.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;"><code>CLONE_FS</code></td>
            <td style="padding: 10px 14px;">The child shares filesystem attributes (<code>task-&gt;fs</code>), including root directory, current working directory, and the file mode creation mask (<code>umask</code>).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;"><code>CLONE_SIGHAND</code></td>
            <td style="padding: 10px 14px;">The child shares signal dispositions and handlers (<code>task-&gt;sighand</code>). Calling <code>sigaction()</code> in one thread updates the signal handler for all sibling threads. Requires <code>CLONE_VM</code>.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;"><code>CLONE_THREAD</code></td>
            <td style="padding: 10px 14px;">The child is placed into the same thread group as the caller (inheriting the same <code>tgid</code>). The parent of the new thread is set to the parent of the calling thread, preventing deep hierarchical process trees. Requires <code>CLONE_SIGHAND</code>.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;"><code>CLONE_SYSVSEM</code></td>
            <td style="padding: 10px 14px;">The child shares System V semaphore undo values (<code>semundo</code>), preventing resource leaks when individual threads terminate.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;"><code>CLONE_SETTLS</code></td>
            <td style="padding: 10px 14px;">Instructs the kernel to load the architecture segment register (e.g., <code>%fs</code> base on x86-64) with the memory address of the new thread's Thread Control Block (TCB), establishing Thread-Local Storage during creation.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;"><code>CLONE_CHILD_CLEARTID</code></td>
            <td style="padding: 10px 14px;">Directs the kernel to zero out a specified memory address in user space when the child terminates (<code>do_exit()</code>) and wake any waiting threads via a <code>futex</code> wake system call. This is the exact mechanism that enables non-polling <code>pthread_join()</code>.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h5>Classical Process Spawning vs. Thread Creation in Terms of clone()</h5>
    <p>
      The flexibility of <code>clone()</code> unifies all process and thread creation across the entire Linux operating system:
    </p>
    <ul>
      <li><strong>Standard <code>fork()</code>:</strong> Equivalent to calling <code>clone(SIGCHLD, 0)</code>—zero resource-sharing flags set; full Copy-on-Write page table duplication.</li>
      <li><strong>Optimized <code>vfork()</code>:</strong> Equivalent to <code>clone(CLONE_VM | CLONE_VFORK | SIGCHLD, 0)</code>—shares the parent's memory space temporarily and suspends the parent until the child calls <code>execve()</code> or <code>_exit()</code>.</li>
      <li><strong>POSIX <code>pthread_create()</code>:</strong> Implemented via NPTL by passing:
        <pre><code><span class="syn-fn">clone</span><span class="syn-punc">(</span><span class="syn-var">CLONE_VM</span> <span class="syn-punc">|</span> <span class="syn-var">CLONE_FS</span> <span class="syn-punc">|</span> <span class="syn-var">CLONE_FILES</span> <span class="syn-punc">|</span> <span class="syn-var">CLONE_SIGHAND</span> <span class="syn-punc">|</span>
      <span class="syn-var">CLONE_THREAD</span> <span class="syn-punc">|</span> <span class="syn-var">CLONE_SYSVSEM</span> <span class="syn-punc">|</span> <span class="syn-var">CLONE_SETTLS</span> <span class="syn-punc">|</span>
      <span class="syn-var">CLONE_PARENT_SETTID</span> <span class="syn-punc">|</span> <span class="syn-var">CLONE_CHILD_CLEARTID</span><span class="syn-punc">,</span>
      <span class="syn-var">child_stack</span><span class="syn-punc">,</span> <span class="syn-punc">&amp;</span><span class="syn-var">parent_tid</span><span class="syn-punc">,</span> <span class="syn-var">tls_ptr</span><span class="syn-punc">, &amp;</span><span class="syn-var">child_tid</span><span class="syn-punc">);</span></code></pre>
      </li>
    </ul>

    <h4>4. Fast Userspace Mutexes (futex)</h4>
    <p>
      Prior to NPTL, acquiring a mutual exclusion lock required a system call to ask the kernel to verify lock state. Because lock acquisitions in well-engineered applications are rarely contested (i.e., the lock is free 99% of the time), forcing a supervisor trap into Ring 0 on every lock acquisition severely degraded CPU performance.
    </p>
    <p>
      The <strong>futex (Fast Userspace Mutex)</strong> mechanism provides a high-performance hybrid locking primitive:
    </p>
    <ol>
      <li><strong>Uncontended Fast Path (User Space):</strong> To acquire a lock, the thread executes an atomic hardware assembly instruction (such as <code>CMPXCHG</code> on x86-64). If the integer value in user memory was <code>0</code> (free), it atomically transitions to <code>1</code> (locked). <em>No system call occurs; the operation completes in nanoseconds entirely in user space.</em></li>
      <li><strong>Contended Slow Path (Kernel Sleep):</strong> If another thread already holds the lock, the atomic compare-and-swap fails. The acquiring thread enters the kernel by issuing the <code>futex()</code> system call with the <code>FUTEX_WAIT</code> operation:
        <pre><code><span class="syn-fn">syscall</span><span class="syn-punc">(</span><span class="syn-var">SYS_futex</span><span class="syn-punc">, &amp;</span><span class="syn-var">lock_val</span><span class="syn-punc">,</span> <span class="syn-var">FUTEX_WAIT</span><span class="syn-punc">,</span> <span class="syn-var">1</span><span class="syn-punc">,</span> <span class="syn-var">NULL</span><span class="syn-punc">,</span> <span class="syn-var">NULL</span><span class="syn-punc">,</span> <span class="syn-var">0</span><span class="syn-punc">);</span></code></pre>
        The kernel places the calling task into a wait hash table associated with the physical memory address of <code>lock_val</code> and shifts its state to <code>TASK_INTERRUPTIBLE</code> (Blocked).</li>
      <li><strong>Release and Wakeup:</strong> When the lock holder finishes, it atomically decrements the lock integer. If it detects waiting threads, it invokes <code>futex(..., FUTEX_WAKE, 1)</code> to wake the next queued thread from the kernel sleep queue.</li>
    </ol>

    <h4>5. Signal Delivery Routing in NPTL</h4>
    <p>
      Under NPTL, signal dispatching distinguishes between <strong>process-directed signals</strong> and <strong>thread-directed signals</strong>:
    </p>
    <ul>
      <li><strong>Process-Directed Signals:</strong> Signals sent to the general process (e.g., via <code>kill(pid, SIGINT)</code>) are added to the shared pending signal queue of the thread group. The kernel selects <em>exactly one</em> arbitrary thread in the group that does not currently have the signal blocked in its signal mask, interrupting that thread to execute the signal handler.</li>
      <li><strong>Thread-Directed Signals:</strong> Hardware-generated exceptions tied to instruction execution (such as <code>SIGSEGV</code> on invalid memory access, <code>SIGFPE</code> on divide-by-zero, or explicit inter-thread signals via <code>pthread_kill(tid, sig)</code>) are placed into that specific thread's private pending signal queue. The faulting thread must handle the exception directly.</li>
    </ul>

    <h4>6. Thread Teardown and Reaping: How pthread_join() Works</h4>
    <p>
      When a process exits, the parent reaps its exit code via <code>waitpid()</code>. For threads, <code>pthread_join()</code> reaps the thread's return pointer. But how does <code>pthread_join()</code> know when a thread dies without constantly polling its state?
    </p>
    <p>
      NPTL implements this via the <code>CLONE_CHILD_CLEARTID</code> flag:
    </p>
    <ol>
      <li>When <code>pthread_create()</code> launches a thread, it passes the address of an internal integer field (<code>ctid</code>) inside the thread's Thread Control Block.</li>
      <li>When the thread terminates—either by calling <code>pthread_exit()</code> or returning from its start function—it executes the <code>exit</code> system call (<code>sys_exit</code>).</li>
      <li>Inside the kernel's <code>do_exit()</code> routine, the kernel checks whether <code>CLONE_CHILD_CLEARTID</code> was set. If so, the kernel:
        <ul>
          <li>Writes <code>0</code> directly into the user-space integer at <code>ctid</code>.</li>
          <li>Executes an internal <code>futex_wake()</code> on that exact memory address.</li>
        </ul>
      </li>
      <li>The joining thread, which had been suspended in <code>futex(..., FUTEX_WAIT, ...)</code> inside <code>pthread_join()</code>, is immediately awakened by the kernel, reads the return value from the thread's stack structure, and deallocates the thread stack.</li>
    </ol>

    <h3>4. Direct Architectural Comparison: Windows vs. POSIX/Linux</h3>
    <div style="overflow-x: auto; margin: 20px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 14px; width: 25%;">Feature / Mechanism</th>
            <th style="padding: 10px 14px; width: 37%;">Windows NT (Win32)</th>
            <th style="padding: 10px 14px; width: 38%;">UNIX / Linux (POSIX / NPTL)</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;">Kernel Representation</td>
            <td style="padding: 10px 14px;">Dedicated <code>ETHREAD</code> and <code>KTHREAD</code> objects in Executive/Kernel.</td>
            <td style="padding: 10px 14px;">Unified <code>struct task_struct</code> (treated as a task with shared pointers).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;">Thread Creation API</td>
            <td style="padding: 10px 14px;"><code>CreateThread()</code> / <code>_beginthreadex()</code></td>
            <td style="padding: 10px 14px;"><code>pthread_create()</code> (wraps <code>clone(2)</code>)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;">Synchronization Model</td>
            <td style="padding: 10px 14px;">Object Handles: <code>WaitForSingleObject</code>, <code>CRITICAL_SECTION</code>.</td>
            <td style="padding: 10px 14px;">Pthreads Primitives: <code>pthread_mutex_t</code> (powered by <code>futex</code>).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;">Hardware TLS Register</td>
            <td style="padding: 10px 14px;"><code>%gs</code> segment register points to Thread Information Block (TIB).</td>
            <td style="padding: 10px 14px;"><code>%fs</code> segment register points to Thread Control Block (TCB).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;">User-Space Cooperative Model</td>
            <td style="padding: 10px 14px;">Native Win32 <strong>Fibers</strong> (<code>CreateFiber</code>, <code>SwitchToFiber</code>).</td>
            <td style="padding: 10px 14px;">Language runtimes (goroutines) or POSIX <code>ucontext_t</code>.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <nav class="nav-bar" style="margin-top: 36px; border-bottom: none; border-top: 1px solid var(--border); padding-top: 16px;">
      <a href="03-classical-threads.html">&larr; Previous: 03. Classical Threads</a>
      <a href="index.html">&#127968; Week 2 Index</a>
      <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">Module 04 (End of Week 2)</span>
    </nav>
  </div>

  <script>
    const implSteps = {
      klt: [
        {
          phase: "1. Multi-Core Execution (Windows & Linux)",
          sched: "OS Kernel Scheduler (SMP)",
          ring: "Ring 0 Supervised",
          cores: "3 Cores Saturated",
          ut1State: "Active on Core 0",
          ut2State: "Active on Core 1",
          ut3State: "Active on Core 2",
          kt1Status: "Core 0: RUNNING",
          kt2Status: "Core 1: RUNNING",
          kt3Status: "Core 2: RUNNING",
          ut1BoxClass: "node-box active",
          ut2BoxClass: "node-box active",
          ut3BoxClass: "node-box active",
          kt1BoxClass: "node-box active",
          kt2BoxClass: "node-box active",
          kt3BoxClass: "node-box active",
          narrative: "In a 1:1 kernel thread model (Windows ETHREAD or Linux task_struct), each user thread maps to an independent kernel scheduling object. All three physical CPU cores execute instructions concurrently.",
          what: "Each thread has a dedicated kernel TCB. The operating system dispatcher maps each thread to a separate hardware core simultaneously.",
          why: "Kernel-level threads enable true symmetric multiprocessing (SMP) parallelism, allowing compute-bound applications to scale linearly with physical core counts."
        },
        {
          phase: "2. Thread 2 Blocks on I/O (Isolated Sleep)",
          sched: "Kernel Traps & Suspends Only Thread 2",
          ring: "Ring 0 Trap Handled",
          cores: "2 Cores Active (Core 0 & Core 2)",
          ut1State: "RUNNING on Core 0",
          ut2State: "BLOCKED on Disk I/O",
          ut3State: "RUNNING on Core 2",
          kt1Status: "Core 0: RUNNING",
          kt2Status: "Wait Queue: SLEEP",
          kt3Status: "Core 2: RUNNING",
          ut1BoxClass: "node-box active",
          ut2BoxClass: "node-box blocked",
          ut3BoxClass: "node-box active",
          kt1BoxClass: "node-box active",
          kt2BoxClass: "node-box blocked",
          kt3BoxClass: "node-box active",
          narrative: "Thread 2 executes a synchronous read() call. The kernel traps into Ring 0 and transitions ONLY Thread 2 into the I/O wait queue. Threads 1 and 3 continue executing on their respective cores without interruption.",
          what: "The kernel updates TCB 2 to BLOCKED and yields Core 1, while leaving TCB 1 and TCB 3 executing unimpeded on Core 0 and Core 2.",
          why: "Because the kernel maintains independent execution state for every thread, blocking operations are isolated to the faulting thread alone."
        },
        {
          phase: "3. I/O Completion & Multi-Core Re-Dispatch",
          sched: "Hardware Interrupt Wakes Thread 2",
          ring: "Kernel IRQ Vector Handled",
          cores: "All 3 Cores Saturated",
          ut1State: "Compute Finished",
          ut2State: "I/O Done (Resumed)",
          ut3State: "Processing Results",
          kt1Status: "Core 0: RUNNING",
          kt2Status: "Core 1: DISPATCHED",
          kt3Status: "Core 2: RUNNING",
          ut1BoxClass: "node-box active",
          ut2BoxClass: "node-box active",
          ut3BoxClass: "node-box active",
          kt1BoxClass: "node-box active",
          kt2BoxClass: "node-box active",
          kt3BoxClass: "node-box active",
          narrative: "The disk controller completes the transfer and triggers a hardware interrupt. The kernel awakens Thread 2, marks it Ready, and dispatches it to an idle core. All threads continue progressing concurrently.",
          what: "The kernel's disk interrupt handler moves TCB 2 from Blocked to Ready, restoring its execution context without user-space runtime intervention.",
          why: "Kernel-level multithreading guarantees optimal CPU utilization and high responsiveness, forming the foundation of modern POSIX/Linux and Windows systems."
        }
      ],
      ult: [
        {
          phase: "1. User-Space Execution (Many-to-One)",
          sched: "User Runtime Library / Fiber Manager",
          ring: "Ring 3 (Unprivileged User Mode)",
          cores: "1 Physical Core (Bound to Process)",
          ut1State: "Compute Burst",
          ut2State: "Ready to Read",
          ut3State: "Ready Queue",
          kt1Status: "Allocated to Core 0",
          kt2Status: "Unmapped",
          kt3Status: "Unmapped",
          ut1BoxClass: "node-box active",
          ut2BoxClass: "node-box",
          ut3BoxClass: "node-box",
          kt1BoxClass: "node-box active",
          kt2BoxClass: "node-box",
          kt3BoxClass: "node-box",
          narrative: "User Thread 1 executes arithmetic instructions inside the user-space runtime. The kernel schedules the single underlying process thread onto CPU Core 0, completely unaware that multiple sub-threads exist.",
          what: "User Thread 1 executes instructions on the CPU via the single kernel thread assigned to this process. Threads 2 and 3 sit inside the user runtime library's ready list.",
          why: "User-level threads allow applications to implement custom scheduling policies without kernel support, achieving near-zero overhead switches when operations remain non-blocking."
        },
        {
          phase: "2. Thread 2 Issues Blocking read()",
          sched: "System Call Trap to Kernel",
          ring: "Ring 0 Trap (Supervisor Mode)",
          cores: "Core 0 Stalled on I/O Trap",
          ut1State: "Yielded to T2",
          ut2State: "TRAPPED: read() Syscall",
          ut3State: "Ready Queue",
          kt1Status: "Trapped in sys_read()",
          kt2Status: "Unmapped",
          kt3Status: "Unmapped",
          ut1BoxClass: "node-box",
          ut2BoxClass: "node-box active",
          ut3BoxClass: "node-box",
          kt1BoxClass: "node-box active",
          kt2BoxClass: "node-box",
          kt3BoxClass: "node-box",
          narrative: "User Thread 2 issues a blocking disk read() system call. The CPU transitions into Ring 0 supervisor mode. Because the kernel only knows about the single process thread, it prepares to suspend the entire process.",
          what: "Thread 2 executes a syscall trap instruction. The kernel receives the request and issues an unbuffered block fetch command to the disk controller.",
          why: "The kernel cannot selectively schedule user threads it cannot see. To the kernel, the process is a single execution stream that has just blocked."
        },
        {
          phase: "3. Entire Process Frozen (Fatal Many-to-One Flaw)",
          sched: "Kernel Scheduler (Process Suspended)",
          ring: "Kernel Mode Suspension",
          cores: "0 Cores Active (Process Stalled)",
          ut1State: "STALLED (Process Blocked)",
          ut2State: "BLOCKED ON DISK",
          ut3State: "STALLED (Starved in User Ready)",
          kt1Status: "BLOCKED in Wait Queue",
          kt2Status: "Unmapped",
          kt3Status: "Unmapped",
          ut1BoxClass: "node-box blocked",
          ut2BoxClass: "node-box blocked",
          ut3BoxClass: "node-box blocked",
          kt1BoxClass: "node-box blocked",
          kt2BoxClass: "node-box",
          kt3BoxClass: "node-box",
          narrative: "The entire process is placed in the kernel's Blocked queue. Even though Thread 3 has compute work ready to execute, it cannot run because the process's sole kernel thread is suspended. This illustrates the primary vulnerability of pure user-level threads.",
          what: "The kernel marks the process as BLOCKED and removes it from the CPU runqueue. All user threads are starved of CPU time.",
          why: "Without scheduler activations or non-blocking system call wrappers, a blocking call in one thread inadvertently freezes all sibling threads."
        }
      ]
    };

    let activeImplDim = "klt";
    let activeImplStep = 0;

    function renderImplStepper() {
      const steps = implSteps[activeImplDim];
      const step = steps[activeImplStep];

      // Update Live Telemetry Strip
      document.getElementById("m-telem-phase").textContent = step.phase;
      document.getElementById("m-telem-sched").textContent = step.sched;
      document.getElementById("m-telem-ring").textContent = step.ring;
      document.getElementById("m-telem-cores").textContent = step.cores;

      // Update Node Subtitles
      document.getElementById("ut1-sub").textContent = step.ut1State;
      document.getElementById("ut2-sub").textContent = step.ut2State;
      document.getElementById("ut3-sub").textContent = step.ut3State;
      document.getElementById("txt-kt1-status").textContent = step.kt1Status;
      document.getElementById("txt-kt2-status").textContent = step.kt2Status;
      document.getElementById("txt-kt3-status").textContent = step.kt3Status;

      // Update SVG Node Classes
      document.getElementById("box-ut1").querySelector(".node-box").className.baseVal = step.ut1BoxClass;
      document.getElementById("box-ut2").querySelector(".node-box").className.baseVal = step.ut2BoxClass;
      document.getElementById("box-ut3").querySelector(".node-box").className.baseVal = step.ut3BoxClass;
      document.getElementById("box-kt-1").querySelector(".node-box").className.baseVal = step.kt1BoxClass;
      document.getElementById("box-kt-2").querySelector(".node-box").className.baseVal = step.kt2BoxClass;
      document.getElementById("box-kt-3").querySelector(".node-box").className.baseVal = step.kt3BoxClass;

      // Update Narrative Panel
      document.getElementById("m-txt-narrative").textContent = step.narrative;
      document.getElementById("m-btn-prev").disabled = (activeImplStep === 0);
      document.getElementById("m-btn-next").disabled = (activeImplStep === steps.length - 1);

      // Update Analytical Panes
      document.getElementById("m-txt-what").textContent = step.what;
      document.getElementById("m-txt-why").textContent = step.why;
    }

    function stepImpl(delta) {
      const steps = implSteps[activeImplDim];
      activeImplStep = Math.max(0, Math.min(steps.length - 1, activeImplStep + delta));
      renderImplStepper();
    }

    function resetImpl() {
      activeImplStep = 0;
      renderImplStepper();
    }

    function setImplDim(dim) {
      activeImplDim = dim;
      activeImplStep = 0;
      document.getElementById("dim-klt").classList.toggle("active", dim === "klt");
      document.getElementById("dim-ult").classList.toggle("active", dim === "ult");

      const isKlt = (dim === "klt");
      document.getElementById("txt-kt1-title").textContent = isKlt ? "Kernel TCB 1" : "Single Process PCB";
      document.getElementById("txt-kt2-title").textContent = isKlt ? "Kernel TCB 2" : "No Kernel Object";
      document.getElementById("txt-kt3-title").textContent = isKlt ? "Kernel TCB 3" : "No Kernel Object";

      // Mapping Edges in Many-to-One vs One-to-One
      const edge1 = document.getElementById("map-edge-1");
      const edge2 = document.getElementById("map-edge-2");
      const edge3 = document.getElementById("map-edge-3");

      if (isKlt) {
        edge1.setAttribute("d", "M 125 105 L 125 170");
        edge2.setAttribute("d", "M 360 105 L 360 170");
        edge3.setAttribute("d", "M 595 105 L 595 170");
      } else {
        edge1.setAttribute("d", "M 125 105 L 125 170");
        edge2.setAttribute("d", "M 360 105 L 125 170");
        edge3.setAttribute("d", "M 595 105 L 125 170");
      }

      const scenarioText = isKlt
        ? "Thread 1 runs compute, Thread 2 blocks on a disk read(), and Thread 3 handles background tasks. In a 1:1 kernel model (Windows & Linux), blocking calls are isolated to the calling thread."
        : "Thread 1 runs compute, Thread 2 issues a blocking disk read(), and Thread 3 is ready. In a Many-to-One model (User Threads / Fibers), one blocked call stalls the entire process.";
      document.getElementById("impl-scenario-text").innerHTML = scenarioText;

      renderImplStepper();
    }

    document.addEventListener("DOMContentLoaded", () => {
      renderImplStepper();
    });
  </script>
</body>
</html>
"""

def execute_expansion():
    os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(MODULE_HTML.strip() + "\n")

    print(f"--> Successfully expanded Section 3 in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand NPTL and clone(2) architecture in Module 04\n\n"
            "Detail task_struct PID/TGID duality, LinuxThreads historical flaws,\n"
            "clone3 flag mechanics, userspace futex locking, and signal routing."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    execute_expansion()
