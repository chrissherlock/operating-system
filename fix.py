#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand Section 4 (Disks, I/O Devices, & Controller Hardware)
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def expand_section_four():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Old concise Section 4 heading and text
    old_section_4 = """      <h2>4. Disks, I/O Devices, &amp; Controller Hardware</h2>
      <p>I/O devices consist of physical components and electronic device controllers that accept commands from the OS.</p>"""

    # Expanded Section 4 markup
    new_section_4 = """      <h2>4. Disks, I/O Devices, &amp; Controller Hardware</h2>
      <p>
        Input/output (I/O) hardware bridges the CPU and memory with the outside digital and physical world. Because physical devices (keyboards, network interfaces, NVMe drives, and displays) operate at speeds orders of magnitude slower than CPU registers and DRAM buses, computer architectures utilize a specialized hierarchy of hardware controllers and communication pathways.
      </p>

      <h3>The Component Hierarchy</h3>
      <ul>
        <li><strong>Physical Devices:</strong> The electromechanical or solid-state endpoints (e.g., spinning magnetic platters, NAND flash cells, LED backlights, or sensor arrays) that interact directly with the physical environment.</li>
        <li><strong>Device Controllers (Adapters):</strong> Integrated circuits or expansion cards (such as a PCIe NVMe controller or USB host controller) attached to the motherboard. The controller provides an electronic hardware interface that translates low-level physical signals into structured digital registers and buffers.</li>
        <li><strong>Device Drivers:</strong> Software modules running in kernel mode (Ring 0) that understand the specific register layouts, command sets, and quirks of a given controller, translating generic OS read/write requests into device-specific operations.</li>
      </ul>

      <h3>How I/O Communication Works</h3>
      <p>The CPU communicates with device controllers using two primary hardware mechanisms:</p>
      <ol>
        <li><strong>Port-Mapped I/O (PMIO):</strong> The CPU uses dedicated, isolated hardware instructions (such as <code>in</code> and <code>out</code> on x86) interacting with a separate address space specifically reserved for I/O ports.</li>
        <li><strong>Memory-Mapped I/O (MMIO):</strong> The controller's control and data registers are mapped directly into the system's physical address space. When the CPU writes to a specific MMIO physical address, the memory bus routes the write directly to the hardware controller's internal registers instead of DRAM.</li>
      </ol>

      <h3>Direct Memory Access (DMA)</h3>
      <p>
        To prevent the CPU from wasting valuable cycles moving large blocks of data byte-by-byte between an I/O device and DRAM, systems employ a <strong>Direct Memory Access (DMA)</strong> controller:
      </p>
      <ul>
        <li><strong>Offloading Data Transfers:</strong> The CPU programs the DMA controller with source and destination addresses, byte counts, and direction flags, then issues a transfer command.</li>
        <li><strong>Bus Mastership:</strong> The DMA controller takes control of the memory bus (bus mastership), reading data directly from the device controller and writing it straight into physical RAM at hardware speeds.</li>
        <li><strong>Completion Interrupt:</strong> Once the entire block transfer finishes, the DMA controller asserts a hardware interrupt line to notify the CPU, eliminating software polling overhead entirely.</li>
      </ul>"""

    if old_section_4 in content:
        content = content.replace(old_section_4, new_section_4)
        print("--> Successfully expanded Section 4 in 02-hardware-review.html")
    else:
        print("--> Warning: Exact Section 4 markup not matched. Trying alternative replacement...")
        # Fallback replacement if exact string varies slightly
        simple_old = "<h2>4. Disks, I/O Devices, &amp; Controller Hardware</h2>"
        if simple_old in content:
            # Replace just the heading and following paragraph up to heading 5
            parts = content.split("<h2>4. Disks, I/O Devices, &amp; Controller Hardware</h2>")
            if len(parts) == 2:
                sub_parts = parts[1].split("<h2>5. Buses &amp; The Boot Process</h2>")
                if len(sub_parts) == 2:
                    content = parts[0] + new_section_4 + "\n\n      <h2>5. Buses &amp; The Boot Process</h2>" + sub_parts[1]
                    print("--> Successfully replaced Section 4 via boundary split.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add detailed section on Disks, I/O Devices, and Controllers to Module 2\n\n"
            "Update 02-hardware-review.html to expand Section 4 with comprehensive\n"
            "explanations of physical endpoints, controllers, MMIO vs PMIO, and DMA."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for Section 4 expansion!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    expand_section_four()
