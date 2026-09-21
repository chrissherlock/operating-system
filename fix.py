#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand Section 5 (Buses & The Boot Process)
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def expand_section_five():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Old concise Section 5 heading and text
    old_section_5 = """      <h2>5. Buses &amp; The Boot Process</h2>
      <p>Modern computers utilize a hierarchy of specialized buses connecting processors, memory, and controllers.</p>"""

    # Expanded Section 5 markup
    new_section_5 = """      <h2>5. Buses &amp; The Boot Process</h2>
      <p>
        Modern computers rely on a high-speed hierarchy of communication pathways known as <strong>buses</strong> to transport data, addresses, and control signals between the CPU, memory, and peripheral controllers. Following power-on, a carefully choreographed <strong>boot sequence</strong> transitions the bare silicon into a fully operational operating system.
      </p>

      <h3>System Bus Architecture &amp; The PCIe Hierarchy</h3>
      <p>
        System bus topology has evolved from shared parallel buses (like the old PCI bus) to high-speed point-to-point serial packet interconnects:
      </p>
      <ul>
        <li><strong>The Memory Bus:</strong> A high-bandwidth, low-latency channel directly connecting the CPU memory controller to physical DRAM DIMMs, operating at multi-gigahertz clock rates.</li>
        <li><strong>PCI Express (PCIe):</strong> The ubiquitous high-speed serial expansion bus used for graphics cards, NVMe storage controllers, and high-performance network interfaces. PCIe organizes lanes into bidirectional differential pairs (x1, x4, x8, x16) supporting packetized transactions and Direct Memory Access.</li>
        <li><strong>Low-Pin-Count (LPC) / SPI Bus:</strong> Lower-bandwidth serial buses dedicated to legacy peripherals, Trusted Platform Modules (TPM), and the system's flash storage chip containing UEFI firmware.</li>
      </ul>

      <h3>The Boot Process: From Power-On to Operating System Handoff</h3>
      <p>
        When a computer is powered on, the CPU has no operating system loaded, RAM is uninitialized, and registers contain undefined values. The system initializes through distinct sequential stages:
      </p>
      <ol>
        <li>
          <strong>Power-On Reset &amp; The Reset Vector:</strong>
          The motherboard chipset asserts a reset signal. Upon deassertion, the CPU forces its Program Counter (PC) to a hardwired architectural address known as the <strong>Reset Vector</strong> (e.g., <code>0xFFFFFFF0</code> in legacy x86 or mapped ROM addresses in modern UEFI). At this exact location sits the CPU's first instruction: a jump to the motherboard flash ROM.
        </li>
        <li>
          <strong>Firmware Initialization (UEFI / BIOS):</strong>
          The CPU executes the Extensible Firmware Interface (UEFI) stored in non-volatile flash memory. The firmware performs the <strong>Power-On Self-Test (POST)</strong>, initializes memory controllers, trains DRAM timing parameters, and discovers attached hardware devices.
        </li>
        <li>
          <strong>Device Discovery &amp; Boot Selection:</strong>
          The UEFI firmware scans storage volumes for a valid EFI System Partition (ESP) containing signed bootloader binaries (e.g., <code>EFI/BOOT/BOOTX64.EFI</code>) according to stored NVRAM boot variables.
        </li>
        <li>
          <strong>The Bootloader Handoff:</strong>
          The primary bootloader (such as GRUB or the Windows Boot Manager) loads the operating system kernel image and initial RAM disk (initrd/initramfs) into physical RAM.
        </li>
        <li>
          <strong>Entering Protected / Long Mode &amp; Kernel Entry:</strong>
          The bootloader transitions the CPU from 16-bit real mode into 64-bit Long Mode, enables paging and the MMU by loading the root register (CR3), and jumps directly into the kernel's entry point (`kernel_main`). The OS initializes driver subsystems, spawns the first user-space process (<code>init</code> or <code>systemd</code>), and presents the user login environment.
        </li>
      </ol>"""

    if old_section_5 in content:
        content = content.replace(old_section_5, new_section_5)
        print("--> Successfully expanded Section 5 in 02-hardware-review.html")
    else:
        print("--> Warning: Exact Section 5 markup not matched. Trying boundary replacement...")
        # Fallback replacement using boundary split
        simple_old = "<h2>5. Buses &amp; The Boot Process</h2>"
        if simple_old in content:
            parts = content.split("<h2>5. Buses &amp; The Boot Process</h2>")
            if len(parts) == 2:
                # Find where article body ends
                sub_parts = parts[1].split("</article>")
                if len(sub_parts) >= 2:
                    content = parts[0] + new_section_5 + "\n    </article>" + "".join(sub_parts[1:])
                    print("--> Successfully replaced Section 5 via boundary split.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add comprehensive coverage of system buses and the boot sequence to Module 2\n\n"
            "Update 02-hardware-review.html to expand Section 5 with detailed explanations\n"
            "of bus topologies, PCIe hierarchies, the CPU reset vector, UEFI firmware,\n"
            "and the OS bootloader handoff."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for Section 5 expansion!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    expand_section_five()
