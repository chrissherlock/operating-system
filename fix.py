#!/usr/bin/env python3
# =====================================================================
# fix.py: Update Week 2 modules to integrate Tanenbaum architecture depth
# =====================================================================
import os
import subprocess

TARGET_DIR = "week02-processes"

MODULE_1_TANENBAUM = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>01. Limited Direct Execution &amp; Process Tables | Week 2</title>
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
    p { color: #475569; margin-bottom: 12px; }
    ul, ol { margin-left: 20px; color: #475569; margin-bottom: 12px; }
    li { margin-bottom: 4px; }
    code { font-family: var(--font-mono); background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.88rem; color: #0369a1; }
  </style>
</head>
<body>
  <div class="container">
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #cbd5e1;">
      <a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&#127968; Week 2 Index</a>
      <a href="02-process-api.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">Next: 02. Process APIs &rarr;</a>
    </nav>

    <h2>01. Limited Direct Execution &amp; Process Tables</h2>
    <p>
      While virtualization relies on running user code directly on bare silicon, architectural integrity requires strict kernel supervision. Combining OSTEP's virtualization principles with Tanenbaum's structural focus on <strong>Process Tables</strong> reveals the precise mechanics of how the operating system tracks active execution.
    </p>

    <h3>The Process Table and Interrupt Vectors</h3>
    <p>
      Every process in the system is represented by an entry in the kernel's central <strong>Process Table</strong> (containing Process Control Blocks). When a hardware interrupt or system call trap occurs:
    </p>
    <ul>
      <li><strong>The Interrupt Vector:</strong> The CPU hardware indexes into an interrupt vector table containing pointers to kernel service routines.</li>
      <li><strong>Assembly Save Routine:</strong> Low-level assembly code saves program counter registers (RIP), stack pointers (RSP), and general-purpose registers into the current process table entry.</li>
      <li><strong>Mode Switch:</strong> The CPU privilege level transitions from User Mode (Ring 3) to Kernel Mode (Ring 0).</li>
    </ul>

    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 12px; border-top: 1px solid #cbd5e1;">
      <a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&#127968; Week 2 Index</a>
      <a href="02-process-api.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">Next: 02. Process APIs &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

MODULE_2_TANENBAUM = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>02. Process APIs &amp; Hierarchical Trees | Week 2</title>
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
    p { color: #475569; margin-bottom: 12px; }
    ul, ol { margin-left: 20px; color: #475569; margin-bottom: 12px; }
    li { margin-bottom: 4px; }
    code { font-family: var(--font-mono); background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.88rem; color: #0369a1; }
  </style>
</head>
<body>
  <div class="container">
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #cbd5e1;">
      <a href="01-limited-direct-execution.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&larr; Previous: 01. LDE</a>
      <a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&#127968; Week 2 Index</a>
      <a href="03-cpu-scheduling.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">Next: 03. Scheduling &rarr;</a>
    </nav>

    <h2>02. Process APIs &amp; Hierarchical Trees</h2>
    <p>
      Examining process creation through both POSIX and Tanenbaum’s architectural lenses reveals how operating systems organize tasks into structured relationships.
    </p>

    <h3>Hierarchical Process Trees vs. Flat Object Models</h3>
    <ul>
      <li><strong>POSIX Parent-Child Trees:</strong> In UNIX and Linux, processes form an strict tree hierarchy rooted at <code>init</code> (or <code>systemd</code>). Every process has a parent PID (PPID). When a child terminates, its exit status is preserved until the parent collects it via <code>wait()</code>.</li>
      <li><strong>Windows Object Handle Model:</strong> In contrast, Windows NT employs a flat process model where processes are peer entities created via <code>CreateProcess()</code>, which returns an opaque handle with explicit security descriptors rather than relying on strict parent-child ownership trees.</li>
    </ul>

    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 12px; border-top: 1px solid #cbd5e1;">
      <a href="01-limited-direct-execution.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&larr; Previous: 01. LDE</a>
      <a href="03-cpu-scheduling.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">Next: 03. Scheduling &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

MODULE_3_TANENBAUM = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>03. CPU Scheduling &amp; Real-World Trade-offs | Week 2</title>
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
    p { color: #475569; margin-bottom: 12px; }
    ul, ol { margin-left: 20px; color: #475569; margin-bottom: 12px; }
    li { margin-bottom: 4px; }
    code { font-family: var(--font-mono); background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.88rem; color: #0369a1; }
  </style>
</head>
<body>
  <div class="container">
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #cbd5e1;">
      <a href="02-process-api.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&larr; Previous: 02. Process APIs</a>
      <a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&#127968; Week 2 Index</a>
      <a href="04-mlfq.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">Next: 04. MLFQ &rarr;</a>
    </nav>

    <h2>03. CPU Scheduling &amp; Real-World Trade-offs</h2>
    <p>
      Integrating OSTEP's evaluation metrics with Tanenbaum's structural classification highlights how schedulers must balance batch throughput against interactive responsiveness and multi-core cache affinity.
    </p>

    <h3>Scheduling Categories Across Environments</h3>
    <ul>
      <li><strong>Batch Systems:</strong> Prioritize high throughput and low turnaround time (e.g., FIFO, SJF).</li>
      <li><strong>Interactive Systems:</strong> Require guaranteed low response time and fairness via round-robin and priority scheduling.</li>
      <li><strong>Real-Time Systems:</strong> Demand strict deterministic deadlines (Hard vs. Soft real-time scheduling).</li>
    </ul>

    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 12px; border-top: 1px solid #cbd5e1;">
      <a href="02-process-api.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&larr; Previous: 02. Process APIs</a>
      <a href="04-mlfq.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">Next: 04. MLFQ &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

MODULE_4_TANENBAUM = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>04. Multi-Level Feedback Queues &amp; Adaptive Scheduling | Week 2</title>
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
    p { color: #475569; margin-bottom: 12px; }
    ul, ol { margin-left: 20px; color: #475569; margin-bottom: 12px; }
    li { margin-bottom: 4px; }
    code { font-family: var(--font-mono); background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.88rem; color: #0369a1; }
  </style>
</head>
<body>
  <div class="container">
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #cbd5e1;">
      <a href="03-cpu-scheduling.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&larr; Previous: 03. Scheduling</a>
      <a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&#127968; Week 2 Index</a>
      <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">End of Week 2</span>
    </nav>

    <h2>04. Multi-Level Feedback Queues &amp; Adaptive Scheduling</h2>
    <p>
      Multi-Level Feedback Queues successfully combine OSTEP's dynamic priority adjustments with Tanenbaum's structural emphasis on aging and starvation prevention, allowing modern operating systems to adapt to arbitrary workloads seamlessly.
    </p>

    <h3>Balancing I/O-Bound and CPU-Bound Workloads</h3>
    <ul>
      <li><strong>I/O-Bound Tasks:</strong> Frequently yield the CPU before exhausting their time slice, remaining in high-priority queues for instant responsiveness.</li>
      <li><strong>CPU-Bound Tasks:</strong> Consume their entire quantum, dropping progressively lower in priority while receiving longer time slices for efficient batch execution.</li>
    </ul>

    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 12px; border-top: 1px solid #cbd5e1;">
      <a href="03-cpu-scheduling.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&larr; Previous: 03. Scheduling</a>
      <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">End of Week 2</span>
    </nav>
  </div>
</body>
</html>
"""

def execute_updates():
    os.makedirs(TARGET_DIR, exist_ok=True)

    files = {
        "01-limited-direct-execution.html": MODULE_1_TANENBAUM,
        "02-process-api.html": MODULE_2_TANENBAUM,
        "03-cpu-scheduling.html": MODULE_3_TANENBAUM,
        "04-mlfq.html": MODULE_4_TANENBAUM
    }

    added_paths = ["fix.py"]
    for filename, content in files.items():
        filepath = os.path.join(TARGET_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        added_paths.append(filepath)
        print(f"--> Updated {filepath}")

    try:
        subprocess.run(["git", "add"] + added_paths, check=True)
        commit_msg = (
            "Enhance Week 2 modules with Tanenbaum architectural depth\n\n"
            "Expand week02-processes HTML modules to integrate Tanenbaum's structural\n"
            "insights on process tables, hierarchical process trees, and scheduling."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    execute_updates()
