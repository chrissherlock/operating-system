#!/usr/bin/env python3
import os
import subprocess
import sys

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>03. File-System Implementation — COSC240 Week 10</title>
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

    /* Simulator Styles */
    .sim-card {
      background: #0f172a;
      color: #f8fafc;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .sim-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #334155;
      padding-bottom: 8px;
    }
    .sim-title {
      font-size: 1.05rem;
      font-weight: 700;
      color: #38bdf8;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-family: var(--font-mono);
    }
    .sim-controls {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      background: #020617;
      border: 1px solid #1e293b;
      padding: 10px 14px;
      border-radius: 6px;
    }
    button.sim-btn {
      background-color: #1e293b;
      color: #cbd5e1;
      border: 1px solid #334155;
      padding: 7px 14px;
      border-radius: 5px;
      font-size: 0.8rem;
      font-weight: 600;
      font-family: var(--font-mono);
      cursor: pointer;
      transition: all 0.15s ease;
    }
    button.sim-btn:hover {
      background-color: #334155;
      color: #ffffff;
    }
    button.sim-btn.active-btn {
      background-color: var(--accent);
      border-color: #38bdf8;
      color: #ffffff;
      box-shadow: 0 0 10px rgba(2, 132, 199, 0.4);
    }
    .sim-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }
    @media (max-width: 820px) {
      .sim-grid { grid-template-columns: 1fr; }
    }
    .sim-panel {
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
    .sim-panel-title {
      color: #fbbf24;
      font-size: 0.82rem;
      font-weight: 700;
      text-transform: uppercase;
      border-bottom: 1px solid #1e293b;
      padding-bottom: 6px;
    }
    .sim-row {
      display: flex;
      justify-content: space-between;
      padding: 3px 0;
      border-bottom: 1px dashed #1e293b;
      color: #cbd5e1;
    }
    .sim-row span.val { color: #38bdf8; font-weight: 700; }
    .sim-console {
      background: #020617;
      border: 1px solid #1e293b;
      border-radius: 6px;
      padding: 12px 14px;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      color: #38bdf8;
      min-height: 60px;
      line-height: 1.5;
      white-space: pre-wrap;
    }
  </style>
</head>
<body>
  <div class="nav-back">
    <a href="index.html">&larr; Back to Week 10 Index</a>
  </div>
  <header>
    <h1>03. File-System Implementation</h1>
    <p class="subtitle">Tanenbaum Chapter 4.3: Physical Layouts, Storage Allocation Models, Directory Records, Virtual File Systems, and Journaling.</p>
  </header>
  <div class="main-container">

    <!-- Section 4.3.1: File-System Layout -->
    <div class="card">
      <h2>4.3.1 File-System Layout</h2>
      <p>
        File systems are stored on non-volatile disks, solid-state drives, or partitions. Physical storage devices divide raw media into fixed-size physical sectors (typically 512 bytes or 4096 bytes). Operating system file systems group these physical sectors into larger logical <strong>blocks</strong> (clusters), typically ranging from 1 KB to 64 KB, to balance metadata overhead against internal fragmentation.
      </p>

      <h3>1. Partitioning &amp; Boot Records</h3>
      <p>
        Before a filesystem can be initialized, a storage drive is segmented into one or more partitions. Sector 0 of the entire physical disk contains the <strong>Master Boot Record (MBR)</strong> or the primary <strong>GUID Partition Table (GPT)</strong>:
      </p>
      <ul>
        <li><strong>Master Boot Record (MBR):</strong> Contains bootstrap executable code executed by the BIOS, along with a 64-byte partition table defining the boundaries and types of up to four primary partitions.</li>
        <li><strong>GPT / UEFI:</strong> Modern replacement for MBR supporting 64-bit logical block addressing, redundant partition headers, CRC32 checksums, and globally unique partition identifiers.</li>
      </ul>

      <h3>2. On-Disk Structural Regions</h3>
      <p>
        When a partition is formatted (for instance, via <code>mkfs</code>), the operating system initializes several distinct functional regions laid out sequentially across the partition blocks:
      </p>
      <ol>
        <li><strong>Boot Block:</strong> The first block of the partition. Contains partition-specific bootstrap code read into memory by the MBR/UEFI to launch the target operating system. Present even if the partition is not bootable.</li>
        <li><strong>Superblock:</strong> The central administrative descriptor. Stores critical geometry parameters: magic number (identifying filesystem type), total number of blocks, number of i-nodes, block size, volume state flags (clean/dirty), and pointers to free-space tracking structures. If the superblock is corrupted, the filesystem cannot be mounted; thus, kernels maintain redundant backup copies across the volume.</li>
        <li><strong>Free Space Management:</strong> Data structures tracking unallocated blocks available for new file data. Common implementations include:
          <ul>
            <li><em>Bitmap (Bit Vector):</em> An array of bits where bit $i = 0$ indicates block $i$ is free, and bit $i = 1$ indicates allocation. Compact and cache-friendly.</li>
            <li><em>Linked Free List:</em> Dedicated disk blocks holding arrays of free block numbers chained together.</li>
          </ul>
        </li>
        <li><strong>I-Node Table:</strong> An array of linear metadata records (index-nodes), pre-allocated across contiguous tracks. Every file and directory on the partition occupies exactly one slot in this table, indexed by a unique integer (the i-node number).</li>
        <li><strong>Root Directory:</strong> The top-level directory node (often bound to a hard-coded index, such as i-node 2 in ext2/ext3/ext4) from which the entire hierarchical namespace tree descends.</li>
        <li><strong>Data Blocks:</strong> The vast remainder of the partition volume dedicated to storing actual file content bytes and subdirectory entry tables.</li>
      </ol>

      <div class="figure-container">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure 4-5: Standard Unix/POSIX Disk Partition Layout</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 140" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <rect x="15" y="20" width="730" height="90" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5" rx="6"/>

          <rect x="25" y="30" width="70" height="70" fill="#e0f2fe" stroke="#38bdf8" stroke-width="1.2" rx="3"/>
          <text x="60" y="60" font-size="9" font-weight="700" fill="#0369a1" text-anchor="middle">Boot</text>
          <text x="60" y="74" font-size="8" fill="#0369a1" text-anchor="middle">Block</text>

          <rect x="100" y="30" width="90" height="70" fill="#fee2e2" stroke="#f87171" stroke-width="1.2" rx="3"/>
          <text x="145" y="60" font-size="9" font-weight="700" fill="#991b1b" text-anchor="middle">Superblock</text>
          <text x="145" y="74" font-size="7.5" fill="#7f1d1d" text-anchor="middle">Geometry / Magic</text>

          <rect x="195" y="30" width="110" height="70" fill="#fef3c7" stroke="#fbbf24" stroke-width="1.2" rx="3"/>
          <text x="250" y="60" font-size="9" font-weight="700" fill="#92400e" text-anchor="middle">Free Space</text>
          <text x="250" y="74" font-size="7.5" fill="#b45309" text-anchor="middle">Bitmap / Free List</text>

          <rect x="310" y="30" width="120" height="70" fill="#ecfdf5" stroke="#34d399" stroke-width="1.2" rx="3"/>
          <text x="370" y="60" font-size="9" font-weight="700" fill="#065f46" text-anchor="middle">i-Node Table</text>
          <text x="370" y="74" font-size="7.5" fill="#047857" text-anchor="middle">Pre-allocated Metadata</text>

          <rect x="435" y="30" width="75" height="70" fill="#ede9fe" stroke="#a78bfa" stroke-width="1.2" rx="3"/>
          <text x="472" y="60" font-size="9" font-weight="700" fill="#5b21b6" text-anchor="middle">Root Dir</text>
          <text x="472" y="74" font-size="7.5" fill="#6d28d9" text-anchor="middle">i-node #2</text>

          <rect x="515" y="30" width="220" height="70" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.2" rx="3"/>
          <text x="625" y="60" font-size="10" font-weight="700" fill="#334155" text-anchor="middle">Data Blocks Area</text>
          <text x="625" y="74" font-size="8" fill="#64748b" text-anchor="middle">File Content &amp; Subdirectories</text>
        </svg>
      </div>
    </div>

    <!-- Section 4.3.2: Implementing Files / Allocation Strategies -->
    <div class="card">
      <h2>4.3.2 Implementing Files: Allocation Strategies</h2>
      <p>
        The central design challenge of a file system is mapping a linear stream of logical file bytes into non-contiguous physical storage blocks:
      </p>
      <div class="callout">
        $$\text{Logical Address Stream } [0, 1, 2, \dots, \text{Size} - 1] \quad \xrightarrow{\text{Allocation Strategy}} \quad \text{Physical Disk Blocks } \{B_{k_1}, B_{k_2}, \dots\}$$
      </div>
      <p>
        Over the evolution of operating systems, four foundational allocation strategies have emerged:
      </p>

      <h3>1. Contiguous Allocation</h3>
      <p>
        Stores each file as a continuous run of disk blocks.
      </p>
      <ul>
        <li><strong>Advantages:</strong> Optimal sequential read/write performance. Accessing an entire file requires only one seek. Logical offsets map via simple addition ($B_{\text{phys}} = B_{\text{start}} + B_{\text{logic}}$).</li>
        <li><strong>Disadvantages:</strong> Severe <strong>external fragmentation</strong>. Compaction is expensive, and expanding an existing file requires relocating it if adjacent blocks are occupied.</li>
      </ul>

      <h3>2. Linked-List Allocation</h3>
      <p>
        Each file is a linked chain of physical blocks, where each block reserves a few bytes for a pointer to the next block.
      </p>
      <ul>
        <li><strong>Advantages:</strong> No external fragmentation. Any free block from the pool can be used immediately.</li>
        <li><strong>Disadvantages:</strong> Random access is slow ($O(N)$ sequential disk seeks). Pointers inside blocks break power-of-two sector alignments.</li>
      </ul>

      <h3>3. File Allocation Table (FAT)</h3>
      <p>
        Pointers are extracted from data blocks and stored in a centralized table residing in memory.
      </p>
      <ul>
        <li><strong>Advantages:</strong> Clean power-of-two data blocks. Random access is fast because chain traversal happens in RAM without mechanical head movements.</li>
        <li><strong>Disadvantages:</strong> Scalability limits. The entire table must remain in RAM; large modern drives require hundreds of megabytes or gigabytes of memory for the FAT table alone.</li>
      </ul>

      <h3>4. Index-Nodes (I-Nodes)</h3>
      <p>
        Associates each file with a dedicated metadata structure containing direct pointers and multi-level indirect pointers (single, double, triple).
      </p>
      <ul>
        <li><strong>Advantages:</strong> Fast random access, clean data blocks, and memory consumption that scales strictly with active open files rather than total volume capacity.</li>
      </ul>
    </div>

    <!-- Section 4.3.5: Log-Structured File Systems (LFS) -->
    <div class="card">
      <h2>4.3.5 Log-Structured File Systems (LFS)</h2>
      <p>
        Log-Structured File Systems (LFS) were developed by Mendel Rosenblum and John Ousterhout at UC Berkeley to solve an emerging hardware bottleneck: <strong>the growing performance disparity between CPU speed and mechanical disk seek times</strong>.
      </p>

      <h3>1. The Rationale: Read Caching vs. Write Bottlenecks</h3>
      <p>
        As computer memories grew, operating system page caches successfully satisfied a large percentage of file read requests directly from RAM. As a result, disk traffic became heavily dominated by <strong>writes</strong>. In traditional Unix filesystems (such as the Berkeley Fast File System), creating a small file requires multiple small, scattered synchronous writes:
      </p>
      <ol>
        <li>Write to directory data block (binding name).</li>
        <li>Write to directory i-node (updating modification timestamp).</li>
        <li>Write to new file i-node (allocating metadata).</li>
        <li>Write to free-space bitmap (marking blocks used).</li>
        <li>Write to actual file data block.</li>
      </ol>
      <p>
        Each of these distinct operations required a separate mechanical disk seek, causing physical drive throughput to drop below 5% of theoretical drive bandwidth.
      </p>

      <h3>2. The LFS Architecture: Everything is a Log</h3>
      <p>
        LFS eliminates random disk seeks by structuring the entire disk as an <strong>append-only circular log</strong>.
      </p>
      <ul>
        <li><strong>Segment Buffering:</strong> All writes (file data, updated i-nodes, directory entries) are accumulated in an in-memory segment buffer (typically 1 MB or 2 MB in size).</li>
        <li><strong>Sequential Flushes:</strong> When the buffer fills, the entire segment is flushed to disk in a single continuous sequential write, utilizing 100% of the drive's streaming bandwidth.</li>
        <li><strong>Floating I-Nodes &amp; The I-Node Map (imap):</strong> Because writes are appended to the head of the log, an i-node's physical disk location changes every time the file is updated. To avoid rewriting the parent directory whenever an i-node moves, LFS introduces the <strong>i-node map (<code>imap</code>)</strong>: a table translating invariant i-node numbers to their current physical disk positions.</li>
        <li><strong>Checkpoint Region:</strong> A fixed, well-known area on disk pointing to the latest fragments of the <code>imap</code>, updated periodically to establish clean recovery points.</li>
      </ul>

      <h3>3. Cleaning and Garbage Collection</h3>
      <p>
        Because files are updated by writing new versions to the log head rather than modifying data in place, earlier blocks become <strong>dead (stale)</strong>. To keep free contiguous space available, LFS runs a continuous background task called the <strong>Segment Cleaner</strong>:
      </p>
      <div class="callout">
        $$\text{Cleaner Workflow: } \quad \text{Read Segments with Dead Data} \;\longrightarrow\; \text{Identify Active Blocks via imap} \;\longrightarrow\; \text{Pack into New Segment} \;\longrightarrow\; \text{Reclaim Old Segments}$$
      </div>

      <div class="figure-container">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure 4-6: Log-Structured File System (Segment Flushing &amp; Cleaner Compaction)</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 170" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <!-- In-Memory Buffer -->
          <rect x="20" y="20" width="200" height="130" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" rx="4"/>
          <text x="120" y="42" font-size="10" font-weight="700" fill="#0284c7" text-anchor="middle">In-Memory Segment Buffer</text>

          <rect x="35" y="55" width="170" height="22" fill="#ffffff" stroke="#bae6fd" rx="3"/>
          <text x="120" y="70" font-size="8.5" fill="#0369a1" text-anchor="middle">Data Block A (File 1)</text>

          <rect x="35" y="82" width="170" height="22" fill="#ffffff" stroke="#bae6fd" rx="3"/>
          <text x="120" y="97" font-size="8.5" fill="#0369a1" text-anchor="middle">Data Block B (File 2)</text>

          <rect x="35" y="109" width="170" height="22" fill="#fef3c7" stroke="#fbbf24" rx="3"/>
          <text x="120" y="124" font-size="8.5" fill="#92400e" text-anchor="middle">Updated i-nodes &amp; imap slice</text>

          <!-- Sequential Flush Arrow -->
          <path d="M 220 85 L 290 85" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-blue)"/>
          <text x="255" y="78" font-size="7.5" font-weight="700" fill="#0284c7" text-anchor="middle">Sequential</text>
          <text x="255" y="100" font-size="7.5" font-weight="700" fill="#0284c7" text-anchor="middle">Flush (2 MB)</text>

          <!-- On-Disk Circular Log -->
          <rect x="290" y="20" width="450" height="130" fill="#f8fafc" stroke="#334155" stroke-width="1.5" rx="4"/>
          <text x="515" y="42" font-size="10" font-weight="700" fill="#0f172a" text-anchor="middle">Physical Disk Circular Log (Sequential Track Extents)</text>

          <!-- Segment 1 -->
          <rect x="305" y="55" width="130" height="80" fill="#ecfdf5" stroke="#059669" stroke-width="1.2" rx="3"/>
          <text x="370" y="72" font-size="8.5" font-weight="700" fill="#047857" text-anchor="middle">Segment 1 (Active)</text>
          <rect x="315" y="80" width="110" height="18" fill="#ffffff" stroke="#a7f3d0" rx="2"/>
          <text x="370" y="93" font-size="8" fill="#065f46" text-anchor="middle">Live Data Block A</text>
          <rect x="315" y="103" width="110" height="18" fill="#ffffff" stroke="#a7f3d0" rx="2"/>
          <text x="370" y="116" font-size="8" fill="#065f46" text-anchor="middle">i-node #10 &amp; imap</text>

          <!-- Segment 2 (Cleanable) -->
          <rect x="445" y="55" width="130" height="80" fill="#fee2e2" stroke="#dc2626" stroke-width="1.2" rx="3"/>
          <text x="510" y="72" font-size="8.5" font-weight="700" fill="#b91c1c" text-anchor="middle">Segment 2 (Fragmented)</text>
          <rect x="455" y="80" width="110" height="18" fill="#ffffff" stroke="#fca5a5" rx="2"/>
          <text x="510" y="93" font-size="8" fill="#991b1b" text-anchor="middle">DEAD Block (Stale)</text>
          <rect x="455" y="103" width="110" height="18" fill="#ffffff" stroke="#86efac" rx="2"/>
          <text x="510" y="116" font-size="8" fill="#065f46" text-anchor="middle">Live Block C (Migrate)</text>

          <!-- Segment Cleaner -->
          <rect x="585" y="55" width="140" height="80" fill="#fffbeb" stroke="#d97706" stroke-width="1.2" rx="3"/>
          <text x="655" y="72" font-size="8.5" font-weight="700" fill="#92400e" text-anchor="middle">Clean Segment Target</text>
          <text x="655" y="95" font-size="8" fill="#b45309" text-anchor="middle">Cleaner compacts live</text>
          <text x="655" y="110" font-size="8" fill="#b45309" text-anchor="middle">data &amp; reclaims free</text>
          <text x="655" y="125" font-size="8" fill="#b45309" text-anchor="middle">continuous space.</text>

          <defs>
            <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
            </marker>
          </defs>
        </svg>
      </div>
    </div>

    <!-- Section 4.3.6: Journaling File Systems -->
    <div class="card">
      <h2>4.3.6 Journaling File Systems</h2>
      <p>
        Traditional filesystems risk severe corruption if a system crashes or loses power in the middle of a metadata update sequence. A file append might allocate an i-node, write data, and update a directory entry; if power cuts between steps 2 and 3, the filesystem state becomes inconsistent.
      </p>

      <h3>1. The Consistency Problem and `fsck` Overhead</h3>
      <p>
        Early systems relied on utilities like <code>fsck</code> (File System Consistency Check) during reboot. The checker performs an exhaustive traversal of every directory, i-node, and allocation bitmap on the volume to locate orphaned blocks, link count discrepancies, and duplicate claims. On modern multi-terabyte storage arrays, an <code>fsck</code> run can take hours or days, during which the system remains offline.
      </p>

      <h3>2. The Journaling Architecture</h3>
      <p>
        Journaling solves this by borrowing the concept of an <strong>atomic transaction log</strong> from database management systems. Before making any changes to the active filesystem data structures on disk, the kernel writes a concise description of the intended changes to a dedicated disk region called the <strong>journal</strong> (or intent log).
      </p>

      <div class="figure-container">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure 4-7: Atomic Journaling Transaction State Pipeline</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 140" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <!-- Step 1: Journal Write -->
          <g transform="translate(30, 25)">
            <rect width="150" height="85" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" rx="4"/>
            <text x="75" y="24" font-size="9.5" font-weight="700" fill="#0284c7" text-anchor="middle">1. Journal Write</text>
            <text x="75" y="44" font-size="8" fill="#334155" text-anchor="middle">Write transaction record</text>
            <text x="75" y="58" font-size="8" fill="#334155" text-anchor="middle">(i-node, dir entry, bitmap)</text>
            <text x="75" y="72" font-size="8" fill="#0369a1" text-anchor="middle">to sequential log</text>
          </g>

          <path d="M 180 67 L 220 67" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-j)"/>

          <!-- Step 2: Journal Commit -->
          <g transform="translate(220, 25)">
            <rect width="150" height="85" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
            <text x="75" y="24" font-size="9.5" font-weight="700" fill="#047857" text-anchor="middle">2. Journal Commit</text>
            <text x="75" y="44" font-size="8" fill="#334155" text-anchor="middle">Write atomic COMMIT</text>
            <text x="75" y="58" font-size="8" fill="#334155" text-anchor="middle">marker to disk.</text>
            <text x="75" y="72" font-size="8" font-weight="700" fill="#059669" text-anchor="middle">Point of No Return</text>
          </g>

          <path d="M 370 67 L 410 67" stroke="#059669" stroke-width="2" marker-end="url(#arrow-j)"/>

          <!-- Step 3: Checkpoint -->
          <g transform="translate(410, 25)">
            <rect width="150" height="85" fill="#fffbeb" stroke="#d97706" stroke-width="1.5" rx="4"/>
            <text x="75" y="24" font-size="9.5" font-weight="700" fill="#b45309" text-anchor="middle">3. Checkpoint</text>
            <text x="75" y="44" font-size="8" fill="#334155" text-anchor="middle">Write changes to</text>
            <text x="75" y="58" font-size="8" fill="#334155" text-anchor="middle">permanent on-disk</text>
            <text x="75" y="72" font-size="8" fill="#92400e" text-anchor="middle">filesystem locations</text>
          </g>

          <path d="M 560 67 L 600 67" stroke="#d97706" stroke-width="2" marker-end="url(#arrow-j)"/>

          <!-- Step 4: Free Journal -->
          <g transform="translate(600, 25)">
            <rect width="130" height="85" fill="#f8fafc" stroke="#64748b" stroke-width="1.5" rx="4"/>
            <text x="65" y="24" font-size="9.5" font-weight="700" fill="#334155" text-anchor="middle">4. Release</text>
            <text x="65" y="44" font-size="8" fill="#64748b" text-anchor="middle">Invalidate transaction</text>
            <text x="65" y="58" font-size="8" fill="#64748b" text-anchor="middle">in journal circular log.</text>
            <text x="65" y="72" font-size="8" fill="#059669" text-anchor="middle">Space Reclaimed</text>
          </g>

          <defs>
            <marker id="arrow-j" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
            </marker>
          </defs>
        </svg>
      </div>

      <h3>3. Crash Recovery Mechanics</h3>
      <p>
        When the operating system reboots following a sudden power failure, it inspects only the journal, avoiding a full-disk sweep:
      </p>
      <ul>
        <li><strong>Crash occurs before Step 2 (Commit):</strong> The log contains an incomplete transaction without a commit marker. The kernel discards the transaction, rolling back any partial metadata. Zero corruption occurs.</li>
        <li><strong>Crash occurs after Step 2 (Commit) but before Step 4 (Release):</strong> The transaction is fully committed in the log. The recovery routine <strong>replays (redoes)</strong> the logged operations, writing them to their permanent disk blocks. The filesystem returns to a 100% consistent state in fractions of a second.</li>
      </ul>
      <p>
        Modern filesystems (such as Linux <code>ext4</code>, Windows <code>NTFS</code>, and macOS <code>APFS</code>) typically operate in <strong>Ordered Mode</strong> (journaling metadata only, while ensuring user data blocks are flushed prior to committing the metadata transaction), balancing integrity with write performance.
      </p>
    </div>

    <!-- Section 4.3.7: Flash-Based File Systems & Solid-State Drives -->
    <div class="card">
      <h2>4.3.7 Flash-Based File Systems &amp; Solid-State Drives (SSDs)</h2>
      <p>
        Solid-State Drives (SSDs) and raw NAND flash memory devices differ fundamentally from magnetic spinning disks. Flash memory has no moving read/write heads, rotational delays, or mechanical seek latency, but introduces distinct physical constraints:
      </p>

      <h3>1. The Asymmetric Read / Write / Erase Granularity</h3>
      <ul>
        <li><strong>Page Granularity (Reads &amp; Writes):</strong> NAND flash is organized into pages (typically 4 KB to 16 KB). Read and program (write) operations occur at page granularity.</li>
        <li><strong>Block Granularity (Erase Only):</strong> Pages cannot be rewritten in place. A page that contains data cannot be overwritten until the entire surrounding <strong>Erase Block</strong> (typically 128 to 512 pages, totaling 2 MB to 8 MB) is completely erased. Erasing resets all bits to 1, after which pages can be programmed (switching bits from 1 to 0).</li>
      </ul>

      <h3>2. The Flash Translation Layer (FTL)</h3>
      <p>
        Because legacy operating systems expect a traditional hard drive interface (reading and overwriting 512-byte or 4 KB sectors in place), modern SSDs embed a specialized micro-controller executing firmware called the <strong>Flash Translation Layer (FTL)</strong>:
      </p>
      <ul>
        <li><strong>Out-of-Place Writes:</strong> When an operating system overwrites Logical Block Address (LBA) 500, the FTL does not erase the existing physical page. Instead, it programs an unallocated free page elsewhere on the flash media, updates an internal translation mapping table, and marks the old page as <strong>invalid (dead)</strong>.</li>
        <li><strong>Garbage Collection:</strong> As free blocks diminish, the controller reads valid pages from a fragmented block, copies them to a new block, and erases the old block to restore free capacity.</li>
        <li><strong>Wear-Leveling:</strong> Flash cells degrade physically after a finite number of program/erase cycles (often 1,000 to 10,000 cycles for MLC/TLC flash). The FTL actively distributes writes evenly across all physical cells, swapping cold (static) data with hot (frequently written) data to prevent premature drive failure.</li>
      </ul>

      <h3>3. The Operating System `TRIM` Command</h3>
      <p>
        When a user deletes a file, a traditional filesystem simply updates its internal metadata (marking the directory slot or i-node as free), issuing no write command to the underlying sectors. To the SSD controller, those sectors appear to contain active, valid data, forcing the garbage collector to waste write cycles migrating dead blocks.
      </p>
      <div class="callout">
        <strong>The TRIM Solution:</strong> Modern operating systems use the ATA <code>TRIM</code> (or NVMe <code>Deallocate</code>) command to explicitly notify the SSD controller when sector ranges are unlinked. The FTL marks those physical pages invalid immediately, eliminating unnecessary rewrite cycles during garbage collection and preserving SSD endurance.
      </div>
    </div>

    <!-- Section 4.3.8: Virtual File Systems (VFS) -->
    <div class="card">
      <h2>4.3.8 Virtual File Systems (VFS)</h2>
      <p>
        Modern operating systems frequently mount multiple distinct filesystems simultaneously on the same machine: an <code>ext4</code> partition for root, a <code>FAT32</code> or <code>exFAT</code> flash drive, an <code>NTFS</code> external drive, and a network-attached <code>NFS</code> share.
      </p>
      <p>
        Pioneered by Sun Microsystems in 1985, the <strong>Virtual File System (VFS)</strong> provides an object-oriented kernel abstraction layer that hides the structural differences of concrete filesystems behind a single, uniform interface.
      </p>

      <div class="figure-container">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure 4-8: The Virtual File System (VFS) Kernel Architecture</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 180" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <!-- User Space -->
          <rect x="20" y="15" width="720" height="30" fill="#f8fafc" stroke="#94a3b8" stroke-dasharray="3,3" rx="4"/>
          <text x="380" y="34" font-size="10" font-weight="700" fill="#0f172a" text-anchor="middle">User Applications (Standard POSIX Calls: open(), read(), write(), close())</text>

          <!-- System Call Interface -->
          <line x1="380" y1="45" x2="380" y2="60" stroke="#0284c7" stroke-width="1.5" marker-end="url(#arrow-vfs)"/>

          <!-- VFS Layer -->
          <rect x="20" y="60" width="720" height="40" fill="#0284c7" stroke="#0369a1" rx="4"/>
          <text x="380" y="84" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">Virtual File System (VFS) Layer — Uniform Inode / Dentry Abstractions</text>

          <!-- Dispatch lines -->
          <path d="M 120 100 L 120 120" stroke="#0284c7" stroke-width="1.5" marker-end="url(#arrow-vfs)"/>
          <path d="M 295 100 L 295 120" stroke="#0284c7" stroke-width="1.5" marker-end="url(#arrow-vfs)"/>
          <path d="M 470 100 L 470 120" stroke="#0284c7" stroke-width="1.5" marker-end="url(#arrow-vfs)"/>
          <path d="M 640 100 L 640 120" stroke="#0284c7" stroke-width="1.5" marker-end="url(#arrow-vfs)"/>

          <!-- Concrete File Systems -->
          <rect x="50" y="120" width="140" height="42" fill="#ecfdf5" stroke="#059669" rx="3"/>
          <text x="120" y="137" font-size="9.5" font-weight="700" fill="#047857" text-anchor="middle">ext4 Driver</text>
          <text x="120" y="151" font-size="8" fill="#065f46" text-anchor="middle">Local Linux Block Extents</text>

          <rect x="225" y="120" width="140" height="42" fill="#ecfdf5" stroke="#059669" rx="3"/>
          <text x="295" y="137" font-size="9.5" font-weight="700" fill="#047857" text-anchor="middle">NTFS / FAT Driver</text>
          <text x="295" y="151" font-size="8" fill="#065f46" text-anchor="middle">Windows Compatibility</text>

          <rect x="400" y="120" width="140" height="42" fill="#ecfdf5" stroke="#059669" rx="3"/>
          <text x="470" y="137" font-size="9.5" font-weight="700" fill="#047857" text-anchor="middle">NFS Driver</text>
          <text x="470" y="151" font-size="8" fill="#065f46" text-anchor="middle">Network RPC Protocols</text>

          <rect x="575" y="120" width="140" height="42" fill="#ecfdf5" stroke="#059669" rx="3"/>
          <text x="645" y="137" font-size="9.5" font-weight="700" fill="#047857" text-anchor="middle">APFS / ZFS Driver</text>
          <text x="645" y="151" font-size="8" fill="#065f46" text-anchor="middle">Copy-on-Write Storage</text>

          <defs>
            <marker id="arrow-vfs" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
            </marker>
          </defs>
        </svg>
      </div>

      <h3>Core Object Model of VFS</h3>
      <p>
        The VFS architecture standardizes operations across four primary object structures:
      </p>
      <ul>
        <li><strong>Superblock Object:</strong> Represents an entire mounted filesystem. Contains pointers to filesystem geometry and a table of superblock operations (e.g., <code>alloc_inode</code>, <code>write_super</code>).</li>
        <li><strong>Inode Object (v-node):</strong> Represents a specific file or directory in memory. Contains file attributes and the table of allowable operations (e.g., <code>create</code>, <code>link</code>, <code>mkdir</code>).</li>
        <li><strong>Dentry Object (Directory Entry):</strong> Represents a specific path component (e.g., <code>home</code>, <code>alice</code>). VFS caches dentries in a hash table (the <em>dcache</em>) to rapidly resolve path traversals without re-reading physical directory blocks.</li>
        <li><strong>File Object:</strong> Represents an active open file descriptor held by a process. Stores the current read/write offset pointer and operational flags.</li>
      </ul>
    </div>

    <!-- Interactive Advanced Systems Simulator (Crash Recovery & LFS Cleaning) -->
    <div class="card sim-card">
      <div class="sim-header">
        <span class="sim-title">Interactive Advanced Systems Simulator</span>
        <span style="color:#94a3b8; font-size:0.75rem; font-family:var(--font-mono);">Journaling &amp; LFS Mechanisms</span>
      </div>

      <p style="color:#cbd5e1; font-size:0.86rem;">
        Simulate crash recovery in a Journaling Filesystem or trigger the Segment Cleaning and Compaction routine in a Log-Structured Filesystem (LFS).
      </p>

      <div class="sim-controls">
        <button class="sim-btn active-btn" id="btn-mode-journal" onclick="setAdvMode('journal')">1. Journaling Crash &amp; Recovery</button>
        <button class="sim-btn" id="btn-mode-lfs" onclick="setAdvMode('lfs')">2. LFS Segment Cleaning</button>
      </div>

      <!-- Mode-Specific Action Controls -->
      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <button class="sim-btn" id="btnActionA" onclick="runAdvAction('A')">Step 1: Write Journal Entry</button>
        <button class="sim-btn" id="btnActionB" onclick="runAdvAction('B')">Step 2: Commit Transaction</button>
        <button class="sim-btn" id="btnActionC" onclick="runAdvAction('C')" style="background:#b91c1c; border-color:#ef4444; color:#fff;">Trigger Sudden Power Cut!</button>
        <button class="sim-btn" id="btnActionD" onclick="runAdvAction('D')" style="background:#059669; border-color:#34d399; color:#fff;">Reboot &amp; Replay</button>
      </div>

      <div class="sim-grid">
        <div class="sim-panel">
          <div class="sim-panel-title" id="advPanelTitleA">Journal Log State</div>
          <div class="sim-row"><span>Transaction #104:</span><span class="val" id="advRow1">INACTIVE</span></div>
          <div class="sim-row"><span>Commit Record:</span><span class="val" id="advRow2">UNCOMMITTED</span></div>
          <div class="sim-row"><span>Checkpoint State:</span><span class="val" id="advRow3">PENDING</span></div>
          <div class="sim-row"><span>Recovery Strategy:</span><span class="val" id="advRow4">Normal Operation</span></div>
        </div>

        <div class="sim-panel">
          <div class="sim-panel-title" id="advPanelTitleB">Filesystem Metadata Status</div>
          <div class="sim-row"><span>Directory Entry:</span><span class="val" id="advRow5">Clean</span></div>
          <div class="sim-row"><span>i-Node Invariant:</span><span class="val" id="advRow6">Consistent</span></div>
          <div class="sim-row"><span>Free Block Bitmap:</span><span class="val" id="advRow7">Verified</span></div>
          <div class="sim-row"><span>Volume Status:</span><span class="val" id="advRow8">MOUNTED</span></div>
        </div>
      </div>

      <div class="sim-console" id="advConsole">$ Subsystem initialized. Select actions above to simulate atomic transactions...</div>
    </div>

  </div>

  <script>
    // --- Advanced Simulator Logic (Journaling & LFS) ---
    let advMode = 'journal';
    let journalState = {
      written: false,
      committed: false,
      crashed: false,
      checkpointed: false
    };

    let lfsState = {
      dirtyBlocks: 4,
      freeSegments: 2,
      cleanedSegments: 0
    };

    function setAdvMode(mode) {
      advMode = mode;
      document.getElementById('btn-mode-journal').classList.toggle('active-btn', mode === 'journal');
      document.getElementById('btn-mode-lfs').classList.toggle('active-btn', mode === 'lfs');

      const bA = document.getElementById('btnActionA');
      const bB = document.getElementById('btnActionB');
      const bC = document.getElementById('btnActionC');
      const bD = document.getElementById('btnActionD');

      if (mode === 'journal') {
        document.getElementById('advPanelTitleA').textContent = "Journal Log State";
        document.getElementById('advPanelTitleB').textContent = "Filesystem Metadata Status";
        bA.textContent = "Step 1: Write Journal Entry";
        bB.textContent = "Step 2: Commit Transaction";
        bC.textContent = "Trigger Sudden Power Cut!";
        bD.textContent = "Reboot & Replay";
        resetJournalUI();
      } else {
        document.getElementById('advPanelTitleA').textContent = "LFS Circular Log State";
        document.getElementById('advPanelTitleB').textContent = "Segment Cleaner Metrics";
        bA.textContent = "Write Log Burst (2 MB)";
        bB.textContent = "Update Existing File";
        bC.textContent = "Run Segment Cleaner";
        bC.style.background = "#0284c7";
        bC.style.borderColor = "#38bdf8";
        bD.textContent = "Reset Log";
        bD.style.background = "#334155";
        bD.style.borderColor = "#475569";
        resetLfsUI();
      }
    }

    function resetJournalUI() {
      journalState = { written: false, committed: false, crashed: false, checkpointed: false };
      document.getElementById('advRow1').textContent = "INACTIVE";
      document.getElementById('advRow2').textContent = "UNCOMMITTED";
      document.getElementById('advRow3').textContent = "PENDING";
      document.getElementById('advRow4').textContent = "Normal Operation";
      document.getElementById('advRow5').textContent = "Clean";
      document.getElementById('advRow6').textContent = "Consistent";
      document.getElementById('advRow7').textContent = "Verified";
      document.getElementById('advRow8').textContent = "MOUNTED";
      document.getElementById('advConsole').textContent = "$ Journaling subsystem online. Click 'Step 1: Write Journal Entry' to begin transaction...";
    }

    function resetLfsUI() {
      lfsState = { dirtyBlocks: 4, freeSegments: 2, cleanedSegments: 0 };
      document.getElementById('advRow1').textContent = "Active Log Head (Seg #1)";
      document.getElementById('advRow2').textContent = "4 Dead Blocks Present";
      document.getElementById('advRow3').textContent = "2 Free Clean Segments";
      document.getElementById('advRow4').textContent = "Continuous Append";
      document.getElementById('advRow5').textContent = "imap Cached in RAM";
      document.getElementById('advRow6').textContent = "Zero Seeks (Streaming)";
      document.getElementById('advRow7').textContent = "Cleaner Idle";
      document.getElementById('advRow8').textContent = "OPERATIONAL";
      document.getElementById('advConsole').textContent = "$ LFS online. Writes are buffered in memory and appended to the head of the log.";
    }

    function runAdvAction(act) {
      const logEl = document.getElementById('advConsole');
      const r1 = document.getElementById('advRow1');
      const r2 = document.getElementById('advRow2');
      const r3 = document.getElementById('advRow3');
      const r4 = document.getElementById('advRow4');
      const r5 = document.getElementById('advRow5');
      const r6 = document.getElementById('advRow6');
      const r7 = document.getElementById('advRow7');
      const r8 = document.getElementById('advRow8');

      if (advMode === 'journal') {
        if (act === 'A') {
          journalState.written = true;
          journalState.committed = false;
          r1.textContent = "WRITTEN (Uncommitted)";
          r2.textContent = "NO COMMIT RECORD";
          r3.textContent = "HOLDING";
          r4.textContent = "Rollback if Crashed";
          logEl.textContent = "$ journal_write(Tx #104):\n[Journal] Wrote intended modifications (inode #42, dentry 'file.txt', block bitmap) to sequential journal.\n[Notice] Permanent filesystem tables on disk are NOT yet altered.";
        } else if (act === 'B') {
          if (!journalState.written) {
            logEl.textContent = "$ Error: No transaction to commit. Run Step 1 first.";
            return;
          }
          journalState.committed = true;
          r1.textContent = "COMMITTED";
          r2.textContent = "COMMIT RECORD ON DISK";
          r3.textContent = "Checkpointing...";
          r4.textContent = "Guaranteed Redo";
          logEl.textContent = "$ journal_commit(Tx #104):\n[Journal] Appended COMMIT sector to disk log.\n[Point of No Return] Transaction is now guaranteed to survive crashes.";
        } else if (act === 'C') {
          journalState.crashed = true;
          r8.textContent = "POWER CUT (OFFLINE)";
          r5.textContent = "DIRTY";
          r6.textContent = "UNVERIFIED";
          r7.textContent = "DIRTY";
          logEl.textContent = "$ [SYSTEM CRASH] Power interrupted suddenly!\n[Alert] Memory cache lost. Volatile state vanished.\n[Action Required] Reboot to test crash recovery.";
        } else if (act === 'D') {
          if (!journalState.crashed) {
            logEl.textContent = "$ System is already running normally. Click 'Trigger Sudden Power Cut!' first to simulate recovery.";
            return;
          }
          r8.textContent = "RECOVERED & MOUNTED";
          r5.textContent = "Consistent";
          r6.textContent = "Consistent";
          r7.textContent = "Verified";

          if (journalState.committed) {
            r4.textContent = "Replayed Committed Tx";
            logEl.textContent = "$ mount_volume():\n[Recovery] Inspecting journal log...\n[Found] Fully committed Tx #104.\n[Redo] Fast-forwarded changes to permanent disk locations.\n[Success] Filesystem restored to 100% consistent state in 0.04 seconds (Zero fsck needed!).";
          } else {
            r4.textContent = "Discarded Uncommitted Tx";
            logEl.textContent = "$ mount_volume():\n[Recovery] Inspecting journal log...\n[Found] Incomplete transaction without COMMIT marker.\n[Rollback] Discarded partial journal fragments.\n[Success] Consistency preserved with zero orphan corruption.";
          }
          journalState.crashed = false;
        }
      } else {
        // LFS Simulator Mode
        if (act === 'A') {
          logEl.textContent = "$ lfs_flush_segment():\n[LFS] Flushed 2 MB segment buffer sequentially to log head.\n[I/O Efficiency] 100% disk bandwidth utilized; zero random mechanical seeks.";
        } else if (act === 'B') {
          lfsState.dirtyBlocks += 2;
          r2.textContent = `${lfsState.dirtyBlocks} Dead Blocks Present`;
          logEl.textContent = "$ lfs_update_file(\"data.db\"):\n[LFS Out-of-Place Write] Wrote new data blocks to log head.\n[imap] Updated i-node mapping table to point to new block locations.\n[Garbage] Old block locations marked DEAD (stale).";
        } else if (act === 'C') {
          lfsState.cleanedSegments++;
          lfsState.dirtyBlocks = 0;
          lfsState.freeSegments++;
          r2.textContent = "0 Dead Blocks (Clean)";
          r3.textContent = `${lfsState.freeSegments} Free Clean Segments`;
          r7.textContent = `Cleaned Seg #${lfsState.cleanedSegments}`;
          logEl.textContent = `$ lfs_clean_segment():\n[Cleaner] Scanned fragmented segment -> Identified live blocks via imap.\n[Compaction] Packed live blocks into current active segment.\n[Reclaimed] Recycled segment, yielding contiguous free space.`;
        } else if (act === 'D') {
          resetLfsUI();
        }
      }
    }
  </script>
</body>
</html>
"""

COMMIT_MSG = """Expand sections 4.3.5-4.3.8 with advanced FS theory, SVGs, and simulator

Update week10-file-management/03-filesystem-implementation.html to expand
LFS, Journaling, Flash/SSDs, and VFS into distinct sections with custom
SVGs and an interactive crash recovery and segment cleaning simulator."""

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
    target_file = os.path.join(target_dir, "03-filesystem-implementation.html")

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Wrote updated module file 03-filesystem-implementation.html to {target_file}")

    run_git_step(["git", "add", target_file], "Staging updated 03-filesystem-implementation.html")
    run_git_step(["git", "commit", "-a", "-m", COMMIT_MSG], "Committing changes")
    run_git_step(["git", "push", "origin", "main"], "Pushing main to origin")
    print("--> Module 03 Advanced File Systems update successfully deployed!")

if __name__ == "__main__":
    deploy_module()
