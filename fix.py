#!/usr/bin/env python3
# =====================================================================
# update_chapter_index_portal.py: Update Chapter 1 index layout
# =====================================================================
import os
import subprocess
import sys

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>COSC240 - Chapter 1: Introduction (Tanenbaum)</title>
  <style>
    :root {
      --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      --bg: #f8fafc;
      --surface: #ffffff;
      --text: #0f172a;
      --text-muted: #64748b;
      --primary: #0284c7;
      --border: #cbd5e1;
    }
    body { font-family: var(--font-sans); background: var(--bg); color: var(--text); margin: 0; padding: 0; line-height: 1.6; display: flex; min-height: 100vh; }

    /* Sidebar Navigation */
    nav { width: 260px; background: #ffffff; border-right: 1px solid var(--border); padding: 30px 20px; display: flex; flex-direction: column; gap: 20px; flex-shrink: 0; }
    nav h2 { font-size: 1.1rem; color: #1e293b; margin-top: 0; }
    nav ul { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px; }
    nav a { color: var(--text-muted); text-decoration: none; font-size: 0.9rem; padding: 6px 10px; border-radius: 4px; transition: background 0.15s, color 0.15s; }
    nav a:hover, nav a.active { background: #e0f2fe; color: var(--primary); font-weight: 500; }

    /* Main Content Area */
    main { flex-grow: 1; padding: 40px 60px; max-width: 900px; }
    .breadcrumb { font-family: var(--font-mono); font-size: 0.85rem; color: var(--text-muted); margin-bottom: 15px; }
    .breadcrumb a { color: var(--primary); text-decoration: none; }
    .breadcrumb a:hover { text-decoration: underline; }

    h1 { font-size: 2rem; color: #0f172a; margin-top: 0; margin-bottom: 10px; }
    .subtitle { font-size: 1.1rem; color: var(--text-muted); margin-bottom: 30px; }

    .content-section { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 30px; margin-bottom: 30px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
    .content-section h2 { font-size: 1.25rem; color: #0369a1; margin-top: 0; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }

    .module-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 20px; }
    .card { background: #f8fafc; border: 1px solid var(--border); border-radius: 6px; padding: 18px; text-decoration: none; color: inherit; transition: transform 0.15s ease, border-color 0.15s ease; }
    .card:hover { transform: translateY(-2px); border-color: var(--primary); }
    .card h3 { margin: 0 0 8px 0; font-size: 1rem; color: #1e293b; }
    .card p { margin: 0; font-size: 0.85rem; color: var(--text-muted); }
  </style>
</head>
<body>

  <!-- Sidebar Navigation -->
  <nav>
    <h2>COSC240 Curriculum</h2>
    <div>
      <div style="font-size: 0.75rem; font-family: var(--font-mono); font-weight: bold; color: #64748b; text-transform: uppercase; margin-bottom: 8px;">Chapter 1</div>
      <ul>
        <li><a href="index.html" class="active">Overview &amp; Index</a></li>
        <li><a href="intro/index.html">What Is an OS &amp; History</a></li>
      </ul>
    </div>
  </nav>

  <!-- Main Content -->
  <main>
    <div class="breadcrumb">
      <a href="../index.html">COSC240 Home</a> / <a href="index.html">Chapter 1</a> / Overview
    </div>

    <h1>Chapter 1: Introduction</h1>
    <div class="subtitle">Operating Systems Design &amp; Implementation (Andrew S. Tanenbaum)</div>

    <div class="content-section">
      <h2>Curriculum Modules &amp; Core Sections</h2>
      <p>
        Explore the foundational concepts of operating systems, hardware abstractions, architectural models, and system programming interfaces following Tanenbaum's text.
      </p>

      <div class="module-grid">
        <a href="intro/index.html" class="card" style="background: #e0f2fe; border-color: #bae6fd;">
          <h3>What Is an Operating System &amp; History</h3>
          <p>The operating system as a resource manager, extended machine, and the five generations of computing.</p>
        </a>
        <div class="card">
          <h3>Computer Hardware Review</h3>
          <p>Processors, memory hierarchy, disks, I/O devices, and system buses.</p>
        </div>
        <div class="card">
          <h3>The Operating System Zoo</h3>
          <p>Mainframe, server, multiprocessor, personal computer, and real-time operating systems.</p>
        </div>
        <div class="card">
          <h3>Operating System Concepts</h3>
          <p>Processes, address spaces, files, input/output, protection, and the shell.</p>
        </div>
        <div class="card">
          <h3>System Calls</h3>
          <p>API mechanics, trap instructions, and system call execution flow.</p>
        </div>
        <div class="card">
          <h3>Operating System Structure</h3>
          <p>Monolithic, layered, microkernel, client-server, and virtual machine architectures.</p>
        </div>
        <div class="card">
          <h3>The World According to C</h3>
          <p>Overview of the C programming language in low-level systems engineering.</p>
        </div>
      </div>
    </div>
  </main>

</body>
</html>
"""

def run():
    portal_dir = "week01-operating-system-concepts"
    os.makedirs(portal_dir, exist_ok=True)
    portal_path = os.path.join(portal_dir, "index.html")

    with open(portal_path, "w", encoding="utf-8") as f:
        f.write(INDEX_HTML)

    modified = [portal_path]
    fix_path = "fix.py"
    if os.path.exists(fix_path):
        modified.append(fix_path)

    print(f"--> Staging modified files: {modified}")
    try:
        subprocess.run(["git", "add"] + modified, check=True)
        commit_msg = (
            "Update Chapter 1 index portal to standard course layout\n\n"
            "Align week01-operating-system-concepts/index.html layout with course curriculum standards\n"
            "featuring sidebar navigation, breadcrumbs, and structured module grid cards."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Chapter 1 index portal successfully deployed!")

if __name__ == "__main__":
    run()
