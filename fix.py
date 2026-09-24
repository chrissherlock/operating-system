#!/usr/bin/env python3
# =====================================================================
# fix.py: Update course materials index at repo root (index.html)
# =====================================================================
import os
import subprocess

TARGET_FILE = "index.html"

COURSE_INDEX_HTML = r"""<!DOCTYPE html>
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
      max-width: 980px;
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
      font-size: 1.85rem;
      color: #0f172a;
      margin: 0 0 6px 0;
    }
    .subtitle {
      font-size: 0.98rem;
      color: var(--text-muted);
      margin: 0;
    }
    .badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .badge-success { background: #dcfce7; color: #166534; }
    .badge-accent { background: #e0f2fe; color: #0369a1; }

    .curriculum-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 20px;
      margin-top: 24px;
    }
    .week-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .week-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 12px rgba(0,0,0,0.06);
    }
    .week-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }
    .week-title {
      font-size: 1.15rem;
      font-weight: 700;
      color: #0f172a;
      margin: 0 0 6px 0;
    }
    .week-desc {
      font-size: 0.88rem;
      color: var(--text-muted);
      margin-bottom: 16px;
      line-height: 1.5;
    }
    .module-list {
      list-style: none;
      padding: 0;
      margin: 0 0 18px 0;
      font-size: 0.84rem;
    }
    .module-list li {
      margin-bottom: 8px;
      padding-left: 14px;
      position: relative;
    }
    .module-list li::before {
      content: "\2022";
      position: absolute;
      left: 0;
      color: var(--accent);
      font-weight: bold;
    }
    .module-list a {
      color: #0369a1;
      text-decoration: none;
      font-weight: 600;
    }
    .module-list a:hover {
      text-decoration: underline;
    }
    .btn-hub {
      display: block;
      text-align: center;
      padding: 8px 14px;
      background: #f1f5f9;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #0f172a;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.85rem;
      transition: all 0.15s ease;
    }
    .btn-hub:hover {
      background: #0f172a;
      color: #ffffff;
      border-color: #0f172a;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>COSC240: Operating Systems</h1>
      <p class="subtitle">Interactive Pedagogical Modules &amp; Hardware Execution Guides</p>
    </header>

    <div class="curriculum-grid">
      <!-- Week 1 -->
      <div class="week-card">
        <div>
          <div class="week-header">
            <span class="badge badge-success">Completed</span>
          </div>
          <h2 class="week-title">Week 1: Introduction to Operating Systems</h2>
          <p class="week-desc">The hardware-software interface, system call dispatch mechanisms, dual-mode protection rings, and interrupt vectors.</p>
          <ul class="module-list">
            <li><a href="week01-intro/index.html">Week 1 Overview &amp; Architecture</a></li>
            <li>Dual-Mode Protection &amp; Hardware Rings</li>
            <li>System Call Traps &amp; Context Transition</li>
          </ul>
        </div>
        <a href="week01-intro/index.html" class="btn-hub">&#127968; Open Week 1 Modules &rarr;</a>
      </div>

      <!-- Week 2 -->
      <div class="week-card">
        <div>
          <div class="week-header">
            <span class="badge badge-success">Completed</span>
          </div>
          <h2 class="week-title">Week 2: Processes &amp; Threads</h2>
          <p class="week-desc">Process address spaces, Process Control Block (PCB) anatomy, thread lifecycle models, POSIX fork/exec, and context switches.</p>
          <ul class="module-list">
            <li><a href="week02-processes/index.html">Week 2 Overview &amp; Architecture</a></li>
            <li>Process Control Blocks &amp; Linux task_struct</li>
            <li>POSIX Process Creation (fork, exec, wait)</li>
            <li>Thread Models (1:1, N:1, M:N) &amp; Race Conditions</li>
          </ul>
        </div>
        <a href="week02-processes/index.html" class="btn-hub">&#127968; Open Week 2 Modules &rarr;</a>
      </div>

      <!-- Week 3 -->
      <div class="week-card" style="border-color: var(--accent);">
        <div>
          <div class="week-header">
            <span class="badge badge-accent">Modules 01&ndash;04 Complete</span>
          </div>
          <h2 class="week-title" style="color: var(--accent);">Week 3: CPU Scheduling &amp; Resource Allocation</h2>
          <p class="week-desc">Processor burst distributions, dispatch latency, batch proofs, time-sharing feedback queues, and real-time multiprocessor systems.</p>
          <ul class="module-list">
            <li><a href="week03-process-scheduling/01-scheduling-introduction.html">01. Intro to Scheduling (CR3, Dispatch Latency)</a></li>
            <li><a href="week03-process-scheduling/02-batch-scheduling.html">02. Batch Scheduling (FCFS, SJF, SRTN, HRRN)</a></li>
            <li><a href="week03-process-scheduling/03-interactive-scheduling.html">03. Interactive Scheduling (RR, MLFQ, Stride)</a></li>
            <li><a href="week03-process-scheduling/04-realtime-multiprocessor.html">04. Real-Time &amp; SMP (RMS, EDF, Work Stealing)</a></li>
          </ul>
        </div>
        <a href="week03-process-scheduling/index.html" class="btn-hub" style="background: var(--accent); color: #ffffff; border-color: var(--accent);">&#127968; Open Week 3 Hub &rarr;</a>
      </div>
    </div>
  </div>
</body>
</html>
"""

def write_root_index():
    target_dir = os.path.dirname(TARGET_FILE)
    if target_dir:
        os.makedirs(target_dir, exist_ok=True)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(COURSE_INDEX_HTML.strip() + "\n")

    print(f"--> Successfully updated {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Update course index in root index.html with complete Week 3 modules\n\n"
            "Add curriculum cards and direct links for Week 3 Modules 01-04, and\n"
            "fix empty string dirname bug when resolving root index path in fix.py."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    write_root_index()
