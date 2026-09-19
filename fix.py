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

    /* STREAMLINED LFS & JOURNALING WALKTHROUGH WIDGETS */
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
    .blk-candidate { outline: 2px solid #ef4444; }
    .blk-identified-live { background: #059669 !important; color: #fff; outline: 2px solid #34d399; }
    .blk-discarded { opacity: 0.25; text-decoration: line-through; }

    /* Journaling Interactive Block States */
    .blk-journal-head { background: #9333ea; color: #fff; }
    .blk-journal-tx { background: #3b82f6; color: #fff; }
    .blk-journal-commit { background: #059669; color: #fff; font-weight: 900; }
    .blk-journal-corrupt { background: #dc2626; color: #fff; text-decoration: line-through; }
    .blk-fs-checkpointed { background: #10b981; color: #fff; }

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

      <!-- STREAMLINED LFS INTERACTIVE WALKTHROUGH 1 -->
      <div class="lfs-sim-container" id="lfsSimulator">
        <div class="lfs-topbar">
          <span class="lfs-title">Walkthrough Part 1: Sequential Appends &amp; Dead Space Accumulation</span>
          <span class="lfs-step-indicator" id="lfsStepTag">Step 1 of 3: Ready</span>
        </div>

        <div class="lfs-explanation-box" id="lfsExplanationBox">
          <strong>Welcome to the LFS Walkthrough!</strong> LFS converts all file system writes into a fast, contiguous sequential stream. Click <strong>'1. Append New File'</strong> to stream files into the log tail.
        </div>

        <div class="lfs-controls">
          <button class="lfs-btn primary" onclick="lfsStepAppend()">1. Append New File</button>
          <button class="lfs-btn" onclick="lfsStepOverwrite()">2. Overwrite / Create Dead Space</button>
          <button class="lfs-btn primary" onclick="lfsStepClean()">3. Run Segment Cleaner (GC)</button>
          <button class="lfs-btn" onclick="lfsResetSim()" style="margin-left: auto;">Reset Walkthrough</button>
        </div>

        <div class="lfs-segments-grid" id="lfsSegmentsGrid"></div>

        <div class="lfs-status-panel">
          <span id="lfsStatusMsg">Ready to begin LFS demonstration.</span>
          <span id="lfsMetricMsg">Live Blocks: 0 | Dead Blocks: 0 | Free Blocks: 32</span>
        </div>
      </div>

      <!-- Deepened Inode Map & Log Tail Section -->
      <h3>2. The Inode Map (Imap) Architecture &amp; Indirection</h3>
      <p>
        In traditional file systems, every file possesses an unchanging identity tied to a static location: <strong>inode number $N$ resides at a mathematically fixed disk offset</strong> within the partition's inode table. An application reading a file simply computes this static address directly.
      </p>
      <p>
        In an append-only architecture like LFS, however, <strong>a static inode table is impossible</strong>. Whenever an existing file is updated, writing modified data blocks also requires updating its metadata (such as timestamps, file length, and block pointers). Because LFS forbids in-place updates, the updated inode cannot overwrite its original location; instead, it is appended to the current tail of the log. As files are repeatedly modified, their inodes continually relocate across different segments on disk. Without an indirection mechanism, locating a file's latest inode would demand an exhaustive, sequential scan of the entire disk volume.
      </p>
      <p>
        To solve this, Rosenblum and Ousterhout created the <strong>Inode Map (Imap)</strong>. The imap is a table that decouples a file's persistent identifier (its inode number) from its physical location, maintaining the current on-disk block address for every active inode in the file system.
      </p>

      <h4>The Sequential Log Tail (Active Write Frontier)</h4>
      <p>
        The <strong>log tail</strong> is the dynamic write-pointer frontier of the storage volume where all newly generated data enters the media:
      </p>
      <ul>
        <li><strong>Continuous Memory Buffering:</strong> File system operations do not immediately trigger physical writes. Instead, file data blocks, updated directory entries, newly positioned inodes, and even updated chunks of the imap are collected in large main-memory segment buffers (typically 512 KB to 1 MB).</li>
        <li><strong>High-Speed Streaming:</strong> When the in-memory segment buffer fills, it is flushed to disk in one large, continuous write operation at the <strong>log tail</strong>. By advancing the write frontier sequentially across the disk platter, head seeks and rotational delays are completely eliminated during write operations.</li>
        <li><strong>Logging the Imap Itself:</strong> Because the imap updates every time an inode moves, the imap itself is divided into small chunks and written to the log tail alongside the file data and inodes it describes. The fixed <strong>Checkpoint Region</strong> at the beginning of the volume periodically stores pointers to the latest imap chunks, completing the lookup chain.</li>
      </ul>

      <!-- Enhanced Diagram 2: Imap Architecture & Log Tail Frontier -->
      <figure class="diagram-figure">
        <svg class="diagram-svg" viewBox="0 0 800 240" xmlns="http://www.w3.org/2000/svg">
          <rect width="800" height="240" fill="#ffffff" rx="6" stroke="#cbd5e1"/>
          <text x="400" y="26" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Figure 4.3.5B: Dynamic Inode Map (Imap) Resolution to the Sequential Log Tail</text>

          <rect x="30" y="90" width="110" height="65" fill="#e0f2fe" stroke="#0284c7" rx="4"/>
          <text x="85" y="115" font-family="sans-serif" font-size="11" font-weight="bold" fill="#0369a1" text-anchor="middle">File Inode #</text>
          <text x="85" y="136" font-family="sans-serif" font-size="13" font-weight="bold" fill="#0f172a" text-anchor="middle">Inode 42</text>

          <line x1="140" y1="122" x2="200" y2="122" stroke="#0284c7" stroke-width="2"/>
          <polygon points="200,122 192,117 192,127" fill="#0284c7"/>
          <text x="170" y="112" font-family="sans-serif" font-size="9" fill="#0284c7" text-anchor="middle">Index</text>

          <rect x="200" y="60" width="170" height="135" fill="#f8fafc" stroke="#64748b" rx="4"/>
          <text x="285" y="82" font-family="sans-serif" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">Inode Map (Imap Chunk)</text>
          <line x1="210" y1="92" x2="360" y2="92" stroke="#cbd5e1" stroke-width="1"/>
          <text x="285" y="110" font-family="sans-serif" font-size="10" fill="#64748b" text-anchor="middle">Inode 0 &rarr; Sector 1024</text>
          <rect x="210" y="122" width="150" height="22" fill="#e0f2fe" rx="2"/>
          <text x="285" y="137" font-weight="bold" font-size="10" fill="#0284c7" text-anchor="middle">Inode 42 &rarr; Block 8420</text>
          <text x="285" y="162" font-family="sans-serif" font-size="10" fill="#64748b" text-anchor="middle">Inode 43 &rarr; Sector 3120</text>
          <text x="285" y="182" font-family="sans-serif" font-size="9" font-style="italic" fill="#94a3b8" text-anchor="middle">(Decouples static ID from offset)</text>

          <line x1="370" y1="133" x2="430" y2="133" stroke="#0284c7" stroke-width="2"/>
          <polygon points="430,133 422,128 422,138" fill="#0284c7"/>
          <text x="400" y="123" font-family="sans-serif" font-size="9" fill="#0284c7" text-anchor="middle">Locates</text>

          <rect x="430" y="60" width="340" height="135" fill="#0f172a" stroke="#334155" rx="4"/>
          <text x="600" y="84" font-family="sans-serif" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">Active Log Tail (Append Frontier)</text>

          <rect x="445" y="102" width="85" height="50" fill="#0284c7" rx="3"/>
          <text x="487.5" y="124" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">Block 8420</text>
          <text x="487.5" y="140" font-family="sans-serif" font-size="9" fill="#e0f2fe" text-anchor="middle">Inode 42</text>

          <rect x="535" y="102" width="85" height="50" fill="#0284c7" rx="3"/>
          <text x="577.5" y="124" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">Block 8421</text>
          <text x="577.5" y="140" font-family="sans-serif" font-size="9" fill="#e0f2fe" text-anchor="middle">File Data Bytes</text>

          <rect x="625" y="102" width="95" height="50" fill="#059669" rx="3"/>
          <text x="672.5" y="124" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">Block 8422</text>
          <text x="672.5" y="140" font-family="sans-serif" font-size="9" fill="#d1fae5" text-anchor="middle">Updated Imap</text>

          <line x1="725" y1="127" x2="755" y2="127" stroke="#38bdf8" stroke-width="2" stroke-dasharray="3,3"/>
          <polygon points="758,127 750,122 750,132" fill="#38bdf8"/>
          <text x="600" y="178" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">&rarr; Writes stream contiguously; Frontier advances forward &rarr;</text>
        </svg>
        <figcaption>Figure 4.3.5B: The Inode Map decoupling persistent file numbers from dynamic log tail write offsets.</figcaption>
      </figure>

      <!-- Section 3: Checkpoints & Crash Recovery -->
      <h3>3. Checkpoint Regions &amp; Rapid Crash Recovery</h3>
      <p>
        The introduction of the Inode Map introduces an architectural dilemma: <em>if inodes move because files are appended to the log, and chunks of the imap move because inodes are appended to the log, how does the operating system locate the imap itself when mounting the disk?</em>
      </p>
      <p>
        Without a fixed anchoring point, the file system would suffer infinite recursive indirection. LFS breaks this cycle by reserving fixed physical disk locations known as <strong>Checkpoint Regions (CR)</strong>.
      </p>

      <h4>The Anatomy of a Checkpoint Region</h4>
      <p>
        A Checkpoint Region is written periodically (typically every 30 seconds, or during a clean system unmount). It contains:
      </p>
      <ul>
        <li><strong>Array of Imap Block Addresses:</strong> Pointers to all current, valid chunks of the inode map scattered across the log.</li>
        <li><strong>Segment Usage Table Pointers:</strong> The locations of blocks tracking the number of live bytes and modification timestamps of every segment on disk (used by the segment cleaner).</li>
        <li><strong>Active Log Tail Pointer:</strong> The exact segment and block offset where new appends were occurring when the checkpoint was taken.</li>
        <li><strong>Monotonic Timestamp &amp; Checksum:</strong> Verification records ensuring that the checkpoint region was completely and safely flushed to physical disk.</li>
      </ul>

      <h4>Dual Alternating Checkpoint Regions (Crash Consistency)</h4>
      <p>
        Writing to a fixed location creates an immediate crash vulnerability: if power fails midway through updating the Checkpoint Region, the partially written CR will be corrupt, rendering the entire file system unreadable.
      </p>
      <p>
        To guarantee atomicity, LFS allocates <strong>two identical Checkpoint Regions (CR A and CR B)</strong> at known, fixed disk offsets (typically at the absolute start and end of the partition). LFS alternates writes between them:
      </p>
      <ol>
        <li>At interval $T_1$, LFS flushes dirty buffers to the log tail, writes the latest imap chunks, and writes CR A with timestamp $T_1$.</li>
        <li>At interval $T_2$, LFS repeats this sequence but writes exclusively to CR B with timestamp $T_2$.</li>
        <li>During boot recovery, LFS inspects both CR A and CR B, computes their checksums, and mounts whichever region is intact and possesses the most recent valid timestamp. If a crash interrupted writing to CR B, LFS safely discards it and falls back to CR A.</li>
      </ol>

      <!-- Diagram: Dual Alternating Checkpoints -->
      <figure class="diagram-figure">
        <svg class="diagram-svg" viewBox="0 0 800 230" xmlns="http://www.w3.org/2000/svg">
          <rect width="800" height="230" fill="#ffffff" rx="6" stroke="#cbd5e1"/>
          <text x="400" y="26" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Figure 4.3.5C: Dual Alternating Checkpoints for Atomic Consistency</text>

          <rect x="50" y="60" width="220" height="130" fill="#ecfdf5" stroke="#10b981" rx="4"/>
          <text x="160" y="82" font-family="sans-serif" font-size="12" font-weight="bold" fill="#047857" text-anchor="middle">Checkpoint Region A (Block 0)</text>
          <line x1="60" y1="92" x2="260" y2="92" stroke="#a7f3d0" stroke-width="1"/>
          <text x="160" y="112" font-family="sans-serif" font-size="10" fill="#065f46" text-anchor="middle">Timestamp: 10:45:00 (Valid)</text>
          <text x="160" y="132" font-family="sans-serif" font-size="10" fill="#065f46" text-anchor="middle">Imap Chunk Pointers: [P1, P2, ...]</text>
          <text x="160" y="152" font-family="sans-serif" font-size="10" fill="#065f46" text-anchor="middle">CRC Checksum: OK &check;</text>
          <text x="160" y="174" font-family="sans-serif" font-size="11" font-weight="bold" fill="#047857" text-anchor="middle">&larr; Selected on Boot &larr;</text>

          <rect x="310" y="95" width="180" height="60" fill="#f8fafc" stroke="#94a3b8" stroke-dasharray="3,3" rx="4"/>
          <text x="400" y="122" font-family="sans-serif" font-size="11" font-weight="bold" fill="#475569" text-anchor="middle">Segments &amp; Log Stream</text>
          <text x="400" y="140" font-family="sans-serif" font-size="9" fill="#64748b" text-anchor="middle">(Continuous Sequential Appends)</text>

          <rect x="530" y="60" width="220" height="130" fill="#fef2f2" stroke="#ef4444" rx="4"/>
          <text x="640" y="82" font-family="sans-serif" font-size="12" font-weight="bold" fill="#b91c1c" text-anchor="middle">Checkpoint Region B (Block 1)</text>
          <line x1="540" y1="92" x2="740" y2="92" stroke="#fecaca" stroke-width="1"/>
          <text x="640" y="112" font-family="sans-serif" font-size="10" fill="#991b1b" text-anchor="middle">Timestamp: 10:45:30 (Interrupted)</text>
          <text x="640" y="132" font-family="sans-serif" font-size="10" fill="#991b1b" text-anchor="middle">Imap Chunk Pointers: [Truncated]</text>
          <text x="640" y="152" font-family="sans-serif" font-size="10" fill="#dc2626" font-weight="bold" text-anchor="middle">CRC Checksum: MISMATCH &cross;</text>
          <text x="640" y="174" font-family="sans-serif" font-size="11" font-weight="bold" fill="#dc2626" text-anchor="middle">&cross; Safely Discarded &cross;</text>
        </svg>
        <figcaption>Figure 4.3.5C: Alternating checkpoints guarantee crash resilience even if power fails mid-write.</figcaption>
      </figure>

      <h4>Roll-Forward Recovery via Segment Summary Blocks</h4>
      <p>
        If LFS only recovered data referenced by the most recent checkpoint, all operations committed in the 30-second window between the last checkpoint and the sudden power cut would be lost. LFS overcomes this limitation with <strong>roll-forward recovery</strong>:
      </p>
      <ul>
        <li><strong>Segment Summary Blocks:</strong> Every segment written at the log tail includes a compact summary block at its end. This summary explicitly lists the inode number and logical file offset for every single data block residing in that segment.</li>
        <li><strong>Scanning from Checkpoint to Tail:</strong> During boot, after mounting the latest valid Checkpoint Region, LFS identifies the segment where the checkpoint concluded and scans forward through subsequent segments until it encounters unwritten media.</li>
        <li><strong>Rebuilding Recent Inodes:</strong> By reading the Segment Summary Blocks of these recent segments, LFS detects files written after the checkpoint, reconstructs their inodes in memory, updates the imap entries, and establishes a newly verified log tail frontier.</li>
      </ul>
      <p>
        Because LFS only scans the small tail of the log written since the last checkpoint (usually just a few megabytes), recovery completes in milliseconds, avoiding the hours-long volume scans typical of traditional <code>fsck</code> utilities.
      </p>

      <!-- Diagram: Roll-Forward Mechanism -->
      <figure class="diagram-figure">
        <svg class="diagram-svg" viewBox="0 0 800 210" xmlns="http://www.w3.org/2000/svg">
          <rect width="800" height="210" fill="#ffffff" rx="6" stroke="#cbd5e1"/>
          <text x="400" y="26" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Figure 4.3.5D: Roll-Forward Recovery from Checkpoint to Crash Frontier</text>

          <rect x="40" y="70" width="130" height="90" fill="#ecfdf5" stroke="#10b981" rx="4"/>
          <text x="105" y="98" font-family="sans-serif" font-size="11" font-weight="bold" fill="#047857" text-anchor="middle">Last Valid CR</text>
          <text x="105" y="118" font-family="sans-serif" font-size="10" fill="#065f46" text-anchor="middle">Timestamp: $T_{CR}$</text>
          <text x="105" y="138" font-family="sans-serif" font-size="9" fill="#047857" text-anchor="middle">&check; Consistent State</text>

          <path d="M 170 115 L 260 115" stroke="#0284c7" stroke-width="3" stroke-dasharray="4,4"/>
          <polygon points="260,115 250,109 250,121" fill="#0284c7"/>
          <text x="215" y="105" font-family="sans-serif" font-size="10" font-weight="bold" fill="#0284c7" text-anchor="middle">Roll Forward</text>

          <rect x="260" y="65" width="220" height="100" fill="#f0f9ff" stroke="#0284c7" rx="4"/>
          <text x="370" y="86" font-family="sans-serif" font-size="11" font-weight="bold" fill="#0369a1" text-anchor="middle">Segment Written After Checkpoint</text>
          <rect x="275" y="98" width="50" height="35" fill="#0284c7" rx="2"/><text x="300" y="120" font-family="sans-serif" font-size="9" fill="#fff" text-anchor="middle">Data F7</text>
          <rect x="335" y="98" width="50" height="35" fill="#0284c7" rx="2"/><text x="360" y="120" font-family="sans-serif" font-size="9" fill="#fff" text-anchor="middle">Inode 7</text>
          <rect x="395" y="98" width="70" height="35" fill="#f59e0b" rx="2"/><text x="430" y="120" font-family="sans-serif" font-size="9" font-weight="bold" fill="#fff" text-anchor="middle">Summary Blk</text>
          <text x="370" y="152" font-family="sans-serif" font-size="9" fill="#0369a1" text-anchor="middle">Summary identifies new inode &amp; updates Imap</text>

          <line x1="510" y1="50" x2="510" y2="180" stroke="#ef4444" stroke-width="2" stroke-dasharray="5,5"/>
          <text x="510" y="198" font-family="sans-serif" font-size="10" font-weight="bold" fill="#dc2626" text-anchor="middle">&cross; Sudden Power Cut &cross;</text>

          <rect x="540" y="65" width="220" height="100" fill="#f8fafc" stroke="#cbd5e1" stroke-dasharray="3,3" rx="4"/>
          <text x="650" y="110" font-family="sans-serif" font-size="11" fill="#94a3b8" text-anchor="middle">Unwritten / Clean Segments</text>
          <text x="650" y="128" font-family="sans-serif" font-size="9" fill="#94a3b8" text-anchor="middle">(Becomes new active log tail frontier)</text>
        </svg>
        <figcaption>Figure 4.3.5D: Fast roll-forward scan parsing segment summaries to recover blocks committed after checkpoint.</figcaption>
      </figure>

      <!-- MASSIVELY EXPANDED SECTION 4: SEGMENT CLEANING & GARBAGE COLLECTION -->
      <h3>4. Background Garbage Collection &amp; Segment Cleaning</h3>
      <p>
        While append-only logging achieves optimal sequential write performance, it creates a fundamental storage management challenge: <strong>free space fragmentation</strong>.
      </p>
      <p>
        Because LFS never overwrites existing blocks in place, modifying a file writes new data to the log tail, leaving previous versions of those data blocks and their old inodes orphaned in older segments. Over time, segments become riddled with obsolete &ldquo;holes&rdquo; (dead space). If the disk simply wrapped around in a circular fashion without intervention, the log tail would soon collide with older segments containing a mixture of live data and dead holes, forcing writes to fragment into tiny random slivers and destroying LFS's throughput advantage.
      </p>

      <h4>Determining Block Liveness via Segment Summaries</h4>
      <p>
        To reclaim contiguous free space, LFS runs a background cleaning daemon. The cleaner reads several partially filled candidate segments, identifies which blocks are still <strong>live</strong> (currently referenced by an active file), compacts those live blocks together, and writes them out into a fresh, contiguous clean segment at the log tail. The original segments are then marked completely free and recycled.
      </p>
      <p>
        A central efficiency question is: <em>How does the cleaner determine whether a specific block in an old segment is live or dead without performing a full volume scan?</em>
      </p>
      <p>
        The cleaner uses the <strong>Segment Summary Block</strong> located at the end of each segment. The summary record stores a tuple <code>(inode_number, block_offset)</code> for every block in the segment. The cleaner verifies liveness in three constant-time steps:
      </p>
      <ol>
        <li>Read block $B$'s metadata tuple from the Segment Summary: <code>(Inode 14, Offset 0)</code>.</li>
        <li>Consult the Inode Map (Imap) to find the current on-disk location of Inode 14.</li>
        <li>Read Inode 14 and inspect its block pointer for Offset 0. If that pointer matches block $B$'s address, <strong>the block is live</strong> and must be preserved. If the pointer points to a newer block at the log tail (or if Inode 14 was deleted), <strong>block $B$ is dead</strong> and can be discarded immediately.</li>
      </ol>

      <!-- Diagram: Block Liveness Verification Pipeline -->
      <figure class="diagram-figure">
        <svg class="diagram-svg" viewBox="0 0 800 230" xmlns="http://www.w3.org/2000/svg">
          <rect width="800" height="230" fill="#ffffff" rx="6" stroke="#cbd5e1"/>
          <text x="400" y="26" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Figure 4.3.5E: Three-Step Block Liveness Verification Pipeline</text>

          <rect x="40" y="60" width="200" height="135" fill="#f8fafc" stroke="#94a3b8" rx="4"/>
          <text x="140" y="82" font-family="sans-serif" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">1. Segment Summary Block</text>
          <line x1="50" y1="92" x2="230" y2="92" stroke="#cbd5e1" stroke-width="1"/>
          <text x="140" y="112" font-family="sans-serif" font-size="10" fill="#475569" text-anchor="middle">Candidate Block: #4096</text>
          <rect x="55" y="122" width="170" height="26" fill="#e0f2fe" rx="3"/>
          <text x="140" y="139" font-family="sans-serif" font-size="10" font-weight="bold" fill="#0284c7" text-anchor="middle">Summary: (Inode 14, Off 0)</text>
          <text x="140" y="172" font-family="sans-serif" font-size="9" fill="#64748b" text-anchor="middle">Identifies block ownership</text>

          <line x1="240" y1="125" x2="295" y2="125" stroke="#0284c7" stroke-width="2"/>
          <polygon points="295,125 287,120 287,130" fill="#0284c7"/>
          <text x="268" y="115" font-family="sans-serif" font-size="9" fill="#0284c7" text-anchor="middle">Query</text>

          <rect x="295" y="60" width="195" height="135" fill="#f0f9ff" stroke="#0284c7" rx="4"/>
          <text x="392" y="82" font-family="sans-serif" font-size="11" font-weight="bold" fill="#0369a1" text-anchor="middle">2. Consult Inode Map</text>
          <line x1="305" y1="92" x2="480" y2="92" stroke="#bae6fd" stroke-width="1"/>
          <text x="392" y="112" font-family="sans-serif" font-size="10" fill="#0369a1" text-anchor="middle">Query Inode 14 address</text>
          <rect x="310" y="122" width="165" height="26" fill="#ffffff" stroke="#38bdf8" rx="3"/>
          <text x="392" y="139" font-family="sans-serif" font-size="10" font-weight="bold" fill="#0f172a" text-anchor="middle">Imap[14] &rarr; Block #8100</text>
          <text x="392" y="172" font-family="sans-serif" font-size="9" fill="#64748b" text-anchor="middle">Locates latest inode copy</text>

          <line x1="490" y1="125" x2="545" y2="125" stroke="#0284c7" stroke-width="2"/>
          <polygon points="545,125 537,120 537,130" fill="#0284c7"/>
          <text x="518" y="115" font-family="sans-serif" font-size="9" fill="#0284c7" text-anchor="middle">Compare</text>

          <rect x="545" y="60" width="215" height="135" fill="#ecfdf5" stroke="#10b981" rx="4"/>
          <text x="652" y="82" font-family="sans-serif" font-size="11" font-weight="bold" fill="#047857" text-anchor="middle">3. Check Inode Offset 0</text>
          <line x1="555" y1="92" x2="750" y2="92" stroke="#a7f3d0" stroke-width="1"/>
          <text x="652" y="112" font-family="sans-serif" font-size="10" fill="#065f46" text-anchor="middle">Does Inode.ptr[0] == #4096?</text>
          <text x="652" y="136" font-family="sans-serif" font-size="10" font-weight="bold" fill="#047857" text-anchor="middle">&check; YES: Keep block (Live)</text>
          <text x="652" y="154" font-family="sans-serif" font-size="10" font-weight="bold" fill="#dc2626" text-anchor="middle">&cross; NO: Discard hole (Dead)</text>
          <text x="652" y="178" font-family="sans-serif" font-size="9" fill="#065f46" text-anchor="middle">Constant time $O(1)$ decision</text>
        </svg>
        <figcaption>Figure 4.3.5E: The three-step constant time liveness check comparing segment summary entries against current inode pointers.</figcaption>
      </figure>

      <h4>The Cost-Benefit Policy: Managing Hot vs. Cold Data</h4>
      <p>
        Segment cleaning is not free. Moving live data incurs <strong>write amplification</strong>: reading live blocks off disk, copying them through memory, and rewriting them at the log tail consumes I/O bandwidth that could otherwise serve user applications.
      </p>
      <p>
        A naive policy would be to clean whichever segment has the highest proportion of dead space (the lowest utilization $u$, where $u$ is the fraction of live bytes in the segment). However, Rosenblum and Ousterhout discovered that this simple greedy policy performs poorly because it ignores data temperature:
      </p>
      <ul>
        <li><strong>Hot Data:</strong> Files that are overwritten or appended to frequently (such as log files or database temporary tables). Dead space accumulates rapidly in hot segments. If a hot segment is cleaned early while its utilization is moderate, the cleaner will expend effort copying live blocks that are destined to become dead shortly thereafter.</li>
        <li><strong>Cold Data:</strong> Files that are written once and rarely modified (such as system binaries, code libraries, or archived media). If a cold segment reaches 75% dead space, the remaining 25% of live data will likely remain valid for months. Cleaning this segment frees 75% contiguous space permanently without risking repeated re-cleaning.</li>
      </ul>
      <p>
        To balance these dynamics, Rosenblum and Ousterhout formulated the <strong>Cost-Benefit Cleaning Policy</strong>:
      </p>
      $$\frac{\text{Benefit}}{\text{Cost}} = \frac{\text{Free Space Reclaimed} \times \text{Age}}{\text{Cost of Cleaning}} = \frac{(1 - u) \times \text{Age}}{1 + u}$$
      <p>
        Where:
      </p>
      <ul>
        <li>$u$ is the segment utilization ($0 \le u \le 1$), representing the fraction of blocks that are still live.</li>
        <li>$(1 - u)$ represents the amount of contiguous free space reclaimed by cleaning the segment.</li>
        <li>$\text{Age}$ is the elapsed time since the newest block in the segment was written. An older segment indicates stable, cold data that is unlikely to generate new dead space on its own.</li>
        <li>$(1 + u)$ reflects the physical I/O cost: reading the full segment (cost of $1$) plus rewriting the surviving live fraction (cost of $u$).</li>
      </ul>

      <!-- Diagram: Cost-Benefit Hot vs Cold Cleaning -->
      <figure class="diagram-figure">
        <svg class="diagram-svg" viewBox="0 0 800 240" xmlns="http://www.w3.org/2000/svg">
          <rect width="800" height="240" fill="#ffffff" rx="6" stroke="#cbd5e1"/>
          <text x="400" y="26" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Figure 4.3.5F: Cost-Benefit Cleaning Dynamics (Hot vs. Cold Data Segments)</text>

          <rect x="40" y="55" width="340" height="155" fill="#fef2f2" stroke="#f87171" rx="4"/>
          <text x="210" y="78" font-family="sans-serif" font-size="12" font-weight="bold" fill="#b91c1c" text-anchor="middle">Hot Segment (Frequent Modifications)</text>
          <line x1="50" y1="88" x2="370" y2="88" stroke="#fecaca" stroke-width="1"/>
          <text x="210" y="106" font-family="sans-serif" font-size="10" fill="#7f1d1d" text-anchor="middle">Utilization: $u = 0.40$ (40% Live, 60% Dead)</text>
          <text x="210" y="124" font-family="sans-serif" font-size="10" fill="#7f1d1d" text-anchor="middle">Age: Low (Recent writes)</text>
          <rect x="55" y="136" width="310" height="28" fill="#ffffff" stroke="#ef4444" rx="3"/>
          <text x="210" y="154" font-family="sans-serif" font-size="10" font-weight="bold" fill="#dc2626" text-anchor="middle">Decision: DELAY CLEANING</text>
          <text x="210" y="190" font-family="sans-serif" font-size="9" fill="#991b1b" text-anchor="middle">Waiting allows active churn to naturally kill remaining live blocks</text>

          <rect x="420" y="55" width="340" height="155" fill="#f0fdf4" stroke="#4ade80" rx="4"/>
          <text x="590" y="78" font-family="sans-serif" font-size="12" font-weight="bold" fill="#15803d" text-anchor="middle">Cold Segment (Stable, Read-Only Data)</text>
          <line x1="430" y1="88" x2="750" y2="88" stroke="#bbf7d0" stroke-width="1"/>
          <text x="590" y="106" font-family="sans-serif" font-size="10" fill="#14532d" text-anchor="middle">Utilization: $u = 0.60$ (60% Live, 40% Dead)</text>
          <text x="590" y="124" font-family="sans-serif" font-size="10" fill="#14532d" text-anchor="middle">Age: Very High (Unchanged for hours/days)</text>
          <rect x="435" y="136" width="310" height="28" fill="#ffffff" stroke="#22c55e" rx="3"/>
          <text x="590" y="154" font-family="sans-serif" font-size="10" font-weight="bold" fill="#16a34a" text-anchor="middle">Decision: CLEAN &amp; COMPACT</text>
          <text x="590" y="190" font-family="sans-serif" font-size="9" fill="#166534" text-anchor="middle">Compacting cold data isolates stable blocks into dedicated segments</text>
        </svg>
        <figcaption>Figure 4.3.5F: The cost-benefit cleaning policy delays cleaning hot segments to avoid write amplification while proactively compacting cold segments.</figcaption>
      </figure>

      <h4>The Complete Four-Phase Compaction Cycle</h4>
      <p>
        The complete cleaning sequence executes in four discrete, coordinated phases:
      </p>
      <ol>
        <li><strong>Selection:</strong> The cleaner evaluates on-disk segment usage tables, computes cost-benefit metrics across candidates, and selects a batch of segments $S_1, S_2, \ldots, S_k$.</li>
        <li><strong>Identification:</strong> For each selected segment, the cleaner reads the Segment Summary block and verifies block liveness via the Inode Map.</li>
        <li><strong>Compaction &amp; Append:</strong> All identified live blocks are bundled into a contiguous in-memory buffer and appended to the <strong>log tail</strong> as part of a new clean segment. Because the live blocks now reside at new physical addresses, their corresponding inodes and imap entries are updated and committed to the log tail as well.</li>
        <li><strong>Reclamation:</strong> The original segments $S_1, S_2, \ldots, S_k$ are marked as free in the Segment Usage Table and added to the pool of available clean segments for future log tail streaming.</li>
      </ol>

      <!-- WALKTHROUGH PART 2: THE 4-PHASE COMPACTION CYCLE -->
      <div class="lfs-sim-container" id="fourPhaseCompactionSim">
        <div class="lfs-topbar">
          <span class="lfs-title">Walkthrough Part 2: The 4-Phase Compaction Cycle</span>
          <span class="lfs-step-indicator" id="fourPhaseStepTag">Phase 0: Ready</span>
        </div>

        <div class="lfs-explanation-box" id="fourPhaseExplanationBox">
          <strong>Interactive 4-Phase Compaction:</strong> Observe how LFS reclaims fragmented space without taking the file system offline. Click <strong>"1. Phase 1: Selection"</strong> to begin!
        </div>

        <div class="lfs-controls">
          <button class="lfs-btn primary" id="btnPhase1" onclick="compactionPhase1Selection()">1. Phase 1: Selection</button>
          <button class="lfs-btn" id="btnPhase2" onclick="compactionPhase2Identification()">2. Phase 2: Identification</button>
          <button class="lfs-btn" id="btnPhase3" onclick="compactionPhase3Compaction()">3. Phase 3: Compaction &amp; Append</button>
          <button class="lfs-btn accent" id="btnPhase4" onclick="compactionPhase4Reclamation()">4. Phase 4: Reclamation</button>
          <button class="lfs-btn" onclick="compactionResetWalkthrough()" style="margin-left: auto;">Reset Cycle</button>
        </div>

        <div class="lfs-segments-grid" id="fourPhaseSegmentsGrid"></div>

        <div class="lfs-status-panel">
          <span id="fourPhaseStatusMsg">Walkthrough ready. Segments 0 &amp; 1 are fragmented candidate segments.</span>
          <span id="fourPhaseMetricMsg">Selected: None | Live Migrated: 0 | Reclaimed Segments: 0</span>
        </div>
      </div>
    </div>

    <!-- Section 4.3.6: Journaling File Systems -->
    <div class="section-block">
      <h2>4.3.6 Journaling File Systems</h2>
      <p>
        System crashes mid-write often leave traditional filesystems in an inconsistent state, requiring lengthy full-volume integrity scans (such as <code>fsck</code>). <strong>Journaling File Systems</strong> introduce Write-Ahead Logging (WAL) to guarantee crash consistency.
      </p>

      <h3>1. The Crash Consistency Problem</h3>
      <p>
        Modifying a file in a standard filesystem requires multiple non-atomic disk operations. Consider appending data to an existing file:
      </p>
      <ol>
        <li><strong>Data Block Write:</strong> New file payload bytes must be written to a free data block on storage media.</li>
        <li><strong>Inode Metadata Update:</strong> The file's inode must be updated with the new file length, modification timestamp, and a direct/indirect pointer addressing the new block.</li>
        <li><strong>Block Bitmap Modification:</strong> The free block allocation bitmap must clear the bit for the allocated block to mark it as occupied.</li>
      </ol>
      <p>
        Because physical storage devices only guarantee atomic writes for single sectors (typically 512 or 4096 bytes), a sudden power failure or operating system panic occurring midway through these writes produces catastrophic corruption:
      </p>
      <ul>
        <li><strong>If only the data block is written:</strong> The data exists on disk, but neither the inode nor the bitmap references it. The block becomes an undetectable space leak until a complete filesystem scan runs.</li>
        <li><strong>If only the inode is updated:</strong> The inode points to a block that the bitmap still marks as free. A subsequent file creation may allocate that same block, leading to mutual block theft and corrupted data.</li>
        <li><strong>If only the bitmap is updated:</strong> A block is marked occupied, but no inode points to it, permanently wasting storage space.</li>
      </ul>
      <p>
        Historically, traditional Unix filesystems relied on the <code>fsck</code> (File System Consistency Check) utility upon reboot. <code>fsck</code> performs a multi-pass sweep across the entire storage partition: scanning every inode, rebuilding allocation bitmaps from scratch, cross-referencing link counts, and resolving orphaned blocks into <code>lost+found</code>. On multi-terabyte drives containing millions of files, an <code>fsck</code> scan can consume many hours, causing unacceptable downtime.
      </p>

      <!-- Diagram 4.3.6A: The Crash Consistency Window & WAL -->
      <figure class="diagram-figure">
        <svg class="diagram-svg" viewBox="0 0 800 240" xmlns="http://www.w3.org/2000/svg">
          <rect width="800" height="240" fill="#ffffff" rx="6" stroke="#cbd5e1"/>
          <text x="400" y="26" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Figure 4.3.6A: Crash Window Vulnerability vs. Write-Ahead Logging (WAL)</text>

          <!-- Vulnerable In-Place Writes -->
          <rect x="30" y="55" width="340" height="155" fill="#fef2f2" stroke="#f87171" rx="4"/>
          <text x="200" y="78" font-family="sans-serif" font-size="12" font-weight="bold" fill="#b91c1c" text-anchor="middle">Traditional Non-Atomic Writes</text>
          <line x1="40" y1="88" x2="360" y2="88" stroke="#fecaca" stroke-width="1"/>

          <rect x="50" y="100" width="80" height="35" fill="#0284c7" rx="2"/><text x="90" y="122" font-family="sans-serif" font-size="10" fill="#fff" text-anchor="middle">1. Data</text>
          <line x1="135" y1="117" x2="160" y2="117" stroke="#dc2626" stroke-width="2"/>
          <rect x="165" y="100" width="80" height="35" fill="#f59e0b" rx="2"/><text x="205" y="122" font-family="sans-serif" font-size="10" fill="#fff" text-anchor="middle">2. Inode</text>

          <!-- Crash Bolt -->
          <line x1="260" y1="92" x2="260" y2="145" stroke="#ef4444" stroke-width="3" stroke-dasharray="4,3"/>
          <text x="260" y="88" font-family="sans-serif" font-size="14" fill="#dc2626" text-anchor="middle">&#9889;</text>
          <text x="260" y="160" font-family="sans-serif" font-size="9" font-weight="bold" fill="#dc2626" text-anchor="middle">Crash Window</text>

          <rect x="275" y="100" width="80" height="35" fill="#94a3b8" rx="2" stroke="#dc2626" stroke-dasharray="2,2"/><text x="315" y="122" font-family="sans-serif" font-size="10" fill="#fff" text-anchor="middle">3. Bitmap</text>
          <text x="200" y="192" font-family="sans-serif" font-size="9" fill="#7f1d1d" text-anchor="middle">Partial write leaves bitmap desynchronized from inode!</text>

          <!-- WAL Journaling -->
          <rect x="410" y="55" width="360" height="155" fill="#f0fdf4" stroke="#4ade80" rx="4"/>
          <text x="590" y="78" font-family="sans-serif" font-size="12" font-weight="bold" fill="#15803d" text-anchor="middle">Write-Ahead Logging (WAL) Protocol</text>
          <line x1="420" y1="88" x2="760" y2="88" stroke="#bbf7d0" stroke-width="1"/>

          <rect x="430" y="100" width="70" height="35" fill="#3b82f6" rx="2"/><text x="465" y="122" font-family="sans-serif" font-size="9" fill="#fff" text-anchor="middle">Tx Header</text>
          <rect x="505" y="100" width="70" height="35" fill="#3b82f6" rx="2"/><text x="540" y="122" font-family="sans-serif" font-size="9" fill="#fff" text-anchor="middle">Metadata</text>
          <rect x="580" y="100" width="70" height="35" fill="#059669" rx="2"/><text x="615" y="122" font-family="sans-serif" font-size="9" font-weight="bold" fill="#fff" text-anchor="middle">Commit Blk</text>

          <line x1="655" y1="117" x2="680" y2="117" stroke="#16a34a" stroke-width="2"/>
          <polygon points="685,117 678,112 678,122" fill="#16a34a"/>

          <rect x="685" y="100" width="75" height="35" fill="#10b981" rx="2"/><text x="722" y="122" font-family="sans-serif" font-size="9" font-weight="bold" fill="#fff" text-anchor="middle">Checkpoint</text>
          <text x="590" y="160" font-family="sans-serif" font-size="9" fill="#14532d" text-anchor="middle">Atomic commit record precedes permanent in-place update</text>
          <text x="590" y="180" font-family="sans-serif" font-size="9" font-style="italic" fill="#166534" text-anchor="middle">Boot recovery replays commit or discards uncommitted partial write</text>
        </svg>
        <figcaption>Figure 4.3.6A: Write-Ahead Logging isolates multi-block updates behind an atomic commit boundary.</figcaption>
      </figure>

      <h3>2. Write-Ahead Logging &amp; The Transaction Lifecycle</h3>
      <p>
        Journaling file systems borrow the technique of <strong>Write-Ahead Logging (WAL)</strong> from relational database engines. The fundamental invariant of WAL states: <em>No modified metadata or data may overwrite its permanent disk location until the corresponding change description has been committed to a non-volatile log.</em>
      </p>
      <p>
        The dedicated log space is arranged as a circular ring buffer (either inside a reserved inode or on a separate partition). Changes execute across four strict stages:
      </p>
      <ol>
        <li><strong>Journal Write:</strong> The operating system bundles related updates into a transaction. A transaction descriptor header is emitted, followed by modified filesystem blocks (such as inodes, allocation bitmaps, or directory entries).</li>
        <li><strong>Journal Commit:</strong> Once all transaction records reach disk, an explicit <strong>commit block</strong> containing a sequence number and transaction checksum is written. The arrival of the commit block marks the <em>commit boundary</em>: the transaction is now formally committed and durable.</li>
        <li><strong>Checkpointing:</strong> With the transaction safely committed to the journal, the operating system writes the pending changes to their permanent in-place filesystem blocks across disk cylinders.</li>
        <li><strong>Journal Free:</strong> Once in-place checkpointing finishes, the circular journal marks that transaction's ring buffer space as free for reuse.</li>
      </ol>

      <!-- Diagram 4.3.6B: Circular Journal Ring Buffer & Lifecycle -->
      <figure class="diagram-figure">
        <svg class="diagram-svg" viewBox="0 0 800 240" xmlns="http://www.w3.org/2000/svg">
          <rect width="800" height="240" fill="#ffffff" rx="6" stroke="#cbd5e1"/>
          <text x="400" y="26" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Figure 4.3.6B: Circular Journal Ring Buffer &amp; In-Place Checkpoint Pipeline</text>

          <!-- Circular Ring Buffer Representation -->
          <rect x="40" y="60" width="440" height="150" fill="#0f172a" stroke="#334155" rx="6"/>
          <text x="260" y="84" font-family="sans-serif" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">Circular Journal Ring Buffer</text>

          <!-- Ring slots -->
          <rect x="55" y="102" width="70" height="50" fill="#1e293b" stroke="#334155" rx="3"/>
          <text x="90" y="125" font-family="sans-serif" font-size="9" fill="#94a3b8" text-anchor="middle">Tx 101</text>
          <text x="90" y="140" font-family="sans-serif" font-size="8" fill="#4ade80" text-anchor="middle">(Freed)</text>

          <rect x="135" y="102" width="85" height="50" fill="#3b82f6" rx="3"/>
          <text x="177" y="125" font-family="sans-serif" font-size="9" font-weight="bold" fill="#fff" text-anchor="middle">Tx 102 Data</text>
          <text x="177" y="140" font-family="sans-serif" font-size="8" fill="#dbeafe" text-anchor="middle">Descriptor</text>

          <rect x="230" y="102" width="85" height="50" fill="#059669" rx="3"/>
          <text x="272" y="125" font-family="sans-serif" font-size="9" font-weight="bold" fill="#fff" text-anchor="middle">Tx 102 Commit</text>
          <text x="272" y="140" font-family="sans-serif" font-size="8" fill="#d1fae5" text-anchor="middle">CRC Checksum</text>

          <rect x="325" y="102" width="80" height="50" fill="#3b82f6" rx="3"/>
          <text x="365" y="125" font-family="sans-serif" font-size="9" font-weight="bold" fill="#fff" text-anchor="middle">Tx 103 Writing</text>
          <text x="365" y="140" font-family="sans-serif" font-size="8" fill="#dbeafe" text-anchor="middle">Pending</text>

          <rect x="415" y="102" width="55" height="50" fill="#1e293b" stroke="#334155" rx="3"/>
          <text x="442" y="132" font-family="sans-serif" font-size="9" fill="#64748b" text-anchor="middle">Unused</text>

          <text x="260" y="190" font-family="sans-serif" font-size="9" fill="#94a3b8" text-anchor="middle">&larr; Checkpoint Head advances &bull; Journal Tail writes forward &rarr;</text>

          <!-- Checkpointing Arrow -->
          <path d="M 480 127 L 530 127" stroke="#10b981" stroke-width="3"/>
          <polygon points="535,127 525,121 525,133" fill="#10b981"/>
          <text x="507" y="115" font-family="sans-serif" font-size="9" font-weight="bold" fill="#10b981" text-anchor="middle">Flush</text>

          <!-- Permanent In-Place File System Structures -->
          <rect x="535" y="60" width="225" height="150" fill="#f8fafc" stroke="#cbd5e1" rx="6"/>
          <text x="647" y="84" font-family="sans-serif" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">Permanent In-Place Blocks</text>

          <rect x="550" y="102" width="60" height="40" fill="#0284c7" rx="3"/><text x="580" y="126" font-family="sans-serif" font-size="9" fill="#fff" text-anchor="middle">Inode Table</text>
          <rect x="620" y="102" width="60" height="40" fill="#f59e0b" rx="3"/><text x="650" y="126" font-family="sans-serif" font-size="9" fill="#fff" text-anchor="middle">Bitmap</text>
          <rect x="690" y="102" width="60" height="40" fill="#10b981" rx="3"/><text x="720" y="126" font-family="sans-serif" font-size="9" fill="#fff" text-anchor="middle">Data Block</text>

          <text x="647" y="180" font-family="sans-serif" font-size="9" fill="#475569" text-anchor="middle">Checkpointing writes in-place;</text>
          <text x="647" y="196" font-family="sans-serif" font-size="9" fill="#475569" text-anchor="middle">Transaction 102 can then be freed</text>
        </svg>
        <figcaption>Figure 4.3.6B: Transactions advance through the circular ring buffer before updating permanent in-place structures.</figcaption>
      </figure>

      <h3>3. Journaling Modes &amp; Performance Trade-offs</h3>
      <p>
        Writing every piece of data twice (once to the journal, and once to its permanent location) imposes significant I/O overhead. To balance write performance against data safety, modern journaling filesystems (such as Linux <strong>ext3</strong> and <strong>ext4</strong>) provide three distinct journaling operational modes:
      </p>
      <ul>
        <li><strong>Journal Mode (Full Data Journaling):</strong> Both file payload data and filesystem metadata are written to the journal before being committed and checkpointed to permanent blocks.
          <ul>
            <li><em>Safety:</em> Highest possible consistency guarantee. Neither metadata nor file data can be lost or corrupted on crash.</li>
            <li><em>Trade-off:</em> Lowest throughput. Every byte is written twice, imposing an unavoidable 2&times; write amplification penalty.</li>
          </ul>
        </li>
        <li><strong>Ordered Mode (Metadata-Only with Ordered Data Writes):</strong> Only filesystem metadata is recorded in the journal. However, the operating system enforces a strict ordering rule: <em>all user data blocks must be flushed to their permanent in-place disk blocks before the associated metadata transaction commits to the journal.</em>
          <ul>
            <li><em>Safety:</em> Guaranteed metadata consistency with strong data protection. A crash cannot leave an inode pointing to unwritten garbage or stale remnants of deleted files.</li>
            <li><em>Trade-off:</em> Highly optimized. Data is written to disk exactly once, eliminating write amplification while maintaining crash consistency. (Default mode in ext3/ext4).</li>
          </ul>
        </li>
        <li><strong>Writeback Mode (Metadata-Only with Relaxed Ordering):</strong> Only metadata is journaled, and no ordering constraints are imposed between user data writes and journal commits. Metadata can commit before user data blocks reach persistent media.
          <ul>
            <li><em>Safety:</em> Metadata integrity is preserved, but files modified just before a crash may contain stale remnants of previous deleted files from those blocks.</li>
            <li><em>Trade-off:</em> Maximum write performance and lowest I/O latency.</li>
          </ul>
        </li>
      </ul>

      <h3>4. Fast Crash Recovery: Redo Logging</h3>
      <p>
        When an operating system boots after a crash, the recovery sequence replaces exhaustive disk scans with an immediate inspection of the journal:
      </p>
      <ol>
        <li><strong>Locate Journal Boundaries:</strong> Read the journal superblock to determine the active head and tail offsets of the circular ring buffer.</li>
        <li><strong>Scan for Committed Transactions:</strong> Scan sequentially from the head. If a transaction possesses a valid header, intact payload blocks, and a matching checksum commit block, it is recognized as durable.</li>
        <li><strong>Redo Logging (Replay):</strong> For every valid committed transaction, the recovery engine reads the logged metadata blocks and writes them directly into their corresponding in-place filesystem disk blocks. This guarantees that all committed updates survive.</li>
        <li><strong>Discard Uncommitted Writes:</strong> If a transaction was interrupted mid-write (evidenced by a missing commit block or a checksum mismatch), the recovery engine discards it entirely. The filesystem cleanly reverts to the exact state it held prior to the uncommitted transaction.</li>
      </ol>
      <p>
        Because recovery only scans the compact journal ring buffer, the entire process completes in seconds regardless of partition capacity.
      </p>

      <!-- WALKTHROUGH PART 3: JOURNALING TRANSACTION & RECOVERY SIMULATOR -->
      <div class="lfs-sim-container" id="journalingSim">
        <div class="lfs-topbar">
          <span class="lfs-title">Walkthrough Part 3: Journaling Transaction &amp; Crash Recovery Simulator</span>
          <span class="lfs-step-indicator" id="journalStepTag">State: Normal Operation</span>
        </div>

        <div class="lfs-explanation-box" id="journalExplanationBox">
          <strong>Interactive Crash Recovery:</strong> Step through a journaling transaction. You can commit normally or inject a sudden power cut midway through to see how <strong>Redo Logging</strong> or <strong>Torn Transaction Discard</strong> protects filesystem integrity.
        </div>

        <div class="lfs-controls">
          <button class="lfs-btn primary" onclick="journalStepWriteTx()">1. Write Journal Transaction</button>
          <button class="lfs-btn accent" onclick="journalStepCommitTx()">2. Commit Transaction (Commit Blk)</button>
          <button class="lfs-btn" onclick="journalStepCheckpoint()">3. Checkpoint In-Place &amp; Free Log</button>
          <button class="lfs-btn danger" onclick="journalInjectCrash()">Inject Sudden Power Cut!</button>
          <button class="lfs-btn" onclick="journalResetWalkthrough()" style="margin-left: auto;">Reset Simulator</button>
        </div>

        <div class="lfs-segments-grid" id="journalSegmentsGrid"></div>

        <div class="lfs-status-panel">
          <span id="journalStatusMsg">Filesystem running in Ordered Journaling Mode. Ring buffer empty.</span>
          <span id="journalMetricMsg">Journal Ring: 0/8 Used | Checkpoint Status: Synchronized</span>
        </div>
      </div>
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
    // =========================================================
    // 1. WALKTHROUGH PART 1: SEQUENTIAL APPEND & DEAD SPACE
    // =========================================================
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
      document.getElementById("lfsStepTag").textContent = "Step 1 of 3: Ready";
      document.getElementById("lfsExplanationBox").innerHTML =
        "<strong>Welcome to the LFS Walkthrough!</strong> LFS converts all file system writes into a fast, contiguous sequential stream. Click <strong>'1. Append New File'</strong> to stream files into the log tail.";
      document.getElementById("lfsStatusMsg").textContent = "Walkthrough reset. Ready to append files.";
    }

    function lfsStepAppend() {
      if (currentWriteIndex >= NUM_SEGMENTS * BLOCKS_PER_SEGMENT) {
        document.getElementById("lfsExplanationBox").innerHTML =
          "<strong>Log Full!</strong> The disk log has filled up with mixed live and dead blocks. Click <strong>'3. Run Segment Cleaner'</strong> to perform garbage collection.";
        return;
      }
      let segIdx = Math.floor(currentWriteIndex / BLOCKS_PER_SEGMENT);
      let blkIdx = currentWriteIndex % BLOCKS_PER_SEGMENT;
      let fileId = `F${Math.floor(Math.random() * 90) + 10}`;
      lfsSegments[segIdx].blocks[blkIdx] = { type: 'live', fileId: fileId };
      currentWriteIndex++;

      lfsRenderSim();
      document.getElementById("lfsStepTag").textContent = "Step 1: Appending Data";
      document.getElementById("lfsExplanationBox").innerHTML =
        `<strong>Sequential Append in Action:</strong> File <code>${fileId}</code> was written instantly to Segment ${segIdx}, Block ${blkIdx} without any mechanical disk head seeks. Keep appending or proceed to step 2 to overwrite files.`;
      document.getElementById("lfsStatusMsg").textContent = `Successfully appended ${fileId} at sequential log tail.`;
    }

    function lfsStepOverwrite() {
      let liveBlocks = [];
      lfsSegments.forEach((seg, sIdx) => {
        seg.blocks.forEach((blk, bIdx) => {
          if (blk.type === 'live') liveBlocks.push({ sIdx, bIdx, fileId: blk.fileId });
        });
      });
      if (liveBlocks.length === 0) {
        document.getElementById("lfsExplanationBox").innerHTML =
          "<strong>No files to overwrite!</strong> Please click <strong>'1. Append New File'</strong> a few times first so there is data in the log.";
        return;
      }
      let target = liveBlocks[Math.floor(Math.random() * liveBlocks.length)];
      lfsSegments[target.sIdx].blocks[target.bIdx].type = 'dead';

      if (currentWriteIndex < NUM_SEGMENTS * BLOCKS_PER_SEGMENT) {
        let segIdx = Math.floor(currentWriteIndex / BLOCKS_PER_SEGMENT);
        let blkIdx = currentWriteIndex % BLOCKS_PER_SEGMENT;
        lfsSegments[segIdx].blocks[blkIdx] = { type: 'live', fileId: target.fileId };
        currentWriteIndex++;
      }

      lfsRenderSim();
      document.getElementById("lfsStepTag").textContent = "Step 2: Overwriting (Dead Space)";
      document.getElementById("lfsExplanationBox").innerHTML =
        `<strong>LFS No-Overwrite Policy:</strong> File <code>${target.fileId}</code> was updated. Its old block in Segment ${target.sIdx} is now marked <s>strikethrough</s> (Dead Space), and the new version is appended at the log tail. This creates fragmentation over time!`;
      document.getElementById("lfsStatusMsg").textContent = `Overwrote ${target.fileId}; old version marked dead.`;
    }

    function lfsStepClean() {
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
      document.getElementById("lfsStepTag").textContent = "Step 3: Garbage Collection";
      document.getElementById("lfsExplanationBox").innerHTML =
        "<strong>Segment Cleaner (GC) Complete:</strong> The background cleaner gathered all active live blocks, discarded the dead holes, and compacted everything neatly back to the front of the log. Free space is successfully reclaimed!";
      document.getElementById("lfsStatusMsg").textContent = "Segment compaction finished successfully.";
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
    }

    lfsResetSim();

    // =========================================================
    // 2. WALKTHROUGH PART 2: FOUR-PHASE COMPACTION CYCLE
    // =========================================================
    let fourPhaseSegments = [];
    let currentCompactionPhase = 0;
    let identifiedLiveBlocks = [];

    function compactionResetWalkthrough() {
      currentCompactionPhase = 0;
      identifiedLiveBlocks = [];

      fourPhaseSegments = [
        {
          id: 0,
          label: "Segment 0 (Candidate)",
          status: "normal",
          blocks: [
            { id: "A1", state: "live", highlight: false },
            { id: "A2", state: "dead", highlight: false },
            { id: "A3", state: "dead", highlight: false },
            { id: "A4", state: "live", highlight: false },
            { id: "A5", state: "dead", highlight: false },
            { id: "A6", state: "dead", highlight: false },
            { id: "A7", state: "dead", highlight: false },
            { id: "A8", state: "dead", highlight: false }
          ]
        },
        {
          id: 1,
          label: "Segment 1 (Candidate)",
          status: "normal",
          blocks: [
            { id: "B1", state: "dead", highlight: false },
            { id: "B2", state: "live", highlight: false },
            { id: "B3", state: "dead", highlight: false },
            { id: "B4", state: "dead", highlight: false },
            { id: "B5", state: "dead", highlight: false },
            { id: "B6", state: "live", highlight: false },
            { id: "B7", state: "dead", highlight: false },
            { id: "B8", state: "dead", highlight: false }
          ]
        },
        {
          id: 2,
          label: "Segment 2 (Log Tail)",
          status: "tail",
          blocks: [
            { id: "T1", state: "live", highlight: false },
            { id: "T2", state: "live", highlight: false },
            { id: "·", state: "free", highlight: false },
            { id: "·", state: "free", highlight: false },
            { id: "·", state: "free", highlight: false },
            { id: "·", state: "free", highlight: false },
            { id: "·", state: "free", highlight: false },
            { id: "·", state: "free", highlight: false }
          ]
        },
        {
          id: 3,
          label: "Segment 3 (Clean Free Pool)",
          status: "free_pool",
          blocks: [
            { id: "·", state: "free", highlight: false },
            { id: "·", state: "free", highlight: false },
            { id: "·", state: "free", highlight: false },
            { id: "·", state: "free", highlight: false },
            { id: "·", state: "free", highlight: false },
            { id: "·", state: "free", highlight: false },
            { id: "·", state: "free", highlight: false },
            { id: "·", state: "free", highlight: false }
          ]
        }
      ];

      fourPhaseRender();
      document.getElementById("fourPhaseStepTag").textContent = "Phase 0: Ready";
      document.getElementById("fourPhaseExplanationBox").innerHTML =
        "<strong>Ready to Begin 4-Phase Compaction:</strong> Segments 0 and 1 are fragmented with dead space holes. Click <strong>'1. Phase 1: Selection'</strong> to have the cleaner select candidates based on the cost-benefit formula.";
      document.getElementById("fourPhaseStatusMsg").textContent = "Walkthrough reset. Segments 0 and 1 are ready for cleaning evaluation.";
      document.getElementById("fourPhaseMetricMsg").textContent = "Selected: None | Live Migrated: 0 | Reclaimed Segments: 0";
    }

    function compactionPhase1Selection() {
      currentCompactionPhase = 1;
      fourPhaseSegments[0].status = "candidate";
      fourPhaseSegments[1].status = "candidate";
      fourPhaseSegments[0].label = "Seg 0 [SELECTED CANDIDATE]";
      fourPhaseSegments[1].label = "Seg 1 [SELECTED CANDIDATE]";

      fourPhaseRender();
      document.getElementById("fourPhaseStepTag").textContent = "Phase 1: Candidate Selection";
      document.getElementById("fourPhaseExplanationBox").innerHTML =
        "<strong>Phase 1 (Selection) Complete:</strong> The cleaner queried the on-disk segment usage table and computed ((1 - u) &times; Age) / (1 + u). Segments 0 and 1 were selected because their low utilization (u = 0.25) yields maximum contiguous free space. Click <strong>'2. Phase 2: Identification'</strong> to check block liveness!";
      document.getElementById("fourPhaseStatusMsg").textContent = "Phase 1: Segments 0 & 1 selected for compaction.";
      document.getElementById("fourPhaseMetricMsg").textContent = "Selected: Segments 0 & 1 | Live Migrated: 0 | Reclaimed Segments: 0";
    }

    function compactionPhase2Identification() {
      if (currentCompactionPhase < 1) {
        document.getElementById("fourPhaseExplanationBox").innerHTML = "Please click <strong>'1. Phase 1: Selection'</strong> first!";
        return;
      }
      currentCompactionPhase = 2;
      identifiedLiveBlocks = [];

      [0, 1].forEach(sIdx => {
        fourPhaseSegments[sIdx].blocks.forEach(blk => {
          if (blk.state === "live") {
            blk.highlight = "live";
            identifiedLiveBlocks.push(blk.id);
          } else {
            blk.highlight = "dead";
          }
        });
      });

      fourPhaseRender();
      document.getElementById("fourPhaseStepTag").textContent = "Phase 2: Liveness Verification";
      document.getElementById("fourPhaseExplanationBox").innerHTML =
        `<strong>Phase 2 (Identification) Complete:</strong> The cleaner read the Segment Summary blocks and performed O(1) Inode Map lookups. It confirmed <strong>4 surviving live blocks</strong> (<code>A1, A4, B2, B6</code> in green), while obsolete dead holes (dimmed) will be discarded. Click <strong>'3. Phase 3: Compaction & Append'</strong> to stream them to the log tail!`;
      document.getElementById("fourPhaseStatusMsg").textContent = `Phase 2: 4 live blocks verified against Imap (${identifiedLiveBlocks.join(', ')}).`;
      document.getElementById("fourPhaseMetricMsg").textContent = `Selected: Segments 0 & 1 | Verified Live: ${identifiedLiveBlocks.length} | Reclaimed Segments: 0`;
    }

    function compactionPhase3Compaction() {
      if (currentCompactionPhase < 2) {
        document.getElementById("fourPhaseExplanationBox").innerHTML = "Please complete <strong>Phase 2: Identification</strong> first!";
        return;
      }
      currentCompactionPhase = 3;

      let tailFreeSlots = fourPhaseSegments[2].blocks.filter(b => b.state === "free");
      for (let i = 0; i < identifiedLiveBlocks.length && i < tailFreeSlots.length; i++) {
        tailFreeSlots[i].id = identifiedLiveBlocks[i];
        tailFreeSlots[i].state = "live";
        tailFreeSlots[i].highlight = "migrated";
      }

      fourPhaseSegments[2].label = "Segment 2 [COMPACTED APPEND]";

      fourPhaseRender();
      document.getElementById("fourPhaseStepTag").textContent = "Phase 3: Compaction & Append";
      document.getElementById("fourPhaseExplanationBox").innerHTML =
        `<strong>Phase 3 (Compaction & Append) Complete:</strong> The 4 surviving live blocks were bundled into an in-memory segment buffer and written sequentially to the <strong>active log tail</strong> (Segment 2) without seeks! Their Inode Map entries were updated with their new addresses. Click <strong>'4. Phase 4: Reclamation'</strong> to free the old segments!`;
      document.getElementById("fourPhaseStatusMsg").textContent = "Phase 3: Live blocks written contiguously to log tail; Inode Map updated.";
      document.getElementById("fourPhaseMetricMsg").textContent = `Selected: Segments 0 & 1 | Live Migrated: ${identifiedLiveBlocks.length} | Reclaimed Segments: 0`;
    }

    function compactionPhase4Reclamation() {
      if (currentCompactionPhase < 3) {
        document.getElementById("fourPhaseExplanationBox").innerHTML = "Please complete <strong>Phase 3: Compaction & Append</strong> first!";
        return;
      }
      currentCompactionPhase = 4;

      [0, 1].forEach(sIdx => {
        fourPhaseSegments[sIdx].blocks = [
          { id: "·", state: "free", highlight: false },
          { id: "·", state: "free", highlight: false },
          { id: "·", state: "free", highlight: false },
          { id: "·", state: "free", highlight: false },
          { id: "·", state: "free", highlight: false },
          { id: "·", state: "free", highlight: false },
          { id: "·", state: "free", highlight: false },
          { id: "·", state: "free", highlight: false }
        ];
        fourPhaseSegments[sIdx].status = "free_pool";
        fourPhaseSegments[sIdx].label = `Segment ${sIdx} (Clean Free Pool)`;
      });

      fourPhaseSegments[2].blocks.forEach(b => b.highlight = false);

      fourPhaseRender();
      document.getElementById("fourPhaseStepTag").textContent = "Phase 4: Reclamation Finished!";
      document.getElementById("fourPhaseExplanationBox").innerHTML =
        "<strong>Phase 4 (Reclamation) Complete:</strong> Segments 0 and 1 were cleared and added to the Clean Free Pool. <strong>16 contiguous blocks (2 full segments) are now 100% free</strong> for future log streaming! Compaction finished with zero downtime.";
      document.getElementById("fourPhaseStatusMsg").textContent = "Phase 4: Segments 0 & 1 recycled. Clean free pool expanded!";
      document.getElementById("fourPhaseMetricMsg").textContent = "Selected: None | Live Migrated: 4 | Reclaimed Segments: 2 (16 Blocks)";
    }

    function fourPhaseRender() {
      const grid = document.getElementById("fourPhaseSegmentsGrid");
      grid.innerHTML = "";

      fourPhaseSegments.forEach(seg => {
        let segDiv = document.createElement("div");
        segDiv.className = "lfs-segment-box";
        if (seg.status === "candidate") segDiv.classList.add("blk-candidate");

        segDiv.innerHTML = `<div class="lfs-seg-header"><span>${seg.label}</span></div>`;

        let blocksDiv = document.createElement("div");
        blocksDiv.className = "lfs-seg-blocks";

        seg.blocks.forEach(blk => {
          let bEl = document.createElement("div");
          bEl.className = "lfs-block";
          bEl.textContent = blk.id;

          if (blk.state === "free") {
            bEl.classList.add("blk-free");
          } else if (blk.state === "live") {
            bEl.classList.add("blk-live");
          } else if (blk.state === "dead") {
            bEl.classList.add("blk-dead");
          }

          if (blk.highlight === "live") {
            bEl.classList.add("blk-identified-live");
          } else if (blk.highlight === "dead") {
            bEl.classList.add("blk-discarded");
          } else if (blk.highlight === "migrated") {
            bEl.classList.add("blk-identified-live");
          }

          blocksDiv.appendChild(bEl);
        });

        segDiv.appendChild(blocksDiv);
        grid.appendChild(segDiv);
      });
    }

    compactionResetWalkthrough();

    // =========================================================
    // 3. WALKTHROUGH PART 3: JOURNALING & CRASH RECOVERY SIM
    // =========================================================
    let journalState = "idle"; // idle, written, committed, checkpointed, crashed
    let journalBlocks = [];
    let permanentFsBlocks = [];

    function journalResetWalkthrough() {
      journalState = "idle";
      journalBlocks = [
        { id: "·", state: "free", label: "Empty" },
        { id: "·", state: "free", label: "Empty" },
        { id: "·", state: "free", label: "Empty" },
        { id: "·", state: "free", label: "Empty" },
        { id: "·", state: "free", label: "Empty" },
        { id: "·", state: "free", label: "Empty" },
        { id: "·", state: "free", label: "Empty" },
        { id: "·", state: "free", label: "Empty" }
      ];

      permanentFsBlocks = [
        { id: "Ino: 2", state: "fs", label: "Inode Table" },
        { id: "Map: OK", state: "fs", label: "Bitmap" },
        { id: "Blk: 10", state: "fs", label: "Data Block" },
        { id: "Blk: 11", state: "fs", label: "Data Block" }
      ];

      journalRender();
      document.getElementById("journalStepTag").textContent = "State: Normal Operation (Idle)";
      document.getElementById("journalExplanationBox").innerHTML =
        "<strong>Ready to Trace WAL Transaction:</strong> In Ordered Mode, user data writes directly to disk before metadata commits. Click <strong>'1. Write Journal Transaction'</strong> to start appending to the circular ring buffer.";
      document.getElementById("journalStatusMsg").textContent = "Filesystem running in Ordered Journaling Mode. Ring buffer empty.";
      document.getElementById("journalMetricMsg").textContent = "Journal Ring: 0/8 Used | Checkpoint Status: Synchronized";
    }

    function journalStepWriteTx() {
      if (journalState !== "idle") {
        document.getElementById("journalExplanationBox").innerHTML =
          "A transaction is already in flight! Commit it or reset the simulator.";
        return;
      }
      journalState = "written";

      journalBlocks[0] = { id: "TxHead", state: "head", label: "Header" };
      journalBlocks[1] = { id: "Ino: 2*", state: "tx", label: "Inode Update" };
      journalBlocks[2] = { id: "Map: *", state: "tx", label: "Bitmap Update" };

      journalRender();
      document.getElementById("journalStepTag").textContent = "State: Journal Written (Uncommitted)";
      document.getElementById("journalExplanationBox").innerHTML =
        "<strong>Transaction In Flight:</strong> Changes are written to the journal ring buffer, but <strong>NO Commit Block exists yet</strong>. If power cuts right now, this partial transaction will be cleanly ignored. Click <strong>'2. Commit Transaction'</strong> or test <strong>'Inject Sudden Power Cut!'</strong>.";
      document.getElementById("journalStatusMsg").textContent = "Transaction written to journal. Awaiting atomic commit record.";
      document.getElementById("journalMetricMsg").textContent = "Journal Ring: 3/8 Used | Checkpoint Status: Pending Commit";
    }

    function journalStepCommitTx() {
      if (journalState !== "written") {
        document.getElementById("journalExplanationBox").innerHTML =
          "Please write a transaction first by clicking <strong>'1. Write Journal Transaction'</strong>!";
        return;
      }
      journalState = "committed";

      journalBlocks[3] = { id: "COMMIT", state: "commit", label: "Commit Block (CRC)" };

      journalRender();
      document.getElementById("journalStepTag").textContent = "State: Transaction COMMITTED";
      document.getElementById("journalExplanationBox").innerHTML =
        "<strong>Commit Boundary Established!</strong> The Commit Block with CRC checksum reached non-volatile media. The transaction is now formally durable. Even if a crash strikes this instant, <strong>Redo Logging</strong> will guarantee recovery. Click <strong>'3. Checkpoint In-Place'</strong> to flush to permanent blocks.";
      document.getElementById("journalStatusMsg").textContent = "Transaction committed! Safe from data loss.";
      document.getElementById("journalMetricMsg").textContent = "Journal Ring: 4/8 Used | Checkpoint Status: Ready to Checkpoint";
    }

    function journalStepCheckpoint() {
      if (journalState !== "committed") {
        document.getElementById("journalExplanationBox").innerHTML =
          "Transaction must be committed before checkpointing! Click <strong>'2. Commit Transaction'</strong>.";
        return;
      }
      journalState = "checkpointed";

      // Flush changes to permanent in-place filesystem blocks
      permanentFsBlocks[0] = { id: "Ino: 2*", state: "checkpointed", label: "Inode Table (Updated)" };
      permanentFsBlocks[1] = { id: "Map: *", state: "checkpointed", label: "Bitmap (Updated)" };

      // Free journal ring
      journalBlocks = [
        { id: "·", state: "free", label: "Freed" },
        { id: "·", state: "free", label: "Freed" },
        { id: "·", state: "free", label: "Freed" },
        { id: "·", state: "free", label: "Freed" },
        { id: "·", state: "free", label: "Empty" },
        { id: "·", state: "free", label: "Empty" },
        { id: "·", state: "free", label: "Empty" },
        { id: "·", state: "free", label: "Empty" }
      ];

      journalRender();
      document.getElementById("journalStepTag").textContent = "State: Checkpointed & Log Freed";
      document.getElementById("journalExplanationBox").innerHTML =
        "<strong>Checkpoint Complete!</strong> Changes were written in-place to the permanent filesystem structures. The journal ring buffer slots are now freed for upcoming transactions. Full cycle executed with zero integrity risk!";
      document.getElementById("journalStatusMsg").textContent = "In-place blocks synchronized. Circular journal freed.";
      document.getElementById("journalMetricMsg").textContent = "Journal Ring: 0/8 Used | Checkpoint Status: Fully Checkpointed";
    }

    function journalInjectCrash() {
      if (journalState === "written") {
        // Crash before commit block: torn transaction
        journalState = "crashed_uncommitted";
        journalBlocks[0].state = "corrupt";
        journalBlocks[1].state = "corrupt";
        journalBlocks[2].state = "corrupt";

        journalRender();
        document.getElementById("journalStepTag").textContent = "Crash Recovery: Torn Write Discarded";
        document.getElementById("journalExplanationBox").innerHTML =
          "<strong>Power Cut Occurred Before Commit:</strong> On boot, the recovery engine scanned the journal ring and discovered an incomplete transaction without a valid Commit Block. <strong>The uncommitted write was discarded in 2 milliseconds</strong>. Permanent in-place structures remain 100% consistent!";
        document.getElementById("journalStatusMsg").textContent = "Recovery completed: partial transaction discarded. Filesystem consistent.";
        document.getElementById("journalMetricMsg").textContent = "Journal Ring: Cleaned | Recovery Time: 2 ms";
      } else if (journalState === "committed") {
        // Crash after commit block: redo recovery
        journalState = "crashed_committed";
        permanentFsBlocks[0] = { id: "Ino: 2*", state: "checkpointed", label: "Inode Table (Replayed)" };
        permanentFsBlocks[1] = { id: "Map: *", state: "checkpointed", label: "Bitmap (Replayed)" };

        journalRender();
        document.getElementById("journalStepTag").textContent = "Crash Recovery: Redo Logging Replay";
        document.getElementById("journalExplanationBox").innerHTML =
          "<strong>Power Cut Occurred After Commit:</strong> Permanent in-place blocks had not been updated yet. On boot, the recovery engine verified the Commit Block CRC and <strong>replayed the transaction into permanent blocks</strong>. Zero committed data was lost!";
        document.getElementById("journalStatusMsg").textContent = "Recovery completed: Redo logging replayed transaction into in-place blocks.";
        document.getElementById("journalMetricMsg").textContent = "Journal Ring: Replayed | Recovery Time: 5 ms";
      } else {
        document.getElementById("journalExplanationBox").innerHTML =
          "Please write a transaction (Phase 1) or commit it (Phase 2) before testing a crash!";
      }
    }

    function journalRender() {
      const grid = document.getElementById("journalSegmentsGrid");
      grid.innerHTML = "";

      // Render Journal Ring Container
      let jDiv = document.createElement("div");
      jDiv.className = "lfs-segment-box";
      jDiv.style.gridColumn = "span 2";
      jDiv.innerHTML = `<div class="lfs-seg-header"><span>Circular Journal Ring Buffer</span><span>Head &rarr; Tail</span></div>`;

      let jBlocksDiv = document.createElement("div");
      jBlocksDiv.className = "lfs-seg-blocks";
      jBlocksDiv.style.gridTemplateColumns = "repeat(8, 1fr)";

      journalBlocks.forEach(blk => {
        let bEl = document.createElement("div");
        bEl.className = "lfs-block";
        bEl.textContent = blk.id;

        if (blk.state === "free") bEl.classList.add("blk-free");
        else if (blk.state === "head") bEl.classList.add("blk-journal-head");
        else if (blk.state === "tx") bEl.classList.add("blk-journal-tx");
        else if (blk.state === "commit") bEl.classList.add("blk-journal-commit");
        else if (blk.state === "corrupt") bEl.classList.add("blk-journal-corrupt");

        jBlocksDiv.appendChild(bEl);
      });
      jDiv.appendChild(jBlocksDiv);
      grid.appendChild(jDiv);

      // Render Permanent Filesystem Container
      let fsDiv = document.createElement("div");
      fsDiv.className = "lfs-segment-box";
      fsDiv.style.gridColumn = "span 2";
      fsDiv.innerHTML = `<div class="lfs-seg-header"><span>Permanent In-Place Storage</span><span>Checkpoint Destination</span></div>`;

      let fsBlocksDiv = document.createElement("div");
      fsBlocksDiv.className = "lfs-seg-blocks";
      fsBlocksDiv.style.gridTemplateColumns = "repeat(4, 1fr)";

      permanentFsBlocks.forEach(blk => {
        let bEl = document.createElement("div");
        bEl.className = "lfs-block";
        bEl.textContent = blk.id;

        if (blk.state === "fs") bEl.classList.add("blk-live");
        else if (blk.state === "checkpointed") bEl.classList.add("blk-fs-checkpointed");

        fsBlocksDiv.appendChild(bEl);
      });
      fsDiv.appendChild(fsBlocksDiv);
      grid.appendChild(fsDiv);
    }

    journalResetWalkthrough();

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

    print(f"--> Writing expanded Journaling section to {html_file}...")
    os.makedirs(os.path.dirname(html_file), exist_ok=True)
    final_content = HTML_CONTENT.replace("AUDIO_DATA_URI_PLACEHOLDER", data_uri)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(final_content)
    print("--> HTML structure successfully written!")

    commit_msg = (
        "Expand section 4.3.6 on journaling file systems with theory and diagrams\n\n"
        "Update week10-file-management/03-filesystem-implementation.html to "
        "comprehensively expand section 4.3.6 with deep crash consistency theory, "
        "ordered vs writeback modes, two SVG diagrams, and an interactive crash "
        "recovery simulation widget."
    )

    execute_git_command(["git", "add", html_file], "Staging HTML file")
    execute_git_command(["git", "commit", "-am", commit_msg], "Committing changes")
    execute_git_command(["git", "push", "origin", "main"], "Pushing changes to origin")
    print("--> Deployment complete!")

if __name__ == "__main__":
    execute_deployment()
