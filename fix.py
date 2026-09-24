#!/usr/bin/env python3
# =====================================================================
# fix.py: Standardize index hubs for Weeks 5 through 12
# =====================================================================
import os
import subprocess

HUBS = {
    os.path.join("week05-io-and-disk-scheduling", "index.html"): r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 5: I/O Systems &amp; Disk Scheduling | COSC240</title>
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
      padding: 40px 16px;
      line-height: 1.6;
    }
    .container {
      max-width: 980px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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
    h1 {
      font-size: 1.85rem;
      color: #0f172a;
      margin: 0 0 6px 0;
    }
    .subtitle {
      font-size: 0.95rem;
      color: var(--text-muted);
      margin: 0 0 24px 0;
    }
    .lead-card {
      background: #f0f9ff;
      border-left: 4px solid var(--accent);
      padding: 16px 20px;
      border-radius: 0 6px 6px 0;
      margin-bottom: 32px;
      font-size: 0.92rem;
      color: #0369a1;
    }
    .lead-card strong { color: #0f172a; }

    .module-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }
    .module-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .module-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 12px rgba(0,0,0,0.06);
    }
    .module-num {
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
    }
    .module-title {
      font-size: 1.12rem;
      font-weight: 700;
      color: #0f172a;
      margin: 0 0 8px 0;
      line-height: 1.35;
    }
    .module-desc {
      font-size: 0.86rem;
      color: var(--text-muted);
      margin: 0 0 16px 0;
      line-height: 1.5;
      flex-grow: 1;
    }
    .btn-module {
      display: block;
      text-align: center;
      padding: 8px 14px;
      background: #f1f5f9;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #0f172a;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.84rem;
      transition: all 0.15s ease;
    }
    .btn-module:hover {
      background: #0f172a;
      color: #ffffff;
      border-color: #0f172a;
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="../index.html">&#127968; Course Index</a>
      <a href="../week04-concurrency-and-mutual-exclusion/index.html">&larr; Week 4 Hub</a>
      <span style="font-size: 0.85rem; font-weight: 700; color: #64748b;">Week 5: I/O &amp; Disks</span>
      <a href="../week06-synchronisation-and-deadlock/index.html">Next: Week 6 Hub &rarr;</a>
    </nav>

    <h1>Week 5: I/O Systems &amp; Disk Scheduling</h1>
    <p class="subtitle">Hardware Controllers, Interrupt Pipelines, Direct Memory Access, and Storage Geometry</p>

    <div class="lead-card">
      <strong>Core Conceptual Shift:</strong> While CPU cycles execute in nanoseconds, mechanical and peripheral devices operate in milliseconds. The operating system bridges this six-order-of-magnitude performance gap using asynchronous interrupt pipelines, Direct Memory Access (DMA) offloading, and physical seek-time optimization algorithms.
    </div>

    <div class="module-grid">
      <div class="module-card">
        <div>
          <div class="module-num">Module 01</div>
          <h2 class="module-title">I/O Hardware &amp; Device Controllers</h2>
          <p class="module-desc">
            Memory-mapped I/O vs. Port I/O, device registers (command, status, data), polling overhead, and controller architectures.
          </p>
        </div>
        <a href="placeholder.html" class="btn-module">Open Module 01 &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 02</div>
          <h2 class="module-title">Interrupts &amp; Direct Memory Access (DMA)</h2>
          <p class="module-desc">
            Interrupt handler top/bottom halves, programmable interrupt controllers (APIC), bus mastering, and cycle stealing in DMA engines.
          </p>
        </div>
        <a href="placeholder.html" class="btn-module">Open Module 02 &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 03</div>
          <h2 class="module-title">Disk Geometry &amp; Arm Scheduling</h2>
          <p class="module-desc">
            Platters, tracks, sectors, cylinder seek latency, rotational delay, and scheduling algorithms: FCFS, SSTF, SCAN (Elevator), and C-SCAN.
          </p>
        </div>
        <a href="placeholder.html" class="btn-module">Open Module 03 &rarr;</a>
      </div>
    </div>
  </div>
</body>
</html>
""",

    os.path.join("week06-synchronisation-and-deadlock", "index.html"): r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 6: Synchronization &amp; Deadlock | COSC240</title>
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
      padding: 40px 16px;
      line-height: 1.6;
    }
    .container {
      max-width: 980px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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
    h1 {
      font-size: 1.85rem;
      color: #0f172a;
      margin: 0 0 6px 0;
    }
    .subtitle {
      font-size: 0.95rem;
      color: var(--text-muted);
      margin: 0 0 24px 0;
    }
    .lead-card {
      background: #f0f9ff;
      border-left: 4px solid var(--accent);
      padding: 16px 20px;
      border-radius: 0 6px 6px 0;
      margin-bottom: 32px;
      font-size: 0.92rem;
      color: #0369a1;
    }
    .lead-card strong { color: #0f172a; }

    .module-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }
    .module-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .module-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 12px rgba(0,0,0,0.06);
    }
    .module-num {
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
    }
    .module-title {
      font-size: 1.12rem;
      font-weight: 700;
      color: #0f172a;
      margin: 0 0 8px 0;
      line-height: 1.35;
    }
    .module-desc {
      font-size: 0.86rem;
      color: var(--text-muted);
      margin: 0 0 16px 0;
      line-height: 1.5;
      flex-grow: 1;
    }
    .btn-module {
      display: block;
      text-align: center;
      padding: 8px 14px;
      background: #f1f5f9;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #0f172a;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.84rem;
      transition: all 0.15s ease;
    }
    .btn-module:hover {
      background: #0f172a;
      color: #ffffff;
      border-color: #0f172a;
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="../index.html">&#127968; Course Index</a>
      <a href="../week05-io-and-disk-scheduling/index.html">&larr; Week 5 Hub</a>
      <span style="font-size: 0.85rem; font-weight: 700; color: #64748b;">Week 6: Deadlock</span>
      <a href="../week09-memory-management/index.html">Next: Week 9 Hub &rarr;</a>
    </nav>

    <h1>Week 6: Synchronization &amp; Deadlock</h1>
    <p class="subtitle">Coffman Conditions, Resource Allocation Graphs, and Deadlock Prevention &amp; Detection</p>

    <div class="lead-card">
      <strong>Core Conceptual Shift:</strong> When concurrent threads lock multiple shared resources, circular dependencies can freeze the entire system permanently. Deadlock is not an accident of speed—it is a mathematical consequence of four simultaneous conditions that must be proactively broken through avoidance or detected and resolved.
    </div>

    <div class="module-grid">
      <div class="module-card">
        <div>
          <div class="module-num">Interactive Tool 01</div>
          <h2 class="module-title">Deadlock Detector &amp; RAG Simulator</h2>
          <p class="module-desc">
            Graph cycle detection algorithms (Tarjan/DFS), Resource Allocation Graphs (RAG), and tracing circular wait states interactively.
          </p>
        </div>
        <a href="deadlock-detector.html" class="btn-module">Launch Deadlock Detector &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Interactive Tool 02</div>
          <h2 class="module-title">Dining Philosophers Problem Sandbox</h2>
          <p class="module-desc">
            Dijkstra's classical synchronization challenge: asymmetric chopsticks, state arrays, and starvation-free resource acquisition.
          </p>
        </div>
        <a href="dining-philosophers.html" class="btn-module">Launch Philosophers Sandbox &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Interactive Tool 03</div>
          <h2 class="module-title">IPC Deadlock &amp; Mutex Analysis</h2>
          <p class="module-desc">
            Inter-process pipe buffer deadlocks, reciprocal lock ordering errors, and message queue blocking conditions.
          </p>
        </div>
        <a href="ipc-deadlock.html" class="btn-module">Launch IPC Deadlock Tool &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Interactive Tool 04</div>
          <h2 class="module-title">Database Two-Phase Locking Deadlock</h2>
          <p class="module-desc">
            Strict Two-Phase Locking (2PL), shared vs. exclusive row locks, serializability, and transaction rollback mechanics.
          </p>
        </div>
        <a href="database-deadlock.html" class="btn-module">Launch Database 2PL Tool &rarr;</a>
      </div>
    </div>
  </div>
</body>
</html>
""",

    os.path.join("week09-memory-management", "index.html"): r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 9: Memory Management &amp; Virtual Memory | COSC240</title>
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
      padding: 40px 16px;
      line-height: 1.6;
    }
    .container {
      max-width: 980px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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
    h1 {
      font-size: 1.85rem;
      color: #0f172a;
      margin: 0 0 6px 0;
    }
    .subtitle {
      font-size: 0.95rem;
      color: var(--text-muted);
      margin: 0 0 24px 0;
    }
    .lead-card {
      background: #f0f9ff;
      border-left: 4px solid var(--accent);
      padding: 16px 20px;
      border-radius: 0 6px 6px 0;
      margin-bottom: 32px;
      font-size: 0.92rem;
      color: #0369a1;
    }
    .lead-card strong { color: #0f172a; }

    .module-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }
    .module-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .module-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 12px rgba(0,0,0,0.06);
    }
    .module-num {
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
    }
    .module-title {
      font-size: 1.12rem;
      font-weight: 700;
      color: #0f172a;
      margin: 0 0 8px 0;
      line-height: 1.35;
    }
    .module-desc {
      font-size: 0.86rem;
      color: var(--text-muted);
      margin: 0 0 16px 0;
      line-height: 1.5;
      flex-grow: 1;
    }
    .btn-module {
      display: block;
      text-align: center;
      padding: 8px 14px;
      background: #f1f5f9;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #0f172a;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.84rem;
      transition: all 0.15s ease;
    }
    .btn-module:hover {
      background: #0f172a;
      color: #ffffff;
      border-color: #0f172a;
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="../index.html">&#127968; Course Index</a>
      <a href="../week06-synchronisation-and-deadlock/index.html">&larr; Week 6 Hub</a>
      <span style="font-size: 0.85rem; font-weight: 700; color: #64748b;">Week 9: Memory Management</span>
      <a href="../week10-file-management/index.html">Next: Week 10 Hub &rarr;</a>
    </nav>

    <h1>Week 9: Memory Management &amp; Virtual Memory</h1>
    <p class="subtitle">Physical Allocation, Address Translation, Paging Hardware, TLBs, and Page Replacement</p>

    <div class="lead-card">
      <strong>Core Conceptual Shift:</strong> Physical memory is finite, fragmented, and insecure if accessed directly. Virtual memory decouples program addresses from physical silicon via hardware MMU page tables, giving every process an isolated 64-bit address space while transparently paging data between RAM and storage.
    </div>

    <div class="module-grid">
      <div class="module-card">
        <div>
          <div class="module-num">Module 01</div>
          <h2 class="module-title">Buddy Allocator &amp; Free Lists</h2>
          <p class="module-desc">
            Binary buddy allocation trees, power-of-two block splitting, coalescing buddies, and internal vs. external fragmentation.
          </p>
        </div>
        <a href="buddy-allocator-tutorial.html" class="btn-module">Open Buddy Allocator &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 02</div>
          <h2 class="module-title">Page Table Entries (PTE) Sandbox</h2>
          <p class="module-desc">
            Hardware PTE bit anatomy: Present, R/W, User/Supervisor, Accessed, Dirty, and Page Frame Numbers (PFN).
          </p>
        </div>
        <a href="pte-sandbox.html" class="btn-module">Open PTE Sandbox &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 03</div>
          <h2 class="module-title">Translation Lookaside Buffer (TLB)</h2>
          <p class="module-desc">
            Hardware associative cache lookup, TLB hits vs. misses, multi-level hardware page table walkers, and shootdowns.
          </p>
        </div>
        <a href="tlb-sandbox.html" class="btn-module">Open TLB Sandbox &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 04</div>
          <h2 class="module-title">Page Fault Handling Pipeline</h2>
          <p class="module-desc">
            CR2 fault registers, trap vector dispatch, disk page fetch, frame allocation, and restarting faulting instructions.
          </p>
        </div>
        <a href="fault-tracer.html" class="btn-module">Open Fault Tracer &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 05</div>
          <h2 class="module-title">The Aging Replacement Algorithm</h2>
          <p class="module-desc">
            Simulating True LRU in hardware with R-bit shift registers, decay weightings, and Belady's Anomaly resistance.
          </p>
        </div>
        <a href="08-aging-algorithm.html" class="btn-module">Open Aging Algorithm &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 06</div>
          <h2 class="module-title">Working Set &amp; WSClock Algorithms</h2>
          <p class="module-desc">
            Peter Denning's working set model, thrashing prevention, time-of-last-use tracking, and the circular WSClock hand.
          </p>
        </div>
        <a href="wsclock.html" class="btn-module">Open WSClock Sandbox &rarr;</a>
      </div>
    </div>
  </div>
</body>
</html>
""",

    os.path.join("week10-file-management", "index.html"): r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 10: File Management | COSC240</title>
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
      padding: 40px 16px;
      line-height: 1.6;
    }
    .container {
      max-width: 980px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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
    h1 {
      font-size: 1.85rem;
      color: #0f172a;
      margin: 0 0 6px 0;
    }
    .subtitle {
      font-size: 0.95rem;
      color: var(--text-muted);
      margin: 0 0 24px 0;
    }
    .lead-card {
      background: #f0f9ff;
      border-left: 4px solid var(--accent);
      padding: 16px 20px;
      border-radius: 0 6px 6px 0;
      margin-bottom: 32px;
      font-size: 0.92rem;
      color: #0369a1;
    }
    .lead-card strong { color: #0f172a; }

    .module-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }
    .module-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .module-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 12px rgba(0,0,0,0.06);
    }
    .module-num {
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
    }
    .module-title {
      font-size: 1.12rem;
      font-weight: 700;
      color: #0f172a;
      margin: 0 0 8px 0;
      line-height: 1.35;
    }
    .module-desc {
      font-size: 0.86rem;
      color: var(--text-muted);
      margin: 0 0 16px 0;
      line-height: 1.5;
      flex-grow: 1;
    }
    .btn-module {
      display: block;
      text-align: center;
      padding: 8px 14px;
      background: #f1f5f9;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #0f172a;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.84rem;
      transition: all 0.15s ease;
    }
    .btn-module:hover {
      background: #0f172a;
      color: #ffffff;
      border-color: #0f172a;
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="../index.html">&#127968; Course Index</a>
      <a href="../week09-memory-management/index.html">&larr; Week 9 Hub</a>
      <span style="font-size: 0.85rem; font-weight: 700; color: #64748b;">Week 10: File Systems</span>
      <a href="../week11-multiprocessors/index.html">Next: Week 11 Hub &rarr;</a>
    </nav>

    <h1>Week 10: File System Architecture &amp; Implementation</h1>
    <p class="subtitle">File Abstractions, Directory Paths, Inodes, Block Allocation, and Buffer Cache Optimization</p>

    <div class="lead-card">
      <strong>Core Conceptual Shift:</strong> Raw storage disks understand only linear block sectors (`LBA 0...N`). File systems transform these raw byte sectors into human-readable hierarchical namespaces with persistent metadata, crash-resistant indexing structures (inodes and extents), and high-performance buffer caches.
    </div>

    <div class="module-grid">
      <div class="module-card">
        <div>
          <div class="module-num">Module 01</div>
          <h2 class="module-title">The File Abstraction &amp; APIs</h2>
          <p class="module-desc">
            Byte streams, file types, access modes, file descriptors, file position offsets, and POSIX file system call mechanics.
          </p>
        </div>
        <a href="01-files-abstraction.html" class="btn-module">Open Module 01 &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 02</div>
          <h2 class="module-title">Directories &amp; Path Resolution</h2>
          <p class="module-desc">
            Hierarchical directory entries, linear directories, B-Tree lookups, hard links vs. symbolic links, and path traversal.
          </p>
        </div>
        <a href="02-directories.html" class="btn-module">Open Module 02 &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 03</div>
          <h2 class="module-title">File System Implementation &amp; Inodes</h2>
          <p class="module-desc">
            Contiguous allocation, linked lists (FAT), Unix multi-level direct/indirect index nodes (inodes), and extents.
          </p>
        </div>
        <a href="03-filesystem-implementation.html" class="btn-module">Open Module 03 &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 04</div>
          <h2 class="module-title">Layout, Free Space &amp; Optimization</h2>
          <p class="module-desc">
            Block size trade-offs, free space bitmaps, disk defragmentation, page cache read-ahead, and synchronous write flush policies.
          </p>
        </div>
        <a href="04-management-optimization.html" class="btn-module">Open Module 04 &rarr;</a>
      </div>
    </div>
  </div>
</body>
</html>
""",

    os.path.join("week11-multiprocessors", "index.html"): r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 11: Multiprocessors &amp; Distributed Systems | COSC240</title>
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
      padding: 40px 16px;
      line-height: 1.6;
    }
    .container {
      max-width: 980px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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
    h1 {
      font-size: 1.85rem;
      color: #0f172a;
      margin: 0 0 6px 0;
    }
    .subtitle {
      font-size: 0.95rem;
      color: var(--text-muted);
      margin: 0 0 24px 0;
    }
    .lead-card {
      background: #f0f9ff;
      border-left: 4px solid var(--accent);
      padding: 16px 20px;
      border-radius: 0 6px 6px 0;
      margin-bottom: 32px;
      font-size: 0.92rem;
      color: #0369a1;
    }
    .lead-card strong { color: #0f172a; }

    .module-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }
    .module-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .module-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 12px rgba(0,0,0,0.06);
    }
    .module-num {
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
    }
    .module-title {
      font-size: 1.12rem;
      font-weight: 700;
      color: #0f172a;
      margin: 0 0 8px 0;
      line-height: 1.35;
    }
    .module-desc {
      font-size: 0.86rem;
      color: var(--text-muted);
      margin: 0 0 16px 0;
      line-height: 1.5;
      flex-grow: 1;
    }
    .btn-module {
      display: block;
      text-align: center;
      padding: 8px 14px;
      background: #f1f5f9;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #0f172a;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.84rem;
      transition: all 0.15s ease;
    }
    .btn-module:hover {
      background: #0f172a;
      color: #ffffff;
      border-color: #0f172a;
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="../index.html">&#127968; Course Index</a>
      <a href="../week10-file-management/index.html">&larr; Week 10 Hub</a>
      <span style="font-size: 0.85rem; font-weight: 700; color: #64748b;">Week 11: Multiprocessors</span>
      <a href="../week12-security/index.html">Next: Week 12 Hub &rarr;</a>
    </nav>

    <h1>Week 11: Multiprocessors &amp; Distributed Systems</h1>
    <p class="subtitle">Hardware Topologies, Cache Coherency, Multiprocessor Scheduling, and Distributed Middleware</p>

    <div class="lead-card">
      <strong>Core Conceptual Shift:</strong> When computation expands beyond a single memory bus to multicore sockets, NUMA nodes, and networked clusters, shared physical state vanishes. The OS must maintain coherency using hardware snooping protocols (MESI), handle NUMA memory latencies, and orchestrate distributed communication over unreliable networks via RPCs.
    </div>

    <div class="module-grid">
      <div class="module-card">
        <div>
          <div class="module-num">Module 01</div>
          <h2 class="module-title">Multiprocessor Hardware &amp; Coherency</h2>
          <p class="module-desc">
            UMA vs. NUMA architectures, bus snooping, MESI cache coherency state transitions, and memory interconnect fabrics.
          </p>
        </div>
        <a href="01-multiprocessor-hardware.html" class="btn-module">Open Module 01 &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 02</div>
          <h2 class="module-title">Multiprocessor Scheduling &amp; Affinity</h2>
          <p class="module-desc">
            Single-queue vs. multi-queue schedulers, soft/hard processor affinity, work stealing, and gang scheduling for parallel threads.
          </p>
        </div>
        <a href="02-multiprocessor-scheduling.html" class="btn-module">Open Module 02 &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 03</div>
          <h2 class="module-title">Multicomputers &amp; Interconnects</h2>
          <p class="module-desc">
            Message-passing architectures, cluster interconnect topologies (torus, hypercube), packet routing, and network interface cards.
          </p>
        </div>
        <a href="03-multicomputers-interconnects.html" class="btn-module">Open Module 03 &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 04</div>
          <h2 class="module-title">Distributed Shared Memory &amp; RPC</h2>
          <p class="module-desc">
            Page-based Distributed Shared Memory (DSM), Remote Procedure Calls (RPC), parameter marshaling, and stub generators.
          </p>
        </div>
        <a href="04-rpc-dsm-load-balancing.html" class="btn-module">Open Module 04 &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 05</div>
          <h2 class="module-title">Distributed Systems Middleware</h2>
          <p class="module-desc">
            Distributed file systems (NFS), clock synchronization (Lamport logical timestamps), consensus algorithms, and load balancing.
          </p>
        </div>
        <a href="05-distributed-systems-middleware.html" class="btn-module">Open Module 05 &rarr;</a>
      </div>
    </div>
  </div>
</body>
</html>
""",

    os.path.join("week12-security", "index.html"): r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 12: Security &amp; Protection | COSC240</title>
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
      padding: 40px 16px;
      line-height: 1.6;
    }
    .container {
      max-width: 980px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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
    h1 {
      font-size: 1.85rem;
      color: #0f172a;
      margin: 0 0 6px 0;
    }
    .subtitle {
      font-size: 0.95rem;
      color: var(--text-muted);
      margin: 0 0 24px 0;
    }
    .lead-card {
      background: #f0f9ff;
      border-left: 4px solid var(--accent);
      padding: 16px 20px;
      border-radius: 0 6px 6px 0;
      margin-bottom: 32px;
      font-size: 0.92rem;
      color: #0369a1;
    }
    .lead-card strong { color: #0f172a; }

    .module-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }
    .module-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .module-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 12px rgba(0,0,0,0.06);
    }
    .module-num {
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
    }
    .module-title {
      font-size: 1.12rem;
      font-weight: 700;
      color: #0f172a;
      margin: 0 0 8px 0;
      line-height: 1.35;
    }
    .module-desc {
      font-size: 0.86rem;
      color: var(--text-muted);
      margin: 0 0 16px 0;
      line-height: 1.5;
      flex-grow: 1;
    }
    .btn-module {
      display: block;
      text-align: center;
      padding: 8px 14px;
      background: #f1f5f9;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #0f172a;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.84rem;
      transition: all 0.15s ease;
    }
    .btn-module:hover {
      background: #0f172a;
      color: #ffffff;
      border-color: #0f172a;
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="../index.html">&#127968; Course Index</a>
      <a href="../week11-multiprocessors/index.html">&larr; Week 11 Hub</a>
      <span style="font-size: 0.85rem; font-weight: 700; color: #64748b;">Week 12: Security</span>
      <span style="font-size: 0.85rem; font-weight: 700; color: #94a3b8;">End of Course</span>
    </nav>

    <h1>Week 12: Operating System Security &amp; Protection</h1>
    <p class="subtitle">Security Environments, Access Matrices, Capability-Based Security, and Vulnerability Containment</p>

    <div class="lead-card">
      <strong>Core Conceptual Shift:</strong> An operating system cannot guarantee correctness without security. Security models formalize authorization and confidentiality: bounding process privileges via Access Control Lists (ACLs) and cryptographically unforgeable capability tokens, while employing address space randomization (ASLR) and hardware containment to prevent exploitation.
    </div>

    <div class="module-grid">
      <div class="module-card">
        <div>
          <div class="module-num">Module 01</div>
          <h2 class="module-title">The Security Environment &amp; Threats</h2>
          <p class="module-desc">
            Confidentiality, integrity, availability (CIA), threat models, passive wiretapping vs. active intrusion, and insider attacks.
          </p>
        </div>
        <a href="placeholder.html" class="btn-module">Open Module 01 &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 02</div>
          <h2 class="module-title">Protection Domains &amp; Access Control</h2>
          <p class="module-desc">
            The Lampson Access Matrix, Access Control Lists (ACLs), Capability Lists (C-Lists), and dynamic domain switching.
          </p>
        </div>
        <a href="placeholder.html" class="btn-module">Open Module 02 &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Module 03</div>
          <h2 class="module-title">Vulnerability Exploits &amp; Defenses</h2>
          <p class="module-desc">
            Stack buffer overflows, return-oriented programming (ROP), Address Space Layout Randomization (ASLR), and hardware execution disable (NX/XD).
          </p>
        </div>
        <a href="placeholder.html" class="btn-module">Open Module 03 &rarr;</a>
      </div>
    </div>
  </div>
</body>
</html>
"""
}

def update_all_week_hubs():
    updated_files = []
    for hub_path, hub_html in HUBS.items():
        os.makedirs(os.path.dirname(hub_path), exist_ok=True)
        with open(hub_path, "w", encoding="utf-8") as f:
            f.write(hub_html.strip() + "\n")
        print(f"--> Successfully updated {hub_path}")
        updated_files.append(hub_path)

    try:
        subprocess.run(["git", "add", "fix.py"] + updated_files, check=True)
        commit_msg = (
            "Standardize index hubs for Weeks 05 through 12 to unified design format\n\n"
            "Apply consistent navigation bar, core conceptual shift banner, and\n"
            "responsive module card grid across all remaining course index hubs."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_all_week_hubs()
