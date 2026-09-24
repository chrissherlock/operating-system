#!/usr/bin/env python3
# =====================================================================
# fix.py: Synchronize index.html and hubs with actual physical disk tree
# =====================================================================
import os
import shutil
import subprocess

# 1. Prune redundant stub folders that shadowed real directories
PHANTOM_DIRS = [
    "week01-intro",
    "week04-concurrency"
]

for p_dir in PHANTOM_DIRS:
    if os.path.exists(p_dir) and os.path.isdir(p_dir):
        # Only remove if it only has index.html or is an artificial stub
        files = os.listdir(p_dir)
        if len(files) <= 1:
            shutil.rmtree(p_dir)
            print(f"--> Pruned shadow stub directory: {p_dir}")

# 2. Complete, accurate index.html matching YOUR actual files
ACCURATE_INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>COSC240: Operating Systems &mdash; Course Materials</title>
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
      max-width: 1060px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    header {
      margin-bottom: 32px;
      padding-bottom: 20px;
      border-bottom: 2px solid #e2e8f0;
    }
    h1 {
      font-size: 1.95rem;
      color: #0f172a;
      margin: 0 0 6px 0;
    }
    .subtitle {
      font-size: 0.98rem;
      color: var(--text-muted);
      margin: 0;
    }

    .curriculum-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
      gap: 20px;
      margin-top: 24px;
    }
    .week-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .week-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 12px rgba(0,0,0,0.06);
    }
    .week-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }
    .week-number {
      font-family: var(--font-mono);
      font-size: 0.78rem;
      font-weight: 700;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .status-badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .status-badge.complete { background: #dcfce7; color: #166534; }
    .status-badge.active { background: #e0f2fe; color: #0369a1; }
    .status-badge.ready { background: #fef3c7; color: #b45309; }

    .week-title {
      font-size: 1.16rem;
      font-weight: 700;
      color: #0f172a;
      margin: 0 0 8px 0;
      line-height: 1.35;
    }
    .week-desc {
      font-size: 0.88rem;
      color: var(--text-muted);
      margin: 0 0 16px 0;
      line-height: 1.5;
      flex-grow: 1;
    }
    .module-links {
      list-style: none;
      padding: 0;
      margin: 0 0 20px 0;
      font-size: 0.84rem;
    }
    .module-links li {
      margin-bottom: 8px;
      padding-left: 14px;
      position: relative;
    }
    .module-links li::before {
      content: "\2022";
      position: absolute;
      left: 0;
      color: var(--accent);
      font-weight: bold;
    }
    .module-links a {
      color: #0369a1;
      text-decoration: none;
      font-weight: 600;
    }
    .module-links a:hover {
      text-decoration: underline;
    }
    .week-card-footer {
      margin-top: auto;
      padding-top: 14px;
      border-top: 1px solid #f1f5f9;
    }
    .hub-link {
      display: block;
      text-align: center;
      padding: 9px 14px;
      background: #f1f5f9;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #0f172a;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.85rem;
      transition: all 0.15s ease;
    }
    .hub-link:hover {
      background: #0f172a;
      color: #ffffff;
      border-color: #0f172a;
    }
    .hub-link.primary {
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
    }
    .hub-link.primary:hover {
      background: var(--accent-hover);
      border-color: var(--accent-hover);
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>COSC240: Operating Systems</h1>
      <p class="subtitle">Interactive Pedagogical Modules &amp; Systems Engineering Curriculum</p>
    </header>

    <div class="curriculum-grid">
      <!-- Week 1 -->
      <div class="week-card">
        <div class="week-card-header">
          <span class="week-number">Week 01</span>
          <span class="status-badge complete">4 Modules</span>
        </div>
        <h2 class="week-title">Operating System Concepts &amp; Architecture</h2>
        <p class="week-desc">
          The hardware-software interface, system call dispatch mechanisms, dual-mode protection rings, and trap handling.
        </p>
        <ul class="module-links">
          <li><a href="week01-operating-system-concepts/01-what-is-an-os-and-history.html">01. What is an OS &amp; History</a></li>
          <li><a href="week01-operating-system-concepts/02-hardware-review.html">02. Hardware Review &amp; CPU Modes</a></li>
          <li><a href="week01-operating-system-concepts/03-os-concepts.html">03. Fundamental OS Concepts</a></li>
          <li><a href="week01-operating-system-concepts/04-os-structure.html">04. OS Structure &amp; Kernel Models</a></li>
        </ul>
        <div class="week-card-footer">
          <a href="week01-operating-system-concepts/index.html" class="hub-link">&#127968; Open Week 1 Hub &rarr;</a>
        </div>
      </div>

      <!-- Week 2 -->
      <div class="week-card">
        <div class="week-card-header">
          <span class="week-number">Week 02</span>
          <span class="status-badge complete">4 Modules</span>
        </div>
        <h2 class="week-title">Processes &amp; Threads</h2>
        <p class="week-desc">
          Address space anatomy, Process Control Blocks (PCB), Linux task_struct, lifecycle transitions, and kernel threading models.
        </p>
        <ul class="module-links">
          <li><a href="week02-processes/01-process-model.html">01. The Process Model &amp; Memory Layout</a></li>
          <li><a href="week02-processes/02-process-lifecycle.html">02. Process Lifecycle &amp; State Transitions</a></li>
          <li><a href="week02-processes/03-classical-threads.html">03. Classical Thread Concepts</a></li>
          <li><a href="week02-processes/04-thread-implementation.html">04. Thread Implementation &amp; POSIX APIs</a></li>
        </ul>
        <div class="week-card-footer">
          <a href="week02-processes/index.html" class="hub-link">&#127968; Open Week 2 Hub &rarr;</a>
        </div>
      </div>

      <!-- Week 3 -->
      <div class="week-card" style="border-color: var(--accent);">
        <div class="week-card-header">
          <span class="week-number" style="color: var(--accent);">Week 03</span>
          <span class="status-badge active">4 Modules</span>
        </div>
        <h2 class="week-title" style="color: var(--accent);">CPU Scheduling &amp; Resource Allocation</h2>
        <p class="week-desc">
          Burst distributions, dispatch latency, batch algorithms, multi-level feedback queues (MLFQ), and real-time multiprocessor systems.
        </p>
        <ul class="module-links">
          <li><a href="week03-process-scheduling/01-scheduling-introduction.html">01. Intro to Scheduling (CR3, Latency)</a></li>
          <li><a href="week03-process-scheduling/02-batch-scheduling.html">02. Batch Scheduling (FCFS, SJF, SRTN, HRRN)</a></li>
          <li><a href="week03-process-scheduling/03-interactive-scheduling.html">03. Interactive Scheduling (RR, MLFQ, Stride)</a></li>
          <li><a href="week03-process-scheduling/04-realtime-multiprocessor.html">04. Real-Time &amp; SMP (RMS, EDF, Work Stealing)</a></li>
        </ul>
        <div class="week-card-footer">
          <a href="week03-process-scheduling/index.html" class="hub-link primary">&#127968; Open Week 3 Hub &rarr;</a>
        </div>
      </div>

      <!-- Week 4 -->
      <div class="week-card">
        <div class="week-card-header">
          <span class="week-number">Week 04</span>
          <span class="status-badge ready">Hub Ready</span>
        </div>
        <h2 class="week-title">Concurrency &amp; Mutual Exclusion</h2>
        <p class="week-desc">
          Race conditions, critical regions, software solutions (Peterson's), hardware atomic instructions (TSL, CAS), and spinlocks.
        </p>
        <ul class="module-links">
          <li><a href="week04-concurrency-and-mutual-exclusion/index.html">Week 4 Overview &amp; Learning Objectives</a></li>
          <li>Shared State Hazards &amp; Non-Atomic Code</li>
          <li>The 4 Conditions for Mutual Exclusion</li>
        </ul>
        <div class="week-card-footer">
          <a href="week04-concurrency-and-mutual-exclusion/index.html" class="hub-link">&#127968; Open Week 4 Hub &rarr;</a>
        </div>
      </div>

      <!-- Week 5 -->
      <div class="week-card">
        <div class="week-card-header">
          <span class="week-number">Week 05</span>
          <span class="status-badge ready">Hub Ready</span>
        </div>
        <h2 class="week-title">I/O Systems &amp; Disk Scheduling</h2>
        <p class="week-desc">
          Device controllers, polling vs. interrupts, Direct Memory Access (DMA), disk geometry, and rotational media arm scheduling.
        </p>
        <ul class="module-links">
          <li><a href="week05-io-and-disk-scheduling/index.html">Week 5 Overview &amp; Architecture</a></li>
          <li>Device Controllers &amp; DMA Hardware</li>
          <li>Rotational Head Scheduling (SSTF, SCAN, C-SCAN)</li>
        </ul>
        <div class="week-card-footer">
          <a href="week05-io-and-disk-scheduling/index.html" class="hub-link">&#127968; Open Week 5 Hub &rarr;</a>
        </div>
      </div>

      <!-- Week 6 -->
      <div class="week-card">
        <div class="week-card-header">
          <span class="week-number">Week 06</span>
          <span class="status-badge complete">4 Interactive Aids</span>
        </div>
        <h2 class="week-title">Synchronization &amp; Deadlocks</h2>
        <p class="week-desc">
          Semaphores, condition variables, Coffman conditions, Resource Allocation Graphs, and classical deadlock sandboxes.
        </p>
        <ul class="module-links">
          <li><a href="week06-synchronisation-and-deadlock/deadlock-detector.html">Deadlock Detector &amp; RAG Simulator</a></li>
          <li><a href="week06-synchronisation-and-deadlock/dining-philosophers.html">Dining Philosophers Problem Sandbox</a></li>
          <li><a href="week06-synchronisation-and-deadlock/ipc-deadlock.html">IPC Deadlock &amp; Mutex Analysis</a></li>
          <li><a href="week06-synchronisation-and-deadlock/database-deadlock.html">Database Two-Phase Locking Deadlock</a></li>
        </ul>
        <div class="week-card-footer">
          <a href="week06-synchronisation-and-deadlock/index.html" class="hub-link">&#127968; Open Week 6 Hub &rarr;</a>
        </div>
      </div>

      <!-- Week 9 -->
      <div class="week-card">
        <div class="week-card-header">
          <span class="week-number">Week 09</span>
          <span class="status-badge complete">15+ Modules &amp; Aids</span>
        </div>
        <h2 class="week-title">Memory Management &amp; Virtual Memory</h2>
        <p class="week-desc">
          Physical allocation, buddy allocator, address translation, page tables, TLBs, page faults, and replacement algorithms.
        </p>
        <ul class="module-links">
          <li><a href="week09-memory-management/buddy-allocator-tutorial.html">Buddy Allocator Interactive Tutorial</a></li>
          <li><a href="week09-memory-management/pte-sandbox.html">Page Table Entry (PTE) Sandbox</a></li>
          <li><a href="week09-memory-management/tlb-sandbox.html">Translation Lookaside Buffer (TLB) Tracer</a></li>
          <li><a href="week09-memory-management/08-aging-algorithm.html">Page Replacement: Aging Algorithm</a></li>
          <li><a href="week09-memory-management/wsclock.html">Working Set &amp; WSClock Sandboxes</a></li>
        </ul>
        <div class="week-card-footer">
          <a href="week09-memory-management/index.html" class="hub-link">&#127968; Open Week 9 Hub &rarr;</a>
        </div>
      </div>

      <!-- Week 10 -->
      <div class="week-card">
        <div class="week-card-header">
          <span class="week-number">Week 10</span>
          <span class="status-badge complete">4 Modules</span>
        </div>
        <h2 class="week-title">File System Architecture &amp; Implementation</h2>
        <p class="week-desc">
          File abstractions, directory hierarchies, Unix inodes, extent trees, free space management, and performance caching.
        </p>
        <ul class="module-links">
          <li><a href="week10-file-management/01-files-abstraction.html">01. The File Abstraction</a></li>
          <li><a href="week10-file-management/02-directories.html">02. Directories &amp; Hierarchical Paths</a></li>
          <li><a href="week10-file-management/03-filesystem-implementation.html">03. File System Implementation (Inodes)</a></li>
          <li><a href="week10-file-management/04-management-optimization.html">04. Reliability, Layout &amp; Optimization</a></li>
        </ul>
        <div class="week-card-footer">
          <a href="week10-file-management/index.html" class="hub-link">&#127968; Open Week 10 Hub &rarr;</a>
        </div>
      </div>

      <!-- Week 11 -->
      <div class="week-card">
        <div class="week-card-header">
          <span class="week-number">Week 11</span>
          <span class="status-badge complete">5 Modules</span>
        </div>
        <h2 class="week-title">Multiprocessor Systems &amp; Distributed Computing</h2>
        <p class="week-desc">
          SMP cache coherency (MESI), multicomputers, Remote Procedure Calls (RPC), Distributed Shared Memory (DSM), and middleware.
        </p>
        <ul class="module-links">
          <li><a href="week11-multiprocessors/01-multiprocessor-hardware.html">01. Multiprocessor Hardware &amp; Caches</a></li>
          <li><a href="week11-multiprocessors/02-multiprocessor-scheduling.html">02. Multiprocessor Scheduling &amp; Affinity</a></li>
          <li><a href="week11-multiprocessors/03-multicomputers-interconnects.html">03. Multicomputers &amp; Interconnects</a></li>
          <li><a href="week11-multiprocessors/04-rpc-dsm-load-balancing.html">04. Distributed Shared Memory &amp; RPC</a></li>
          <li><a href="week11-multiprocessors/05-distributed-systems-middleware.html">05. Distributed Systems Middleware</a></li>
        </ul>
        <div class="week-card-footer">
          <a href="week11-multiprocessors/index.html" class="hub-link">&#127968; Open Week 11 Hub &rarr;</a>
        </div>
      </div>

      <!-- Week 12 -->
      <div class="week-card">
        <div class="week-card-header">
          <span class="week-number">Week 12</span>
          <span class="status-badge ready">Hub Ready</span>
        </div>
        <h2 class="week-title">Operating System Security &amp; Protection</h2>
        <p class="week-desc">
          Security environments, access control lists (ACLs), capabilities, protection rings, buffer overflows, and hardware containment.
        </p>
        <ul class="module-links">
          <li><a href="week12-security/index.html">Week 12 Overview &amp; Learning Objectives</a></li>
          <li>Access Matrix &amp; Protection Domains</li>
          <li>Security Vulnerabilities &amp; Containment</li>
        </ul>
        <div class="week-card-footer">
          <a href="week12-security/index.html" class="hub-link">&#127968; Open Week 12 Hub &rarr;</a>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# Write the accurate master index
with open("index.html", "w", encoding="utf-8") as f:
    f.write(ACCURATE_INDEX_HTML.strip() + "\n")
print("--> Updated index.html with all real directory targets.")

# 3. Synchronize internal navigation bars in Week 1, 2, and 3 hubs
# Week 1 hub -> week01-operating-system-concepts/index.html
w1_hub_path = os.path.join("week01-operating-system-concepts", "index.html")
w1_hub_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 1: Operating System Concepts | COSC240</title>
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
      <span style="font-size: 0.85rem; font-weight: 700; color: #64748b;">Week 1: Introduction</span>
      <a href="../week02-processes/index.html">Next: Week 2 Hub &rarr;</a>
    </nav>

    <h1>Week 1: Operating System Concepts</h1>
    <p class="subtitle">The Hardware-Software Interface, Dual-Mode Protection, and Kernel Models</p>

    <div class="lead-card">
      <strong>Core Conceptual Shift:</strong> Software cannot be trusted with raw hardware access. The operating system acts as an illusionist and an arbiter: virtualizing physical devices to provide safe abstractions, while using CPU hardware privilege rings to enforce strict protection boundaries between untrusted user code and the privileged supervisor kernel.
    </div>

    <div class="module-grid">
      <!-- Module 01 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 01</div>
          <h2 class="module-title">What is an Operating System &amp; History</h2>
          <p class="module-desc">
            The dual role of the OS as extended machine and resource manager, computing eras from vacuum tubes to modern personal computing.
          </p>
        </div>
        <a href="01-what-is-an-os-and-history.html" class="btn-module">Open Module 01 &rarr;</a>
      </div>

      <!-- Module 02 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 02</div>
          <h2 class="module-title">Hardware Review &amp; CPU Modes</h2>
          <p class="module-desc">
            Processors, memory hierarchies (registers, caches, main memory), hardware protection rings, and interrupt mechanisms.
          </p>
        </div>
        <a href="02-hardware-review.html" class="btn-module">Open Module 02 &rarr;</a>
      </div>

      <!-- Module 03 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 03</div>
          <h2 class="module-title">Fundamental OS Concepts</h2>
          <p class="module-desc">
            Processes, address spaces, file system abstractions, input/output architecture, and protection boundaries.
          </p>
        </div>
        <a href="03-os-concepts.html" class="btn-module">Open Module 03 &rarr;</a>
      </div>

      <!-- Module 04 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 04</div>
          <h2 class="module-title">Operating System Structure</h2>
          <p class="module-desc">
            Monolithic systems, layered architectures, microkernel paradigms, client-server models, and virtual machine hypervisors.
          </p>
        </div>
        <a href="04-os-structure.html" class="btn-module">Open Module 04 &rarr;</a>
      </div>
    </div>
  </div>
</body>
</html>
"""
with open(w1_hub_path, "w", encoding="utf-8") as f:
    f.write(w1_hub_html.strip() + "\n")
print(f"--> Updated Week 1 hub at {w1_hub_path}")

# Update Week 2 hub next link
w2_hub_path = os.path.join("week02-processes", "index.html")
if os.path.exists(w2_hub_path):
    with open(w2_hub_path, "r", encoding="utf-8") as f:
        w2_content = f.read()
    w2_content = w2_content.replace('href="../week01-intro/index.html"', 'href="../week01-operating-system-concepts/index.html"')
    with open(w2_hub_path, "w", encoding="utf-8") as f:
        f.write(w2_content)
    print(f"--> Updated Week 2 hub links at {w2_hub_path}")

# Update Week 3 hub next link
w3_hub_path = os.path.join("week03-process-scheduling", "index.html")
if os.path.exists(w3_hub_path):
    with open(w3_hub_path, "r", encoding="utf-8") as f:
        w3_content = f.read()
    w3_content = w3_content.replace('href="../week04-concurrency/index.html"', 'href="../week04-concurrency-and-mutual-exclusion/index.html"')
    with open(w3_hub_path, "w", encoding="utf-8") as f:
        f.write(w3_content)
    print(f"--> Updated Week 3 hub links at {w3_hub_path}")

# Update Week 4 hub
w4_hub_path = os.path.join("week04-concurrency-and-mutual-exclusion", "index.html")
w4_hub_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 4: Concurrency &amp; Mutual Exclusion | COSC240</title>
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
      <a href="../week03-process-scheduling/index.html">&larr; Week 3 Hub</a>
      <span style="font-size: 0.85rem; font-weight: 700; color: #64748b;">Week 4: Concurrency</span>
      <a href="../week05-io-and-disk-scheduling/index.html">Next: Week 5 Hub &rarr;</a>
    </nav>

    <h1>Week 4: Concurrency &amp; Mutual Exclusion</h1>
    <p class="subtitle">Shared Resources, Race Hazards, Hardware Primitives, and Mutual Exclusion</p>

    <div class="lead-card">
      <strong>Core Conceptual Shift:</strong> Processes and threads cannot be assumed to run in isolation. When execution paths access shared memory without coordination, non-deterministic preemption produces race hazards. This week analyzes how software invariants and hardware synchronization primitives enforce mutual exclusion across single-core and multiprocessor architectures.
    </div>

    <div class="module-grid">
      <!-- Module 01 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 01</div>
          <h2 class="module-title">Race Conditions &amp; Critical Regions</h2>
          <p class="module-desc">
            Shared state hazards, non-atomic assembly instruction decomposition, execution interleaving, and the four conditions for mutual exclusion.
          </p>
        </div>
        <a href="01-race-conditions-critical-regions.html" class="btn-module">Open Module 01 &rarr;</a>
      </div>

      <!-- Module 02 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 02</div>
          <h2 class="module-title">Hardware Primitives &amp; Spinlocks</h2>
          <p class="module-desc">
            Interrupt masking limits, Peterson's software algorithm, atomic hardware instructions (TSL, CAS), spinlocks, and cache line contention.
          </p>
        </div>
        <a href="02-hardware-primitives-spinlocks.html" class="btn-module">Open Module 02 &rarr;</a>
      </div>

      <!-- Module 03 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 03</div>
          <h2 class="module-title">Sleep/Wakeup, Semaphores &amp; Monitors</h2>
          <p class="module-desc">
            Lost wakeups, Dijkstra's integer semaphores, mutexes, futex kernel queues, language-level monitors, and condition variables.
          </p>
        </div>
        <a href="03-semaphores-mutexes-monitors.html" class="btn-module">Open Module 03 &rarr;</a>
      </div>

      <!-- Module 04 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 04</div>
          <h2 class="module-title">Classical Synchronization Problems</h2>
          <p class="module-desc">
            The Bounded-Buffer (Producer-Consumer) problem, lock ordering deadlocks, Dining Philosophers, and Readers-Writers fairness.
          </p>
        </div>
        <a href="04-classical-synchronization.html" class="btn-module">Open Module 04 &rarr;</a>
      </div>
    </div>
  </div>
</body>
</html>
"""
with open(w4_hub_path, "w", encoding="utf-8") as f:
    f.write(w4_hub_html.strip() + "\n")
print(f"--> Updated Week 4 hub at {w4_hub_path}")

# Git stage & commit
try:
    subprocess.run(["git", "add", "fix.py", "index.html", w1_hub_path, w2_hub_path, w3_hub_path, w4_hub_path], check=True)
    commit_msg = (
        "Align root index.html and navigation hubs with actual repository layout\n\n"
        "Prune phantom stub folders and restore exact links to real course modules\n"
        "for Week 01, 04, 05, 06, 09, 10, 11, and 12 across the curriculum grid."
    )
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("--> Git sync completed successfully!")
except Exception as e:
    print(f"Git execution note: {e}")
