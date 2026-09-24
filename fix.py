#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 3 in 03-classical-threads.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "03-classical-threads.html")

MODULE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>03. The Classical Thread Model | Week 2: Processes &amp; Concurrency</title>
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

    /* Diagram Styles */
    .mem-block {
      fill: #f8fafc;
      stroke: #cbd5e1;
      stroke-width: 2;
      transition: all 0.3s ease;
    }
    .thread-card {
      fill: #ffffff;
      stroke: #cbd5e1;
      stroke-width: 1.5;
      transition: all 0.3s ease;
    }
    .thread-card.active {
      stroke: #0284c7;
      stroke-width: 2.5;
      fill: #f0f9ff;
    }
    .thread-card.blocked {
      stroke: #d97706;
      stroke-width: 2;
      fill: #fef3c7;
    }
    .stack-segment {
      fill: #e2e8f0;
      stroke: #94a3b8;
      stroke-width: 1.5;
      transition: all 0.3s ease;
    }
    .stack-segment.active {
      fill: #bae6fd;
      stroke: #0284c7;
      stroke-width: 2;
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="02-process-lifecycle.html">&larr; Previous: 02. Process Lifecycle</a>
      <a href="index.html">&#127968; Week 2 Index</a>
      <a href="04-thread-implementation.html">Next: 04. Implementation &rarr;</a>
    </nav>

    <h2>03. The Classical Thread Model</h2>
    <p>
      In traditional operating system designs, every process possesses a single thread of control executing in an isolated address space. While this model provides robust memory protection, modern software architectures frequently require multiple parallel streams of execution collaborating within the exact same dataset.
    </p>
    <p>
      The <strong>thread abstraction</strong> decomposes the traditional heavyweight process into two distinct responsibilities: <strong>resource grouping</strong> and <strong>execution scheduling</strong>.
    </p>

    <h3>1. Why Threads: Motivation and Utility</h3>
    <p>
      Before the emergence of multithreading, concurrent applications relied entirely on multi-process architectures (such as calling <code>fork()</code>). While robust, multi-process concurrency imposes substantial performance bottlenecks:
    </p>
    <ul>
      <li>
        <strong>Shared Memory Access:</strong> Independent processes inhabit isolated virtual address spaces. Sharing data requires explicit inter-process communication (IPC)—such as pipes, message queues, sockets, or shared memory segments requiring complex synchronization. Threads inherently share the same address space, allowing pointers, buffers, and global variables to be accessed directly without serialization.
      </li>
      <li>
        <strong>Creation and Teardown Economy:</strong> Creating a new process requires allocating a new page directory root, duplicating page tables via Copy-on-Write, and building file descriptor tables. Threads require only an execution stack and a lightweight Thread Control Block (TCB). Thread creation is routinely 10 to 100 times faster than process creation.
      </li>
      <li>
        <strong>Context-Switch Overhead:</strong> Switching between processes requires invalidating or switching the Memory Management Unit (MMU) page table pointer (e.g., register <code>CR3</code> on x86-64), which forces a complete or partial flush of the Translation Lookaside Buffer (TLB). Switching between threads in the same process retains the exact same address space mappings, completely avoiding TLB flushes and cache misses.
      </li>
      <li>
        <strong>Overlapping Computation with Blocking I/O:</strong> On a single CPU core, while one thread is blocked waiting for network packets or disk blocks, another thread within the same process can actively perform arithmetic calculations or render a user interface, preventing the entire application from freezing.
      </li>
      <li>
        <strong>True Multi-Core Parallelism:</strong> On multicore processors, multiple threads of a single application run concurrently across distinct physical CPU cores, delivering near-linear throughput scaling for compute-bound algorithms.
      </li>
    </ul>

    <h3>2. Resource Grouping vs. Execution</h3>
    <p>
      The classical thread model cleanly separates what a program <em>owns</em> from what a program <em>executes</em>:
    </p>
    <ul>
      <li>
        <strong>The Process (Resource Grouping Container):</strong> The process serves as the static resource grouping entity. It owns a private virtual address space (containing text, data, and heap segments), open file descriptors, child process linkages, signal action dispositions, network socket handles, and accounting quotas.
      </li>
      <li>
        <strong>The Thread (Unit of Execution Scheduling):</strong> The thread serves as the lightweight entity scheduled for execution on a CPU core. Each thread possesses its own distinct Program Counter (PC), hardware register set, private stack, and scheduling state (Running, Ready, or Blocked).
      </li>
    </ul>

    <div style="overflow-x: auto; margin: 20px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 14px; width: 50%;">Per-Process Resources (Shared by All Threads)</th>
            <th style="padding: 10px 14px; width: 50%;">Per-Thread Items (Private to Each Thread)</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px;">Virtual Address Space (Text, Initialized Data, BSS)</td>
            <td style="padding: 10px 14px; font-weight: 600; color: #0284c7;">Program Counter (PC / RIP)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px;">Dynamic Memory Heap (Allocated via <code>malloc</code> / <code>brk</code>)</td>
            <td style="padding: 10px 14px; font-weight: 600; color: #0284c7;">CPU Register Set (RAX, RBX, RCX, etc.)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px;">Open File Descriptors (STDIN, STDOUT, Network Sockets)</td>
            <td style="padding: 10px 14px; font-weight: 600; color: #0284c7;">Private Execution Stack (Local activation frames)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px;">Child Processes &amp; Session Group ID</td>
            <td style="padding: 10px 14px; font-weight: 600; color: #0284c7;">Stack Pointer (RSP) &amp; Base Pointer (RBP)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px;">Signal Handlers &amp; Dispositions</td>
            <td style="padding: 10px 14px; font-weight: 600; color: #0284c7;">Thread Execution State (Running, Ready, Blocked)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px;">User and Group Identification (UID, GID, Capabilities)</td>
            <td style="padding: 10px 14px; font-weight: 600; color: #0284c7;">Thread-Specific Data (Thread-Local Storage / TLS)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Directed Narrative Stepper Standard: Classical Thread Model -->
    <div class="aid-wrapper">
      <div class="aid-header">
        <h4>Interactive Stepper: Multithreaded Execution in a Shared Address Space</h4>
        <div class="dimension-toggles">
          <button class="dim-btn active" id="dim-threads" onclick="setThreadDim('threads')">Multithreaded Architecture</button>
          <button class="dim-btn" id="dim-processes" onclick="setThreadDim('processes')">Multiprocess (fork) Model</button>
        </div>
      </div>

      <div class="scenario-banner">
        <span class="scenario-tag">Scenario Arc</span>
        <span id="thread-scenario-text">A multi-threaded Web Server (PID 2040) handles an incoming HTTP connection: Dispatcher (TID 1) receives the socket and hands it to Worker (TID 2), while Background Flusher (TID 3) syncs logs.</span>
      </div>

      <div class="telemetry-strip">
        <div class="telemetry-cell">
          <span class="telemetry-label">Active Entity</span>
          <span class="telemetry-val highlight" id="t-telem-entity">Thread 1: Dispatcher (TID 1)</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Virtual Address Space</span>
          <span class="telemetry-val" id="t-telem-vm">Shared: PID 2040 (CR3 Unchanged)</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Active Stack Frame</span>
          <span class="telemetry-val" id="t-telem-stack">Stack 1 (0x7FFF00 - 0x7FFE00)</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Memory Protection</span>
          <span class="telemetry-val" id="t-telem-prot">Shared Heap &amp; Global Buffers</span>
        </div>
      </div>

      <div class="canvas-container">
        <svg class="thread-canvas" viewBox="0 0 720 250">
          <!-- Shared Process Container -->
          <rect class="mem-block" x="20" y="20" width="680" height="210" rx="8" />
          <text id="container-title" x="40" y="44" font-family="system-ui" font-size="13" font-weight="700" fill="#0f172a">PROCESS CONTAINER (PID 2040: WebServer)</text>
          <text id="container-sub" x="40" y="62" font-family="var(--font-mono)" font-size="11" fill="#64748b">Shared Resources: Code Segment | Global Variables | Dynamic Heap | Open Sockets (FD 3, 4)</text>

          <!-- Shared Heap & Code Box -->
          <rect x="40" y="75" width="220" height="135" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
          <text x="55" y="98" font-family="system-ui" font-size="12" font-weight="700" fill="#0284c7">SHARED MEMORY</text>
          <rect x="55" y="110" width="190" height="26" rx="4" fill="#f1f5f9" stroke="#e2e8f0"/>
          <text x="65" y="127" font-family="var(--font-mono)" font-size="10" fill="#334155">Text: Compiled Server Code</text>
          <rect x="55" y="142" width="190" height="26" rx="4" fill="#f1f5f9" stroke="#e2e8f0"/>
          <text x="65" y="159" font-family="var(--font-mono)" font-size="10" fill="#334155">Heap: Dynamic Buffer Cache</text>
          <rect x="55" y="174" width="190" height="26" rx="4" fill="#f1f5f9" stroke="#e2e8f0"/>
          <text x="65" y="191" font-family="var(--font-mono)" font-size="10" fill="#334155">Globals: Server Connection Pool</text>

          <!-- Thread 1 Card -->
          <g id="card-t1" class="thread-group" transform="translate(280, 75)">
            <rect class="thread-card active" width="130" height="135" rx="6" />
            <text x="15" y="24" font-family="system-ui" font-size="11" font-weight="700" fill="#0f172a">THREAD 1</text>
            <text id="t1-role" x="15" y="40" font-family="var(--font-mono)" font-size="10" fill="#0284c7">Role: Dispatcher</text>
            <text id="t1-state" x="15" y="56" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#059669">State: RUNNING</text>
            <rect class="stack-segment active" x="12" y="70" width="106" height="52" rx="4"/>
            <text x="20" y="90" font-family="var(--font-mono)" font-size="9" fill="#0369a1">Stack Frame 1</text>
            <text id="t1-sp" x="20" y="106" font-family="var(--font-mono)" font-size="9" fill="#0369a1">RSP: 0x7FFE00</text>
          </g>

          <!-- Thread 2 Card -->
          <g id="card-t2" class="thread-group" transform="translate(425, 75)">
            <rect class="thread-card" width="130" height="135" rx="6" />
            <text x="15" y="24" font-family="system-ui" font-size="11" font-weight="700" fill="#0f172a">THREAD 2</text>
            <text id="t2-role" x="15" y="40" font-family="var(--font-mono)" font-size="10" fill="#64748b">Role: Worker</text>
            <text id="t2-state" x="15" y="56" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#d97706">State: READY</text>
            <rect class="stack-segment" x="12" y="70" width="106" height="52" rx="4"/>
            <text x="20" y="90" font-family="var(--font-mono)" font-size="9" fill="#475569">Stack Frame 2</text>
            <text id="t2-sp" x="20" y="106" font-family="var(--font-mono)" font-size="9" fill="#475569">RSP: 0x7FCE00</text>
          </g>

          <!-- Thread 3 Card -->
          <g id="card-t3" class="thread-group" transform="translate(570, 75)">
            <rect class="thread-card" width="115" height="135" rx="6" />
            <text x="12" y="24" font-family="system-ui" font-size="11" font-weight="700" fill="#0f172a">THREAD 3</text>
            <text id="t3-role" x="12" y="40" font-family="var(--font-mono)" font-size="10" fill="#64748b">Role: Flusher</text>
            <text id="t3-state" x="12" y="56" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#64748b">State: BLOCKED</text>
            <rect class="stack-segment" x="10" y="70" width="95" height="52" rx="4"/>
            <text x="16" y="90" font-family="var(--font-mono)" font-size="9" fill="#475569">Stack Frame 3</text>
            <text id="t3-sp" x="16" y="106" font-family="var(--font-mono)" font-size="9" fill="#475569">RSP: 0x7FAE00</text>
          </g>
        </svg>
      </div>

      <!-- Stepper Controls & Current Step Summary Panel -->
      <div class="controls-narrative-strip">
        <div class="stepper-btn-group">
          <button class="btn-step" id="t-btn-prev" onclick="stepThread(-1)" disabled>&larr; Previous</button>
          <button class="btn-step" id="t-btn-next" onclick="stepThread(1)">Next Step &rarr;</button>
          <button class="btn-step" id="t-btn-reset" onclick="resetThread()">Reset</button>
        </div>
        <div class="narrative-preview-panel">
          <strong>Current Step Summary</strong>
          <span id="t-txt-narrative">Thread 1 (Dispatcher) executes in user mode on the CPU, listening on port 80. The step aims to accept incoming network connections without delaying background threads.</span>
        </div>
      </div>

      <div class="analytical-grid">
        <div class="pane-card">
          <div class="pane-title what">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            What Is Happening
          </div>
          <p class="pane-content" id="t-txt-what">Thread 1 (Dispatcher) executes the network polling loop using its private stack frame. Thread 2 sits in the Ready queue waiting for request assignments.</p>
        </div>
        <div class="pane-card">
          <div class="pane-title why">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
            Why The System Does This
          </div>
          <p class="pane-content" id="t-txt-why">Dedication of a separate dispatcher thread ensures the server immediately accepts new TCP handshakes, maintaining high connection responsiveness under load.</p>
        </div>
      </div>
    </div>

    <h3>3. Thread Usage in Applications</h3>
    <p>
      The genuine architectural value of multithreading becomes evident when examining systems that balance real-time user responsiveness with computationally demanding or blocking background operations. Without threads, software developers are forced to invent convoluted asynchronous callback loops or incur the steep overhead of multi-process architectures.
    </p>

    <h4>1. Interactive Desktop Applications: The Collaborative Word Processor</h4>
    <p>
      Consider an interactive desktop word processor managing a manuscript of several thousand pages with embedded vector diagrams and typographical styling. The software must accomplish three distinct operational tasks concurrently:
    </p>
    <ul>
      <li><strong>Task 1: Keystroke &amp; Pointer Interaction:</strong> Processing hardware keyboard input events, drawing the blinking text insertion caret, and rendering typed characters on the display canvas within a 16-millisecond frame deadline (60 frames per second).</li>
      <li><strong>Task 2: Continuous Paragraph &amp; Layout Reformatting:</strong> Whenever a user types a new sentence on page 20, the reflow of text may push lines down across all subsequent 980 pages, altering line breaks, hyphenation points, footnotes, and page numbers. On a modern CPU, recomputing the page layout of a massive document can consume hundreds of milliseconds of intense integer and floating-point computation.</li>
      <li><strong>Task 3: Periodic Disk Snapshot &amp; Autosave:</strong> Every two minutes, the entire document state must be committed to permanent non-volatile storage (SSD) to prevent data loss in the event of a power failure or system crash. Writing megabytes of formatted binary XML down through the virtual file system layer forces blocking disk I/O traps.</li>
    </ul>

    <h5>The Single-Threaded Failure Mode</h5>
    <p>
      If the word processor is constructed as a single-threaded process, its sole execution thread must execute an interleaved loop:
    </p>
    <pre>while (application_running) {
    check_keyboard_and_mouse_events();
    recalculate_entire_document_pagination();
    if (autosave_timer_expired) {
        write_document_to_disk_blocking(); /* Stalls for 50-200ms */
    }
}</pre>
    <p>
      Under this design, whenever the user types a single character that triggers page reformatting, the event processing loop stops dead. Keyboard input queues back up, characters appear on screen with jarring delays, and during autosave events, the entire window freezes, leading the operating system desktop manager to display an unresponsive "beach ball" or "not responding" banner.
    </p>

    <h5>The Multi-Process Failure Mode</h5>
    <p>
      Attempting to solve this using independent processes via <code>fork()</code> introduces severe IPC latency. While a child process could handle autosaving using Copy-on-Write snapshots, the background reformatting engine must continually read and modify the active document data structure (such as a gap buffer or piece table). Serializing large document graphs over IPC pipes or managing synchronized shared memory regions adds immense software complexity and cache thrashing.
    </p>

    <h5>The Three-Thread Solution</h5>
    <p>
      Organizing the application into three collaborative threads operating within a single shared address space resolves all constraints elegantly:
    </p>
    <ul>
      <li><strong>Thread 1 (Interactive Dispatcher):</strong> Bounded strictly to window event queues. It captures keystrokes, inserts characters into the in-memory document piece table, and renders glyphs to the framebuffer immediately. It never executes complex layout math or blocking disk system calls.</li>
      <li><strong>Thread 2 (Formatting Worker):</strong> Awakens whenever Thread 1 notifies a condition variable indicating that text has changed. It runs concurrently on a secondary CPU core, calculating line wraps, kerning, and pagination, updating page boundary pointers directly in the shared heap using reader-writer locks (<code>pthread_rwlock_t</code>).</li>
      <li><strong>Thread 3 (Disk Autosave Worker):</strong> Sleeps on a periodic timer barrier. Upon waking, it acquires a shared read-lock on the document buffer, writes the snapshot to the SSD via asynchronous file I/O, and returns to sleep. Even if the underlying NVMe storage controller experiences a momentary I/O queue stall, Thread 1 continues rendering keystrokes at native display refresh rates without a single dropped frame.</li>
    </ul>

    <h4>2. High-Performance Web Servers: Architectural Comparisons</h4>
    <p>
      Network server design represents the canonical engineering domain for concurrency paradigms. A production web server listening on TCP port 80 or 443 must process thousands of incoming HTTP requests concurrently, retrieve static files from disk or query memory caches, and transmit HTTP responses over varying network connection speeds.
    </p>
    <p>
      Operating systems support three primary architectural patterns for constructing web servers:
    </p>

    <h5>Model A: The Multi-Threaded Worker Pool Architecture</h5>
    <p>
      In a classical multi-threaded server (such as Apache HTTP Server with the <code>worker</code> or <code>event</code> MPM), the process instantiates an initial pool of worker threads during startup. A dedicated master <strong>dispatcher thread</strong> executes a blocking <code>accept()</code> system call on the listening socket:
    </p>
    <ol>
      <li>When a client TCP connection arrives, <code>accept()</code> returns a new connected socket file descriptor.</li>
      <li>The dispatcher thread places the client socket descriptor into an in-memory job queue residing in the shared heap and signals a condition variable (<code>pthread_cond_signal</code>).</li>
      <li>An idle worker thread in the pool unblocks, dequeues the socket descriptor, parses the HTTP request headers, issues a blocking disk read (or cache lookup) for the requested resource, writes the HTTP response body over the network socket, and closes the connection.</li>
      <li>The worker thread returns itself to the idle pool to await another client.</li>
    </ol>
    <p>
      <strong>Key Advantage:</strong> The programming model is straightforward and sequential. A worker thread can invoke standard blocking I/O calls (such as <code>read()</code> and <code>write()</code>) because a block on one thread does not stall the execution of competing threads in the pool.
    </p>
    <p>
      <strong>Key Limitation:</strong> Thread scalability is constrained by per-thread memory footprint. If each thread requires an 8MB virtual stack, running 50,000 concurrent threads would consume 400GB of virtual address space. Furthermore, scheduling tens of thousands of active threads incurs severe CPU cache degradation and kernel runqueue lock contention.
    </p>

    <h5>Model B: The Single-Threaded Event-Driven State Machine (Reactor Pattern)</h5>
    <p>
      To circumvent the thread stack and context-switch limits (the classic <em>C10K problem</em>), servers like NGINX and Node.js implement a single-threaded, event-driven architecture based on the Reactor design pattern.
    </p>
    <p>
      In this model, a single thread executes an infinite event loop driving an operating system <strong>I/O multiplexing mechanism</strong> (such as <code>epoll</code> on Linux, <code>kqueue</code> on FreeBSD/macOS, or IOCP on Windows):
    </p>
    <ol>
      <li>All client network sockets are marked as <strong>non-blocking</strong> (via <code>fcntl(fd, F_SETFL, O_NONBLOCK)</code>).</li>
      <li>The server registers thousands of open sockets with an <code>epoll</code> descriptor and enters a dormant state inside <code>epoll_wait()</code>.</li>
      <li>When the network interface card (NIC) receives packets, the kernel wakes the event loop, returning a batch list of file descriptors that are ready for immediate read or write operations.</li>
      <li>The single thread executes a non-blocking state machine for each active descriptor: reading available bytes into a buffer, updating the protocol state, and returning immediately without ever sleeping on I/O.</li>
    </ol>
    <p>
      <strong>Key Advantage:</strong> Zero context-switching overhead, zero synchronization locks, and minuscule memory consumption per connection (often less than 4KB for connection state buffers). A single core can sustain 100,000+ concurrent idle connections.
    </p>
    <p>
      <strong>The Fatal Vulnerability:</strong> <em>Any compute-heavy operation or unbuffered disk operation destroys the server.</em> Because there is only one thread of execution, if a request triggers a complex mathematical calculation, an image resize, or a page fault that stalls on disk retrieval, the entire event loop halts. Thousands of other active client connections freeze instantly until that single thread resumes spinning.
    </p>

    <h5>Model C: The Multi-Process Architecture (Historical Precursor)</h5>
    <p>
      Historically utilized by classic Apache 1.3 (<code>prefork</code> MPM), the server forks an independent child process for each connected client:
    </p>
    <p>
      <strong>Key Advantage:</strong> Total hardware fault isolation. If a worker process contains a memory leak, corrupts its heap, or encounters a fatal segmentation fault (<code>SIGSEGV</code>) caused by a malicious exploit payload, only that isolated process crashes. The master daemon and all other client connections continue executing unharmed.
    </p>
    <p>
      <strong>Key Limitation:</strong> Heavy memory waste, slow process creation latency, and inability to share dynamic caches directly without constructing complex shared memory arenas.
    </p>

    <h4>Comparative Matrix of Server Concurrency Architectures</h4>
    <div style="overflow-x: auto; margin: 20px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 14px;">Architecture Model</th>
            <th style="padding: 10px 14px;">Concurrency Primitive</th>
            <th style="padding: 10px 14px;">Memory Footprint per Connection</th>
            <th style="padding: 10px 14px;">CPU Scheduling Overhead</th>
            <th style="padding: 10px 14px;">Blocking I/O Vulnerability</th>
            <th style="padding: 10px 14px;">Failure Blast Radius</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;">Multi-Threaded Pool</td>
            <td style="padding: 10px 14px;">Kernel Threads (Pthreads)</td>
            <td style="padding: 10px 14px; color: var(--warning); font-weight: 600;">Moderate (Stack: 2MB&ndash;8MB)</td>
            <td style="padding: 10px 14px;">Moderate (Kernel thread switches, warm TLB)</td>
            <td style="padding: 10px 14px; color: var(--success); font-weight: 600;">Low (Only the calling thread blocks)</td>
            <td style="padding: 10px 14px; color: var(--danger); font-weight: 600;">High (Crash kills entire shared process)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;">Event-Driven Reactor</td>
            <td style="padding: 10px 14px;">Single Thread + <code>epoll</code></td>
            <td style="padding: 10px 14px; color: var(--success); font-weight: 600;">Minimal (Connection state: ~4KB)</td>
            <td style="padding: 10px 14px; color: var(--success); font-weight: 600;">Minimal (Zero thread context switches)</td>
            <td style="padding: 10px 14px; color: var(--danger); font-weight: 600;">Severe (One block stalls all connections)</td>
            <td style="padding: 10px 14px; color: var(--danger); font-weight: 600;">High (Crash terminates the entire event loop)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 600;">Multi-Process Model</td>
            <td style="padding: 10px 14px;">Forked Processes (<code>fork</code>)</td>
            <td style="padding: 10px 14px; color: var(--danger); font-weight: 600;">Heavy (Full page tables &amp; address space)</td>
            <td style="padding: 10px 14px; color: var(--danger); font-weight: 600;">High (Full TLB flushes &amp; cache misses)</td>
            <td style="padding: 10px 14px; color: var(--success); font-weight: 600;">Low (Only the calling process blocks)</td>
            <td style="padding: 10px 14px; color: var(--success); font-weight: 600;">Minimal (Isolated; other processes survive)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h4>3. Asynchronous Data Processing &amp; Pipeline Streaming</h4>
    <p>
      In high-throughput distributed systems, real-time analytics engines, and machine learning pipelines, multithreading organizes sequential computational tasks into <strong>pipelined stages</strong> connected by lock-free circular ring buffers:
    </p>
    <ul>
      <li><strong>Ingress Producer Thread:</strong> Polls incoming high-speed network interfaces (e.g., streaming market data feeds or raw camera frames) and writes unparsed binary buffers into a pre-allocated shared memory ring buffer.</li>
      <li><strong>Transformation Worker Threads:</strong> A pool of parallel computational worker threads reads raw frames, decrypts or decompresses payloads, runs tensor inference or analytical filtering across multiple CPU cores, and stores formatted results in an egress queue.</li>
      <li><strong>Telemetry &amp; Health Monitor Thread:</strong> Operates at low priority on a distinct scheduler timer, periodically verifying thread health, emitting heartbeat pings to orchestrators (like Kubernetes), and recording latency histograms without interrupting ingress packet flows.</li>
    </ul>

    <h3>4. Private Stacks and Thread-Local Storage</h3>
    <p>
      While all threads share the process heap, global data, and open file descriptors, <em>each thread must possess its own independent execution stack</em>:
    </p>
    <ul>
      <li><strong>Separate Function Call Frames:</strong> Each thread executes different functions at different times. Thread 1 might be three levels deep in a string parsing function, while Thread 2 is calling a database library. Each stack stores return addresses, CPU frame pointers, and automatic local variables.</li>
      <li><strong>Stack Placement in Virtual Memory:</strong> When a thread is created (e.g., via <code>pthread_create</code>), the thread runtime allocates a distinct memory region (typically 2MB to 8MB) within the shared address space to serve as that thread's stack.</li>
      <li><strong>Stack Guard Pages:</strong> To prevent a thread stack from overflowing into an adjacent thread's memory, modern operating systems place an unmapped, read/write-protected <strong>guard page</strong> directly between consecutive thread stacks. Any stack overflow triggers a hardware page fault (<code>#PF</code>), terminating the faulty thread immediately.</li>
      <li><strong>Thread-Local Storage (TLS):</strong> In addition to the stack, programming languages provide thread-local variables (e.g., <code>__thread</code> in C or <code>thread_local</code> in C++). Each thread receives its own unique instance of the variable, accessible via a specialized segment register (such as <code>FS</code> on x86-64).</li>
    </ul>

    <nav class="nav-bar" style="margin-top: 36px; border-bottom: none; border-top: 1px solid var(--border); padding-top: 16px;">
      <a href="02-process-lifecycle.html">&larr; Previous: 02. Process Lifecycle</a>
      <a href="index.html">&#127968; Week 2 Index</a>
      <a href="04-thread-implementation.html">Next: 04. Implementation &rarr;</a>
    </nav>
  </div>

  <script>
    const threadSteps = {
      threads: [
        {
          entity: "Thread 1: Dispatcher (TID 1)",
          vm: "Shared: PID 2040 (CR3 Unchanged)",
          stack: "Stack 1 (0x7FFF00 - 0x7FFE00)",
          prot: "Shared Heap & Global Buffers",
          t1State: "State: RUNNING",
          t2State: "State: READY",
          t3State: "State: BLOCKED",
          t1Color: "#059669",
          t2Color: "#d97706",
          t3Color: "#64748b",
          activeCard: "card-t1",
          narrative: "Thread 1 (Dispatcher) executes in user mode on the CPU, listening on port 80. The step aims to accept incoming network connections without delaying background threads.",
          what: "Thread 1 (Dispatcher) executes the network polling loop using its private stack frame. Thread 2 sits in the Ready queue waiting for request assignments.",
          why: "Dedication of a separate dispatcher thread ensures the server immediately accepts new TCP handshakes, maintaining high connection responsiveness under load."
        },
        {
          entity: "Thread 1 -> Shared Queue Hand-off",
          vm: "Shared: PID 2040 (Zero Memory Copy)",
          stack: "Queue Pointer Passed via Heap",
          prot: "Direct Pointer Dereference",
          t1State: "State: RUNNING",
          t2State: "State: AWAKENING",
          t3State: "State: BLOCKED",
          t1Color: "#059669",
          t2Color: "#0284c7",
          t3Color: "#64748b",
          activeCard: "card-t1",
          narrative: "Dispatcher receives an HTTP GET request, allocates a request struct on the shared heap, and signals Worker Thread 2. The step aims to pass work using direct memory pointers without expensive inter-process data copying.",
          what: "Thread 1 places the socket file descriptor directly into a shared job queue on the heap and signals a condition variable.",
          why: "Because all threads share the same address space, communication requires only passing 8-byte memory pointers, eliminating serialization and pipe buffering overhead."
        },
        {
          entity: "Thread 2: Worker Execution (TID 2)",
          vm: "Shared: PID 2040 (CR3 Retained)",
          stack: "Stack 2 (0x7FCE00 - 0x7FCD00)",
          prot: "Cache-Warm TLB Retained",
          t1State: "State: READY",
          t2State: "State: RUNNING",
          t3State: "State: BLOCKED",
          t1Color: "#d97706",
          t2Color: "#059669",
          t3Color: "#64748b",
          activeCard: "card-t2",
          narrative: "The scheduler switches execution to Thread 2. Because Thread 2 inhabits the same process, the hardware page table register (CR3) remains unchanged and TLB caches stay warm. The step aims to execute worker logic with near-zero switching cost.",
          what: "The kernel restores Thread 2's registers and Stack Pointer (RSP). The CPU executes Worker instructions using Stack 2.",
          why: "Thread context switching requires only saving and restoring integer registers, completely avoiding the Translation Lookaside Buffer (TLB) flushes mandatory during process switches."
        },
        {
          entity: "Thread 3: Background Flusher (TID 3)",
          vm: "Shared: PID 2040 (Async I/O)",
          stack: "Stack 3 (0x7FAE00 - 0x7FAD00)",
          prot: "Non-Interfering Background Run",
          t1State: "State: RUNNING",
          t2State: "State: READY",
          t3State: "State: RUNNING (Core 1)",
          t1Color: "#059669",
          t2Color: "#d97706",
          t3Color: "#059669",
          activeCard: "card-t3",
          narrative: "Thread 3 wakes up on Core 1 to flush access logs to disk, while Thread 1 simultaneously accepts another request on Core 0. The step aims to achieve true multi-core parallel execution across distinct execution contexts.",
          what: "Thread 3 executes disk write operations on a secondary CPU core while the Dispatcher continues listening on the primary core.",
          why: "Multithreading enables true symmetric multiprocessing (SMP): multiple execution streams run simultaneously on separate silicon cores."
        }
      ],
      processes: [
        {
          entity: "Process 1 (Parent Master: PID 2040)",
          vm: "Private: CR3 Root 0x1A000",
          stack: "Isolated Stack Frame",
          prot: "Hardware MMU Boundary Enforced",
          t1State: "State: RUNNING",
          t2State: "State: UNSPAWNED",
          t3State: "State: UNSPAWNED",
          t1Color: "#059669",
          t2Color: "#94a3b8",
          t3Color: "#94a3b8",
          activeCard: "card-t1",
          narrative: "In a multi-process architecture, the parent process runs in an isolated virtual address space. The step aims to accept connections while preparing to call fork() to instantiate completely separate memory spaces.",
          what: "Master process listens on socket. It cannot share heap buffers directly with other tasks without configuring shared memory segments.",
          why: "Processes prioritize strong memory isolation over low-overhead collaboration, ensuring bugs in one task cannot corrupt others."
        },
        {
          entity: "fork() Invocation -> Memory Cloning",
          vm: "Cloned Address Space: PID 2041",
          stack: "Duplicate Stack Allocated",
          prot: "Copy-on-Write Page Tables",
          t1State: "State: FORKING",
          t2State: "State: FORKED (PID 2041)",
          t3State: "State: UNSPAWNED",
          t1Color: "#0284c7",
          t2Color: "#d97706",
          t3Color: "#94a3b8",
          activeCard: "card-t2",
          narrative: "The master calls fork() to create child process 2041. The kernel allocates a new page directory root, duplicates page tables, and marks physical memory as Copy-on-Write. The step aims to establish process isolation at the cost of memory structures.",
          what: "The kernel builds a new PCB, clones file descriptor tables, and sets up duplicate virtual memory mappings.",
          why: "Memory isolation guarantees that if a worker process crashes on a malicious HTTP payload, the master process continues operating unharmed."
        },
        {
          entity: "IPC Data Serialization via Pipe",
          vm: "Isolated: Separate CR3 Roots",
          stack: "Separate Independent Stacks",
          prot: "Kernel Buffer Copy Required",
          t1State: "State: WRITING PIPE",
          t2State: "State: READING PIPE",
          t3State: "State: UNSPAWNED",
          t1Color: "#0284c7",
          t2Color: "#059669",
          t3Color: "#94a3b8",
          activeCard: "card-t2",
          narrative: "To pass the client request to Child 2041, the master must write bytes through an IPC pipe. The kernel copies data from user space into a kernel buffer, switches CR3, and copies data into Child 2041. The step illustrates the data transfer tax of process isolation.",
          what: "Data must be copied through the kernel boundary via system calls, incurring memory bus traffic and CPU cache pollution.",
          why: "Because memory is strictly isolated, processes cannot directly read each other's memory pointers."
        },
        {
          entity: "Process Context Switch (TLB Flushed)",
          vm: "CR3 Swapped: 0x1A000 -> 0x2B000",
          stack: "Swapped Kernel Stacks",
          prot: "Complete TLB Eviction",
          t1State: "State: READY",
          t2State: "State: RUNNING",
          t3State: "State: UNSPAWNED",
          t1Color: "#d97706",
          t2Color: "#059669",
          t3Color: "#94a3b8",
          activeCard: "card-t2",
          narrative: "Switching execution between Parent 2040 and Child 2041 requires swapping CR3, flushing the Translation Lookaside Buffer (TLB), and repopulating CPU hardware caches. The step demonstrates the heavy overhead of multi-process scheduling.",
          what: "The CPU flushes its address translation cache, reloads page tables, and incurs cache misses on subsequent instructions.",
          why: "MMU page table roots must be updated to prevent process 2041 from accessing the physical memory pages of process 2040."
        }
      ]
    };

    let activeThreadDim = "threads";
    let activeThreadStep = 0;

    function renderThreadStepper() {
      const steps = threadSteps[activeThreadDim];
      const step = steps[activeThreadStep];

      // Update Live Telemetry
      document.getElementById("t-telem-entity").textContent = step.entity;
      document.getElementById("t-telem-vm").textContent = step.vm;
      document.getElementById("t-telem-stack").textContent = step.stack;
      document.getElementById("t-telem-prot").textContent = step.prot;

      // Update Thread States and Colors
      document.getElementById("t1-state").textContent = step.t1State;
      document.getElementById("t1-state").setAttribute("fill", step.t1Color);
      document.getElementById("t2-state").textContent = step.t2State;
      document.getElementById("t2-state").setAttribute("fill", step.t2Color);
      document.getElementById("t3-state").textContent = step.t3State;
      document.getElementById("t3-state").setAttribute("fill", step.t3Color);

      // Update Active Card Visual Highlights
      ["card-t1", "card-t2", "card-t3"].forEach(id => {
        const card = document.getElementById(id);
        const rect = card.querySelector(".thread-card");
        const stack = card.querySelector(".stack-segment");
        if (id === step.activeCard) {
          rect.classList.add("active");
          stack.classList.add("active");
        } else {
          rect.classList.remove("active");
          stack.classList.remove("active");
        }
      });

      // Update Dedicated Narrative Summary Panel
      document.getElementById("t-txt-narrative").textContent = step.narrative;
      document.getElementById("t-btn-prev").disabled = (activeThreadStep === 0);
      document.getElementById("t-btn-next").disabled = (activeThreadStep === steps.length - 1);

      // Update Analytical Panes
      document.getElementById("t-txt-what").textContent = step.what;
      document.getElementById("t-txt-why").textContent = step.why;
    }

    function stepThread(delta) {
      const steps = threadSteps[activeThreadDim];
      activeThreadStep = Math.max(0, Math.min(steps.length - 1, activeThreadStep + delta));
      renderThreadStepper();
    }

    function resetThread() {
      activeThreadStep = 0;
      renderThreadStepper();
    }

    function setThreadDim(dim) {
      activeThreadDim = dim;
      activeThreadStep = 0;
      document.getElementById("dim-threads").classList.toggle("active", dim === "threads");
      document.getElementById("dim-processes").classList.toggle("active", dim === "processes");

      const isThread = dim === "threads";
      document.getElementById("container-title").textContent = isThread
        ? "PROCESS CONTAINER (PID 2040: WebServer)"
        : "ISOLATED PROCESS MODEL (Parent PID 2040 / Child PID 2041)";
      document.getElementById("container-sub").textContent = isThread
        ? "Shared Resources: Code Segment | Global Variables | Dynamic Heap | Open Sockets (FD 3, 4)"
        : "Isolated Resources: Separate Address Spaces | Independent Heaps | IPC via Kernel Buffers";

      document.getElementById("t1-role").textContent = isThread ? "Role: Dispatcher" : "Role: Master";
      document.getElementById("t2-role").textContent = isThread ? "Role: Worker" : "Role: Child 2041";
      document.getElementById("t3-role").textContent = isThread ? "Role: Flusher" : "Role: Unused";

      const scenarioText = isThread
        ? "A multi-threaded Web Server (PID 2040) handles an incoming HTTP connection: Dispatcher (TID 1) receives the socket and hands it to Worker (TID 2), while Background Flusher (TID 3) syncs logs."
        : "A multi-process Web Server handles an HTTP connection by calling fork() to create Child 2041, transferring socket descriptors via IPC, and incurring TLB flush context switches.";
      document.getElementById("thread-scenario-text").innerHTML = scenarioText;

      renderThreadStepper();
    }

    document.addEventListener("DOMContentLoaded", () => {
      renderThreadStepper();
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
            "Expand thread usage patterns and server architectures in Module 03\n\n"
            "Provide deep analysis of word processor concurrency, comparative web server\n"
            "architectures (worker pools vs event-driven state machines), and pipelines."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    execute_expansion()
