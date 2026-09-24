#!/usr/bin/env python3
# =====================================================================
# fix.py: Consolidate week03-process-scheduling and generate pages
# =====================================================================
import os
import shutil
import subprocess

CANONICAL_DIR = "week03-process-scheduling"
REDUNDANT_DIR = "week03-scheduling"

COMMON_CSS = r"""
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
"""

INDEX_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 3: CPU Scheduling | Operating Systems</title>
  <style>
{COMMON_CSS}
    .module-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
      gap: 20px;
      margin-top: 24px;
    }}
    .module-card {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .module-card:hover {{
      border-color: var(--accent);
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.08);
    }}
    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }}
    .module-badge {{
      background: #e0f2fe;
      color: #0369a1;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .module-card h3 {{
      margin: 0 0 8px 0;
      font-size: 1.15rem;
      color: #0f172a;
    }}
    .module-card p {{
      font-size: 0.9rem;
      line-height: 1.55;
      margin-bottom: 16px;
      flex-grow: 1;
    }}
    .topic-list {{
      margin: 0 0 20px 0;
      padding-left: 18px;
      font-size: 0.85rem;
      color: var(--text-muted);
    }}
    .topic-list li {{
      margin-bottom: 4px;
    }}
    .btn-launch {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 8px 16px;
      background: var(--accent);
      color: #ffffff;
      text-decoration: none;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.88rem;
      transition: background-color 0.15s ease;
      align-self: flex-start;
    }}
    .btn-launch:hover {{
      background: var(--accent-hover);
    }}
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="../week02-processes/index.html">&larr; Previous: Week 2 (Processes &amp; Threads)</a>
      <a href="../index.html">&#127968; Course Index</a>
      <a href="../week04-concurrency-and-mutual-exclusion/index.html">Next: Week 4 (Concurrency) &rarr;</a>
    </nav>

    <h2>Week 3: CPU Scheduling &amp; Resource Allocation</h2>
    <p>
      An operating system allows multiple processes and execution threads to exist simultaneously, but physical hardware provides a finite number of CPU execution cores. The <strong>CPU scheduler</strong> decides which runnable task is granted processor time, for how long, and when it must be preempted. Week 3 explores the fundamental conflict between competing scheduling objectives—such as maximizing system throughput versus minimizing user response latency—and evaluates the algorithms designed to balance them.
    </p>

    <div class="module-grid">
      <!-- Module 01 -->
      <div class="module-card">
        <div>
          <div class="card-header">
            <span class="module-badge">Module 01</span>
          </div>
          <h3>01. Introduction to CPU Scheduling</h3>
          <p>
            The role of the dispatcher and scheduler. Analyzing compute-bound versus I/O-bound process behavior, scheduling trigger points, non-preemptive versus preemptive mechanisms, and conflicting optimization goals across diverse operating environments.
          </p>
          <ul class="topic-list">
            <li>Alternating CPU and I/O Burst Cycles</li>
            <li>Scheduling Trigger Invariants: Exit, Block, Ready, Interrupt</li>
            <li>Preemptive vs. Non-Preemptive Execution Modes</li>
            <li>Environment Goals: Batch, Interactive &amp; Real-Time Metrics</li>
          </ul>
        </div>
        <a class="btn-launch" href="01-scheduling-introduction.html">Open Module 01 &rarr;</a>
      </div>

      <!-- Module 02 -->
      <div class="module-card">
        <div>
          <div class="card-header">
            <span class="module-badge">Module 02</span>
          </div>
          <h3>02. Scheduling in Batch Systems</h3>
          <p>
            Evaluation of non-preemptive and baseline scheduling algorithms optimized for batch processing. Analyzing turnaround times, throughput metrics, the convoy effect, and provable optimality limits.
          </p>
          <ul class="topic-list">
            <li>First-Come, First-Served (FCFS) &amp; The Convoy Effect</li>
            <li>Shortest Job First (SJF) &amp; Provable Turnaround Optimality</li>
            <li>Shortest Remaining Time Next (SRTN) Preemption</li>
            <li>Predicting Future Bursts via Exponential Smoothing</li>
          </ul>
        </div>
        <a class="btn-launch" href="02-batch-scheduling.html">Open Module 02 &rarr;</a>
      </div>

      <!-- Module 03 -->
      <div class="module-card">
        <div>
          <div class="card-header">
            <span class="module-badge">Module 03</span>
          </div>
          <h3>03. Scheduling in Interactive Systems</h3>
          <p>
            Algorithms designed for responsive desktop and multi-user server operating systems. Exploring the quantum sizing trade-off in Round-Robin, dynamic priority adjustments, and multi-level feedback queues.
          </p>
          <ul class="topic-list">
            <li>Round-Robin (RR) &amp; Time Quantum Selection Dilemmas</li>
            <li>Priority Scheduling, Priority Inversion &amp; Starvation Aging</li>
            <li>Multi-Level Feedback Queues (MLFQ) Rules &amp; Tuning</li>
            <li>Lottery Scheduling &amp; Proportional-Share Allocations</li>
          </ul>
        </div>
        <a class="btn-launch" href="03-interactive-scheduling.html">Open Module 03 &rarr;</a>
      </div>

      <!-- Module 04 -->
      <div class="module-card">
        <div>
          <div class="card-header">
            <span class="module-badge">Module 04</span>
          </div>
          <h3>04. Real-Time &amp; Multiprocessor Scheduling</h3>
          <p>
            Scheduling under hard timing deadlines and multi-core architectures. Mathematical schedulability conditions, periodic task scheduling algorithms, symmetric multiprocessing, and cache affinity.
          </p>
          <ul class="topic-list">
            <li>Hard vs. Soft Real-Time Constraints &amp; Deadlines</li>
            <li>Rate Monotonic Scheduling (RMS) &amp; Utilization Bounds</li>
            <li>Earliest Deadline First (EDF) Dynamic Priority</li>
            <li>SMP Scheduling, Processor Affinity &amp; Gang Scheduling</li>
          </ul>
        </div>
        <a class="btn-launch" href="04-realtime-multiprocessor.html">Open Module 04 &rarr;</a>
      </div>
    </div>

    <nav class="nav-bar" style="margin-top: 36px; border-bottom: none; border-top: 1px solid var(--border); padding-top: 16px;">
      <a href="../week02-processes/index.html">&larr; Previous: Week 2 (Processes &amp; Threads)</a>
      <a href="../index.html">&#127968; Course Index</a>
      <a href="../week04-concurrency-and-mutual-exclusion/index.html">Next: Week 4 (Concurrency) &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

