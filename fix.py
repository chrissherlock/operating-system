#!/usr/bin/env python3
# =====================================================================
# fix.py: Correct title and header in week02-processes/index.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "index.html")

CORRECTED_INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 2: Processes and Threads | COSC240</title>
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
    p { color: #475569; margin-bottom: 16px; }
    .card-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      margin-top: 24px;
    }
    .card {
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 20px;
      text-decoration: none;
      color: inherit;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    .card:hover {
      border-color: #0284c7;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .card h3 {
      margin-top: 0;
      color: #0284c7;
      font-size: 1.1rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #cbd5e1;">
      <a href="../index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&#127968; Course Index</a>
      <span style="color: #64748b; font-size: 0.85rem; font-weight: 600;">COSC240 Operating Systems</span>
    </nav>

    <h1>Week 2: Processes and Threads</h1>
    <p>
      Exploring core process abstractions, lifecycle states, process APIs, and the classical thread model, aligned with Modern Operating Systems (Chapters 2.1-2.2) and OSTEP (Chapter 4).
    </p>

    <div class="card-grid">
      <a href="01-limited-direct-execution.html" class="card">
        <h3>01. The Process Model &amp; States</h3>
        <p>Examine the process abstraction, pseudoparallelism, lifecycle events, and the three-state model (Running, Ready, Blocked).</p>
      </a>
      <a href="02-process-api.html" class="card">
        <h3>02. The Classical Thread Model</h3>
        <p>Explore resource grouping versus execution, per-thread stacks, and user-space versus kernel-space thread implementations.</p>
      </a>
    </div>
  </div>
</body>
</html>
"""

def update_index_file():
    os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(CORRECTED_INDEX_HTML.strip() + "\n")

    print(f"--> Successfully updated title and header in {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Correct title and header in week02-processes/index.html\n\n"
            "Update the page title and heading of the Week 2 landing page to accurately\n"
            "reflect Processes and Threads (MOS Chapter 2.1-2.2 and OSTEP Chapter 4)."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_index_file()
