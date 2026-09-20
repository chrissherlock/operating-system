#!/usr/bin/env python3
# =====================================================================
# fix.py: Inject interactive boot sequence walkthrough into Module 2
# =====================================================================
import os
import re
import subprocess

BOOT_WALKTHROUGH_HTML = """
      <div id="interactive-boot-simulator" style="margin: 32px 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <!-- Simulator Header -->
        <div style="border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 18px;">
          <h3 style="margin: 0; color: #0284c7; font-size: 1.15rem;">Guided Walkthrough: The System Boot Sequence</h3>
          <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Trace the hardware and firmware execution hand-offs from power-on reset to user space initialization.</p>
        </div>

        <!-- Instructions Guide -->
        <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px; margin-bottom: 16px;">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">How to Use This Simulator</div>
          <ol style="margin-left: 20px; margin-bottom: 0; color: #334155; font-size: 0.88rem; line-height: 1.5;">
            <li><strong>Step Through the Hand-offs:</strong> Use the controls below to advance through each stage of the bootstrap process.</li>
            <li><strong>Monitor the Execution Domain Bar:</strong> Track how the <strong>Active Program Counter</strong>, <strong>Privilege Environment</strong>, and <strong>Active Memory Target</strong> shift across hardware components.</li>
            <li><strong>Observe Bus Transitions:</strong> The animated vector diagram below highlights the exact data buses, firmware chips, disks, and memory buffers active during each phase.</li>
          </ol>
        </div>

        <!-- Action Controls & Inline Next Step Explanation -->
        <div style="display: grid; grid-template-columns: auto 1fr; gap: 16px; align-items: stretch; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px; margin-bottom: 20px;">
          <!-- Controls -->
          <div style="display: flex; flex-direction: column; gap: 8px; justify-content: center; min-width: 170px;">
            <button id="boot-next-btn" style="padding: 10px 16px; font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; border-radius: 6px; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; cursor: pointer; text-align: center; transition: all 0.15s ease;">Next Step &rarr;</button>
            <div style="display: flex; gap: 8px;">
              <button id="boot-prev-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 600; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">&larr; Prev</button>
              <button id="boot-reset-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #64748b; cursor: pointer;">Reset</button>
            </div>
          </div>

          <!-- Inline Next Step Explanation Pane -->
          <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-left: 4px solid #0284c7; border-radius: 0 6px 6px 0; padding: 10px 14px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: #0369a1; text-transform: uppercase; letter-spacing: 0.03em;">Upcoming Action When You Click Next:</div>
            <div id="boot-inline-next-desc" style="font-size: 0.88rem; color: #0c4a6e; line-height: 1.45; margin-top: 4px;">
              The firmware will run the Power-On Self-Test (POST), inventory system RAM, and scan buses for attached NVMe and SATA storage controllers.
            </div>
          </div>
        </div>

        <!-- System State Bar -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin-bottom: 20px; font-family: var(--font-mono); font-size: 0.8rem;">
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Boot Phase</div>
            <div id="boot-status-phase" style="font-weight: 700; color: #0284c7; margin-top: 2px;">Stage 1 of 5</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Execution Target</div>
            <div id="boot-status-target" style="font-weight: 700; color: #0f172a; margin-top: 2px;">Motherboard ROM / Flash</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Program Counter (PC)</div>
            <div id="boot-status-pc" style="font-weight: 700; color: #0369a1; margin-top: 2px;">0xFFFFFFF0 (Reset Vector)</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Execution Mode</div>
            <div id="boot-status-mode" style="font-weight: 700; color: #166534; margin-top: 2px;">Real / Flat Protected</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Primary Storage Media</div>
            <div id="boot-status-media" style="font-weight: 700; color: #475569; margin-top: 2px;">SPI Flash NVRAM</div>
          </div>
        </div>

        <!-- Boot Sequence Interactive SVG -->
        <div style="display: flex; justify-content: center; margin-bottom: 20px; overflow-x: auto;">
          <svg id="boot-anim-svg" viewBox="0 0 860 300" width="100%" height="auto" style="max-width: 860px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <marker id="bootBlueArrow" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto">
                <path d="M0,0 L6,3 L0,6 Z" fill="#0284c7" />
              </marker>
            </defs>

            <!-- Main System Interconnect Bus -->
            <rect x="30" y="130" width="800" height="22" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.5" />
            <text x="430" y="145" fill="#475569" font-size="10" font-weight="700" text-anchor="middle">SYSTEM &amp; EXPANSION BUS (SPI / PCIe / Memory Channels)</text>

            <!-- Node 1: Power & Reset -->
            <g id="boot-node-power" transform="translate(30, 30)">
              <rect x="0" y="0" width="140" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="70" y="26" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">1. Power-On Reset</text>
              <text x="70" y="44" fill="#64748b" font-size="9.5" text-anchor="middle">PSU Stable Signal</text>
              <text x="70" y="56" fill="#0284c7" font-size="9" text-anchor="middle">PC &larr; Reset Vector</text>
            </g>

            <!-- Node 2: Firmware (BIOS/UEFI) -->
            <g id="boot-node-firmware" transform="translate(195, 30)">
              <rect x="0" y="0" width="145" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="72" y="26" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">2. BIOS / UEFI ROM</text>
              <text x="72" y="44" fill="#64748b" font-size="9.5" text-anchor="middle">Hardware POST</text>
              <text x="72" y="56" fill="#0284c7" font-size="9" text-anchor="middle">Probes RAM &amp; Buses</text>
            </g>

            <!-- Node 3: Bootloader Storage -->
            <g id="boot-node-storage" transform="translate(365, 30)">
              <rect x="0" y="0" width="145" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="72" y="26" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">3. Boot Device</text>
              <text x="72" y="44" fill="#64748b" font-size="9.5" text-anchor="middle">MBR / EFI Partition</text>
              <text x="72" y="56" fill="#0284c7" font-size="9" text-anchor="middle">Loads GRUB Stage 1/2</text>
            </g>

            <!-- Node 4: System RAM & Kernel Relocation -->
            <g id="boot-node-ram" transform="translate(535, 30)">
              <rect x="0" y="0" width="145" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="72" y="26" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">4. RAM &amp; Kernel</text>
              <text x="72" y="44" fill="#64748b" font-size="9.5" text-anchor="middle">vmlinuz &amp; initramfs</text>
              <text x="72" y="56" fill="#0284c7" font-size="9" text-anchor="middle">Unpacks into Memory</text>
            </g>

            <!-- Node 5: Kernel Execution & Userspace Init -->
            <g id="boot-node-kernel" transform="translate(705, 30)">
              <rect x="0" y="0" width="125" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="62" y="26" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">5. Kernel Init</text>
              <text x="62" y="44" fill="#64748b" font-size="9.5" text-anchor="middle">Drivers &amp; MMU Tables</text>
              <text x="62" y="56" fill="#0284c7" font-size="9" text-anchor="middle">Spawns /sbin/init</text>
            </g>

            <!-- Bus Interconnect Vertical Lines -->
            <line id="boot-line-1" x1="100" y1="95" x2="100" y2="130" stroke="#cbd5e1" stroke-width="2" />
            <line id="boot-line-2" x1="267" y1="95" x2="267" y2="130" stroke="#cbd5e1" stroke-width="2" />
            <line id="boot-line-3" x1="437" y1="95" x2="437" y2="130" stroke="#cbd5e1" stroke-width="2" />
            <line id="boot-line-4" x1="607" y1="95" x2="607" y2="130" stroke="#cbd5e1" stroke-width="2" />
            <line id="boot-line-5" x1="767" y1="95" x2="767" y2="130" stroke="#cbd5e1" stroke-width="2" />

            <!-- Dynamic Data Flow Representation Box in Lower Half -->
            <g transform="translate(30, 180)">
              <rect x="0" y="0" width="800" height="95" rx="6" fill="#f8fafc" stroke="#cbd5e1" />
              <text x="20" y="26" fill="#0369a1" font-size="11" font-weight="700">ACTIVE BUS TRANSFER &amp; MEMORY MAPPING</text>
              <text id="boot-flow-label" x="20" y="52" fill="#0f172a" font-size="11" font-family="var(--font-mono)">
                Power circuitry asserts RESET line &rarr; CPU hardware forces PC to 0xFFFFFFF0.
              </text>
              <text id="boot-flow-sublabel" x="20" y="74" fill="#64748b" font-size="10" font-family="var(--font-mono)">
                No RAM initialized yet. CPU executes directly from mapped Flash ROM.
              </text>
            </g>
          </svg>
        </div>

        <!-- Two-Pane Pedagogical Explanation Dashboard -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <!-- Current Action Pane -->
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0284c7; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #0284c7; text-transform: uppercase; letter-spacing: 0.03em;">Current State: What Is Happening</div>
            <div id="boot-desc-what" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;">
              When power is switched on, electrical voltages stabilize and the power supply asserts the <code>POWER_GOOD</code> signal. The CPU resets registers and automatically points its Program Counter to the hardwired reset vector address <code>0xFFFFFFF0</code>.
            </div>
          </div>

          <!-- Rationale Pane -->
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #10b981; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 0.03em;">Why The System Does This</div>
            <div id="boot-desc-why" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;">
              Main memory (DRAM) is volatile and completely empty at power-on. The CPU requires an unchangeable, hardwired physical address mapped directly to non-volatile flash ROM so execution can begin immediately without operating system assistance.
            </div>
          </div>
        </div>
      </div>

      <script>
        (function() {
          const bootSteps = [
            {
              phase: "Stage 1 of 5",
              target: "Motherboard ROM / Flash",
              pc: "0xFFFFFFF0 (Reset Vector)",
              mode: "Real Mode / Flat Protected",
              media: "SPI Flash NVRAM",
              activeNode: "boot-node-power",
              activeLine: "boot-line-1",
              btnNextText: "Next Step &rarr;",
              btnPrevText: "&larr; Prev",
              inlineNext: "The firmware will execute the Power-On Self-Test (POST), inventory system RAM, and scan buses for attached NVMe and SATA storage controllers.",
              flowTitle: "CPU RESET ASSERTION &rarr; Direct Flash ROM Execution",
              flowSub: "No DRAM available yet. CPU executes initial jump instruction directly from mapped SPI ROM.",
              what: "When power is switched on, electrical voltages stabilize and the power supply asserts the <code>POWER_GOOD</code> signal. The CPU resets registers and automatically points its Program Counter to the hardwired reset vector address <code>0xFFFFFFF0</code>.",
              why: "Main memory (DRAM) is volatile and completely empty at power-on. The CPU requires an unchangeable, hardwired physical address mapped directly to non-volatile flash ROM so execution can begin immediately without operating system assistance."
            },
            {
              phase: "Stage 2 of 5",
              target: "UEFI / BIOS Firmware",
              pc: "0x000F0000 (Firmware Exec)",
              mode: "Firmware Runtime",
              media: "Motherboard ROM / NVRAM",
              activeNode: "boot-node-firmware",
              activeLine: "boot-line-2",
              btnNextText: "Next Step &rarr;",
              btnPrevText: "&larr; Prev",
              inlineNext: "The firmware will read the boot sector (MBR) or execute the EFI bootloader binary (GRUB) from the designated storage drive.",
              flowTitle: "POST EXECUTION &rarr; Memory Controller Initialization &amp; Bus Inventory",
              flowSub: "Firmware checks RAM chips, detects GPU and disks across PCIe/DMI, and selects boot drive.",
              what: "The BIOS/UEFI firmware executes the Power-On Self-Test (POST). It tests and initializes the memory controllers, configures attached buses (PCIe, USB, DMI), and inventories boot media listed in the NVRAM boot priority table.",
              why: "The operating system cannot boot until basic physical hardware—specifically system RAM and storage interfaces—are verified, clocked, and operating with reliable signaling."
            },
            {
              phase: "Stage 3 of 5",
              target: "Boot Media (NVMe / SSD)",
              pc: "0x00007C00 (MBR / GRUB)",
              mode: "Protected Mode (32-bit)",
              media: "ESP Partition / MBR Sector",
              activeNode: "boot-node-storage",
              activeLine: "boot-line-3",
              btnNextText: "Next Step &rarr;",
              btnPrevText: "&larr; Prev",
              inlineNext: "The bootloader will read the Linux kernel image (vmlinuz) and initial ramdisk (initramfs) into memory and configure initial CPU registers.",
              flowTitle: "BOOTLOADER STAGING &rarr; Reading Partition Sectors into System RAM",
              flowSub: "Firmware hands off execution to GRUB, which presents the boot menu and locates the kernel image.",
              what: "Firmware loads the first 512 bytes (MBR) or reads the EFI executable file from the EFI System Partition (ESP) into RAM and branches to it. The bootloader (e.g., GRUB) runs, locates the configured kernel binary, and loads its secondary stages.",
              why: "Motherboard firmware lacks the specialized filesystem drivers to understand complex filesystems like ext4, Btrfs, or ZFS. A dedicated bootloader bridges this gap."
            },
            {
              phase: "Stage 4 of 5",
              target: "System RAM (Low &amp; High)",
              pc: "0x01000000 (Kernel Entry)",
              mode: "Long Mode (64-bit Kernel)",
              media: "DDR4 / DDR5 System RAM",
              activeNode: "boot-node-ram",
              activeEdges: [],
              activeLine: "boot-line-4",
              btnNextText: "Next Step &rarr;",
              btnPrevText: "&larr; Prev",
              inlineNext: "The kernel will activate virtual memory paging, configure the Interrupt Descriptor Table (IDT), and launch the initial user-space process (/sbin/init).",
              flowTitle: "KERNEL EXTRACTION &rarr; Copying vmlinuz &amp; initramfs into Memory",
              flowSub: "Bootloader configures initial page tables, switches CPU to 64-bit Long Mode, and jumps to startup_64.",
              what: "The bootloader loads the compressed kernel image (<code>vmlinuz</code>) and temporary RAM filesystem (<code>initramfs</code>) into RAM, configures hardware registers, and jumps directly to the kernel entry point (e.g., <code>startup_64</code> on x86-64).",
              why: "Firmware services are permanently discarded after this point. The operating system kernel must take full, autonomous control of all hardware devices and memory spaces."
            },
            {
              phase: "Stage 5 of 5",
              target: "Operating System Kernel",
              pc: "0xFFFFFFFF81000000 (Kernel)",
              mode: "Kernel (Ring 0) &rarr; User (Ring 3)",
              media: "Virtual Memory &amp; Root FS",
              activeNode: "boot-node-kernel",
              activeLine: "boot-line-5",
              btnNextText: "Restart Walkthrough &#8634;",
              btnPrevText: "&larr; Prev",
              inlineNext: "Boot sequence complete. Clicking restart will reset the walkthrough back to Stage 1.",
              flowTitle: "KERNEL INITIALIZATION &rarr; Spawning /sbin/init or systemd (PID 1)",
              flowSub: "Virtual memory paging enabled, drivers mounted, root FS mounted, CPU drops to Ring 3.",
              what: "The kernel configures the MMU page tables, registers interrupt vectors in the IDT, initializes device drivers, mounts the root filesystem, and executes <code>/sbin/init</code> (or <code>systemd</code> as PID 1), dropping into user space.",
              why: "The system transitions to its normal operating state, where applications run isolated in user mode and all hardware requests are brokered by the kernel via system calls."
            }
          ];

          let bootIndex = 0;

          function renderBootState() {
            const data = bootSteps[bootIndex];
            document.getElementById("boot-status-phase").textContent = data.phase;
            document.getElementById("boot-status-target").textContent = data.target;
            document.getElementById("boot-status-pc").textContent = data.pc;
            document.getElementById("boot-status-mode").textContent = data.mode;
            document.getElementById("boot-status-media").textContent = data.media;

            document.getElementById("boot-inline-next-desc").innerHTML = data.inlineNext;
            document.getElementById("boot-desc-what").innerHTML = data.what;
            document.getElementById("boot-desc-why").innerHTML = data.why;

            document.getElementById("boot-flow-label").textContent = data.flowTitle;
            document.getElementById("boot-flow-sublabel").textContent = data.flowSub;

            const nextBtn = document.getElementById("boot-next-btn");
            const prevBtn = document.getElementById("boot-prev-btn");

            if (nextBtn) nextBtn.innerHTML = data.btnNextText;
            if (prevBtn) {
              prevBtn.innerHTML = data.btnPrevText;
              prevBtn.style.opacity = bootIndex === 0 ? "0.5" : "1.0";
              prevBtn.style.cursor = bootIndex === 0 ? "not-allowed" : "pointer";
            }

            const allNodes = ["boot-node-power", "boot-node-firmware", "boot-node-storage", "boot-node-ram", "boot-node-kernel"];
            allNodes.forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                const rect = el.querySelector("rect");
                if (rect) {
                  rect.setAttribute("stroke", "#cbd5e1");
                  rect.setAttribute("stroke-width", "1.5");
                  rect.setAttribute("fill", "#ffffff");
                }
              }
            });

            const allLines = ["boot-line-1", "boot-line-2", "boot-line-3", "boot-line-4", "boot-line-5"];
            allLines.forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                el.setAttribute("stroke", "#cbd5e1");
                el.setAttribute("stroke-width", "2");
              }
            });

            const activeNodeEl = document.getElementById(data.activeNode);
            if (activeNodeEl) {
              const rect = activeNodeEl.querySelector("rect");
              if (rect) {
                rect.setAttribute("stroke", "#0284c7");
                rect.setAttribute("stroke-width", "2.5");
                rect.setAttribute("fill", "#f0f9ff");
              }
            }

            const activeLineEl = document.getElementById(data.activeLine);
            if (activeLineEl) {
              activeLineEl.setAttribute("stroke", "#0284c7");
              activeLineEl.setAttribute("stroke-width", "3");
            }
          }

          document.getElementById("boot-next-btn").addEventListener("click", function() {
            if (bootIndex < bootSteps.length - 1) {
              bootIndex++;
            } else {
              bootIndex = 0;
            }
            renderBootState();
          });

          document.getElementById("boot-prev-btn").addEventListener("click", function() {
            if (bootIndex > 0) {
              bootIndex--;
              renderBootState();
            }
          });

          document.getElementById("boot-reset-btn").addEventListener("click", function() {
            bootIndex = 0;
            renderBootState();
          });

          renderBootState();
        })();
      </script>
"""

def inject_boot_simulator():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'id="interactive-boot-simulator"' not in content:
        # Locate the Section 5 boot sequence list
        target_marker = "<li>The bootloader transfers execution to the kernel entry point. The OS kernel initializes hardware drivers, activates protected virtual memory, and spawns the initial user-space environment (such as <code>init</code> or <code>systemd</code>).</li>\n      </ol>"
        if target_marker in content:
            content = content.replace(target_marker, f"{target_marker}\n{BOOT_WALKTHROUGH_HTML}")
            print("--> Injected interactive boot simulator after boot sequence list.")
        else:
            pattern = r"(<li>The bootloader transfers execution to the kernel entry point.*?</li>\s*</ol>)"
            content = re.sub(pattern, f"\\1\n{BOOT_WALKTHROUGH_HTML}", content, count=1, flags=re.DOTALL)
            print("--> Injected interactive boot simulator via fallback pattern.")
    else:
        print("--> Interactive boot simulator already exists.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Add interactive boot sequence walkthrough simulator to Module 2\n\n"
            "Inject five-stage guided bootloader and kernel initialization simulator\n"
            "into week01-operating-system-concepts/02-hardware-review.html via fix.py."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    inject_boot_simulator()
