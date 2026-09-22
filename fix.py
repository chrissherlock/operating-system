#!/usr/bin/env python3
# =====================================================================
# fix.py: Create week02-processes/index.html matching Week 1 index structure
# =====================================================================
import os
import subprocess

TARGET_DIR = "week02-processes"
TARGET_FILE = os.path.join(TARGET_DIR, "index.html")

WEEK02_INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 2: Processes &amp; Concurrency -- COSC240</title>
  <style>
    :root {
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --text: #0f172a;
      --text-muted: #475569;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; overflow-wrap: break-word; word-break: break-word; }
    body {
      font-family: var(--font-sans);
      color: var(--text);
      background-color: var(--bg);
      margin: 0;
      padding: 32px 16px;
      line-height: 1.6;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .module-nav-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
    }
    .module-nav-bar.bottom {
      margin-top: 36px;
      margin-bottom: 0;
      padding-top: 16px;
      padding-bottom: 0;
      border-bottom: none;
      border-top: 1px solid var(--border);
    }
    .module-nav-btn {
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
      font-family: var(--font-sans);
      transition: all 0.15s ease;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }
    .module-nav-btn:hover {
      background-color: #f8fafc;
      color: var(--accent);
      border-color: var(--accent);
    }
    header {
      margin-bottom: 24px;
    }
    h1 {
      font-size: 1.8rem;
      color: var(--accent);
      margin-bottom: 8px;
    }
    p.subtitle {
      color: var(--text-muted);
      font-size: 0.95rem;
    }
    h2 {
      font-size: 1.3rem;
      color: #0369a1;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 8px;
      margin-top: 28px;
      margin-bottom: 12px;
    }
    p {
      color: var(--text-muted);
      line-height: 1.6;
      font-size: 0.95rem;
      margin-bottom: 12px;
    }
    ul, ol {
      margin-left: 20px;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 12px;
    }
    li {
      margin-bottom: 8px;
    }
    a.module-link {
      color: var(--accent);
      text-decoration: none;
      font-weight: 600;
    }
    a.module-link:hover {
      text-decoration: underline;
      color: var(--accent-hover);
    }
  </style>
</head>
<body>
  <div class="container">

    <nav class="module-nav-bar">
      <div>
        <a href="../week01-operating-system-concepts/index.html" class="module-nav-btn">&larr; Week 1: Operating System Concepts</a>
      </div>
      <div>
        <span style="font-size: 0.85rem; font-weight: 600; color: #334155;">COSC240 Operating Systems</span>
      </div>
      <div>
        <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 600;">Week 2 Index</span>
      </div>
    </nav>

    <header>
      <h1>Week 2: Processes &amp; Concurrency</h1>
      <p class="subtitle">CPU Virtualization, Limited Direct Execution, Process APIs, and Scheduling Foundations.</p>
    </header>

    <article class="module-body">
      <p>
        Welcome to Week 2 of COSC240. Following our review of computer hardware and architectural abstractions in Week 1, this week investigates how operating systems virtualize the CPU to support concurrent execution. Grounded in the pedagogical frameworks of <em>Operating Systems: Three Easy Pieces</em> (OSTEP) and Andrew Tanenbaum's <em>Modern Operating Systems</em>, these modules explore how kernels multiplex physical hardware across multiple active processes.
      </p>

      <h2>Week 2 Module Directory</h2>
      <ul>
        <li>
          <strong>01. <a href="01-limited-direct-execution.html" class="module-link">Limited Direct Execution (LDE)</a>:</strong>
          Examines how the OS runs programs directly on bare silicon while retaining absolute control via hardware traps, return-from-trap assembly routines, and timer interrupts.
        </li>
        <li>
          <strong>02. <a href="02-process-api.html" class="module-link">Process APIs &amp; Lifecycle Control</a>:</strong>
          Explores POSIX process creation primitives (<code>fork()</code>, <code>exec()</code>, <code>wait()</code>, <code>exit()</code>) and process teardown dynamics.
        </li>
        <li>
          <strong>03. <a href="03-cpu-scheduling.html" class="module-link">CPU Scheduling Metrics &amp; Algorithms</a>:</strong>
          Evaluates core performance metrics (turnaround time, response time, fairness) and classical scheduling algorithms including FIFO, SJF, STCF, and Round Robin.
        </li>
        <li>
          <strong>04. <a href="04-mlfq.html" class="module-link">Multi-Level Feedback Queues (MLFQ)</a>:</strong>
          Analyzes how production schedulers balance interactive responsiveness and batch throughput dynamically without requiring a priori job length knowledge.
        </li>
      </ul>
    </article>

    <nav class="module-nav-bar bottom">
      <div>
        <a href="../week01-operating-system-concepts/index.html" class="module-nav-btn">&larr; Week 1: Operating System Concepts</a>
      </div>
      <div>
        <span style="font-size: 0.85rem; font-weight: 600; color: #334155;">Week 2: Processes &amp; Concurrency</span>
      </div>
      <div>
        <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">Next Week &rarr;</span>
      </div>
    </nav>

  </div>
</body>
</html>
"""

def generate_week_two_index():
    os.makedirs(TARGET_DIR, exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(WEEK02_INDEX_HTML.strip() + "\n")

    print(f"--> Successfully created {TARGET_FILE} matching Week 1 index structure.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Create week02-processes/index.html matching Week 1 module index structure\n\n"
            "Establish the Week 2 landing page with standard card layout, module links,\n"
            "and OSTEP/Tanenbaum alignment."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    generate_week_two_index()
