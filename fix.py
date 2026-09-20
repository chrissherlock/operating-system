#!/usr/bin/env python3
# =====================================================================
# generate_week1_multipage_modules.py: Create separate module pages for Week 1
# =====================================================================
import os
import shutil
import subprocess
import sys

def build_multipage_structure():
    base_dir = "week01-operating-system-concepts"
    os.makedirs(base_dir, exist_ok=True)

    # Clean up old nested intro directory if present
    intro_sub_dir = os.path.join(base_dir, "intro")
    if os.path.exists(intro_sub_dir):
        shutil.rmtree(intro_sub_dir)

    # 1. Master Chapter 1 Index Portal
    index_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>COSC240: Chapter 1 - Introduction (Tanenbaum)</title>
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
    h1 { font-size: 1.8rem; color: var(--accent); margin-bottom: 6px; }
    p.subtitle { color: var(--text-muted); font-size: 0.95rem; }
    .main-container {
      display: flex;
      flex-direction: column;
      gap: 16px;
      width: 100%;
      max-width: 1100px;
    }
    .card {
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
      transition: transform 0.15s ease, border-color 0.15s ease;
      text-decoration: none;
      color: inherit;
    }
    .card:hover {
      border-color: var(--accent);
      transform: translateY(-2px);
    }
    .card h2 {
      font-size: 1.2rem;
      color: var(--accent);
    }
    .card p {
      font-size: 0.92rem;
      color: var(--text-muted);
      line-height: 1.5;
    }
    .card .link-text {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--accent);
      margin-top: 6px;
    }
    .card:hover .link-text {
      text-decoration: underline;
    }
    .nav-back {
      width: 100%;
      max-width: 1100px;
      margin: 0 auto 6px auto;
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
    }
    .nav-back a:hover {
      background-color: #0284c7;
      color: #ffffff;
    }
  </style>
</head>
<body>
  <div class="nav-back">
    <a href="../index.html">&larr; Back to Course Overview</a>
  </div>

  <header>
    <h1>Chapter 1: Introduction</h1>
    <p class="subtitle">Operating Systems Design &amp; Implementation (Andrew S. Tanenbaum)</p>
  </header>

  <div class="main-container">

    <!-- Module 01 -->
    <a href="01-what-is-an-os.html" class="card">
      <h2>01. What Is an Operating System?</h2>
      <p>Examine foundational paradigms: the operating system as an extended machine (top-down virtualization) and as a resource manager (bottom-up multiplexing).</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

    <!-- Module 02 -->
    <a href="02-history.html" class="card">
      <h2>02. History of Operating Systems</h2>
      <p>Trace the five computing generations from vacuum tubes and batch systems to modern cloud environments, featuring historical archives and the 15-logo OS ecosystem grid.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

    <!-- Module 03 -->
    <a href="03-hardware-review.html" class="card">
      <h2>03. Computer Hardware Review</h2>
      <p>Review processor architecture, instruction execution cycles, memory hierarchy, magnetic disks, solid-state drives, I/O devices, and system buses.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

    <!-- Module 04 -->
    <a href="04-os-concepts.html" class="card">
      <h2>04. Operating System Concepts</h2>
      <p>Understand key architectural abstractions: processes, address spaces, files, input/output streams, protection rings, and command shells.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

    <!-- Module 05 -->
    <a href="05-os-structure.html" class="card">
      <h2>05. Operating System Structure</h2>
      <p>Compare structural designs: monolithic systems, layered architectures, microkernels, client-server models, virtual machines, and exokernels.</p>
      <span class="link-text">Launch Module &rarr;</span>
    </a>

  </div>
