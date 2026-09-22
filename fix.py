#!/usr/bin/env python3
# =====================================================================
# fix.py: Embed I/O Component Hierarchy diagram in 02-hardware-review.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)

HIERARCHY_SVG_BLOCK = r"""
      <div class="diagram-container" style="margin: 24px 0;">
        <svg viewBox="0 0 880 580" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 880px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;">
          <defs>
            <marker id="arrow-down" viewBox="0 0 10 10" refX="5" refY="8" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 1 1 L 5 8 L 9 1 z" fill="#0284c7" />
            </marker>
            <marker id="arrow-up" viewBox="0 0 10 10" refX="5" refY="2" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 1 9 L 5 2 L 9 9 z" fill="#059669" />
            </marker>
            <filter id="io-card-shadow" x="-3%" y="-3%" width="106%" height="106%">
              <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.06" />
            </filter>
          </defs>

          <!-- Canvas Background -->
          <rect width="880" height="580" fill="#f8fafc" rx="8" />

          <!-- Title Header -->
          <text x="440" y="32" fill="#0f172a" font-size="13" font-weight="700" text-anchor="middle">THE I/O HARDWARE &amp; SOFTWARE COMPONENT HIERARCHY</text>
          <text x="440" y="50" fill="#64748b" font-size="10" text-anchor="middle">From User-Space System Calls down to Silicon Controller Registers and Physical Media</text>

          <!-- TIER 1: USER SPACE -->
          <g transform="translate(40, 70)">
            <rect width="800" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#io-card-shadow)" />
            <rect width="180" height="20" rx="3" fill="#f1f5f9" x="12" y="8" />
            <text x="20" y="22" fill="#475569" font-size="9" font-weight="700">USER SPACE (RING 3)</text>

            <rect x="220" y="14" width="560" height="38" rx="4" fill="#f8fafc" stroke="#e2e8f0" />
            <text x="500" y="32" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">User Application / Standard C Library (POSIX I/O)</text>
            <text x="500" y="45" fill="#64748b" font-size="9" text-anchor="middle">Issues high-level calls: read(), write(), ioctl() via file descriptors</text>
          </g>

          <!-- Transition Arrow: System Call -->
          <path d="M 440, 135 L 440, 160" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-down)" />
          <text x="450" y="152" fill="#0284c7" font-size="8.5" font-weight="700">System Call Trap (syscall / sysenter)</text>

          <!-- TIER 2: KERNEL SUBSYSTEM & DRIVERS -->
          <g transform="translate(40, 165)">
            <rect width="800" height="120" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" filter="url(#io-card-shadow)" />
            <rect width="210" height="20" rx="3" fill="#e0f2fe" x="12" y="8" />
            <text x="20" y="22" fill="#0369a1" font-size="9" font-weight="700">KERNEL SPACE (RING 0 / SUPERVISOR)</text>

            <!-- Generic OS I/O Layer -->
            <g transform="translate(20, 36)">
              <rect width="365" height="70" rx="4" fill="#f0f9ff" stroke="#bae6fd" />
              <text x="182" y="24" fill="#0369a1" font-size="10.5" font-weight="700" text-anchor="middle">Generic I/O Subsystem (VFS &amp; Block Layer)</text>
              <text x="182" y="42" fill="#334155" font-size="8.5" text-anchor="middle">Uniform naming, file permissions, page cache,</text>
              <text x="182" y="56" fill="#334155" font-size="8.5" text-anchor="middle">I/O request queueing, and elevator scheduling</text>
            </g>

            <!-- Device Driver Layer -->
            <g transform="translate(415, 36)">
              <rect width="365" height="70" rx="4" fill="#f0fdf4" stroke="#86efac" />
              <text x="182" y="24" fill="#15803d" font-size="10.5" font-weight="700" text-anchor="middle">Device Driver (e.g., nvme.ko, e1000e.sys)</text>
              <text x="182" y="42" fill="#334155" font-size="8.5" text-anchor="middle">Translates OS requests into controller commands;</text>
              <text x="182" y="56" fill="#334155" font-size="8.5" text-anchor="middle">Services Interrupt Service Routines (ISRs)</text>
            </g>
          </g>

          <!-- Transition Arrows: Bus Interface -->
          <path d="M 360, 285 L 360, 318" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-down)" />
          <path d="M 520, 318 L 520, 285" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#arrow-up)" />
          <text x="350" y="306" fill="#0284c7" font-size="8.5" font-weight="700" text-anchor="end">Programmed I/O (MMIO / PMIO)</text>
          <text x="530" y="306" fill="#059669" font-size="8.5" font-weight="700" text-anchor="start">Hardware Interrupt Line (IRQ)</text>

          <!-- TIER 3: HARDWARE CONTROLLER -->
          <g transform="translate(40, 325)">
            <rect width="800" height="115" rx="6" fill="#ffffff" stroke="#d97706" stroke-width="1.5" filter="url(#io-card-shadow)" />
            <rect width="250" height="20" rx="3" fill="#fef3c7" x="12" y="8" />
            <text x="20" y="22" fill="#b45309" font-size="9" font-weight="700">DEVICE CONTROLLER / ADAPTER (SILICON IC)</text>

            <!-- Register Bank -->
            <g transform="translate(20, 36)">
              <rect width="450" height="66" rx="4" fill="#fffbeb" stroke="#fde68a" />
              <text x="225" y="20" fill="#92400e" font-size="10" font-weight="700" text-anchor="middle">Controller Internal Registers &amp; Data Buffers</text>
              <g transform="translate(15, 30)">
                <rect x="0" y="0" width="95" height="24" rx="3" fill="#ffffff" stroke="#cbd5e1" />
                <text x="47" y="16" fill="#475569" font-size="8" font-weight="600" text-anchor="middle">Command Reg</text>

                <rect x="105" y="0" width="95" height="24" rx="3" fill="#ffffff" stroke="#cbd5e1" />
                <text x="152" y="16" fill="#475569" font-size="8" font-weight="600" text-anchor="middle">Status Reg</text>

                <rect x="210" y="0" width="95" height="24" rx="3" fill="#ffffff" stroke="#cbd5e1" />
                <text x="257" y="16" fill="#475569" font-size="8" font-weight="600" text-anchor="middle">Data In/Out</text>

                <rect x="315" y="0" width="105" height="24" rx="3" fill="#ffffff" stroke="#cbd5e1" />
                <text x="367" y="16" fill="#475569" font-size="8" font-weight="600" text-anchor="middle">On-chip FIFO</text>
              </g>
            </g>

            <!-- DMA Engine Sub-block -->
            <g transform="translate(490, 36)">
              <rect width="290" height="66" rx="4" fill="#ecfdf5" stroke="#a7f3d0" />
              <text x="145" y="22" fill="#065f46" font-size="10" font-weight="700" text-anchor="middle">Direct Memory Access (DMA)</text>
              <text x="145" y="40" fill="#334155" font-size="8.5" text-anchor="middle">Bypasses CPU to stream data directly</text>
              <text x="145" y="54" fill="#047857" font-size="8.5" font-weight="600" text-anchor="middle">to/from Physical DRAM Bus</text>
            </g>
          </g>

          <!-- Transition Arrow: Low-Level Signals -->
          <path d="M 440, 440 L 440, 475" fill="none" stroke="#d97706" stroke-width="2" marker-end="url(#arrow-down)" />
          <text x="450" y="462" fill="#b45309" font-size="8.5" font-weight="700">Proprietary Physical Bus Signaling (PCIe PHY, NVMe, SATA, USB)</text>

          <!-- TIER 4: PHYSICAL DEVICE -->
          <g transform="translate(40, 480)">
            <rect width="800" height="75" rx="6" fill="#ffffff" stroke="#64748b" stroke-width="1.5" filter="url(#io-card-shadow)" />
            <rect width="230" height="20" rx="3" fill="#f1f5f9" x="12" y="8" />
            <text x="20" y="22" fill="#334155" font-size="9" font-weight="700">PHYSICAL HARDWARE DEVICE (ELECTROMECHANICAL / PHY)</text>

            <g transform="translate(20, 34)">
              <rect x="0" y="0" width="180" height="30" rx="4" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="90" y="19" fill="#0f172a" font-size="9" font-weight="600" text-anchor="middle">NVMe NAND Flash Cells</text>

              <rect x="195" y="0" width="180" height="30" rx="4" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="285" y="19" fill="#0f172a" font-size="9" font-weight="600" text-anchor="middle">Magnetic HDD Platters</text>

              <rect x="390" y="0" width="180" height="30" rx="4" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="480" y="19" fill="#0f172a" font-size="9" font-weight="600" text-anchor="middle">Ethernet PHY &amp; RJ45 Port</text>

              <rect x="585" y="0" width="175" height="30" rx="4" fill="#f8fafc" stroke="#e2e8f0" />
              <text x="672" y="19" fill="#0f172a" font-size="9" font-weight="600" text-anchor="middle">Display OLED/LCD Matrix</text>
            </g>
          </g>
        </svg>
      </div>
"""

