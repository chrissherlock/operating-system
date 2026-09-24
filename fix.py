#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix Week 6 hub index links and author Module 04
# =====================================================================
import os
import subprocess

TARGET_DIR = "week06-synchronization-and-deadlock"

# 1. Author Module 04
MOD_04_FILE = os.path.join(TARGET_DIR, "04-classic-synchronization-real-world-defenses.html")
MOD_04_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Module 04: Classic Synchronization Problems &amp; Real-World Defenses - COSC240</title>
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
    .content-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 36px;
      margin-bottom: 28px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    h1 { margin: 0 0 12px 0; font-size: 1.85rem; color: var(--primary); letter-spacing: -0.02em; }
    h3 { font-size: 1.25rem; color: var(--primary); margin-top: 28px; border-bottom: 2px solid var(--border); padding-bottom: 8px; }
    p, li { font-size: 0.95rem; color: var(--text); }
    pre {
      background: #0f172a;
      color: #e2e8f0;
      padding: 16px;
      border-radius: 6px;
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      margin: 16px 0;
    }
    code { font-family: var(--font-mono); font-size: 0.88rem; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; color: #0f172a; }
    pre code { background: none; padding: 0; color: inherit; }
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="03-deadlock-handling-bankers-algorithm.html" class="nav-btn">&larr; Module 03</a>
      <a href="index.html" class="nav-btn">&#127968; Week 6 Hub</a>
      <a href="../week07-memory-management-virtual-memory/index.html" class="nav-btn">Week 7 Hub &rarr;</a>
    </nav>

    <div class="content-card">
      <span style="font-size: 0.75rem; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.05em;">Module 04 &bull; COSC240</span>
      <h1>Classic Synchronization Problems &amp; Real-World Defenses</h1>
      <p style="font-size: 1.05rem; color: var(--text-muted); margin-bottom: 24px;">
        Analyze classical synchronization challenges including the Dining Philosophers, Readers-Writers starvation, and database lock contention. Examine production OS kernel deadlock defenses such as Linux <code>lockdep</code> and Windows Driver Verifier.
      </p>

      <h3>1. The Dining Philosophers Problem</h3>
      <p>
        Introduced by Edsger Dijkstra, the Dining Philosophers problem models <i>N</i> concurrent processes competing for a limited set of exclusive resources (forks/chopsticks).
      </p>
      <ul>
        <li><strong>The Deadlock Hazard:</strong> If all 5 philosophers pick up their left fork simultaneously, every right fork is held by a neighbor, creating a symmetric 5-way circular wait deadlock.</li>
        <li><strong>Tanenbaum's Solution:</strong> Protect fork acquisition inside a critical region guarded by a mutex, checking philosopher states (Thinking, Hungry, Eating) and only transitioning to Eating if both neighbors are not eating.</li>
      </ul>

      <h3>2. Readers-Writers Starvation &amp; Database 2PL</h3>
      <p>
        In database management systems, multiple concurrent readers can share access to data items, but writers require exclusive access.
      </p>
      <ul>
        <li><strong>Two-Phase Locking (2PL):</strong> Guarantees serializability by dividing transactions into a growing phase (acquiring locks without releasing any) and a shrinking phase (releasing locks without acquiring new ones).</li>
        <li><strong>Deadlock Resolution:</strong> DBMS engines run background lock-manager deadlock detectors, aborting and rolling back victim transactions when circular waits occur.</li>
      </ul>

      <h3>3. Real-World Kernel Defenses: Linux lockdep &amp; Driver Verifier</h3>
      <p>
        Modern operating systems do not rely solely on prevention algorithms; they employ aggressive static and runtime diagnostic subsystems:
      </p>
      <ul>
        <li><strong>Linux <code>lockdep</code>:</strong> A runtime lock validation subsystem that tracks every lock acquisition dependency in the running kernel, building a directed graph of lock classes to warn developers instantly upon observing potential lock-order inversions.</li>
        <li><strong>Windows Driver Verifier:</strong> An OS kernel driver testing framework that stresses kernel-mode drivers by injecting resource shortages, forcing deadlock detection checks, and trapping invalid IRQL lock operations.</li>
      </ul>
    </div>

    <nav class="nav-bar">
      <a href="03-deadlock-handling-bankers-algorithm.html" class="nav-btn">&larr; Module 03</a>
      <a href="index.html" class="nav-btn">&#127968; Week 6 Hub</a>
      <a href="../week07-memory-management-virtual-memory/index.html" class="nav-btn">Week 7 Hub &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

with open(MOD_04_FILE, "w", encoding="utf-8") as f:
    f.write(MOD_04_HTML.strip() + "\n")
print(f"--> Created Module 04 at {MOD_04_FILE}")

# 2. Re-write Week 6 Hub Index with correct links
HUB_FILE = os.path.join(TARGET_DIR, "index.html")
HUB_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 6: Synchronization &amp; Deadlock - COSC240</title>
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
      <a href="../week05-io-and-disk-scheduling/index.html" class="nav-btn">&larr; Week 5: I/O &amp; Disks</a>
      <a href="../index.html" class="nav-btn">&#127968; Course Index</a>
      <a href="../week07-memory-management-virtual-memory/index.html" class="nav-btn">Week 7 Hub &rarr;</a>
    </nav>

    <div class="hero-card">
      <span class="week-tag">COSC240 &bull; Operating Systems</span>
      <h1>Week 6: Synchronization &amp; Deadlock</h1>
      <p class="lead-text">
        Now that our operating system supports true multiprocessing and preemptive scheduling, we confront the structural pathologies of concurrent execution. Expanding beyond race conditions on shared memory, we examine the systemic failure states that emerge when threads compete for scarce system resources: <strong>Deadlock</strong>, <strong>Livelock</strong>, and <strong>Starvation</strong>.
      </p>

      <div class="briefing-grid">
        <div class="briefing-box">
          <div class="briefing-title">
            <span>&#128218;</span> What You Will Learn
          </div>
          <ul class="briefing-list">
            <li>Differentiating <strong>Deadlock</strong> (permanent blockage), <strong>Livelock</strong> (active state oscillation), and <strong>Starvation</strong> (scheduling unfairness).</li>
            <li>The <strong>Four Coffman Conditions</strong> governing necessary and sufficient deadlock states.</li>
            <li>Resource Allocation Graphs (RAGs), wait-for graph reduction, and cycle detection algorithms.</li>
            <li>The four canonical handling strategies: The Ostrich Algorithm, Deadlock Prevention, Detection/Recovery, and Dijkstra's <strong>Banker's Algorithm</strong>.</li>
            <li>Classic synchronization problems: Dining Philosophers, Readers-Writers starvation, and modern kernel defenses (Linux <code>lockdep</code>).</li>
          </ul>
        </div>

        <div class="briefing-box">
          <div class="briefing-title">
            <span>&#9989;</span> What You Should Do
          </div>
          <ul class="briefing-list">
            <li>Review the Week 6 concurrency lecture recordings and guided notes.</li>
            <li>Engage with the interactive directed narrative steppers embedded in each module.</li>
            <li>Complete <strong>Theory Tutorial 06</strong> (Resource Allocation Graphs &amp; Coffman Analysis).</li>
            <li>Complete <strong>Practical Tutorial 06</strong> (Deadlock Detection &amp; POSIX Lock Ordering in C).</li>
            <li>Prepare for <strong>Quiz 3</strong> (covering Week 5 I/O / Disks and Week 6 Synchronization / Deadlock).</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Modules Section -->
    <div class="modules-heading">
      <span>&#128194;</span> Course Modules &amp; Deep-Dive Texts
    </div>

    <div class="modules-grid">
      <!-- Module 01 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 01</div>
          <h2 class="module-title">Concurrency Hazards: Livelock, Starvation &amp; PIP</h2>
          <p class="module-desc">Contrast CPU-burning livelock with blocking deadlocks, study scheduling starvation, and analyze Priority Inheritance Protocols (PIP) using the Mars Pathfinder anomaly.</p>
          <div class="module-tags">
            <span class="tag">Livelock</span>
            <span class="tag">Starvation</span>
            <span class="tag">Priority Inversion</span>
            <span class="tag">PIP Protocol</span>
          </div>
        </div>
        <a href="01-concurrency-hazards-livelock-starvation.html" class="launch-btn">Launch Module 01 &rarr;</a>
      </div>

      <!-- Module 02 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 02</div>
          <h2 class="module-title">Deadlock Characterization &amp; Coffman Conditions</h2>
          <p class="module-desc">Dissect the four necessary and sufficient Coffman conditions: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait. Construct Resource Allocation Graphs (RAGs) and execute graph cycle detection.</p>
          <div class="module-tags">
            <span class="tag">Coffman Conditions</span>
            <span class="tag">RAG Matrices</span>
            <span class="tag">Wait-For Graphs</span>
            <span class="tag">Cycle Detection</span>
          </div>
        </div>
        <a href="02-deadlock-characterization-coffman-conditions.html" class="launch-btn">Launch Module 02 &rarr;</a>
      </div>

      <!-- Module 03 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 03</div>
          <h2 class="module-title">Deadlock Handling Strategies &amp; The Banker's Algorithm</h2>
          <p class="module-desc">Evaluate the Ostrich policy, static prevention via global lock hierarchy, runtime detection with victim preemption, and Dijkstra's Banker's Algorithm for multi-unit resource allocation.</p>
          <div class="module-tags">
            <span class="tag">Banker's Algorithm</span>
            <span class="tag">Safe Sequence</span>
            <span class="tag">Deadlock Prevention</span>
            <span class="tag">Victim Selection</span>
          </div>
        </div>
        <a href="03-deadlock-handling-bankers-algorithm.html" class="launch-btn">Launch Module 03 &rarr;</a>
      </div>

      <!-- Module 04 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 04</div>
          <h2 class="module-title">Classic Synchronization Problems &amp; Real-World Defenses</h2>
          <p class="module-desc">Analyze the Dining Philosophers, Readers-Writers starvation, and Sleeping Barber challenges. Investigate production OS deadlock defenses, including Linux <code>lockdep</code> validation and Windows Driver Verifier.</p>
          <div class="module-tags">
            <span class="tag">Dining Philosophers</span>
            <span class="tag">Readers-Writers</span>
            <span class="tag">Linux lockdep</span>
            <span class="tag">Static Analysis</span>
          </div>
        </div>
        <a href="04-classic-synchronization-real-world-defenses.html" class="launch-btn">Launch Module 04 &rarr;</a>
      </div>
    </div>

    <!-- Interactive Sandboxes -->
    <div class="modules-heading">
      <span>&#128302;</span> Interactive Visualizers &amp; Simulation Laboratories
    </div>

    <div class="lab-grid">
      <div class="lab-card">
        <div>
          <h3 class="lab-title">Deadlock Detector</h3>
          <p class="lab-desc">Interactive graph cycle detection sandbox for Resource Allocation Graphs.</p>
        </div>
        <a href="deadlock-detector.html" class="lab-link">Open Detector &rarr;</a>
      </div>
      <div class="lab-card">
        <div>
          <h3 class="lab-title">Dining Philosophers</h3>
          <p class="lab-desc">Simulate concurrent resource contention, deadlocks, and asymmetric fork solutions.</p>
        </div>
        <a href="dining-philosophers.html" class="lab-link">Open Simulation &rarr;</a>
      </div>
      <div class="lab-card">
        <div>
          <h3 class="lab-title">Database Deadlock</h3>
          <p class="lab-desc">Trace lock contention, two-phase locking (2PL), and transaction abort/rollback.</p>
        </div>
        <a href="database-deadlock.html" class="lab-link">Open Database 2PL &rarr;</a>
      </div>
      <div class="lab-card">
        <div>
          <h3 class="lab-title">IPC Deadlock</h3>
          <p class="lab-desc">Explore synchronous rendezvous message queues and circular wait deadlocks.</p>
        </div>
        <a href="ipc-deadlock.html" class="lab-link">Open IPC Lab &rarr;</a>
      </div>
    </div>

    <nav class="nav-bar">
      <a href="../week05-io-and-disk-scheduling/index.html" class="nav-btn">&larr; Week 5: I/O &amp; Disks</a>
      <a href="../index.html" class="nav-btn">&#127968; Course Index</a>
      <a href="../week07-memory-management-virtual-memory/index.html" class="nav-btn">Week 7 Hub &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

with open(HUB_FILE, "w", encoding="utf-8") as f:
    f.write(HUB_HTML.strip() + "\n")
print(f"--> Successfully updated Week 6 Hub at {HUB_FILE}")

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_DIR], check=True)
        status = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
        if not status:
            print("--> Working tree is clean. Nothing to commit.")
            return

        commit_msg = (
            "Fix Week 6 hub module links and create missing Module 04\n\n"
            "Correct hyperlink paths in the Week 6 hub index and author Module 04\n"
            "on classic synchronization problems and kernel deadlock defenses."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    run_git_sync()
