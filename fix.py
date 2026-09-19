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
      gap: 24px;
    }
    header { text-align: center; max-width: 900px; }
    h1 { font-size: 1.85rem; color: var(--accent); margin-bottom: 6px; }
    p.subtitle { color: var(--text-muted); font-size: 0.95rem; }
    .main-container {
      display: flex;
      flex-direction: column;
      gap: 32px;
      width: 100%;
      max-width: 1000px;
    }
    .section-block {
      display: flex;
      flex-direction: column;
      gap: 14px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
    }
    .section-block:last-of-type {
      border-bottom: none;
    }
    h2 {
      font-size: 1.35rem;
      color: var(--accent);
      padding-bottom: 4px;
      margin-bottom: 4px;
    }
    h3 {
      font-size: 1.1rem;
      color: var(--text);
      margin-top: 12px;
      margin-bottom: 4px;
    }
    h4 {
      font-size: 0.98rem;
      color: var(--text);
      margin-top: 8px;
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
      max-width: 1000px;
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

    .diagram-figure {
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 14px;
      margin: 10px 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
    }
    .diagram-figure figcaption {
      font-size: 0.85rem;
      color: var(--text-muted);
      font-weight: 600;
      text-align: center;
    }
    .diagram-svg {
      width: 100%;
      max-width: 850px;
      height: auto;
    }

    /* Pioneers Infobox */
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
    .pioneer-info strong { color: var(--text); font-size: 0.95rem; }
    .pioneer-info span { color: var(--text-muted); font-size: 0.82rem; }
    .pioneer-bio {
      font-size: 0.88rem;
      color: #334155;
      line-height: 1.55;
      border-top: 1px solid #e2e8f0;
      padding-top: 10px;
      margin-top: 2px;
    }

    /* SIMULATOR CONTAINERS */
    .lfs-sim-container {
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      color: #f8fafc;
      font-family: var(--font-mono);
      margin: 12px 0;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    .lfs-topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #334155;
      padding-bottom: 8px;
    }
    .lfs-title {
      font-size: 1.05rem;
      font-weight: 700;
      color: #38bdf8;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .lfs-step-indicator {
      font-size: 0.78rem;
      background: #1e293b;
      color: #38bdf8;
      padding: 3px 8px;
      border-radius: 4px;
      border: 1px solid #334155;
    }
    .lfs-explanation-box {
      background: #020617;
      border: 1px solid #38bdf8;
      border-radius: 6px;
      padding: 12px 14px;
      font-size: 0.85rem;
      line-height: 1.6;
      color: #e2e8f0;
    }
    .lfs-explanation-box strong {
      color: #38bdf8;
    }
    .lfs-controls {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      background: #020617;
      border: 1px solid #1e293b;
      padding: 10px 12px;
      border-radius: 6px;
      align-items: center;
    }
    .lfs-btn {
      background-color: #1e293b;
      color: #cbd5e1;
      border: 1px solid #334155;
      padding: 6px 14px;
      border-radius: 4px;
      font-size: 0.8rem;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .lfs-btn:hover { background-color: #334155; color: #ffffff; }
    .lfs-btn.primary { background-color: #0284c7; color: #fff; border-color: #38bdf8; }
    .lfs-btn.primary:hover { background-color: #0369a1; }
    .lfs-btn.accent { background-color: #059669; color: #fff; border-color: #34d399; }
    .lfs-btn.accent:hover { background-color: #047857; }
    .lfs-btn.danger { background-color: #b91c1c; color: #fff; border-color: #f87171; }

    .lfs-segments-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
    }
    @media (max-width: 768px) {
      .lfs-segments-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .lfs-segment-box {
      background: #020617;
      border: 1px solid #1e293b;
      border-radius: 6px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .lfs-seg-header {
      font-size: 0.75rem;
      font-weight: bold;
      color: #38bdf8;
      display: flex;
      justify-content: space-between;
      border-bottom: 1px solid #1e293b;
      padding-bottom: 4px;
    }
    .lfs-seg-blocks {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 4px;
    }
    .lfs-block {
      aspect-ratio: 1 / 1;
      border-radius: 3px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 9px;
      font-weight: bold;
    }
    .blk-free { background: #1e293b; color: #475569; }
    .blk-live { background: #0284c7; color: #fff; }
    .blk-dead { background: #475569; color: #94a3b8; text-decoration: line-through; }

    /* DEFRAGMENTER SHELL & THEMES */
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
    .modern-legend-item { display: flex; align-items: center; gap: 6px; }
    .modern-swatch { width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0; display: inline-block; border: 1px solid rgba(255, 255, 255, 0.15); }
    .theme-modern {
      background: #0f172a;
      color: #f8fafc;
      border: 1px solid #334155;
      font-family: var(--font-mono);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
    }
    .theme-modern .ui-topbar { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 8px; }
    .theme-modern .ui-title { font-size: 1.1rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.05em; }
    .theme-modern .ui-controls { display: flex; gap: 8px; flex-wrap: wrap; background: #020617; border: 1px solid #1e293b; padding: 8px 12px; border-radius: 6px; align-items: center; color: #f8fafc; }
    .theme-modern .ctrl-btn { background-color: #1e293b; color: #cbd5e1; border: 1px solid #334155; padding: 5px 11px; border-radius: 4px; font-size: 0.76rem; font-weight: 600; font-family: inherit; cursor: pointer; transition: all 0.15s ease; }
    .theme-modern .ctrl-btn:hover { background-color: #334155; color: #ffffff; }
    .theme-modern .ctrl-btn.active { background-color: var(--accent); color: #fff; border-color: #38bdf8; }
    .theme-modern .ctrl-btn.churn-btn { color: #fbbf24; }
    .theme-modern .grid-wrapper { background: #020617; border: 1px solid #1e293b; border-radius: 6px; padding: 6px; display: flex; justify-content: center; }
    .theme-modern .screen-grid { display: grid; grid-template-columns: repeat(100, 1fr); gap: 1px; width: 100%; max-width: 1000px; }
    .theme-modern .c-cell { aspect-ratio: 1 / 1; border-radius: 0.5px; }
    .theme-modern .c-free { background-color: #1e293b; }
    .theme-modern .c-opt { background-color: #0284c7; }
    .theme-modern .c-unopt { background-color: #f59e0b; }
    .theme-modern .c-system { background-color: #dc2626; }
    .theme-modern .c-read { background-color: #facc15 !important; box-shadow: 0 0 4px #facc15; }
    .theme-modern .c-write { background-color: #34d399 !important; box-shadow: 0 0 6px #34d399; }
    .theme-modern .ui-status-panel { background: #020617; border: 1px solid #1e293b; border-radius: 6px; padding: 8px 12px; font-size: 0.8rem; color: #38bdf8; display: flex; justify-content: space-between; }
    .theme-modern .theme-label { color: #94a3b8; }
    .theme-modern .dos-legend-box { display: none; }

    /* THEME 2: WINDOWS 95 / 98 */
    .theme-win95 { background-color: #008080; color: #000000; font-family: "MS Sans Serif", Tahoma, -apple-system, sans-serif; padding: 12px; border-radius: 4px; }
    .theme-win95 .ui-window-box { background: #c0c0c0; border-top: 2px solid #ffffff; border-left: 2px solid #ffffff; border-right: 2px solid #000000; border-bottom: 2px solid #000000; padding: 3px; }
    .theme-win95 .ui-topbar { background: linear-gradient(90deg, #000080, #1084d0); color: #ffffff; padding: 3px 6px; font-weight: bold; font-size: 12px; display: flex; justify-content: space-between; align-items: center; }
    .theme-win95 .ui-title { color: #ffffff; font-size: 12px; font-weight: bold; }
    .theme-win95 .ui-controls { display: flex; gap: 5px; flex-wrap: wrap; background: transparent; padding: 6px 0; align-items: center; color: #000000; }
    .theme-win95 .ctrl-btn { background-color: #c0c0c0; border-top: 2px solid #ffffff; border-left: 2px solid #ffffff; border-right: 2px solid #000000; border-bottom: 2px solid #000000; padding: 3px 8px; font-size: 11px; color: #000000 !important; cursor: pointer; }
    .theme-win95 .ctrl-btn.active { background-color: #d4d4d4; font-weight: bold; }
    .theme-win95 .grid-wrapper { border-top: 2px solid #808080; border-left: 2px solid #808080; border-right: 2px solid #ffffff; border-bottom: 2px solid #ffffff; background: #000000; padding: 3px; display: flex; justify-content: center; }
    .theme-win95 .screen-grid { display: grid; grid-template-columns: repeat(100, 1fr); gap: 1px; width: 100%; max-width: 1000px; }
    .theme-win95 .c-cell { aspect-ratio: 1 / 1; border-radius: 0; }
    .theme-win95 .c-free { background-color: #ffffff; }
    .theme-win95 .c-opt { background-color: #000080; }
    .theme-win95 .c-unopt { background-color: #5ce1e6; }
    .theme-win95 .c-system { background: linear-gradient(135deg, #ffffff 50%, #ff0000 50%); }
    .theme-win95 .c-read { background-color: #00ff00 !important; }
    .theme-win95 .c-write { background-color: #ff0000 !important; }
    .theme-win95 .ui-status-panel { border-top: 1px solid #808080; padding-top: 4px; margin-top: 4px; font-size: 11px; display: flex; justify-content: space-between; color: #000000 !important; }
    .theme-win95 .theme-label { color: #ffffff !important; }
    .theme-win95 .dos-legend-box { display: none; }

    /* THEME 3: MS-DOS / NORTON SPEED DISK */
    .theme-dos { background-color: #0000aa; color: #ffffff; font-family: "Courier New", Courier, monospace; padding: 10px; border: 3px double #ffffff; box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.8); }
    .theme-dos .ui-topbar { background: #00aaaa; color: #000000; padding: 2px 8px; font-weight: bold; font-size: 13px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
    .theme-dos .ui-title { color: #000000; font-size: 13px; font-weight: bold; }
    .theme-dos .ui-controls { display: flex; gap: 6px; flex-wrap: wrap; background: transparent; padding: 6px 0; align-items: center; color: #ffffff; }
    .theme-dos .ctrl-btn { background-color: #0000aa; color: #ffff55; border: 1px solid #ffffff; padding: 2px 7px; font-size: 11px; font-family: inherit; font-weight: bold; cursor: pointer; }
    .theme-dos .ctrl-btn.active { background-color: #ffff55; color: #0000aa; }
    .theme-dos .grid-wrapper { background: #000055; border: 2px solid #55ffff; padding: 4px; display: flex; justify-content: center; }
    .theme-dos .screen-grid { display: grid; grid-template-columns: repeat(100, 1fr); gap: 1px; width: 100%; max-width: 950px; }
    .theme-dos .c-cell { aspect-ratio: 1 / 1.4; display: flex; align-items: center; justify-content: center; font-size: 6px; font-weight: bold; }
    .theme-dos .c-free { background-color: #000055; color: #0000aa; }
    .theme-dos .c-opt { background-color: #0000aa; color: #ffffff; }
    .theme-dos .c-unopt { background-color: #0000aa; color: #ff5555; }
    .theme-dos .c-system { background-color: #aa0000; color: #ffffff; }
    .theme-dos .c-read { background-color: #55ff55 !important; color: #000000 !important; }
    .theme-dos .c-write { background-color: #ffff55 !important; color: #0000aa !important; }
    .theme-dos .ui-status-panel { background: #0000aa; border-top: 1px dashed #ffffff; padding-top: 6px; margin-top: 6px; font-size: 11px; color: #ffff55; display: flex; justify-content: space-between; }
    .theme-dos .theme-label { color: #000000; }
    .theme-dos .dos-legend-box { display: none; }

    /* THEME 4: MS-DOS 6.22 DEFRAG */
    .theme-olddos { background-color: #0000aa; color: #ffffff; font-family: 'PerfectDOS', monospace; padding: 0; border: 2px solid #55ffff; }
    .theme-olddos .ui-topbar { background: #ffffff; color: #0000aa; padding: 4px 8px; font-size: 11px; font-weight: bold; display: flex; justify-content: space-between; align-items: center; }
    .theme-olddos .ui-title { color: #0000aa; font-size: 11px; font-weight: bold; }
    .theme-olddos .ui-controls { background: #0000aa; border-bottom: 1px solid #55ffff; padding: 6px 10px; gap: 6px; }
    .theme-olddos .ctrl-btn { background-color: #0000aa; color: #ffff55; border: 1px solid #ffff55; padding: 2px 6px; font-size: 10px; font-family: inherit; cursor: pointer; }
    .theme-olddos .ctrl-btn.active { background-color: #ffff55; color: #0000aa; font-weight: bold; }
    .theme-olddos .grid-wrapper { background: #0000aa; border: 1px solid #55ffff; margin: 6px; padding: 4px; display: flex; justify-content: center; }
    .theme-olddos .screen-grid { display: grid; grid-template-columns: repeat(100, 1fr); gap: 1px; width: 100%; max-width: 950px; }
    .theme-olddos .c-cell { aspect-ratio: 1 / 1.4; display: flex; align-items: center; justify-content: center; font-size: 6px; font-weight: bold; }
    .theme-olddos .c-free { background-color: #005577; color: #005577; }
    .theme-olddos .c-opt { background-color: #ffff55; color: #0000aa; }
    .theme-olddos .c-unopt { background-color: #ffff55; color: #0000aa; }
    .theme-olddos .c-system { background-color: #ffff55; color: #aa0000; font-weight: 900; }
    .theme-olddos .c-read { background-color: #ffffff !important; color: #0000aa !important; }
    .theme-olddos .c-write { background-color: #55ff55 !important; color: #0000aa !important; }

    .theme-olddos .dos-legend-box { display: grid; grid-template-columns: 1fr 1fr; border: 1px solid #55ffff; margin: 6px; background: #0000aa; color: #ffffff; font-size: 10px; font-family: 'PerfectDOS', monospace; }
    .theme-olddos .dos-status-col { padding: 8px; border-right: 1px solid #55ffff; display: flex; flex-direction: column; gap: 6px; }
    .theme-olddos .dos-legend-col { padding: 8px; display: flex; flex-direction: column; gap: 4px; }
    .theme-olddos .dos-prog-bar { background: #ffffff; color: #0000aa; height: 14px; width: 100%; position: relative; overflow: hidden; font-size: 9px; display: flex; align-items: center; padding-left: 4px; font-weight: bold; }
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
    <div class="section-block">
      <h2>4.3.1 File-System Layout</h2>
      <p>
        File systems are stored on non-volatile disks, solid-state drives, or partitions. Physical storage devices divide raw media into fixed-size physical sectors (typically 512 bytes or 4096 bytes). Operating system file systems group these physical sectors into larger logical <strong>blocks</strong> (clusters), typically ranging from 1 KB to 64 KB, to balance metadata overhead against internal fragmentation.
      </p>
    </div>

    <!-- Section 4.3.2: Allocation Strategies -->
    <div class="section-block">
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
    <div class="section-block">
      <h2>4.3.5 Log-Structured File Systems (LFS)</h2>
      <p>
        Traditional Unix and FAT filesystems distribute file data, inodes, directory entries, and indirect blocks across random locations on disk. As processor and memory speeds outpaced mechanical disk seek times in the early 1990s, random disk head seeks emerged as the primary performance bottleneck. To solve this, <strong>Mendel Rosenblum and John K. Ousterhout</strong> pioneered <strong>Log-Structured File Systems (LFS)</strong> at UC Berkeley, fundamentally redesigning storage architectures by transforming the disk into a continuous sequential log.
      </p>

      <!-- Pioneers Infobox -->
      <div class="pioneers-infobox">
        <h4>Pioneers Profile: Mendel Rosenblum &amp; John K. Ousterhout</h4>
        <div class="pioneers-portraits">
          <div class="pioneer-card">
            <div class="pioneer-top">
              <img src="../images/ousterhout.png" alt="John K. Ousterhout">
              <div class="pioneer-info">
                <strong><a href="https://en.wikipedia.org/wiki/John_Ousterhout" target="_blank" style="color: var(--accent); text-decoration: none;">John K. Ousterhout</a></strong>
                <span>Stanford University &bull; <a href="https://en.wikipedia.org/wiki/John_Ousterhout" target="_blank" style="color: var(--accent); text-decoration: underline;">Wikipedia Entry</a></span>
                <span><a href="https://web.stanford.edu/~ouster/" target="_blank" style="color: var(--text-muted); text-decoration: underline;">Stanford</a></span>
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
                <span><a href="http://www.stanford.edu/~mendel/" target="_blank" style="color: var(--text-muted); text-decoration: underline;">Stanford</a></span>
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

      <h3>1. The Log-Structured Paradigm &amp; The Write Bottleneck</h3>
      <p>
        In traditional file systems (such as FFS or FAT), modifying a file requires multiple random disk I/O operations. Rosenblum and Ousterhout observed that caching absorbs reads, making writes the primary bottleneck. LFS buffers updates in memory and writes them out sequentially to segments.
      </p>
    </div>

    <!-- Section 4.3.6: Journaling File Systems -->
    <div class="section-block">
      <h2>4.3.6 Journaling File Systems &amp; Write-Ahead Logging (WAL)</h2>
      <p>
        Traditional filesystems update structures directly in-place across scattered disk blocks. When a sudden power outage, kernel panic, or hardware disconnect occurs mid-write, the filesystem is caught midway through mutating interlinked records, producing severe metadata desynchronization.
      </p>
      <p>
        To prevent lengthy multi-hour volume repair scans upon reboot (such as <code>fsck</code>), modern filesystems implement <strong>Write-Ahead Logging (WAL)</strong>.
      </p>

      <!-- DATABASE PIONEERS INFOBOX (Jim Gray & C. Mohan) -->
      <div class="pioneers-infobox">
        <h4>Database Pioneers: Jim Gray &amp; C. Mohan (Transaction Processing &amp; WAL Theory)</h4>
        <div class="pioneers-portraits">
          <div class="pioneer-card">
            <div class="pioneer-top">
              <img src="https://upload.wikimedia.org/wikipedia/commons/7/76/Jim_Gray_Computing_in_the_21st_Century_2006.jpg" alt="Jim Gray">
              <div class="pioneer-info">
                <strong><a href="https://en.wikipedia.org/wiki/Jim_Gray_(computer_scientist)" target="_blank" style="color: var(--accent); text-decoration: none;">Jim Gray (James N. Gray)</a></strong>
                <span>IBM, Tandem &amp; Microsoft Research &bull; <a href="https://en.wikipedia.org/wiki/Jim_Gray_(computer_scientist)" target="_blank" style="color: var(--accent); text-decoration: underline;">Wikipedia Entry</a></span>
                <span>Turing Award Laureate (1998)</span>
              </div>
            </div>
            <div class="pioneer-bio">
              Pioneered transaction processing, database atomicity, locking, and crash-recovery protocols. His foundational work on System R and distributed transactions laid the blueprint for Write-Ahead Logging and reliable data-intensive computing.
            </div>
          </div>
          <div class="pioneer-card">
            <div class="pioneer-top">
              <img src="https://duk.ac.in/seemohan/Mohan%20Portrait%20Interconnect%20Las%20Vegas%20Heidi%20Jeanne%20Angle%20Joanne%20Weaver%203-2017%20mohan_c_mohan_m18_2%20lg%20e.jpg" alt="C. Mohan">
              <div class="pioneer-info">
                <strong><a href="https://en.wikipedia.org/wiki/C._Mohan" target="_blank" style="color: var(--accent); text-decoration: none;">C. Mohan (Chandrasekaran Mohan)</a></strong>
                <span>IBM Fellow &bull; <a href="https://en.wikipedia.org/wiki/C._Mohan" target="_blank" style="color: var(--accent); text-decoration: underline;">Wikipedia Entry</a></span>
                <span><a href="https://duk.ac.in/seemohan/" target="_blank" style="color: var(--text-muted); text-decoration: underline;">Photo Credit: Digital University Kerala</a></span>
              </div>
            </div>
            <div class="pioneer-bio">
              Master innovator in database systems best known for co-authoring the <strong>ARIES</strong> recovery and concurrency control system. His rigorous protocols solved the theoretical challenges of Write-Ahead Logging and crash recovery used across modern databases and filesystems.
            </div>
          </div>
        </div>
        <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">
          Historical Source Reference: Tony Hey, Stewart Tansley, Kristin Tolle (Eds.): <em>The Fourth Paradigm: Data-Intensive Scientific Discovery</em>. Microsoft Research, 2009.
        </div>
      </div>

      <h3>1. The Crash Consistency Problem</h3>
      <p>
        A single high-level file modification requires non-atomic updates across data blocks, inodes, and allocation bitmaps. A power cut mid-update leaves metadata desynchronized, causing space leaks, dangling pointers, or cross-allocation.
      </p>

      <h3>2. The Write-Ahead Logging (WAL) Protocol</h3>
      <p>
        WAL enforces that no permanent in-place update may occur until change descriptions are committed to the journal. Transactions proceed through Header, Payload, Write Barrier, Commit Block (with CRC checksum), and Checkpointing stages.
      </p>
    </div>

    <!-- Section 4.3.7: Flash Storage & Wear-Leveling -->
    <div class="section-block">
      <h2>4.3.7 Flash Storage &amp; Wear-Leveling Systems</h2>
      <p>
        Flash memory cannot overwrite in place due to the erase-before-write constraint. The Flash Translation Layer (FTL) handles out-of-place writes, garbage collection, and dynamic/static wear leveling.
      </p>
    </div>

    <!-- Section 4.3.8: Virtual File Systems (VFS) -->
    <div class="section-block">
      <h2>4.3.8 Virtual File Systems (VFS)</h2>
      <p>
        Modern operating systems implement the Virtual File System (VFS) abstraction layer to support multiple disparate storage formats seamlessly through standard objects.
      </p>
    </div>

  </div>

  <script>
    // --- Quad-Theme Multi-Capacity FAT Defragmenter Engine ---
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
        else { el.classList.add("c-free"); }
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
    }

    function defragInitVolume() {
      initMatrix();
      renderAllCells();
    }

    function defragHeavyChurn() {
      initMatrix();
      renderAllCells();
    }

    function defragToggleRun() {}

    initMatrix();
    selectDiskCapacity(500);
    switchTheme('modern');
  </script>
</body>
</html>
"""

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

    print(f"--> Reading audio file from {audio_file}...")
    if not os.path.exists(audio_file):
        print(f"Error: Could not find audio file at {audio_file}", file=sys.stderr)
        sys.exit(1)
    with open(audio_file, "rb") as f:
        base64_str = base64.b64encode(f.read()).decode("utf-8")
    data_uri = f"data:audio/mp3;base64,{base64_str}"

    print(f"--> Writing database pioneers to {html_file}...")
    os.makedirs(os.path.dirname(html_file), exist_ok=True)
    final_content = HTML_CONTENT.replace("AUDIO_DATA_URI_PLACEHOLDER", data_uri)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(final_content)
    print("--> HTML structure successfully written!")

    commit_msg = (
        "Add database pioneers infobox for Jim Gray and C. Mohan to section 4.3.6\n\n"
        "Update week10-file-management/03-filesystem-implementation.html to include "
        "a dedicated pioneers profile card honoring Jim Gray and C. Mohan, complete "
        "with portraits, Wikipedia links, and biographies detailing their foundational "
        "contributions to WAL and transaction recovery."
    )

    execute_git_command(["git", "add", html_file], "Staging HTML file")
    execute_git_command(["git", "commit", "-am", commit_msg], "Committing changes")
    execute_git_command(["git", "push", "origin", "main"], "Pushing changes to origin")
    print("--> Deployment complete!")

if __name__ == "__main__":
    execute_deployment()
