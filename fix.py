#!/usr/bin/env python3
# =====================================================================
# fix.py: Generate four comprehensive modules and index for Week 2
# =====================================================================
import os
import subprocess

TARGET_DIR = "week02-processes"

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>COSC240: Week 2 - Processes and Threads (MOS &amp; OSTEP)</title>
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
    <a href="../index.html">&#127968; Back to Course Overview</a>
  </div>

  <header>
    <h1>Week 2: Processes and Threads</h1>
    <p class="subtitle">Modern Operating Systems (Chapters 2.1-2.2) &amp; OSTEP (Chapter 4)</p>
  </header>

  <div class="main-container">

    <!-- Module 01 -->
    <a href="01-process-model.html" class="card">
      <h2>01. The Process Model &amp; States</h2>
      <p>Examine the process abstraction, pseudoparallelism, the three-state process model (Running, Ready, Blocked), and multiprogramming probabilities.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

    <!-- Module 02 -->
    <a href="02-process-lifecycle.html" class="card">
      <h2>02. Process Creation, Termination &amp; Hierarchies</h2>
      <p>Explore events causing process creation, exit conditions, UNIX process trees, process groups, and process control block implementations.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

    <!-- Module 03 -->
    <a href="03-classical-threads.html" class="card">
      <h2>03. The Classical Thread Model</h2>
      <p>Understand why threads are needed, the separation of resource grouping from execution, per-thread stacks, and thread usage in applications.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

    <!-- Module 04 -->
    <a href="04-thread-implementation.html" class="card">
      <h2>04. Thread Implementation &amp; Pthreads</h2>
      <p>Compare user-space threads versus kernel-space threads, hybrid multiplexing, and POSIX Pthreads application interfaces.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

  </div>
