#!/usr/bin/env python3
import os
import subprocess
import sys

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 10: File Management — COSC240</title>
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
    }
    .card:hover {
      border-color: var(--accent);
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
    .card a {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      text-decoration: none;
      color: var(--accent);
      margin-top: 6px;
    }
    .card a:hover {
      text-decoration: underline;
    }
    .nav-back {
      width: 100%;
      max-width: 1100px;
      margin: 0 auto 16px auto;
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
      color: #0284c7;
      background-color: #f0f9ff;
      border: 1px solid #bae6fd;
      padding: 6px 12px;
      border-radius: 6px;
      transition: background-color 0.15s ease, color 0.15s ease;
    }
    .nav-back a:hover {
      background-color: #0284c7;
      color: #ffffff;
    }
  </style>
</head>
<body>
  <div class="nav-back">
    <a href="../index.html">&larr; Back to Course Overview</a>
  </div>
  <header>
    <h1>Week 10: File Management</h1>
    <p class="subtitle">Tanenbaum Chapter 4: Files, Directories, Implementation, and System Optimization.</p>
  </header>

  <div class="main-container">

    <!-- Module 1 -->
    <div class="card">
      <h2>01. Files &amp; Naming Abstractions</h2>
      <p>Explore fundamental file abstractions, naming rules, structure types, sequential/random access models, attributes, and common POSIX system calls[cite: 3].</p>
      <a href="01-files-abstraction.html">Launch Module &rarr;</a>
    </div>

    <!-- Module 2 -->
    <div class="card">
      <h2>02. Directories &amp; Hierarchical Layouts</h2>
      <p>Examine single-level vs. hierarchical directory structures, absolute and relative path resolution, and directory management system calls[cite: 3].</p>
      <a href="02-directories.html">Launch Module &rarr;</a>
    </div>

    <!-- Module 3 -->
    <div class="card">
      <h2>03. File-System Implementation</h2>
      <p>Analyze disk layouts, superblock structures, allocation strategies (contiguous, FAT, i-nodes), shared links, journaling, and virtual file systems (VFS)[cite: 3].</p>
      <a href="03-filesystem-implementation.html">Launch Module &rarr;</a>
    </div>

    <!-- Module 4 -->
    <div class="card">
      <h2>04. Management &amp; Optimization</h2>
      <p>Study disk-space management, free-space bitmaps, backup policies, consistency checking (`fsck`), caching performance, and disk defragmentation[cite: 3].</p>
      <a href="04-management-optimization.html">Launch Module &rarr;</a>
    </div>

  </div>
</body>
</html>
"""

COMMIT_MSG = """Align week10 file management index with week09 modular course layout

Update generate_week10_index.py to structure week10-file-management/
index.html using the card-based submodule layout established in Week 09,
categorizing Chapter 4 into discrete interactive learning modules."""

def run_git_step(cmd, desc):
    print(f"--> {desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout.strip():
        print(res.stdout.strip())
    if res.stderr.strip():
        print(f"[{desc} stderr]\n{res.stderr.strip()}")
    if res.returncode != 0:
        print(f"Error during {desc} (code {res.returncode})", file=sys.stderr)
        sys.exit(res.returncode)

def execute_pipeline():
    target_dir = "week10-file-management"
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, "index.html")

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Wrote generated modular index page to {target_file}")

    run_git_step(["git", "add", target_file], "Staging week10 modular index file")
    run_git_step(["git", "commit", "-a", "-m", COMMIT_MSG], "Committing changes")
    run_git_step(["git", "push", "origin", "main"], "Pushing main to origin")
    print("--> Week 10 modular index page created, committed, and pushed successfully!")

if __name__ == "__main__":
    execute_pipeline()