MODULES_DATA = [
    {
        "file": "01-scheduling-introduction.html",
        "title": "01. Introduction to CPU Scheduling",
        "prev": None,
        "next": ("02-batch-scheduling.html", "02. Batch Scheduling &rarr;"),
        "body": """
    <h2>01. Introduction to CPU Scheduling</h2>
    <p>
      In a multiprogrammed system, multiple processes reside in main memory simultaneously. When more processes are in the Ready state than there are available CPU execution cores, the operating system must decide which process to allocate to a CPU, when to switch it, and how long it should run. This decision is the responsibility of the <strong>CPU scheduler</strong>, while the low-level mechanism that switches execution context is the <strong>dispatcher</strong>.
    </p>

    <h3>1. Process Behavior: CPU vs. I/O Bursts</h3>
    <p>
      Process execution consists of a cycle of alternating <strong>CPU execution bursts</strong> (running instructions, calculations, arithmetic) and <strong>I/O wait bursts</strong> (requesting disk, network, or keyboard operations). Understanding this distribution governs effective scheduling design:
    </p>
    <ul>
      <li>
        <strong>Compute-Bound (CPU-Bound) Processes:</strong> Characterized by infrequent but prolonged CPU bursts lasting tens or hundreds of milliseconds, interspersed with brief I/O operations (e.g., scientific matrix multiplication, cryptographic hashing, 3D rendering).
      </li>
      <li>
        <strong>I/O-Bound Processes:</strong> Characterized by frequent, very short CPU bursts (e.g., 1 to 5 ms) followed by long blocking periods waiting on secondary storage or network data (e.g., interactive text editors, web browsers, database query parsers).
      </li>
    </ul>

    <h3>2. When to Schedule: Preemptive vs. Non-Preemptive</h3>
    <p>
      CPU scheduling decisions arise at four fundamental execution transition points:
    </p>
    <ol>
      <li><strong>Process Transitions from Running to Waiting:</strong> Occurs when a task invokes a blocking system call (e.g., <code>read()</code>, <code>waitpid()</code>).</li>
      <li><strong>Process Transitions from Running to Ready:</strong> Occurs when a hardware timer interrupt fires, signaling quantum expiration, or when a higher-priority task unblocks.</li>
      <li><strong>Process Transitions from Waiting to Ready:</strong> Occurs upon I/O completion or signal delivery.</li>
      <li><strong>Process Terminates:</strong> Occurs when a task calls <code>exit()</code> or encounters a fatal fault.</li>
    </ol>
    <p>
      When scheduling occurs only under circumstances 1 and 4, the scheduling discipline is <strong>non-preemptive (cooperative)</strong>. A process holds the CPU until it voluntarily releases control. When scheduling occurs across circumstances 2 and 3, the discipline is <strong>preemptive</strong>: the operating system can forcibly suspend a running task via hardware interrupts to reassign the core.
    </p>

    <h3>3. Scheduling Categories &amp; Optimization Goals</h3>
    <p>
      Different operational environments impose contradictory optimization targets on the scheduler:
    </p>
    <ul>
      <li><strong>All Systems (Fairness &amp; Policy Enforcement):</strong> Giving comparable processes comparable shares of CPU time, and ensuring stated execution policies are faithfully enforced.</li>
      <li><strong>Batch Systems:</strong>
        <ul>
          <li><em>Throughput:</em> Maximizing the number of jobs completed per unit time.</li>
          <li><em>Turnaround Time:</em> Minimizing the total elapsed duration from submission to completion.</li>
          <li><em>CPU Utilization:</em> Keeping CPU hardware execution units active 100% of the time.</li>
        </ul>
      </li>
      <li><strong>Interactive Systems:</strong>
        <ul>
          <li><em>Response Time:</em> Minimizing the latency between user input (keystroke, click) and observable system response.</li>
          <li><em>Proportionality:</em> Meeting user expectations (e.g., file saving can take 1 second, but typing must register within 16 ms).</li>
        </ul>
      </li>
      <li><strong>Real-Time Systems:</strong>
        <ul>
          <li><em>Meeting Deadlines:</em> Ensuring critical tasks complete before periodic or aperiodic time limits expire to prevent catastrophic system failure.</li>
          <li><em>Predictability:</em> Eliminating scheduling jitter and non-deterministic delays.</li>
        </ul>
      </li>
    </ul>
"""
    },
    {
        "file": "02-batch-scheduling.html",
        "title": "02. Scheduling in Batch Systems",
        "prev": ("01-scheduling-introduction.html", "&larr; 01. Intro to Scheduling"),
        "next": ("03-interactive-scheduling.html", "03. Interactive Scheduling &rarr;"),
        "body": """
    <h2>02. Scheduling in Batch Systems</h2>
    <p>
      Batch systems prioritize overall workflow efficiency and maximum computational throughput over instant interactive responsiveness. In these environments, jobs are submitted to a queue and executed without user intervention.
    </p>

    <h3>1. First-Come, First-Served (FCFS)</h3>
    <p>
      The simplest scheduling discipline: tasks are assigned the CPU strictly in the order they arrive in the ready queue (managed via a FIFO queue). FCFS is non-preemptive: once a task acquires the processor, it executes until it terminates or blocks for I/O.
    </p>
    <h4>The Convoy Effect</h4>
    <p>
      While simple and starvation-free, FCFS suffers severely from the <strong>convoy effect</strong>: if a massive compute-bound job enters the CPU ahead of several brief I/O-bound tasks, all I/O-bound tasks queue behind it. During this time, I/O devices sit idle. Once the compute job finally blocks, the short jobs execute rapidly and block on I/O, leaving the CPU idle. This results in poor average turnaround time and degraded hardware utilization.
    </p>

    <h3>2. Shortest Job First (SJF)</h3>
    <p>
      When job running times are known in advance, <strong>Shortest Job First (SJF)</strong> chooses the ready process with the smallest CPU burst time.
    </p>
    <p>
      <strong>Provable Optimality:</strong> SJF is mathematically optimal in minimizing average turnaround time for non-preemptive batch scheduling when all jobs arrive simultaneously.
    </p>

    <h3>3. Shortest Remaining Time Next (SRTN)</h3>
    <p>
      The preemptive variant of Shortest Job First. When a new job arrives in the ready queue, its expected burst time is compared against the remaining execution time of the currently running job:
    </p>
    <ul>
      <li>If the new job requires less time to finish than the current job has remaining, the current job is preempted and returned to the ready queue.</li>
      <li>SRTN provides even lower average turnaround times than non-preemptive SJF, but introduces the risk of <strong>starvation</strong> for long-running compute jobs if short tasks arrive continuously.</li>
    </ul>

    <h3>4. Predicting Future Burst Times: Exponential Smoothing</h3>
    <p>
      In general-purpose systems, future CPU burst durations cannot be known in advance. The operating system estimates the next burst length by calculating an exponential moving average of past behavior:
    </p>
    <pre><code>tau_{n+1} = alpha * t_n + (1 - alpha) * tau_n</code></pre>
    <p>
      Here, <code>t_n</code> is the length of the most recent actual burst, <code>tau_n</code> is the past predicted value, and <code>alpha</code> (typically 0.5) balances the weight of recent history against older historical trends.
    </p>
"""
    },
    {
        "file": "03-interactive-scheduling.html",
        "title": "03. Scheduling in Interactive Systems",
        "prev": ("02-batch-scheduling.html", "&larr; 02. Batch Scheduling"),
        "next": ("04-realtime-multiprocessor.html", "04. Real-Time &amp; SMP &rarr;"),
        "body": """
    <h2>03. Scheduling in Interactive Systems</h2>
    <p>
      In desktop, mobile, and interactive server environments, short response time and fair allocation of resources among multiple users and background processes are critical.
    </p>

    <h3>1. Round-Robin (RR) Scheduling</h3>
    <p>
      Round-Robin is the oldest, most reliable, and most widely used general-purpose scheduling algorithm:
    </p>
    <ul>
      <li>Each ready process is granted a fixed slice of execution time known as a <strong>time quantum</strong> (or time slice), typically between 10 ms and 100 ms.</li>
      <li>If the process is still running when the hardware timer interrupt fires, the process is preempted and moved to the tail of the FIFO ready list.</li>
    </ul>
    <h4>The Quantum Sizing Dilemma</h4>
    <ul>
      <li><strong>Quantum Too Small (e.g., 1 ms):</strong> If a context switch consumes 0.1 ms (100 microseconds), 10% of total CPU time is wasted solely on context switching overhead and cache invalidation.</li>
      <li><strong>Quantum Too Large (e.g., 500 ms):</strong> The system degenerates into FCFS; interactive tasks (such as mouse clicks or typing) stutter, producing unacceptable input latency.</li>
    </ul>

    <h3>2. Priority Scheduling &amp; Aging</h3>
    <p>
      Not all processes possess equal importance. Each task is assigned a priority integer, and the scheduler dispatches the highest-priority runnable process first:
    </p>
    <ul>
      <li><strong>Static vs. Dynamic Priorities:</strong> Static priorities remain fixed throughout process lifetime. Dynamic priorities fluctuate based on behavior—boosting I/O-bound tasks that yield quickly, and penalizing CPU-bound tasks that exhaust their quantums.</li>
      <li><strong>Starvation &amp; Aging:</strong> To prevent low-priority tasks from starving indefinitely, schedulers implement <strong>aging</strong>: gradually incrementing the priority of a process the longer it waits in the ready queue.</li>
    </ul>

    <h3>3. Multi-Level Feedback Queues (MLFQ)</h3>
    <p>
      The Multi-Level Feedback Queue is the foundational discipline of modern general-purpose schedulers. It establishes multiple distinct priority queues:
    </p>
    <ol>
      <li>Rule 1: If Priority(A) &gt; Priority(B), A runs, B does not.</li>
      <li>Rule 2: If Priority(A) == Priority(B), A &amp; B run in Round-Robin.</li>
      <li>Rule 3: When a job enters the system, it is placed at the highest priority queue.</li>
      <li>Rule 4: Once a job exhausts its time allotment at a given priority level (regardless of how many times it yielded), its priority is demoted one level down.</li>
      <li>Rule 5: After some time period S, all jobs in the system are boosted to the top queue (Periodic Priority Boost to prevent starvation and accommodate changing task phases).</li>
    </ol>
"""
    },
    {
        "file": "04-realtime-multiprocessor.html",
        "title": "04. Real-Time &amp; Multiprocessor Scheduling",
        "prev": ("03-interactive-scheduling.html", "&larr; 03. Interactive Scheduling"),
        "next": None,
        "body": """
    <h2>04. Real-Time &amp; Multiprocessor Scheduling</h2>
    <p>
      Modern systems increasingly operate under stringent timing deadlines (real-time systems) and distribute workloads across multiple physical CPU execution cores (symmetric multiprocessing).
    </p>

    <h3>1. Real-Time Systems: Hard vs. Soft</h3>
    <ul>
      <li><strong>Hard Real-Time:</strong> Missing a single deadline causes total system failure (e.g., automotive anti-lock braking, avionics flight control, pacemaker monitors).</li>
      <li><strong>Soft Real-Time:</strong> Missing occasional deadlines degrades quality of service but does not cause system collapse (e.g., video streaming frames, audio playback, online gaming physics).</li>
    </ul>

    <h3>2. Periodic Real-Time Schedulability</h3>
    <p>
      Consider a set of $m$ periodic events where event $i$ occurs with period $P_i$ and requires $C_i$ seconds of CPU computation. The system is schedulable if and only if the total processor utilization does not exceed capacity:
    </p>
    <pre><code>sum_{i=1}^{m} (C_i / P_i) &lt;= 1</code></pre>

    <h3>3. Real-Time Algorithms</h3>
    <ul>
      <li><strong>Rate Monotonic Scheduling (RMS):</strong> A static-priority assignment algorithm. Tasks with shorter periods (higher frequencies) are assigned higher static priorities. Optimal among all static-priority periodic scheduling algorithms.</li>
      <li><strong>Earliest Deadline First (EDF):</strong> A dynamic-priority assignment algorithm. The runnable task whose deadline is closest in time is granted the CPU. EDF can theoretically achieve 100% CPU utilization without missing deadlines.</li>
    </ul>

    <h3>4. Multiprocessor Scheduling (SMP)</h3>
    <p>
      When scheduling across multiple CPU cores, operating systems must manage data structures and hardware caches:
    </p>
    <ul>
      <li><strong>Single-Queue Multiprocessor Scheduling (SQMS):</strong> All CPUs pull tasks from a single shared ready queue. Suffers from lock contention on multi-core systems and lacks cache affinity.</li>
      <li><strong>Multi-Queue Multiprocessor Scheduling (MQMS):</strong> Each CPU core maintains its own independent ready queue. Provides near-linear scaling and preserves warm CPU caches, requiring occasional load balancing (work stealing).</li>
      <li><strong>Processor Affinity:</strong> Preferring to run a task on the exact same CPU core where it previously executed to maximize L1/L2 cache hit rates.</li>
      <li><strong>Gang Scheduling:</strong> Scheduling all related threads of a parallel application simultaneously across distinct physical CPU cores so they can communicate via shared memory without spinning on descheduled peers.</li>
    </ul>
"""
    }
]

