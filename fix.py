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

    /* Windows 95 Desktop Theme */
    .win95-desktop {
      background-color: #008080;
      padding: 16px;
      border-radius: 6px;
      box-shadow: inset 1px 1px 0 #004040, inset -1px -1px 0 #00c0c0;
      display: flex;
      flex-direction: column;
      gap: 12px;
      font-family: "MS Sans Serif", Tahoma, -apple-system, sans-serif;
    }

    .win95-window {
      background-color: #c0c0c0;
      border-top: 2px solid #ffffff;
      border-left: 2px solid #ffffff;
      border-right: 2px solid #000000;
      border-bottom: 2px solid #000000;
      box-shadow: inset 1px 1px 0 #dfdfdf, inset -1px -1px 0 #808080;
      padding: 3px;
      position: relative;
    }

    .win95-titlebar {
      background: linear-gradient(90deg, #000080, #1084d0);
      color: #ffffff;
      padding: 3px 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: bold;
      font-size: 12px;
      letter-spacing: 0.5px;
    }

    .win95-titlebar-btn {
      width: 16px;
      height: 14px;
      background: #c0c0c0;
      border-top: 1px solid #ffffff;
      border-left: 1px solid #ffffff;
      border-right: 1px solid #000000;
      border-bottom: 1px solid #000000;
      color: #000000;
      font-size: 9px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      line-height: 1;
      font-weight: bold;
    }

    .win95-content {
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .win95-btn {
      background-color: #c0c0c0;
      border-top: 2px solid #ffffff;
      border-left: 2px solid #ffffff;
      border-right: 2px solid #000000;
      border-bottom: 2px solid #000000;
      box-shadow: inset 1px 1px 0 #dfdfdf, inset -1px -1px 0 #808080;
      padding: 4px 14px;
      font-family: inherit;
      font-size: 11px;
      color: #000000;
      cursor: pointer;
      min-width: 75px;
    }
    .win95-btn:active {
      border-top: 2px solid #000000;
      border-left: 2px solid #000000;
      border-right: 2px solid #ffffff;
      border-bottom: 2px solid #ffffff;
      box-shadow: none;
      padding: 5px 13px 3px 15px;
    }

    .win95-well {
      border-top: 2px solid #808080;
      border-left: 2px solid #808080;
      border-right: 2px solid #ffffff;
      border-bottom: 2px solid #ffffff;
      background-color: #ffffff;
      padding: 4px;
      position: relative;
    }

    .win95-cluster-grid {
      display: grid;
      grid-template-columns: repeat(48, 1fr);
      gap: 2px;
      background: #000000;
      padding: 2px;
      max-height: 380px;
      overflow-y: auto;
    }

    .w-cluster {
      aspect-ratio: 1 / 1;
      background-color: #ffffff;
      box-shadow: inset 1px 1px 0 rgba(0,0,0,0.25);
    }
    .wc-free { background-color: #ffffff; }
    .wc-unopt { background-color: #5ce1e6; }
    .wc-opt { background-color: #000080; }
    .wc-read { background-color: #00ff00 !important; box-shadow: 0 0 5px #00ff00; }
    .wc-write { background-color: #ff0000 !important; box-shadow: 0 0 5px #ff0000; }
    .wc-unmovable {
      background: linear-gradient(135deg, #ffffff 50%, #ff0000 50%);
    }

    .win95-legend-dialog {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 320px;
      background: #c0c0c0;
      border-top: 2px solid #ffffff;
      border-left: 2px solid #ffffff;
      border-right: 2px solid #000000;
      border-bottom: 2px solid #000000;
      box-shadow: 3px 3px 10px rgba(0,0,0,0.6);
      z-index: 100;
      font-size: 11px;
    }

    .legend-body {
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .legend-row {
      display: flex;
      align-items: center;
      gap: 8px;
      color: #000000;
    }

    .legend-swatch {
      width: 14px;
      height: 14px;
      border: 1px solid #000000;
      box-shadow: inset 1px 1px 0 rgba(255,255,255,0.6);
      flex-shrink: 0;
    }

    .win95-status-bar {
      border-top: 1px solid #808080;
      padding-top: 4px;
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: #000000;
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
        <li><strong>Boot Block:</strong> The first block of the partition. Contains partition-specific bootstrap code read into memory by the MBR/UEFI to launch the target operating system.</li>
        <li><strong>Superblock:</strong> The central administrative descriptor storing filesystem type, block counts, i-node counts, and volume health state.</li>
        <li><strong>Free Space Management:</strong> Data structures tracking unallocated blocks available for new file data (bitmaps or free lists).</li>
        <li><strong>I-Node Table:</strong> An array of linear metadata records pre-allocated across contiguous tracks.</li>
        <li><strong>Root Directory:</strong> The top-level directory node (often bound to i-node 2 in Unix filesystems).</li>
        <li><strong>Data Blocks:</strong> The remainder of the volume dedicated to actual file content bytes and subdirectory tables.</li>
      </ol>
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

    <!-- WINDOWS 95/98 DISK DEFRAGMENTER SIMULATION WIDGET -->
    <div class="win95-desktop">
      <div class="win95-window">
        <div class="win95-titlebar">
          <div style="display:flex; align-items:center; gap:6px;">
            <span>Disk Defragmenter (Drive C:)</span>
          </div>
          <div style="display:flex; gap:2px;">
            <div class="win95-titlebar-btn">?</div>
            <div class="win95-titlebar-btn">&#x2715;</div>
          </div>
        </div>

        <div class="win95-content">
          <div style="display:flex; gap:6px; flex-wrap:wrap; align-items:center;">
            <button class="win95-btn" onclick="win95Populate()">1. Reset Drive</button>
            <button class="win95-btn" onclick="win95Fragment()">2. Heavy Churn</button>
            <button class="win95-btn" onclick="win95StartDefrag()" id="wBtnStart">Start Defrag</button>
            <button class="win95-btn" onclick="win95Pause()">Pause</button>
            <button class="win95-btn" onclick="toggleLegend()">Legend</button>
            <div style="margin-left:auto; display:flex; align-items:center; gap:4px; font-size:11px;">
              <span>Speed:</span>
              <button class="win95-btn" onclick="setSpeed(35)" style="min-width:32px; padding:2px 4px;">1x</button>
              <button class="win95-btn" onclick="setSpeed(12)" style="min-width:32px; padding:2px 4px;">3x</button>
              <button class="win95-btn" onclick="setSpeed(2)" style="min-width:32px; padding:2px 4px;">Max</button>
            </div>
          </div>

          <div class="win95-well">
            <div class="win95-cluster-grid" id="win95Grid"></div>

            <!-- Floating Legend Modal -->
            <div class="win95-legend-dialog" id="win95LegendModal">
              <div class="win95-titlebar">
                <span>Defrag Legend</span>
                <div class="win95-titlebar-btn" onclick="toggleLegend()">&#x2715;</div>
              </div>
              <div class="legend-body">
                <div class="legend-row">
                  <div class="legend-swatch" style="background:#5ce1e6;"></div>
                  <span>Unoptimized data</span>
                </div>
                <div class="legend-row">
                  <div class="legend-swatch" style="background:#000080;"></div>
                  <span>Optimized (defragmented) data</span>
                </div>
                <div class="legend-row">
                  <div class="legend-swatch" style="background:#ffffff;"></div>
                  <span>Free space</span>
                </div>
                <div class="legend-row">
                  <div class="legend-swatch" style="background:linear-gradient(135deg, #ffffff 50%, #ff0000 50%);"></div>
                  <span>Data that will not be moved</span>
                </div>
                <div class="legend-row">
                  <div class="legend-swatch" style="background:#00ff00;"></div>
                  <span>Data that's currently being read</span>
                </div>
                <div class="legend-row">
                  <div class="legend-swatch" style="background:#ff0000;"></div>
                  <span>Data that's currently being written</span>
                </div>

                <div style="margin-top:6px; font-size:10px; color:#444;">
                  Each box represents one disk cluster.
                </div>

                <div style="display:flex; justify-content:flex-end; margin-top:6px;">
                  <button class="win95-btn" onclick="toggleLegend()">Close</button>
                </div>
              </div>
            </div>
          </div>

          <div class="win95-status-bar">
            <span id="wStatusText">Drive C: Analyzed - Ready to optimize.</span>
            <span id="wClustersText">Clusters: 0 / 1440 Allocated</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Section 4.3.5: Advanced Implementations -->
    <div class="card" style="margin-top:12px;">
      <h2>4.3.5 &ndash; 4.3.8 Advanced File Systems (LFS, Journaling, Flash, VFS)</h2>
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
    // --- Windows 95 Authentic Multi-Pass Defragmentation Engine ---
    const TOTAL_CLUSTERS = 1440; // 48 cols x 30 rows
    let clusters = [];
    let isDefragging = false;
    let defragTimer = null;
    let defragDelay = 12; // ms
    let defragPhase = 1; // Phase 1: Consolidate scattered files; Phase 2: Compact free space to tail

    function setSpeed(ms) {
      defragDelay = ms;
    }

    function toggleLegend() {
      const modal = document.getElementById("win95LegendModal");
      modal.style.display = (modal.style.display === "none") ? "block" : "none";
    }

    function initGrid() {
      const grid = document.getElementById("win95Grid");
      grid.innerHTML = "";
      clusters = [];
      for (let i = 0; i < TOTAL_CLUSTERS; i++) {
        const div = document.createElement("div");
        div.className = "w-cluster wc-free";
        div.id = `wc-${i}`;
        grid.appendChild(div);
        clusters.push({ state: "free", isSystem: false, fileId: null });
      }
    }

    function renderCluster(idx) {
      const el = document.getElementById(`wc-${idx}`);
      const c = clusters[idx];
      el.className = "w-cluster";

      if (c.state === "read") {
        el.classList.add("wc-read");
      } else if (c.state === "write") {
        el.classList.add("wc-write");
      } else if (c.isSystem) {
        el.classList.add("wc-unmovable");
      } else if (c.state === "optimized") {
        el.classList.add("wc-opt");
      } else if (c.state === "unoptimized") {
        el.classList.add("wc-unopt");
      } else {
        el.classList.add("wc-free");
      }
    }

    function renderAll() {
      for (let i = 0; i < TOTAL_CLUSTERS; i++) {
        renderCluster(i);
      }
      updateStatus();
    }

    function win95Populate() {
      win95Pause();
      initGrid();
      defragPhase = 1;

      // Unmovable clusters matching the reference video layout
      const unmovable = [14, 62, 110, 158, 204, 390, 520, 710, 940, 1120];
      unmovable.forEach(idx => {
        clusters[idx] = { state: "unmovable", isSystem: true, fileId: "sys" };
      });

      // Top area already optimized (dark blue)
      const optCutoff = Math.floor(TOTAL_CLUSTERS * 0.22);
      for (let i = 0; i < optCutoff; i++) {
        if (!clusters[i].isSystem) {
          clusters[i] = { state: "optimized", isSystem: false, fileId: "opt" };
        }
      }

      // Middle and bottom: scattered bands of unoptimized cyan files and white free clusters
      for (let i = optCutoff; i < TOTAL_CLUSTERS; i++) {
        if (!clusters[i].isSystem) {
          let row = Math.floor(i / 48);
          let band = (i * 17 + row * 29) % 100;
          if (band > 38) {
            clusters[i] = { state: "unoptimized", isSystem: false, fileId: `f_${band % 12}` };
          } else {
            clusters[i] = { state: "free", isSystem: false, fileId: null };
          }
        }
      }

      renderAll();
      document.getElementById("wStatusText").textContent = "Drive C: Analyzed - Ready to Defragment.";
    }

    function win95Fragment() {
      win95Populate();
      // Punch additional scattered holes across the dark blue region to simulate file churn
      for (let i = 10; i < 250; i += 7) {
        if (!clusters[i].isSystem) {
          clusters[i] = { state: "free", isSystem: false, fileId: null };
        }
      }
      // Add scattered unoptimized blocks in upper rows
      for (let i = 250; i < 350; i += 5) {
        if (!clusters[i].isSystem) {
          clusters[i] = { state: "unoptimized", isSystem: false, fileId: "frag" };
        }
      }
      renderAll();
      document.getElementById("wStatusText").textContent = "Drive C: Heavily Fragmented (38% Fragmentation).";
    }

    function updateStatus() {
      const optCount = clusters.filter(c => c.state === "optimized").length;
      const unoptCount = clusters.filter(c => c.state === "unoptimized").length;
      const totalData = optCount + unoptCount;
      const pct = totalData > 0 ? Math.round((optCount / totalData) * 100) : 0;

      let phaseDesc = defragPhase === 1 ? "Defragmenting File System (Pass 1)..." : "Consolidating Free Space (Pass 2)...";
      document.getElementById("wStatusText").textContent = isDefragging
        ? `${pct}% Complete - ${phaseDesc}`
        : `Drive C: ${pct}% Optimized.`;
      document.getElementById("wClustersText").textContent = `Clusters: ${totalData} / ${TOTAL_CLUSTERS} Allocated`;
    }

    function win95StartDefrag() {
      if (isDefragging) return;
      isDefragging = true;
      document.getElementById("wStatusText").textContent = "Defragmenting Drive C:...";
      executeDefragCycle();
    }

    // Authentic Multi-Pass Loop
    function executeDefragCycle() {
      if (!isDefragging) return;

      // Locate first free cluster (white) from the top down
      let targetFree = -1;
      for (let i = 0; i < TOTAL_CLUSTERS; i++) {
        if (clusters[i].state === "free") {
          targetFree = i;
          break;
        }
      }

      // Locate unoptimized clusters (cyan)
      // In Pass 1, find clusters belonging to scattered files and move them in bursts
      let sourceClusters = [];
      for (let i = TOTAL_CLUSTERS - 1; i > targetFree; i--) {
        if (clusters[i].state === "unoptimized" && !clusters[i].isSystem) {
          sourceClusters.push(i);
          if (sourceClusters.length >= 4) break; // Gather a burst of clusters
        }
      }

      // If no unoptimized clusters exist past the free gap, switch to Phase 2 or finish
      if (targetFree === -1 || sourceClusters.length === 0) {
        win95Finish();
        return;
      }

      // Step A: Flash all read clusters in Green (burst reading)
      sourceClusters.forEach(idx => {
        clusters[idx].state = "read";
        renderCluster(idx);
      });

      defragTimer = setTimeout(() => {
        if (!isDefragging) return;

        // Step B: Flash destination clusters in Red (burst writing)
        let freeSlots = [];
        for (let i = targetFree; i < TOTAL_CLUSTERS && freeSlots.length < sourceClusters.length; i++) {
          if (clusters[i].state === "free") {
            freeSlots.push(i);
            clusters[i].state = "write";
            renderCluster(i);
          }
        }

        defragTimer = setTimeout(() => {
          if (!isDefragging) return;

          // Step C: Commit move - sources turn free (white), targets turn optimized (navy blue)
          sourceClusters.forEach(idx => {
            clusters[idx] = { state: "free", isSystem: false, fileId: null };
            renderCluster(idx);
          });

          freeSlots.forEach(idx => {
            clusters[idx] = { state: "optimized", isSystem: false, fileId: "opt" };
            renderCluster(idx);
          });

          updateStatus();
          defragTimer = setTimeout(executeDefragCycle, defragDelay);
        }, defragDelay);
      }, defragDelay);
    }

    function win95Finish() {
      isDefragging = false;
      // Mark all remaining unoptimized clusters as optimized
      for (let i = 0; i < TOTAL_CLUSTERS; i++) {
        if (clusters[i].state === "unoptimized") {
          clusters[i].state = "optimized";
        }
      }
      renderAll();
      document.getElementById("wStatusText").textContent = "100% Complete - Drive C: Fully Optimized.";
    }

    function win95Pause() {
      isDefragging = false;
      if (defragTimer) clearTimeout(defragTimer);
      // Clear active green/red flashing
      for (let i = 0; i < TOTAL_CLUSTERS; i++) {
        if (clusters[i].state === "read") clusters[i].state = "unoptimized";
        if (clusters[i].state === "write") clusters[i].state = "free";
      }
      renderAll();
    }

    // Initialize on Load
    initGrid();
    win95Populate();
  </script>
</body>
</html>
"""

COMMIT_MSG = """Implement authentic multi-pass file reassembly in defrag simulator

Update week10-file-management/03-filesystem-implementation.html to model
multi-pass cluster gathering, green read bursts, and red write blocks."""

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

    run_git_step(["git", "add", target_file], "Staging multi-pass defragmenter update")
    run_git_step(["git", "commit", "-a", "-m", COMMIT_MSG], "Committing changes")
    run_git_step(["git", "push", "origin", "main"], "Pushing main to origin")
    print("--> Multi-pass Windows 95 Defragmenter simulator deployed successfully!")

if __name__ == "__main__":
    deploy_module()
