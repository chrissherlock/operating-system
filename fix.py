#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 1 in 01-process-model.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "01-process-model.html")

MODULE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>01. The Process Model &amp; States | Week 2: Processes &amp; Concurrency</title>
  <style>
    :root {
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }
    body {
      font-family: var(--font-sans);
      color: #1e293b;
      background: #f8fafc;
      margin: 0;
      padding: 32px 16px;
      line-height: 1.6;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    h1, h2, h3, h4 { color: #0f172a; }
    h2 { border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 28px; }
    h3 { margin-top: 20px; margin-bottom: 8px; color: #0284c7; font-size: 1.15rem; }
    h4 { margin-top: 16px; margin-bottom: 6px; color: #334155; font-size: 1.0rem; }
    p { color: #475569; margin-bottom: 12px; }
    ul, ol { margin-left: 20px; color: #475569; margin-bottom: 12px; }
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
      border-bottom: 1px solid #cbd5e1;
    }
    .nav-bar a {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      background: #ffffff;
      border: 1px solid #cbd5e1;
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
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="index.html">&#127968; Week 2 Index</a>
      <a href="02-process-lifecycle.html">Next: 02. Process Lifecycle &rarr;</a>
    </nav>

    <h2>01. The Process Model &amp; States</h2>
    <p>
      At the heart of modern operating system architecture lies the <strong>process abstraction</strong>: a software model representing a program in execution. Modern hardware frequently juggles dozens to hundreds of concurrent activities—including network listeners, background daemons, audio decoders, and user interfaces. Even when a machine possesses only a single CPU core, the operating system manages these simultaneous tasks by rapidly switching the processor among them, establishing the illusion of simultaneous execution known as <strong>pseudoparallelism</strong>.
    </p>

    <h3>1. The Conceptual Process Model</h3>
    <p>
      In this model, all runnable software is organized into a collection of sequential processes. Conceptually, every process operates with its own virtual CPU and its own private flow of control. While the physical hardware switches between tasks every few milliseconds, viewing each running program as an independent sequential process makes system behavior and concurrency far easier to reason about.
    </p>

    <h4>Distinguishing the Program from the Process</h4>
    <p>
      The distinction between a program and a process is subtle yet foundational:
    </p>
    <ul>
      <li><strong>The Program:</strong> A passive sequence of bytes stored on stable storage (such as an ELF binary or PE executable file on an SSD). It encompasses compiled instructions, static constants, and variable declarations, but performs no actions on its own.</li>
      <li><strong>The Process:</strong> An active execution context. It represents the actual execution of those instructions over time, complete with dynamic state: current program counter (PC), CPU registers, stack pointers, open file descriptors, allocated physical memory pages, and child linkages.</li>
    </ul>
    <p>
      A classic analogy makes this boundary intuitive. Consider a computer scientist baking a cake in a kitchen:
    </p>
    <ul>
      <li><strong>The Recipe:</strong> Represents the <em>program</em>—the static algorithm written down step-by-step.</li>
      <li><strong>The Ingredients:</strong> Represent the <em>input data</em>—flour, sugar, and eggs ready to be transformed.</li>
      <li><strong>The Baker:</strong> Represents the <em>processor (CPU)</em>—the active engine capable of fetching instructions and executing steps.</li>
      <li><strong>The Process:</strong> The dynamic <em>activity</em> of following the recipe, measuring ingredients, and mixing the batter over time.</li>
    </ul>
    <p>
      If an urgent interruption occurs (such as a medical emergency), the baker saves their place in the recipe, stores current measurements on a notepad (saving CPU registers and state), and shifts attention to a first-aid manual (an interrupt routine or higher-priority process). Once the emergency is resolved, the baker reloads the saved state and resumes baking exactly where they left off.
    </p>

    <h4>Multiple Instances and Shared Code</h4>
    <p>
      Running the same program multiple times produces distinct, isolated processes. If two users launch the text editor <code>vim</code> simultaneously, or if a single user opens two independent instances of a terminal shell, each execution constitutes an independent process. Each instance possesses its own unique process identifier (PID), private memory space, independent stack, and distinct file handles.
    </p>
    <p>
      Underneath, modern operating systems optimize memory usage through virtual memory mechanisms: while each process maintains private writable data and stack segments, the immutable text segment (the compiled executable machine code) can be shared among all running instances, preventing redundant allocations in physical RAM.
    </p>

    <h4>Independent Rates of Progress</h4>
    <p>
      Because the operating system dynamically schedules processes based on timer interrupts, system calls, and varying I/O completion times, programs cannot assume a constant or predictable rate of execution. A loop that counts to one million might complete in a fraction of a millisecond on one run, but take substantially longer on another run if the kernel switches CPU time to a competing process mid-loop. As a result, software must never rely on CPU idle loops for timing or synchronization; robust systems rely on kernel timers, event notifications, and formal synchronization primitives.
    </p>

    <h3>2. The Three-State Process Model</h3>
    <p>
      During its lifetime, a process transitions between distinct operational states as it competes for processor time and waits for external events:
    </p>
    <ul>
      <li><strong>Running:</strong> The process currently holds the physical CPU and is actively executing instructions. Only one process can be in this state per core at any given instant.</li>
      <li><strong>Ready:</strong> The process is fully runnable and logically willing to execute, but is temporarily suspended because the scheduler allocated the CPU to another task.</li>
      <li><strong>Blocked:</strong> The process cannot execute, even if the CPU is completely idle, because it is waiting for an external event to occur (such as keyboard input arriving, a network packet being received, or a disk block read completing).</li>
    </ul>
    <p>
      State transitions occur dynamically: a running process becomes blocked when it issues an I/O request; a blocked process transitions to ready when its awaited event completes; and a ready process transitions to running when selected by the CPU scheduler.
    </p>

    <h3>3. Modeling Multiprogramming Efficiency</h3>
    <p>
      Multiprogramming aims to maximize CPU utilization by keeping multiple processes in memory. If a compute-bound process spends only a fraction of its time executing before waiting for I/O, a uniprocessor would otherwise sit idle. We can model CPU utilization probabilistically:
    </p>
    <p>
      Let <code>p</code> represent the fraction of time a process spends waiting for I/O. If <code>n</code> independent processes reside in memory simultaneously, the probability that all <code>n</code> processes are waiting for I/O concurrently is <code>p^n</code>. Consequently, the estimated aggregate CPU utilization is expressed as:
    </p>
    <pre>CPU Utilization = 1 - p^n</pre>
    <p>
      This mathematical model demonstrates why increasing the degree of multiprogramming is vital for masking I/O latency and keeping processor cores saturated.
    </p>

    <nav class="nav-bar" style="margin-top: 36px; border-bottom: none; border-top: 1px solid #cbd5e1; padding-top: 16px;">
      <a href="index.html">&#127968; Week 2 Index</a>
      <a href="02-process-lifecycle.html">Next: 02. Process Lifecycle &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

def apply_expansion():
    os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(MODULE_HTML.strip() + "\n")

    print(f"--> Successfully expanded Section 1 in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand conceptual process model in 01-process-model.html\n\n"
            "Enrich Section 1 with detailed mechanics distinguishing programs from\n"
            "processes, resource grouping versus execution, and pseudoparallelism."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    apply_expansion()
