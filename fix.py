#!/usr/bin/env python3
# =====================================================================
# fix.py: Standardize Weeks 1, 2, and 3 hubs to match Week 4 format
# =====================================================================
import os
import subprocess

HUBS = {
    os.path.join("week01-intro", "index.html"): r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 1: Introduction to Operating Systems | COSC240</title>
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

    <h1>Week 1: Introduction to Operating Systems</h1>
    <p class="subtitle">The Hardware-Software Interface, Dual-Mode Protection, and System Calls</p>

    <div class="lead-card">
      <strong>Core Conceptual Shift:</strong> Software cannot be trusted with raw hardware access. The operating system acts as an illusionist and an arbiter: virtualizing physical devices to provide safe abstractions, while using CPU hardware privilege rings to enforce strict protection boundaries between untrusted user code and the privileged supervisor kernel.
    </div>

    <div class="module-grid">
      <!-- Module 01 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 01</div>
          <h2 class="module-title">Operating System Fundamentals</h2>
          <p class="module-desc">
            The dual role of the OS as extended machine and resource manager, kernel architectures (monolithic vs. microkernels), and the hardware boundary.
          </p>
        </div>
        <a href="01-os-fundamentals.html" class="btn-module">Open Module 01 &rarr;</a>
      </div>

      <!-- Module 02 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 02</div>
          <h2 class="module-title">Dual-Mode Operation &amp; Protection</h2>
          <p class="module-desc">
            Hardware privilege rings (Ring 0 vs. Ring 3), privileged instruction enforcement, memory protection registers, and hardware timer interrupt preemption.
          </p>
        </div>
        <a href="02-dual-mode-protection.html" class="btn-module">Open Module 02 &rarr;</a>
      </div>

      <!-- Module 03 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 03</div>
          <h2 class="module-title">System Call Mechanics &amp; Traps</h2>
          <p class="module-desc">
            The low-level anatomy of a system call, software interrupt traps (syscall/sysenter), register calling conventions, and user-to-kernel stack switching.
          </p>
        </div>
        <a href="03-system-calls.html" class="btn-module">Open Module 03 &rarr;</a>
      </div>
    </div>
  </div>
</body>
</html>
""",

    os.path.join("week02-processes", "index.html"): r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 2: Processes &amp; Threads | COSC240</title>
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
      <a href="../week01-intro/index.html">&larr; Week 1 Hub</a>
      <span style="font-size: 0.85rem; font-weight: 700; color: #64748b;">Week 2: Processes &amp; Threads</span>
      <a href="../week03-process-scheduling/index.html">Next: Week 3 Hub &rarr;</a>
    </nav>

    <h1>Week 2: Processes &amp; Threads</h1>
    <p class="subtitle">Address Space Virtualization, Process Control Blocks, and Thread Execution Models</p>

    <div class="lead-card">
      <strong>Core Conceptual Shift:</strong> The CPU executes instructions linearly, but applications require independent, concurrent environments. The OS provides the <em>Process abstraction</em>&mdash;giving each program the illusion of exclusive ownership over a dedicated CPU and a private, contiguous virtual address space&mdash;and the <em>Thread abstraction</em> for lightweight parallel execution within a shared address space.
    </div>

    <div class="module-grid">
      <!-- Module 01 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 01</div>
          <h2 class="module-title">The Process Abstraction &amp; Lifecycle</h2>
          <p class="module-desc">
            Virtual memory memory layout (text, data, heap, stack), seven-state lifecycle transitions, and the internal architecture of the Process Control Block (PCB).
          </p>
        </div>
        <a href="01-process-model.html" class="btn-module">Open Module 01 &rarr;</a>
      </div>

      <!-- Module 02 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 02</div>
          <h2 class="module-title">POSIX Process Control APIs</h2>
          <p class="module-desc">
            Deterministic process creation via fork(), image overlay through execve(), termination tracking via waitpid(), and zombie/orphan process states.
          </p>
        </div>
        <a href="02-process-creation.html" class="btn-module">Open Module 02 &rarr;</a>
      </div>

      <!-- Module 03 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 03</div>
          <h2 class="module-title">Thread Models &amp; Concurrency Basics</h2>
          <p class="module-desc">
            Threads vs. processes, 1:1 kernel threading, N:1 user-space green threads, M:N hybrid systems, Linux clone() flags, and shared heap hazards.
          </p>
        </div>
        <a href="03-thread-models.html" class="btn-module">Open Module 03 &rarr;</a>
      </div>
    </div>
  </div>
</body>
</html>
""",

    os.path.join("week03-process-scheduling", "index.html"): r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 3: CPU Scheduling &amp; Resource Allocation | COSC240</title>
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
      <a href="../week02-processes/index.html">&larr; Week 2 Hub</a>
      <span style="font-size: 0.85rem; font-weight: 700; color: #64748b;">Week 3: CPU Scheduling</span>
      <a href="../week04-concurrency/index.html">Next: Week 4 Hub &rarr;</a>
    </nav>

    <h1>Week 3: CPU Scheduling &amp; Resource Allocation</h1>
    <p class="subtitle">Burst Distributions, Dispatch Latency, Feedback Queues, and Multiprocessor Systems</p>

    <div class="lead-card">
      <strong>Core Conceptual Shift:</strong> When multiple runnable threads compete for finite hardware cores, the operating system must decide who runs, for how long, and when to forcibly intervene. Scheduling policies balance irreconcilable trade-offs: minimizing turnaround time in batch computing, guaranteeing responsive interaction on user terminals, and satisfying deterministic deadlines in real-time avionics.
    </div>

    <div class="module-grid">
      <!-- Module 01 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 01</div>
          <h2 class="module-title">Introduction to CPU Scheduling</h2>
          <p class="module-desc">
            CPU vs. I/O burst distributions, scheduler vs. dispatcher separation, CR3/PCID register switches, direct/indirect dispatch latency, and preemption triggers.
          </p>
        </div>
        <a href="01-scheduling-introduction.html" class="btn-module">Open Module 01 &rarr;</a>
      </div>

      <!-- Module 02 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 02</div>
          <h2 class="module-title">Scheduling in Batch Systems</h2>
          <p class="module-desc">
            FCFS convoy effects, SJF turnaround optimality proofs, preemptive SRTN, exponential burst smoothing (&tau;), and Highest Response Ratio Next (HRRN).
          </p>
        </div>
        <a href="02-batch-scheduling.html" class="btn-module">Open Module 02 &rarr;</a>
      </div>

      <!-- Module 03 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 03</div>
          <h2 class="module-title">Scheduling in Interactive Systems</h2>
          <p class="module-desc">
            Round-Robin quantum dilemmas, Priority Inversion and Priority Inheritance, the 5 MLFQ rules, lottery scheduling, and deterministic Stride fair-share.
          </p>
        </div>
        <a href="03-interactive-scheduling.html" class="btn-module">Open Module 03 &rarr;</a>
      </div>

      <!-- Module 04 -->
      <div class="module-card">
        <div>
          <div class="module-num">Module 04</div>
          <h2 class="module-title">Real-Time &amp; Multiprocessor Scheduling</h2>
          <p class="module-desc">
            Hard vs. soft real-time constraints, Rate-Monotonic Liu &amp; Layland bounds, Earliest Deadline First (EDF), SMP cache affinity, NUMA nodes, and work stealing.
          </p>
        </div>
        <a href="04-realtime-multiprocessor.html" class="btn-module">Open Module 04 &rarr;</a>
      </div>
    </div>
  </div>
</body>
</html>
"""
}

def standardize_all_hubs():
    updated_files = []
    for hub_path, hub_html in HUBS.items():
        os.makedirs(os.path.dirname(hub_path), exist_ok=True)
        with open(hub_path, "w", encoding="utf-8") as f:
            f.write(hub_html.strip() + "\n")
        print(f"--> Standardized hub format for: {hub_path}")
        updated_files.append(hub_path)

    try:
        subprocess.run(["git", "add", "fix.py"] + updated_files, check=True)
        commit_msg = (
            "Standardize Weeks 01-03 index hubs to match Week 04 design format\n\n"
            "Update hub pages across Weeks 1, 2, and 3 with the unified navigation\n"
            "bar, core conceptual shift lead card, and responsive module card grid."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    standardize_all_hubs()
