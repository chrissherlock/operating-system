#!/usr/bin/env python3
import base64
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
    @font-face {
      font-family: 'PerfectDOS';
      src: url('https://cdn.jsdelivr.net/gh/IdreesInc/Monocraft@main/web/Monocraft.woff2') format('woff2');
      font-weight: normal;
      font-style: normal;
    }

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

    /* Pioneers Infobox with Enlarged Headshots & Integrated Biographies */
    .pioneers-infobox {
      background-color: #f0f9ff;
      border: 1px solid #bae6fd;
      border-left: 4px solid var(--accent);
      border-radius: 6px;
      padding: 16px;
      margin: 14px 0;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .pioneers-infobox h4 {
      color: var(--accent);
      font-size: 1rem;
      font-weight: 700;
      margin-bottom: 2px;
    }
    .pioneers-portraits {
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
      margin-top: 6px;
      margin-bottom: 6px;
    }
    .pioneer-card {
      display: flex;
      flex-direction: column;
      gap: 12px;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 14px;
      flex: 1;
      min-width: 300px;
    }
    .pioneer-top {
      display: flex;
      align-items: flex-start;
      gap: 14px;
    }
    .pioneer-card img {
      width: 90px;
      height: 110px;
      object-fit: cover;
      border-radius: 4px;
      border: 1px solid #94a3b8;
      flex-shrink: 0;
    }
    .pioneer-info {
      display: flex;
      flex-direction: column;
      font-size: 0.88rem;
      gap: 3px;
    }
    .pioneer-info strong {
      color: var(--text);
      font-size: 0.95rem;
    }
    .pioneer-info span {
      color: var(--text-muted);
      font-size: 0.82rem;
    }
    .pioneer-bio {
      font-size: 0.88rem;
      color: #334155;
      line-height: 1.55;
      border-top: 1px solid #e2e8f0;
      padding-top: 10px;
      margin-top: 2px;
    }

    /* =========================================================
       DEFRAGMENTER SHELL & THEME CONTAINER STYLING
       ========================================================= */
    .defrag-outer-frame {
      width: 100%;
      border-radius: 8px;
      transition: all 0.25s ease;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .modern-legend {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      background: #020617;
      border: 1px solid #1e293b;
      padding: 10px 14px;
      border-radius: 6px;
      font-size: 0.78rem;
      color: #cbd5e1;
      align-items: center;
    }
    .modern-legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .modern-swatch {
      width: 14px;
      height: 14px;
      border-radius: 3px;
      flex-shrink: 0;
      display: inline-block;
      border: 1px solid rgba(255, 255, 255, 0.15);
    }

    .theme-modern {
      background: #0f172a;
      color: #f8fafc;
      border: 1px solid #334155;
      font-family: var(--font-mono);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
    }
    .theme-modern .ui-topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #334155;
      padding-bottom: 8px;
    }
    .theme-modern .ui-title {
      font-size: 1.1rem;
      font-weight: 700;
      color: #38bdf8;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .theme-modern .ui-controls {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      background: #020617;
      border: 1px solid #1e293b;
      padding: 8px 12px;
      border-radius: 6px;
      align-items: center;
      color: #f8fafc;
    }
    .theme-modern .ctrl-btn {
      background-color: #1e293b;
      color: #cbd5e1;
      border: 1px solid #334155;
      padding: 5px 11px;
      border-radius: 4px;
      font-size: 0.76rem;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .theme-modern .ctrl-btn:hover { background-color: #334155; color: #ffffff; }
    .theme-modern .ctrl-btn.active { background-color: var(--accent); color: #fff; border-color: #38bdf8; }
    .theme-modern .ctrl-btn.churn-btn { color: #fbbf24; }
    .theme-modern .grid-wrapper {
      background: #020617;
      border: 1px solid #1e293b;
      border-radius: 6px;
      padding: 6px;
      display: flex;
      justify-content: center;
    }
    .theme-modern .screen-grid {
      display: grid;
      grid-template-columns: repeat(100, 1fr);
      gap: 1px;
      width: 100%;
      max-width: 1000px;
    }
    .theme-modern .c-cell { aspect-ratio: 1 / 1; border-radius: 0.5px; }
    .theme-modern .c-free { background-color: #1e293b; }
    .theme-modern .c-opt { background-color: #0284c7; }
    .theme-modern .c-unopt { background-color: #f59e0b; }
    .theme-modern .c-system { background-color: #dc2626; }
    .theme-modern .c-read { background-color: #facc15 !important; box-shadow: 0 0 4px #facc15; }
    .theme-modern .c-write { background-color: #34d399 !important; box-shadow: 0 0 6px #34d399; }
    .theme-modern .ui-status-panel {
      background: #020617;
      border: 1px solid #1e293b;
      border-radius: 6px;
      padding: 8px 12px;
      font-size: 0.8rem;
      color: #38bdf8;
      display: flex;
      justify-content: space-between;
    }
    .theme-modern .theme-label { color: #94a3b8; }
    .theme-modern .dos-legend-box { display: none; }

    /* THEME 2: WINDOWS 95 / 98 */
    .theme-win95 {
      background-color: #008080;
      color: #000000;
      font-family: "MS Sans Serif", Tahoma, -apple-system, sans-serif;
      padding: 12px;
      border-radius: 4px;
    }
    .theme-win95 .ui-window-box {
      background: #c0c0c0;
      border-top: 2px solid #ffffff;
      border-left: 2px solid #ffffff;
      border-right: 2px solid #000000;
      border-bottom: 2px solid #000000;
      box-shadow: inset 1px 1px 0 #dfdfdf, inset -1px -1px 0 #808080;
      padding: 3px;
    }
    .theme-win95 .ui-topbar {
      background: linear-gradient(90deg, #000080, #1084d0);
      color: #ffffff;
      padding: 3px 6px;
      font-weight: bold;
      font-size: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .theme-win95 .ui-title { color: #ffffff; font-size: 12px; font-weight: bold; }
    .theme-win95 .ui-controls {
      display: flex;
      gap: 5px;
      flex-wrap: wrap;
      background: transparent;
      padding: 6px 0;
      align-items: center;
      color: #000000;
    }
    .theme-win95 .ctrl-btn {
      background-color: #c0c0c0;
      border-top: 2px solid #ffffff;
      border-left: 2px solid #ffffff;
      border-right: 2px solid #000000;
      border-bottom: 2px solid #000000;
      box-shadow: inset 1px 1px 0 #dfdfdf, inset -1px -1px 0 #808080;
      padding: 3px 8px;
      font-size: 11px;
      color: #000000 !important;
      cursor: pointer;
    }
    .theme-win95 .ctrl-btn.active { background-color: #d4d4d4; font-weight: bold; }
    .theme-win95 .grid-wrapper {
      border-top: 2px solid #808080;
      border-left: 2px solid #808080;
      border-right: 2px solid #ffffff;
      border-bottom: 2px solid #ffffff;
      background: #000000;
      padding: 3px;
      display: flex;
      justify-content: center;
    }
    .theme-win95 .screen-grid {
      display: grid;
      grid-template-columns: repeat(100, 1fr);
      gap: 1px;
      width: 100%;
      max-width: 1000px;
    }
    .theme-win95 .c-cell { aspect-ratio: 1 / 1; border-radius: 0; }
    .theme-win95 .c-free { background-color: #ffffff; }
    .theme-win95 .c-opt { background-color: #000080; }
    .theme-win95 .c-unopt { background-color: #5ce1e6; }
    .theme-win95 .c-system { background: linear-gradient(135deg, #ffffff 50%, #ff0000 50%); }
    .theme-win95 .c-read { background-color: #00ff00 !important; }
    .theme-win95 .c-write { background-color: #ff0000 !important; }
    .theme-win95 .ui-status-panel {
      border-top: 1px solid #808080;
      padding-top: 4px;
      margin-top: 4px;
      font-size: 11px;
      display: flex;
      justify-content: space-between;
      color: #000000 !important;
    }
    .theme-win95 .theme-label { color: #ffffff !important; }
    .theme-win95 .dos-legend-box { display: none; }

    /* THEME 3: MS-DOS / NORTON SPEED DISK */
    .theme-dos {
      background-color: #0000aa;
      color: #ffffff;
      font-family: "Courier New", Courier, monospace;
      padding: 10px;
      border: 3px double #ffffff;
      box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.8);
    }
    .theme-dos .ui-topbar {
      background: #00aaaa;
      color: #000000;
      padding: 2px 8px;
      font-weight: bold;
      font-size: 13px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }
    .theme-dos .ui-title { color: #000000; font-size: 13px; font-weight: bold; }
    .theme-dos .ui-controls {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      background: transparent;
      padding: 6px 0;
      align-items: center;
      color: #ffffff;
    }
    .theme-dos .ctrl-btn {
      background-color: #0000aa;
      color: #ffff55;
      border: 1px solid #ffffff;
      padding: 2px 7px;
      font-size: 11px;
      font-family: inherit;
      font-weight: bold;
      cursor: pointer;
    }
    .theme-dos .ctrl-btn.active { background-color: #ffff55; color: #0000aa; }
    .theme-dos .grid-wrapper {
      background: #000055;
      border: 2px solid #55ffff;
      padding: 4px;
      display: flex;
      justify-content: center;
    }
    .theme-dos .screen-grid {
      display: grid;
      grid-template-columns: repeat(100, 1fr);
      gap: 1px;
      width: 100%;
      max-width: 950px;
    }
    .theme-dos .c-cell { aspect-ratio: 1 / 1.4; display: flex; align-items: center; justify-content: center; font-size: 6px; font-weight: bold; }
    .theme-dos .c-free { background-color: #000055; color: #0000aa; }
    .theme-dos .c-opt { background-color: #0000aa; color: #ffffff; }
    .theme-dos .c-unopt { background-color: #0000aa; color: #ff5555; }
    .theme-dos .c-system { background-color: #aa0000; color: #ffffff; }
    .theme-dos .c-read { background-color: #55ff55 !important; color: #000000 !important; }
    .theme-dos .c-write { background-color: #ffff55 !important; color: #0000aa !important; }
    .theme-dos .ui-status-panel {
      background: #0000aa;
      border-top: 1px dashed #ffffff;
      padding-top: 6px;
      margin-top: 6px;
      font-size: 11px;
      color: #ffff55;
      display: flex;
      justify-content: space-between;
    }
    .theme-dos .theme-label { color: #000000; }
    .theme-dos .dos-legend-box { display: none; }

    /* THEME 4: MS-DOS 6.22 DEFRAG */
    .theme-olddos {
      background-color: #0000aa;
      color: #ffffff;
      font-family: 'PerfectDOS', monospace;
      padding: 0;
      border: 2px solid #55ffff;
    }
    .theme-olddos .ui-topbar {
      background: #ffffff;
      color: #0000aa;
      padding: 4px 8px;
      font-size: 11px;
      font-weight: bold;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .theme-olddos .ui-title { color: #0000aa; font-size: 11px; font-weight: bold; }
    .theme-olddos .ui-controls {
      background: #0000aa;
      border-bottom: 1px solid #55ffff;
      padding: 6px 10px;
      gap: 6px;
    }
    .theme-olddos .ctrl-btn {
      background-color: #0000aa;
      color: #ffff55;
      border: 1px solid #ffff55;
      padding: 2px 6px;
      font-size: 10px;
      font-family: inherit;
      cursor: pointer;
    }
    .theme-olddos .ctrl-btn.active { background-color: #ffff55; color: #0000aa; font-weight: bold; }
    .theme-olddos .grid-wrapper {
      background: #0000aa;
      border: 1px solid #55ffff;
      margin: 6px;
      padding: 4px;
      display: flex;
      justify-content: center;
    }
    .theme-olddos .screen-grid {
      display: grid;
      grid-template-columns: repeat(100, 1fr);
      gap: 1px;
      width: 100%;
      max-width: 950px;
    }
    .theme-olddos .c-cell { aspect-ratio: 1 / 1.4; display: flex; align-items: center; justify-content: center; font-size: 6px; font-weight: bold; }
    .theme-olddos .c-free { background-color: #005577; color: #005577; }
    .theme-olddos .c-opt { background-color: #ffff55; color: #0000aa; }
    .theme-olddos .c-unopt { background-color: #ffff55; color: #0000aa; }
    .theme-olddos .c-system { background-color: #ffff55; color: #aa0000; font-weight: 900; }
    .theme-olddos .c-read { background-color: #ffffff !important; color: #0000aa !important; }
    .theme-olddos .c-write { background-color: #55ff55 !important; color: #0000aa !important; }

    .theme-olddos .dos-legend-box {
      display: grid;
      grid-template-columns: 1fr 1fr;
      border: 1px solid #55ffff;
      margin: 6px;
      background: #0000aa;
      color: #ffffff;
      font-size: 10px;
      font-family: 'PerfectDOS', monospace;
    }
    .theme-olddos .dos-status-col { padding: 8px; border-right: 1px solid #55ffff; display: flex; flex-direction: column; gap: 6px; }
    .theme-olddos .dos-legend-col { padding: 8px; display: flex; flex-direction: column; gap: 4px; }
    .theme-olddos .dos-prog-bar {
      background: #ffffff;
      color: #0000aa;
      height: 14px;
      width: 100%;
      position: relative;
      overflow: hidden;
      font-size: 9px;
      display: flex;
      align-items: center;
      padding-left: 4px;
      font-weight: bold;
    }
    .theme-olddos .ui-status-panel { display: none; }
    .theme-olddos .theme-label { color: #0000aa; }

    #btnAudioToggle { display: none; }
    .theme-dos #btnAudioToggle, .theme-olddos #btnAudioToggle { display: inline-block; }
  </style>
</head>
<body>
  <audio id="defragAudio" src="AUDIO_DATA_URI_PLACEHOLDER" preload="auto" loop></audio>

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
    </div>

    <!-- Section 4.3.2: Allocation Strategies -->
    <div class="card">
      <h2>4.3.2 Implementing Files: Allocation Strategies &amp; Fragmentation</h2>
      <p>
        The central design challenge of a file system is mapping a linear stream of logical file bytes into physical storage blocks. Over time, file churn produces external and internal fragmentation.
      </p>
    </div>

    <!-- QUAD-THEME DEFRAG SIMULATOR -->
    <div class="defrag-outer-frame theme-modern" id="defragShell">
      <div class="ui-window-box">
        <div class="ui-topbar">
          <span class="ui-title" id="shellTitle">FAT32 Volume Optimizer (500 MB Drive)</span>
          <div style="display:flex; gap:6px; align-items:center;">
            <span style="font-size:11px;" class="theme-label" id="themeLabel">Theme:</span>
            <button class="ctrl-btn active" onclick="switchTheme('modern')" id="btn-theme-modern">Modern</button>
            <button class="ctrl-btn" onclick="switchTheme('win95')" id="btn-theme-win95">Windows 95</button>
            <button class="ctrl-btn" onclick="switchTheme('dos')" id="btn-theme-dos">MS-DOS</button>
            <button class="ctrl-btn" onclick="switchTheme('olddos')" id="btn-theme-olddos">MS-DOS 6.22</button>
          </div>
        </div>

        <div class="ui-controls">
          <div style="display:flex; align-items:center; gap:4px; margin-right:4px;">
            <span style="font-size:11px; font-weight:700;">Disk Size:</span>
            <button class="ctrl-btn" onclick="selectDiskCapacity(10)" id="size-10">10MB</button>
            <button class="ctrl-btn" onclick="selectDiskCapacity(100)" id="size-100">100MB</button>
            <button class="ctrl-btn active" onclick="selectDiskCapacity(500)" id="size-500">500MB</button>
            <button class="ctrl-btn" onclick="selectDiskCapacity(1000)" id="size-1000">1GB</button>
          </div>

          <button class="ctrl-btn" onclick="defragInitVolume()" id="btnFormatDisk">Format Disk</button>
          <button class="ctrl-btn churn-btn" onclick="defragHeavyChurn()">Heavy Churn (Fragment!)</button>
          <button class="ctrl-btn" onclick="defragToggleRun()" id="btnStartDefrag" style="font-weight:700;">Start Defrag</button>
          <button class="ctrl-btn" onclick="toggleAudioMute()" id="btnAudioToggle" style="background: #059669; color: #fff;">🔊 Audio: On</button>

          <div style="margin-left:auto; display:flex; align-items:center; gap:5px; font-size:11px;">
            <span>Speed:</span>
            <button class="ctrl-btn" onclick="setDefragSpeed(150, 'spd-slow')" id="spd-slow">Slow</button>
            <button class="ctrl-btn active" onclick="setDefragSpeed(45, 'spd-norm')" id="spd-norm">Medium</button>
            <button class="ctrl-btn" onclick="setDefragSpeed(10, 'spd-fast')" id="spd-fast">Fast</button>
          </div>
        </div>

        <div class="grid-wrapper">
          <div class="screen-grid" id="clusterGrid"></div>
        </div>

        <div class="dos-legend-box" id="dosLegendBox">
          <div class="dos-status-col">
            <div style="border-bottom:1px solid #55ffff; padding-bottom:2px; font-weight:bold; color:#ffff55;">Status</div>
            <div style="display:flex; justify-content:space-between; font-size:9.5px;">
              <span id="dosClusterText">Cluster 16,936</span>
              <span id="dosPctText">29%</span>
            </div>
            <div class="dos-prog-bar">
              <div id="dosProgressBarFill" style="background:#55ffff; width:29%; height:100%; position:absolute; left:0; top:0; z-index:1;"></div>
              <span id="dosProgressText" style="position:relative; z-index:2; color:#0000aa; margin:auto;"></span>
            </div>
            <div style="text-align:center; font-size:9.5px;" id="dosElapsedText">Elapsed Time: 00:00:00</div>
            <div style="text-align:center; font-size:9.5px; font-weight:bold; color:#ffff55;" id="dosOptModeText">Full Optimization</div>
          </div>
          <div class="dos-legend-col">
            <div style="border-bottom:1px solid #55ffff; padding-bottom:2px; font-weight:bold; color:#ffff55;">Legend</div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:2px; font-size:9px;">
              <div>■ - Used</div>
              <div>▒ - Unused</div>
              <div>r - Reading</div>
              <div>W - Writing</div>
              <div>B - Bad</div>
              <div>X - Unmovable</div>
            </div>
            <div style="margin-top:auto; font-size:9px; color:#55ffff;" id="dosDriveBlockText">Drive C:  1 block = 27 clusters</div>
          </div>
        </div>

        <div class="modern-legend" id="modernLegend">
          <span style="font-weight:700; color:#38bdf8;">Legend:</span>
          <div class="modern-legend-item"><div class="modern-swatch" style="background:#1e293b;"></div><span>Free Space</span></div>
          <div class="modern-legend-item"><div class="modern-swatch" style="background:#0284c7;"></div><span>Optimized</span></div>
          <div class="modern-legend-item"><div class="modern-swatch" style="background:#f59e0b;"></div><span>Unoptimized</span></div>
          <div class="modern-legend-item"><div class="modern-swatch" style="background:#dc2626;"></div><span>System</span></div>
        </div>

        <div class="ui-status-panel">
          <span id="txtStatusMsg">500 MB Volume Initialized. 3,000 Blocks on Screen.</span>
          <span id="txtProgressMetric">Optimization: 0% | Fragmentation: High</span>
        </div>
      </div>
    </div>

    <div style="text-align: right; font-size: 0.75rem; color: var(--text-muted); padding: 0 4px;">
      Sound FX: <a href="https://www.youtube.com/watch?v=Nidwz3BzFCM" target="_blank" style="color: var(--accent); text-decoration: none;">Defrag in MS-DOS 6.22 (ASMR) by Christopher Swenson</a>
    </div>

    <!-- Section 4.3.5: Log-Structured File Systems (LFS) -->
    <div class="card" style="margin-top:12px;">
      <h2>4.3.5 Log-Structured File Systems (LFS)</h2>
      <p>
        Traditional Unix and FAT filesystems distribute file data, inodes, directory entries, and indirect blocks across random locations on disk. As processor and memory speeds outpaced mechanical disk seek times in the early 1990s, random disk head seeks emerged as the primary performance bottleneck. To solve this, <strong>Mendel Rosenblum and John K. Ousterhout</strong> pioneered <strong>Log-Structured File Systems (LFS)</strong> at UC Berkeley, fundamentally redesigning storage architectures by transforming the disk into a continuous sequential log.
      </p>

      <!-- Pioneers Infobox with Enlarged Headshots, Wikipedia links, & Biographies -->
      <div class="pioneers-infobox">
        <h4>Pioneers Profile: Mendel Rosenblum &amp; John K. Ousterhout</h4>
        <div class="pioneers-portraits">
          <div class="pioneer-card">
            <div class="pioneer-top">
              <img src="../images/ousterhout.png" alt="John K. Ousterhout">
              <div class="pioneer-info">
                <strong><a href="https://en.wikipedia.org/wiki/John_Ousterhout" target="_blank" style="color: var(--accent); text-decoration: none;">John K. Ousterhout</a></strong>
                <span>Stanford University &bull; <a href="https://en.wikipedia.org/wiki/John_Ousterhout" target="_blank" style="color: var(--accent); text-decoration: underline;">Wikipedia Entry</a></span>
                <span><a href="https://web.stanford.edu/~ouster/" target="_blank" style="color: var(--text-muted); text-decoration: underline;">Photo Credit: Photo2012Small.png</a></span>
              </div>
            </div>
            <div class="pioneer-bio">
              Professor of computer science at Stanford University. Received his B.S. from Yale and Ph.D. from Carnegie Mellon. Alongside foundational work on LFS, he is renowned for creating the <strong>Tcl/Tk scripting language</strong> and leading the Sprite distributed operating system project at UC Berkeley.
            </div>
          </div>
          <div class="pioneer-card">
            <div class="pioneer-top">
              <img src="../images/rosenblum.jpg" alt="Mendel Rosenblum">
              <div class="pioneer-info">
                <strong><a href="https://en.wikipedia.org/wiki/Mendel_Rosenblum" target="_blank" style="color: var(--accent); text-decoration: none;">Mendel Rosenblum</a></strong>
                <span>Stanford University &bull; <a href="https://en.wikipedia.org/wiki/Mendel_Rosenblum" target="_blank" style="color: var(--accent); text-decoration: underline;">Wikipedia Entry</a></span>
                <span><a href="http://www.stanford.edu/~mendel/" target="_blank" style="color: var(--text-muted); text-decoration: underline;">Photo Credit: RosenblumLowRes.jpg</a></span>
              </div>
            </div>
            <div class="pioneer-bio">
              Professor of computer science at Stanford University and co-founder of <strong>VMware</strong>. Received his B.A., M.S., and Ph.D. from UC Berkeley. His pioneering research spans operating systems, virtual machine monitors, distributed storage, and large-scale systems architecture.
            </div>
          </div>
        </div>
        <ul>
          <li><strong>Institution:</strong> University of California, Berkeley</li>
          <li><strong>Key Publication:</strong> &ldquo;The Design and Implementation of a Log-Structured File System&rdquo; (ACM TOCS, 1992)</li>
          <li><strong>Core Innovation:</strong> Replaced random in-place metadata and data updates with continuous sequential log writes, accompanied by inode maps and background segment cleaning.</li>
        </ul>
      </div>

      <h3>1. The Log-Structured Paradigm &amp; Sequential Writes</h3>
      <p>
        Traditional file systems update metadata and file data in-place across scattered disk sectors. In contrast, LFS buffers all modifications in main memory and appends them sequentially in large, contiguous units called <strong>segments</strong> (typically 512 KB to 1 MB). By eliminating random writes and mechanical head repositioning, LFS achieves write performance that approaches the raw bandwidth limits of the storage media.
      </p>

      <h3>2. The Inode Map (Imap) &amp; Dynamic Location Tracking</h3>
      <p>
        In traditional file systems, every inode has a fixed, static disk address derived from its inode number and the fixed offset of the inode table. In an LFS, because files and their inodes are continually rewritten to the tail of the log, an inode's physical location changes with every update.
      </p>
      <ul>
        <li><strong>Decoupling Inode Numbers:</strong> LFS introduces an <strong>inode map (imap)</strong> that acts as a dynamic translation layer, mapping every file's unique inode number to its current physical disk address within the log.</li>
        <li><strong>Logging the Imap:</strong> Pieces of the inode map are written directly into the log alongside file data. When an inode moves, its new address is recorded in the imap, and updated imap blocks are committed to the log tail.</li>
      </ul>

      <h3>3. Checkpoint Regions &amp; Fast Crash Recovery</h3>
      <p>
        To locate the inode map during system startup without scanning the entire multi-gigabyte log, LFS maintains a fixed <strong>Checkpoint Region (CR)</strong> on disk.
      </p>
      <ul>
        <li><strong>Checkpoint Contents:</strong> The checkpoint region stores pointers to the current blocks of the inode map, the last segment usage summary, and a timestamp.</li>
        <li><strong>Roll-Forward Recovery:</strong> In the event of a system crash, LFS reads the latest consistent checkpoint region and then <em>rolls forward</em> through subsequent segments written after the checkpoint, rebuilding any lost metadata without requiring a lengthy volume scan like <code>fsck</code>.</li>
      </ul>

      <h3>4. Background Garbage Collection &amp; Segment Cleaning</h3>
      <p>
        Appending data sequentially means that updating a file creates obsolete versions of data blocks and old inodes elsewhere in the log, creating "holes" or dead space. Over time, free space becomes fragmented across old segments.
      </p>
      <ul>
        <li><strong>Segment Cleaner Daemon:</strong> LFS runs a continuous background cleaning process that reads existing segments, identifies live blocks (blocks still referenced by current inodes), and compacts them into new, tightly packed clean segments.</li>
        <li><strong>Cost-Benefit Cleaning Policies:</strong> Because cleaning requires reading, moving, and rewriting data (incurring write amplification overhead), advanced LFS implementations prioritize cleaning segments based on a cost-benefit formula that balances segment age (how long dead space has sat idle) against the degree of fragmentation.</li>
      </ul>
    </div>

    <!-- Section 4.3.6: Journaling File Systems -->
    <div class="card">
      <h2>4.3.6 Journaling File Systems</h2>
      <p>
        System crashes mid-write often leave traditional filesystems in an inconsistent state, requiring lengthy full-volume integrity scans (such as <code>fsck</code>). <strong>Journaling File Systems</strong> introduce Write-Ahead Logging (WAL) to guarantee crash consistency.
      </p>
    </div>

    <!-- Section 4.3.7: Flash Storage & Wear-Leveling -->
    <div class="card">
      <h2>4.3.7 Flash Storage &amp; Wear-Leveling Systems</h2>
      <p>
        Solid-state drives built on NAND flash memory replace mechanical platters with electronic memory cells, requiring specialized FTL layers and wear-leveling algorithms.
      </p>
    </div>

    <!-- Section 4.3.8: Virtual File Systems (VFS) -->
    <div class="card">
      <h2>4.3.8 Virtual File Systems (VFS)</h2>
      <p>
        Modern operating systems implement the Virtual File System (VFS) abstraction layer to support multiple disparate storage formats seamlessly through standard objects.
      </p>
    </div>

  </div>

  <script>
    const TOTAL_CELLS = 3000;
    let cells = [];
    let isRunning = false;
    let stepTimer = null;
    let stepDelay = 45;
    let currentTheme = 'modern';
    let selectedCapacityMB = 500;
    let startTime = 0;
    let elapsedTimer = null;
    let audioEnabled = true;

    function toggleAudioMute() {
      audioEnabled = !audioEnabled;
      const btn = document.getElementById("btnAudioToggle");
      const audioEl = document.getElementById("defragAudio");
      if (audioEnabled) {
        btn.textContent = "🔊 Audio: On";
        btn.style.background = "#059669";
        if (isRunning && (currentTheme === 'dos' || currentTheme === 'olddos') && audioEl) {
          audioEl.play().catch(e => console.log("Audio play failed:", e));
        }
      } else {
        btn.textContent = "🔇 Audio: Off";
        btn.style.background = "#0284c7";
        if (audioEl) audioEl.pause();
      }
    }

    function selectDiskCapacity(sizeMB) {
      selectedCapacityMB = sizeMB;
      [10, 100, 500, 1000].forEach(s => {
        const b = document.getElementById(`size-${s}`);
        if (b) b.classList.toggle('active', s === sizeMB);
      });
      updateShellTitle();
      defragInitVolume();
    }

    function updateShellTitle() {
      const titleEl = document.getElementById("shellTitle");
      const label = selectedCapacityMB >= 1000 ? "1 GB" : `${selectedCapacityMB} MB`;
      if (currentTheme === 'modern') titleEl.textContent = `FAT32 Volume Optimizer (${label} Drive)`;
      else if (currentTheme === 'win95') titleEl.textContent = `Disk Defragmenter - Drive C: (${label} FAT)`;
      else if (currentTheme === 'dos') titleEl.textContent = `NORTON SPEED DISK - DRIVE C: [${label}]`;
      else if (currentTheme === 'olddos') titleEl.textContent = `Optimize            Esc=Stop Defrag`;
    }

    function switchTheme(theme) {
      currentTheme = theme;
      const shell = document.getElementById("defragShell");
      shell.className = `defrag-outer-frame theme-${theme}`;

      ['modern', 'win95', 'dos', 'olddos'].forEach(t => {
        const b = document.getElementById(`btn-theme-${t}`);
        if (b) b.classList.toggle('active', t === theme);
      });

      const leg = document.getElementById("modernLegend");
      if (leg) leg.style.display = (theme === 'modern') ? 'flex' : 'none';

      const dosLeg = document.getElementById("dosLegendBox");
      if (dosLeg) dosLeg.style.display = (theme === 'olddos') ? 'grid' : 'none';

      updateShellTitle();
      renderAllCells();

      if (theme === 'dos' || theme === 'olddos') {
        setDefragSpeed(150, 'spd-slow');
        defragHeavyChurn();
        defragPause();
        defragToggleRun();
        if (audioEnabled) {
          const audioEl = document.getElementById("defragAudio");
          if (audioEl) {
            audioEl.currentTime = 0;
            audioEl.volume = 0.05;
            audioEl.play().catch(e => console.log("Audio autoplay blocked:", e));
          }
        }
      } else {
        defragPause();
      }
    }

    function setDefragSpeed(ms, activeId) {
      stepDelay = ms;
      ['spd-slow', 'spd-norm', 'spd-fast'].forEach(id => {
        const btn = document.getElementById(id);
        if (btn) btn.classList.toggle('active', id === activeId);
      });
    }

    function initMatrix() {
      const grid = document.getElementById("clusterGrid");
      grid.innerHTML = "";
      cells = [];
      for (let i = 0; i < TOTAL_CELLS; i++) {
        const d = document.createElement("div");
        d.className = "c-cell c-free";
        d.id = `blk-${i}`;
        grid.appendChild(d);
        cells.push({ state: "free", isSystem: false, fileId: null });
      }
    }

    function renderCell(idx) {
      const el = document.getElementById(`blk-${idx}`);
      const c = cells[idx];
      el.className = "c-cell";
      el.textContent = "";

      if (currentTheme === 'olddos') {
        if (c.state === "read") { el.classList.add("c-read"); el.textContent = "r"; }
        else if (c.state === "write") { el.classList.add("c-write"); el.textContent = "W"; }
        else if (c.isSystem) { el.classList.add("c-system"); el.textContent = "X"; }
        else if (c.state === "optimized" || c.state === "unoptimized") { el.classList.add("c-opt"); el.textContent = "■"; }
        else { el.classList.add("c-free"); }
      } else if (currentTheme === 'dos') {
        if (c.state === "read") { el.classList.add("c-read"); el.textContent = "R"; }
        else if (c.state === "write") { el.classList.add("c-write"); el.textContent = "W"; }
        else if (c.isSystem) { el.classList.add("c-system"); el.textContent = "X"; }
        else if (c.state === "optimized") { el.classList.add("c-opt"); el.textContent = "■"; }
        else if (c.state === "unoptimized") { el.classList.add("c-unopt"); el.textContent = "▓"; }
        else { el.classList.add("c-free"); el.textContent = "·"; }
      } else {
        if (c.state === "read") el.classList.add("c-read");
        else if (c.state === "write") el.classList.add("c-write");
        else if (c.isSystem) el.classList.add("c-system");
        else if (c.state === "optimized") el.classList.add("c-opt");
        else if (c.state === "unoptimized") el.classList.add("c-unopt");
        else el.classList.add("c-free");
      }
    }

    function renderAllCells() {
      for (let i = 0; i < TOTAL_CELLS; i++) renderCell(i);
      updateStatus();
    }

    function defragInitVolume() {
      defragPause();
      initMatrix();
      const unmovable = [36, 110, 224, 320, 480, 780, 1040, 1420, 1780, 2280, 2760];
      unmovable.forEach(idx => { if (idx < TOTAL_CELLS) cells[idx] = { state: "unmovable", isSystem: true, fileId: "sys" }; });

      const optCutoff = Math.floor(TOTAL_CELLS * 0.18);
      for (let i = 0; i < optCutoff; i++) {
        if (!cells[i].isSystem) cells[i] = { state: "optimized", isSystem: false, fileId: "opt" };
      }
      for (let i = optCutoff; i < Math.floor(TOTAL_CELLS * 0.70); i++) {
        if (!cells[i].isSystem) cells[i] = { state: "unoptimized", isSystem: false, fileId: `f_${i % 25}` };
      }
      renderAllCells();
    }

    function defragHeavyChurn() {
      defragPause();
      if (cells.length === 0) initMatrix();
      for (let i = 0; i < TOTAL_CELLS; i++) {
        if (cells[i].isSystem) continue;
        let row = Math.floor(i / 100);
        if (row < 5) cells[i] = { state: "optimized", isSystem: false, fileId: "opt" };
        else {
          let seed = (i * 31 + row * 43) % 100;
          if (seed > 46) cells[i] = { state: "unoptimized", isSystem: false, fileId: `f_${seed % 15}` };
          else cells[i] = { state: "free", isSystem: false, fileId: null };
        }
      }
      const unmovable = [36, 110, 224, 320, 480, 780, 1040, 1420, 1780, 2280, 2760];
      unmovable.forEach(idx => { if (idx < TOTAL_CELLS) cells[idx] = { state: "unmovable", isSystem: true, fileId: "sys" }; });
      renderAllCells();
    }

    function updateStatus() {
      const opt = cells.filter(c => c.state === "optimized").length;
      const unopt = cells.filter(c => c.state === "unoptimized").length;
      const totalData = opt + unopt;
      const pct = totalData > 0 ? Math.round((opt / totalData) * 100) : 0;
      document.getElementById("txtProgressMetric").textContent = `Optimization: ${pct}% | Clusters: ${totalData}/3,000`;
      const dosPct = document.getElementById("dosPctText");
      if (dosPct) dosPct.textContent = `${pct}%`;
      const dosBar = document.getElementById("dosProgressBarFill");
      if (dosBar) dosBar.style.width = `${pct}%`;
    }

    function defragToggleRun() {
      const audioEl = document.getElementById("defragAudio");
      if (isRunning) {
        defragPause();
      } else {
        if (cells.length === 0 || cells.filter(c => c.state === "unoptimized").length === 0) defragHeavyChurn();
        isRunning = true;
        startTime = Date.now();
        if (audioEnabled && (currentTheme === 'dos' || currentTheme === 'olddos') && audioEl) {
          audioEl.currentTime = 0;
          audioEl.volume = 0.05;
          audioEl.play().catch(e => console.log("Audio play failed:", e));
        }
        const btn = document.getElementById("btnStartDefrag");
        btn.textContent = "Pause";
        btn.style.background = "#b91c1c";
        runDefragCycle();
      }
    }

    function defragPause() {
      isRunning = false;
      if (stepTimer) clearTimeout(stepTimer);
      const audioEl = document.getElementById("defragAudio");
      if (audioEl) audioEl.pause();
      const btn = document.getElementById("btnStartDefrag");
      if (btn) { btn.textContent = "Start Defrag"; btn.style.background = "#059669"; }
      renderAllCells();
    }

    function runDefragCycle() {
      if (!isRunning) return;
      let firstFree = -1;
      for (let i = 0; i < TOTAL_CELLS; i++) { if (cells[i].state === "free") { firstFree = i; break; } }
      let sourceBlocks = [];
      for (let i = TOTAL_CELLS - 1; i > firstFree; i--) {
        if (cells[i].state === "unoptimized" && !cells[i].isSystem) { sourceBlocks.push(i); if (sourceBlocks.length >= 4) break; }
      }
      if (firstFree === -1 || sourceBlocks.length === 0) { defragPause(); return; }
      sourceBlocks.forEach(idx => { cells[idx].state = "read"; renderCell(idx); });
      stepTimer = setTimeout(() => {
        if (!isRunning) return;
        let targetSlots = [];
        for (let i = firstFree; i < TOTAL_CELLS && targetSlots.length < sourceBlocks.length; i++) {
          if (cells[i].state === "free") { targetSlots.push(i); cells[i].state = "write"; renderCell(i); }
        }
        stepTimer = setTimeout(() => {
          if (!isRunning) return;
          sourceBlocks.forEach(idx => { cells[idx] = { state: "free", isSystem: false, fileId: null }; renderCell(idx); });
          targetSlots.forEach(idx => { cells[idx] = { state: "optimized", isSystem: false, fileId: "opt" }; renderCell(idx); });
          updateStatus();
          stepTimer = setTimeout(runDefragCycle, stepDelay);
        }, stepDelay);
      }, stepDelay);
    }

    initMatrix();
    selectDiskCapacity(500);
    switchTheme('modern');
  </script>
</body>
</html>
"""

def read_and_encode_audio(audio_path):
    print(f"--> Reading audio file from {audio_path}...")
    if not os.path.exists(audio_path):
        print(f"Error: Could not find audio file at {audio_path}", file=sys.stderr)
        sys.exit(1)
    with open(audio_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def execute_git_command(cmd, desc):
    print(f"--> {desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout.strip():
        print(res.stdout.strip())
    if res.stderr.strip():
        print(f"[{desc} stderr]\n{res.stderr.strip()}")
    if res.returncode != 0 and "nothing to commit" not in res.stdout and "nothing to commit" not in res.stderr:
        print(f"Error during {desc} (code {res.returncode})", file=sys.stderr)
        sys.exit(res.returncode)

def execute_deployment():
    audio_file = os.path.join("images", "defrag2.mp3")
    html_file = os.path.join("week10-file-management", "03-filesystem-implementation.html")

    base64_str = read_and_encode_audio(audio_file)
    data_uri = f"data:audio/mp3;base64,{base64_str}"

    print(f"--> Writing complete file structure to {html_file}...")
    os.makedirs(os.path.dirname(html_file), exist_ok=True)
    final_content = HTML_CONTENT.replace("AUDIO_DATA_URI_PLACEHOLDER", data_uri)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(final_content)
    print("--> HTML structure successfully written!")

    commit_msg = (
        "Add explicit Wikipedia entry links to pioneer cards in LFS infobox\n\n"
        "Update week10-file-management/03-filesystem-implementation.html to include "
        "direct Wikipedia biography hyperlinks in John Ousterhout and Mendel Rosenblum's "
        "pioneer metadata cards."
    )

    execute_git_command(["git", "add", html_file], "Staging HTML file")
    execute_git_command(["git", "commit", "-am", commit_msg], "Committing changes")
    execute_git_command(["git", "push", "origin", "main"], "Pushing changes to origin")
    print("--> Deployment complete!")

if __name__ == "__main__":
    execute_deployment()
