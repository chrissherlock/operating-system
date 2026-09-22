#!/usr/bin/env python3
# =====================================================================
# fix.py: Create week02-processes/index.html matching Week 1 card index
# =====================================================================
import os
import subprocess

TARGET_DIR = "week02-processes"
TARGET_FILE = os.path.join(TARGET_DIR, "index.html")

WEEK02_CARD_INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>COSC240: Chapter 2 - Processes &amp; Concurrency</title>
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
      --border-dark: #94a3b8;
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --text: #0f172a;
      --text-muted: #475569;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 18px;
    }
    header { text-align: center; max-width: 900px; }
    h1 { font-size: 1.8rem; color: var(--accent); margin-bottom: 6px; }
    p.subtitle { color: var(--text-muted); font-size: 0.95rem; }
    .main-container {
      display: flex;
      flex-direction: column;
      gap: 16px;
      width: 100%;
      max-width: 1100px;
    }
    .card {
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
      transition: transform 0.15s ease, border-color 0.15s ease;
      text-decoration: none;
      color: inherit;
    }
    .card:hover {
      border-color: var(--accent);
      transform: translateY(-2px);
    }
    .card h2 {
      font-size: 1.2rem;
      color: var(--accent);
    }
    .card p {
      font-size: 0.92rem;
      color: var(--text-muted);
      line-height: 1.5;
    }
    .card .link-text {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--accent);
      margin-top: 6px;
    }
    .card:hover .link-text {
      text-decoration: underline;
    }
    .nav-back {
      width: 100%;
      max-width: 1100px;
      margin: 0 auto 6px auto;
      padding: 0 4px;
      display: flex;
    }
    .nav-back a {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      font-family: var(--font-mono);
      text-decoration: none;
      color: #0f172a;
      background-color: #ffffff;
      border: 1px solid #bae6fd;
      padding: 6px 12px;
      border-radius: 6px;
      transition: background-color 0.15s ease, color 0.15s ease;
    }
    .nav-back a:hover {
      background-color: #0f172a;
      color: #ffffff;
    }
  </style>
</head>
<body>
  <div class="nav-back">
    <a href="../index.html">&larr; Back to Course Overview</a>
  </div>

  <header>
    <h1>Chapter 2: Processes &amp; Concurrency</h1>
    <p class="subtitle">CPU Virtualization, Limited Direct Execution, Process APIs, and Scheduling Foundations</p>
  </header>

  <div class="main-container">

    <!-- Module 01 -->
    <a href="01-limited-direct-execution.html" class="card">
      <h2>01. Limited Direct Execution (LDE)</h2>
      <p>Examine how operating systems virtualize the CPU by running user code directly on bare silicon while retaining absolute control via hardware traps, return-from-trap assembly routines, and timer interrupts.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

    <!-- Module 02 -->
    <a href="02-process-api.html" class="card">
      <h2>02. Process APIs &amp; Lifecycle Control</h2>
      <p>Explore POSIX process creation primitives (<code>fork()</code>, <code>exec()</code>, <code>wait()</code>, <code>exit()</code>) alongside process tree hierarchies and teardown mechanics.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

    <!-- Module 03 -->
    <a href="03-cpu-scheduling.html" class="card">
      <h2>03. CPU Scheduling Metrics &amp; Algorithms</h2>
      <p>Evaluate core scheduling metrics (turnaround time, response time, fairness) and classical algorithms including FIFO, SJF, STCF, and Round Robin.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

    <!-- Module 04 -->
    <a href="04-mlfq.html" class="card">
      <h2>04. Multi-Level Feedback Queues (MLFQ)</h2>
      <p>Analyze how production kernels balance interactive responsiveness and batch throughput dynamically without requiring a priori job length knowledge.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

  </div>
</body>
</html>
"""

def generate_week_two_card_index():
    os.makedirs(TARGET_DIR, exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(WEEK02_CARD_INDEX_HTML.strip() + "\n")

    print(f"--> Successfully created {TARGET_FILE} following Week 1 card structure.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Create week02-processes/index.html matching Week 1 card index structure\n\n"
            "Establish the Week 2 landing page using the exact card layout, styling,\n"
            "and navigation format of week01-operating-system-concepts/index.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    generate_week_two_card_index()
