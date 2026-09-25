#!/usr/bin/env python3
# =====================================================================
# fix.py: Merge Week 7 into Week 9 Memory Management and prune Week 7
# =====================================================================
import os
import shutil
import subprocess

SRC_DIR = "week07-memory-management-virtual-memory"
DEST_DIR = "week09-memory-management"

WEEK09_INDEX_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 9: Memory Management &amp; Virtual Memory - COSC240</title>
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
    .nav-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #ffffff;
      border: 1px solid var(--border);
      padding: 12px 20px;
      border-radius: 8px;
      margin-bottom: 24px;
    }
    .nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--accent);
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 6px;
      transition: background 0.15s ease;
    }
    .nav-btn:hover { background: #f0f9ff; }
    .hero-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 32px;
      margin-bottom: 28px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .week-tag {
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
    h1 { margin: 0 0 12px 0; font-size: 1.85rem; color: var(--primary); }
    .lead-text { margin: 0 0 20px 0; font-size: 1.05rem; color: var(--text); line-height: 1.7; }
    .briefing-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-top: 24px;
      padding-top: 24px;
      border-top: 1px solid var(--border);
    }
    .briefing-box {
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px 20px;
    }
    .briefing-title {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--primary);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .briefing-list { margin: 0; padding-left: 18px; font-size: 0.88rem; color: var(--text); }
    .briefing-list li { margin-bottom: 6px; }
    .modules-heading {
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--primary);
      margin: 28px 0 16px 0;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .modules-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 24px;
    }
    .module-card {
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
    .module-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
    }
    .module-num {
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }
    .module-title { font-size: 1.15rem; font-weight: 700; color: var(--primary); margin: 0 0 10px 0; }
    .module-desc { font-size: 0.88rem; color: var(--text-muted); margin: 0 0 14px 0; line-height: 1.55; }
    .module-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px; }
    .tag {
      background: #f1f5f9;
      color: #475569;
      font-size: 0.72rem;
      font-family: var(--font-mono);
      padding: 3px 8px;
      border-radius: 4px;
    }
    .launch-btn {
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
    .launch-btn:hover { background: var(--accent-hover); }
    /* Interactive Lab Grid */
    .lab-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      margin-bottom: 32px;
    }
    .lab-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .lab-title { font-size: 0.88rem; font-weight: 700; color: var(--primary); margin: 0 0 6px 0; }
    .lab-desc { font-size: 0.78rem; color: var(--text-muted); margin: 0 0 12px 0; line-height: 1.4; }
    .lab-link { color: var(--accent); text-decoration: none; font-size: 0.8rem; font-weight: 600; }
    .lab-link:hover { text-decoration: underline; }
    @media (max-width: 768px) {
      .briefing-grid, .modules-grid, .lab-grid { grid-template-columns: 1fr; }
      body { padding: 16px; }
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="../week06-synchronization-and-deadlock/index.html" class="nav-btn">&larr; Week 6: Synchronization &amp; Deadlock</a>
      <a href="../index.html" class="nav-btn">&#127968; Course Index</a>
      <a href="../week10-file-management/index.html" class="nav-btn">Week 10: File Management &rarr;</a>
    </nav>

    <div class="hero-card">
      <span class="week-tag">COSC240 &bull; Operating Systems</span>
      <h1>Week 9: Memory Management &amp; Virtual Memory</h1>
      <p class="lead-text">
        Following the mid-trimester break, we bridge the chasm between raw physical hardware addressing and isolated virtual memory abstractions. We analyze <strong>Address Relocation</strong>, <strong>Dynamic Partitioning</strong>, <strong>Paging Architectures</strong>, <strong>Hardware TLB Caching</strong>, and <strong>Page Replacement Algorithms</strong>.
      </p>

      <div class="briefing-grid">
        <div class="briefing-box">
          <div class="briefing-title">
            <span>&#128218;</span> What You Will Learn
          </div>
          <ul class="briefing-list">
            <li>The evolution from <strong>bare-metal monoprogramming</strong> to dynamic hardware relocation via Base and Limit registers.</li>
            <li>Contiguous allocation algorithms (First-Fit, Best-Fit, Worst-Fit) and buddy-system power-of-two coalescing.</li>
            <li>Internal vs. external <strong>memory fragmentation</strong>, Knuth's 50% rule, and compaction overheads.</li>
            <li>Hardware page tables, virtual address decomposition ($p, d$), and MMU translation mechanics.</li>
            <li>Hardware acceleration via <strong>Translation Lookaside Buffers (TLBs)</strong> and Effective Memory Access Time (EMAT).</li>
            <li>Page replacement algorithms: FIFO, Optimal (Belady), LRU, Clock, Aging, and Working Set (WSClock).</li>
          </ul>
        </div>

        <div class="briefing-box">
          <div class="briefing-title">
            <span>&#9989;</span> What You Should Do
          </div>
          <ul class="briefing-list">
            <li>Read <strong>Tanenbaum &amp; Bos</strong> Chapter 3 (Memory Management) and <strong>OSTEP</strong> Chapters 13–23.</li>
            <li>Work through Modules 01 to 04 sequentially, tracing address translation formulas.</li>
            <li>Engage with the Page Replacement Deep-Dives (Clock, Aging, Working Set).</li>
            <li>Complete <strong>Theory Tutorial 07/09</strong> (Multi-Level Page Table Footprints &amp; EMAT).</li>
            <li>Complete <strong>Practical Tutorial 07/09</strong> (Simulating Free List Allocation Policies in C).</li>
            <li>Prepare for <strong>Quiz 4</strong> (covering Virtual Memory, Paging, and Address Translation).</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Core Foundational Modules -->
    <div class="modules-heading">
      <span>&#128194;</span> Foundational Memory Virtualization Modules
    </div>

    <div class="modules-grid">
      <!-- Module 01 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 01</div>
          <h2 class="module-title">Physical Address Spaces &amp; Monoprogramming</h2>
          <p class="module-desc">Trace the evolution from early bare-metal execution to dynamic hardware relocation using Base and Limit registers, swapping, and memory overlays.</p>
          <div class="module-tags">
            <span class="tag">Monoprogramming</span>
            <span class="tag">Base &amp; Limit</span>
            <span class="tag">Address Relocation</span>
            <span class="tag">Fragmentation</span>
          </div>
        </div>
        <a href="01-physical-memory-abstractions.html" class="launch-btn">Launch Module 01 &rarr;</a>
      </div>

      <!-- Module 02 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 02</div>
          <h2 class="module-title">Dynamic Partitioning &amp; Free Space Management</h2>
          <p class="module-desc">Analyze contiguous memory allocation policies (First-Fit, Best-Fit, Worst-Fit), bitmap tracking vs. free linked lists, and power-of-two buddy allocators.</p>
          <div class="module-tags">
            <span class="tag">Dynamic Partitioning</span>
            <span class="tag">Free Lists</span>
            <span class="tag">Buddy Allocator</span>
            <span class="tag">Compaction</span>
          </div>
        </div>
        <a href="02-dynamic-partitioning-free-lists.html" class="launch-btn">Launch Module 02 &rarr;</a>
      </div>

      <!-- Module 03 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 03</div>
          <h2 class="module-title">Virtual Memory &amp; Paging Architectures</h2>
          <p class="module-desc">Examine the Memory Management Unit (MMU), virtual address split ($p, d$), Page Table Entries (PTE flags), and 64-bit multi-level hierarchical page tables.</p>
          <div class="module-tags">
            <span class="tag">Virtual Memory</span>
            <span class="tag">MMU Translation</span>
            <span class="tag">Page Tables</span>
            <span class="tag">PTE Flags</span>
          </div>
        </div>
        <a href="03-virtual-memory-paging-tables.html" class="launch-btn">Launch Module 03 &rarr;</a>
      </div>

      <!-- Module 04 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 04</div>
          <h2 class="module-title">TLB Acceleration &amp; Inverted Page Tables</h2>
          <p class="module-desc">Study hardware TLB caching, associative address matching, hardware vs. software walks, EMAT calculations, and inverted page tables with hash anchors.</p>
          <div class="module-tags">
            <span class="tag">TLB Cache</span>
            <span class="tag">EMAT Formula</span>
            <span class="tag">Inverted Page Tables</span>
            <span class="tag">Hardware Walk</span>
          </div>
        </div>
        <a href="04-tlb-hardware-inverted-page-tables.html" class="launch-btn">Launch Module 04 &rarr;</a>
      </div>
    </div>

    <!-- Page Replacement Algorithms Deep-Dives -->
    <div class="modules-heading">
      <span>&#9881;</span> Page Replacement &amp; Thrashing Subsystems
    </div>

    <div class="modules-grid">
      <div class="module-card">
        <div>
          <div class="module-num">Algorithm 07</div>
          <h2 class="module-title">Clock Page Replacement</h2>
          <p class="module-desc">The circular first-in, first-out buffer using hardware referenced bits to approximate Least Recently Used (LRU) eviction with minimal software overhead.</p>
          <div class="module-tags">
            <span class="tag">Clock Pointer</span>
            <span class="tag">Reference Bit</span>
            <span class="tag">Second-Chance</span>
          </div>
        </div>
        <a href="07-clock.html" class="launch-btn">Explore Clock Algorithm &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Algorithm 08</div>
          <h2 class="module-title">Aging Algorithm in Software</h2>
          <p class="module-desc">Simulating true LRU eviction through shift registers updated at timer clock ticks, tracking recent page reference recency.</p>
          <div class="module-tags">
            <span class="tag">Aging Registers</span>
            <span class="tag">Shift Vectors</span>
            <span class="tag">LRU Approximation</span>
          </div>
        </div>
        <a href="08-aging-algorithm.html" class="launch-btn">Explore Aging Algorithm &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Algorithm 09 &amp; 10</div>
          <h2 class="module-title">Working Set &amp; WSClock</h2>
          <p class="module-desc">Peter Denning's working set principle: calculating page sets referenced in virtual time window $\tau$ to prevent thrashing and maintain multiprogramming equilibrium.</p>
          <div class="module-tags">
            <span class="tag">Working Set W(t, &tau;)</span>
            <span class="tag">WSClock</span>
            <span class="tag">Thrashing Control</span>
          </div>
        </div>
        <a href="10-wsclock.html" class="launch-btn">Explore WSClock &rarr;</a>
      </div>

      <div class="module-card">
        <div>
          <div class="module-num">Policy 11</div>
          <h2 class="module-title">Local vs. Global Allocation Policies</h2>
          <p class="module-desc">Contrasting fixed process partition boundaries with dynamic page stealing across competing processes, Page Fault Frequency (PFF), and load control.</p>
          <div class="module-tags">
            <span class="tag">Local Allocation</span>
            <span class="tag">Global Allocation</span>
            <span class="tag">PFF Tracing</span>
          </div>
        </div>
        <a href="11-local-vs-global.html" class="launch-btn">Explore Allocation Policies &rarr;</a>
      </div>
    </div>

    <!-- Interactive Sandboxes -->
    <div class="modules-heading">
      <span>&#128302;</span> Interactive Visualizers &amp; Simulation Laboratories
    </div>

    <div class="lab-grid">
      <div class="lab-card">
        <div>
          <h3 class="lab-title">PTE Sandbox</h3>
          <p class="lab-desc">Inspect bitfields, protection flags, and dirty/accessed states in Page Table Entries.</p>
        </div>
        <a href="pte-sandbox.html" class="lab-link">Open PTE Sandbox &rarr;</a>
      </div>
      <div class="lab-card">
        <div>
          <h3 class="lab-title">TLB Sandbox</h3>
          <p class="lab-desc">Trace associative TLB lookups, cache misses, and multi-level page table walks.</p>
        </div>
        <a href="03-tlb-sandbox.html" class="lab-link">Open TLB Sandbox &rarr;</a>
      </div>
      <div class="lab-card">
        <div>
          <h3 class="lab-title">Buddy Allocator</h3>
          <p class="lab-desc">Interactive visualization of block splitting and power-of-two buddy coalescing.</p>
        </div>
        <a href="buddy-allocator-tutorial.html" class="lab-link">Open Allocator &rarr;</a>
      </div>
      <div class="lab-card">
        <div>
          <h3 class="lab-title">Multi-Level Page Tables</h3>
          <p class="lab-desc">Step through x86-64 4-level hierarchical page walks (PML4 &rarr; PDPT &rarr; PD &rarr; PT).</p>
        </div>
        <a href="multilevel-pt.html" class="lab-link">Open Hierarchy Lab &rarr;</a>
      </div>
    </div>

    <nav class="nav-bar">
      <a href="../week06-synchronization-and-deadlock/index.html" class="nav-btn">&larr; Week 6: Synchronization &amp; Deadlock</a>
      <a href="../index.html" class="nav-btn">&#127968; Course Index</a>
      <a href="../week10-file-management/index.html" class="nav-btn">Week 10: File Management &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

def execute_merge():
    # 1. Move the 4 authored modules from week07 into week09
    files_to_move = [
        "01-physical-memory-abstractions.html",
        "02-dynamic-partitioning-free-lists.html",
        "03-virtual-memory-paging-tables.html",
        "04-tlb-hardware-inverted-page-tables.html"
    ]

    for fname in files_to_move:
        src_path = os.path.join(SRC_DIR, fname)
        dest_path = os.path.join(DEST_DIR, fname)
        if os.path.exists(src_path):
            with open(src_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Harmonize internal links:
            content = content.replace("Week 7 Hub", "Week 9 Hub")
            content = content.replace('href="../week09-memory-management/index.html"', 'href="../week10-file-management/index.html"')
            content = content.replace('Week 9 Hub &rarr;', 'Week 10 Hub &rarr;')
            content = content.replace('href="../week06-synchronization-and-deadlock/index.html"', 'href="index.html"')
            content = content.replace('&larr; Week 6: Synchronization &amp; Deadlock', '&larr; Week 9 Hub')

            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"--> Transferred and harmonized {fname} into {DEST_DIR}")

    # 2. Write the comprehensive Week 9 Index
    week09_index_path = os.path.join(DEST_DIR, "index.html")
    with open(week09_index_path, "w", encoding="utf-8") as f:
        f.write(WEEK09_INDEX_CONTENT.strip() + "\n")
    print(f"--> Successfully created consolidated {week09_index_path}")

    # 3. Remove week07 directory
    if os.path.exists(SRC_DIR):
        shutil.rmtree(SRC_DIR)
        print(f"--> Removed redundant {SRC_DIR}")

    # 4. Update Week 6 links to point directly to Week 9
    week06_index_path = os.path.join("week06-synchronization-and-deadlock", "index.html")
    if os.path.exists(week06_index_path):
        with open(week06_index_path, "r", encoding="utf-8") as f:
            w6_content = f.read()
        w6_content = w6_content.replace("../week07-memory-management-virtual-memory/index.html", "../week09-memory-management/index.html")
        w6_content = w6_content.replace("Week 7 Hub &rarr;", "Week 9 Hub &rarr;")
        with open(week06_index_path, "w", encoding="utf-8") as f:
            f.write(w6_content)
        print(f"--> Updated links in {week06_index_path} to point to Week 9")

    # Also check week 6 module 04
    w6_mod04 = os.path.join("week06-synchronization-and-deadlock", "04-classic-synchronization-real-world-defenses.html")
    if os.path.exists(w6_mod04):
        with open(w6_mod04, "r", encoding="utf-8") as f:
            w6_m4_content = f.read()
        w6_m4_content = w6_m4_content.replace("../week07-memory-management-virtual-memory/index.html", "../week09-memory-management/index.html")
        w6_m4_content = w6_m4_content.replace("Week 7 &rarr;", "Week 9 &rarr;")
        with open(w6_mod04, "w", encoding="utf-8") as f:
            f.write(w6_m4_content)
        print(f"--> Updated links in {w6_mod04}")

    return True

if __name__ == "__main__":
    if execute_merge():
        try:
            subprocess.run(["git", "add", "fix.py", DEST_DIR, "week06-synchronization-and-deadlock"], check=True)
            # Remove deleted directory from git index
            subprocess.run(["git", "rm", "-r", "--ignore-unmatch", SRC_DIR], check=True)
            commit_msg = (
                "Merge Week 7 into Week 9 Memory Management and update curriculum links\n\n"
                "Consolidate modules 01-04 into week09-memory-management, update Week 9 hub\n"
                "index with full syllabus and sandboxes, and repoint Week 6 links to Week 9."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