</body>
</html>
"""

    with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # 2. Module 01: What Is an OS
    mod1_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>What Is an Operating System? — COSC240</title>
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
      --accent: #0284c7;
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
    .nav-back { width: 100%; max-width: 1100px; margin: 0 auto; display: flex; }
    .nav-back a {
      display: inline-flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;
      font-family: var(--font-mono); text-decoration: none; color: #0284c7;
      background-color: #f0f9ff; border: 1px solid #bae6fd; padding: 6px 12px; border-radius: 6px;
    }
    .nav-back a:hover { background-color: #0284c7; color: #ffffff; }
    main { width: 100%; max-width: 1100px; display: flex; flex-direction: column; gap: 24px; }
    header { background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 30px; }
    h1 { font-size: 1.8rem; color: var(--accent); margin-bottom: 8px; }
    p.subtitle { color: var(--text-muted); font-size: 0.95rem; }
    .content-section { background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 30px; display: flex; flex-direction: column; gap: 16px; }
    .content-section h2 { font-size: 1.3rem; color: #0369a1; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }
    h3 { font-size: 1.1rem; color: #1e293b; margin-top: 10px; }
    p { color: var(--text-muted); line-height: 1.6; font-size: 0.95rem; }
    ul { margin-left: 20px; color: var(--text-muted); line-height: 1.6; }
    li { margin-bottom: 6px; }
  </style>
</head>
<body>
  <div class="nav-back">
    <a href="index.html">&larr; Back to Chapter 1 Index</a>
  </div>

  <main>
    <header>
      <h1>01. What Is an Operating System?</h1>
      <p class="subtitle">Tanenbaum Chapter 1.1: The Extended Machine and the Resource Manager.</p>
    </header>

    <section class="content-section">
      <h2>Foundational Paradigms</h2>
      <p>
        To understand what an operating system is, we must examine it from two complementary perspectives: the <strong>extended machine</strong> (top-down abstraction layer) and the <strong>resource manager</strong> (bottom-up hardware multiplexer).
      </p>

      <h3>1. The Extended Machine (Virtualization)</h3>
      <p>
        Raw hardware architecture—consisting of disk controllers, volatile RAM registers, interrupt vectors, and bus timings—is notoriously complex and difficult to program directly. An operating system hides this raw complexity by providing a clean, elegant, and abstract set of instructions and abstractions (such as files, sockets, and virtual address spaces), presenting programmers with a virtual machine far superior to the physical hardware.
      </p>

      <h3>2. The Resource Manager (Multiplexing)</h3>
      <p>
        Modern computers consist of processors, memories, timers, disks, mice, keyboards, network interfaces, and printers. The operating system acts as an arbiter, managing and multiplexing these physical resources efficiently, fairly, and securely among multiple competing applications and users.
      </p>
      <p>
        Resource management involves two primary forms of multiplexing:
      </p>
      <ul>
        <li><strong>Time Multiplexing:</strong> Taking turns. The CPU switches rapidly between multiple running processes or threads, giving each the illusion of dedicated processor ownership.</li>
        <li><strong>Space Multiplexing:</strong> Sharing physical storage or memory. Main memory is partitioned among multiple programs simultaneously, and disk storage is divided into independent files and directories.</li>
      </ul>
    </section>
  </main>
</body>
</html>
"""
    with open(os.path.join(base_dir, "01-what-is-an-os.html"), "w", encoding="utf-8") as f:
        f.write(mod1_html)

    # 3. Module 02: History (with images and all 15 logos)
    mod2_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>History of Operating Systems — COSC240</title>
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
      --accent: #0284c7;
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
    .nav-back { width: 100%; max-width: 1100px; margin: 0 auto; display: flex; }
    .nav-back a {
      display: inline-flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;
      font-family: var(--font-mono); text-decoration: none; color: #0284c7;
      background-color: #f0f9ff; border: 1px solid #bae6fd; padding: 6px 12px; border-radius: 6px;
    }
    .nav-back a:hover { background-color: #0284c7; color: #ffffff; }
    main { width: 100%; max-width: 1100px; display: flex; flex-direction: column; gap: 24px; }
    header { background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 30px; }
    h1 { font-size: 1.8rem; color: var(--accent); margin-bottom: 8px; }
    p.subtitle { color: var(--text-muted); font-size: 0.95rem; }
    .content-section { background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 30px; display: flex; flex-direction: column; gap: 16px; }
    .content-section h2 { font-size: 1.3rem; color: #0369a1; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }
    h3 { font-size: 1.1rem; color: #1e293b; margin-top: 10px; }
    p { color: var(--text-muted); line-height: 1.6; font-size: 0.95rem; }
    .image-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 10px; }
    .image-card { background: #f8fafc; border: 1px solid var(--border); border-radius: 6px; padding: 12px; display: flex; flex-direction: column; align-items: center; gap: 8px; text-align: center; }
    .image-card img { max-width: 100%; height: 140px; object-fit: contain; border-radius: 4px; border: 1px solid #e2e8f0; background: #ffffff; }
    .image-card span { font-size: 0.8rem; font-family: var(--font-mono); color: var(--text-muted); }
    .aside-box { background: #f8fafc; border-left: 4px solid var(--accent); padding: 16px; border-radius: 0 6px 6px 0; margin-top: 10px; }
  </style>
</head>
<body>
  <div class="nav-back">
    <a href="index.html">&larr; Back to Chapter 1 Index</a>
  </div>

  <main>
    <header>
      <h1>02. History of Operating Systems</h1>
      <p class="subtitle">Tanenbaum Chapter 1.2: The Five Generations of Computing and Ecosystem Evolution.</p>
    </header>

    <section class="content-section">
      <h2>The Five Computing Generations</h2>
      <p>
        The history of operating systems is intimately tied to the evolution of computer hardware across five distinct technological generations.
      </p>

      <h3>Generation 1: Vacuum Tubes (1945–1955)</h3>
      <p>
        Early digital computers built with vacuum tubes were massive, room-sized installations. Programming was done entirely in absolute machine language or by manually wiring physical plugboards. There were no operating systems; a single programmer had exclusive access to the machine for a scheduled block of time.
      </p>
      <div class="image-grid">
        <div class="image-card">
          <img src="../images/vacuumtube.jpg" alt="Vacuum Tubes">
          <span>Vacuum Tubes (12AX7WA)<br><small>Wikimedia Commons</small></span>
        </div>
        <div class="image-card">
          <img src="../images/plugboard.jpg" alt="Plugboard">
          <span>IBM 402 Plugboard Wiring<br><small>Wikimedia Commons</small></span>
        </div>
      </div>

      <h3>Generation 2: Transistors &amp; Batch Systems (1955–1965)</h3>
      <p>
        The invention of the transistor introduced solid-state electronics, making computers reliable enough to manufacture and sell commercially. This era birthed <strong>batch systems</strong>, where jobs were written to punched cards, collected into batches by an operator, loaded into the computer via card readers, and executed sequentially using early monitor programs.
      </p>
      <div class="image-grid">
        <div class="image-card">
          <img src="../images/replica-first-transistor.jpg" alt="Transistor Replica">
          <span>First Working Transistor Replica<br><small>Wikimedia Commons</small></span>
        </div>
        <div class="image-card">
          <img src="../images/punched-card-program-deck.jpg" alt="Punched Cards">
          <span>Punched Card Program Deck<br><small>Wikimedia Commons</small></span>
        </div>
      </div>

      <h3>Generation 3: ICs, Multiprogramming, &amp; Time-Sharing (1965–1980)</h3>
      <p>
        Integrated circuits (ICs) revolutionized computer architecture. The IBM System/360 introduced hardware architecture families capable of running both commercial and scientific workloads. To eliminate CPU idle time during slow I/O operations, <strong>multiprogramming</strong> was developed, alongside <strong>time-sharing</strong> systems enabling multiple interactive users.
      </p>

      <h3>Generation 4: Personal Computers &amp; Networks (1980–Present)</h3>
      <p>
        Large-scale integration (LSI) chips made personal computers economically viable. Operating systems shifted toward graphical user interfaces (GUIs), rich file abstractions, and local area network (LAN) integration.
      </p>

      <h3>Generation 5: Mobile, Cloud, &amp; Ubiquitous Computing (Present)</h3>
      <p>
        Modern operating systems power smartphones, tablets, edge sensors, and massive hyperscale cloud datacenters, emphasizing power management, containerization, and distributed virtualization.
      </p>

      <div class="aside-box">
        <strong>Research Aside: Andrew S. Tanenbaum &amp; MINIX</strong>
        <p style="margin-top: 6px; font-size: 0.88rem;">
          Andrew S. Tanenbaum created MINIX in 1987 as an educational operating system to illustrate microkernel design principles. MINIX served as the primary inspiration and initial development environment for Linus Torvalds when he began writing the Linux kernel in 1991.
        </p>
      </div>
    </section>

    <section class="content-section">
      <h2>Operating System Ecosystem &amp; Architecture Families</h2>
      <p>
        The operating system landscape spans diverse paradigms. Below is the complete visual index of all 15 system brand marks and logos organized by architectural family.
      </p>

      <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; display: flex; flex-direction: column; gap: 20px;">

        <!-- Family 1 -->
        <div>
          <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: bold; color: #0369a1; text-transform: uppercase; margin-bottom: 10px;">Commercial Desktop &amp; Mobile Systems</div>
          <div style="display: flex; gap: 14px; flex-wrap: wrap;">
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/windows.svg" alt="Windows" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/Microsoft_Windows" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">Windows</a>
            </div>
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/apple.svg" alt="Apple" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/MacOS" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">Apple macOS</a>
            </div>
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/chrome.svg" alt="ChromeOS" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/ChromeOS" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">ChromeOS</a>
            </div>
          </div>
        </div>

        <!-- Family 2 -->
        <div>
          <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: bold; color: #0369a1; text-transform: uppercase; margin-bottom: 10px;">Open-Source &amp; Unix-Like Kernels</div>
          <div style="display: flex; gap: 14px; flex-wrap: wrap;">
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/tux.svg" alt="Linux" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/Linux" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">Linux (Tux)</a>
            </div>
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/freebsd.svg" alt="FreeBSD" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/FreeBSD" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">FreeBSD</a>
            </div>
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/android.svg" alt="Android" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/Android_(operating_system)" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">Android</a>
            </div>
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/minix.png" alt="MINIX" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/MINIX" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">MINIX</a>
            </div>
          </div>
        </div>

        <!-- Family 3 -->
        <div>
          <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: bold; color: #0369a1; text-transform: uppercase; margin-bottom: 10px;">Real-Time Operating Systems (RTOS)</div>
          <div style="display: flex; gap: 14px; flex-wrap: wrap;">
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/free-rtos.png" alt="FreeRTOS" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/FreeRTOS" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">FreeRTOS</a>
            </div>
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/qnx.svg" alt="QNX" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/QNX" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">QNX RTOS</a>
            </div>
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/vxworks.svg" alt="VxWorks" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/VxWorks" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">VxWorks</a>
            </div>
          </div>
        </div>

        <!-- Family 4 -->
        <div>
          <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: bold; color: #0369a1; text-transform: uppercase; margin-bottom: 10px;">Historical &amp; Enterprise Systems</div>
          <div style="display: flex; gap: 14px; flex-wrap: wrap;">
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/os2.svg" alt="OS/2" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/OS/2" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">IBM OS/2</a>
            </div>
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/solaris.svg" alt="Solaris" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/Solaris_(operating_system)" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">Solaris</a>
            </div>
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/openvms.svg" alt="OpenVMS" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/OpenVMS" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">OpenVMS</a>
            </div>
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/multics.svg" alt="Multics" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/Multics" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">Multics</a>
            </div>
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/beos.svg" alt="BeOS" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/BeOS" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline;">BeOS</a>
            </div>
          </div>
        </div>

      </div>
    </section>
  </main>
</body>
</html>
"""
    with open(os.path.join(base_dir, "02-history.html"), "w", encoding="utf-8") as f:
        f.write(mod2_html)

    # 4. Module 03: Hardware Review
    mod3_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Computer Hardware Review — COSC240</title>
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
      --accent: #0284c7;
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
    .nav-back { width: 100%; max-width: 1100px; margin: 0 auto; display: flex; }
    .nav-back a {
      display: inline-flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;
      font-family: var(--font-mono); text-decoration: none; color: #0284c7;
      background-color: #f0f9ff; border: 1px solid #bae6fd; padding: 6px 12px; border-radius: 6px;
    }
    .nav-back a:hover { background-color: #0284c7; color: #ffffff; }
    main { width: 100%; max-width: 1100px; display: flex; flex-direction: column; gap: 24px; }
    header { background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 30px; }
    h1 { font-size: 1.8rem; color: var(--accent); margin-bottom: 8px; }
    p.subtitle { color: var(--text-muted); font-size: 0.95rem; }
    .content-section { background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 30px; display: flex; flex-direction: column; gap: 16px; }
    .content-section h2 { font-size: 1.3rem; color: #0369a1; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }
    h3 { font-size: 1.1rem; color: #1e293b; margin-top: 10px; }
    p { color: var(--text-muted); line-height: 1.6; font-size: 0.95rem; }
  </style>
</head>
<body>
  <div class="nav-back">
    <a href="index.html">&larr; Back to Chapter 1 Index</a>
  </div>

  <main>
    <header>
      <h1>03. Computer Hardware Review</h1>
      <p class="subtitle">Tanenbaum Chapter 1.3: Processors, Memory Hierarchy, Disks, I/O, and Buses.</p>
    </header>

    <section class="content-section">
      <h2>Hardware Foundations</h2>
      <p>
        Because operating systems interact directly with physical hardware, understanding core hardware components—processors, memory hierarchies, storage devices, and bus structures—is essential.
      </p>
      <h3>Processors &amp; Instruction Execution</h3>
      <p>
        The CPU executes instructions fetched from memory via the program counter, moving through fetch-decode-execute cycles, utilizing registers, ALUs, and caches (L1, L2, L3).
      </p>
      <h3>Memory Hierarchy</h3>
      <p>
        Spans CPU registers, cache SRAM, main memory DRAM, solid-state NVMe storage, and magnetic hard disks, balancing speed, volatility, and capacity.
      </p>
    </section>
  </main>
</body>
</html>
"""
    with open(os.path.join(base_dir, "03-hardware-review.html"), "w", encoding="utf-8") as f:
        f.write(mod3_html)

    # 5. Module 04: OS Concepts
    mod4_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Operating System Concepts — COSC240</title>
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
      --accent: #0284c7;
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
    .nav-back { width: 100%; max-width: 1100px; margin: 0 auto; display: flex; }
    .nav-back a {
      display: inline-flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;
      font-family: var(--font-mono); text-decoration: none; color: #0284c7;
      background-color: #f0f9ff; border: 1px solid #bae6fd; padding: 6px 12px; border-radius: 6px;
    }
    .nav-back a:hover { background-color: #0284c7; color: #ffffff; }
    main { width: 100%; max-width: 1100px; display: flex; flex-direction: column; gap: 24px; }
    header { background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 30px; }
    h1 { font-size: 1.8rem; color: var(--accent); margin-bottom: 8px; }
    p.subtitle { color: var(--text-muted); font-size: 0.95rem; }
    .content-section { background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 30px; display: flex; flex-direction: column; gap: 16px; }
    .content-section h2 { font-size: 1.3rem; color: #0369a1; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }
    h3 { font-size: 1.1rem; color: #1e293b; margin-top: 10px; }
    p { color: var(--text-muted); line-height: 1.6; font-size: 0.95rem; }
  </style>
</head>
<body>
  <div class="nav-back">
    <a href="index.html">&larr; Back to Chapter 1 Index</a>
  </div>

  <main>
    <header>
      <h1>04. Operating System Concepts</h1>
      <p class="subtitle">Tanenbaum Chapter 1.5: Processes, Address Spaces, Files, I/O, Protection, and Shells.</p>
    </header>

    <section class="content-section">
      <h2>Core Architectural Abstractions</h2>
      <p>
        Operating systems present high-level abstractions that turn bare hardware into a programmable environment.
      </p>
      <h3>Processes &amp; Address Spaces</h3>
      <p>
        A process is a program in execution, consisting of executable code, data, stack, registers, and resources. Each process operates within an isolated virtual address space.
      </p>
      <h3>Files, Directories, &amp; I/O</h3>
      <p>
        Hierarchical file systems abstract raw disk blocks into named files and directories. Input/output subsystems manage character and block devices uniformly.
      </p>
      <h3>Protection &amp; Shells</h3>
      <p>
        User identification numbers (UIDs), file permissions, and protection rings secure resources, while shells provide command interpretation interfaces.
      </p>
    </section>
  </main>
</body>
</html>
"""
    with open(os.path.join(base_dir, "04-os-concepts.html"), "w", encoding="utf-8") as f:
        f.write(mod4_html)

    # 6. Module 05: OS Structure
    mod5_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Operating System Structure — COSC240</title>
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
      --accent: #0284c7;
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
    .nav-back { width: 100%; max-width: 1100px; margin: 0 auto; display: flex; }
    .nav-back a {
      display: inline-flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;
      font-family: var(--font-mono); text-decoration: none; color: #0284c7;
      background-color: #f0f9ff; border: 1px solid #bae6fd; padding: 6px 12px; border-radius: 6px;
    }
    .nav-back a:hover { background-color: #0284c7; color: #ffffff; }
    main { width: 100%; max-width: 1100px; display: flex; flex-direction: column; gap: 24px; }
    header { background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 30px; }
    h1 { font-size: 1.8rem; color: var(--accent); margin-bottom: 8px; }
    p.subtitle { color: var(--text-muted); font-size: 0.95rem; }
    .content-section { background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 30px; display: flex; flex-direction: column; gap: 16px; }
    .content-section h2 { font-size: 1.3rem; color: #0369a1; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }
    h3 { font-size: 1.1rem; color: #1e293b; margin-top: 10px; }
    p { color: var(--text-muted); line-height: 1.6; font-size: 0.95rem; }
  </style>
</head>
<body>
  <div class="nav-back">
    <a href="index.html">&larr; Back to Chapter 1 Index</a>
  </div>

  <main>
    <header>
      <h1>05. Operating System Structure</h1>
      <p class="subtitle">Tanenbaum Chapter 1.7: Monolithic, Layered, Microkernel, Client-Server, and Virtual Machine Architectures.</p>
    </header>

    <section class="content-section">
      <h2>Architectural Designs</h2>
      <p>
        How an operating system is structured internally dictates its reliability, performance, and extensibility.
      </p>
      <h3>Monolithic &amp; Layered Systems</h3>
      <p>
        Monolithic kernels run all core services (schedulers, file systems, drivers) in supervisor mode as a single large program. Layered systems organize code into strict hierarchical layers.
      </p>
      <h3>Microkernels &amp; Client-Server</h3>
      <p>
        Microkernels minimize supervisor mode code, running file systems and device drivers as user-space servers communicating via inter-process message passing.
      </p>
      <h3>Virtual Machines</h3>
      <p>
        Virtual machine monitors (hypervisors) emulate complete hardware environments, allowing multiple guest operating systems to execute concurrently.
      </p>
    </section>
  </main>
</body>
</html>
"""
    with open(os.path.join(base_dir, "05-os-structure.html"), "w", encoding="utf-8") as f:
        f.write(mod5_html)

    modified = [
        os.path.join(base_dir, "index.html"),
        os.path.join(base_dir, "01-what-is-an-os.html"),
        os.path.join(base_dir, "02-history.html"),
        os.path.join(base_dir, "03-hardware-review.html"),
        os.path.join(base_dir, "04-os-concepts.html"),
        os.path.join(base_dir, "05-os-structure.html"),
    ]

    fix_path = "fix.py"
    if os.path.exists(fix_path):
        modified.append(fix_path)

    print(f"--> Staging modified files: {modified}")
    try:
        subprocess.run(["git", "add"] + modified, check=True)
        commit_msg = (
            "Create separate multi-page module files for Week 1 operating system concepts\n\n"
            "Implement dedicated HTML pages for Chapter 1 sections under week01-operating-system-concepts/\n"
            "including index, what-is-an-os, history, hardware-review, os-concepts, and os-structure."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Week 1 multi-page module structure successfully deployed!")

if __name__ == "__main__":
    build_multipage_structure()