def generate_module_page(mod):
    prev_link = f'<a href="{mod["prev"][0]}">{mod["prev"][1]}</a>' if mod["prev"] else '<span></span>'
    next_link = f'<a href="{mod["next"][0]}">{mod["next"][1]}</a>' if mod["next"] else '<span></span>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{mod["title"]} | Week 3: CPU Scheduling</title>
  <style>
{COMMON_CSS}
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      {prev_link}
      <a href="index.html">&#127968; Week 3 Index</a>
      {next_link}
    </nav>

{mod["body"].strip()}

    <nav class="nav-bar" style="margin-top: 36px; border-bottom: none; border-top: 1px solid var(--border); padding-top: 16px;">
      {prev_link}
      <a href="index.html">&#127968; Week 3 Index</a>
      {next_link}
    </nav>
  </div>
</body>
</html>
"""
    return html

def build_structure():
    # 1. Clean up redundant directory
    if os.path.exists(REDUNDANT_DIR):
        shutil.rmtree(REDUNDANT_DIR, ignore_errors=True)
        print(f"--> Removed redundant directory: {REDUNDANT_DIR}")

    # 2. Ensure canonical directory exists
    os.makedirs(CANONICAL_DIR, exist_ok=True)

    # 3. Write canonical index.html
    index_path = os.path.join(CANONICAL_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(INDEX_HTML.strip() + "\n")
    print(f"--> Wrote: {index_path}")

    # 4. Remove placeholder.html if present
    placeholder_path = os.path.join(CANONICAL_DIR, "placeholder.html")
    if os.path.exists(placeholder_path):
        os.remove(placeholder_path)
        print(f"--> Removed obsolete placeholder: {placeholder_path}")

    # 5. Write the 4 module HTML files
    for mod in MODULES_DATA:
        file_path = os.path.join(CANONICAL_DIR, mod["file"])
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(generate_module_page(mod).strip() + "\n")
        print(f"--> Wrote module: {file_path}")

    # 6. Stage and commit
    try:
        subprocess.run(["git", "add", "-A"], check=True)
        commit_msg = (
            "Consolidate week03-process-scheduling and generate 4-module structure\n\n"
            "Remove redundant week03-scheduling directory, update the week 3 index,\n"
            "and generate foundational structured pages for all four scheduling modules."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    build_structure()
