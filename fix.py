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
          <!-- Disk container -->
          <rect x="15" y="20" width="730" height="90" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5" rx="6"/>

          <!-- Boot Block -->
          <rect x="25" y="30" width="70" height="70" fill="#e0f2fe" stroke="#38bdf8" stroke-width="1.2" rx="3"/>
          <text x="60" y="60" font-size="9" font-weight="700" fill="#0369a1" text-anchor="middle">Boot</text>
          <text x="60" y="74" font-size="8" fill="#0369a1" text-anchor="middle">Block</text>

          <!-- Superblock -->
          <rect x="100" y="30" width="90" height="70" fill="#fee2e2" stroke="#f87171" stroke-width="1.2" rx="3"/>
          <text x="145" y="60" font-size="9" font-weight="700" fill="#991b1b" text-anchor="middle">Superblock</text>
          <text x="145" y="74" font-size="7.5" fill="#7f1d1d" text-anchor="middle">Geometry / Magic</text>

          <!-- Free Space Mgmt -->
          <rect x="195" y="30" width="110" height="70" fill="#fef3c7" stroke="#fbbf24" stroke-width="1.2" rx="3"/>
          <text x="250" y="60" font-size="9" font-weight="700" fill="#92400e" text-anchor="middle">Free Space</text>
          <text x="250" y="74" font-size="7.5" fill="#b45309" text-anchor="middle">Bitmap / Free List</text>

          <!-- i-node Table -->
          <rect x="310" y="30" width="120" height="70" fill="#ecfdf5" stroke="#34d399" stroke-width="1.2" rx="3"/>
          <text x="370" y="60" font-size="9" font-weight="700" fill="#065f46" text-anchor="middle">i-Node Table</text>
          <text x="370" y="74" font-size="7.5" fill="#047857" text-anchor="middle">Pre-allocated Metadata</text>

          <!-- Root Directory -->
          <rect x="435" y="30" width="75" height="70" fill="#ede9fe" stroke="#a78bfa" stroke-width="1.2" rx="3"/>
          <text x="472" y="60" font-size="9" font-weight="700" fill="#5b21b6" text-anchor="middle">Root Dir</text>
          <text x="472" y="74" font-size="7.5" fill="#6d28d9" text-anchor="middle">i-node #2</text>

          <!-- Data Blocks -->
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
        The central design challenge of a file system is mapping a linear stream of logical file bytes:
      </p>
      <div class="callout">
        $$\text{Logical Address Stream } [0, 1, 2, \dots, \text{Size} - 1] \quad \xrightarrow{\text{Allocation Strategy}} \quad \text{Physical Disk Blocks } \{B_{k_1}, B_{k_2}, \dots\}$$
      </div>
      <p>
        Over the evolution of operating systems, four foundational allocation strategies have been developed, each presenting distinct performance tradeoffs between sequential throughput, random-access latency, and disk space fragmentation.
      </p>

      <h3>1. Contiguous Allocation</h3>
      <p>
        Stores each file as a contiguous sequence of physical disk blocks. For example, a 20 KB file using 4 KB blocks starting at block 100 occupies blocks 100, 101, 102, 103, and 104.
      </p>
      <ul>
        <li><strong>Advantages:</strong> Read/write performance is optimal. Accessing an entire file requires only a single disk seek operation. Successive blocks stream beneath the drive read/write head without rotational delay. Directory entries need only two integers: starting block and length.</li>
        <li><strong>Disadvantages:</strong> Suffers from severe <strong>external fragmentation</strong>. As files are created and deleted over time, the free disk space becomes fragmented into small gaps. Compaction is expensive. Furthermore, files cannot easily grow: appending to a file requires relocating the entire file if the adjacent block is already occupied.</li>
        <li><strong>Modern Context:</strong> Standard in read-only optical media (CD-ROMs, DVDs via ISO 9660) where file sizes are permanently known in advance. Also used in high-performance streaming or continuous recording setups.</li>
      </ul>

      <h3>2. Linked-List Allocation</h3>
      <p>
        Each file is represented as a linked list of disk blocks. The directory entry stores the address of the first block. Inside each block, a small header (e.g., 4 bytes) stores a pointer to the next physical block in the sequence.
      </p>
      <ul>
        <li><strong>Advantages:</strong> Eliminates external fragmentation entirely. Any free block from the pool can be appended to any file without relocation. Directory entries only store the first block pointer.</li>
        <li><strong>Disadvantages:</strong> Random access is slow: retrieving logical block $N$ requires traversing and reading all $N-1$ preceding blocks from disk sequentially. Furthermore, storing pointers inside data blocks wastes space (e.g., 4092 bytes data + 4 bytes pointer), breaking standard power-of-two buffer alignments required by hardware controllers.</li>
      </ul>

      <h3>3. File Allocation Table (FAT)</h3>
      <p>
        Takes the linked-list concept and removes pointers from data blocks, placing them in an in-memory table called the <strong>File Allocation Table</strong>.
      </p>
      <ul>
        <li><strong>Mechanism:</strong> The table contains an entry for every physical cluster on disk. The directory entry stores the starting cluster number. The table entry at index $k$ points to the next cluster in the chain, or holds an End-of-File (EOF) marker.</li>
        <li><strong>Advantages:</strong> Full block capacity is preserved for user data (power-of-two alignment). Random access is fast because the chain can be traversed in system memory without issuing mechanical disk seeks.</li>
        <li><strong>Disadvantages:</strong> Scalability limits. The entire allocation table must reside in RAM to deliver acceptable access performance. On a 1 TB drive with 4 KB clusters ($2^{28}$ clusters), a 32-bit FAT table requires over 1 GB of non-pageable memory.</li>
      </ul>

      <h3>4. Index-Nodes (I-Nodes)</h3>
      <p>
        Associates each file with a dedicated metadata structure known as an <strong>i-node (Index-Node)</strong>. Rather than maintaining a global table in memory, the index structure is stored with the file itself.
      </p>
      <ul>
        <li><strong>Multi-Level Indirect Addressing:</strong> A standard Unix i-node contains:
          <ul>
            <li>12 <strong>Direct Pointers:</strong> Address the first 12 data blocks directly. Small files (up to 48 KB with 4 KB blocks) incur zero indirect lookup overhead.</li>
            <li>1 <strong>Single Indirect Pointer:</strong> Points to a block containing an array of direct block addresses (adds $1024 \times 4\text{ KB} = 4\text{ MB}$).</li>
            <li>1 <strong>Double Indirect Pointer:</strong> Points to a block containing an array of indirect block pointers (adds $1024 \times 1024 \times 4\text{ KB} = 4\text{ GB}$).</li>
            <li>1 <strong>Triple Indirect Pointer:</strong> Supports files exceeding 4 TB.</li>
          </ul>
        </li>
        <li><strong>Memory Efficiency:</strong> An i-node is loaded into RAM only when its corresponding file is open, making memory consumption proportional to the number of active open files rather than total disk capacity.</li>
      </ul>

      <!-- Comparison Matrix -->
      <h3>Comparison of File Allocation Strategies</h3>
      <table>
        <thead>
          <tr>
            <th>Strategy</th>
            <th>Sequential Access</th>
            <th>Random Access</th>
            <th>Space Efficiency</th>
            <th>Fragmentation</th>
            <th>Primary Limitation</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Contiguous</strong></td>
            <td>Optimal (Single seek)</td>
            <td>Fast ($O(1)$ arithmetic)</td>
            <td>High (No pointers)</td>
            <td>Severe External</td>
            <td>Files cannot grow easily; compaction cost</td>
          </tr>
          <tr>
            <td><strong>Linked List</strong></td>
            <td>Good</td>
            <td>Slow ($O(N)$ disk seeks)</td>
            <td>Unaligned (Pointer in block)</td>
            <td>None External; Internal</td>
            <td>Slow random access; pointer corruption vulnerability</td>
          </tr>
          <tr>
            <td><strong>FAT Table</strong></td>
            <td>Good</td>
            <td>Fast (RAM traversal)</td>
            <td>Good (Clean data blocks)</td>
            <td>None External; Internal</td>
            <td>Entire table must reside in memory; scale limits</td>
          </tr>
          <tr>
            <td><strong>I-Nodes</strong></td>
            <td>Good</td>
            <td>Fast ($O(1)$ to $O(3)$ lookups)</td>
            <td>High (Scales per open file)</td>
            <td>None External; Internal</td>
            <td>Indirect block traversal latency on very large files</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Interactive Allocation Visualizer & Address Translation Sandbox -->
    <div class="card sim-card">
      <div class="sim-header">
        <span class="sim-title">Interactive Allocation Model &amp; Offset Translator</span>
        <span style="color:#94a3b8; font-size:0.75rem; font-family:var(--font-mono);">Tanenbaum &sect;4.3.2 Simulator</span>
      </div>

      <p style="color:#cbd5e1; font-size:0.86rem;">
        Select an allocation model below and adjust the logical file byte offset to observe how the operating system translates logical file positions into physical disk blocks and calculates required I/O operations.
      </p>

      <div class="sim-controls">
        <button class="sim-btn active-btn" id="btn-alloc-inode" onclick="selectAllocModel('inode')">1. I-Node (Unix Multi-Level)</button>
        <button class="sim-btn" id="btn-alloc-fat" onclick="selectAllocModel('fat')">2. FAT (Cluster Chaining)</button>
        <button class="sim-btn" id="btn-alloc-linked" onclick="selectAllocModel('linked')">3. Linked-List (Block Pointers)</button>
        <button class="sim-btn" id="btn-alloc-contiguous" onclick="selectAllocModel('contiguous')">4. Contiguous (Run Extents)</button>
      </div>

      <div style="display:flex; align-items:center; gap:12px; background:#020617; border:1px solid #1e293b; padding:10px 14px; border-radius:6px; font-family:var(--font-mono); font-size:0.82rem;">
        <span style="color:#fbbf24; font-weight:700;">Target Byte Offset:</span>
        <input type="range" id="offsetSlider" min="0" max="65536" step="1024" value="16384" oninput="updateOffset(this.value)" style="flex-grow:1; cursor:pointer;" />
        <span id="offsetDisplay" style="color:#38bdf8; font-weight:700; width:90px; text-align:right;">16,384 B</span>
      </div>

      <div class="sim-grid">
        <div class="sim-panel">
          <div class="sim-panel-title">Logical Address Translation</div>
          <div class="sim-row"><span>Logical Block Index:</span><span class="val" id="resLogicBlock">Block #4</span></div>
          <div class="sim-row"><span>Block Offset:</span><span class="val" id="resBlockOffset">0 Bytes</span></div>
          <div class="sim-row"><span>Physical Disk Block:</span><span class="val" id="resPhysBlock">Sector 1024</span></div>
          <div class="sim-row"><span>Address Strategy:</span><span class="val" id="resStrategy">Direct Pointer</span></div>
        </div>

        <div class="sim-panel">
          <div class="sim-panel-title">Performance &amp; Memory Metrics</div>
          <div class="sim-row"><span>Mechanical Disk Seeks:</span><span class="val" id="resSeeks">1 Seek</span></div>
          <div class="sim-row"><span>RAM Footprint:</span><span class="val" id="resRam">128 Bytes (Open File)</span></div>
          <div class="sim-row"><span>Data Alignment:</span><span class="val" id="resAlign">Clean (4096 B / Block)</span></div>
          <div class="sim-row"><span>External Fragmentation:</span><span class="val" id="resFrag">Zero (Any block allocable)</span></div>
        </div>
      </div>

      <div class="sim-console" id="allocConsole">$ Translation engine initialized. Ready to simulate offset resolution...</div>
    </div>

    <!-- Section 4.3.3 to 4.3.8: Overview of Advanced Implementations -->
    <div class="card">
      <h2>4.3.5 &ndash; 4.3.8 Advanced File Systems (LFS, Journaling, Flash, VFS)</h2>
      <p>
        Modern workloads require specialized architectures beyond basic block tables:
      </p>
      <ul>
        <li>
          <strong>Log-Structured File Systems (LFS):</strong> Capitalizes on large main-memory caches. Since most reads are satisfied from cache, disk traffic is dominated by writes. LFS structures the entire disk as an append-only log, batching small random writes into large sequential segments to eliminate disk head seek latency.
        </li>
        <li>
          <strong>Journaling File Systems:</strong> Protects filesystem consistency across sudden crashes (e.g., power loss). Critical metadata modifications are written to an idempotent sequential journal on disk before physical directory or i-node tables are updated. Upon reboot, the system replays or rolls back the log, recovering in seconds rather than running exhaustive disk-wide checks (such as <code>fsck</code>).
        </li>
        <li>
          <strong>Flash-Based File Systems (SSDs):</strong> Flash memory cells cannot be overwritten in place without first erasing an entire block (typically 128 KB to 2 MB). Storage devices utilize a <strong>Flash Translation Layer (FTL)</strong> to manage wear-leveling, garbage collection, and out-of-place writes, supported by the operating system's <code>TRIM</code> command.
        </li>
        <li>
          <strong>Virtual File Systems (VFS):</strong> An object-oriented abstraction layer within the kernel. VFS exposes uniform abstract data structures (superblock, inode, dentry, file) and function pointer tables, allowing user-space POSIX calls (<code>read</code>, <code>write</code>, <code>open</code>) to seamlessly interact with heterogeneous local (ext4, NTFS, FAT) and remote network filesystems (NFS, SMB).
        </li>
      </ul>
    </div>

  </div>

  <script>
    let currentModel = 'inode';
    let currentByteOffset = 16384;
    const BLOCK_SIZE = 4096;

    function selectAllocModel(model) {
      currentModel = model;
      const btns = ['inode', 'fat', 'linked', 'contiguous'];
      btns.forEach(b => {
        const btn = document.getElementById(`btn-alloc-${b}`);
        if (b === model) {
          btn.classList.add('active-btn');
        } else {
          btn.classList.remove('active-btn');
        }
      });
      recomputeTranslation();
    }

    function updateOffset(val) {
      currentByteOffset = parseInt(val, 10);
      document.getElementById('offsetDisplay').textContent = Number(val).toLocaleString() + " B";
      recomputeTranslation();
    }

    function recomputeTranslation() {
      const logicalBlock = Math.floor(currentByteOffset / BLOCK_SIZE);
      const blockOffset = currentByteOffset % BLOCK_SIZE;

      document.getElementById('resLogicBlock').textContent = `Block #${logicalBlock}`;
      document.getElementById('resBlockOffset').textContent = `${blockOffset} Bytes`;

      const physEl = document.getElementById('resPhysBlock');
      const stratEl = document.getElementById('resStrategy');
      const seeksEl = document.getElementById('resSeeks');
      const ramEl = document.getElementById('resRam');
      const alignEl = document.getElementById('resAlign');
      const fragEl = document.getElementById('resFrag');
      const consoleEl = document.getElementById('allocConsole');

      if (currentModel === 'inode') {
        alignEl.textContent = "Clean (4096 B / Block)";
        fragEl.textContent = "Zero (Any block allocable)";
        ramEl.textContent = "128 Bytes (Active i-node in RAM)";

        if (logicalBlock < 12) {
          stratEl.textContent = `Direct Pointer [${logicalBlock}]`;
          physEl.textContent = `Sector ${500 + logicalBlock * 8}`;
          seeksEl.textContent = "1 Seek (Direct Data Access)";
          consoleEl.textContent = `$ resolve_offset(${currentByteOffset}):\n[i-Node] Logical block #${logicalBlock} mapped directly via direct_pointers[${logicalBlock}].\n[Physical] Disk head targets block ${500 + logicalBlock * 8} with zero indirect table reads.`;
        } else {
          stratEl.textContent = "Single Indirect Table";
          physEl.textContent = `Sector ${800 + (logicalBlock - 12) * 8}`;
          seeksEl.textContent = "2 Seeks (1 Indirect Block + 1 Data)";
          consoleEl.textContent = `$ resolve_offset(${currentByteOffset}):\n[i-Node] Offset exceeds 12 direct blocks (48 KB).\n[i-Node] Read indirect pointer block at Sector 750 -> Traversed entry index [${logicalBlock - 12}] -> Physical sector ${800 + (logicalBlock - 12) * 8}.`;
        }
      } else if (currentModel === 'fat') {
        alignEl.textContent = "Clean (4096 B / Block)";
        fragEl.textContent = "Zero External";
        ramEl.textContent = "Full Table in RAM (~32 MB - 1 GB)";
        stratEl.textContent = `FAT Table Chain [Step ${logicalBlock}]`;
        physEl.textContent = `Cluster ${120 + logicalBlock * 3}`;
        seeksEl.textContent = "1 Seek (RAM chain pre-computed)";
        consoleEl.textContent = `$ resolve_offset(${currentByteOffset}):\n[FAT] Traversed in-memory cluster chain: 120 -> 123 -> 126 -> 129 -> ${120 + logicalBlock * 3}.\n[I/O] Zero disk seeks spent traversing pointers; table lookup resolved completely in RAM.`;
      } else if (currentModel === 'linked') {
        const usableData = 4092;
        const actualBlock = Math.floor(currentByteOffset / usableData);
        alignEl.textContent = "Unaligned (4092 B Data + 4 B Ptr)";
        fragEl.textContent = "Zero External";
        ramEl.textContent = "Minimal (Only current block pointer)";
        stratEl.textContent = `Linked Block Pointer Traversal`;
        physEl.textContent = `Block ${200 + actualBlock * 14}`;
        seeksEl.textContent = `${actualBlock + 1} Sequential Seeks`;
        consoleEl.textContent = `$ resolve_offset(${currentByteOffset}):\n[Linked-List] Severe random access penalty: must sequentially read ${actualBlock} disk blocks to follow pointer chains.\n[Warning] Required ${actualBlock + 1} mechanical disk I/O operations to access target offset.`;
      } else if (currentModel === 'contiguous') {
        alignEl.textContent = "Clean (4096 B / Block)";
        fragEl.textContent = "Severe External Fragmentation";
        ramEl.textContent = "Minimal (Starting Block + Length)";
        stratEl.textContent = `Arithmetic Offset (${logicalBlock})`;
        physEl.textContent = `Block ${1000 + logicalBlock}`;
        seeksEl.textContent = "1 Direct Seek";
        consoleEl.textContent = `$ resolve_offset(${currentByteOffset}):\n[Contiguous] Physical Block = Starting Block (1000) + Logical Block (${logicalBlock}) = Block ${1000 + logicalBlock}.\n[Performance] Optimal streaming throughput; $O(1)$ arithmetic address resolution.`;
      }
    }

    // Initialize Simulator
    recomputeTranslation();
  </script>
</body>
</html>
"""

COMMIT_MSG = """Split and expand sections 4.3.1 and 4.3.2 with allocation visualizer

Update week10-file-management/03-filesystem-implementation.html to separate
file-system layout (4.3.1) from file allocation strategies (4.3.2), adding
detailed theory, architectural SVGs, and an interactive lookup sandbox."""

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
    print("--> Module 03 Layout & Allocation update successfully deployed!")

if __name__ == "__main__":
    deploy_module()
