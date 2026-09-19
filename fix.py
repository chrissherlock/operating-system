#!/usr/bin/env python3
import os
import subprocess
import sys

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Directory Systems &amp; Hierarchies — COSC240 Week 10</title>
  <script>
    window.MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']]
      }
    };
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
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
      --inspect-color: #d97706;
      --success-color: #059669;
      --danger-color: #dc2626;
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
    h1 { font-size: 1.85rem; color: var(--accent); margin-bottom: 6px; }
    p.subtitle { color: var(--text-muted); font-size: 0.95rem; }
    .main-container {
      display: flex;
      flex-direction: column;
      gap: 18px;
      width: 100%;
      max-width: 1100px;
    }
    .card {
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 22px;
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
    .card h3 {
      font-size: 1.05rem;
      color: var(--text);
      margin-top: 8px;
      margin-bottom: 4px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
      margin-top: 8px;
      margin-bottom: 8px;
    }
    th, td {
      border: 1px solid var(--border);
      padding: 8px 12px;
      text-align: left;
    }
    th {
      background-color: #f1f5f9;
      color: var(--text);
      font-weight: 600;
    }
    td {
      color: #334155;
    }
    ul, ol {
      padding-left: 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      color: #334155;
      font-size: 0.93rem;
      line-height: 1.5;
    }
    p {
      line-height: 1.65;
      color: #334155;
      font-size: 0.94rem;
    }
    .nav-back {
      width: 100%;
      max-width: 1100px;
      margin: 0 auto 16px auto;
      padding: 0 4px;
      display: flex;
      flex-direction: column;
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
      width: fit-content;
    }
    .nav-back a:hover {
      background-color: #0284c7;
      color: #ffffff;
    }

    .figure-container {
      width: 100%;
      margin: 10px auto;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      overflow-x: auto;
    }

    .callout {
      background-color: #f0f9ff;
      border-left: 4px solid var(--accent);
      padding: 12px 16px;
      border-radius: 0 6px 6px 0;
      font-size: 0.9rem;
      color: #0369a1;
      line-height: 1.5;
      margin-top: 4px;
      margin-bottom: 4px;
    }

    /* Sandbox Styles */
    .kernel-sandbox {
      background: #0f172a;
      color: #ffffff;
      border-radius: 8px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .sticky-control-bar {
      position: sticky;
      top: 10px;
      z-index: 100;
      background: #020617;
      border: 1px solid #38bdf8;
      border-radius: 6px;
      padding: 12px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    .inspector-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
    }
    .inspector-panel {
      background: #020617;
      border: 1px solid #334155;
      border-radius: 6px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      font-family: var(--font-mono);
      font-size: 0.82rem;
    }
    .inspector-title {
      font-size: 0.85rem;
      font-weight: 700;
      color: #38bdf8;
      text-transform: uppercase;
      border-bottom: 1px solid #1e293b;
      padding-bottom: 6px;
      display: flex;
      justify-content: space-between;
    }
    .inspector-row {
      display: flex;
      justify-content: space-between;
      color: #ffffff;
      padding: 3px 0;
      border-bottom: 1px dashed #1e293b;
    }
    .inspector-row span.highlight { color: #34d399; font-weight: 700; }
    .inspector-row span.alert { color: #f87171; font-weight: 700; }
    .sandbox-controls {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    button {
      background-color: var(--accent);
      color: #fff;
      border: none;
      padding: 8px 14px;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.85rem;
      cursor: pointer;
      transition: background-color 0.15s ease;
    }
    button:hover { background-color: var(--accent-hover); }
    button.btn-sec { background-color: #334155; border: 1px solid #475569; color: #fff; }
    button.btn-sec:hover { background-color: #475569; }
    button.btn-danger { background-color: var(--danger-color); color: #fff; }
    button.btn-danger:hover { background-color: #b91c1c; }
    .kernel-console {
      background-color: #020617;
      color: #38bdf8;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      padding: 14px;
      border-radius: 6px;
      min-height: 90px;
      line-height: 1.5;
      white-space: pre-wrap;
      border: 1px solid #1e293b;
    }
  </style>
</head>
<body>
  <div class="nav-back">
    <a href="index.html">&larr; Back to Week 10 Index</a>
  </div>
  <header>
    <h1>02. Directory Systems &amp; Hierarchies</h1>
    <p class="subtitle">Tanenbaum Chapter 4.2: Comprehensive Reference on Single-Level, Two-Level, and Hierarchical Directory Structures, Path Resolution, and System Operations.</p>
  </header>
  <div class="main-container">

    <!-- Section 4.2.1: Single-Level Directory Systems -->
    <div class="card">
      <h2>4.2.1 Single-Level Directory Systems</h2>
      <p>
        To track files stored on secondary storage media, the operating system maintains a mapping between human-readable file names and physical storage locations. The simplest conceivable design is a <strong>single-level directory system</strong> (often termed a flat directory structure).
      </p>

      <h3>Architectural Characteristics</h3>
      <ul>
        <li><strong>Unified Global Namespace:</strong> A single directory contains every file present on the entire storage volume. There are no subdirectories, namespaces, or divisions by user account.</li>
        <li><strong>Global Name Uniqueness:</strong> Every file must have a distinct, globally unique identifier. If one user creates a file named <code>assignment.c</code>, no other user can create a file named <code>assignment.c</code> on that disk volume.</li>
        <li><strong>Direct Linear Mapping:</strong> The directory entry directly pairs each file name with its file attributes and disk allocation addresses (or a pointer to a metadata block).</li>
      </ul>

      <h3>Practical Applications &amp; Legacy Context</h3>
      <p>
        Single-level directory systems appeared in early mainframe operating systems and first-generation personal microcomputers, such as early CP/M and the original MS-DOS 1.0 release for floppy disk media. On a 160 KB or 360 KB 5.25-inch diskette holding at most a few dozen files, a flat directory was computationally inexpensive and simple to maintain.
      </p>

      <h3>Fundamental Limitations</h3>
      <ol>
        <li><strong>Name Collisions in Shared Environments:</strong> As soon as multiple users share a machine, coordinate naming conventions break down. Users are forced to invent artificial prefixes (e.g., <code>alice_prog.c</code> versus <code>bob_prog.c</code>) to avoid clobbering one another's files.</li>
        <li><strong>Project Segmentation Failure:</strong> Even for a single user, once a disk stores hundreds or thousands of files, keeping source code, object binaries, data files, and system tools in a single flat list makes search and cataloging difficult.</li>
        <li><strong>Linear Search Bottlenecks:</strong> Directory lookup requires scanning an increasingly large linear table, increasing disk access latency on file creation and retrieval.</li>
      </ol>

      <div class="figure-container">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure 4-1: Single-Level Flat Directory Layout</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 140" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <rect x="20" y="15" width="720" height="45" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" rx="6"/>
          <text x="380" y="34" font-size="11" font-weight="700" fill="#0284c7" text-anchor="middle">Root / Master Directory (Flat Table)</text>
          <text x="380" y="48" font-size="9" fill="#0369a1" text-anchor="middle">All users share one namespace | High collision probability</text>

          <g transform="translate(45, 75)">
            <rect width="110" height="45" fill="#ffffff" stroke="#94a3b8" rx="4"/>
            <text x="55" y="20" font-size="10" font-weight="600" fill="#0f172a" text-anchor="middle">file1.txt</text>
            <text x="55" y="34" font-size="8" fill="#64748b" text-anchor="middle">Blocks: 10, 11</text>
          </g>
          <g transform="translate(190, 75)">
            <rect width="110" height="45" fill="#ffffff" stroke="#94a3b8" rx="4"/>
            <text x="55" y="20" font-size="10" font-weight="600" fill="#0f172a" text-anchor="middle">notes.c</text>
            <text x="55" y="34" font-size="8" fill="#64748b" text-anchor="middle">Blocks: 14, 15</text>
          </g>
          <g transform="translate(335, 75)">
            <rect width="110" height="45" fill="#ffffff" stroke="#94a3b8" rx="4"/>
            <text x="55" y="20" font-size="10" font-weight="600" fill="#0f172a" text-anchor="middle">game.exe</text>
            <text x="55" y="34" font-size="8" fill="#64748b" text-anchor="middle">Blocks: 22, 23</text>
          </g>
          <g transform="translate(480, 75)">
            <rect width="110" height="45" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5" rx="4"/>
            <text x="55" y="20" font-size="10" font-weight="700" fill="#dc2626" text-anchor="middle">memo.txt</text>
            <text x="55" y="34" font-size="8" fill="#b91c1c" text-anchor="middle">Alice's Copy</text>
          </g>
          <g transform="translate(615, 75)">
            <rect width="110" height="45" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="3,3" rx="4"/>
            <text x="55" y="20" font-size="10" font-weight="700" fill="#dc2626" text-anchor="middle">memo.txt</text>
            <text x="55" y="34" font-size="8" fill="#b91c1c" text-anchor="middle">COLLISION (Denied)</text>
          </g>

          <line x1="100" y1="60" x2="100" y2="75" stroke="#94a3b8" stroke-width="1.5"/>
          <line x1="245" y1="60" x2="245" y2="75" stroke="#94a3b8" stroke-width="1.5"/>
          <line x1="390" y1="60" x2="390" y2="75" stroke="#94a3b8" stroke-width="1.5"/>
          <line x1="535" y1="60" x2="535" y2="75" stroke="#94a3b8" stroke-width="1.5"/>
          <line x1="670" y1="60" x2="670" y2="75" stroke="#dc2626" stroke-width="1.5"/>
        </svg>
      </div>
    </div>

    <!-- Section 4.2.2: Two-Level Directory Systems -->
    <div class="card">
      <h2>4.2.2 Two-Level Directory Systems</h2>
      <p>
        To eliminate name collisions between different users without incurring the overhead of arbitrary tree traversal, operating systems transitioned to <strong>two-level directory systems</strong>.
      </p>

      <h3>Structural Division</h3>
      <p>
        A two-level directory system splits the storage namespace into two distinct operational tiers:
      </p>
      <ul>
        <li><strong>Master File Directory (MFD):</strong> The primary root-level system table. The MFD is indexed by user identity or account number; each entry points directly to that user's private directory.</li>
        <li><strong>User File Directory (UFD):</strong> A private directory allocated to each individual user. A UFD lists only the files belonging to that user, paired with their respective attributes and storage block pointers.</li>
      </ul>

      <h3>Operational Advantages</h3>
      <ul>
        <li><strong>Namespace Isolation:</strong> Different users can pick identical names without conflict. User $A$ and User $B$ can both create a file named <code>prog.c</code>; the operating system resolves them unambiguously based on the executing context's active UFD.</li>
        <li><strong>Access Control Boundaries:</strong> The operating system enforces natural isolation boundaries by confining standard file lookups strictly to the calling user's allocated UFD.</li>
      </ul>

      <h3>Limitations &amp; The Sharing Dilemma</h3>
      <p>
        While two-level structures resolve inter-user name collisions, they introduce severe operational constraints:
      </p>
      <ol>
        <li><strong>No Intra-User Grouping:</strong> Individual users cannot subdivide their work into functional subdirectories, courses, or components. A user with 500 files must still manage them inside a single, flat UFD.</li>
        <li><strong>Restricted File Sharing:</strong> If User $A$ needs to run an executable or inspect a data file belonging to User $B$, the system requires explicit syntax to cross UFD boundaries (e.g., <code>[UserB]data.txt</code> or <code>/userB/data.txt</code>), complicating file lookup routines and permission checking.</li>
        <li><strong>System Program Duplication:</strong> Standard utilities (compilers, text editors, system binaries) either had to be copied into every user's UFD—wasting limited disk space—or the operating system had to build an ad-hoc search rule that checked a special system directory whenever a file was not found in the local UFD.</li>
      </ol>

      <div class="figure-container">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure 4-2: Two-Level Directory Architecture (MFD to UFD Separation)</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 190" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <!-- MFD -->
          <rect x="230" y="15" width="300" height="40" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5" rx="4"/>
          <text x="380" y="32" font-size="11" font-weight="700" fill="#0284c7" text-anchor="middle">Master File Directory (MFD)</text>
          <text x="380" y="45" font-size="9" fill="#64748b" text-anchor="middle">Indexes User Accounts</text>

          <!-- Links to UFDs -->
          <path d="M 310 55 L 140 85" stroke="#94a3b8" stroke-width="1.5"/>
          <path d="M 380 55 L 380 85" stroke="#94a3b8" stroke-width="1.5"/>
          <path d="M 450 55 L 620 85" stroke="#94a3b8" stroke-width="1.5"/>

          <!-- UFD 1 -->
          <rect x="50" y="85" width="180" height="90" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
          <text x="140" y="102" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">User A Directory (UFD)</text>
          <rect x="65" y="112" width="150" height="24" fill="#ffffff" stroke="#a7f3d0" rx="3"/>
          <text x="140" y="128" font-size="9" fill="#065f46" text-anchor="middle">prog.c (Blocks: 4, 5)</text>
          <rect x="65" y="142" width="150" height="24" fill="#ffffff" stroke="#a7f3d0" rx="3"/>
          <text x="140" y="158" font-size="9" fill="#065f46" text-anchor="middle">data.dat (Blocks: 9)</text>

          <!-- UFD 2 -->
          <rect x="290" y="85" width="180" height="90" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
          <text x="380" y="102" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">User B Directory (UFD)</text>
          <rect x="305" y="112" width="150" height="24" fill="#ffffff" stroke="#a7f3d0" rx="3"/>
          <text x="380" y="128" font-size="9" fill="#065f46" text-anchor="middle">prog.c (Blocks: 18, 19)</text>
          <rect x="305" y="142" width="150" height="24" fill="#ffffff" stroke="#a7f3d0" rx="3"/>
          <text x="380" y="158" font-size="9" fill="#065f46" text-anchor="middle">test.out (Blocks: 21)</text>

          <!-- UFD 3 -->
          <rect x="530" y="85" width="180" height="90" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
          <text x="620" y="102" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">System / Shared UFD</text>
          <rect x="545" y="112" width="150" height="24" fill="#ffffff" stroke="#a7f3d0" rx="3"/>
          <text x="620" y="128" font-size="9" fill="#065f46" text-anchor="middle">cc (Compiler binary)</text>
          <rect x="545" y="142" width="150" height="24" fill="#ffffff" stroke="#a7f3d0" rx="3"/>
          <text x="620" y="158" font-size="9" fill="#065f46" text-anchor="middle">sh (Shell binary)</text>
        </svg>
      </div>
    </div>

    <!-- Section 4.2.3: Hierarchical Directory Systems -->
    <div class="card">
      <h2>4.2.3 Hierarchical (Tree-Structured) Directory Systems</h2>
      <p>
        The limitations of the two-level scheme led directly to the generalization of the directory concept: allowing directories to contain not only regular files, but also <strong>subdirectories</strong>. This produces an arbitrary, tree-structured hierarchy.
      </p>

      <h3>1. Directories as Specialized Regular Files</h3>
      <p>
        In modern operating systems (most notably Unix-like systems and Windows NTFS), a directory is conceptually treated just like a regular file with one crucial difference: <strong>its contents are structured as a lookup table of directory entries, and user-space programs are not permitted to write raw bytes to it directly</strong>.
      </p>
      <ul>
        <li>The operating system kernel retains exclusive write privileges over directory contents to preserve namespace and file system integrity.</li>
        <li>Each entry in the directory table maps a file name component to an identifier: an <strong>i-node number</strong> (in Unix file systems) or a <strong>file record index / File Control Block pointer</strong> (in FAT/NTFS).</li>
      </ul>

      <h3>2. Arbitrary Nesting &amp; Path Scoping</h3>
      <p>
        Users can construct arbitrary tree topologies to match logical mental models. A software project can place source code in <code>src/</code>, headers in <code>include/</code>, compiled objects in <code>build/</code>, and documentation in <code>doc/</code>. Identical component names (e.g., <code>Makefile</code> or <code>README.txt</code>) coexist cleanly across separate subtrees without collision.
      </p>

      <h3>3. The Self and Parent Links (<code>.</code> and <code>..</code>)</h3>
      <p>
        Every directory created in a standard hierarchical system automatically initializes two structural entries:
      </p>
      <ul>
        <li><strong><code>.</code> (dot):</strong> A hard reference pointing directly to the directory itself.</li>
        <li><strong><code>..</code> (dot-dot):</strong> A hard reference pointing to the parent directory immediately above it in the tree hierarchy (in the root directory <code>/</code>, <code>..</code> points back to <code>/</code> itself).</li>
      </ul>
      <p>
        These two built-in entries make tree traversal recursive, allowing programs to navigate upward and downward through relative paths without knowing the absolute location of the directory in the overall file system tree.
      </p>

      <div class="figure-container">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure 4-3: Hierarchical Tree &amp; Structural Self/Parent Links</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 210" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <!-- Tree Nodes -->
          <rect x="330" y="15" width="100" height="35" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5" rx="4"/>
          <text x="380" y="36" font-size="11" font-weight="700" fill="#0284c7" text-anchor="middle">/ (Root)</text>

          <path d="M 350 50 L 180 80" stroke="#94a3b8" stroke-width="1.5"/>
          <path d="M 380 50 L 380 80" stroke="#94a3b8" stroke-width="1.5"/>
          <path d="M 410 50 L 580 80" stroke="#94a3b8" stroke-width="1.5"/>

          <rect x="130" y="80" width="100" height="30" fill="#f0f9ff" stroke="#0284c7" rx="3"/>
          <text x="180" y="100" font-size="10" font-weight="600" fill="#0369a1" text-anchor="middle">bin/</text>

          <rect x="330" y="80" width="100" height="30" fill="#f0f9ff" stroke="#0284c7" rx="3"/>
          <text x="380" y="100" font-size="10" font-weight="600" fill="#0369a1" text-anchor="middle">etc/</text>

          <rect x="530" y="80" width="100" height="30" fill="#fffbeb" stroke="#d97706" stroke-width="1.5" rx="3"/>
          <text x="580" y="100" font-size="10" font-weight="700" fill="#b45309" text-anchor="middle">home/</text>

          <path d="M 580 110 L 580 135" stroke="#d97706" stroke-width="1.5"/>

          <rect x="520" y="135" width="120" height="65" fill="#fffbeb" stroke="#d97706" stroke-width="1.5" rx="4"/>
          <text x="580" y="152" font-size="10" font-weight="700" fill="#b45309" text-anchor="middle">student/ (i: 104)</text>

          <!-- Internal directory entries -->
          <rect x="526" y="160" width="50" height="18" fill="#ffffff" stroke="#cbd5e1" rx="2"/>
          <text x="551" y="173" font-size="8" font-family="monospace" fill="#0f172a" text-anchor="middle">. (104)</text>

          <rect x="584" y="160" width="50" height="18" fill="#ffffff" stroke="#cbd5e1" rx="2"/>
          <text x="609" y="173" font-size="8" font-family="monospace" fill="#0f172a" text-anchor="middle">.. (42)</text>

          <rect x="526" y="180" width="108" height="16" fill="#ecfdf5" stroke="#10b981" rx="2"/>
          <text x="580" y="192" font-size="8" font-family="monospace" fill="#065f46" text-anchor="middle">lab10.c (112)</text>

          <!-- Annotations for dot and dot-dot -->
          <path d="M 526 169 C 480 169, 480 145, 515 145" fill="none" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="2,2"/>
          <text x="470" y="158" font-size="8" font-weight="600" fill="#0284c7" text-anchor="end">. points to self</text>

          <path d="M 634 169 C 680 169, 680 95, 635 95" fill="none" stroke="#d97706" stroke-width="1.5" stroke-dasharray="2,2"/>
          <text x="685" y="135" font-size="8" font-weight="600" fill="#d97706" text-anchor="start">.. points to parent (/home)</text>
        </svg>
      </div>

      <h3>Comparison of Directory Organization Models</h3>
      <table>
        <thead>
          <tr>
            <th>Dimension</th>
            <th>Single-Level</th>
            <th>Two-Level</th>
            <th>Hierarchical (Tree)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Namespace Scope</strong></td>
            <td>Single global table</td>
            <td>Master directory with per-user tables</td>
            <td>Arbitrary tree rooted at <code>/</code> or drive letters</td>
          </tr>
          <tr>
            <td><strong>Subdirectory Support</strong></td>
            <td>None</td>
            <td>Fixed at 1 level below master</td>
            <td>Arbitrary depth ($\ge 1$)</td>
          </tr>
          <tr>
            <td><strong>Name Clashes</strong></td>
            <td>Frequent across all users</td>
            <td>Prevented between users; frequent within user</td>
            <td>Prevented across distinct directories</td>
          </tr>
          <tr>
            <td><strong>File Grouping</strong></td>
            <td>Impossible</td>
            <td>Limited to user boundary</td>
            <td>Fully user-configurable</td>
          </tr>
          <tr>
            <td><strong>Lookup Mechanism</strong></td>
            <td>Linear scan of global list</td>
            <td>2-step scan (MFD $\rightarrow$ UFD)</td>
            <td>Recursive path traversal component-by-component</td>
          </tr>
          <tr>
            <td><strong>Implementation Complexity</strong></td>
            <td>Minimal</td>
            <td>Low</td>
            <td>Moderate to High (requires path parsing &amp; recursion)</td>
          </tr>
          <tr>
            <td><strong>Modern Usage</strong></td>
            <td>Embedded microcontrollers, small FAT12 partitions</td>
            <td>Specialized embedded or batch systems</td>
            <td>Standard across Linux, macOS, Windows, BSD</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Section 4.2.4: Directory Operations & System Calls -->
    <div class="card">
      <h2>4.2.4 Directory Operations &amp; System Calls</h2>
      <p>
        Operating systems provide a specialized suite of system calls to manage directories and link namespaces together:
      </p>
      <ol>
        <li><strong>Create:</strong> Creates a new, empty directory (such as <code>mkdir</code>). Initially, it contains only two structural entries: <code>.</code> (referencing itself) and <code>..</code> (referencing its parent directory).</li>
        <li><strong>Delete:</strong> Removes a directory (such as <code>rmdir</code>). Most operating systems require the directory to be completely empty (containing only <code>.</code> and <code>..</code>) before deletion is permitted to prevent accidental orphan trees.</li>
        <li><strong>Opendir:</strong> Opens a directory for inspection, returning a directory stream pointer or descriptor.</li>
        <li><strong>Readdir:</strong> Reads the next entry from an open directory stream, returning file names and i-node numbers. Historically, applications read raw directory bytes directly, but modern systems enforce <code>readdir</code> to abstract internal directory block layouts and prevent direct corruption of symbol tables.</li>
        <li><strong>Closedir:</strong> Releases directory stream resources when directory traversal concludes.</li>
        <li><strong>Rename:</strong> Changes a file or directory name within the namespace tree without duplicating underlying data blocks.</li>
        <li><strong>Link:</strong> Creates a new hard link—an additional directory entry pointing to an existing file's i-node. This allows a single file to exist under multiple names or in different directories simultaneously.</li>
        <li><strong>Unlink:</strong> Removes a directory entry. If the entry being unlinked is the final hard link pointing to an i-node (and no execution contexts have it open), the i-node and its associated data blocks are deallocated.</li>
      </ol>
    </div>

    <!-- Interactive Hard Link & Unlink Simulator Sandbox -->
    <div class="card kernel-sandbox">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
        <div style="font-weight: 700; font-size: 1.1rem; color: #ffffff;">Interactive Hard Link &amp; Unlink Simulator</div>
      </div>

      <div class="sticky-control-bar">
        <div style="font-weight: 700; color: #fbbf24; font-size: 0.8rem; text-transform: uppercase; font-family: var(--font-mono);">Directory System Call Controls:</div>
        <div class="sandbox-controls">
          <button onclick="simOp('create')" style="font-size: 0.8rem; padding: 6px 12px;">creat("notes.txt")</button>
          <button onclick="simOp('link')" class="btn-sec" style="font-size: 0.8rem; padding: 6px 12px;">link("notes.txt", "backup.txt")</button>
          <button onclick="simOp('unlink1')" class="btn-sec" style="font-size: 0.8rem; padding: 6px 12px;">unlink("notes.txt")</button>
          <button onclick="simOp('unlink2')" class="btn-sec btn-danger" style="font-size: 0.8rem; padding: 6px 12px;">unlink("backup.txt")</button>
        </div>
      </div>

      <div class="inspector-grid">
        <div class="inspector-panel">
          <div class="inspector-title"><span>Directory Namespace</span><span>(/home/student)</span></div>
          <div class="inspector-row"><span>notes.txt:</span><span id="dir-notes" class="alert">-- UNUSED --</span></div>
          <div class="inspector-row"><span>backup.txt:</span><span id="dir-backup" class="alert">-- UNUSED --</span></div>
        </div>

        <div class="inspector-panel">
          <div class="inspector-title"><span>i-Node Table</span><span>(#42 Metadata)</span></div>
          <div class="inspector-row"><span>Link Count:</span><span id="inode-links" class="highlight">0</span></div>
          <div class="inspector-row"><span>Storage Blocks:</span><span id="inode-blocks">0 Blocks</span></div>
          <div class="inspector-row"><span>Status:</span><span id="inode-status" class="alert">DEALLOCATED</span></div>
        </div>
      </div>

      <div id="dirConsole" class="kernel-console">$ directory simulation initialized. Ready for link/unlink operations...</div>
    </div>

  </div>

  <script>
    let state = {
      notesExists: false,
      backupExists: false,
      linkCount: 0,
      blocks: 0,
      status: "DEALLOCATED"
    };

    function updateDirUI(msg) {
      const nEl = document.getElementById("dir-notes");
      nEl.textContent = state.notesExists ? "i-Node #42" : "-- UNUSED --";
      nEl.className = state.notesExists ? "highlight" : "alert";

      const bEl = document.getElementById("dir-backup");
      bEl.textContent = state.backupExists ? "i-Node #42" : "-- UNUSED --";
      bEl.className = state.backupExists ? "highlight" : "alert";

      document.getElementById("inode-links").textContent = state.linkCount;
      document.getElementById("inode-blocks").textContent = state.blocks + " Blocks";

      const stEl = document.getElementById("inode-status");
      stEl.textContent = state.status;
      stEl.className = state.status === "ACTIVE" ? "highlight" : "alert";

      document.getElementById("dirConsole").textContent = msg;
    }

    function simOp(op) {
      if (op === 'create') {
        state.notesExists = true;
        state.linkCount = 1;
        state.blocks = 4;
        state.status = "ACTIVE";
        updateDirUI("$ creat(\"notes.txt\");\n[Kernel] Created directory entry 'notes.txt' pointing to i-Node #42. Link count = 1.");
      } else if (op === 'link') {
        if (!state.notesExists) {
          updateDirUI("$ link(\"notes.txt\", \"backup.txt\");\n[Error] No such file or directory: 'notes.txt'");
          return;
        }
        state.backupExists = true;
        state.linkCount = 2;
        updateDirUI("$ link(\"notes.txt\", \"backup.txt\");\n[Kernel] Created hard link 'backup.txt' pointing to i-Node #42. Link count incremented to 2.");
      } else if (op === 'unlink1') {
        if (!state.notesExists) {
          updateDirUI("$ unlink(\"notes.txt\");\n[Error] File not found.");
          return;
        }
        state.notesExists = false;
        state.linkCount = 1;
        updateDirUI("$ unlink(\"notes.txt\");\n[Kernel] Removed directory entry 'notes.txt'. i-Node #42 link count decreased to 1. File data remains accessible via 'backup.txt'.");
      } else if (op === 'unlink2') {
        if (!state.backupExists) {
          updateDirUI("$ unlink(\"backup.txt\");\n[Error] File not found.");
          return;
        }
        state.backupExists = false;
        state.linkCount = 0;
        state.blocks = 0;
        state.status = "DEALLOCATED";
        updateDirUI("$ unlink(\"backup.txt\");\n[Kernel] Removed final directory entry. i-Node #42 link count reached 0. Deallocated disk blocks and purged i-Node.");
      }
    }
  </script>
</body>
</html>
"""

COMMIT_MSG = """Expand module 02 with deep directory hierarchy theory and SVGs

Update week10-file-management/02-directories.html to expand sections
4.2.1 and 4.2.2 with detailed architectural analysis, custom SVGs for
single/two-level/hierarchical systems, and dot/dot-dot self-links."""

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

def deploy_module():
    target_dir = "week10-file-management"
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, "02-directories.html")

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Wrote updated module file 02-directories.html to {target_file}")

    run_git_step(["git", "add", target_file], "Staging expanded 02-directories.html update")
    run_git_step(["git", "commit", "-a", "-m", COMMIT_MSG], "Committing changes")
    run_git_step(["git", "push", "origin", "main"], "Pushing main to origin")
    print("--> Module 02 Directory Systems updated, committed, and pushed successfully!")

if __name__ == "__main__":
    deploy_module()
