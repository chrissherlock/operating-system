#!/usr/bin/env python3
# =====================================================================
# update_chapter_index_clean.py: Clean up Chapter 1 index cards & numbers
# =====================================================================
import os
import subprocess
import sys

CHAPTER_1_INDEX_CLEAN_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>COSC240: Chapter 1 - Introduction (Tanenbaum)</title>
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
    body { font-family: var(--font-sans); background: var(--bg); color: var(--text); margin: 0; padding: 30px; line-height: 1.6; }
    .container { max-width: 900px; margin: 0 auto; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 40px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    h1 { font-size: 1.8rem; color: #0f172a; margin-top: 0; border-bottom: 2px solid var(--border); padding-bottom: 12px; }
    h2 { font-size: 1.2rem; color: #0369a1; margin-top: 30px; }
    p { color: var(--text-muted); }
    .section-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 20px; }
    .card { background: #f8fafc; border: 1px solid var(--border); border-radius: 6px; padding: 18px; text-decoration: none; color: inherit; transition: transform 0.15s ease, border-color 0.15s ease; }
    .card:hover { transform: translateY(-2px); border-color: var(--primary); }
    .card h3 { margin: 0 0 8px 0; font-size: 1rem; color: #1e293b; }
    .card p { margin: 0; font-size: 0.85rem; }
    .back-link { display: inline-block; margin-bottom: 20px; font-family: var(--font-mono); font-size: 0.85rem; color: var(--primary); text-decoration: none; }
    .back-link:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <div class="container">
    <a href="../index.html" class="back-link">&larr; Return to Course Curriculum Home</a>
    <h1>Chapter 1: Introduction (Tanenbaum)</h1>
    <p>
      Welcome to Chapter 1 of COSC240 Operating Systems, following Andrew S. Tanenbaum's foundational text. Below is the curriculum index covering all core sections, architectural paradigms, and system fundamentals.
    </p>

    <h2>Curriculum Modules &amp; Sections</h2>
    <div class="section-grid">
      <a href="intro/index.html" class="card" style="background: #e0f2fe; border-color: #bae6fd;">
        <h3>What Is an Operating System &amp; History</h3>
        <p>Detailed overview of the operating system as a resource manager, extended machine, and the five generations of computing.</p>
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
</body>
</html>
"""

def update_index_clean():
    portal_path = os.path.join("week01-operating-system-concepts", "index.html")
    os.makedirs("week01-operating-system-concepts", exist_ok=True)

    with open(portal_path, "w", encoding="utf-8") as f:
        f.write(CHAPTER_1_INDEX_CLEAN_HTML)

    modified = [portal_path]
    fix_path = "fix.py"
    if os.path.exists(fix_path):
        modified.append(fix_path)

    print(f"--> Staging modified files: {modified}")
    try:
        subprocess.run(["git", "add"] + modified, check=True)
        commit_msg = (
            "Remove section numbers and intro cards from Chapter 1 index portal\n\n"
            "Update week01-operating-system-concepts/index.html to remove section cards 1.1 and 1.2\n"
            "and strip numerical section prefixes from remaining Chapter 1 modules."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Chapter 1 index successfully cleaned and deployed!")

if __name__ == "__main__":
    update_index_clean()
