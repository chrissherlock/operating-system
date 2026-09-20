#!/usr/bin/env python3
# =====================================================================
# fix.py: Strip card containers from main text and git sync
# =====================================================================
import os
import subprocess

def overhaul_page_layout():
    target_dir = "week01-operating-system-concepts"
    file_name = "02-hardware-review.html"
    file_path = os.path.join(target_dir, file_name)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>02. Computer Hardware Review -- COSC240</title>
  <style id="module-nav-styles">
    .module-nav-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      max-width: 1000px;
      margin: 0 auto 20px auto;
      gap: 12px;
      box-sizing: border-box;
    }
    .module-nav-bar.bottom {
      margin-top: 36px;
      margin-bottom: 36px;
    }
    .module-nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      text-decoration: none;
      color: #0284c7;
      background-color: #f0f9ff;
      border: 1px solid #bae6fd;
      padding: 7px 13px;
      border-radius: 6px;
      transition: all 0.15s ease;
    }
    .module-nav-btn:hover {
      background-color: #0284c7;
      color: #ffffff;
    }
    .module-nav-placeholder {
      visibility: hidden;
      padding: 7px 13px;
      font-size: 0.85rem;
    }
  </style>
  <style>
    :root {
      --bg: #ffffff;
      --border: #e2e8f0;
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --text: #0f172a;
      --text-muted: #334155;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      padding: 32px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      line-height: 1.65;
    }
    main {
      width: 100%;
      max-width: 1000px;
      display: flex;
      flex-direction: column;
      gap: 28px;
    }
    header {
      border-bottom: 2px solid var(--border);
      padding-bottom: 20px;
      margin-bottom: 8px;
    }
    h1 {
      font-size: 2.1rem;
      color: var(--text);
      margin-bottom: 6px;
      letter-spacing: -0.02em;
    }
    p.subtitle {
      color: #64748b;
      font-size: 1.05rem;
    }
    h2 {
      font-size: 1.45rem;
      color: #0f172a;
      margin-top: 20px;
      margin-bottom: 8px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 8px;
      letter-spacing: -0.01em;
    }
    h3 {
      font-size: 1.15rem;
      color: #1e293b;
      margin-top: 14px;
      margin-bottom: 6px;
    }
    p {
      color: var(--text-muted);
      font-size: 1rem;
      margin-bottom: 12px;
    }
    ul, ol {
      margin-left: 24px;
      color: var(--text-muted);
      margin-bottom: 16px;
    }
    li {
      margin-bottom: 8px;
    }
    code {
      font-family: var(--font-mono);
      font-size: 0.88rem;
      background-color: #f1f5f9;
      padding: 2px 6px;
      border-radius: 4px;
      color: #0369a1;
    }
    .diagram-container {
      display: flex;
      justify-content: center;
      margin: 28px 0;
      width: 100%;
      overflow-x: auto;
    }
    .aside-note {
      background: #f8fafc;
      border-left: 4px solid var(--accent);
      padding: 16px 20px;
      border-radius: 0 6px 6px 0;
      margin: 18px 0;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      font-size: 0.92rem;
    }
    th, td {
      border: 1px solid var(--border);
      padding: 10px 14px;
      text-align: left;
    }
    th {
      background-color: #f8fafc;
      color: #0f172a;
      font-weight: 600;
    }
  </style>
