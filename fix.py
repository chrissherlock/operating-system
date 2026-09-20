#!/usr/bin/env python3
# =====================================================================
# fix.py: Inject technical SVG diagrams into Module 2 and git sync
# =====================================================================
import os
import subprocess

SVG_MEMORY_PYRAMID = """
      <div style="display: flex; justify-content: center; margin: 24px 0;">
        <svg viewBox="0 0 760 380" width="100%" height="auto" style="max-width: 760px; font-family: ui-monospace, Menlo, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="gradReg" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#0284c7" />
              <stop offset="100%" stop-color="#38bdf8" />
            </linearGradient>
            <linearGradient id="gradCache" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#0369a1" />
              <stop offset="100%" stop-color="#0ea5e9" />
            </linearGradient>
            <linearGradient id="gradRAM" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#075985" />
              <stop offset="100%" stop-color="#0284c7" />
            </linearGradient>
            <linearGradient id="gradSSD" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#0c4a6e" />
              <stop offset="100%" stop-color="#0369a1" />
            </linearGradient>
            <linearGradient id="gradDisk" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#1e293b" />
              <stop offset="100%" stop-color="#334155" />
            </linearGradient>
            <marker id="arrowUp" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
              <path d="M0,6 L3,0 L6,6 Z" fill="#0284c7" />
            </marker>
            <marker id="arrowDown" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
              <path d="M0,0 L3,6 L6,0 Z" fill="#64748b" />
            </marker>
          </defs>

          <!-- Pyramid Slices -->
          <!-- Registers -->
          <polygon points="380,20 330,80 430,80" fill="url(#gradReg)" stroke="#ffffff" stroke-width="2" />
          <text x="380" y="62" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">Registers (&lt; 2 KB, &lt; 1 ns)</text>

          <!-- Cache -->
          <polygon points="330,80 270,150 490,150 430,80" fill="url(#gradCache)" stroke="#ffffff" stroke-width="2" />
          <text x="380" y="122" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">L1 / L2 / L3 Caches (SRAM, 1–15 ns)</text>

          <!-- Main Memory -->
          <polygon points="270,150 200,225 560,225 490,150" fill="url(#gradRAM)" stroke="#ffffff" stroke-width="2" />
          <text x="380" y="195" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">Main Memory (DRAM, 16–128 GB, 50–100 ns)</text>

          <!-- Solid-State Disk -->
          <polygon points="200,225 130,300 630,300 560,225" fill="url(#gradSSD)" stroke="#ffffff" stroke-width="2" />
          <text x="380" y="270" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">Solid-State Drives (NVMe / Flash, 10–50 μs)</text>

          <!-- Magnetic Disk -->
          <polygon points="130,300 60,370 700,370 630,300" fill="url(#gradDisk)" stroke="#ffffff" stroke-width="2" />
          <text x="380" y="342" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">Magnetic Disks / Archival (HDDs, 5–10 ms)</text>

          <!-- Side Indicators -->
          <!-- Left: Speed & Cost -->
          <line x1="45" y1="360" x2="45" y2="35" stroke="#0284c7" stroke-width="3" marker-end="url(#arrowUp)" />
          <text x="38" y="200" fill="#0284c7" font-size="11" font-weight="bold" transform="rotate(-90 38 200)" text-anchor="middle">HIGHER ACCESS SPEED &amp; COST / BIT</text>

          <!-- Right: Capacity -->
          <line x1="715" y1="35" x2="715" y2="360" stroke="#64748b" stroke-width="3" marker-end="url(#arrowDown)" />
          <text x="723" y="200" fill="#64748b" font-size="11" font-weight="bold" transform="rotate(90 723 200)" text-anchor="middle">LARGER CAPACITY &amp; PERSISTENCE</text>
        </svg>
      </div>
"""

SVG_TRAP_MODE = """
      <div style="display: flex; justify-content: center; margin: 24px 0;">
        <svg viewBox="0 0 740 260" width="100%" height="auto" style="max-width: 740px; font-family: ui-monospace, Menlo, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <!-- Background Boundaries -->
          <rect x="20" y="20" width="700" height="100" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="6,4" />
          <text x="35" y="45" fill="#64748b" font-size="11" font-weight="bold">USER SPACE (User Mode / Ring 3)</text>

          <rect x="20" y="140" width="700" height="100" rx="8" fill="#f0f9ff" stroke="#bae6fd" stroke-width="2" />
          <text x="35" y="165" fill="#0369a1" font-size="11" font-weight="bold">KERNEL SPACE (Kernel Mode / Ring 0)</text>

          <!-- Process Box -->
          <rect x="60" y="55" width="190" height="50" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1.5" />
          <text x="155" y="78" fill="#0f172a" font-size="12" font-weight="bold" text-anchor="middle">User Process</text>
          <text x="155" y="94" fill="#64748b" font-size="10" text-anchor="middle">Calls open() / read()</text>

          <!-- Hardware Transition Box -->
          <rect x="290" y="85" width="160" height="50" rx="6" fill="#0284c7" stroke="#0369a1" stroke-width="1.5" />
          <text x="370" y="107" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">TRAP / SYSCALL</text>
          <text x="370" y="123" fill="#e0f2fe" font-size="10" text-anchor="middle">Hardware CPU Mode Bit &rarr; 0</text>

          <!-- Kernel Box -->
          <rect x="490" y="170" width="190" height="55" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" />
          <text x="585" y="193" fill="#0369a1" font-size="12" font-weight="bold" text-anchor="middle">System Call Dispatcher</text>
          <text x="585" y="210" fill="#475569" font-size="10" text-anchor="middle">Execute Kernel Routine (IDT)</text>

          <!-- Path Arrows -->
          <!-- User to TRAP -->
          <path d="M 250,80 L 285,100" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowUp)" />
          <!-- TRAP to Kernel -->
          <path d="M 450,115 L 485,185" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowUp)" />
          <!-- Return Path -->
          <path d="M 490,205 C 360,240 240,160 160,110" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="4,4" />
          <text x="330" y="220" fill="#64748b" font-size="10" text-anchor="middle">IRET / SYSRET (Mode Bit &rarr; 1)</text>
        </svg>
      </div>
"""

