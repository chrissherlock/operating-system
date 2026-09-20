#!/usr/bin/env python3
# =====================================================================
# fix.py: Build complete 02-hardware-review.html and sync to repository
# =====================================================================
import os
import subprocess

def write_hardware_module():
    target_dir = "week01-operating-system-concepts"
    file_name = "02-hardware-review.html"
    file_path = os.path.join(target_dir, file_name)

    os.makedirs(target_dir, exist_ok=True)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>02. Computer Hardware Review -- COSC240</title>
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
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
    .nav-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      max-width: 1100px;
      margin: 0 auto;
    }
    .nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      font-family: var(--font-mono);
      text-decoration: none;
      color: var(--accent);
      background-color: #f0f9ff;
      border: 1px solid #bae6fd;
      padding: 6px 12px;
      border-radius: 6px;
    }
    .nav-btn:hover {
      background-color: var(--accent);
      color: #ffffff;
    }
    main {
      width: 100%;
      max-width: 1100px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }
    header {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 30px;
    }
    h1 {
      font-size: 1.8rem;
      color: var(--accent);
      margin-bottom: 8px;
    }
    p.subtitle {
      color: var(--text-muted);
      font-size: 0.95rem;
    }
    .content-section {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 30px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .content-section h2 {
      font-size: 1.3rem;
      color: var(--accent-hover);
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 8px;
    }
    h3 {
      font-size: 1.1rem;
      color: #1e293b;
      margin-top: 10px;
    }
    p {
      color: var(--text-muted);
      line-height: 1.6;
      font-size: 0.95rem;
    }
    ul {
      margin-left: 20px;
      color: var(--text-muted);
      line-height: 1.6;
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
    .callout-box {
      background: #f8fafc;
      border-left: 4px solid var(--accent);
      padding: 16px;
      border-radius: 0 6px 6px 0;
      margin-top: 8px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
      font-size: 0.9rem;
    }
    th, td {
      border: 1px solid var(--border);
      padding: 10px 14px;
      text-align: left;
    }
    th {
      background-color: #f1f5f9;
      color: #1e293b;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="nav-bar">
    <a href="01-what-is-an-os-and-history.html" class="nav-btn">&larr; Previous: 01. What Is an OS &amp; History</a>
    <a href="index.html" class="nav-btn">Chapter 1 Index</a>
  </div>

  <main>
    <header>
      <h1>02. Computer Hardware Review</h1>
      <p class="subtitle">Tanenbaum Chapter 1.3: Processors, Memory Hierarchy, Disks, I/O Devices, Buses, and Booting.</p>
    </header>

    <section class="content-section">
      <h2>1. Processors (CPUs) &amp; Execution Mechanics</h2>
      <p>
        The Central Processing Unit (CPU) is the brain of the computer, executing instructions fetched from main memory. The fundamental operation of the CPU follows the classical <strong>fetch-decode-execute cycle</strong>:
      </p>
      <ul>
        <li><strong>Fetch:</strong> Retrieve the instruction at the memory address currently designated by the Program Counter (PC).</li>
        <li><strong>Decode:</strong> Interpret the operation code (opcode) to determine the instruction type and identify the required operands.</li>
        <li><strong>Execute:</strong> Carry out the operation within the Arithmetic Logic Unit (ALU), manipulate data registers, and adjust processor state flags.</li>
      </ul>

      <h3>Key Processor Registers</h3>
      <p>
        CPUs contain internal high-speed storage registers that can be accessed with zero wait states:
      </p>
      <ul>
        <li><strong>General-Purpose Registers:</strong> Hold local variables, arithmetic operands, and temporary intermediate results.</li>
        <li><strong>Program Counter (PC):</strong> Stores the memory address of the next instruction to be fetched.</li>
        <li><strong>Stack Pointer (SP):</strong> Points to the top of the current call stack frame in memory, tracking local variables, parameters, and return addresses.</li>
        <li><strong>Program Status Word (PSW):</strong> Contains condition code bits (carry, overflow, zero, sign), CPU priority level, mode bits (user vs. kernel mode), and interrupt enablement flags.</li>
      </ul>

      <h3>Pipelining, Superscalar, &amp; Multicore Architectures</h3>
      <p>
        Modern processors maximize throughput by executing multiple instructions concurrently:
      </p>
      <ul>
        <li><strong>Pipelining:</strong> Deconstructs instruction processing into sequential stages (e.g., Fetch, Decode, Execute, Writeback), allowing an instruction to be decoded while the previous one is executed and the next one is fetched.</li>
        <li><strong>Superscalar Execution:</strong> Features multiple parallel execution units (multiple ALUs, floating-point units). If two consecutive instructions are mutually independent, both are issued and executed simultaneously.</li>
        <li><strong>Multithreading &amp; Hyperthreading:</strong> Duplicates architectural state (registers, PC, PSW) on a single physical core, allowing near-instantaneous thread context switching when one thread stalls on memory access.</li>
        <li><strong>Multicore Processors:</strong> Embed multiple complete, independent CPU cores onto a single silicon die, each with dedicated L1/L2 caches and shared L3 caches.</li>
      </ul>
    </section>

    <section class="content-section">
      <h2>2. Privilege Modes &amp; Hardware Protection</h2>
      <p>
        To prevent rogue or faulty user software from crashing the operating system or corrupting other programs, CPU hardware enforces distinct privilege execution levels:
      </p>
      <ul>
        <li><strong>Kernel Mode (Supervisor Mode):</strong> Complete, unrestricted access to the entire physical address space, all machine instructions (including direct device I/O, MMU modifications, and timer interrupts), and system configuration tables. The operating system kernel runs exclusively in kernel mode.</li>
        <li><strong>User Mode:</strong> A restricted subset of instructions is available. Direct memory access to kernel space, modification of control registers, and raw I/O instructions are strictly prohibited and trap to the OS kernel.</li>
      </ul>

      <div class="callout-box">
        <strong>The TRAP Instruction &amp; System Calls</strong>
        <p style="margin-top: 6px;">
          When a user program requires hardware services (e.g., reading a file from disk), it executes a specialized <code>TRAP</code> instruction (or <code>syscall</code> / <code>sysenter</code>). This hardware instruction switches the CPU from user mode to kernel mode and branches unconditionally to a predefined vector in the kernel's interrupt descriptor table, allowing controlled privileged execution.
        </p>
      </div>
    </section>

    <section class="content-section">
      <h2>3. The Memory Hierarchy</h2>
      <p>
        System memory is organized as a hierarchy balancing access latency, total capacity, and cost per bit:
      </p>

      <table>
        <thead>
          <tr>
            <th>Level</th>
            <th>Technology</th>
            <th>Typical Latency</th>
            <th>Typical Capacity</th>
            <th>Management</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Registers</strong></td>
            <td>Flip-flops (CPU die)</td>
            <td>&lt; 1 ns</td>
            <td>&lt; 2 KB</td>
            <td>Compiler / Assembly</td>
          </tr>
          <tr>
            <td><strong>Cache (L1/L2/L3)</strong></td>
            <td>Static RAM (SRAM)</td>
            <td>1 – 15 ns</td>
            <td>64 KB – 64 MB</td>
            <td>Hardware controller</td>
          </tr>
          <tr>
            <td><strong>Main Memory</strong></td>
            <td>Dynamic RAM (DRAM)</td>
            <td>50 – 100 ns</td>
            <td>8 GB – 128 GB</td>
            <td>Operating System</td>
          </tr>
          <tr>
            <td><strong>Solid-State Drive</strong></td>
            <td>NAND Flash (NVMe)</td>
            <td>10 – 50 &mu;s</td>
            <td>512 GB – 4 TB</td>
            <td>Operating System</td>
          </tr>
          <tr>
            <td><strong>Magnetic Disk</strong></td>
            <td>Rotational platters</td>
            <td>5 – 10 ms</td>
            <td>1 TB – 20 TB</td>
            <td>Operating System</td>
          </tr>
        </tbody>
      </table>

      <h3>Virtual Memory &amp; The MMU</h3>
      <p>
        Operating systems decouple program addresses from physical memory chips using <strong>virtual memory</strong>. The processor contains a dedicated hardware component known as the <strong>Memory Management Unit (MMU)</strong>. The MMU dynamically maps virtual addresses generated by application code into actual physical RAM addresses using page tables, enforcing memory boundaries and protecting isolated processes.
      </p>
    </section>

    <section class="content-section">
      <h2>4. Disks, I/O Devices, &amp; Controller Hardware</h2>
      <p>
        I/O devices generally consist of two distinct parts: a physical component (the mechanical drive, screen, or cable) and an electronic component called the <strong>device controller</strong>.
      </p>
      <ul>
        <li><strong>Device Controllers:</strong> The electronic chip or circuit board that accepts commands from the OS and manages low-level electrical signals to the physical peripheral.</li>
        <li><strong>Memory-Mapped I/O &amp; I/O Ports:</strong> The operating system communicates with device controllers by writing to and reading from designated controller registers mapped into memory addresses or separate I/O port spaces.</li>
      </ul>

      <h3>Three Fundamental I/O Approaches</h3>
      <ul>
        <li><strong>1. Programmed I/O (Busy Waiting):</strong> The CPU polls the device controller in a tight loop until the requested operation completes. This wastes CPU cycles.</li>
        <li><strong>2. Interrupt-Driven I/O:</strong> The CPU starts the transfer, moves on to execute other work, and receives a hardware <strong>interrupt</strong> signal from the controller when the transfer completes.</li>
        <li><strong>3. Direct Memory Access (DMA):</strong> A dedicated DMA controller chip orchestrates the bulk transfer of data directly between peripheral controllers and main memory without continuous CPU intervention, interrupting the processor only after an entire data block has been transferred.</li>
      </ul>
    </section>

    <section class="content-section">
      <h2>5. Buses &amp; The Boot Process</h2>
      <p>
        Modern computers utilize a hierarchy of specialized <strong>buses</strong> (PCIe, DMI, USB, DDR memory channels) connecting processors, memory, and controllers. Fast buses connect the CPU to high-speed caches and RAM, while secondary buses link standard peripherals.
      </p>

      <h3>How the Computer Boots Up</h3>
      <ol style="margin-left: 20px; color: var(--text-muted); line-height: 1.6;">
        <li>When power is supplied, the CPU initializes its registers and executes boot firmware stored in non-volatile ROM/flash (the <strong>BIOS</strong> or modern <strong>UEFI</strong>).</li>
        <li>The firmware checks physical RAM, scans buses, and detects attached peripheral devices (Power-On Self-Test / POST).</li>
        <li>The firmware identifies the designated boot device and reads the first sector (Master Boot Record) or loads the EFI bootloader binary from the EFI System Partition (ESP).</li>
        <li>The bootloader (such as GRUB) copies the operating system kernel and initial RAM filesystem into main memory.</li>
        <li>The bootloader transfers execution to the kernel entry point. The OS kernel initializes hardware drivers, activates protected virtual memory, and spawns the initial user-space environment (such as <code>init</code> or <code>systemd</code>).</li>
      </ol>
    </section>

    <div class="nav-bar" style="margin-top: 10px; margin-bottom: 20px;">
      <a href="01-what-is-an-os-and-history.html" class="nav-btn">&larr; Previous: 01. What Is an OS &amp; History</a>
      <a href="index.html" class="nav-btn">Chapter 1 Index &rarr;</a>
    </div>
  </main>
</body>
</html>
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"--> Successfully generated complete content for {file_path}")

    files_to_sync = [
        "fix.py",
        file_path,
        os.path.join(target_dir, "01-what-is-an-os-and-history.html")
    ]
    staged = [f for f in files_to_sync if os.path.exists(f)]
    print(f"--> Staging files: {staged}")

    try:
        subprocess.run(["git", "add"] + staged, check=True)
        commit_msg = "Build comprehensive 02-hardware-review.html module via fix.py"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git note: {e}")

if __name__ == "__main__":
    write_hardware_module()
