#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand Sections 2, 4, 5, and 6 in 03-os-concepts.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "03-os-concepts.html"
)

EXPANDED_SECTIONS_BLOCK = r"""    <h3>2. Address Spaces &amp; Virtual Memory: Diverse Architectures</h3>
    <p>
      To prevent concurrent programs from corrupting one another's data and to decouple software from the limits of physical RAM, operating systems provide the <strong>address space</strong> abstraction. While contemporary systems predominantly utilize flat, paged virtual memory architectures, operating system design encompasses three distinct structural paradigms:
    </p>

    <h4>Memory Architectures Across Operating Systems</h4>
    <ul>
      <li><strong>Flat Paged Virtual Memory (Linux, Windows NT, macOS):</strong> Memory is partitioned into fixed-size chunks called <em>pages</em> (typically 4 KiB, with 2 MiB / 1 GiB huge pages). The hardware Memory Management Unit (MMU) consults multi-level page tables (e.g., x86-64 4-level or 5-level paging, ARM64 translation tables) to translate virtual addresses into physical frames dynamically. Paging enables fine-grained protection flags (read, write, execute), copy-on-write sharing, and demand paging to swap space or page files.</li>
      <li><strong>Segmented Memory (x86 Protected Mode, Multics, OS/2):</strong> Instead of a uniform flat array, memory is divided into variable-length, semantically meaningful logical blocks called <em>segments</em> (e.g., Code Segment, Data Segment, Stack Segment). Each address consists of a segment selector and an offset. While pure segmentation fell out of favor on 64-bit consumer systems due to fragmentation, it provided hardware-enforced bounds checking and capabilities natively.</li>
      <li><strong>Single-Level Store &amp; Single Address Space (IBM OS/400 / IBM i):</strong> Rather than maintaining private, isolated address spaces per program, systems like IBM i treat all storage—volatile DRAM and non-volatile disk arrays—as one enormous, globally addressed 64-bit or 128-bit virtual address space. Programs, files, and database records reside permanently within this unified store, accessed via hardware-enforced 16-byte capability pointers rather than traditional file path opens.</li>
    </ul>

    <!-- Diagram: Address Space Architectures -->
    <div style="display: flex; justify-content: center; margin: 24px 0;">
      <svg viewBox="0 0 760 250" width="100%" height="100%" style="max-width: 760px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <filter id="mem-shadow" x="-5%" y="-5%" width="110%" height="110%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.06" />
          </filter>
        </defs>

        <!-- Left Box: Isolated Virtual Address Spaces -->
        <g transform="translate(30, 20)" filter="url(#mem-shadow)">
          <rect width="335" height="210" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" />
          <rect width="335" height="28" rx="6" fill="#f0f9ff" />
          <line x1="0" y1="28" x2="335" y2="28" stroke="#bae6fd" />
          <text x="167" y="19" fill="#0369a1" font-size="10" font-weight="700" text-anchor="middle">Isolated Address Spaces (Linux / Windows NT)</text>

          <!-- Space A -->
          <rect x="25" y="45" width="125" height="75" rx="4" fill="#f8fafc" stroke="#cbd5e1" />
          <text x="87" y="62" fill="#0f172a" font-size="9" font-weight="700" text-anchor="middle">Process A</text>
          <text x="87" y="76" fill="#64748b" font-size="7.5" text-anchor="middle">0x0000..0xFFFF</text>
          <rect x="35" y="85" width="105" height="25" rx="3" fill="#e0f2fe" stroke="#0284c7" />
          <text x="87" y="101" fill="#0369a1" font-size="8" text-anchor="middle">Private Page Map</text>

          <!-- Space B -->
          <rect x="185" y="45" width="125" height="75" rx="4" fill="#f8fafc" stroke="#cbd5e1" />
          <text x="247" y="62" fill="#0f172a" font-size="9" font-weight="700" text-anchor="middle">Process B</text>
          <text x="247" y="76" fill="#64748b" font-size="7.5" text-anchor="middle">0x0000..0xFFFF</text>
          <rect x="195" y="85" width="105" height="25" rx="3" fill="#e0f2fe" stroke="#0284c7" />
          <text x="247" y="101" fill="#0369a1" font-size="8" text-anchor="middle">Private Page Map</text>

          <!-- Shared Physical RAM Bottom -->
          <rect x="25" y="145" width="285" height="48" rx="4" fill="#ecfdf5" stroke="#059669" stroke-width="1.2" />
          <text x="167" y="165" fill="#065f46" font-size="9.5" font-weight="700" text-anchor="middle">Shared Physical DRAM Frames</text>
          <text x="167" y="180" fill="#047857" font-size="8" text-anchor="middle">MMU swaps page roots on context switch</text>
        </g>

        <!-- Right Box: Single-Level Store -->
        <g transform="translate(395, 20)" filter="url(#mem-shadow)">
          <rect width="335" height="210" rx="6" fill="#ffffff" stroke="#d97706" stroke-width="1.5" />
          <rect width="335" height="28" rx="6" fill="#fffbeb" />
          <line x1="0" y1="28" x2="335" y2="28" stroke="#fde68a" />
          <text x="167" y="19" fill="#92400e" font-size="10" font-weight="700" text-anchor="middle">Single-Level Store (IBM i / OS/400)</text>

          <!-- Unified continuous space -->
          <rect x="25" y="45" width="285" height="148" rx="4" fill="#f8fafc" stroke="#cbd5e1" stroke-dasharray="4,4" />
          <text x="167" y="65" fill="#1e293b" font-size="9.5" font-weight="700" text-anchor="middle">Universal 128-Bit Virtual Address Space</text>

          <rect x="40" y="80" width="115" height="42" rx="3" fill="#fef3c7" stroke="#d97706" />
          <text x="97" y="98" fill="#92400e" font-size="8.5" font-weight="600" text-anchor="middle">Objects &amp; Data</text>
          <text x="97" y="112" fill="#78350f" font-size="7.5" text-anchor="middle">Permanent Storage</text>

          <rect x="180" y="80" width="115" height="42" rx="3" fill="#eff6ff" stroke="#0284c7" />
          <text x="237" y="98" fill="#0369a1" font-size="8.5" font-weight="600" text-anchor="middle">Active Programs</text>
          <text x="237" y="112" fill="#1e40af" font-size="7.5" text-anchor="middle">Volatile DRAM</text>

          <rect x="40" y="136" width="255" height="44" rx="3" fill="#ffffff" stroke="#94a3b8" />
          <text x="167" y="154" fill="#334155" font-size="8.5" font-weight="700" text-anchor="middle">Hardware Capability Pointers</text>
          <text x="167" y="168" fill="#64748b" font-size="7.5" text-anchor="middle">No file open/close; accessed via direct memory pointer</text>
        </g>
      </svg>
    </div>

    <!-- Section 3 remains intact before Section 4 -->
"""