</head>
<body>

  <nav class="module-nav-bar">
    <a href="01-what-is-an-os-and-history.html" class="module-nav-btn">&larr; Previous: 01. What Is an Operating System &amp; History</a>
    <a href="index.html" class="module-nav-btn">Week Index</a>
    <a href="03-os-concepts.html" class="module-nav-btn">Next: 03. OS Concepts &rarr;</a>
  </nav>

  <main>
    <header>
      <h1>02. Computer Hardware Review</h1>
      <p class="subtitle">Tanenbaum Chapter 1.3: Processors, Memory Hierarchy, Disks, I/O Devices, Buses, and Booting.</p>
    </header>

    <article>
      <h2>1. Processors (CPUs) &amp; Execution Mechanics</h2>
      <p>
        The Central Processing Unit (CPU) is the computational engine of the computer, executing instructions fetched from main memory. The operation of the CPU follows the classical <strong>fetch-decode-execute cycle</strong>:
      </p>
      <ul>
        <li><strong>Fetch:</strong> The CPU retrieves the instruction at the physical memory address currently held in the Program Counter (PC).</li>
        <li><strong>Decode:</strong> The instruction decoder interprets the operation code (opcode) to determine the operation type and identify required source and destination operands.</li>
        <li><strong>Execute:</strong> The Arithmetic Logic Unit (ALU) performs the computation, manipulates internal registers, and updates status flags.</li>
      </ul>

      <h3>Key Processor Registers</h3>
      <p>
        Processors contain internal registers that operate at CPU clock speeds with zero wait states:
      </p>
      <ul>
        <li><strong>General-Purpose Registers:</strong> Hold active variables, parameters, and intermediate computational results.</li>
        <li><strong>Program Counter (PC):</strong> Holds the memory address of the next machine instruction to be fetched and executed.</li>
        <li><strong>Stack Pointer (SP):</strong> Points to the top of the active call stack, tracking execution frames, return addresses, and local variables.</li>
        <li><strong>Program Status Word (PSW):</strong> Contains CPU status flags (carry, zero, sign, overflow), the current privilege level mode bit, and interrupt mask flags.</li>
      </ul>

      <h3>Pipelining, Superscalar, &amp; Multicore Architectures</h3>
      <p>
        Modern processors maximize instruction throughput through concurrency:
      </p>
      <ul>
        <li><strong>Pipelining:</strong> Splits execution into sequential stages (Fetch, Decode, Execute, Writeback), allowing consecutive instructions to execute across overlapping stages simultaneously.</li>
        <li><strong>Superscalar Design:</strong> Employs multiple parallel execution pipelines to dispatch and complete multiple independent instructions per clock cycle.</li>
        <li><strong>Multithreading &amp; Hyperthreading:</strong> Duplicates register state and execution contexts on a single CPU core, enabling zero-cycle thread switching whenever a thread stalls on memory latency.</li>
        <li><strong>Multicore Processors:</strong> Places multiple independent physical execution cores onto a single silicon die, each with dedicated L1/L2 caches and shared L3 caches.</li>
      </ul>

      <h2>2. Privilege Modes &amp; Hardware Protection</h2>
      <p>
        To prevent unprivileged application code from destabilizing the operating system or corrupting concurrent processes, CPU hardware enforces distinct privilege levels:
      </p>
      <ul>
        <li><strong>Kernel Mode (Supervisor Mode):</strong> Full, unrestricted access to the entire physical address space, all machine instructions (including direct device I/O and MMU page table manipulation), and system control registers. The operating system kernel executes in kernel mode.</li>
        <li><strong>User Mode:</strong> Applications run with restricted capabilities. Direct device I/O, control register modifications, and access to kernel address spaces are prohibited by hardware.</li>
      </ul>

      <div class="aside-note">
        <strong>The TRAP Instruction &amp; System Calls</strong>
        <p style="margin-top: 6px;">
          When an application requires operating system services (such as file reads or process creation), it executes a <code>TRAP</code> instruction (or <code>syscall</code> / <code>sysenter</code>). This hardware instruction automatically switches the processor from user mode to kernel mode and vectors execution to a predefined handler in the kernel's Interrupt Descriptor Table (IDT).
        </p>
      </div>

      <div class="diagram-container">
        <svg viewBox="0 0 740 260" width="100%" height="auto" style="max-width: 740px; font-family: ui-monospace, Menlo, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <rect x="20" y="20" width="700" height="100" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="6,4" />
          <text x="35" y="45" fill="#64748b" font-size="11" font-weight="bold">USER SPACE (User Mode / Ring 3)</text>
          <rect x="20" y="140" width="700" height="100" rx="8" fill="#f0f9ff" stroke="#bae6fd" stroke-width="2" />
          <text x="35" y="165" fill="#0369a1" font-size="11" font-weight="bold">KERNEL SPACE (Kernel Mode / Ring 0)</text>

          <rect x="60" y="55" width="190" height="50" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1.5" />
          <text x="155" y="78" fill="#0f172a" font-size="12" font-weight="bold" text-anchor="middle">User Application</text>
          <text x="155" y="94" fill="#64748b" font-size="10" text-anchor="middle">Issues open() / read()</text>

          <rect x="290" y="85" width="160" height="50" rx="6" fill="#0284c7" stroke="#0369a1" stroke-width="1.5" />
          <text x="370" y="107" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">TRAP / SYSCALL</text>
          <text x="370" y="123" fill="#e0f2fe" font-size="10" text-anchor="middle">Mode Bit: User &rarr; Kernel</text>

          <rect x="490" y="170" width="190" height="55" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" />
          <text x="585" y="193" fill="#0369a1" font-size="12" font-weight="bold" text-anchor="middle">Syscall Dispatcher</text>
          <text x="585" y="210" fill="#475569" font-size="10" text-anchor="middle">Execute Kernel Handler (IDT)</text>

          <path d="M 250,80 L 285,100" fill="none" stroke="#0284c7" stroke-width="2" />
          <path d="M 450,115 L 485,185" fill="none" stroke="#0284c7" stroke-width="2" />
          <path d="M 490,205 C 360,240 240,160 160,110" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="4,4" />
          <text x="330" y="220" fill="#64748b" font-size="10" text-anchor="middle">IRET / SYSRET (Kernel &rarr; User)</text>
        </svg>
      </div>

      <h2>3. The Memory Hierarchy</h2>
      <p>
        Memory systems are organized into a strict latency and capacity hierarchy. The operating system coordinates with hardware MMUs and caches to keep frequently referenced data at the fastest tiers:
      </p>

      <table>
        <thead>
          <tr>
            <th>Hierarchy Level</th>
            <th>Technology</th>
            <th>Typical Latency</th>
            <th>Typical Capacity</th>
            <th>Managed By</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>CPU Registers</strong></td>
            <td>Flip-flops (on-die)</td>
            <td>&lt; 1 ns</td>
            <td>&lt; 2 KB</td>
            <td>Compiler / Machine Code</td>
          </tr>
          <tr>
            <td><strong>L1 / L2 / L3 Caches</strong></td>
            <td>Static RAM (SRAM)</td>
            <td>1 – 15 ns</td>
            <td>64 KB – 64 MB</td>
            <td>Hardware Cache Controller</td>
          </tr>
          <tr>
            <td><strong>Main Memory</strong></td>
            <td>Dynamic RAM (DRAM)</td>
            <td>50 – 100 ns</td>
            <td>16 GB – 128 GB</td>
            <td>Operating System (Virtual Memory)</td>
          </tr>
          <tr>
            <td><strong>Solid-State Drives (SSD)</strong></td>
            <td>NAND Flash (NVMe)</td>
            <td>10 – 50 &mu;s</td>
            <td>512 GB – 4 TB</td>
            <td>Operating System / File System</td>
          </tr>
          <tr>
            <td><strong>Magnetic Disks (HDD)</strong></td>
            <td>Rotational Magnetic Platters</td>
            <td>5 – 10 ms</td>
            <td>1 TB – 20 TB</td>
            <td>Operating System / File System</td>
          </tr>
        </tbody>
      </table>

      <div class="diagram-container">
        <svg viewBox="0 0 960 430" width="100%" height="auto" style="max-width: 960px; min-width: 650px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="arrowSpeed" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
              <path d="M0,8 L4,0 L8,8 Z" fill="#0284c7" />
            </marker>
            <marker id="arrowCapacity" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
              <path d="M0,0 L4,8 L8,0 Z" fill="#334155" />
            </marker>
          </defs>

          <!-- Left Axis: Speed & Cost -->
          <line x1="45" y1="390" x2="45" y2="35" stroke="#0284c7" stroke-width="3" marker-end="url(#arrowSpeed)" />
          <text x="35" y="215" fill="#0284c7" font-size="11" font-weight="700" transform="rotate(-90 35 215)" text-anchor="middle">FASTER ACCESS &amp; HIGHER COST / BIT</text>

          <!-- Tier 1: CPU Registers -->
          <g transform="translate(70, 25)">
            <rect x="180" y="0" width="280" height="52" rx="6" fill="#0284c7" stroke="#0369a1" stroke-width="2" />
            <text x="320" y="24" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">CPU Registers</text>
            <text x="320" y="42" fill="#e0f2fe" font-size="11" font-weight="600" text-anchor="middle">&lt; 2 KB | &lt; 1 ns</text>
            <line x1="470" y1="26" x2="520" y2="26" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="530" y="7" width="280" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="545" y="31" fill="#0f172a" font-size="12" font-weight="700">Internal registers on CPU core</text>
          </g>

          <!-- Tier 2: Cache Memory -->
          <g transform="translate(70, 97)">
            <rect x="140" y="0" width="320" height="52" rx="6" fill="#0369a1" stroke="#075985" stroke-width="2" />
            <text x="300" y="24" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">L1 / L2 / L3 Caches (SRAM)</text>
            <text x="300" y="42" fill="#e0f2fe" font-size="11" font-weight="600" text-anchor="middle">64 KB – 64 MB | 1 – 15 ns</text>
            <line x1="470" y1="26" x2="520" y2="26" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="530" y="7" width="280" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="545" y="31" fill="#0f172a" font-size="12" font-weight="700">On-die static RAM cache</text>
          </g>

          <!-- Tier 3: Main Memory -->
          <g transform="translate(70, 169)">
            <rect x="100" y="0" width="360" height="52" rx="6" fill="#075985" stroke="#0c4a6e" stroke-width="2" />
            <text x="280" y="24" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Main Memory (DRAM)</text>
            <text x="280" y="42" fill="#e0f2fe" font-size="11" font-weight="600" text-anchor="middle">16 GB – 128 GB | 50 – 100 ns</text>
            <line x1="470" y1="26" x2="520" y2="26" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="530" y="7" width="280" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="545" y="31" fill="#0f172a" font-size="12" font-weight="700">Primary volatile system RAM</text>
          </g>

          <!-- Tier 4: Solid-State Drives -->
          <g transform="translate(70, 241)">
            <rect x="60" y="0" width="400" height="52" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2" />
            <text x="260" y="24" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Solid-State Drives (NVMe / SSD)</text>
            <text x="260" y="42" fill="#e2e8f0" font-size="11" font-weight="600" text-anchor="middle">512 GB – 4 TB | 10 – 50 μs</text>
            <line x1="470" y1="26" x2="520" y2="26" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="530" y="7" width="280" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="545" y="31" fill="#0f172a" font-size="12" font-weight="700">Non-volatile NAND flash storage</text>
          </g>

          <!-- Tier 5: Magnetic Disks -->
          <g transform="translate(70, 313)">
            <rect x="20" y="0" width="440" height="52" rx="6" fill="#0f172a" stroke="#1e293b" stroke-width="2" />
            <text x="240" y="24" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Magnetic Hard Disks (HDD)</text>
            <text x="240" y="42" fill="#cbd5e1" font-size="11" font-weight="600" text-anchor="middle">1 TB – 20 TB | 5 – 10 ms</text>
            <line x1="470" y1="26" x2="520" y2="26" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
            <rect x="530" y="7" width="280" height="38" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="545" y="31" fill="#0f172a" font-size="12" font-weight="700">Secondary rotational storage</text>
          </g>

          <!-- Right Axis: Capacity & Persistence -->
          <line x1="895" y1="35" x2="895" y2="390" stroke="#334155" stroke-width="3" marker-end="url(#arrowCapacity)" />
          <text x="912" y="215" fill="#334155" font-size="11" font-weight="700" transform="rotate(90 912 215)" text-anchor="middle">LARGER STORAGE CAPACITY &amp; PERSISTENCE</text>
        </svg>
      </div>

      <h3>Virtual Memory &amp; The MMU</h3>
      <p>
        The CPU incorporates a dedicated hardware component known as the <strong>Memory Management Unit (MMU)</strong>. The MMU dynamically translates program virtual memory addresses into physical RAM addresses using page tables. This decouples user programs from physical memory layouts, prevents rogue programs from accessing unauthorized address spaces, and enables virtual memory paging to disk.
      </p>

      <h2>4. Disks, I/O Devices, &amp; Controller Hardware</h2>
      <p>
        I/O devices consist of two distinct elements: the physical peripheral (e.g., the disk platter, SSD NAND flash array, monitor, keyboard) and the <strong>device controller</strong> (the electronic circuitry interfacing the device to the system bus).
      </p>

      <h3>Three Fundamental I/O Strategies</h3>
      <ul>
        <li><strong>Programmed I/O (Polling / Busy Waiting):</strong> The CPU repeatedly checks a device controller status register in a tight loop until the operation completes. Polling ties up the CPU and wastes clock cycles.</li>
        <li><strong>Interrupt-Driven I/O:</strong> The CPU issues a command to the device controller and continues executing other tasks. When the device finishes, the controller raises an electrical interrupt line, triggering the kernel's interrupt service routine.</li>
        <li><strong>Direct Memory Access (DMA):</strong> A dedicated DMA controller orchestrates high-speed bulk data transfers directly between device controllers and main memory without continuous CPU intervention, raising an interrupt only after the full block is transferred.</li>
      </ul>

      <div class="diagram-container">
        <svg viewBox="0 0 740 280" width="100%" height="auto" style="max-width: 740px; font-family: ui-monospace, Menlo, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <rect x="40" y="30" width="140" height="70" rx="6" fill="#f8fafc" stroke="#0284c7" stroke-width="2" />
          <text x="110" y="62" fill="#0284c7" font-size="14" font-weight="bold" text-anchor="middle">CPU Core</text>
          <text x="110" y="82" fill="#64748b" font-size="10" text-anchor="middle">1. Programs DMA transfer</text>

          <rect x="300" y="30" width="160" height="70" rx="6" fill="#0284c7" stroke="#0369a1" stroke-width="2" />
          <text x="380" y="62" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">DMA Controller</text>
          <text x="380" y="82" fill="#e0f2fe" font-size="10" text-anchor="middle">2. Arbitrates bus cycles</text>

          <rect x="560" y="30" width="140" height="70" rx="6" fill="#f8fafc" stroke="#0284c7" stroke-width="2" />
          <text x="630" y="62" fill="#0284c7" font-size="14" font-weight="bold" text-anchor="middle">Main Memory</text>
          <text x="630" y="82" fill="#64748b" font-size="10" text-anchor="middle">Buffer Source / Target</text>

          <rect x="40" y="145" width="660" height="24" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.5" />
          <text x="370" y="161" fill="#475569" font-size="11" font-weight="bold" text-anchor="middle">SYSTEM &amp; MEMORY BUS (PCIe / DMI / Memory Channels)</text>

          <rect x="300" y="200" width="160" height="60" rx="6" fill="#f8fafc" stroke="#64748b" stroke-width="1.5" />
          <text x="380" y="226" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">Device Controller</text>
          <text x="380" y="244" fill="#64748b" font-size="10" text-anchor="middle">(NVMe / Disk / NIC)</text>

          <line x1="110" y1="100" x2="110" y2="145" stroke="#0284c7" stroke-width="2" />
          <line x1="380" y1="100" x2="380" y2="145" stroke="#0284c7" stroke-width="2" />
          <line x1="630" y1="100" x2="630" y2="145" stroke="#0284c7" stroke-width="2" />
          <line x1="380" y1="169" x2="380" y2="200" stroke="#64748b" stroke-width="2" />

          <path d="M 460,230 C 580,230 630,190 630,105" fill="none" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="6,3" />
          <text x="595" y="245" fill="#0284c7" font-size="10" font-weight="bold">Direct Memory Stream (Bypasses CPU)</text>
        </svg>
      </div>

      <h2>5. Buses &amp; The Boot Sequence</h2>
      <p>
        Modern computers use a hierarchy of physical <strong>buses</strong> (PCIe, DMI, USB, and memory channels) operating at different clock speeds. The high-speed memory bus connects the CPU directly to RAM, while expansion buses connect peripherals to controllers.
      </p>

      <h3>The System Boot Sequence</h3>
      <ol>
        <li><strong>Power-On &amp; Reset:</strong> When power is supplied, the CPU initializes its registers and executes firmware stored in non-volatile ROM/Flash memory (the <strong>BIOS</strong> or <strong>UEFI</strong>).</li>
        <li><strong>Hardware Probing (POST):</strong> Firmware executes the Power-On Self-Test (POST), checks available RAM, scans internal buses, and inventories attached controllers and peripherals.</li>
        <li><strong>Bootloader Loading:</strong> Firmware inspects configured boot media to locate the Master Boot Record (MBR) or EFI System Partition (ESP), reading the primary bootloader (e.g., GRUB) into RAM.</li>
        <li><strong>Kernel Relocation:</strong> The bootloader loads the operating system kernel and initial ramdisk image into memory, configures basic page tables, and transfers execution control to the kernel entry point.</li>
        <li><strong>Kernel Initialization:</strong> The operating system kernel takes full control, initializes device drivers, configures interrupts, initializes the scheduler and virtual memory, and launches the first user-space initialization daemon (such as <code>systemd</code> or <code>init</code>).</li>
      </ol>
    </article>
  </main>

  <nav class="module-nav-bar bottom">
    <a href="01-what-is-an-os-and-history.html" class="module-nav-btn">&larr; Previous: 01. What Is an Operating System &amp; History</a>
    <a href="index.html" class="module-nav-btn">Week Index</a>
    <a href="03-os-concepts.html" class="module-nav-btn">Next: 03. OS Concepts &rarr;</a>
  </nav>

</body>
</html>
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"--> Successfully updated {file_path} without card enclosures.")

    # Git sync
    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Remove card enclosures from main text in 02-hardware-review.html\n\n"
            "Update week01-operating-system-concepts/02-hardware-review.html to flow as\n"
            "standard document prose without card boxes around core section text."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    overhaul_page_layout()
