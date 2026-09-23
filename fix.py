#!/usr/bin/env python3
# =====================================================================
# fix.py: Populate Week 2 modules covering MOS Ch 2.1-2.2 & OSTEP Ch 4
# =====================================================================
import os
import subprocess

TARGET_DIR = "week02-processes"

MODULE_1 = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>01. The Process Model &amp; States | Week 2</title>
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

    <h2>01. The Process Model &amp; States</h2>
    <p>
      Following Andrew S. Tanenbaum's <em>Modern Operating Systems</em> (Chapter 2.1) and OSTEP (Chapter 4), the most central concept in any operating system is the <strong>process</strong>: an abstraction of a running program. A process turns a single physical CPU into multiple virtual CPUs through rapid context switching, creating the illusion of pseudoparallelism.
    </p>

    <h3>The Process Model and Lifecycle</h3>
    <ul>
      <li><strong>Process vs. Program:</strong> A program is static code stored on disk, whereas a process is an active execution instance containing its own program counter, registers, stack, and address space.</li>
      <li><strong>Process Creation:</strong> Initiated via system initialization, process-creation system calls (such as UNIX <code>fork()</code>), user requests, or batch job submissions.</li>
      <li><strong>Process Termination:</strong> Occurs via normal voluntary exit, error exit, fatal hardware/software errors, or external termination by another process.</li>
    </ul>

    <h3>Three-State Process Model</h3>
    <p>
      At any given moment, a process resides in one of three fundamental execution states:
    </p>
    <ul>
      <li><strong>Running:</strong> The process currently holds the CPU and is executing instructions.</li>
      <li><strong>Ready:</strong> The process is runnable and temporarily stopped only because the scheduler allocated the CPU to another task.</li>
      <li><strong>Blocked:</strong> The process cannot run, even if the CPU is completely idle, because it is waiting for an external event (such as I/O completion).</li>
    </ul>

    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 12px; border-top: 1px solid #cbd5e1;">
      <a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&#127968; Week 2 Index</a>
      <a href="02-process-api.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">Next: 02. Process APIs &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

MODULE_2 = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>02. The Classical Thread Model | Week 2</title>
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
      <a href="01-limited-direct-execution.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&larr; Previous: 01. Process Model</a>
      <a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&#127968; Week 2 Index</a>
      <a href="03-cpu-scheduling.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">Next: 03. Scheduling &rarr;</a>
    </nav>

    <h2>02. The Classical Thread Model</h2>
    <p>
      As outlined in Tanenbaum Chapter 2.2, traditional processes group related resources together, while the <strong>thread</strong> serves as the entity scheduled for execution on the CPU.
    </p>

    <h3>Resource Grouping vs. Execution</h3>
    <ul>
      <li><strong>Shared Process Resources:</strong> Address space, global variables, open files, child processes, and signals are shared across all threads within a process.</li>
      <li><strong>Private Thread Resources:</strong> Each thread maintains its own program counter, register set, execution state, and private stack.</li>
    </ul>

    <h3>Thread Implementation Strategies</h3>
    <ul>
      <li><strong>User-Space Threads:</strong> Implemented via a run-time library. Extremely fast creation and context switching, but blocked system calls can stall the entire process unless wrappers are used.</li>
      <li><strong>Kernel-Space Threads Managed by OS:</strong> The kernel maintains thread tables. Slower to create and manage due to system call overhead, but allows other threads in the process to continue running if one triggers a page fault or blocks.</li>
    </ul>

    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 12px; border-top: 1px solid #cbd5e1;">
      <a href="01-limited-direct-execution.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&larr; Previous: 01. Process Model</a>
      <a href="03-cpu-scheduling.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">Next: 03. Scheduling &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

def build_week_modules():
    os.makedirs(TARGET_DIR, exist_ok=True)
    files = {
        "01-limited-direct-execution.html": MODULE_1,
        "02-process-api.html": MODULE_2
    }

    updated_paths = ["fix.py"]
    for filename, content in files.items():
        filepath = os.path.join(TARGET_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        updated_paths.append(filepath)
        print(f"--> Updated {filepath}")

    try:
        subprocess.run(["git", "add"] + updated_paths, check=True)
        commit_msg = (
            "Align Week 2 modules with MOS Chapter 2.1-2.2 and OSTEP Chapter 4\n\n"
            "Update week02-processes HTML modules to comprehensively cover the process\n"
            "model, process states, thread architecture, and user/kernel thread tradeoffs."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    build_week_modules()
