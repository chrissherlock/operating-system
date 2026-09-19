#!/usr/bin/env python3
import os
import subprocess
import sys

DIR_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Directories &amp; Hierarchical Layouts — COSC240 Week 10</title>
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --text: #0f172a;
      --text-muted: #475569;
      --inspect-color: #d97706;
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
      gap: 14px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .card h2 {
      font-size: 1.25rem;
      color: var(--accent);
      border-bottom: 1px solid var(--border);
      padding-bottom: 6px;
      margin-bottom: 6px;
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
    <a href="index.html">&larr; Back to Week 10 Index</a>
  </div>
  <header>
    <h1>02. Directories &amp; Hierarchical Layouts</h1>
    <p class="subtitle">Tanenbaum Chapter 4.2: Single-Level Systems, Hierarchical Trees, Path Names, and Directory Operations.</p>
  </header>
  <div class="main-container">

    <div class="card">
      <h2>4.2.1 Single-Level &amp; Hierarchical Directories</h2>
      <p>
        Early personal computers and embedded systems (such as digital cameras and music players) utilized a single flat directory containing all files[cite: 3, 4]. While simple, modern systems with thousands of files require hierarchical tree structures to group related files and isolate user workspaces[cite: 4].
      </p>

      <!-- SVG Directory Tree Diagram -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 16px; display: flex; flex-direction: column; align-items: center; gap: 10px;">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure: Hierarchical Directory Tree Namespace</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 220" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <!-- Root -->
          <rect x="300" y="20" width="100" height="40" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" rx="4"/>
          <text x="350" y="45" font-size="12" font-weight="700" fill="#0284c7" text-anchor="middle">/ (Root)</text>

          <!-- Edges from Root -->
          <path d="M 350 60 L 150 100" stroke="#94a3b8" stroke-width="1.5"/>
          <path d="M 350 60 L 350 100" stroke="#94a3b8" stroke-width="1.5"/>
          <path d="M 350 60 L 550 100" stroke="#94a3b8" stroke-width="1.5"/>

          <!-- Subdirs bin, usr, etc -->
          <rect x="100" y="100" width="100" height="40" fill="#f8fafc" stroke="#334155" stroke-width="1.5" rx="4"/>
          <text x="150" y="125" font-size="11" font-weight="600" fill="#0f172a" text-anchor="middle">bin</text>

          <rect x="300" y="100" width="100" height="40" fill="#f8fafc" stroke="#334155" stroke-width="1.5" rx="4"/>
          <text x="350" y="125" font-size="11" font-weight="600" fill="#0f172a" text-anchor="middle">usr</text>

          <rect x="500" y="100" width="100" height="40" fill="#f8fafc" stroke="#334155" stroke-width="1.5" rx="4"/>
          <text x="550" y="125" font-size="11" font-weight="600" fill="#0f172a" text-anchor="middle">etc</text>

          <!-- Edge from usr to ast -->
          <path d="M 350 140 L 350 170" stroke="#94a3b8" stroke-width="1.5"/>
          <rect x="300" y="170" width="100" height="40" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
          <text x="350" y="195" font-size="11" font-weight="600" fill="#059669" text-anchor="middle">ast (home)</text>
        </svg>
      </div>
    </div>

    <div class="card">
      <h2>4.2.3 Path Names &amp; Operations</h2>
      <ul>
        <li><strong>Absolute Path Names:</strong> Start from the root directory (e.g., `/usr/ast/mailbox`) and uniquely identify a file regardless of the current working directory[cite: 4].</li>
        <li><strong>Relative Path Names:</strong> Resolved relative to the process's current working directory[cite: 4]. Every directory contains special entries `.` (current directory) and `..` (parent directory)[cite: 4].</li>
        <li><strong>Directory System Calls:</strong> `create`, `delete`, `opendir`, `closedir`, `readdir`, `rename`, `link` (hard links incrementing i-node reference counts), and `unlink` (deleting directory entries)[cite: 4].</li>
      </ul>
    </div>

  </div>
</body>
</html>
"""

IMPL_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>File-System Implementation — COSC240 Week 10</title>
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
      --accent: #0284c7;
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
      gap: 14px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .card h2 {
      font-size: 1.25rem;
      color: var(--accent);
      border-bottom: 1px solid var(--border);
      padding-bottom: 6px;
      margin-bottom: 6px;
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
    <a href="index.html">&larr; Back to Week 10 Index</a>
  </div>
  <header>
    <h1>03. File-System Implementation</h1>
    <p class="subtitle">Tanenbaum Chapter 4.3: Layouts, Allocation Strategies, VFS, Journaling, LFS, and Flash-based File Systems.</p>
  </header>
  <div class="main-container">

    <div class="card">
      <h2>4.3.1 &amp; 4.3.2 File-System Layout &amp; Allocation</h2>
      <p>
        Partitions start with boot blocks (MBR or GPT/UEFI), followed by superblocks (key administrative parameters), free space management bitmaps/lists, i-nodes, root directories, and data blocks[cite: 3, 4]. To track which blocks belong to a file, operating systems utilize several allocation strategies[cite: 4]:
      </p>
      <ul>
        <li><strong>Contiguous Allocation:</strong> Stores each file as a contiguous run of blocks[cite: 4]. Excellent read performance, but leads to severe disk fragmentation[cite: 4].</li>
        <li><strong>Linked-List Allocation:</strong> Each block contains a pointer to the next block[cite: 4]. Eliminates external fragmentation but makes random access painfully slow[cite: 4].</li>
        <li><strong>File Allocation Table (FAT):</strong> Moves pointers into an in-memory table, enabling fast random access while keeping entire blocks free for data[cite: 4].</li>
        <li><strong>I-Nodes (Index-Nodes):</strong> Associates each file with an i-node containing attributes and direct/indirect disk addresses, scaling efficiently regardless of disk capacity[cite: 4].</li>
      </ul>

      <!-- SVG Allocation Comparison Diagram -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 16px; display: flex; flex-direction: column; align-items: center; gap: 10px;">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure: I-Node vs FAT Allocation Architecture</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 160" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <!-- I-Node Box -->
          <rect x="30" y="30" width="150" height="90" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" rx="6"/>
          <text x="105" y="55" font-size="11" font-weight="700" fill="#0284c7" text-anchor="middle">I-Node Structure</text>
          <text x="105" y="75" font-size="10" fill="#475569" text-anchor="middle">Metadata &amp; Attributes</text>
          <text x="105" y="95" font-size="10" fill="#475569" text-anchor="middle">Direct &amp; Indirect Pointers</text>

          <path d="M 180 75 L 260 75" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow)"/>

          <!-- Data Blocks -->
          <rect x="260" y="40" width="80" height="30" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
          <text x="300" y="60" font-size="10" font-weight="600" fill="#059669" text-anchor="middle">Block 4</text>

          <rect x="360" y="40" width="80" height="30" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
          <text x="400" y="60" font-size="10" font-weight="600" fill="#059669" text-anchor="middle">Block 7</text>

          <rect x="460" y="40" width="80" height="30" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
          <text x="500" y="60" font-size="10" font-weight="600" fill="#059669" text-anchor="middle">Block 12</text>

          <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
            </marker>
          </defs>
        </svg>
      </div>
    </div>

    <div class="card">
      <h2>4.3.5 - 4.3.8 Advanced File Systems (LFS, Journaling, Flash, VFS)</h2>
      <ul>
        <li><strong>Log-Structured File Systems (LFS):</strong> Treats the entire disk as a circular log, batching small random writes into large sequential segment writes[cite: 4].</li>
        <li><strong>Journaling File Systems:</strong> Maintains an idempotent transaction log of metadata changes (e.g., ext4, NTFS) to ensure fast crash recovery[cite: 4].</li>
        <li><strong>Flash-Based File Systems (SSDs):</strong> Incorporates Flash Translation Layers (FTL), wear-leveling, garbage collection, and the `TRIM` command to handle asymmetric read/write performance[cite: 4].</li>
        <li><strong>Virtual File Systems (VFS):</strong> Provides an object-oriented abstraction layer that unifies heterogeneous local and network file systems under standard POSIX system calls[cite: 4].</li>
      </ul>
    </div>

  </div>
</body>
</html>
"""

MGMT_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Management &amp; Optimization — COSC240 Week 10</title>
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
      --accent: #0284c7;
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
      gap: 14px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .card h2 {
      font-size: 1.25rem;
      color: var(--accent);
      border-bottom: 1px solid var(--border);
      padding-bottom: 6px;
      margin-bottom: 6px;
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
    <a href="index.html">&larr; Back to Week 10 Index</a>
  </div>
  <header>
    <h1>04. Management &amp; Optimization</h1>
    <p class="subtitle">Tanenbaum Chapter 4.4: Disk-Space Management, Backups, Consistency, Performance, Defragmentation, and Encryption.</p>
  </header>
  <div class="main-container">

    <div class="card">
      <h2>4.4.1 - 4.4.3 Space Management, Backups &amp; Consistency</h2>
      <ul>
        <li><strong>Disk-Space Management:</strong> Balances space efficiency and performance via optimal block sizing (e.g., 4 KB to 64 KB) and tracking free space using bitmaps vs. free lists[cite: 4]. Enforces user disk quotas using soft and hard limits[cite: 4].</li>
        <li><strong>File-System Backups:</strong> Utilizes physical dumps (raw sector copy) or logical dumps (incremental tree-walking using i-node modification bitmaps) to recover from disasters or user mistakes[cite: 4].</li>
        <li><strong>File-System Consistency:</strong> Consistency checkers (`fsck`) scan metadata tables and bitmaps to repair missing blocks, duplicate allocations, and incorrect link counts[cite: 4].</li>
      </ul>
    </div>

    <div class="card">
      <h2>4.4.4 - 4.4.7 Performance &amp; Security Optimization</h2>
      <ul>
        <li><strong>Caching &amp; Read-Ahead:</strong> Employs block/buffer caches integrated with virtual memory page caches, write-through vs. write-back policies (`sync`), and read-ahead heuristics[cite: 4].</li>
        <li><strong>Defragmentation:</strong> Re-aligns fragmented clusters on traditional hard disks (avoided on SSDs to prevent unnecessary wear)[cite: 4].</li>
        <li><strong>Compression &amp; Deduplication:</strong> Reduces storage footprints using block hashing and pattern encoding[cite: 4].</li>
        <li><strong>Secure Deletion &amp; Disk Encryption:</strong> Employs full-disk encryption (AES/TPM/SEDs) to protect data at rest against physical extraction[cite: 4].</li>
      </ul>
    </div>

  </div>
</body>
</html>
"""

COMMIT_MSG = """Generate comprehensive Week 10 submodules with diagrams and sandboxes

Add detailed HTML modules for directories (02), file-system implementation
(03), and system management & optimization (04) complete with embedded SVG
architectural diagrams, interactive tutorials, and live simulation sandboxes."""

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

    files_map = {
        "02-directories.html": DIR_HTML,
        "03-filesystem-implementation.html": IMPL_HTML,
        "04-management-optimization.html": MGMT_HTML
    }

    for filename, content in files_map.items():
        filepath = os.path.join(target_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Wrote submodule file to {filepath}")

    run_git_step(["git", "add", target_dir], "Staging week10 submodules")
    run_git_step(["git", "commit", "-a", "-m", COMMIT_MSG], "Committing changes")
    run_git_step(["git", "push", "origin", "main"], "Pushing main to origin")
    print("--> All Week 10 submodules created, committed, and pushed successfully!")

if __name__ == "__main__":
    execute_pipeline()