SVG_DMA_ARCHITECTURE = """
      <div style="display: flex; justify-content: center; margin: 24px 0;">
        <svg viewBox="0 0 740 280" width="100%" height="auto" style="max-width: 740px; font-family: ui-monospace, Menlo, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <!-- CPU Box -->
          <rect x="40" y="30" width="140" height="70" rx="6" fill="#f8fafc" stroke="#0284c7" stroke-width="2" />
          <text x="110" y="62" fill="#0284c7" font-size="14" font-weight="bold" text-anchor="middle">CPU Core</text>
          <text x="110" y="82" fill="#64748b" font-size="10" text-anchor="middle">1. Sets up DMA transfer</text>

          <!-- DMA Controller Box -->
          <rect x="300" y="30" width="160" height="70" rx="6" fill="#0284c7" stroke="#0369a1" stroke-width="2" />
          <text x="380" y="62" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">DMA Controller</text>
          <text x="380" y="82" fill="#e0f2fe" font-size="10" text-anchor="middle">2. Manages direct bus flow</text>

          <!-- RAM Box -->
          <rect x="560" y="30" width="140" height="70" rx="6" fill="#f8fafc" stroke="#0284c7" stroke-width="2" />
          <text x="630" y="62" fill="#0284c7" font-size="14" font-weight="bold" text-anchor="middle">Main Memory</text>
          <text x="630" y="82" fill="#64748b" font-size="10" text-anchor="middle">Direct Buffer Destination</text>

          <!-- System Bus Bar -->
          <rect x="40" y="145" width="660" height="24" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.5" />
          <text x="370" y="161" fill="#475569" font-size="11" font-weight="bold" text-anchor="middle">SYSTEM &amp; MEMORY BUS (PCIe / DMI / Memory Channels)</text>

          <!-- Device Controller -->
          <rect x="300" y="200" width="160" height="60" rx="6" fill="#f8fafc" stroke="#64748b" stroke-width="1.5" />
          <text x="380" y="226" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">Device Controller</text>
          <text x="380" y="244" fill="#64748b" font-size="10" text-anchor="middle">(NVMe / Disk / NIC)</text>

          <!-- Vertical Interconnect Lines -->
          <line x1="110" y1="100" x2="110" y2="145" stroke="#0284c7" stroke-width="2" />
          <line x1="380" y1="100" x2="380" y2="145" stroke="#0284c7" stroke-width="2" />
          <line x1="630" y1="100" x2="630" y2="145" stroke="#0284c7" stroke-width="2" />
          <line x1="380" y1="169" x2="380" y2="200" stroke="#64748b" stroke-width="2" />

          <!-- Bulk Data Flow Curve -->
          <path d="M 460,230 C 580,230 630,190 630,105" fill="none" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="6,3" />
          <text x="595" y="245" fill="#0284c7" font-size="10" font-weight="bold">Direct Memory Stream (Bypasses CPU)</text>
        </svg>
      </div>
"""

def inject_diagrams_to_module2():
    target_file = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(target_file):
        print(f"Error: {target_file} not found.")
        return

    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Insert Memory Hierarchy diagram under Section 3
    if 'id="svg-memory-pyramid"' not in content:
        pos_mem = content.find("<h2>3. The Memory Hierarchy</h2>")
        if pos_mem != -1:
            end_p = content.find("</p>", pos_mem) + 4
            wrapped_pyramid = f'<div id="svg-memory-pyramid">{SVG_MEMORY_PYRAMID}</div>'
            content = content[:end_p] + wrapped_pyramid + content[end_p:]
            print("--> Added Memory Pyramid SVG diagram.")

    # 2. Insert Privilege / TRAP diagram under Section 2
    if 'id="svg-trap-diagram"' not in content:
        pos_trap = content.find("<h2>2. Privilege Modes &amp; Hardware Protection</h2>")
        if pos_trap != -1:
            end_p = content.find("</p>", pos_trap) + 4
            wrapped_trap = f'<div id="svg-trap-diagram">{SVG_TRAP_MODE}</div>'
            content = content[:end_p] + wrapped_trap + content[end_p:]
            print("--> Added TRAP / Privilege Modes SVG diagram.")

    # 3. Insert DMA architecture diagram under Section 4
    if 'id="svg-dma-diagram"' not in content:
        pos_dma = content.find("<h3>Three Fundamental I/O Approaches</h3>")
        if pos_dma != -1:
            wrapped_dma = f'<div id="svg-dma-diagram">{SVG_DMA_ARCHITECTURE}</div>'
            content = content[:pos_dma] + wrapped_dma + content[pos_dma:]
            print("--> Added DMA architecture SVG diagram.")

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)

    # Git sync
    try:
        subprocess.run(["git", "add", "fix.py", target_file], check=True)
        commit_msg = (
            "Add inline SVG diagrams for memory hierarchy, TRAP, and DMA in Module 2\n\n"
            "Update week01-operating-system-concepts/02-hardware-review.html with vector\n"
            "diagrams for memory hierarchy pyramid, kernel/user mode switching, and DMA."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    inject_diagrams_to_module2()