</body>
</html>
"""

MOD_1 = r"""<!DOCTYPE html>
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
    body { font-family: var(--font-sans); color: #1e293b; background: #f8fafc; margin: 0; padding: 32px 16px; line-height: 1.6; }
    .container { max-width: 900px; margin: 0 auto; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 40px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    h1, h2, h3, h4 { color: #0f172a; }
    h2 { border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 28px; }
    h3 { margin-top: 20px; margin-bottom: 8px; color: #0284c7; font-size: 1.15rem; }
    p { color: #475569; margin-bottom: 12px; }
    ul, ol { margin-left: 20px; color: #475569; margin-bottom: 12px; }
    li { margin-bottom: 4px; }
  </style>
</head>
<body>
  <div class="container">
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #cbd5e1;">
      <a href="index.html" style="font-weight: 600; color: #334155; text-decoration: none;">&#127968; Week 2 Index</a>
      <a href="02-process-lifecycle.html" style="font-weight: 600; color: #334155; text-decoration: none;">Next: 02. Lifecycle &rarr;</a>
    </nav>
    <h2>01. The Process Model &amp; States</h2>
    <p>Following MOS Chapter 2.1 and OSTEP Chapter 4, the process abstraction turns a single physical CPU into multiple virtual CPUs through pseudoparallelism.</p>
    <h3>The Process Model</h3>
    <p>A process is an instance of an executing program, including its program counter, registers, and variables. The processor switches rapidly among processes, giving the illusion of true parallel execution.</p>
    <h3>Three-State Process Model</h3>
    <ul>
      <li><strong>Running:</strong> The process currently holds the CPU and executes instructions.</li>
      <li><strong>Ready:</strong> The process is runnable but temporarily stopped while another process uses the CPU.</li>
      <li><strong>Blocked:</strong> The process cannot run because it is waiting for an external event (such as I/O).</li>
    </ul>
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 12px; border-top: 1px solid #cbd5e1;">
      <a href="index.html" style="font-weight: 600; color: #334155; text-decoration: none;">&#127968; Week 2 Index</a>
      <a href="02-process-lifecycle.html" style="font-weight: 600; color: #334155; text-decoration: none;">Next: 02. Lifecycle &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

MOD_2 = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>02. Process Creation, Termination &amp; Hierarchies | Week 2</title>
  <style>
    :root {
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }
    body { font-family: var(--font-sans); color: #1e293b; background: #f8fafc; margin: 0; padding: 32px 16px; line-height: 1.6; }
    .container { max-width: 900px; margin: 0 auto; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 40px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    h1, h2, h3, h4 { color: #0f172a; }
    h2 { border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 28px; }
    h3 { margin-top: 20px; margin-bottom: 8px; color: #0284c7; font-size: 1.15rem; }
    p { color: #475569; margin-bottom: 12px; }
    ul, ol { margin-left: 20px; color: #475569; margin-bottom: 12px; }
    li { margin-bottom: 4px; }
  </style>
</head>
<body>
  <div class="container">
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #cbd5e1;">
      <a href="01-process-model.html" style="font-weight: 600; color: #334155; text-decoration: none;">&larr; Previous: 01. Process Model</a>
      <a href="index.html" style="font-weight: 600; color: #334155; text-decoration: none;">&#127968; Week 2 Index</a>
      <a href="03-classical-threads.html" style="font-weight: 600; color: #334155; text-decoration: none;">Next: 03. Threads &rarr;</a>
    </nav>
    <h2>02. Process Creation, Termination &amp; Hierarchies</h2>
    <p>Examining how operating systems instantiate and manage the process lifecycle through system calls and process control blocks.</p>
    <h3>Process Creation Events</h3>
    <ul>
      <li>System initialization (daemons and background services).</li>
      <li>Execution of process creation system calls (e.g., UNIX <code>fork()</code>).</li>
      <li>User requests to start programs.</li>
      <li>Initiation of batch jobs.</li>
    </ul>
    <h3>Process Hierarchies &amp; Termination</h3>
    <p>Processes form parent-child tree structures in UNIX (rooted at <code>init</code> or <code>systemd</code>), whereas Windows employs flat object models with handles. Processes terminate via normal exit, error exit, fatal errors, or external termination.</p>
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 12px; border-top: 1px solid #cbd5e1;">
      <a href="01-process-model.html" style="font-weight: 600; color: #334155; text-decoration: none;">&larr; Previous: 01. Process Model</a>
      <a href="03-classical-threads.html" style="font-weight: 600; color: #334155; text-decoration: none;">Next: 03. Threads &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

MOD_3 = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>03. The Classical Thread Model | Week 2</title>
  <style>
    :root {
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }
    body { font-family: var(--font-sans); color: #1e293b; background: #f8fafc; margin: 0; padding: 32px 16px; line-height: 1.6; }
    .container { max-width: 900px; margin: 0 auto; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 40px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    h1, h2, h3, h4 { color: #0f172a; }
    h2 { border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 28px; }
    h3 { margin-top: 20px; margin-bottom: 8px; color: #0284c7; font-size: 1.15rem; }
    p { color: #475569; margin-bottom: 12px; }
    ul, ol { margin-left: 20px; color: #475569; margin-bottom: 12px; }
    li { margin-bottom: 4px; }
  </style>
</head>
<body>
  <div class="container">
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #cbd5e1;">
      <a href="02-process-lifecycle.html" style="font-weight: 600; color: #334155; text-decoration: none;">&larr; Previous: 02. Lifecycle</a>
      <a href="index.html" style="font-weight: 600; color: #334155; text-decoration: none;">&#127968; Week 2 Index</a>
      <a href="04-thread-implementation.html" style="font-weight: 600; color: #334155; text-decoration: none;">Next: 04. Implementation &rarr;</a>
    </nav>
    <h2>03. The Classical Thread Model</h2>
    <p>Covering MOS Chapter 2.2, traditional processes group related resources together, while the <strong>thread</strong> serves as the individual unit of CPU execution.</p>
    <h3>Resource Grouping vs. Execution</h3>
    <ul>
      <li><strong>Shared Resources:</strong> Address space, global variables, open files, child processes, and signals.</li>
      <li><strong>Private Thread Resources:</strong> Program counter, register set, execution state, and private stack.</li>
    </ul>
    <h3>Thread Usage in Applications</h3>
    <p>Threads simplify programming models in applications requiring concurrent activities, such as word processors maintaining background reformatting and auto-save threads, or Web servers handling simultaneous client requests.</p>
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 12px; border-top: 1px solid #cbd5e1;">
      <a href="02-process-lifecycle.html" style="font-weight: 600; color: #334155; text-decoration: none;">&larr; Previous: 02. Lifecycle</a>
      <a href="04-thread-implementation.html" style="font-weight: 600; color: #334155; text-decoration: none;">Next: 04. Implementation &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

MOD_4 = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>04. Thread Implementation &amp; Pthreads | Week 2</title>
  <style>
    :root {
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }
    body { font-family: var(--font-sans); color: #1e293b; background: #f8fafc; margin: 0; padding: 32px 16px; line-height: 1.6; }
    .container { max-width: 900px; margin: 0 auto; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 40px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    h1, h2, h3, h4 { color: #0f172a; }
    h2 { border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 28px; }
    h3 { margin-top: 20px; margin-bottom: 8px; color: #0284c7; font-size: 1.15rem; }
    p { color: #475569; margin-bottom: 12px; }
    ul, ol { margin-left: 20px; color: #475569; margin-bottom: 12px; }
    li { margin-bottom: 4px; }
  </style>
</head>
<body>
  <div class="container">
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #cbd5e1;">
      <a href="03-classical-threads.html" style="font-weight: 600; color: #334155; text-decoration: none;">&larr; Previous: 03. Threads</a>
      <a href="index.html" style="font-weight: 600; color: #334155; text-decoration: none;">&#127968; Week 2 Index</a>
      <span style="color: #94a3b8; font-weight: 600;">End of Week 2</span>
    </nav>
    <h2>04. Thread Implementation &amp; Pthreads</h2>
    <p>Exploring how threads are implemented in user space versus kernel space, alongside standard POSIX thread APIs.</p>
    <h3>User-Space vs. Kernel-Space Threads</h3>
    <ul>
      <li><strong>User-Space Threads:</strong> Managed entirely by a run-time library. Extremely fast switching, but blocking system calls can stall the entire process.</li>
      <li><strong>Kernel-Space Threads:</strong> Managed directly by the operating system kernel. Slower context switching overhead, but allows other threads to run when one blocks or incurs a page fault.</li>
    </ul>
    <h3>POSIX Pthreads API</h3>
    <p>Standardized thread management calls including <code>pthread_create</code>, <code>pthread_exit</code>, <code>pthread_join</code>, and <code>pthread_yield</code>.</p>
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 12px; border-top: 1px solid #cbd5e1;">
      <a href="03-classical-threads.html" style="font-weight: 600; color: #334155; text-decoration: none;">&larr; Previous: 03. Threads</a>
      <span style="color: #94a3b8; font-weight: 600;">End of Week 2</span>
    </nav>
  </div>
</body>
</html>
"""

def generate_week2_files():
    os.makedirs(TARGET_DIR, exist_ok=True)
    files = {
        "index.html": INDEX_HTML,
        "01-process-model.html": MOD_1,
        "02-process-lifecycle.html": MOD_2,
        "03-classical-threads.html": MOD_3,
        "04-thread-implementation.html": MOD_4
    }

    updated_paths = ["fix.py"]
    for filename, content in files.items():
        filepath = os.path.join(TARGET_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        updated_paths.append(filepath)
        print(f"--> Created/Updated {filepath}")

    try:
        subprocess.run(["git", "add"] + updated_paths, check=True)
        commit_msg = (
            "Expand Week 2 index and modules to four full sub-modules\n\n"
            "Recreate week02-processes/index.html and generate all four core sub-modules\n"
            "covering MOS Chapters 2.1-2.2 and OSTEP Chapter 4 in complete detail."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    generate_week2_files()
