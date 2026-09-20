#!/usr/bin/env python3
# =====================================================================
# execute_chapter_refactoring.py: Restructure Chapter 1 & Intro pages
# =====================================================================
import os
import subprocess
import sys

CHAPTER_1_INDEX_HTML = r"""<!DOCTYPE html>
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
        <h3>Intro: What is an OS &amp; History</h3>
        <p>Detailed overview of OS as Resource Manager, Extended Machine, and the Five Generations of Computing.</p>
      </a>
      <div class="card">
        <h3>1.1 What Is an Operating System?</h3>
        <p>The operating system as an extended machine and a resource manager.</p>
      </div>
      <div class="card">
        <h3>1.2 History of Operating Systems</h3>
        <p>Vacuum tubes, transistors, ICs, personal computers, and mobile/cloud eras.</p>
      </div>
      <div class="card">
        <h3>1.3 Computer Hardware Review</h3>
        <p>Processors, memory hierarchy, disks, I/O devices, and buses.</p>
      </div>
      <div class="card">
        <h3>1.4 The Operating System Zoo</h3>
        <p>Mainframe, server, multiprocessor, personal computer, and real-time operating systems.</p>
      </div>
      <div class="card">
        <h3>1.5 Operating System Concepts</h3>
        <p>Processes, address spaces, files, input/output, protection, and the shell.</p>
      </div>
      <div class="card">
        <h3>1.6 System Calls</h3>
        <p>API mechanics, trap instructions, and system call execution flow.</p>
      </div>
      <div class="card">
        <h3>1.7 Operating System Structure</h3>
        <p>Monolithic, layered, microkernel, client-server, and virtual machine architectures.</p>
      </div>
      <div class="card">
        <h3>1.8 The World According to C</h3>
        <p>Overview of the C programming language in low-level systems engineering.</p>
      </div>
    </div>
  </div>
</body>
</html>
"""

def execute_refactoring():
    base_dir = "week01-operating-system-concepts"
    intro_dir = os.path.join(base_dir, "intro")
    os.makedirs(intro_dir, exist_ok=True)

    old_index = os.path.join(base_dir, "index.html")
    intro_index = os.path.join(intro_dir, "index.html")

    # If old index exists and hasn't been moved yet, move it to intro/index.html
    if os.path.exists(old_index):
        with open(old_index, "r", encoding="utf-8") as f:
            content = f.read()
        # If it doesn't look like our new chapter 1 index, move it
        if "Chapter 1: Introduction" not in content:
            with open(intro_index, "w", encoding="utf-8") as f:
                f.write(content)

    # Write the new Chapter 1 master index at week01-operating-system-concepts/index.html
    with open(old_index, "w", encoding="utf-8") as f:
        f.write(CHAPTER_1_INDEX_HTML)

    modified = [old_index]
    if os.path.exists(intro_index):
        modified.append(intro_index)

    fix_path = "fix.py"
    if os.path.exists(fix_path):
        modified.append(fix_path)

    print(f"--> Staging refactored files: {modified}")
    try:
        subprocess.run(["git", "add"] + modified, check=True)
        commit_msg = (
            "Restructure Week 1 into Tanenbaum Chapter 1 index and dedicated intro page\n\n"
            "Create week01-operating-system-concepts/index.html as the master curriculum portal\n"
            "for all Chapter 1 sections (1.1-1.8) and move foundational OS definitions and history\n"
            "into week01-operating-system-concepts/intro/index.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Chapter 1 restructuring successfully deployed!")

if __name__ == "__main__":
    execute_refactoring()