EXPANDED_SECTIONS_FOUR_TO_SIX = r"""    <h3>4. Input/Output (I/O) Subsystems</h3>
    <p>
      The primary role of the I/O subsystem is to bridge the massive speed and interface discrepancies between the high-speed CPU memory bus and heterogeneous external peripherals. Operating systems differ substantially in how they model, schedule, and notify applications of completed I/O transactions:
    </p>

    <h4>I/O Notification &amp; Completion Models</h4>
    <ul>
      <li><strong>Synchronous Blocking &amp; Readiness Polling (Classic POSIX):</strong> The calling thread initiates an I/O call (e.g., <code>read()</code>) and transitions into a Blocked state until physical hardware completes the transfer. Multiplexing primitives like <code>select()</code>, <code>poll()</code>, and Linux <code>epoll()</code> or BSD <code>kqueue</code> signal when a file descriptor is <em>ready</em> to perform a non-blocking read or write.</li>
      <li><strong>Asynchronous Completion Ports (Windows IOCP):</strong> Instead of waiting for readiness, Windows applications initiate genuine asynchronous operations (via <code>ReadFileEx</code> or overlapped I/O) and specify an <strong>I/O Completion Port (IOCP)</strong>. The NT kernel queues completion packets onto the port as hardware finishes data transfers into application-owned buffers, allowing a small pool of worker threads to service thousands of concurrent sockets without polling.</li>
      <li><strong>Shared Ring-Buffer Submission (Linux <code>io_uring</code>):</strong> Modern Linux bridges the gap with twin circular ring buffers (Submission Queue and Completion Queue) shared between user space and kernel space. Applications submit batches of I/O requests without issuing individual system calls, minimizing context switches for high-throughput NVMe and networking workloads.</li>
      <li><strong>Mainframe Channel Architecture (IBM z/Architecture):</strong> Mainframes completely decouple I/O execution from the main CPUs using dedicated auxiliary coprocessors called <strong>Channel Subsystems</strong>. The CPU simply executes a <code>START SUBCHANNEL</code> instruction pointing to a sequence of <strong>Channel Command Words (CCWs)</strong> in memory; the channel hardware manages bus negotiation, device handshakes, and memory transfers autonomously before raising an I/O interrupt.</li>
    </ul>

    <div style="overflow-x: auto; margin: 16px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; background: #ffffff;">
        <thead>
          <tr style="background: #f1f5f9; color: #1e293b;">
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Platform</th>
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Dominant High-Performance Paradigm</th>
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Hardware Handshake Mechanism</th>
          </tr>
        </thead>
        <tbody style="color: #334155;">
          <tr>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">POSIX / Linux</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Readiness notification (<code>epoll</code>) or shared lockless submission rings (<code>io_uring</code>).</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Kernel drivers issue MMIO register writes and service hardware IRQs.</td>
          </tr>
          <tr style="background: #f8fafc;">
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">Windows NT</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Asynchronous completion packet queues (I/O Completion Ports - IOCP).</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">I/O Request Packets (IRPs) passed down layered driver stacks.</td>
          </tr>
          <tr>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">Microkernels (QNX / seL4)</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Synchronous message passing (IPC) to user-space driver server processes.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Kernel converts IRQs into IPC notification events delivered to driver threads.</td>
          </tr>
          <tr style="background: #f8fafc;">
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">IBM Mainframes</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Autonomous Channel Subsystem executing Channel Command Word (CCW) programs.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Specialized auxiliary I/O processors transfer data directly to/from memory.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h3>5. Protection &amp; Security: Authorization Paradigms</h3>
    <p>
      Operating system protection mechanisms ensure that executing software accesses only authorized resources (memory segments, files, devices, network endpoints). Broadly, three distinct authorization and boundary paradigms are employed across systems:
    </p>

    <h4>Three Core Security Architectures</h4>
    <ul>
      <li><strong>Discretionary Access Control (DAC):</strong> The resource owner dictates access permissions. Traditional Unix uses numerical User IDs (UID), Group IDs (GID), and permission bits (<code>rwxrwxrwx</code>). Windows NT expands this via <strong>Discretionary Access Control Lists (DACLs)</strong> composed of individual Access Control Entries (ACEs) granting or denying specific Security Identifiers (SIDs) fine-grained rights like <code>FILE_APPEND_DATA</code> or <code>WRITE_OWNER</code>.</li>
      <li><strong>Mandatory Access Control (MAC):</strong> Centralized security policy enforced by the kernel regardless of user preferences. Frameworks like <strong>SELinux</strong>, <strong>AppArmor</strong>, and <strong>Windows Mandatory Integrity Control (MIC)</strong> assign security labels to subjects and objects (e.g., Low, Medium, High, System integrity levels in Windows, or Type Enforcement domains in SELinux), isolating processes even if compromised by zero-day exploits.</li>
      <li><strong>Capability-Based Security (seL4, Fuchsia, KeyKOS):</strong> In pure capability systems, access is granted not by matching identity strings against access lists, but through unforgeable cryptographic or kernel-held tokens called <em>capabilities</em>. Possessing a valid capability grants the holder the authority to perform operations on an object directly, eliminating confused deputy vulnerabilities.</li>
    </ul>

    <h3>6. The Command Interpreter: Text, Objects, and Batch Job Control</h3>
    <p>
      The command interpreter provides the direct interface through which users and automation scripts interact with operating system facilities. Far from being a uniform shell environment, modern and historical command systems reflect contrasting philosophies of data exchange and execution control:
    </p>

    <h4>Command Line Paradigms Compared</h4>
    <ul>
      <li><strong>Text Stream &amp; Pipeline Shells (sh, bash, zsh):</strong> Built around the Unix philosophy of small tools connected via linear ASCII/UTF-8 byte streams. Commands read from standard input and emit unstructured text to standard output, requiring external utilities (such as <code>grep</code>, <code>awk</code>, <code>sed</code>) to parse textual fields. Process creation relies on the classical <code>fork()</code> and <code>exec()</code> primitives.</li>
      <li><strong>Object-Oriented Shells (PowerShell):</strong> Instead of untyped byte streams, PowerShell pipelines transmit strongly-typed .NET CLI objects. Commands (called <em>cmdlets</em>) receive and emit structured objects possessing properties and methods, eliminating brittle string scraping and regex parsing. On Windows, execution launches through the Win32 <code>CreateProcess()</code> system call, which creates the address space, initial thread, and handles in a single atomic invocation rather than a split fork/exec.</li>
      <li><strong>Job Control Language (IBM JCL):</strong> In mainframe batch computing, user interaction occurs through structured declarative control cards specifying computational jobs, required program binaries, datasets, and volume dependencies (e.g., <code>//JOB</code>, <code>//EXEC</code>, <code>//DD</code> cards). The operating system's Job Entry Subsystem (JES2/JES3) evaluates resource allocations, queues the job, schedules CPU allocation, and handles spooling without requiring interactive shell sessions.</li>
    </ul>"""