def insert_hierarchy_diagram():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate Section 4's Component Hierarchy list in 02-hardware-review.html
    # We want to place the diagram right after:
    # <li><strong>Device Drivers:</strong> Software modules running in kernel mode ... operations.</li>
    # </ul>
    search_target = "operations.</li>\n      </ul>"
    if search_target not in content:
        # Try alternate whitespace if needed
        search_target = "operations.</li>\r\n      </ul>"

    if search_target not in content:
        # Fallback to general list end after "The Component Hierarchy"
        split_marker = "<h3>The Component Hierarchy</h3>"
        if split_marker in content:
            parts = content.split(split_marker, 1)
            ul_end = parts[1].find("</ul>")
            if ul_end != -1:
                insertion_point = len(parts[0]) + len(split_marker) + ul_end + 5
                content = content[:insertion_point] + "\n" + HIERARCHY_SVG_BLOCK + content[insertion_point:]
                print("--> Inserted diagram via relative anchor point.")
            else:
                print("Error: Could not find </ul> after The Component Hierarchy.")
                return
        else:
            print("Error: Could not find 'The Component Hierarchy' heading.")
            return
    else:
        content = content.replace(search_target, f"{search_target}\n{HIERARCHY_SVG_BLOCK}")
        print("--> Inserted diagram immediately following the Component Hierarchy list.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully updated {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Embed I/O component hierarchy diagram in Module 2\n\n"
            "Add the multi-tier hardware and software component hierarchy SVG diagram\n"
            "into Section 4 of 02-hardware-review.html to visually map user space calls,\n"
            "kernel drivers, MMIO/DMA controllers, and physical storage media."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for Component Hierarchy diagram!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    insert_hierarchy_diagram()
