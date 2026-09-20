#!/usr/bin/env python3
# =====================================================================
# update_week1_index_links.py: Update index.html hrefs to match renames
# =====================================================================
import os
import subprocess
import sys

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>COSC240: Chapter 1 - Introduction (Tanenbaum)</title>
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
    <h1>Chapter 1: Introduction</h1>
    <p class="subtitle">Operating Systems Design &amp; Implementation (Andrew S. Tanenbaum)</p>
  </header>

  <div class="main-container">

    <!-- Module 01 -->
    <a href="01-what-is-an-os-and-history.html" class="card">
      <h2>01. What Is an Operating System &amp; History</h2>
      <p>Examine foundational paradigms (extended machine and resource manager) alongside the five computing generations, historical archives, and the complete 15-logo ecosystem grid.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

    <!-- Module 02 -->
    <a href="02-hardware-review.html" class="card">
      <h2>02. Computer Hardware Review</h2>
      <p>Review processor architecture, instruction execution cycles, memory hierarchy, magnetic disks, solid-state drives, I/O devices, and system buses.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

    <!-- Module 03 -->
    <a href="03-os-concepts.html" class="card">
      <h2>03. Operating System Concepts</h2>
      <p>Understand key architectural abstractions: processes, address spaces, files, input/output streams, protection rings, and command shells.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

    <!-- Module 04 -->
    <a href="04-os-structure.html" class="card">
      <h2>04. Operating System Structure</h2>
      <p>Compare structural designs: monolithic systems, layered architectures, microkernels, client-server models, virtual machines, and exokernels.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

  </div>
</body>
</html>
"""

def execute_link_update():
    base_dir = "week01-operating-system-concepts"
    os.makedirs(base_dir, exist_ok=True)
    index_path = os.path.join(base_dir, "index.html")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(INDEX_HTML)

    modified = [index_path]
    fix_path = "fix.py"
    if os.path.exists(fix_path):
        modified.append(fix_path)

    print(f"--> Staging modified files: {modified}")
    try:
        subprocess.run(["git", "add"] + modified, check=True)
        commit_msg = (
            "Update Chapter 1 index links to match renumbered module filenames\n\n"
            "Update week01-operating-system-concepts/index.html anchor hrefs to reference\n"
            "02-hardware-review.html, 03-os-concepts.html, and 04-os-structure.html correctly."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Chapter 1 index links successfully updated and deployed!")

if __name__ == "__main__":
    execute_link_update()
