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

    /* STREAMLINED SIMULATOR CONTAINERS */
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

    /* Flash / FTL Block Classes */
    .blk-flash-erased { background: #0f172a; border: 1px dashed #38bdf8; color: #38bdf8; }
    .blk-flash-valid { background: #0284c7; color: #ffffff; }
    .blk-flash-invalid { background: #64748b; color: #cbd5e1; text-decoration: line-through; }
    .blk-flash-static { background: #4338ca; color: #ffffff; }

    /* VFS Object Classes */
    .blk-vfs-fd { background: #6366f1; color: #ffffff; }
    .blk-vfs-file { background: #0284c7; color: #ffffff; }
    .blk-vfs-dentry { background: #0d9488; color: #ffffff; }
    .blk-vfs-inode { background: #d97706; color: #ffffff; }

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
        In traditional file systems, inode numbers map to fixed disk offsets. In LFS, inodes relocate on every append, requiring the Inode Map (Imap) indirection layer.
      </p>

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
        LFS breaks recursive imap indirection using fixed Checkpoint Regions (CRs). To prevent write tearing during power cuts, LFS alternates between dual regions (CR A and CR B), picking the most recent valid checksum upon reboot.
      </p>

      <!-- Section 4: Segment Cleaning & Garbage Collection -->
      <h3>4. Background Garbage Collection &amp; Segment Cleaning</h3>
      <p>
        Segment cleaning reclaims fragmented dead space using the Cost-Benefit policy $((1-u) \times \text{Age}) / (1+u)$, balancing hot and cold data compaction.
      </p>

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

    <!-- MASSIVELY EXPANDED SECTION 4.3.6: JOURNALING & WRITE-AHEAD LOGGING -->
    <div class="section-block">
      <h2>4.3.6 Journaling File Systems &amp; Write-Ahead Logging (WAL)</h2>
      <p>
        Traditional filesystems update structures directly in-place across scattered disk blocks. When a sudden power outage, kernel panic, or hardware disconnect occurs mid-write, the filesystem is caught midway through mutating interlinked records, producing severe metadata desynchronization.
      </p>
      <p>
        To prevent lengthy multi-hour volume repair scans upon reboot (such as <code>fsck</code>), modern filesystems (including Linux <code>ext3</code>, <code>ext4</code>, <code>XFS</code>, and Windows <code>NTFS</code>) implement <strong>Write-Ahead Logging (WAL)</strong>, universally referred to as <strong>Journaling</strong>.
      </p>

      <h3>1. The Crash Consistency Problem</h3>
      <p>
        A single high-level file modification rarely maps to a single physical disk write. Appending data to an existing file requires executing three distinct physical writes:
      </p>
      <ol>
        <li><strong>Data Block Write:</strong> Writing user payload bytes into a newly allocated data block ($D$).</li>
        <li><strong>Inode Metadata Update:</strong> Modifying the file's inode ($I$) to update file length, modification timestamps, and insert an address pointer referencing block $D$.</li>
        <li><strong>Data Allocation Bitmap Update:</strong> Toggling the corresponding bit in the block allocation bitmap ($B$) from <code>0</code> (free) to <code>1</code> (allocated) to prevent other files from claiming block $D$.</li>
      </ol>
      <p>
        Physical storage controllers guarantee atomic writes strictly at the granularity of a <strong>single physical sector</strong> (typically 512 bytes or 4 KB). Atomic writes across three completely separate disk blocks located thousands of sectors apart are physically impossible. If the system loses power between any of these operations, the filesystem enters an inconsistent failure state:
      </p>
      <ul>
        <li><strong>Crash after Inode ($I$), before Bitmap ($B$):</strong> The inode references block $D$, but the bitmap marks block $D$ as free. When another process creates a file, the allocator will grant that exact same block $D$ to the new file, producing <strong>block cross-allocation and catastrophic data theft</strong>.</li>
        <li><strong>Crash after Bitmap ($B$), before Inode ($I$):</strong> Block $D$ is marked occupied in the bitmap, but no inode in the entire file system points to it. This creates a permanent, silent <strong>storage space leak</strong>.</li>
        <li><strong>Crash after Inode ($I$), before Data ($D$):</strong> The inode points to block $D$, but block $D$ was never written. Reading the file returns uninitialized remnants of whatever deleted data resided in that sector previously, causing <strong>data corruption and severe security information leakage</strong>.</li>
      </ul>

      <h3>2. The Write-Ahead Logging (WAL) Protocol</h3>
      <p>
        Journaling solves this vulnerability by importing the <strong>Write-Ahead Logging (WAL)</strong> protocol from relational database engines. The governing invariant of Write-Ahead Logging is absolute:
      </p>
      <blockquote>
        <strong>The Fundamental WAL Rule:</strong> Never overwrite or update the permanent in-place filesystem structures on disk until a complete description of the impending changes has been sequentially logged, flushed to non-volatile media, and anchored by an explicit, atomic commit record.
      </blockquote>
      <p>
        Rather than writing directly to the permanent inode tables and allocation bitmaps, the operating system routes modifications through a dedicated, contiguous circular ring buffer called the <strong>Journal</strong> (or log).
      </p>

      <h4>The Anatomy of a Journal Transaction</h4>
      <p>
        Related updates are bundled together into an atomic container called a <strong>Transaction</strong>. A transaction proceeds through four chronological stages:
      </p>
      <ol>
        <li><strong>Transaction Header (Tx Begin):</strong> A special descriptor block containing a unique monotonically increasing Transaction ID (TID), starting timestamp, and a manifest of the dirty metadata blocks scheduled for modification.</li>
        <li><strong>Descriptor &amp; Payload Blocks:</strong> The operating system writes exact in-memory copies of the updated inode ($I$), the updated allocation bitmap ($B$), and any modified directory blocks into the sequential journal stream.</li>
        <li><strong>Write Barrier &amp; The Commit Block:</strong> The controller issues a strict hardware write barrier (e.g., <code>FLUSH CACHE</code> or <code>FUA</code> &ndash; Force Unit Access) to ensure all payload blocks are physically seated on persistent media. Only then does it append the <strong>Commit Block</strong>. The commit block contains the matching Transaction ID and a cryptographic/CRC32 checksum of the entire transaction payload. The instant this commit block reaches disk, the transaction is durable.</li>
        <li><strong>Checkpointing (In-Place Flushing):</strong> With the transaction safely recorded in the journal, the operating system writes the modified blocks out to their permanent locations across the disk (the real inode table, the real bitmap).</li>
        <li><strong>Transaction Release (Journal Free):</strong> Once in-place checkpointing finishes, the circular journal marks that transaction's ring buffer sectors as reclaimed, advancing the journal head pointer.</li>
      </ol>

      <!-- Diagram 4.3.6A: WAL Pipeline & Invariants -->
      <figure class="diagram-figure">
        <svg class="diagram-svg" viewBox="0 0 800 250" xmlns="http://www.w3.org/2000/svg">
          <rect width="800" height="250" fill="#ffffff" rx="6" stroke="#cbd5e1"/>
          <text x="400" y="26" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Figure 4.3.6A: The Write-Ahead Logging (WAL) Architecture and Atomic Commit Boundary</text>

          <!-- Traditional Unsafe Box -->
          <rect x="30" y="55" width="340" height="175" fill="#fef2f2" stroke="#f87171" rx="4"/>
          <text x="200" y="76" font-family="sans-serif" font-size="11" font-weight="bold" fill="#b91c1c" text-anchor="middle">Traditional Non-Atomic Writes (Vulnerable)</text>
          <line x1="40" y1="86" x2="360" y2="86" stroke="#fecaca" stroke-width="1"/>

          <rect x="45" y="100" width="85" height="40" fill="#0284c7" rx="2"/><text x="87.5" y="125" font-family="sans-serif" font-size="10" fill="#fff" text-anchor="middle">1. Data ($D$)</text>
          <line x1="130" y1="120" x2="160" y2="120" stroke="#dc2626" stroke-width="2"/>
          <rect x="160" y="100" width="85" height="40" fill="#f59e0b" rx="2"/><text x="202.5" y="125" font-family="sans-serif" font-size="10" fill="#fff" text-anchor="middle">2. Inode ($I$)</text>

          <!-- Lightning Bolt Crash Window -->
          <line x1="255" y1="92" x2="255" y2="150" stroke="#ef4444" stroke-width="3" stroke-dasharray="4,3"/>
          <text x="255" y="90" font-family="sans-serif" font-size="14" fill="#dc2626" text-anchor="middle">&#9889;</text>
          <text x="255" y="165" font-family="sans-serif" font-size="8" font-weight="bold" fill="#dc2626" text-anchor="middle">Power Cut!</text>

          <rect x="270" y="100" width="85" height="40" fill="#94a3b8" rx="2" stroke="#dc2626" stroke-dasharray="2,2"/><text x="312.5" y="125" font-family="sans-serif" font-size="10" fill="#fff" text-anchor="middle">3. Bitmap ($B$)</text>

          <text x="200" y="195" font-family="sans-serif" font-size="9" fill="#7f1d1d" text-anchor="middle">Result: $I$ points to $D$, but $B$ marks $D$ as free!</text>
          <text x="200" y="212" font-family="sans-serif" font-size="9" font-weight="bold" fill="#b91c1c" text-anchor="middle">Causes cross-allocation, corrupt files, or space leaks.</text>

          <!-- Safe WAL Pipeline Box -->
          <rect x="400" y="55" width="370" height="175" fill="#f0fdf4" stroke="#4ade80" rx="4"/>
          <text x="585" y="76" font-family="sans-serif" font-size="11" font-weight="bold" fill="#15803d" text-anchor="middle">Write-Ahead Logging (WAL) Protocol (Crash-Proof)</text>
          <line x1="410" y1="86" x2="760" y2="86" stroke="#bbf7d0" stroke-width="1"/>

          <!-- Step 1 & 2: Log write -->
          <rect x="415" y="98" width="60" height="38" fill="#3b82f6" rx="2"/><text x="445" y="122" font-family="sans-serif" font-size="9" fill="#fff" text-anchor="middle">Tx Begin</text>
          <rect x="480" y="98" width="65" height="38" fill="#3b82f6" rx="2"/><text x="512.5" y="122" font-family="sans-serif" font-size="9" fill="#fff" text-anchor="middle">Payload ($I, B$)</text>

          <!-- Barrier -->
          <line x1="550" y1="95" x2="550" y2="142" stroke="#0284c7" stroke-width="2"/>

          <!-- Commit block -->
          <rect x="555" y="98" width="70" height="38" fill="#059669" rx="2"/><text x="590" y="122" font-family="sans-serif" font-size="9" font-weight="bold" fill="#fff" text-anchor="middle">Commit Blk</text>

          <!-- Arrow to checkpoint -->
          <line x1="630" y1="117" x2="665" y2="117" stroke="#16a34a" stroke-width="2"/>
          <polygon points="670,117 662,112 662,122" fill="#16a34a"/>

          <!-- Checkpoint -->
          <rect x="670" y="98" width="90" height="38" fill="#10b981" rx="2"/><text x="715" y="122" font-family="sans-serif" font-size="9" font-weight="bold" fill="#fff" text-anchor="middle">In-Place Write</text>

          <text x="585" y="165" font-family="sans-serif" font-size="9" font-weight="bold" fill="#047857" text-anchor="middle">&uarr; Atomic Commit Boundary (CRC Checksum) &uarr;</text>
          <text x="585" y="190" font-family="sans-serif" font-size="9" fill="#14532d" text-anchor="middle">Crash before commit: Drop partial transaction cleanly.</text>
          <text x="585" y="206" font-family="sans-serif" font-size="9" fill="#14532d" text-anchor="middle">Crash after commit: Redo logging replays checkpoint.</text>
        </svg>
        <figcaption>Figure 4.3.6A: The WAL protocol isolates multi-block updates behind an atomic, checksummed commit boundary.</figcaption>
      </figure>

      <h3>3. The Hardware Reality: Write Caches &amp; Write Barriers</h3>
      <p>
        The theoretical integrity of Write-Ahead Logging hinges on sequential execution: payload blocks must be physically recorded on media <em>before</em> the commit block is written.
      </p>
      <p>
        In modern systems, hard drives and SSDs contain volatile onboard DRAM write caches. To optimize throughput, drive firmware reorders writes, grouping adjacent sectors to minimize seek times. Without operating system control, the storage controller might flush the small <strong>commit block</strong> to physical NAND/platters <em>before</em> it finishes writing the dirty inode or bitmap blocks. If power drops at that exact millisecond, the journal contains a valid commit block pointing to unwritten garbage!
      </p>
      <p>
        To prevent this catastrophic out-of-order execution, journaling file systems issue explicit <strong>Write Barriers</strong> (cache flushes). A write barrier instructs the drive controller to flush its entire volatile cache to permanent media before accepting any further writes. Only after the drive acknowledges the completion of the barrier does the filesystem dispatch the commit block.
      </p>

      <h3>4. Journaling Modes &amp; Operational Trade-offs</h3>
      <p>
        Writing every single user data byte to the journal and then writing it again to its permanent file block imposes a 100% write overhead (a write amplification factor of 2.0). To balance data integrity against I/O throughput, filesystems provide three operational modes:
      </p>

      <h4>1. Journal Mode (Full Data &amp; Metadata Logging)</h4>
      <p>
        Both user data bytes and filesystem metadata blocks are written into the circular journal before being committed and checkpointed to permanent blocks.
      </p>
      <ul>
        <li><strong>Consistency Guarantee:</strong> Absolute. Neither metadata nor file data can ever be lost or corrupted across a crash.</li>
        <li><strong>Performance Cost:</strong> Severe. Every byte is written to storage twice, cutting effective sequential write bandwidth in half.</li>
      </ul>

      <h4>2. Ordered Mode (Metadata Journaling with Ordered Data Flushing)</h4>
      <p>
        Only filesystem metadata blocks are logged to the journal. However, to prevent file pointers from referencing garbage, the operating system enforces a strict ordering barrier: <em>all user payload data blocks must be flushed to their permanent in-place disk locations BEFORE the associated metadata transaction commits to the journal.</em>
      </p>
      <ul>
        <li><strong>Consistency Guarantee:</strong> Guaranteed metadata integrity with strong data safety. Inodes never point to unwritten garbage or stale remnants of previously deleted files.</li>
        <li><strong>Performance Cost:</strong> Highly optimal. User data is written to disk exactly once, eliminating write amplification while preserving crash consistency. This is the default mode in Linux <code>ext3</code> and <code>ext4</code>.</li>
      </ul>

      <h4>3. Writeback Mode (Relaxed Metadata Journaling)</h4>
      <p>
        Only metadata is journaled. No ordering constraints are imposed between user data writes and metadata commits. Metadata transactions can commit to the journal while user data blocks still sit dirty in volatile RAM.
      </p>
      <ul>
        <li><strong>Consistency Guarantee:</strong> Metadata remains consistent, but files appended to shortly before a crash may contain stale remnants of old, deleted file content.</li>
        <li><strong>Performance Cost:</strong> Highest possible write throughput and lowest write latency.</li>
      </ul>

      <!-- Diagram 4.3.6B: Circular Journal Ring Buffer -->
      <figure class="diagram-figure">
        <svg class="diagram-svg" viewBox="0 0 800 240" xmlns="http://www.w3.org/2000/svg">
          <rect width="800" height="240" fill="#ffffff" rx="6" stroke="#cbd5e1"/>
          <text x="400" y="26" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">Figure 4.3.6B: Circular Journal Ring Buffer &amp; In-Place Checkpoint Pipeline</text>

          <rect x="40" y="60" width="440" height="150" fill="#0f172a" stroke="#334155" rx="6"/>
          <text x="260" y="84" font-family="sans-serif" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">Circular Journal Ring Buffer</text>

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

          <path d="M 480 127 L 530 127" stroke="#10b981" stroke-width="3"/>
          <polygon points="535,127 525,121 525,133" fill="#10b981"/>
          <text x="507" y="115" font-family="sans-serif" font-size="9" font-weight="bold" fill="#10b981" text-anchor="middle">Flush</text>

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

      <h3>5. Fast Crash Recovery: Redo Logging &amp; Rollback</h3>
      <p>
        When mounting a filesystem after a crash, the operating system bypasses full-disk scans and inspects only the journal:
      </p>
      <ul>
        <li><strong>Committed Transactions (Redo Log Replay):</strong> The recovery engine scans sequentially from the journal head. When it encounters a transaction with an intact commit block and matching CRC checksum, it executes <strong>redo logging</strong>: reading the logged metadata blocks from the journal and writing them directly into their in-place filesystem blocks. Because redo operations are completely <em>idempotent</em>, re-applying a write that already made it to disk before the crash is harmless.</li>
        <li><strong>Uncommitted Transactions (Torn Write Discard):</strong> If the recovery engine encounters a transaction that ends abruptly without a commit block (or whose CRC checksum fails due to a torn write), it halts scanning and discards the transaction. The uncommitted modifications never touch the permanent filesystem blocks, leaving the volume in the clean, consistent state it held prior to the interrupted operation.</li>
      </ul>

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
        Flash memory cannot overwrite in place due to the erase-before-write constraint. The Flash Translation Layer (FTL) handles out-of-place writes, garbage collection, and dynamic/static wear leveling.
      </p>

      <!-- Section 4.3.7 Walkthrough -->
      <div class="lfs-sim-container" id="ftlSim">
        <div class="lfs-topbar">
          <span class="lfs-title">Walkthrough Part 4: FTL Page Remapping, Wear-Leveling &amp; TRIM Simulator</span>
          <span class="lfs-step-indicator" id="ftlStepTag">P/E Telemetry Active</span>
        </div>

        <div class="lfs-explanation-box" id="ftlExplanationBox">
          <strong>Interactive FTL &amp; Flash Memory Walkthrough:</strong> Test out-of-place writes, trigger an OS <code>TRIM</code> notification to invalidate dead records, and observe how <strong>Static Wear-Leveling</strong> moves cold data to preserve flash cells.
        </div>

        <div class="lfs-controls">
          <button class="lfs-btn primary" onclick="ftlWriteLba()">1. Write LBA (Out-of-Place)</button>
          <button class="lfs-btn" onclick="ftlIssueTrim()">2. Issue OS TRIM on LBA 1</button>
          <button class="lfs-btn accent" onclick="ftlRunGarbageCollection()">3. Run Garbage Collection (GC)</button>
          <button class="lfs-btn" onclick="ftlStaticWearLevel()">4. Execute Static Wear-Leveling</button>
          <button class="lfs-btn" onclick="ftlResetWalkthrough()" style="margin-left: auto;">Reset Simulator</button>
        </div>

        <div class="lfs-segments-grid" id="ftlSegmentsGrid"></div>

        <div class="lfs-status-panel">
          <span id="ftlStatusMsg">SSD Initialized. 4 Erase Blocks ready.</span>
          <span id="ftlMetricMsg">Host Writes: 0 | Flash Writes: 0 | WAF: 1.00x</span>
        </div>
      </div>
    </div>

    <!-- Section 4.3.8: Virtual File Systems (VFS) -->
    <div class="section-block">
      <h2>4.3.8 Virtual File Systems (VFS)</h2>
      <p>
        Modern operating systems implement the Virtual File System (VFS) abstraction layer to support multiple disparate storage formats seamlessly through standard objects.
      </p>

      <!-- Section 4.3.8 Walkthrough -->
      <div class="lfs-sim-container" id="vfsSim">
        <div class="lfs-topbar">
          <span class="lfs-title">Walkthrough Part 5: VFS Dispatch, Path Walk &amp; Mount Resolution</span>
          <span class="lfs-step-indicator" id="vfsStepTag">Dcache Initialized</span>
        </div>

        <div class="lfs-explanation-box" id="vfsExplanationBox">
          <strong>Interactive VFS Engine:</strong> Walk a file path, resolve mount boundaries (e.g. crossing into a USB FAT32 filesystem), and execute polymorphic function pointers to see how VFS dynamically routes calls.
        </div>

        <div class="lfs-controls">
          <button class="lfs-btn primary" onclick="vfsResolveRoot()">1. Walk Path: /home/user/doc.txt (ext4)</button>
          <button class="lfs-btn" onclick="vfsCrossMountPoint()">2. Cross Mount Boundary: /mnt/usb/data (FAT32)</button>
          <button class="lfs-btn accent" onclick="vfsPolymorphicRead()">3. Invoke read(fd) &rarr; Polymorphic Dispatch</button>
          <button class="lfs-btn" onclick="vfsResetWalkthrough()" style="margin-left: auto;">Reset Simulator</button>
        </div>

        <div class="lfs-segments-grid" id="vfsSegmentsGrid"></div>

        <div class="lfs-status-panel">
          <span id="vfsStatusMsg">VFS Layer active. Ready for path traversal.</span>
          <span id="vfsMetricMsg">Active Driver: None | Dcache State: Cold</span>
        </div>
      </div>
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
    let journalState = "idle";
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

      permanentFsBlocks[0] = { id: "Ino: 2*", state: "checkpointed", label: "Inode Table (Updated)" };
      permanentFsBlocks[1] = { id: "Map: *", state: "checkpointed", label: "Bitmap (Updated)" };

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
        else if (blk.state === "checkpointed") bEl.classList.add("blk-identified-live");

        fsBlocksDiv.appendChild(bEl);
      });
      fsDiv.appendChild(fsBlocksDiv);
      grid.appendChild(fsDiv);
    }

    journalResetWalkthrough();

    // =========================================================
    // 4. WALKTHROUGH PART 4: FTL WEAR-LEVELING & TRIM SIMULATOR
    // =========================================================
    let ftlBlocks = [];
    let ftlHostWrites = 0;
    let ftlFlashWrites = 0;
    let ftlLbaMapping = { 1: null, 2: null };

    function ftlResetWalkthrough() {
      ftlHostWrites = 0;
      ftlFlashWrites = 0;
      ftlLbaMapping = { 1: "B0:P0", 2: "B0:P1" };

      ftlBlocks = [
        {
          id: 0,
          label: "Block 0 (Active)",
          eraseCount: 42,
          pages: [
            { id: "LBA1", state: "valid" },
            { id: "LBA2", state: "valid" },
            { id: "·", state: "erased" },
            { id: "·", state: "erased" }
          ]
        },
        {
          id: 1,
          label: "Block 1 (Cold Data)",
          eraseCount: 3,
          pages: [
            { id: "OS:1", state: "static" },
            { id: "OS:2", state: "static" },
            { id: "OS:3", state: "static" },
            { id: "OS:4", state: "static" }
          ]
        },
        {
          id: 2,
          label: "Block 2 (Free Pool)",
          eraseCount: 41,
          pages: [
            { id: "·", state: "erased" },
            { id: "·", state: "erased" },
            { id: "·", state: "erased" },
            { id: "·", state: "erased" }
          ]
        },
        {
          id: 3,
          label: "Block 3 (Free Pool)",
          eraseCount: 40,
          pages: [
            { id: "·", state: "erased" },
            { id: "·", state: "erased" },
            { id: "·", state: "erased" },
            { id: "·", state: "erased" }
          ]
        }
      ];

      ftlRender();
      document.getElementById("ftlStepTag").textContent = "FTL Initialized";
      document.getElementById("ftlExplanationBox").innerHTML =
        "<strong>Flash Translation Layer (FTL) Ready:</strong> Notice Block 0 holds dynamic data (Erase: 42), while Block 1 holds cold static OS files (Erase: 3). Click <strong>'1. Write LBA (Out-of-Place)'</strong> to overwrite LBA 1 and observe physical page invalidation.";
      document.getElementById("ftlStatusMsg").textContent = "FTL running with page-level mapping.";
      document.getElementById("ftlMetricMsg").textContent = "Host Writes: 0 | Flash Writes: 0 | WAF: 1.00x";
    }

    function ftlWriteLba() {
      ftlHostWrites++;
      ftlFlashWrites++;

      let oldPage = ftlBlocks[0].pages.find(p => p.id === "LBA1" && p.state === "valid");
      if (oldPage) {
        oldPage.state = "invalid";
      }

      let freePage = ftlBlocks[0].pages.find(p => p.state === "erased");
      if (freePage) {
        freePage.id = "LBA1*";
        freePage.state = "valid";
        ftlLbaMapping[1] = "B0:P2";
      }

      ftlRender();
      let waf = (ftlFlashWrites / ftlHostWrites).toFixed(2);
      document.getElementById("ftlStepTag").textContent = "Out-of-Place Write Applied";
      document.getElementById("ftlExplanationBox").innerHTML =
        "<strong>Out-of-Place Programming:</strong> The host updated LBA 1. Because flash cannot overwrite in-place, the FTL wrote to pre-erased Page 2. The old Page 0 is now <s>invalidated dead space</s>. Next, test <strong>'2. Issue OS TRIM'</strong> or <strong>'3. Run Garbage Collection'</strong>!";
      document.getElementById("ftlStatusMsg").textContent = "LBA 1 remapped out-of-place. Old page marked invalid.";
      document.getElementById("ftlMetricMsg").textContent = `Host Writes: ${ftlHostWrites} | Flash Writes: ${ftlFlashWrites} | WAF: ${waf}x`;
    }

    function ftlIssueTrim() {
      let page = ftlBlocks[0].pages.find(p => p.id.startsWith("LBA1") && p.state === "valid");
      if (page) {
        page.state = "invalid";
        ftlLbaMapping[1] = null;
      }

      ftlRender();
      document.getElementById("ftlStepTag").textContent = "TRIM Notification Received";
      document.getElementById("ftlExplanationBox").innerHTML =
        "<strong>OS TRIM Notification Received:</strong> The operating system informed the FTL that LBA 1 was deleted. The FTL immediately marked its physical page as <s>invalid</s>. Now, when Garbage Collection runs, it won't waste time copying this dead data!";
      document.getElementById("ftlStatusMsg").textContent = "TRIM command executed: physical page invalidated before GC.";
    }

    function ftlRunGarbageCollection() {
      let livePages = ftlBlocks[0].pages.filter(p => p.state === "valid");

      livePages.forEach((p, idx) => {
        ftlBlocks[2].pages[idx].id = p.id;
        ftlBlocks[2].pages[idx].state = "valid";
        ftlFlashWrites++;
      });

      ftlBlocks[0].eraseCount++;
      ftlBlocks[0].pages = [
        { id: "·", state: "erased" },
        { id: "·", state: "erased" },
        { id: "·", state: "erased" },
        { id: "·", state: "erased" }
      ];
      ftlBlocks[0].label = "Block 0 (Clean Free Pool)";
      ftlBlocks[2].label = "Block 2 (Active Compacted)";

      ftlRender();
      let waf = (ftlFlashWrites / Math.max(1, ftlHostWrites)).toFixed(2);
      document.getElementById("ftlStepTag").textContent = "Garbage Collection Complete";
      document.getElementById("ftlExplanationBox").innerHTML =
        `<strong>Erase Block Recycled!</strong> Surviving live pages were copied to Block 2, and Block 0 was erased (Erase Count: ${ftlBlocks[0].eraseCount}). Moving live pages caused Flash Writes (${ftlFlashWrites}) to exceed Host Writes (${ftlHostWrites}), yielding a <strong>WAF of ${waf}x</strong>.`;
      document.getElementById("ftlStatusMsg").textContent = `Block 0 bulk-erased with 20V pulse. WAF: ${waf}x.`;
      document.getElementById("ftlMetricMsg").textContent = `Host Writes: ${ftlHostWrites} | Flash Writes: ${ftlFlashWrites} | WAF: ${waf}x`;
    }

    function ftlStaticWearLevel() {
      let coldPages = [...ftlBlocks[1].pages];

      coldPages.forEach((p, idx) => {
        ftlBlocks[0].pages[idx].id = p.id;
        ftlBlocks[0].pages[idx].state = "static";
        ftlFlashWrites++;
      });
      ftlBlocks[0].label = "Block 0 (Static Data Relocated)";

      ftlBlocks[1].eraseCount++;
      ftlBlocks[1].pages = [
        { id: "·", state: "erased" },
        { id: "·", state: "erased" },
        { id: "·", state: "erased" },
        { id: "·", state: "erased" }
      ];
      ftlBlocks[1].label = "Block 1 (Low-Wear Free Pool)";

      ftlRender();
      let waf = (ftlFlashWrites / Math.max(1, ftlHostWrites)).toFixed(2);
      document.getElementById("ftlStepTag").textContent = "Static Wear-Leveling Executed";
      document.getElementById("ftlExplanationBox").innerHTML =
        "<strong>Static Wear-Leveling in Action:</strong> The FTL noticed Block 1 had only 3 erases because its OS data was static. It relocated the static data to heavily-worn Block 0, freeing low-wear Block 1 to absorb hot writes. This prevents localized cell burnout and prolongs SSD life!";
      document.getElementById("ftlStatusMsg").textContent = "Cold data swapped to worn block; fresh low-wear block recycled.";
      document.getElementById("ftlMetricMsg").textContent = `Host Writes: ${ftlHostWrites} | Flash Writes: ${ftlFlashWrites} | WAF: ${waf}x`;
    }

    function ftlRender() {
      const grid = document.getElementById("ftlSegmentsGrid");
      grid.innerHTML = "";

      ftlBlocks.forEach(blk => {
        let bDiv = document.createElement("div");
        bDiv.className = "lfs-segment-box";
        bDiv.innerHTML = `<div class="lfs-seg-header"><span>${blk.label}</span><span>Erases: ${blk.eraseCount}</span></div>`;

        let pagesDiv = document.createElement("div");
        pagesDiv.className = "lfs-seg-blocks";
        pagesDiv.style.gridTemplateColumns = "repeat(2, 1fr)";

        blk.pages.forEach(p => {
          let pEl = document.createElement("div");
          pEl.className = "lfs-block";
          pEl.textContent = p.id;

          if (p.state === "erased") pEl.classList.add("blk-flash-erased");
          else if (p.state === "valid") pEl.classList.add("blk-flash-valid");
          else if (p.state === "invalid") pEl.classList.add("blk-flash-invalid");
          else if (p.state === "static") pEl.classList.add("blk-flash-static");

          pagesDiv.appendChild(pEl);
        });

        bDiv.appendChild(pagesDiv);
        grid.appendChild(bDiv);
      });
    }

    ftlResetWalkthrough();

    // =========================================================
    // 5. WALKTHROUGH PART 5: VFS DISPATCH & PATH WALK
    // =========================================================
    let vfsState = {
      path: "/",
      dentries: ["/"],
      driver: "ext4",
      activeInode: "ino: 2 (root)",
      activeFop: "ext4_file_operations"
    };

    function vfsResetWalkthrough() {
      vfsState = {
        path: "/",
        dentries: ["/"],
        driver: "ext4",
        activeInode: "ino: 2 (root)",
        activeFop: "ext4_file_operations"
      };
      vfsRender();
      document.getElementById("vfsStepTag").textContent = "Dcache Initialized (Root)";
      document.getElementById("vfsExplanationBox").innerHTML =
        "<strong>Virtual File System Initialized:</strong> The root dentry <code>/</code> maps to ext4 root inode 2. Click <strong>'1. Walk Path: /home/user/doc.txt'</strong> to trace path resolution through the Dcache.";
      document.getElementById("vfsStatusMsg").textContent = "VFS root established. Ready for path traversal.";
      document.getElementById("vfsMetricMsg").textContent = "Active Driver: ext4 | Dcache State: Cold (Root only)";
    }

    function vfsResolveRoot() {
      vfsState = {
        path: "/home/user/doc.txt",
        dentries: ["/", "home", "user", "doc.txt"],
        driver: "ext4",
        activeInode: "ino: 84201 (regular file)",
        activeFop: "ext4_file_operations"
      };
      vfsRender();
      document.getElementById("vfsStepTag").textContent = "Path Walk Complete: ext4";
      document.getElementById("vfsExplanationBox").innerHTML =
        "<strong>Path Walk Resolved via Dcache:</strong> The VFS hashed path components and traversed dentries: <code>/ &rarr; home &rarr; user &rarr; doc.txt</code>. It matched inode 84201 on ext4. An open file descriptor table slot was created. Next, test <strong>'2. Cross Mount Boundary'</strong> or <strong>'3. Invoke read(fd)'</strong>!";
      document.getElementById("vfsStatusMsg").textContent = "Path /home/user/doc.txt resolved. ext4 f_op registered.";
      document.getElementById("vfsMetricMsg").textContent = "Active Driver: ext4 | Dcache State: 4 Dentries Cached";
    }

    function vfsCrossMountPoint() {
      vfsState = {
        path: "/mnt/usb/data.bin",
        dentries: ["/", "mnt", "usb (MOUNT)", "data.bin"],
        driver: "vfat (FAT32)",
        activeInode: "ino: 14002 (FAT cluster 12)",
        activeFop: "fat_file_operations"
      };
      vfsRender();
      document.getElementById("vfsStepTag").textContent = "Mount Boundary Crossed!";
      document.getElementById("vfsExplanationBox").innerHTML =
        "<strong>Mount Point Traversal Detected:</strong> When the VFS path walk hit <code>/mnt/usb</code>, it saw the <code>DCACHE_MOUNTED</code> flag. The VFS seamlessly redirected lookup from the root ext4 filesystem to the <strong>FAT32 Superblock</strong>! Inode and file operations dynamically switched to <code>fat_file_operations</code> without changing the user API.";
      document.getElementById("vfsStatusMsg").textContent = "Mount boundary crossed: ext4 &rarr; FAT32. Polymorphic f_op switched.";
      document.getElementById("vfsMetricMsg").textContent = "Active Driver: vfat | Dcache State: Cross-Mount Validated";
    }

    function vfsPolymorphicRead() {
      let driverName = vfsState.driver;
      let funcName = driverName.includes("vfat") ? "fat_file_read_iter()" : "ext4_file_read_iter()";

      document.getElementById("vfsStepTag").textContent = "Polymorphic Call Dispatched!";
      document.getElementById("vfsExplanationBox").innerHTML =
        `<strong>Polymorphic Dispatch Executed:</strong> Process called <code>read(fd=3, buf, 4096)</code>. The VFS extracted <code>file = current->files->fd[3]</code> and executed <code>file->f_op->read()</code>, which dispatched directly into <strong>${funcName}</strong>! The user application code remains identical regardless of underlying media.`;
      document.getElementById("vfsStatusMsg").textContent = `read() dispatched to ${funcName}. Buffer returned.`;
      document.getElementById("vfsMetricMsg").textContent = `Active Driver: ${driverName} | Function: ${funcName}`;
    }

    function vfsRender() {
      const grid = document.getElementById("vfsSegmentsGrid");
      grid.innerHTML = "";

      let b1 = document.createElement("div");
      b1.className = "lfs-segment-box";
      b1.innerHTML = `<div class="lfs-seg-header"><span>Process File Table</span><span>fd=3</span></div>`;
      let b1Content = document.createElement("div");
      b1Content.className = "lfs-seg-blocks";
      b1Content.style.gridTemplateColumns = "1fr";
      let b1El = document.createElement("div");
      b1El.className = "lfs-block blk-vfs-fd";
      b1El.style.aspectRatio = "auto";
      b1El.style.padding = "6px";
      b1El.textContent = `fd[3] -> ${vfsState.path}`;
      b1Content.appendChild(b1El);
      b1.appendChild(b1Content);
      grid.appendChild(b1);

      let b2 = document.createElement("div");
      b2.className = "lfs-segment-box";
      b2.innerHTML = `<div class="lfs-seg-header"><span>Dcache Path Chain</span><span>Dentries</span></div>`;
      let b2Content = document.createElement("div");
      b2Content.className = "lfs-seg-blocks";
      b2Content.style.gridTemplateColumns = "repeat(4, 1fr)";
      vfsState.dentries.forEach(d => {
        let dEl = document.createElement("div");
        dEl.className = "lfs-block blk-vfs-dentry";
        dEl.textContent = d;
        b2Content.appendChild(dEl);
      });
      b2.appendChild(b2Content);
      grid.appendChild(b2);

      let b3 = document.createElement("div");
      b3.className = "lfs-segment-box";
      b3.innerHTML = `<div class="lfs-seg-header"><span>Active Inode</span><span>${vfsState.driver}</span></div>`;
      let b3Content = document.createElement("div");
      b3Content.className = "lfs-seg-blocks";
      b3Content.style.gridTemplateColumns = "1fr";
      let b3El = document.createElement("div");
      b3El.className = "lfs-block blk-vfs-inode";
      b3El.style.aspectRatio = "auto";
      b3El.style.padding = "6px";
      b3El.textContent = vfsState.activeInode;
      b3Content.appendChild(b3El);
      b3.appendChild(b3Content);
      grid.appendChild(b3);

      let b4 = document.createElement("div");
      b4.className = "lfs-segment-box";
      b4.innerHTML = `<div class="lfs-seg-header"><span>File Operations (f_op)</span><span>Function Table</span></div>`;
      let b4Content = document.createElement("div");
      b4Content.className = "lfs-seg-blocks";
      b4Content.style.gridTemplateColumns = "1fr";
      let b4El = document.createElement("div");
      b4El.className = "lfs-block blk-vfs-file";
      b4El.style.aspectRatio = "auto";
      b4El.style.padding = "6px";
      b4El.textContent = vfsState.activeFop;
      b4Content.appendChild(b4El);
      b4.appendChild(b4Content);
      grid.appendChild(b4);
    }

    vfsResetWalkthrough();

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

    print(f"--> Writing deepened WAL & expanded VFS content to {html_file}...")
    os.makedirs(os.path.dirname(html_file), exist_ok=True)
    final_content = HTML_CONTENT.replace("AUDIO_DATA_URI_PLACEHOLDER", data_uri)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(final_content)
    print("--> HTML structure successfully written!")

    commit_msg = (
        "Deepen WAL theory, failure modes, and commit barriers in section 4.3.6\n\n"
        "Update week10-file-management/03-filesystem-implementation.html to "
        "comprehensively explain Write-Ahead Logging (WAL), physical write barriers, "
        "the anatomy of crash consistency failure modes, and commit block invariants."
    )

    execute_git_command(["git", "add", html_file], "Staging HTML file")
    execute_git_command(["git", "commit", "-am", commit_msg], "Committing changes")
    execute_git_command(["git", "push", "origin", "main"], "Pushing changes to origin")
    print("--> Deployment complete!")

if __name__ == "__main__":
    execute_deployment()
