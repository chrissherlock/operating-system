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

    /* LFS SIMULATOR */
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
      padding: 6px 12px;
      border-radius: 4px;
      font-size: 0.78rem;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .lfs-btn:hover { background-color: #334155; color: #ffffff; }
    .lfs-btn.primary { background-color: #0284c7; color: #fff; border-color: #38bdf8; }
    .lfs-btn.primary:hover { background-color: #0369a1; }
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
    .lfs-status-panel {
      background: #020617;
      border: 1px solid #1e293b;
      border-radius: 6px;
      padding: 10px 14px;
      font-size: 0.8rem;
      color: #38bdf8;
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
    }

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
        In traditional file systems (such as FFS or FAT), modifying a file requires multiple random disk I/O operations: updating the inode, modifying indirect blocks, rewriting data blocks, and updating directory structures scattered across different cylinders. As CPU processing speeds and main memory sizes grew exponentially in the 1980s and 1990s, large main memory caches absorbed most read requests via buffer cache hits. Consequently, <strong>file reads became fast</strong>, but <strong>writes remained bottlenecked by mechanical disk seek times</strong> and rotational latency.
      </p>
      <p>
        Rosenblum and Ousterhout observed that disk technology trends favored sequential throughput over random access. LFS capitalizes on this by buffering all file system updates in memory and writing them out in large, contiguous blocks (called segments) to a single continuous log.
      </p>

      <!-- Diagram 1: Traditional vs LFS Write Layout -->
      <figure class="diagram-figure">
        <svg class="diagram-svg" viewBox="0 0 800 240" xmlns="http://www.w3.org/2000/svg">
          <rect width="800" height="240" fill="#ffffff" rx="6" stroke="#cbd5e1"/>
          <text x="400" y="28" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Figure 4.3.5A: Traditional In-Place Updates vs. LFS Sequential Append Log</text>

          <text x="200" y="55" font-family="sans-serif" font-size="12" font-weight="bold" fill="#dc2626" text-anchor="middle">Traditional File System (Random In-Place Writes)</text>
          <rect x="50" y="70" width="300" height="130" fill="#f8fafc" stroke="#94a3b8" rx="4"/>
          <rect x="70" y="90" width="60" height="30" fill="#f59e0b" rx="3"/><text x="100" y="110" font-family="sans-serif" font-size="10" fill="#fff" text-anchor="middle">Inode</text>
          <rect x="170" y="130" width="60" height="30" fill="#38bdf8" rx="3"/><text x="200" y="150" font-family="sans-serif" font-size="10" fill="#fff" text-anchor="middle">Data</text>
          <rect x="250" y="90" width="60" height="30" fill="#dc2626" rx="3"/><text x="280" y="110" font-family="sans-serif" font-size="10" fill="#fff" text-anchor="middle">Dir</text>
          <path d="M 130 105 Q 150 70 170 140" fill="none" stroke="#dc2626" stroke-width="2" stroke-dasharray="4,4"/>
          <path d="M 230 145 Q 240 70 250 105" fill="none" stroke="#dc2626" stroke-width="2" stroke-dasharray="4,4"/>
          <text x="200" y="215" font-family="sans-serif" font-size="11" fill="#475569" text-anchor="middle">Multiple random head seeks per write</text>

          <text x="600" y="55" font-family="sans-serif" font-size="12" font-weight="bold" fill="#0284c7" text-anchor="middle">Log-Structured File System (Sequential Log)</text>
          <rect x="450" y="70" width="310" height="130" fill="#f8fafc" stroke="#94a3b8" rx="4"/>
          <rect x="470" y="110" width="270" height="50" fill="#0284c7" rx="4"/>
          <text x="500" y="140" font-family="sans-serif" font-size="11" fill="#fff" font-weight="bold">Inode</text>
          <line x1="535" y1="110" x2="535" y2="160" stroke="#fff" stroke-width="2"/>
          <text x="570" y="140" font-family="sans-serif" font-size="11" fill="#fff" font-weight="bold">Data</text>
          <line x1="605" y1="110" x2="605" y2="160" stroke="#fff" stroke-width="2"/>
          <text x="640" y="140" font-family="sans-serif" font-size="11" fill="#fff" font-weight="bold">Inode</text>
          <line x1="675" y1="110" x2="675" y2="160" stroke="#fff" stroke-width="2"/>
          <text x="705" y="140" font-family="sans-serif" font-size="10" fill="#fff" font-weight="bold">Dir</text>
          <polygon points="745,135 735,125 735,145" fill="#0284c7"/>
          <text x="605" y="215" font-family="sans-serif" font-size="11" fill="#475569" text-anchor="middle">Single contiguous sequential stream (No seeks)</text>
        </svg>
        <figcaption>Figure 4.3.5A: Comparison of random in-place updates versus LFS continuous append logging.</figcaption>
      </figure>

      <!-- INTERACTIVE LFS SIMULATOR WIDGET -->
      <div class="lfs-sim-container" id="lfsSimulator">
        <div class="lfs-topbar">
          <span class="lfs-title">Interactive LFS Segment Append &amp; Garbage Collector Simulator</span>
          <span style="font-size: 0.75rem; color: #38bdf8;" id="lfsActiveSegLabel">Active Segment: Segment 0</span>
        </div>

        <div class="lfs-controls">
          <button class="lfs-btn primary" onclick="lfsWriteNewFile()">Append New File (Write)</button>
          <button class="lfs-btn" onclick="lfsUpdateExistingFile()">Overwrite Existing File</button>
          <button class="lfs-btn danger" onclick="lfsTriggerCleaner()">Run Segment Cleaner (GC)</button>
          <button class="lfs-btn" onclick="lfsResetSim()" style="margin-left: auto;">Reset Simulator</button>
        </div>

        <div class="lfs-segments-grid" id="lfsSegmentsGrid"></div>

        <div class="lfs-status-panel">
          <span id="lfsStatusMsg">Simulator Ready. Click 'Append New File' to write sequentially to the log tail.</span>
          <span id="lfsMetricMsg">Live Blocks: 0 | Dead Blocks: 0 | Free Blocks: 32</span>
        </div>
      </div>

      <h3>2. The Inode Map (Imap) Architecture &amp; Indirection</h3>
      <p>
        In a traditional Unix file system, every file has a fixed static disk address. In an LFS, because files and inodes are continually rewritten to the log tail, the inode's physical location changes with every update, requiring the <strong>inode map (imap)</strong> translation layer.
      </p>

      <!-- Diagram 2: Imap Architecture -->
      <figure class="diagram-figure">
        <svg class="diagram-svg" viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg">
          <rect width="800" height="200" fill="#ffffff" rx="6" stroke="#cbd5e1"/>
          <text x="400" y="28" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Figure 4.3.5B: The Inode Map (Imap) Dynamic Indirection Layer</text>

          <rect x="50" y="80" width="100" height="60" fill="#e0f2fe" stroke="#0284c7" rx="4"/>
          <text x="100" y="105" font-family="sans-serif" font-size="11" font-weight="bold" fill="#0369a1" text-anchor="middle">File Inode #</text>
          <text x="100" y="125" font-family="sans-serif" font-size="12" fill="#0f172a" text-anchor="middle">Inode 42</text>

          <line x1="150" y1="110" x2="220" y2="110" stroke="#0284c7" stroke-width="2"/>
          <polygon points="220,110 212,105 212,115" fill="#0284c7"/>

          <rect x="220" y="60" width="160" height="100" fill="#f1f5f9" stroke="#64748b" rx="4"/>
          <text x="300" y="85" font-family="sans-serif" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">Inode Map (Imap)</text>
          <text x="300" y="110" font-family="sans-serif" font-size="10" fill="#475569" text-anchor="middle">[0] &rarr; Block 102</text>
          <text x="300" y="130" font-family="sans-serif" font-size="10" fill="#0284c7" font-weight="bold" text-anchor="middle">[42] &rarr; Block 580</text>
          <text x="300" y="150" font-family="sans-serif" font-size="10" fill="#475569" text-anchor="middle">[43] &rarr; Block 312</text>

          <line x1="380" y1="110" x2="450" y2="110" stroke="#0284c7" stroke-width="2"/>
          <polygon points="450,110 442,105 442,115" fill="#0284c7"/>

          <rect x="450" y="80" width="300" height="60" fill="#0284c7" rx="4"/>
          <text x="600" y="105" font-family="sans-serif" font-size="11" font-weight="bold" fill="#fff" text-anchor="middle">Sequential Log Tail</text>
          <text x="600" y="125" font-family="sans-serif" font-size="10" fill="#e0f2fe" text-anchor="middle">Inode 42 (Block 580) + File Data</text>
        </svg>
        <figcaption>Figure 4.3.5B: How the Inode Map translates static file numbers to dynamic log addresses.</figcaption>
      </figure>

      <h3>3. Checkpoint Regions &amp; Rapid Crash Recovery</h3>
      <p>
        To locate the inode map during system startup without scanning the entire log, LFS maintains a fixed <strong>Checkpoint Region (CR)</strong> on disk, enabling fast roll-forward recovery upon reboot.
      </p>

      <h3>4. Background Garbage Collection &amp; Segment Cleaning</h3>
      <p>
        Appending data sequentially means that updating a file creates obsolete versions of data blocks and old inodes elsewhere in the log, creating dead space ("holes"). The background <strong>Segment Cleaner</strong> compacts live blocks into clean segments.
      </p>

      <!-- Diagram 3: Segment Cleaner Compaction -->
      <figure class="diagram-figure">
        <svg class="diagram-svg" viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg">
          <rect width="800" height="220" fill="#ffffff" rx="6" stroke="#cbd5e1"/>
          <text x="400" y="28" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Figure 4.3.5C: Background Segment Cleaner &amp; Compaction Process</text>

          <rect x="50" y="60" width="200" height="110" fill="#fef2f2" stroke="#f87171" rx="4"/>
          <text x="150" y="82" font-family="sans-serif" font-size="11" font-weight="bold" fill="#b91c1c" text-anchor="middle">Old Segment (Fragmented)</text>
          <rect x="70" y="100" width="35" height="40" fill="#0284c7" rx="2"/><text x="87.5" y="125" font-family="sans-serif" font-size="10" fill="#fff" text-anchor="middle">Live</text>
          <rect x="115" y="100" width="35" height="40" fill="#cbd5e1" rx="2"/><text x="132.5" y="125" font-family="sans-serif" font-size="10" fill="#475569" text-anchor="middle">Dead</text>
          <rect x="160" y="100" width="35" height="40" fill="#0284c7" rx="2"/><text x="177.5" y="125" font-family="sans-serif" font-size="10" fill="#fff" text-anchor="middle">Live</text>
          <rect x="205" y="100" width="35" height="40" fill="#cbd5e1" rx="2"/><text x="222.5" y="125" font-family="sans-serif" font-size="10" fill="#475569" text-anchor="middle">Dead</text>

          <line x1="250" y1="115" x2="310" y2="115" stroke="#0284c7" stroke-width="2"/>
          <polygon points="310,115 302,110 302,120" fill="#0284c7"/>
          <text x="280" y="105" font-family="sans-serif" font-size="9" fill="#0284c7" text-anchor="middle">Cleaner Reads</text>

          <rect x="310" y="75" width="180" height="80" fill="#f0f9ff" stroke="#0284c7" rx="4"/>
          <text x="400" y="98" font-family="sans-serif" font-size="11" font-weight="bold" fill="#0369a1" text-anchor="middle">Segment Cleaner</text>
          <text x="400" y="120" font-family="sans-serif" font-size="10" fill="#334155" text-anchor="middle">Extracts Live Blocks</text>
          <text x="400" y="138" font-family="sans-serif" font-size="10" fill="#334155" text-anchor="middle">Discards Dead Holes</text>

          <line x1="490" y1="115" x2="550" y2="115" stroke="#34d399" stroke-width="2"/>
          <polygon points="550,115 542,110 542,120" fill="#34d399"/>
          <text x="520" y="105" font-family="sans-serif" font-size="9" fill="#059669" text-anchor="middle">Compacts &amp; Writes</text>

          <rect x="550" y="60" width="200" height="110" fill="#ecfdf5" stroke="#34d399" rx="4"/>
          <text x="650" y="82" font-family="sans-serif" font-size="11" font-weight="bold" fill="#059669" text-anchor="middle">New Clean Segment</text>
          <rect x="575" y="100" width="70" height="40" fill="#0284c7" rx="2"/><text x="610" y="125" font-family="sans-serif" font-size="10" fill="#fff" text-anchor="middle">Live Block 1</text>
          <rect x="655" y="100" width="70" height="40" fill="#0284c7" rx="2"/><text x="690" y="125" font-family="sans-serif" font-size="10" fill="#fff" text-anchor="middle">Live Block 2</text>
        </svg>
        <figcaption>Figure 4.3.5C: Segment cleaning mechanism combining live blocks and freeing dead space.</figcaption>
      </figure>
    </div>

    <!-- Section 4.3.6: Journaling File Systems -->
    <div class="section-block">
      <h2>4.3.6 Journaling File Systems</h2>
      <p>
        System crashes mid-write often leave traditional filesystems in an inconsistent state, requiring lengthy full-volume integrity scans (such as <code>fsck</code>). <strong>Journaling File Systems</strong> introduce Write-Ahead Logging (WAL) to guarantee crash consistency.
      </p>
    </div>

    <!-- Section 4.3.7: Flash Storage & Wear-Leveling -->
    <div class="section-block">
      <h2>4.3.7 Flash Storage &amp; Wear-Leveling Systems</h2>
      <p>
        Solid-state drives built on NAND flash memory replace mechanical platters with electronic memory cells, requiring specialized FTL layers and wear-leveling algorithms.
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
    // --- Interactive LFS Simulator Engine ---
    const NUM_SEGMENTS = 4;
    const BLOCKS_PER_SEGMENT = 8;
    let lfsSegments = [];
    let currentWriteIndex = 0;

    function lfsResetSim() {
      lfsSegments = [];
      for (let s = 0; s < NUM_SEGMENTS; s++) {
        let segBlocks = [];
        for (let b = 0; b < BLOCKS_PER_SEGMENT; b++) {
          segBlocks.push({ type: 'free', fileId: null });
        }
        lfsSegments.push({ id: s, blocks: segBlocks });
      }
      currentWriteIndex = 0;
      lfsRenderSim();
      document.getElementById("lfsStatusMsg").textContent = "Simulator Reset. 4 Segments (32 total blocks) ready for sequential logging.";
    }

    function lfsWriteNewFile() {
      if (currentWriteIndex >= NUM_SEGMENTS * BLOCKS_PER_SEGMENT) {
        document.getElementById("lfsStatusMsg").textContent = "Log is full! Run the Segment Cleaner (GC) to reclaim dead space.";
        return;
      }
      let segIdx = Math.floor(currentWriteIndex / BLOCKS_PER_SEGMENT);
      let blkIdx = currentWriteIndex % BLOCKS_PER_SEGMENT;
      let fileId = `F${Math.floor(Math.random() * 90) + 10}`;
      lfsSegments[segIdx].blocks[blkIdx] = { type: 'live', fileId: fileId };
      currentWriteIndex++;
      lfsRenderSim();
      document.getElementById("lfsStatusMsg").textContent = `Appended new file (${fileId}) sequentially to Segment ${segIdx}, Block ${blkIdx}.`;
    }

    function lfsUpdateExistingFile() {
      let liveBlocks = [];
      lfsSegments.forEach((seg, sIdx) => {
        seg.blocks.forEach((blk, bIdx) => {
          if (blk.type === 'live') liveBlocks.push({ sIdx, bIdx, fileId: blk.fileId });
        });
      });
      if (liveBlocks.length === 0) {
        document.getElementById("lfsStatusMsg").textContent = "No live files to overwrite. Click 'Append New File' first.";
        return;
      }
      let target = liveBlocks[Math.floor(Math.random() * liveBlocks.length)];
      lfsSegments[target.sIdx].blocks[target.bIdx].type = 'dead';

      if (currentWriteIndex < NUM_SEGMENTS * BLOCKS_PER_SEGMENT) {
        let segIdx = Math.floor(currentWriteIndex / BLOCKS_PER_SEGMENT);
        let blkIdx = currentWriteIndex % BLOCKS_PER_SEGMENT;
        lfsSegments[segIdx].blocks[blkIdx] = { type: 'live', fileId: target.fileId };
        currentWriteIndex++;
        document.getElementById("lfsStatusMsg").textContent = `Overwrote file ${target.fileId}: old block marked 'dead', new version appended at log tail.`;
      } else {
        document.getElementById("lfsStatusMsg").textContent = `Overwrote file ${target.fileId} (old block dead), but log tail is full! Run Garbage Collection.`;
      }
      lfsRenderSim();
    }

    function lfsTriggerCleaner() {
      let liveBlocks = [];
      lfsSegments.forEach(seg => {
        seg.blocks.forEach(blk => {
          if (blk.type === 'live') liveBlocks.push(blk);
        });
      });
      lfsResetSim();
      liveBlocks.forEach(blk => {
        let segIdx = Math.floor(currentWriteIndex / BLOCKS_PER_SEGMENT);
        let blkIdx = currentWriteIndex % BLOCKS_PER_SEGMENT;
        if (segIdx < NUM_SEGMENTS) {
          lfsSegments[segIdx].blocks[blkIdx] = { type: 'live', fileId: blk.fileId };
          currentWriteIndex++;
        }
      });
      lfsRenderSim();
      document.getElementById("lfsStatusMsg").textContent = `Segment Cleaner (GC) executed! Compacted ${liveBlocks.length} live blocks and discarded all dead holes.`;
    }

    function lfsRenderSim() {
      const grid = document.getElementById("lfsSegmentsGrid");
      grid.innerHTML = "";
      let liveCount = 0;
      let deadCount = 0;
      let freeCount = 0;

      lfsSegments.forEach((seg, sIdx) => {
        let segDiv = document.createElement("div");
        segDiv.className = "lfs-segment-box";
        let activeTag = (Math.floor(currentWriteIndex / BLOCKS_PER_SEGMENT) === sIdx) ? ' (Tail)' : '';
        segDiv.innerHTML = `<div class="lfs-seg-header"><span>Segment ${sIdx}${activeTag}</span></div>`;

        let blocksDiv = document.createElement("div");
        blocksDiv.className = "lfs-seg-blocks";

        seg.blocks.forEach((blk, bIdx) => {
          let bEl = document.createElement("div");
          bEl.className = "lfs-block";
          if (blk.type === 'free') {
            bEl.classList.add("blk-free");
            bEl.textContent = "·";
            freeCount++;
          } else if (blk.type === 'live') {
            bEl.classList.add("blk-live");
            bEl.textContent = blk.fileId;
            liveCount++;
          } else if (blk.type === 'dead') {
            bEl.classList.add("blk-dead");
            bEl.textContent = blk.fileId;
            deadCount++;
          }
          blocksDiv.appendChild(bEl);
        });
        segDiv.appendChild(blocksDiv);
        grid.appendChild(segDiv);
      });

      document.getElementById("lfsMetricMsg").textContent = `Live Blocks: ${liveCount} | Dead Blocks: ${deadCount} | Free Blocks: ${freeCount}`;
      let activeSeg = Math.min(Math.floor(currentWriteIndex / BLOCKS_PER_SEGMENT), NUM_SEGMENTS - 1);
      document.getElementById("lfsActiveSegLabel").textContent = `Active Log Tail: Segment ${activeSeg}`;
    }

    lfsResetSim();

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

    print(f"--> Updating photo credits to Stanford in {html_file}...")
    os.makedirs(os.path.dirname(html_file), exist_ok=True)
    final_content = HTML_CONTENT.replace("AUDIO_DATA_URI_PLACEHOLDER", data_uri)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(final_content)
    print("--> HTML structure successfully written!")

    commit_msg = (
        "Simplify pioneer photo credits to Stanford in LFS infobox\n\n"
        "Update week10-file-management/03-filesystem-implementation.html so that the "
        "photo credit labels for both John K. Ousterhout and Mendel Rosenblum read "
        "simply as Stanford."
    )

    execute_git_command(["git", "add", html_file], "Staging HTML file")
    execute_git_command(["git", "commit", "-am", commit_msg], "Committing changes")
    execute_git_command(["git", "push", "origin", "main"], "Pushing changes to origin")
    print("--> Deployment complete!")

if __name__ == "__main__":
    execute_deployment()
