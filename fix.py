#!/usr/bin/env python3
# =====================================================================
# fix.py: Overwrite Module 4 with standardized Stage Explanation label
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "04-os-structure.html"
)

FULL_HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>04. Operating System Structure | Week 1: Operating System Concepts</title>
  <style>
    :root {
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }
    body {
      font-family: var(--font-sans);
      color: #1e293b;
      background: #f8fafc;
      margin: 0;
      padding: 32px 16px;
      line-height: 1.6;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    h1, h2, h3, h4 {
      color: #0f172a;
    }
    h2 {
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 8px;
      margin-top: 28px;
    }
    h3 {
      margin-top: 20px;
      margin-bottom: 8px;
      color: #0284c7;
      font-size: 1.15rem;
    }
    h4 {
      margin-top: 16px;
      margin-bottom: 6px;
      font-size: 1rem;
      color: #334155;
    }
    p {
      color: #475569;
      margin-bottom: 12px;
    }
    ul, ol {
      margin-left: 20px;
      color: #475569;
      margin-bottom: 12px;
    }
    li {
      margin-bottom: 4px;
    }
    code {
      font-family: var(--font-mono);
      background: #f1f5f9;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.88rem;
      color: #0369a1;
    }
    pre {
      background: #0f172a;
      color: #e2e8f0;
      padding: 16px;
      border-radius: 6px;
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 0.85rem;
    }
    .diagram-container {
      display: flex;
      justify-content: center;
      margin: 24px 0;
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- Navigation Bar Top -->
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #cbd5e1;">
      <a href="03-os-concepts.html" class="module-nav-btn" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&larr; Previous: 03. OS Concepts</a>
      <a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">&#127968; Week 1: Operating System Concepts</a>
      <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">End of Week 1</span>
    </nav>

    <h2>04. Operating System Structure</h2>
    <p>
      An operating system is among the largest and most complex software systems engineered by humans. Because modern kernels encompass device drivers, virtual memory allocators, process schedulers, file systems, and network protocols, their internal structural design dictates their reliability, execution performance, security boundaries, and maintainability.
    </p>
    <p>
      Following the design philosophy outlined in <em>Operating Systems: Three Easy Pieces</em> (OSTEP), the central crux of operating system structure is balancing <strong>protection</strong> (preventing faulty components from crashing the entire system) against <strong>efficiency</strong> (minimizing hardware mode switches, address space context switches, and IPC overheads).
    </p>

    <!-- OSTEP Structural Crux Callout -->
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0284c7; padding: 16px; border-radius: 0 6px 6px 0; margin: 20px 0 28px 0;">
      <div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.88rem; color: #0369a1; text-transform: uppercase; margin-bottom: 4px;">THE CRUX: MODULARITY VS. PROTECTION AND PERFORMANCE</div>
      <p style="font-size: 0.9rem; color: #334155; margin: 0; line-height: 1.5;">
        How should operating system functionality be partitioned between privileged supervisor mode (Ring 0) and unprivileged user mode (Ring 3)? If all subsystems reside in Ring 0 for raw invocation speed, a single driver defect crashes the entire machine. If subsystems are moved to user space for fault isolation, how can the OS maintain acceptable performance in the presence of frequent cross-domain IPC and context switches?
      </p>
    </div>

    <h3>1. Monolithic Systems: Raw Performance &amp; Unified Space</h3>
    <p>
      In a classical <strong>monolithic architecture</strong>, the entire operating system executes as a single large binary image in privileged hardware mode (Ring 0 / Supervisor Mode). All primary components—including the process scheduler, virtual memory manager, VFS, networking stacks, and peripheral device drivers—share a single unified address space.
    </p>
    <p>
      Applications transition from unprivileged user mode into kernel mode using hardware trap instructions (<code>syscall</code> or <code>sysenter</code>). Once inside the kernel, internal subsystems interact via simple, high-speed C function calls with zero address-space switching overhead.
    </p>

    <h4>Architectural Properties of Monolithic Kernels</h4>
    <ul>
      <li><strong>Maximum Execution Speed:</strong> Subsystems exchange pointers directly in memory without marshalling data across protection boundaries or switching MMU translation page roots.</li>
      <li><strong>Absence of Fault Isolation:</strong> Because all kernel code shares a single flat memory space without memory protection rings between modules, an unhandled null-pointer dereference, buffer overrun, or wild write in any third-party device driver corrupts kernel memory and causes a fatal system panic or blue screen.</li>
      <li><strong>Loadable Kernel Modules (LKMs):</strong> Modern monolithic kernels (e.g., Linux, FreeBSD) mitigate monolithic inflexibility by supporting dynamically loaded binary objects (<code>.ko</code> files). Modules can be linked into kernel space on demand to support new hardware without requiring kernel recompilation, though they still execute with unconstrained Ring 0 privileges.</li>
    </ul>

    <!-- Diagram 1: Monolithic vs Microkernel SVG -->
    <div class="diagram-container">
      <svg viewBox="0 0 840 330" width="100%" height="100%" style="max-width: 840px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="mono-arrow" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#0284c7" />
          </marker>
          <marker id="ipc-arrow" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#9333ea" />
          </marker>
          <filter id="struct-shadow" x="-5%" y="-5%" width="110%" height="110%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.06" />
          </filter>
        </defs>

        <!-- Left: Monolithic Architecture -->
        <g transform="translate(30, 20)" filter="url(#struct-shadow)">
          <rect width="365" height="290" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" />
          <rect width="365" height="28" rx="6" fill="#f0f9ff" />
          <line x1="0" y1="28" x2="365" y2="28" stroke="#bae6fd" />
          <text x="182" y="19" fill="#0369a1" font-size="10.5" font-weight="700" text-anchor="middle">Monolithic Architecture (Linux / BSD)</text>

          <!-- User Space -->
          <rect x="20" y="42" width="325" height="50" rx="4" fill="#f8fafc" stroke="#cbd5e1" />
          <text x="182" y="62" fill="#0f172a" font-size="10" font-weight="700" text-anchor="middle">User Applications (Ring 3)</text>
          <text x="182" y="78" fill="#64748b" font-size="8.5" text-anchor="middle">Issues POSIX syscalls: read(), write(), fork()</text>

          <!-- System Call Trap Boundary -->
          <line x1="20" y1="108" x2="345" y2="108" stroke="#0284c7" stroke-width="2" stroke-dasharray="4,3" />
          <text x="182" y="104" fill="#0284c7" font-size="8" font-weight="700" text-anchor="middle">Hardware System Call Boundary (Trap)</text>

          <!-- Monolithic Ring 0 Kernel -->
          <rect x="20" y="118" width="325" height="150" rx="4" fill="#f0fdf4" stroke="#86efac" stroke-width="1.2" />
          <text x="182" y="136" fill="#15803d" font-size="10" font-weight="700" text-anchor="middle">Privileged Monolithic Kernel (Ring 0)</text>

          <g transform="translate(35, 146)">
            <rect x="0" y="0" width="88" height="32" rx="3" fill="#ffffff" stroke="#86efac" />
            <text x="44" y="20" fill="#166534" font-size="8" font-weight="600" text-anchor="middle">VFS / Ext4</text>

            <rect x="98" y="0" width="98" height="32" rx="3" fill="#ffffff" stroke="#86efac" />
            <text x="147" y="20" fill="#166534" font-size="8" font-weight="600" text-anchor="middle">TCP/IP Stack</text>

            <rect x="206" y="0" width="88" height="32" rx="3" fill="#ffffff" stroke="#86efac" />
            <text x="250" y="20" fill="#166534" font-size="8" font-weight="600" text-anchor="middle">Scheduler</text>

            <rect x="0" y="42" width="140" height="32" rx="3" fill="#ffffff" stroke="#86efac" />
            <text x="70" y="62" fill="#166534" font-size="8" font-weight="600" text-anchor="middle">Virtual Memory (Paging)</text>

            <rect x="150" y="42" width="144" height="32" rx="3" fill="#fee2e2" stroke="#ef4444" />
            <text x="222" y="62" fill="#991b1b" font-size="8" font-weight="700" text-anchor="middle">Device Drivers (PCIe, NVMe)</text>
          </g>
          <text x="182" y="258" fill="#991b1b" font-size="7.5" text-anchor="middle">&Delta; Single driver bug can panic entire kernel</text>
        </g>

        <!-- Right: Microkernel Architecture -->
        <g transform="translate(445, 20)" filter="url(#struct-shadow)">
          <rect width="365" height="290" rx="6" fill="#ffffff" stroke="#9333ea" stroke-width="1.5" />
          <rect width="365" height="28" rx="6" fill="#faf5ff" />
          <line x1="0" y1="28" x2="365" y2="28" stroke="#f3e8ff" />
          <text x="182" y="19" fill="#7e22ce" font-size="10.5" font-weight="700" text-anchor="middle">Microkernel Architecture (seL4 / QNX)</text>

          <!-- User Space Servers -->
          <rect x="20" y="42" width="325" height="142" rx="4" fill="#faf5ff" stroke="#e9d5ff" />
          <text x="182" y="58" fill="#581c87" font-size="9.5" font-weight="700" text-anchor="middle">User Space Servers (Ring 3 Isolated Processes)</text>

          <g transform="translate(32, 68)">
            <rect x="0" y="0" width="92" height="30" rx="3" fill="#ffffff" stroke="#c084fc" />
            <text x="46" y="19" fill="#6b21a8" font-size="8" font-weight="600" text-anchor="middle">Client App</text>

            <rect x="102" y="0" width="98" height="30" rx="3" fill="#ffffff" stroke="#c084fc" />
            <text x="151" y="19" fill="#6b21a8" font-size="8" font-weight="600" text-anchor="middle">File Server</text>

            <rect x="210" y="0" width="90" height="30" rx="3" fill="#ffffff" stroke="#c084fc" />
            <text x="255" y="19" fill="#6b21a8" font-size="8" font-weight="600" text-anchor="middle">Network Svc</text>

            <rect x="0" y="38" width="145" height="30" rx="3" fill="#ffffff" stroke="#c084fc" />
            <text x="72" y="57" fill="#6b21a8" font-size="8" font-weight="600" text-anchor="middle">NVMe Storage Driver</text>

            <rect x="155" y="38" width="145" height="30" rx="3" fill="#ffffff" stroke="#c084fc" />
            <text x="227" y="57" fill="#6b21a8" font-size="8" font-weight="600" text-anchor="middle">Display Server</text>
          </g>
          <text x="182" y="174" fill="#059669" font-size="7.5" text-anchor="middle">&checkmark; Driver crash only kills isolated user process</text>

          <!-- Microkernel Boundary -->
          <line x1="20" y1="198" x2="345" y2="198" stroke="#9333ea" stroke-width="2" stroke-dasharray="4,3" />
          <text x="182" y="194" fill="#7e22ce" font-size="8" font-weight="700" text-anchor="middle">Capability / IPC Trap Boundary</text>

          <!-- Minimalist Microkernel in Ring 0 -->
          <rect x="20" y="208" width="325" height="60" rx="4" fill="#f5f3ff" stroke="#a855f7" stroke-width="1.2" />
          <text x="182" y="226" fill="#6b21a8" font-size="9.5" font-weight="700" text-anchor="middle">Minimal Microkernel (Ring 0)</text>
          <text x="182" y="242" fill="#475569" font-size="8" text-anchor="middle">Address Space Switching • Fast IPC • Thread Dispatching</text>
          <text x="182" y="256" fill="#475569" font-size="8" text-anchor="middle">Interrupt Routing &amp; Hardware Capability Validation</text>
        </g>
      </svg>
    </div>

    <h3>2. Layered Systems &amp; Hierarchical Protection Rings</h3>
    <p>
      Pioneered by Edsger Dijkstra's <strong>THE multiprogramming system</strong> (1968), the layered approach organizes the operating system as a strict hierarchy of functional layers, numbered from 0 (the hardware core) to N (the user interface).
    </p>
    <p>
      Under a strict layered discipline, layer <em>M</em> can invoke routines and inspect data structures exclusively in layer <em>M</em> &minus; 1, and cannot access services in layer <em>M</em> + 1.
    </p>

    <!-- Classic THE Multiprogramming Layers -->
    <div style="overflow-x: auto; margin: 16px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; background: #ffffff;">
        <thead>
          <tr style="background: #f1f5f9; color: #1e293b;">
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1; width: 80px;">Layer</th>
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1; width: 220px;">Subsystem Responsibilities</th>
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Hardware / Architectural Abstraction</th>
          </tr>
        </thead>
        <tbody style="color: #334155;">
          <tr>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 700; text-anchor: center;">Layer 5</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">The Operator (Shell)</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">User commands, process creation, input/output redirection.</td>
          </tr>
          <tr style="background: #f8fafc;">
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 700; text-anchor: center;">Layer 4</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">User Programs</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Compilers, applications, math libraries operating within address spaces.</td>
          </tr>
          <tr>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 700; text-anchor: center;">Layer 3</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">I/O Device Buffering</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Buffering keyboard, printer, and tape streams; manages device synchronization.</td>
          </tr>
          <tr style="background: #f8fafc;">
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 700; text-anchor: center;">Layer 2</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">Operator Console</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Communication link between system operator and executing programs.</td>
          </tr>
          <tr>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 700; text-anchor: center;">Layer 1</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">Memory Management</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Allocates core memory and drum storage; handles swapping and page faults.</td>
          </tr>
          <tr style="background: #f8fafc;">
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 700; text-anchor: center;">Layer 0</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">CPU Scheduling &amp; Dispatch</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Hardware timer interrupts, semaphores, low-level process context switching.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>
      While conceptually pure, rigid layering rarely survives in production general-purpose kernels due to bidirectional dependencies. For instance, the virtual memory manager needs the backing file system to page dirty frames out to disk, while the file system needs the virtual memory manager to allocate physical cache buffers. Consequently, contemporary systems use layered concepts logically (such as POSIX VFS &rarr; Block Layer &rarr; Device Driver) rather than enforcing rigid execution boundaries.
    </p>

    <h3>3. Microkernels: Minimalist Privileged Core &amp; Capability IPC</h3>
    <p>
      The <strong>microkernel philosophy</strong> dictates that only mechanisms that strictly require supervisor privilege should remain in Ring 0. Everything else—including file systems, network protocol stacks, device drivers, and window managers—is stripped from the kernel and executed as separate, unprivileged user-space server processes.
    </p>
    <p>
      The microkernel core typically provides only four essential services:
    </p>
    <ol>
      <li><strong>Low-Level Thread Scheduling:</strong> Allocating CPU cores across threads.</li>
      <li><strong>Virtual Memory Translation:</strong> Setting up page tables and mapping hardware address spaces.</li>
      <li><strong>Hardware Interrupt Dispatch:</strong> Converting physical IRQs into asynchronous messages sent to user-space driver threads.</li>
      <li><strong>Inter-Process Communication (IPC):</strong> Providing fast, validated message passing and capability delegation so independent servers can communicate.</li>
    </ol>

    <h4>The Evolution: First-Generation (Mach) vs. Second-Generation (L4 / seL4)</h4>
    <p>
      Early microkernels like Carnegie Mellon's <strong>Mach</strong> suffered significant performance penalties. Servicing an I/O request required bouncing messages between user applications, the file server, the disk driver, and the kernel, incurring excessive TLB flushes and context switch overheads.
    </p>
    <p>
      Second-generation microkernels, pioneered by Jochen Liedtke's <strong>L4</strong> and formally verified systems like <strong>seL4</strong>, demonstrated that IPC overhead could be slashed by an order of magnitude. By using register-passed synchronous IPC, unforgeable capability nodes (Cnodes), and radical minimalist kernel footprints (under 10,000 lines of code), modern microkernels deliver high determinism and formal mathematical proofs of security enforcement.
    </p>

    <h3>4. Client-Server &amp; Hybrid Architectures (Windows NT &amp; macOS XNU)</h3>
    <p>
      Modern desktop and enterprise systems bridge the gap between monolithic throughput and microkernel isolation using <strong>hybrid architectures</strong>:
    </p>
    <ul>
      <li><strong>Windows NT Architecture:</strong> The NT kernel consists of the low-level <strong>Microkernel</strong> (responsible for thread dispatching, interrupt handling, and multiprocessor sync) and the surrounding <strong>NT Executive</strong> (providing object security, virtual memory, process tracking, and I/O request packet [IRP] routing). While both execute in Ring 0 for performance, user applications interact with the system via distinct <strong>Environment Subsystems</strong> (Win32, POSIX/WSL) running in user space as server processes (e.g., <code>csrss.exe</code>).</li>
      <li><strong>macOS XNU Kernel:</strong> Apple's XNU engine merges a customized fork of the <strong>Mach microkernel</strong> (for thread primitives, IPC, and virtual memory tasks) with the <strong>FreeBSD kernel</strong> (providing POSIX APIs, BSD process credentials, network sockets, and file systems) alongside the <strong>IOKit</strong> object-oriented C++ driver framework, all executing inside a single Ring 0 address space.</li>
    </ul>

    <h3>5. Exokernels &amp; Unikernels: End-to-End Application Customization</h3>
    <p>
      Developed at MIT by Dawson Engler and Frans Kaashoek, the <strong>exokernel architecture</strong> challenges the fundamental premise that operating systems should provide high-level abstractions (like files, sockets, and virtual address spaces).
    </p>
    <p>
      An exokernel provides <strong>zero high-level abstractions</strong>. Instead, its sole responsibility is to securely multiplex raw physical hardware resources (physical disk blocks, physical page frames, raw network packet descriptors) using hardware capabilities.
    </p>
    <ul>
      <li><strong>Library Operating Systems (LibOS):</strong> All traditional OS abstractions (e.g., an ext4 file system, a BSD TCP stack) are moved into standard user-space libraries linked directly with the application binary.</li>
      <li><strong>Application-Specific Optimization:</strong> A database engine can bypass conventional file system buffering and page replacement policies, implementing custom disk allocation algorithms optimized specifically for B-tree index traversal.</li>
      <li><strong>Unikernels (MirageOS, OSv):</strong> In cloud virtualization settings, the application code, language runtime, and library OS components are compiled into a single specialized image that executes directly on top of a hypervisor with no multi-user protections or shell, eliminating kernel-user mode transitions entirely.</li>
    </ul>

    <h3>6. Virtual Machines &amp; Hypervisors</h3>
    <p>
      Virtualization abstracts the physical hardware itself, allowing multiple independent guest operating systems to execute concurrently on a single physical machine:
    </p>
    <ul>
      <li><strong>Type-1 Bare-Metal Hypervisors (VMware ESXi, Xen, KVM):</strong> The hypervisor runs directly on the bare metal silicon in the most privileged hardware mode (e.g., VMX root mode on x86-64). Guest operating systems execute inside virtual machine containers with hardware traps intercepting sensitive CPU instructions.</li>
      <li><strong>Type-2 Hosted Hypervisors (VirtualBox, VMware Workstation):</strong> The hypervisor executes as an application atop an existing host operating system, relying on the host kernel for physical hardware drivers and scheduling.</li>
      <li><strong>Hardware Support (Intel VT-x / AMD-V):</strong> Modern CPUs incorporate dedicated hardware execution modes (Root vs. Non-Root) and hardware-managed control blocks (Virtual Machine Control Structure - VMCS) to handle <em>VM exits</em> and hardware-accelerated nested page tables (Extended Page Tables - EPT).</li>
    </ul>

    <h4>Comprehensive Comparison of Operating System Architectures</h4>
    <div style="overflow-x: auto; margin: 20px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; background: #ffffff;">
        <thead>
          <tr style="background: #f1f5f9; color: #1e293b;">
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Architecture Model</th>
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Privileged (Ring 0) Scope</th>
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Fault Isolation Boundary</th>
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Communication Mechanism</th>
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Real-World Examples</th>
          </tr>
        </thead>
        <tbody style="color: #334155;">
          <tr>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 700;">Monolithic</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">All services: VFS, Drivers, Network, Memory, Scheduling.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">User vs. Kernel boundary only. No intra-kernel isolation.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Direct C function calls and shared kernel pointers.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Linux, FreeBSD, OpenBSD.</td>
          </tr>
          <tr style="background: #f8fafc;">
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 700;">Microkernel</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Minimal primitives: Address spaces, Thread dispatch, IPC.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Isolated address space per server and driver process.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Synchronous/Asynchronous message-passing IPC.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">seL4, QNX Neutrino, Minix 3.</td>
          </tr>
          <tr>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 700;">Hybrid</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Microkernel core + OS Executive &amp; File Systems in Ring 0.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Environment subsystems isolated; core drivers in Ring 0.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Internal LPC/ALPC messaging and direct pointer routing.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Windows NT (11/Server), macOS XNU.</td>
          </tr>
          <tr style="background: #f8fafc;">
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 700;">Exokernel</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Hardware resource multiplexing &amp; capability checks only.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Complete application isolation; OS services linked as LibOS.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Direct hardware access via capability tokens.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">MIT Aegis, Xok, Nemesis.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- INTERACTIVE PEDAGOGICAL AID: DIRECTED NARRATIVE STEPPER -->
    <div id="interactive-os-stepper" style="margin: 36px 0; border: 1px solid #cbd5e1; border-radius: 8px; background: #ffffff; padding: 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 16px;">
        <div>
          <h3 style="margin: 0; color: #0284c7; font-size: 1.25rem;">Interactive Simulator: Cross-Architecture I/O Request Stepper</h3>
          <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Scenario: Application issues read() to fetch 4 KiB from an NVMe SSD across OS architectures.</p>
        </div>

        <!-- Comparative Dimension Toggles -->
        <div style="display: flex; gap: 6px;">
          <button type="button" class="arch-toggle active" data-arch="monolithic" style="padding: 6px 12px; font-size: 0.8rem; font-weight: 700; border-radius: 4px; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; cursor: pointer;">Monolithic</button>
          <button type="button" class="arch-toggle" data-arch="microkernel" style="padding: 6px 12px; font-size: 0.8rem; font-weight: 700; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">Microkernel</button>
          <button type="button" class="arch-toggle" data-arch="hybrid" style="padding: 6px 12px; font-size: 0.8rem; font-weight: 700; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">Hybrid (NT)</button>
          <button type="button" class="arch-toggle" data-arch="exokernel" style="padding: 6px 12px; font-size: 0.8rem; font-weight: 700; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">Exokernel</button>
        </div>
      </div>

      <!-- Live State Telemetry Status Bar -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 14px; margin-bottom: 18px; font-family: var(--font-mono); font-size: 0.8rem;">
        <div><span style="color: #64748b;">EXECUTION MODE:</span> <strong id="telemetry-mode" style="color: #0284c7;">USER MODE (RING 3)</strong></div>
        <div><span style="color: #64748b;">ACTIVE COMPONENT:</span> <strong id="telemetry-component" style="color: #059669;">APPLICATION RUNTIME</strong></div>
        <div><span style="color: #64748b;">CONTEXT SWITCHES:</span> <strong id="telemetry-switches" style="color: #475569;">0</strong></div>
        <div><span style="color: #64748b;">COMMUNICATION:</span> <strong id="telemetry-comm" style="color: #475569;">LOCAL CALL</strong></div>
      </div>

      <!-- Synchronized Visual Canvas -->
      <div style="display: flex; justify-content: center; background: #ffffff; border: 1px solid #f1f5f9; border-radius: 6px; padding: 12px; margin-bottom: 18px;">
        <svg id="arch-stepper-svg" viewBox="0 0 820 370" width="100%" height="100%" style="max-width: 820px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="arch-arrow-default" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
              <polygon points="0 1, 6 3.5, 0 6" fill="#94a3b8" />
            </marker>
            <marker id="arch-arrow-active" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
              <polygon points="0 1, 6 3.5, 0 6" fill="#0284c7" />
            </marker>
            <filter id="arch-active-glow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#0284c7" flood-opacity="0.6" />
            </filter>
          </defs>

          <!-- Ring 3 Boundary Zone (Top) -->
          <rect x="10" y="15" width="800" height="150" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-dasharray="4,4" />
          <text x="25" y="34" fill="#64748b" font-size="8.5" font-weight="700">USER MODE (RING 3 - UNPRIVILEGED)</text>

          <!-- Ring 0 Boundary Zone (Bottom) -->
          <rect x="10" y="180" width="800" height="175" rx="6" fill="#f0fdf4" stroke="#86efac" stroke-dasharray="4,4" />
          <text x="25" y="198" fill="#15803d" font-size="8.5" font-weight="700">KERNEL / SUPERVISOR MODE (RING 0 - PRIVILEGED)</text>

          <!-- Node 1: User Application (Ring 3) -->
          <g id="box-app" transform="translate(30, 50)">
            <rect width="130" height="85" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.8" />
            <text x="65" y="32" fill="#0f172a" font-size="10.5" font-weight="700" text-anchor="middle">User App</text>
            <text id="label-app-sub" x="65" y="50" fill="#64748b" font-size="8" text-anchor="middle">read(fd, buf)</text>
            <text x="65" y="68" fill="#0284c7" font-size="7.5" font-weight="600" text-anchor="middle">PID 4092</text>
          </g>

          <!-- Node 2: User-Space OS Service / LibOS (Ring 3) -->
          <g id="box-userservice" transform="translate(200, 50)">
            <rect width="165" height="85" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.8" />
            <text id="label-userservice-title" x="82" y="30" fill="#0f172a" font-size="10" font-weight="700" text-anchor="middle">User Service</text>
            <text id="label-userservice-sub" x="82" y="48" fill="#64748b" font-size="8" text-anchor="middle">Inactive in Monolithic</text>
            <rect id="badge-userservice" x="25" y="58" width="115" height="18" rx="3" fill="#f1f5f9" stroke="#cbd5e1" />
            <text id="label-userservice-badge" x="82" y="70" fill="#475569" font-size="7.5" text-anchor="middle">POSIX Library</text>
          </g>

          <!-- Node 3: User-Space Driver (Used in Microkernel) -->
          <g id="box-userdriver" transform="translate(410, 50)">
            <rect width="165" height="85" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.8" />
            <text id="label-userdriver-title" x="82" y="30" fill="#0f172a" font-size="10" font-weight="700" text-anchor="middle">User Driver</text>
            <text id="label-userdriver-sub" x="82" y="48" fill="#64748b" font-size="8" text-anchor="middle">Ring 3 Server</text>
            <rect id="badge-userdriver" x="25" y="58" width="115" height="18" rx="3" fill="#f1f5f9" stroke="#cbd5e1" />
            <text id="label-userdriver-badge" x="82" y="70" fill="#475569" font-size="7.5" text-anchor="middle">Capability MMIO</text>
          </g>

          <!-- Node 4: Kernel Core / Executive (Ring 0) -->
          <g id="box-kernel" transform="translate(200, 220)">
            <rect width="165" height="95" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.8" />
            <text id="label-kernel-title" x="82" y="30" fill="#0f172a" font-size="10" font-weight="700" text-anchor="middle">Kernel Core</text>
            <text id="label-kernel-sub" x="82" y="48" fill="#64748b" font-size="8" text-anchor="middle">VFS &amp; Subsystems</text>
            <rect id="badge-kernel" x="20" y="62" width="125" height="20" rx="3" fill="#ecfdf5" stroke="#a7f3d0" />
            <text id="label-kernel-badge" x="82" y="75" fill="#065f46" font-size="7.5" font-weight="600" text-anchor="middle">Ring 0 Supervisor</text>
          </g>

          <!-- Node 5: Kernel Device Driver (Ring 0 - Monolithic / Hybrid) -->
          <g id="box-kerneldriver" transform="translate(410, 220)">
            <rect width="165" height="95" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.8" />
            <text id="label-kerneldriver-title" x="82" y="30" fill="#0f172a" font-size="10" font-weight="700" text-anchor="middle">NVMe Driver</text>
            <text id="label-kerneldriver-sub" x="82" y="48" fill="#64748b" font-size="8" text-anchor="middle">Ring 0 Driver Module</text>
            <rect id="badge-kerneldriver" x="20" y="62" width="125" height="20" rx="3" fill="#ecfdf5" stroke="#a7f3d0" />
            <text id="label-kerneldriver-badge" x="82" y="75" fill="#065f46" font-size="7.5" font-weight="600" text-anchor="middle">Direct Bus Master</text>
          </g>

          <!-- Node 6: Physical NVMe Storage Hardware -->
          <g id="box-hardware" transform="translate(640, 130)">
            <rect width="145" height="110" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" />
            <rect width="145" height="24" rx="6" fill="#f8fafc" />
            <text x="72" y="16" fill="#475569" font-size="8.5" font-weight="700" text-anchor="middle">PHYSICAL DEVICE</text>
            <text x="72" y="50" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">NVMe SSD</text>
            <text x="72" y="68" fill="#64748b" font-size="8" text-anchor="middle">PCIe Gen4 x4 Bus</text>
            <rect x="15" y="80" width="115" height="20" rx="3" fill="#fef3c7" stroke="#fde68a" />
            <text x="72" y="93" fill="#92400e" font-size="7.5" font-weight="600" text-anchor="middle">Flash NAND Blocks</text>
          </g>

          <!-- Connecting Paths -->
          <!-- P1: App -> Kernel Syscall Trap -->
          <path id="path-app-kernel-trap" d="M 95,135 L 95,265 L 195,265" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arch-arrow-default)" />

          <!-- P2: App -> User Service (IPC / LibOS) -->
          <path id="path-app-userservice" d="M 160,92 L 195,92" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arch-arrow-default)" />

          <!-- P3: User Service -> Kernel (IPC / Cap Trap) -->
          <path id="path-userservice-kernel" d="M 282,135 L 282,215" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arch-arrow-default)" />

          <!-- P4: Kernel -> User Driver (Microkernel Driver IPC) -->
          <path id="path-kernel-userdriver" d="M 365,245 C 440,245 440,165 440,140" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arch-arrow-default)" />

          <!-- P5: Kernel -> Kernel Driver (Monolithic / Hybrid Direct Call) -->
          <path id="path-kernel-driver" d="M 365,265 L 405,265" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arch-arrow-default)" />

          <!-- P6: Kernel Driver -> Hardware (MMIO Doorbell) -->
          <path id="path-driver-hw" d="M 575,265 L 600,265 L 600,195 L 635,195" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arch-arrow-default)" />

          <!-- P7: User Driver -> Hardware (Direct via Cap) -->
          <path id="path-userdriver-hw" d="M 575,92 L 600,92 L 600,170 L 635,170" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arch-arrow-default)" />
        </svg>
      </div>

      <!-- Foreshadowed Navigation & Controls -->
      <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 20px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 16px;">
        <div style="display: flex; gap: 8px;">
          <button type="button" id="btn-arch-prev" style="padding: 6px 14px; font-weight: 600; font-size: 0.85rem; border: 1px solid #cbd5e1; background: #ffffff; color: #334155; border-radius: 5px; cursor: pointer;">&larr; Prev</button>
          <button type="button" id="btn-arch-next" style="padding: 6px 14px; font-weight: 600; font-size: 0.85rem; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; border-radius: 5px; cursor: pointer;">Next Step &rarr;</button>
          <button type="button" id="btn-arch-reset" style="padding: 6px 12px; font-size: 0.85rem; border: 1px solid #cbd5e1; background: #ffffff; color: #64748b; border-radius: 5px; cursor: pointer;">Reset</button>
        </div>

        <!-- Inline Preview of Active Step (Stage Explanation) -->
        <div style="font-size: 0.85rem; color: #334155;">
          <span style="color: #64748b; font-weight: 600;">Stage Explanation:</span> <span id="arch-preview-text" style="font-weight: 700; color: #0284c7;">Application executes syscall trap into kernel mode</span>
        </div>
      </div>

      <!-- Paired Analytical Panes (Strict Mechanics vs. Rationale) -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
        <!-- Pane 1: Mechanics -->
        <div style="border: 1px solid #bae6fd; background: #f0f9ff; border-radius: 6px; padding: 16px;">
          <div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.85rem; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">1. What Is Happening (Low-Level Mechanics)</div>
          <div id="arch-pane-mechanics" style="font-size: 0.9rem; color: #1e293b; line-height: 1.5;"></div>
        </div>

        <!-- Pane 2: Rationale -->
        <div style="border: 1px solid #fde68a; background: #fffbeb; border-radius: 6px; padding: 16px;">
          <div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.85rem; color: #92400e; text-transform: uppercase; margin-bottom: 6px;">2. Why The System Does This (Design Rationale)</div>
          <div id="arch-pane-rationale" style="font-size: 0.9rem; color: #78350f; line-height: 1.5;"></div>
        </div>
      </div>

      <!-- Dedicated Contextual Definitions Section -->
      <div style="border: 1px solid #e2e8f0; background: #f8fafc; border-radius: 6px; padding: 16px;">
        <div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.85rem; color: #475569; text-transform: uppercase; margin-bottom: 8px;">Contextual Definitions &amp; Architectural Concepts</div>
        <div id="arch-pane-definitions" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 12px;"></div>
      </div>
    </div>

    <!-- Stepper Logic Script -->
    <script>
      (function() {
        const archWorkflows = {
          "monolithic": [
            {
              mode: "USER MODE (RING 3)",
              component: "USER APPLICATION",
              switches: "0",
              comm: "LOCAL CALL",
              activeBox: "box-app",
              activePath: "path-app-kernel-trap",
              preview: "App traps into kernel via syscall instruction",
              mechanics: "The application passes parameters in registers (RAX=0 for sys_read, RDI=fd, RSI=buf) and executes the syscall instruction, switching CPU execution to Ring 0.",
              rationale: "Limited Direct Execution allows native CPU performance for computation while interposing hardware gates for privileged storage operations.",
              definitions: [
                { term: "Limited Direct Execution (LDE)", desc: "Running user code directly on raw CPU hardware while trapping into supervisor mode for privileged operations." },
                { term: "Syscall Gate", desc: "A hardware-enforced CPU transition mechanism that switches execution privilege levels from Ring 3 to Ring 0." }
              ]
            },
            {
              mode: "KERNEL MODE (RING 0)",
              component: "VFS & EXT4 FILE SYSTEM",
              switches: "0 (SAME ADDRESS SPACE)",
              comm: "DIRECT C FUNCTION CALL",
              activeBox: "box-kernel",
              activePath: "path-kernel-driver",
              preview: "VFS resolves inode and passes request directly to NVMe block driver",
              mechanics: "The Virtual File System validates file descriptors, calculates logical block addresses (LBAs) via extent trees, and invokes the NVMe driver via a standard C function pointer.",
              rationale: "Zero address-space switches. All subsystems share a single contiguous supervisor address space, eliminating translation buffer invalidations.",
              definitions: [
                { term: "Virtual File System (VFS)", desc: "The kernel abstraction layer providing standardized POSIX file operations atop diverse underlying filesystem drivers." },
                { term: "Function Pointer Dispatch", desc: "Executing module routines directly via in-memory pointers without inter-process message passing." }
              ]
            },
            {
              mode: "KERNEL MODE (RING 0)",
              component: "NVMe DRIVER & CONTROLLER",
              switches: "0 (SAME CONTEXT)",
              comm: "MMIO DOORBELL WRITE",
              activeBox: "box-kerneldriver",
              activePath: "path-driver-hw",
              preview: "Driver writes submission descriptor to NVMe hardware doorbell",
              mechanics: "The driver constructs a 64-byte command descriptor in DMA host memory and writes the new tail pointer to the controller's memory-mapped I/O (MMIO) register.",
              rationale: "Direct memory-mapped hardware access maximizes storage I/O operations per second (IOPS) with absolute minimum latency.",
              definitions: [
                { term: "Memory-Mapped I/O (MMIO)", desc: "Mapping device controller registers directly into the CPU physical address space for register access via standard store instructions." },
                { term: "Direct Memory Access (DMA)", desc: "Hardware capability allowing storage controllers to stream data directly into host DRAM without CPU cycle consumption." }
              ]
            }
          ],
          "microkernel": [
            {
              mode: "USER MODE (RING 3)",
              component: "USER APPLICATION",
              switches: "0",
              comm: "LOCAL STUB",
              activeBox: "box-app",
              activePath: "path-app-userservice",
              preview: "App formats message and issues IPC call to File System Server",
              mechanics: "The application encodes the read request into a standardized IPC message buffer and transfers execution to the isolated File System Server process.",
              rationale: "Microkernels strip file system logic out of the supervisor core; user applications communicate with independent service daemons.",
              definitions: [
                { term: "User-Space Server", desc: "A system service (e.g. file system or network stack) executing as an isolated unprivileged user process in Ring 3." },
                { term: "Message Marshalling", desc: "Serializing parameters into a standardized buffer for inter-process communication across isolated address spaces." }
              ]
            },
            {
              mode: "USER MODE (RING 3)",
              component: "FILE SYSTEM SERVER",
              switches: "2 (APP -> KERN -> FS)",
              comm: "SYNCHRONOUS IPC VIA MICROKERNEL",
              activeBox: "box-userservice",
              activePath: "path-userservice-kernel",
              preview: "FS server translates request and invokes kernel to route IPC to driver",
              mechanics: "The microkernel switches page tables (CR3 swap) to run the File System Server. The server translates the path to block offsets and calls microkernel IPC to signal the driver.",
              rationale: "Fault isolation: if the file system server crashes, the core kernel and hardware device drivers remain fully operational and unaffected.",
              definitions: [
                { term: "Address Space Switch", desc: "Reloading CPU page directory registers (CR3/TTBR0), invalidating cached TLB address translations." },
                { term: "Fault Domain Isolation", desc: "Confining software failures to an unprivileged container so bugs cannot crash the operating system." }
              ]
            },
            {
              mode: "USER MODE (RING 3)",
              component: "USER-SPACE NVMe DRIVER",
              switches: "4 (FS -> KERN -> DRV)",
              comm: "CAPABILITY-PROTECTED MMIO",
              activeBox: "box-userdriver",
              activePath: "path-userdriver-hw",
              preview: "Driver accesses controller MMIO registers via kernel capability",
              mechanics: "The user-space driver receives the IPC packet. Using physical memory pages explicitly mapped by the microkernel via capability tokens, it writes the NVMe doorbell.",
              rationale: "Running device drivers in user space protects against hardware driver bugs, which account for the vast majority of operating system crashes.",
              definitions: [
                { term: "User-Space Device Driver", desc: "A device driver running in Ring 3 that interacts with hardware strictly through capability-authorized MMIO regions." },
                { term: "Capability Token", desc: "An unforgeable cryptographic or kernel-held authority token granting access to a specific system or hardware resource." }
              ]
            }
          ],
          "hybrid": [
            {
              mode: "USER MODE (RING 3)",
              component: "USER APPLICATION",
              switches: "0",
              comm: "WIN32 SUBSYSTEM CALL",
              activeBox: "box-app",
              activePath: "path-app-kernel-trap",
              preview: "App calls ReadFile() and traps into NT Executive via ntdll.dll",
              mechanics: "The application calls Win32 ReadFile(). System DLLs construct arguments and invoke NtReadFile() in ntdll.dll, executing a syscall trap into Ring 0.",
              rationale: "Separates OS environment personalities (Win32, POSIX) from core kernel primitives while maintaining high-speed entry.",
              definitions: [
                { term: "Environment Subsystem", desc: "User-mode processes (such as csrss.exe) that present specific operating system personalities to applications." },
                { term: "Native API (ntdll.dll)", desc: "The foundational user-mode interface bridging subsystem DLLs directly to the Windows NT Executive." }
              ]
            },
            {
              mode: "KERNEL MODE (RING 0)",
              component: "NT EXECUTIVE & I/O MANAGER",
              switches: "0 (NO ADDRESS SWITCH)",
              comm: "I/O REQUEST PACKET (IRP)",
              activeBox: "box-kernel",
              activePath: "path-kernel-driver",
              preview: "I/O Manager creates IRP and routes it down the layered driver stack",
              mechanics: "The I/O Manager allocates an I/O Request Packet (IRP) representing the read operation and passes it down a chain of filter and filesystem drivers.",
              rationale: "Layered IRP dispatching allows volume management, disk encryption (BitLocker), and antivirus filters to intercept data transparently.",
              definitions: [
                { term: "I/O Request Packet (IRP)", desc: "The core data structure in Windows NT representing an asynchronous I/O transaction through driver stacks." },
                { term: "Layered Driver Model", desc: "Organizing drivers in vertical stacks where each layer performs processing before delegating downward." }
              ]
            },
            {
              mode: "KERNEL MODE (RING 0)",
              component: "STORPORT & NVMe MINI-PORT",
              switches: "0 (SAME CONTEXT)",
              comm: "DIRECT CONTROLLER ACCESS",
              activeBox: "box-kerneldriver",
              activePath: "path-driver-hw",
              preview: "Miniport driver submits command directly to NVMe hardware queue",
              mechanics: "The Storport driver routes the IRP to the NVMe miniport driver, which builds submission queue entries in DMA space and rings the controller doorbell.",
              rationale: "Executes performance-critical hardware drivers in Ring 0 to match monolithic throughput while retaining structured layered abstractions.",
              definitions: [
                { term: "Miniport Driver", desc: "A specialized hardware driver handling device silicon while an OS class driver handles generic OS protocols." },
                { term: "Doorbell Register", desc: "A memory-mapped register used by the host CPU to notify an NVMe controller of new pending commands." }
              ]
            }
          ],
          "exokernel": [
            {
              mode: "USER MODE (RING 3)",
              component: "APPLICATION + LIBOS",
              switches: "0",
              comm: "IN-PROCESS LIBRARY CALL",
              activeBox: "box-userservice",
              activePath: "path-userservice-kernel",
              preview: "LibOS calculates exact physical block and formats capability request",
              mechanics: "The application calls its statically linked Library OS (LibOS). The LibOS calculates the raw physical disk sector and formats a capability token.",
              rationale: "Eliminates centralized kernel abstractions. The application customizes disk layout, cache management, and data indexing directly.",
              definitions: [
                { term: "Library OS (LibOS)", desc: "Operating system services (such as file systems or network stacks) compiled directly into an application binary." },
                { term: "End-to-End Argument", desc: "The systems principle stating that application-specific functions are best implemented in application space rather than in the kernel." }
              ]
            },
            {
              mode: "KERNEL MODE (RING 0)",
              component: "EXOKERNEL CORE",
              switches: "0",
              comm: "CAPABILITY VALIDATION",
              activeBox: "box-kernel",
              activePath: "path-driver-hw",
              preview: "Exokernel verifies capability and gives hardware direct access",
              mechanics: "The tiny exokernel verifies that the calling LibOS possesses the capability key for the target physical block. Once validated, it triggers the transfer.",
              rationale: "Separates protection from management: the exokernel enforces isolation and hardware multiplexing, while the LibOS manages all policies.",
              definitions: [
                { term: "Protection vs. Management", desc: "The exokernel doctrine: the kernel only enforces resource bounds; applications manage all policies." },
                { term: "Secure Binding", desc: "Hardware or software mechanism that locks a resource to an application without runtime kernel intervention." }
              ]
            }
          ]
        };

        let currentArch = "monolithic";
        let currentStep = 0;

        function refreshArchView() {
          const archData = archWorkflows[currentArch];
          if (currentStep >= archData.length) currentStep = 0;
          const stepData = archData[currentStep];

          // 1. Update Telemetry
          document.getElementById("telemetry-mode").textContent = stepData.mode;
          document.getElementById("telemetry-component").textContent = stepData.component;
          document.getElementById("telemetry-switches").textContent = stepData.switches;
          document.getElementById("telemetry-comm").textContent = stepData.comm;

          // 2. Update Narrative Panes
          document.getElementById("arch-preview-text").textContent = stepData.preview;
          document.getElementById("arch-pane-mechanics").textContent = stepData.mechanics;
          document.getElementById("arch-pane-rationale").textContent = stepData.rationale;

          // 3. Render Dedicated Definitions Container
          const defsContainer = document.getElementById("arch-pane-definitions");
          defsContainer.innerHTML = "";
          stepData.definitions.forEach(item => {
            const card = document.createElement("div");
            card.style.background = "#ffffff";
            card.style.border = "1px solid #cbd5e1";
            card.style.borderRadius = "4px";
            card.style.padding = "10px 12px";
            card.innerHTML = `<div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.85rem; color: #0284c7; margin-bottom: 4px;">${item.term}</div><div style="font-size: 0.85rem; color: #475569; line-height: 1.4;">${item.desc}</div>`;
            defsContainer.appendChild(card);
          });

          // 4. Update Node Labels and Visibility by Architecture
          const userServ = document.getElementById("box-userservice");
          const userDrv = document.getElementById("box-userdriver");
          const kernDrv = document.getElementById("box-kerneldriver");
          const kernCore = document.getElementById("box-kernel");

          if (currentArch === "monolithic") {
            userServ.style.opacity = "0.35";
            document.getElementById("label-userservice-title").textContent = "User Service (N/A)";
            document.getElementById("label-userservice-sub").textContent = "In Kernel";
            userDrv.style.opacity = "0.35";
            document.getElementById("label-userdriver-title").textContent = "User Driver (N/A)";
            document.getElementById("label-userdriver-sub").textContent = "In Kernel";
            kernDrv.style.opacity = "1.0";
            document.getElementById("label-kernel-title").textContent = "VFS & Ext4";
            document.getElementById("label-kernel-sub").textContent = "Monolithic Ring 0";
          } else if (currentArch === "microkernel") {
            userServ.style.opacity = "1.0";
            document.getElementById("label-userservice-title").textContent = "File Server";
            document.getElementById("label-userservice-sub").textContent = "User Process (Ring 3)";
            userDrv.style.opacity = "1.0";
            document.getElementById("label-userdriver-title").textContent = "NVMe Driver";
            document.getElementById("label-userdriver-sub").textContent = "User Process (Ring 3)";
            kernDrv.style.opacity = "0.35";
            document.getElementById("label-kernel-title").textContent = "Minimal Microkernel";
            document.getElementById("label-kernel-sub").textContent = "IPC & Scheduling";
          } else if (currentArch === "hybrid") {
            userServ.style.opacity = "0.35";
            document.getElementById("label-userservice-title").textContent = "Subsystem (csrss)";
            document.getElementById("label-userservice-sub").textContent = "User Mode Personality";
            userDrv.style.opacity = "0.35";
            document.getElementById("label-userdriver-title").textContent = "User Driver (UMDF)";
            document.getElementById("label-userdriver-sub").textContent = "Not Used for Disk";
            kernDrv.style.opacity = "1.0";
            document.getElementById("label-kernel-title").textContent = "NT Executive & VFS";
            document.getElementById("label-kernel-sub").textContent = "Ring 0 Subsystems";
          } else if (currentArch === "exokernel") {
            userServ.style.opacity = "1.0";
            document.getElementById("label-userservice-title").textContent = "App Library OS";
            document.getElementById("label-userservice-sub").textContent = "In-Process LibOS";
            userDrv.style.opacity = "0.35";
            document.getElementById("label-userdriver-title").textContent = "User Driver (N/A)";
            document.getElementById("label-userdriver-sub").textContent = "Direct Cap Access";
            kernDrv.style.opacity = "0.35";
            document.getElementById("label-kernel-title").textContent = "Exokernel Core";
            document.getElementById("label-kernel-sub").textContent = "Capability Gate";
          }

          // 5. Highlight Active Box
          const allBoxes = ["box-app", "box-userservice", "box-userdriver", "box-kernel", "box-kerneldriver", "box-hardware"];
          allBoxes.forEach(bid => {
            const el = document.getElementById(bid);
            if (el) {
              const rect = el.querySelector("rect");
              if (rect) {
                rect.removeAttribute("filter");
                rect.style.strokeWidth = "1.8px";
                rect.style.stroke = "#cbd5e1";
              }
            }
          });

          const activeEl = document.getElementById(stepData.activeBox);
          if (activeEl) {
            const rect = activeEl.querySelector("rect");
            if (rect) {
              rect.setAttribute("filter", "url(#arch-active-glow)");
              rect.style.strokeWidth = "3px";
              rect.style.stroke = "#0284c7";
            }
          }

          // 6. Highlight Active Path & Marker
          const allPaths = [
            "path-app-kernel-trap", "path-app-userservice", "path-userservice-kernel",
            "path-kernel-userdriver", "path-kernel-driver", "path-driver-hw", "path-userdriver-hw"
          ];
          allPaths.forEach(pid => {
            const pel = document.getElementById(pid);
            if (pel) {
              pel.style.stroke = "#cbd5e1";
              pel.style.strokeWidth = "2px";
              pel.setAttribute("marker-end", "url(#arch-arrow-default)");
            }
          });

          if (stepData.activePath) {
            const activePel = document.getElementById(stepData.activePath);
            if (activePel) {
              activePel.style.stroke = "#0284c7";
              activePel.style.strokeWidth = "3.2px";
              activePel.setAttribute("marker-end", "url(#arch-arrow-active)");
            }
          }
        }

        // Toggle Buttons
        document.querySelectorAll(".arch-toggle").forEach(btn => {
          btn.addEventListener("click", function() {
            document.querySelectorAll(".arch-toggle").forEach(b => {
              b.style.background = "#ffffff";
              b.style.color = "#475569";
              b.style.borderColor = "#cbd5e1";
            });
            this.style.background = "#0284c7";
            this.style.color = "#ffffff";
            this.style.borderColor = "#0284c7";
            currentArch = this.getAttribute("data-arch");
            currentStep = 0;
            refreshArchView();
          });
        });

        // Stepper Navigation
        document.getElementById("btn-arch-next").addEventListener("click", function() {
          currentStep = (currentStep + 1) % archWorkflows[currentArch].length;
          refreshArchView();
        });

        document.getElementById("btn-arch-prev").addEventListener("click", function() {
          currentStep = (currentStep - 1 + archWorkflows[currentArch].length) % archWorkflows[currentArch].length;
          refreshArchView();
        });

        document.getElementById("btn-arch-reset").addEventListener("click", function() {
          currentStep = 0;
          refreshArchView();
        });

        // Initial Paint
        refreshArchView();
      })();
    </script>

    <!-- Navigation Bar Bottom -->
    <nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 12px; border-top: 1px solid #cbd5e1;">
      <a href="03-os-concepts.html" class="module-nav-btn" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem;">&larr; Previous: 03. OS Concepts</a>
      <a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">&#127968; Week 1: Operating System Concepts</a>
      <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">End of Week 1</span>
    </nav>
  </div>
</body>
</html>
"""

def overwrite_module_four():
    os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(FULL_HTML_CONTENT.strip() + "\n")

    print(f"--> Successfully updated {TARGET_FILE} with standardized Stage Explanation label.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Update Module 4 OS Structure with standardized Stage Explanation label\n\n"
            "Replace Module 4 file 04-os-structure.html with full markup featuring clean\n"
            "Stage Explanation labels and robust cross-architecture stepper logic."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    overwrite_module_four()
