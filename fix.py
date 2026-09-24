#!/usr/bin/env python3
# =====================================================================
# fix.py: Update root index.html with Week 5 & Week 6 full module links
# =====================================================================
import os
import subprocess

TARGET_FILE = "index.html"

ROOT_INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>COSC240: Operating Systems - Course Hub</title>
  <style>
    :root {
      --primary: #0f172a;
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --border: #e2e8f0;
      --card-bg: #ffffff;
      --text: #334155;
      --text-muted: #64748b;
      --bg: #f8fafc;
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: var(--font-sans);
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 24px;
    }
    .container { max-width: 1040px; margin: 0 auto; }
    .hero-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 36px;
      margin-bottom: 32px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .badge {
      display: inline-block;
      background: #e0f2fe;
      color: #0369a1;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 999px;
      margin-bottom: 12px;
    }
    h1 { margin: 0 0 12px 0; font-size: 2rem; color: var(--primary); letter-spacing: -0.02em; }
    .lead-text { margin: 0 0 20px 0; font-size: 1.05rem; color: var(--text); line-height: 1.7; }
    .weeks-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 32px;
    }
    .week-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .week-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
    }
    .week-num {
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }
    .week-title { font-size: 1.15rem; font-weight: 700; color: var(--primary); margin: 0 0 10px 0; }
    .week-desc { font-size: 0.88rem; color: var(--text-muted); margin: 0 0 16px 0; line-height: 1.55; }
    .link-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 16px;
      font-size: 0.85rem;
    }
    .link-list a {
      color: var(--accent);
      text-decoration: none;
      font-weight: 600;
    }
    .link-list a:hover { text-decoration: underline; }
    .hub-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      background: var(--primary);
      color: #ffffff;
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 600;
      padding: 10px 16px;
      border-radius: 6px;
      transition: background 0.15s ease;
      width: 100%;
    }
    .hub-btn:hover { background: var(--accent-hover); }
    @media (max-width: 768px) {
      .weeks-grid { grid-template-columns: 1fr; }
      body { padding: 16px; }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="hero-card">
      <span class="badge">University of New England &bull; COSC240</span>
      <h1>Operating Systems Course Hub</h1>
      <p class="lead-text">
        Welcome to the central course portal for <strong>COSC240 Operating Systems</strong>. Explore interactive pedagogical modules, animated hardware/software steppers, and simulation sandboxes covering processes, synchronization, memory management, file systems, I/O, and RAID architectures.
      </p>
    </div>

    <div class="weeks-grid">
      <!-- Week 1 -->
      <div class="week-card">
        <div>
          <div class="week-num">Week 01</div>
          <h2 class="week-title">OS Concepts &amp; Hardware Review</h2>
          <p class="week-desc">Evolution of operating systems, kernel architectures, dual-mode execution, system calls, and hardware primitives.</p>
        </div>
        <a href="week01-operating-system-concepts/index.html" class="hub-btn">Open Week 1 Hub &rarr;</a>
      </div>

      <!-- Week 2 -->
      <div class="week-card">
        <div>
          <div class="week-num">Week 02</div>
          <h2 class="week-title">Processes, Threads &amp; Concurrency</h2>
          <p class="week-desc">Process control blocks, process lifecycle states, user-space vs. kernel-space threads, and multithreading models.</p>
        </div>
        <a href="week02-processes/index.html" class="hub-btn">Open Week 2 Hub &rarr;</a>
      </div>

      <!-- Week 3 -->
      <div class="week-card">
        <div>
          <div class="week-num">Week 03</div>
          <h2 class="week-title">CPU Scheduling Algorithms</h2>
          <p class="week-desc">Batch scheduling, interactive scheduling, multi-level feedback queues, real-time deadlines, and multiprocessor load balancing.</p>
        </div>
        <a href="week03-process-scheduling/index.html" class="hub-btn">Open Week 3 Hub &rarr;</a>
      </div>

      <!-- Week 4 -->
      <div class="week-card">
        <div>
          <div class="week-num">Week 04</div>
          <h2 class="week-title">Concurrency &amp; Mutual Exclusion</h2>
          <p class="week-desc">Critical sections, race conditions, Peterson's solution, hardware atomic primitives (test-and-set), semaphores, mutexes, and monitors.</p>
        </div>
        <a href="week04-concurrency-and-mutual-exclusion/index.html" class="hub-btn">Open Week 4 Hub &rarr;</a>
      </div>

      <!-- Week 5 -->
      <div class="week-card">
        <div>
          <div class="week-num">Week 05</div>
          <h2 class="week-title">I/O Subsystems &amp; Disk Scheduling</h2>
          <p class="week-desc">Device controllers, PIO vs. MMIO, APIC interrupts, DMA transfers, mechanical disk geometry, arm scheduling (SSTF, SCAN), and RAID levels 0&ndash;6.</p>
          <div class="link-list">
            <a href="week05-io-and-disk-scheduling/01-io-hardware-device-controllers.html">&bull; Module 01: I/O Hardware &amp; Controllers</a>
            <a href="week05-io-and-disk-scheduling/02-interrupts-and-dma.html">&bull; Module 02: Interrupts &amp; DMA</a>
            <a href="week05-io-and-disk-scheduling/03-disk-hardware-scheduling.html">&bull; Module 03: Disk Geometry &amp; Scheduling</a>
            <a href="week05-io-and-disk-scheduling/04-raid-architectures.html">&bull; Module 04: RAID Storage Architectures</a>
          </div>
        </div>
        <a href="week05-io-and-disk-scheduling/index.html" class="hub-btn">Open Week 5 Hub &rarr;</a>
      </div>

      <!-- Week 6 -->
      <div class="week-card">
        <div>
          <div class="week-num">Week 06</div>
          <h2 class="week-title">Synchronization &amp; Deadlock</h2>
          <p class="week-desc">Livelock, starvation, priority inversion (Mars Pathfinder), Coffman conditions, Resource Allocation Graphs, Banker's Algorithm, and dining philosophers.</p>
          <div class="link-list">
            <a href="week06-synchronization-and-deadlock/01-concurrency-hazards-livelock-starvation.html">&bull; Module 01: Livelock, Starvation &amp; PIP</a>
            <a href="week06-synchronization-and-deadlock/02-deadlock-characterization-coffman-conditions.html">&bull; Module 02: Coffman Conditions &amp; RAGs</a>
            <a href="week06-synchronization-and-deadlock/03-deadlock-handling-bankers-algorithm.html">&bull; Module 03: Banker's Algorithm &amp; Prevention</a>
            <a href="week06-synchronization-and-deadlock/04-classic-synchronization-real-world-defenses.html">&bull; Module 04: Classic Problems &amp; Defenses</a>
            <a href="week06-synchronization-and-deadlock/deadlock-detector.html">&bull; Lab: Deadlock Detection Simulator</a>
            <a href="week06-synchronization-and-deadlock/dining-philosophers.html">&bull; Lab: Dining Philosophers Simulator</a>
            <a href="week06-synchronization-and-deadlock/database-deadlock.html">&bull; Lab: Database 2PL Simulator</a>
            <a href="week06-synchronization-and-deadlock/ipc-deadlock.html">&bull; Lab: IPC Message Passing Deadlock</a>
          </div>
        </div>
        <a href="week06-synchronization-and-deadlock/index.html" class="hub-btn">Open Week 6 Hub &rarr;</a>
      </div>

      <!-- Week 7 -->
      <div class="week-card">
        <div>
          <div class="week-num">Week 07</div>
          <h2 class="week-title">Memory Management &amp; Virtual Memory</h2>
          <p class="week-desc">Base and limit registers, swapping, free-space allocation, paging hardware, TLB acceleration, and multi-level page tables.</p>
        </div>
        <a href="week09-memory-management/index.html" class="hub-btn">Open Week 7 Hub &rarr;</a>
      </div>

      <!-- Week 8 -->
      <div class="week-card">
        <div>
          <div class="week-num">Week 08</div>
          <h2 class="week-title">Virtual Memory Replacement &amp; Thrashing</h2>
          <p class="week-desc">Page fault handling, FIFO, Optimal, LRU, Clock, Aging, Working Set model, WSClock policy, and global vs. local allocation.</p>
        </div>
        <a href="week09-memory-management/index.html" class="hub-btn">Open Virtual Memory Hub &rarr;</a>
      </div>

      <!-- Week 9 -->
      <div class="week-card">
        <div>
          <div class="week-num">Week 09</div>
          <h2 class="week-title">File Systems &amp; Storage Management</h2>
          <p class="week-desc">File abstractions, directory structures, inode allocation, contiguous vs. linked vs. indexed allocation, and journaled filesystems.</p>
        </div>
        <a href="week10-file-management/index.html" class="hub-btn">Open Week 9 Hub &rarr;</a>
      </div>

      <!-- Week 10 -->
      <div class="week-card">
        <div>
          <div class="week-num">Week 10</div>
          <h2 class="week-title">Multiprocessors &amp; Distributed Systems</h2>
          <p class="week-desc">Symmetric multiprocessing (SMP), cache coherency (MESI), NUMA architectures, multiprocessor scheduling, RPC, and DSM.</p>
        </div>
        <a href="week11-multiprocessors/index.html" class="hub-btn">Open Week 10 Hub &rarr;</a>
      </div>
    </div>
  </div>
</body>
</html>
"""

def update_root_index():
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(ROOT_INDEX_HTML.strip() + "\n")
    print(f"--> Successfully updated root course index at {TARGET_FILE}")

def run_git_sync():
    status = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
    if not status:
        print("--> Working tree is clean. Nothing to commit.")
        return

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Update root course index.html to link Week 5 and Week 6 modules\n\n"
            "Refresh COSC240 course index card grid to include links for Week 5 I/O\n"
            "and disk scheduling, RAID, Week 6 deadlock detectors, and simulators."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_root_index()
    run_git_sync()
