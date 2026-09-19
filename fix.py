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
      margin-top: 10px;
      margin-bottom: 4px;
    }
    .card h4 {
      font-size: 0.95rem;
      color: var(--text);
      margin-top: 6px;
      margin-bottom: 2px;
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

    <!-- Section 4.2.2: Two-Level Directory Systems (Expanded) -->
    <div class="card">
      <h2>4.2.2 Two-Level Directory Systems</h2>

      <h3>1. Motivation and Historical Impetus</h3>
      <p>
        The transition from batch systems dedicated to a single job at a time to multi-user time-sharing architectures (such as MIT's CTSS and early DEC systems like TOPS-10) exposed the primary flaw of single-level directories: <strong>global namespace collision</strong>.
      </p>
      <p>
        When dozens or hundreds of independent users share a single disk volume, requiring unique file names across the entire storage pool is unworkable. Two users working on independent tasks will naturally choose obvious names like <code>main.c</code>, <code>test.dat</code>, or <code>notes.txt</code>. Under a single-level system, whichever user saves first claims the identifier; the second user is either blocked by a creation error or silently overwrites the existing file. To eliminate this conflict without introducing the structural complexity of recursive tree traversal, operating system designers introduced the <strong>two-level directory system</strong>.
      </p>

      <h3>2. Structural Topology: MFD and UFD</h3>
      <p>
        A two-level directory hierarchy establishes a fixed two-tier topology consisting of two distinct classes of directories:
      </p>
      <ul>
        <li>
          <strong>Master File Directory (MFD):</strong> The root-level administrative symbol table maintained by the kernel. It contains exactly one entry for each registered user account or project group, indexed by username, account number, or project-programmer number (PPN). Each entry contains administrative metadata and a physical pointer to the disk location where that user's private directory begins.
        </li>
        <li>
          <strong>User File Directory (UFD):</strong> A dedicated directory table created for each individual account. It contains entries solely for the files created by or assigned to that specific user. Each entry maps an individual file name to its metadata (file size, access permissions, creation timestamps, and physical disk block addresses). From the user's perspective, the UFD behaves like an isolated single-level directory; no other user's files appear within it by default.
        </li>
      </ul>

      <div class="figure-container">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure 4-2A: Two-Level Directory Structural Topology (MFD to UFD)</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 190" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <!-- MFD -->
          <rect x="230" y="15" width="300" height="42" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5" rx="4"/>
          <text x="380" y="32" font-size="11" font-weight="700" fill="#0284c7" text-anchor="middle">Master File Directory (MFD)</text>
          <text x="380" y="47" font-size="9" fill="#64748b" text-anchor="middle">[ALICE] | [BOB] | [SYSTEM]</text>

          <!-- Links to UFDs -->
          <path d="M 300 57 L 140 85" stroke="#94a3b8" stroke-width="1.5"/>
          <path d="M 380 57 L 380 85" stroke="#94a3b8" stroke-width="1.5"/>
          <path d="M 460 57 L 620 85" stroke="#94a3b8" stroke-width="1.5"/>

          <!-- UFD ALICE -->
          <rect x="50" y="85" width="180" height="92" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
          <text x="140" y="102" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">UFD: ALICE</text>
          <rect x="65" y="110" width="150" height="20" fill="#ffffff" stroke="#a7f3d0" rx="3"/>
          <text x="140" y="124" font-size="8.5" fill="#065f46" text-anchor="middle">main.c (i-node #108)</text>
          <rect x="65" y="134" width="150" height="20" fill="#ffffff" stroke="#a7f3d0" rx="3"/>
          <text x="140" y="148" font-size="8.5" fill="#065f46" text-anchor="middle">test.dat (i-node #109)</text>
          <rect x="65" y="158" width="150" height="15" fill="#ffffff" stroke="#a7f3d0" rx="3"/>
          <text x="140" y="169" font-size="8" fill="#065f46" text-anchor="middle">output.log</text>

          <!-- UFD BOB -->
          <rect x="290" y="85" width="180" height="92" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
          <text x="380" y="102" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">UFD: BOB</text>
          <rect x="305" y="110" width="150" height="20" fill="#ffffff" stroke="#a7f3d0" rx="3"/>
          <text x="380" y="124" font-size="8.5" fill="#065f46" text-anchor="middle">main.c (i-node #214)</text>
          <rect x="305" y="134" width="150" height="20" fill="#ffffff" stroke="#a7f3d0" rx="3"/>
          <text x="380" y="148" font-size="8.5" fill="#065f46" text-anchor="middle">project.asm (i-node #215)</text>
          <rect x="305" y="158" width="150" height="15" fill="#ffffff" stroke="#a7f3d0" rx="3"/>
          <text x="380" y="169" font-size="8" fill="#065f46" text-anchor="middle">notes.txt</text>

          <!-- UFD SYSTEM -->
          <rect x="530" y="85" width="180" height="92" fill="#fffbeb" stroke="#d97706" stroke-width="1.5" rx="4"/>
          <text x="620" y="102" font-size="10" font-weight="700" fill="#b45309" text-anchor="middle">UFD: SYSTEM (SYS:)</text>
          <rect x="545" y="110" width="150" height="20" fill="#ffffff" stroke="#fde68a" rx="3"/>
          <text x="620" y="124" font-size="8.5" fill="#92400e" text-anchor="middle">cc (Compiler binary)</text>
          <rect x="545" y="134" width="150" height="20" fill="#ffffff" stroke="#fde68a" rx="3"/>
          <text x="620" y="148" font-size="8.5" fill="#92400e" text-anchor="middle">ed (Editor binary)</text>
          <rect x="545" y="158" width="150" height="15" fill="#ffffff" stroke="#fde68a" rx="3"/>
          <text x="620" y="169" font-size="8" fill="#92400e" text-anchor="middle">as (Assembler binary)</text>
        </svg>
      </div>

      <h3>3. Operational Mechanics and Resolution Traversal</h3>
      <h4>Login and Context Binding</h4>
      <p>
        When a user logs into the operating system, the authentication sequence performs a targeted lookup:
      </p>
      <ol>
        <li>The kernel queries the user identification table and locates the user's corresponding record within the <strong>MFD</strong>.</li>
        <li>The kernel extracts the disk address of the user's <strong>UFD</strong> and caches its root references in memory.</li>
        <li>The executing session sets its <strong>current default directory pointer</strong> directly to this UFD.</li>
      </ol>

      <h4>Name Resolution Algorithm</h4>
      <p>
        Whenever an executing program executes a file system call (such as <code>open</code>, <code>creat</code>, or <code>delete</code>):
      </p>
      <ul>
        <li>The file name string is resolved <strong>locally</strong> within the active session's UFD.</li>
        <li>Because lookups are scoped strictly to the current UFD, identical file names across different accounts cause zero interference.</li>
        <li>Alice opening <code>main.c</code> accesses i-node/FCB <code>#108</code> from her UFD; Bob opening <code>main.c</code> accesses i-node/FCB <code>#214</code> from his own UFD without naming conflict.</li>
      </ul>

      <h3>4. The System Utility and Library Dilemma</h3>
      <p>
        While segregating accounts resolves user collisions, it introduces a major operational challenge: <strong>how to access standard system software</strong>. Operating systems depend on common executable utilities—compilers (<code>cc</code>), assemblers (<code>as</code>), text editors (<code>ed</code>), linkers (<code>ld</code>), and shared runtime libraries. In a strict two-level system where lookups only query the caller's UFD, standard commands fail unless those programs reside in that specific UFD.
      </p>

      <div class="figure-container">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure 4-2B: Utility Duplication Waste vs. Two-Stage Fallback Search</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 160" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <!-- Option 1 -->
          <rect x="30" y="15" width="320" height="130" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5" rx="4"/>
          <text x="190" y="34" font-size="10" font-weight="700" fill="#dc2626" text-anchor="middle">Option 1: Redundant Executable Duplication</text>

          <rect x="45" y="45" width="135" height="60" fill="#ffffff" stroke="#fca5a5" rx="3"/>
          <text x="112" y="60" font-size="8.5" font-weight="600" fill="#991b1b" text-anchor="middle">UFD: ALICE</text>
          <text x="112" y="75" font-size="8" fill="#334155" text-anchor="middle">cc (1 MB) [Duplicate]</text>
          <text x="112" y="90" font-size="8" fill="#334155" text-anchor="middle">ed (500 KB) [Duplicate]</text>

          <rect x="200" y="45" width="135" height="60" fill="#ffffff" stroke="#fca5a5" rx="3"/>
          <text x="267" y="60" font-size="8.5" font-weight="600" fill="#991b1b" text-anchor="middle">UFD: BOB</text>
          <text x="267" y="75" font-size="8" fill="#334155" text-anchor="middle">cc (1 MB) [Duplicate]</text>
          <text x="267" y="90" font-size="8" fill="#334155" text-anchor="middle">ed (500 KB) [Duplicate]</text>

          <text x="190" y="128" font-size="8.5" fill="#b91c1c" text-anchor="middle">Severe secondary storage exhaustion across accounts</text>

          <!-- Option 2 -->
          <rect x="390" y="15" width="340" height="130" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
          <text x="560" y="34" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">Option 2: Two-Stage Fallback Search Rule</text>

          <rect x="410" y="45" width="130" height="42" fill="#ffffff" stroke="#a7f3d0" rx="3"/>
          <text x="475" y="60" font-size="8.5" font-weight="600" fill="#065f46" text-anchor="middle">Step 1: Local UFD</text>
          <text x="475" y="75" font-size="8" fill="#64748b" text-anchor="middle">Check active user files</text>

          <path d="M 540 66 L 580 66" stroke="#059669" stroke-width="1.5" marker-end="url(#arrow-green)"/>
          <text x="560" y="60" font-size="7.5" fill="#059669" font-weight="700" text-anchor="middle">Miss</text>

          <rect x="580" y="45" width="130" height="42" fill="#ffffff" stroke="#a7f3d0" rx="3"/>
          <text x="645" y="60" font-size="8.5" font-weight="600" fill="#065f46" text-anchor="middle">Step 2: SYSTEM UFD</text>
          <text x="645" y="75" font-size="8" fill="#047857" text-anchor="middle">Locate shared cc / ed</text>

          <text x="560" y="112" font-size="8.5" fill="#065f46" text-anchor="middle">Eliminates duplicate disk storage entirely</text>
          <text x="560" y="128" font-size="8" fill="#64748b" text-anchor="middle">Local file names may shadow system executables</text>

          <defs>
            <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669" />
            </marker>
          </defs>
        </svg>
      </div>

      <h4>The Two-Stage Fallback Search</h4>
      <p>
        Duplicating executables across every user's directory wastes precious secondary storage. Two-level architectures resolved this by designating a special system directory (often indexed in the MFD as <code>SYS</code>, <code>SYSTEM</code>, or user number <code>0</code>) and altering the directory search rule:
      </p>
      <div class="callout">
        $$\text{Search Target} = \begin{cases}
        \text{Search Active UFD}, & \text{Step 1} \\
        \text{If not found} \longrightarrow \text{Search SYSTEM UFD}, & \text{Step 2} \\
        \text{If not found} \longrightarrow \text{Return Error (File Not Found)}, & \text{Step 3}
        \end{cases}$$
      </div>
      <p>
        This fallback rule allowed all users to execute standard system binaries without duplicating blocks on disk. However, it introduced subtle shadowing issues: if Alice created a private data file or test script named <code>cc</code>, her local version shadowed the system compiler, causing unexpected command behavior.
      </p>

      <h3>5. Cross-User File Sharing and Namespace Syntax</h3>
      <p>
        Real-world multi-user collaboration frequently requires reading or executing files belonging to another account. Because the standard lookup stops at the active user's UFD, systems had to invent <strong>cross-directory naming syntax</strong>:
      </p>
      <table>
        <thead>
          <tr>
            <th>Operating System</th>
            <th>Syntax Convention</th>
            <th>Resolution Mechanism</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>DEC PDP-10 (TOPS-10)</strong></td>
            <td><code>[Project,Programmer]Filename</code><br>(e.g., <code>[10,20]DATA.DAT</code>)</td>
            <td>Bypasses active UFD; queries MFD for project 10, programmer 20, then scans target UFD.</td>
          </tr>
          <tr>
            <td><strong>Early UNIX Precursors</strong></td>
            <td><code>username/filename</code> or <code>:user:filename</code></td>
            <td>Explicitly names the peer MFD bucket before locating the file entry.</td>
          </tr>
          <tr>
            <td><strong>CP/M 2.2 / 3.0 (User Areas)</strong></td>
            <td><code>USER N:</code><br>(e.g., <code>USER 2:</code>, <code>B2:FILE.DAT</code>)</td>
            <td>Swaps the active drive user area partition mask before reading directory allocation blocks.</td>
          </tr>
        </tbody>
      </table>

      <h4>Protection and Access Control</h4>
      <p>
        Allowing one user to specify another user's directory entry created immediate security risks. Two-level systems could no longer rely on physical isolation and had to implement explicit protection checks:
      </p>
      <ul>
        <li><strong>Access Permissions:</strong> Every entry in a UFD incorporated permission bits defining whether peer users could read, write, or execute the underlying file.</li>
        <li><strong>Directory Read Restrictions:</strong> Users could be prevented from listing the contents of a peer's UFD, even if they were permitted to read a specifically named file inside it.</li>
      </ul>

      <h3>6. Architectural Evaluation and Inevitable Evolution</h3>
      <table>
        <thead>
          <tr>
            <th>Architectural Dimension</th>
            <th>Single-Level System</th>
            <th>Two-Level System</th>
            <th>Hierarchical Tree System</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Directory Depth</strong></td>
            <td>Exactly 1</td>
            <td>Exactly 2 (Fixed)</td>
            <td>Arbitrary ($N \ge 1$)</td>
          </tr>
          <tr>
            <td><strong>Namespace Isolation</strong></td>
            <td>None (Global shared pool)</td>
            <td>Isolated per user account</td>
            <td>Isolated per directory node</td>
          </tr>
          <tr>
            <td><strong>Inter-User Collisions</strong></td>
            <td>Chronic problem</td>
            <td>Completely eliminated</td>
            <td>Completely eliminated</td>
          </tr>
          <tr>
            <td><strong>Intra-User Grouping</strong></td>
            <td>Impossible</td>
            <td>Impossible (Single flat UFD)</td>
            <td>Fully supported (Nested subfolders)</td>
          </tr>
          <tr>
            <td><strong>Path Traversal Cost</strong></td>
            <td>1 Directory block scan</td>
            <td>2 Directory block scans</td>
            <td>$N$ Directory block scans</td>
          </tr>
          <tr>
            <td><strong>System Utility Access</strong></td>
            <td>Direct lookup</td>
            <td>Requires two-stage fallback</td>
            <td>Handled via configurable <code>PATH</code> search lists</td>
          </tr>
        </tbody>
      </table>

      <h4>The Ceiling of the Two-Level Model</h4>
      <p>
        While the two-level directory solved the inter-user naming dilemma, it quickly reached its architectural limits:
      </p>
      <ol>
        <li><strong>Intra-Account Clutter:</strong> Individual users accumulating hundreds of files suffered from the exact same flat-namespace problem inside their own UFD. A programmer working on three independent projects had to keep all source modules, documentation, and object files in one unorganized pile.</li>
        <li><strong>Artificial Depth Barrier:</strong> The structural distinction between the MFD (which could only point to UFDs) and UFDs (which could only point to data files) was an arbitrary, rigid restriction.</li>
        <li><strong>The Generalization Step:</strong> Operating system researchers realized that if a directory entry could point to either a data file <strong>or another directory</strong>, the rigid two-level structure naturally generalized into an arbitrary <strong>hierarchical tree</strong>. This removed all restrictions on depth and enabled users to build structured, self-contained subtrees.</li>
      </ol>
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

COMMIT_MSG = """Expand section 4.2.2 two-level directories with detailed theory and SVGs

Update week10-file-management/02-directories.html to expand section 4.2.2
with complete coverage of MFD/UFD topology, two-stage search fallbacks,
cross-user sharing conventions, and custom explanatory SVG diagrams."""

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

    run_git_step(["git", "add", target_file], "Staging updated 02-directories.html")
    run_git_step(["git", "commit", "-a", "-m", COMMIT_MSG], "Committing changes")
    run_git_step(["git", "push", "origin", "main"], "Pushing main to origin")
    print("--> Module 02 Two-Level Directories updated, committed, and pushed successfully!")

if __name__ == "__main__":
    deploy_module()
