#!/usr/bin/env python3
# =====================================================================
# fix.py: Add top-level system architecture overview SVG diagram
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def add_system_architecture_diagram():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Target right after the header element
    target_header_end = '</header>'

    architecture_diagram_html = """    </header>

    <!-- High-Level System Architecture Overview Diagram -->
    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
      <h3 style="margin-top: 0; color: #0f172a; font-size: 1.1rem; font-weight: 700;">System Architecture Overview</h3>
      <p style="color: #334155; font-size: 0.92rem; line-height: 1.5; margin-bottom: 16px;">
        The diagram below maps out how the core hardware subsystems covered in this module connect—from CPU execution engines and memory hierarchies down to system buses, storage controllers, and boot firmware.
      </p>

      <div style="display: flex; justify-content: center; overflow-x: auto;">
        <svg viewBox="0 0 940 320" width="100%" height="100%" style="max-width: 940px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="arch-arrow" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#0284c7" />
            </marker>
          </defs>

          <!-- CPU & Cores Box -->
          <g transform="translate(30, 20)">
            <rect x="0" y="0" width="260" height="120" rx="8" fill="#f0f9ff" stroke="#0284c7" stroke-width="2" />
            <text x="130" y="24" fill="#0369a1" font-size="11" font-weight="700" text-anchor="middle">1. PROCESSORS &amp; PIPELINING</text>
            <text x="130" y="48" fill="#0f172a" font-size="10" font-weight="700" text-anchor="middle">CPU Core 0 &amp; Core 1</text>
            <text x="130" y="68" fill="#475569" font-size="9" text-anchor="middle">Fetch • Decode • Execute • WB</text>
            <text x="130" y="88" fill="#475569" font-size="9" text-anchor="middle">Privilege Levels (Ring 0 / Ring 3)</text>
            <text x="130" y="104" fill="#64748b" font-size="8.5" font-style="italic" text-anchor="middle">Superscalar &amp; Multicore Execution</text>
          </g>

          <!-- Memory Hierarchy & MMU Box -->
          <g transform="translate(340, 20)">
            <rect x="0" y="0" width="260" height="120" rx="8" fill="#ecfdf5" stroke="#059669" stroke-width="2" />
            <text x="130" y="24" fill="#047857" font-size="11" font-weight="700" text-anchor="middle">3. VIRTUAL MEMORY &amp; MMU</text>
            <text x="130" y="48" fill="#065f46" font-size="10" font-weight="700" text-anchor="middle">CR3 Root &amp; Page Table Walk</text>
            <text x="130" y="68" fill="#047857" font-size="9" text-anchor="middle">PML4 &rarr; PDPT &rarr; PD &rarr; PT</text>
            <text x="130" y="88" fill="#047857" font-size="9" text-anchor="middle">2 MiB Superpages &amp; Offset Bypass</text>
            <text x="130" y="104" fill="#065f46" font-size="8.5" font-style="italic" text-anchor="middle">Physical DRAM Frame Mapping</text>
          </g>

          <!-- I/O & Controllers Box -->
          <g transform="translate(650, 20)">
            <rect x="0" y="0" width="260" height="120" rx="8" fill="#fef3c7" stroke="#d97706" stroke-width="2" />
            <text x="130" y="24" fill="#b45309" font-size="11" font-weight="700" text-anchor="middle">4. DISKS &amp; I/O CONTROLLERS</text>
            <text x="130" y="48" fill="#78350f" font-size="10" font-weight="700" text-anchor="middle">Device Drivers &amp; MMIO/PMIO</text>
            <text x="130" y="68" fill="#92400e" font-size="9" text-anchor="middle">Direct Memory Access (DMA)</text>
            <text x="130" y="88" fill="#92400e" font-size="9" text-anchor="middle">NVMe Storage &amp; Peripherals</text>
            <text x="130" y="104" fill="#b45309" font-size="8.5" font-style="italic" text-anchor="middle">High-Speed Bus Controllers</text>
          </g>

          <!-- Connecting Bus Backbone -->
          <rect x="30" y="165" width="880" height="40" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2" />
          <text x="470" y="182" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">5. SYSTEM BUS TOPOLOGY &amp; INTERCONNECTS</text>
          <text x="470" y="197" fill="#64748b" font-size="9" text-anchor="middle">High-Speed Memory Bus • PCIe Serial Lanes • SPI / LPC Firmware Bus</text>

          <!-- Arrows between CPU, Memory, I/O and Bus Backbone -->
          <path d="M 160,140 L 160,165" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arch-arrow)" />
          <path d="M 470,140 L 470,165" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#arch-arrow)" />
          <path d="M 780,140 L 780,165" fill="none" stroke="#d97706" stroke-width="2" marker-end="url(#arch-arrow)" />

          <!-- Boot Process / Firmware Foundation Box -->
          <g transform="translate(180, 235)">
            <rect x="0" y="0" width="580" height="60" rx="6" fill="#f8fafc" stroke="#64748b" stroke-width="1.5" />
            <text x="290" y="22" fill="#334155" font-size="10.5" font-weight="700" text-anchor="middle">BOOT SEQUENCE &amp; FIRMWARE INITIALIZATION</text>
            <text x="290" y="42" fill="#64748b" font-size="9" text-anchor="middle">Power-On Reset Vector &rarr; UEFI POST &rarr; Bootloader Handoff &rarr; OS Kernel Entry</text>
          </g>

          <path d="M 470,205 L 470,230" fill="none" stroke="#64748b" stroke-width="2" marker-end="url(#arch-arrow)" />
        </svg>
      </div>
    </div>"""

    if target_header_end in content:
        content = content.replace(target_header_end, architecture_diagram_html)
        print("--> Successfully added system architecture diagram below header.")
    else:
        print("--> Warning: Header end tag not found.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add high-level architectural overview SVG diagram to Module 2 header\n\n"
            "Introduce an architectural overview diagram at the top of 02-hardware-review.html\n"
            "mapping out CPUs, memory hierarchy, buses, I/O controllers, and boot firmware."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for architecture diagram addition!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    add_system_architecture_diagram()
