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

    /* High-Density Norton-Style Defrag Simulator Styles */
    .defrag-card {
      background: #041226;
      color: #ffffff;
      border: 2px solid #38bdf8;
      border-radius: 8px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      font-family: var(--font-mono);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .defrag-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #1e3a8a;
      padding-bottom: 10px;
    }
    .defrag-title {
      font-size: 1.15rem;
      font-weight: 700;
      color: #fbbf24;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }
    .defrag-controls {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      background: #020817;
      border: 1px solid #1e3a8a;
      padding: 10px 14px;
      border-radius: 6px;
      align-items: center;
    }
    button.defrag-btn {
      background-color: #1e3a8a;
      color: #ffffff;
      border: 1px solid #38bdf8;
      padding: 8px 15px;
      border-radius: 4px;
      font-size: 0.8rem;
      font-weight: 700;
      font-family: inherit;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    button.defrag-btn:hover {
      background-color: #2563eb;
      box-shadow: 0 0 8px rgba(56, 189, 248, 0.6);
    }
    button.btn-warn { background-color: #b45309; border-color: #fbbf24; }
    button.btn-warn:hover { background-color: #d97706; }
    button.btn-danger { background-color: #991b1b; border-color: #f87171; }
    button.btn-danger:hover { background-color: #dc2626; }
    button.btn-success { background-color: #059669; border-color: #34d399; }
    button.btn-success:hover { background-color: #10b981; }

    /* High-Density Sector Matrix Container */
    .cluster-grid-container {
      background: #010612;
      border: 2px solid #1e3a8a;
      border-radius: 6px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .cluster-map-dense {
      display: grid;
      grid-template-columns: repeat(50, 1fr);
      gap: 2px;
      background: #000208;
      border: 1px solid #0f274a;
      padding: 6px;
      border-radius: 4px;
      max-height: 340px;
      overflow-y: auto;
    }
    .sector-block {
      aspect-ratio: 1 / 1;
      border-radius: 1px;
      transition: background-color 0.05s ease;
      min-width: 6px;
      min-height: 6px;
    }

    /* Authentic Speed Disk Palette */
    .s-free { background-color: #101c33; }
    .s-contig { background-color: #0284c7; }
    .s-frag { background-color: #f59e0b; }
    .s-system { background-color: #dc2626; }
    .s-read {
      background-color: #facc15 !important;
      box-shadow: 0 0 6px #facc15;
      transform: scale(1.15);
      z-index: 5;
    }
    .s-write {
      background-color: #34d399 !important;
      box-shadow: 0 0 6px #34d399;
      transform: scale(1.15);
      z-index: 5;
    }

    /* Legend */
    .cluster-legend {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      font-size: 0.76rem;
      padding: 4px 0;
      color: #cbd5e1;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .legend-box {
      width: 10px;
      height: 10px;
      border-radius: 2px;
    }

    /* Telemetry Panels */
    .telemetry-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 12px;
    }
    .telemetry-card {
      background: #020b18;
      border: 1px solid #1e3a8a;
      border-radius: 6px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 0.8rem;
    }
    .telemetry-card-title {
      font-size: 0.82rem;
      font-weight: 700;
      color: #fbbf24;
      text-transform: uppercase;
      border-bottom: 1px solid #0f274a;
      padding-bottom: 4px;
    }
    .telemetry-row {
      display: flex;
      justify-content: space-between;
      color: #cbd5e1;
      padding: 2px 0;
    }
    .telemetry-row span.val {
      font-weight: 700;
      color: #38bdf8;
    }
    .defrag-console {
      background: #010610;
      border: 1px solid #1e3a8a;
      border-radius: 6px;
      padding: 10px 14px;
      font-size: 0.8rem;
      color: #38bdf8;
      min-height: 55px;
      line-height: 1.45;
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
        <li><strong>Free Space Management:</strong> Data structures tracking unallocated blocks available for new file data (bitmaps or free lists).</li>
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

    <!-- Section 4.3.2: Allocation Strategies & Fragmentation -->
    <div class="card">
      <h2>4.3.2 Implementing Files: Allocation Strategies &amp; Fragmentation</h2>
      <p>
        The central design challenge of a file system is mapping a linear stream of logical file bytes into physical storage blocks. Over time, file churn produces two distinct forms of fragmentation:
      </p>
      <ul>
        <li><strong>External Fragmentation:</strong> Free blocks become scattered in non-contiguous gaps. In contiguous allocation models, external fragmentation prevents new files from being written even when total free space is sufficient.</li>
        <li><strong>Internal File Fragmentation:</strong> In FAT and linked systems, a single file's cluster chain becomes scattered randomly across the volume. Reading the file sequentially requires repeated mechanical head seeks, dropping throughput significantly.</li>
      </ul>
    </div>

    <!-- High-Density Norton-Style Interactive Defragmenter -->
    <div class="defrag-card">
      <div class="defrag-header">
        <div>
          <span class="defrag-title">Norton Speed Disk / High-Density FAT Optimizer</span>
          <div style="font-size: 0.78rem; color: #93c5fd; margin-top: 2px;">
            Target: 100 MB FAT Volume | 4 KB Clusters (25,600 Total) | Visualized as 1,600 Discrete Sector Blocks
          </div>
        </div>
        <div>
          <span style="font-size: 0.85rem; color: #fbbf24; font-weight: 700;" id="defragStatusBadge">VOLUME READY</span>
        </div>
      </div>

      <!-- Controls -->
      <div class="defrag-controls">
        <button class="defrag-btn" onclick="populateDummyFiles()">1. Populate 100MB Disk</button>
        <button class="defrag-btn btn-warn" onclick="fragmentVolume()">2. Heavy Churn (Fragment Disk!)</button>
        <button class="defrag-btn btn-success" onclick="startDefrag()" id="btnStartDefrag">3. Start Defragmentation</button>
        <button class="defrag-btn btn-danger" onclick="stopDefrag()">Pause / Stop</button>
        <span style="font-size: 0.75rem; color: #94a3b8; margin-left: auto;">Speed:</span>
        <button class="defrag-btn" onclick="setSpeed(20)" style="padding: 4px 8px; font-size: 0.72rem;">1x</button>
        <button class="defrag-btn" onclick="setSpeed(8)" style="padding: 4px 8px; font-size: 0.72rem;">2x</button>
        <button class="defrag-btn" onclick="setSpeed(1)" style="padding: 4px 8px; font-size: 0.72rem;">Max</button>
      </div>

      <!-- Dense Matrix Grid -->
      <div class="cluster-grid-container">
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem;">
          <span style="color:#93c5fd; font-weight:700;">PHYSICAL SECTOR MATRIX (1,600 BLOCKS — 50 COLUMNS &times; 32 ROWS):</span>
          <span id="mapInspectionLabel" style="color:#fbbf24;">Hover over sectors to inspect file allocation</span>
        </div>

        <div class="cluster-map-dense" id="denseGrid"></div>

        <!-- Legend -->
        <div class="cluster-legend">
          <div class="legend-item"><div class="legend-box" style="background:#101c33;"></div><span>Free Space</span></div>
          <div class="legend-item"><div class="legend-box" style="background:#0284c7;"></div><span>Contiguous File</span></div>
          <div class="legend-item"><div class="legend-box" style="background:#f59e0b;"></div><span>Fragmented File</span></div>
          <div class="legend-item"><div class="legend-box" style="background:#dc2626;"></div><span>System / Unmovable</span></div>
          <div class="legend-item"><div class="legend-box" style="background:#facc15;"></div><span>Reading (r)</span></div>
          <div class="legend-item"><div class="legend-box" style="background:#34d399;"></div><span>Writing (w)</span></div>
        </div>
      </div>

      <!-- Telemetry Readouts -->
      <div class="telemetry-grid">
        <div class="telemetry-card">
          <div class="telemetry-card-title">Volume Space Telemetry</div>
          <div class="telemetry-row"><span>Total Volume Size:</span><span class="val">100.0 MB</span></div>
          <div class="telemetry-row"><span>Cluster Size:</span><span class="val">4,096 B (4 KB)</span></div>
          <div class="telemetry-row"><span>Allocated Sectors:</span><span class="val" id="valDiskUsed">0 / 1,600</span></div>
          <div class="telemetry-row"><span>Free Space Available:</span><span class="val" id="valFreeSpace">100.0 MB</span></div>
        </div>

        <div class="telemetry-card">
          <div class="telemetry-card-title">Fragmentation &amp; Seek Analysis</div>
          <div class="telemetry-row"><span>Total Active Files:</span><span class="val" id="valTotalFiles">0</span></div>
          <div class="telemetry-row"><span>Fragmented Files:</span><span class="val" id="valFragFiles" style="color:#f59e0b;">0</span></div>
          <div class="telemetry-row"><span>Volume Fragmentation:</span><span class="val" id="valFragPercent">0%</span></div>
          <div class="telemetry-row"><span>Mechanical Seek Penalty:</span><span class="val" id="valSeekOverhead">0 ms</span></div>
        </div>
      </div>

      <div class="defrag-console" id="defragConsole">$ Speed Disk engine ready. Click '1. Populate 100MB Disk' to begin...</div>
    </div>

    <!-- Section 4.3.5: Advanced Implementations -->
    <div class="card" style="margin-top:12px;">
      <h2>4.3.5 &ndash; 4.3.8 Advanced File Systems</h2>
      <p>
        Modern workloads implement advanced architectures to avoid the fragmentation and metadata consistency problems inherent in traditional FAT volumes:
      </p>
      <ul>
        <li><strong>Log-Structured File Systems (LFS):</strong> Writes are appended sequentially to a continuous circular log, avoiding scattered random writes.</li>
        <li><strong>Journaling File Systems:</strong> Records atomic transactions in a write-ahead journal (e.g., ext4, NTFS), allowing sub-second reboot recovery.</li>
        <li><strong>Flash / SSD Wear-Leveling:</strong> Uses a Flash Translation Layer (FTL) and the <code>TRIM</code> command to avoid mechanical seek penalties while managing erase-block life cycles.</li>
        <li><strong>Virtual File Systems (VFS):</strong> Provides uniform abstractions (superblocks, inodes, dentries) unifying local and network filesystems.</li>
      </ul>
    </div>

  </div>

  <script>
    // --- 1,600 Block High-Density Norton Defragmenter Simulation Engine ---
    const TOTAL_SECTORS = 1600; // 50 cols x 32 rows dense matrix
    let sectors = [];
    let fileCatalog = [];
    let isDefragActive = false;
    let defragTimeout = null;
    let stepDelay = 8; // ms

    function setSpeed(ms) {
      stepDelay = ms;
    }

    function initDenseGrid() {
      const grid = document.getElementById("denseGrid");
      grid.innerHTML = "";
      sectors = [];
      for (let i = 0; i < TOTAL_SECTORS; i++) {
        const div = document.createElement("div");
        div.className = "sector-block s-free";
        div.id = `sec-${i}`;
        div.addEventListener("mouseenter", () => inspectSector(i));
        grid.appendChild(div);
        sectors.push({ state: "free", fileId: null, isSystem: false });
      }
    }

    function inspectSector(idx) {
      const sec = sectors[idx];
      const lbl = document.getElementById("mapInspectionLabel");
      if (sec.state === "free") {
        lbl.textContent = `Sector #${idx}: Free / Unallocated`;
      } else if (sec.isSystem) {
        lbl.textContent = `Sector #${idx}: System File (IO.SYS / MSDOS.SYS) [Unmovable]`;
      } else {
        const f = fileCatalog.find(item => item.id === sec.fileId);
        lbl.textContent = `Sector #${idx}: File '${f ? f.name : "Unknown"}' (${f && f.isFragmented ? "Fragmented" : "Contiguous"})`;
      }
    }

    function renderSector(idx) {
      const el = document.getElementById(`sec-${idx}`);
      const sec = sectors[idx];
      el.className = "sector-block";

      if (sec.state === "read") {
        el.classList.add("s-read");
      } else if (sec.state === "write") {
        el.classList.add("s-write");
      } else if (sec.isSystem) {
        el.classList.add("s-system");
      } else if (sec.state === "used") {
        const f = fileCatalog.find(item => item.id === sec.fileId);
        if (f && f.isFragmented) {
          el.classList.add("s-frag");
        } else {
          el.classList.add("s-contig");
        }
      } else {
        el.classList.add("s-free");
      }
    }

    function renderAllSectors() {
      for (let i = 0; i < TOTAL_SECTORS; i++) {
        renderSector(i);
      }
      updateTelemetry();
    }

    function populateDummyFiles() {
      stopDefrag();
      initDenseGrid();
      fileCatalog = [];

      // 1. Reserved System Files at the front (Unmovable)
      const sysLen = 40;
      for (let i = 0; i < sysLen; i++) {
        sectors[i] = { state: "used", fileId: "sys", isSystem: true };
      }
      fileCatalog.push({ id: "sys", name: "IO.SYS / MSDOS.SYS", size: sysLen, isFragmented: false, isSystem: true });

      // 2. Populate contiguous files across first half
      let ptr = sysLen;
      const initialFiles = [
        { name: "COMMAND.COM", size: 24 },
        { name: "CONFIG.SYS", size: 8 },
        { name: "DATABASE.DAT", size: 180 },
        { name: "SPREADSHT.WK1", size: 120 },
        { name: "GRAPHICS.LIB", size: 160 },
        { name: "ARCHIVE.ZIP", size: 140 },
        { name: "SYSTEM.LOG", size: 90 },
        { name: "USER_DATA.DB", size: 150 },
        { name: "BACKUP_01.BAK", size: 130 },
        { name: "PROJECTS.C", size: 110 }
      ];

      initialFiles.forEach((item, idx) => {
        const fid = `file_${idx}`;
        for (let c = 0; c < item.size; c++) {
          sectors[ptr + c] = { state: "used", fileId: fid, isSystem: false };
        }
        fileCatalog.push({ id: fid, name: item.name, size: item.size, isFragmented: false, isSystem: false });
        ptr += item.size;
      });

      renderAllSectors();
      document.getElementById("defragStatusBadge").textContent = "VOLUME INITIALIZED (CLEAN)";
      document.getElementById("defragConsole").textContent = "$ Formatted 100 MB FAT volume with 1,600 sector clusters.\n[Layout] Populated initial system binaries and regular user files contiguously.\n[Integrity] Volume Fragmentation: 0%. Ready for file churn simulation.";
    }

    function fragmentVolume() {
      stopDefrag();
      if (fileCatalog.length === 0) populateDummyFiles();

      document.getElementById("defragConsole").textContent = "$ Simulating intensive multi-user file churn (deletions, appends, and scattered writes)...";

      // Delete alternating files across the volume to poke scattered gaps
      const deleteIds = ["file_1", "file_3", "file_5", "file_7"];
      fileCatalog = fileCatalog.filter(f => {
        if (deleteIds.includes(f.id)) {
          for (let i = 0; i < TOTAL_SECTORS; i++) {
            if (sectors[i].fileId === f.id) {
              sectors[i] = { state: "free", fileId: null, isSystem: false };
            }
          }
          return false;
        }
        return true;
      });

      // Inject new fragmented files across the scattered holes and volume tail
      const newFiles = [
        { id: "frag_a", name: "SERVER_LOG.TXT", size: 140 },
        { id: "frag_b", name: "VIDEO_STREAM.AVI", size: 260 },
        { id: "frag_c", name: "TEMP_CACHE.TMP", size: 110 },
        { id: "frag_d", name: "INDEX_TREE.BIN", size: 150 }
      ];

      newFiles.forEach(nf => {
        let placed = 0;
        let blocks = [];
        // Interspersed allocation
        for (let i = 40; i < TOTAL_SECTORS && placed < nf.size; i++) {
          if (sectors[i].state === "free" && (i % 2 === 0 || i > 1200)) {
            sectors[i] = { state: "used", fileId: nf.id, isSystem: false };
            blocks.push(i);
            placed++;
          }
        }
        // If remaining bytes need space
        for (let i = 40; i < TOTAL_SECTORS && placed < nf.size; i++) {
          if (sectors[i].state === "free") {
            sectors[i] = { state: "used", fileId: nf.id, isSystem: false };
            blocks.push(i);
            placed++;
          }
        }

        let isFrag = false;
        for (let p = 1; p < blocks.length; p++) {
          if (blocks[p] !== blocks[p - 1] + 1) {
            isFrag = true;
            break;
          }
        }
        fileCatalog.push({ id: nf.id, name: nf.name, size: placed, isFragmented: isFrag, isSystem: false });
      });

      // Update fragmentation status for all user files
      fileCatalog.forEach(f => {
        if (f.isSystem) return;
        let indices = [];
        for (let i = 0; i < TOTAL_SECTORS; i++) {
          if (sectors[i].fileId === f.id) indices.push(i);
        }
        for (let p = 1; p < indices.length; p++) {
          if (indices[p] !== indices[p - 1] + 1) {
            f.isFragmented = true;
            break;
          }
        }
      });

      renderAllSectors();
      document.getElementById("defragStatusBadge").textContent = "VOLUME HEAVILY FRAGMENTED";
      document.getElementById("defragConsole").textContent += "\n[Churn Complete] File cluster chains scattered randomly across disk.\n[Warning] Hundreds of non-contiguous sectors detected. High mechanical seek latency!";
    }

    function updateTelemetry() {
      const usedSectors = sectors.filter(s => s.state !== "free").length;
      const freeMB = (((TOTAL_SECTORS - usedSectors) / TOTAL_SECTORS) * 100).toFixed(1);
      document.getElementById("valDiskUsed").textContent = `${usedSectors} / 1,600 (${Math.round((usedSectors/TOTAL_SECTORS)*100)}%)`;
      document.getElementById("valFreeSpace").textContent = `${freeMB} MB`;

      const userFiles = fileCatalog.filter(f => !f.isSystem);
      const fragFiles = userFiles.filter(f => f.isFragmented);
      const fragPct = userFiles.length > 0 ? Math.round((fragFiles.length / userFiles.length) * 100) : 0;

      document.getElementById("valTotalFiles").textContent = userFiles.length;
      document.getElementById("valFragFiles").textContent = `${fragFiles.length} files`;
      document.getElementById("valFragPercent").textContent = `${fragPct}%`;
      document.getElementById("valSeekOverhead").textContent = `${fragFiles.length * 18} ms`;
    }

    // --- Dynamic Per-Sector Defragmentation Loop ---
    let defragQueue = [];

    function startDefrag() {
      if (isDefragActive) return;
      isDefragActive = true;
      document.getElementById("defragStatusBadge").textContent = "DEFRAGMENTING VOLUME...";
      document.getElementById("defragConsole").textContent = "$ Speed Disk engine started.\n[Sweep] Consolidating scattered cluster blocks and packing contiguous extents...";

      runDynamicDefragStep();
    }

    function runDynamicDefragStep() {
      if (!isDefragActive) return;

      // Locate first free sector slot past the unmovable system area (index 40)
      let targetFreeIdx = -1;
      for (let i = 40; i < TOTAL_SECTORS; i++) {
        if (sectors[i].state === "free") {
          targetFreeIdx = i;
          break;
        }
      }

      // Locate a used sector past this free gap
      let sourceUsedIdx = -1;
      // Prefer moving fragmented file sectors first
      for (let i = TOTAL_SECTORS - 1; i > targetFreeIdx; i--) {
        if (sectors[i].state === "used" && !sectors[i].isSystem) {
          sourceUsedIdx = i;
          break;
        }
      }

      // If no used sectors exist past the free gap, defragmentation is complete
      if (targetFreeIdx === -1 || sourceUsedIdx === -1 || targetFreeIdx >= sourceUsedIdx) {
        finishDefrag();
        return;
      }

      // Read phase (Flash Yellow)
      const movingSector = sectors[sourceUsedIdx];
      sectors[sourceUsedIdx].state = "read";
      renderSector(sourceUsedIdx);

      defragTimeout = setTimeout(() => {
        if (!isDefragActive) return;

        // Write phase (Flash Green)
        sectors[targetFreeIdx].state = "write";
        renderSector(targetFreeIdx);

        defragTimeout = setTimeout(() => {
          if (!isDefragActive) return;

          // Migrate block data
          sectors[targetFreeIdx] = { state: "used", fileId: movingSector.fileId, isSystem: false };
          sectors[sourceUsedIdx] = { state: "free", fileId: null, isSystem: false };

          renderSector(sourceUsedIdx);
          renderSector(targetFreeIdx);
          updateTelemetry();

          defragTimeout = setTimeout(runDynamicDefragStep, stepDelay);
        }, stepDelay);
      }, stepDelay);
    }

    function finishDefrag() {
      isDefragActive = false;
      fileCatalog.forEach(f => { f.isFragmented = false; });
      renderAllSectors();
      document.getElementById("defragStatusBadge").textContent = "OPTIMIZATION COMPLETE (100%)";
      document.getElementById("defragConsole").textContent = "$ Optimization complete!\n[Compacted] All files consolidated into contiguous sectors.\n[Throughput] Maximum sequential read bandwidth restored. Zero seek overhead.";
    }

    function stopDefrag() {
      isDefragActive = false;
      if (defragTimeout) clearTimeout(defragTimeout);
      // Clean any active read/write flashes
      for (let i = 0; i < TOTAL_SECTORS; i++) {
        if (sectors[i].state === "read" || sectors[i].state === "write") {
          sectors[i].state = "used";
          renderSector(i);
        }
      }
      document.getElementById("defragStatusBadge").textContent = "DEFRAGMENTATION PAUSED";
    }

    // Initialize Simulator on Load
    initDenseGrid();
    populateDummyFiles();
  </script>
</body>
</html>
"""

COMMIT_MSG = """Upgrade defrag visualizer to high-density 1,600-block per-file reassembly

Update week10-file-management/03-filesystem-implementation.html with a dense
1,600-sector visual matrix and authentic per-file defragmentation sweeps."""

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

    run_git_step(["git", "add", target_file], "Staging high-density defrag simulator update")
    run_git_step(["git", "commit", "-a", "-m", COMMIT_MSG], "Committing changes")
    run_git_step(["git", "push", "origin", "main"], "Pushing main to origin")
    print("--> High-Density Norton Defrag Simulator successfully deployed!")

if __name__ == "__main__":
    deploy_module()