def expand_remaining_sections():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Step 1: Replace Section 2 (Address Spaces)
    sec2_start = "<h3>2. Address Spaces &amp; Virtual Memory</h3>"
    sec3_start = "<h3>3. Files &amp; Hierarchical Directories"

    if sec2_start in content and sec3_start in content:
        part1 = content.split(sec2_start)[0]
        remainder = content.split(sec3_start)[1]
        content = f"{part1}{EXPANDED_SECTIONS_BLOCK}\n\n    {sec3_start}{remainder}"
        print("--> Successfully expanded Section 2 (Address Spaces).")
    else:
        print("--> Warning: Could not cleanly locate Section 2 boundaries.")

    # Step 2: Replace Sections 4, 5, and 6
    sec4_start = "<h3>4. Input/Output (I/O) Subsystems</h3>"
    nav_bottom_start = "<!-- Navigation Bar Bottom -->"
    if nav_bottom_start not in content:
        nav_bottom_start = '<nav class="module-nav-bar bottom"'

    if sec4_start in content and nav_bottom_start in content:
        part_before_sec4 = content.split(sec4_start)[0]
        part_nav_bottom = content.split(nav_bottom_start)[1]
        content = f"{part_before_sec4}{EXPANDED_SECTIONS_FOUR_TO_SIX}\n\n    {nav_bottom_start}{part_nav_bottom}"
        print("--> Successfully expanded Sections 4, 5, and 6.")
    else:
        print("--> Warning: Could not cleanly locate Sections 4-6 boundaries.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Overwrote {TARGET_FILE} with OS-agnostic technical content.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand and generalize Sections 2, 4, 5, and 6 in Module 3\n\n"
            "Update 03-os-concepts.html to provide OS-agnostic treatments of memory\n"
            "architectures (paging, segmentation, single-level stores), I/O completion\n"
            "paradigms (IOCP, io_uring, CCWs), security models (DAC, MAC, capabilities),\n"
            "and command interpreters (POSIX, PowerShell, IBM JCL)."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for OS-agnostic expansion!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    expand_remaining_sections()
