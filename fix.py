#!/usr/bin/env python3
# =====================================================================
# fix.py: Add multi-OS toggle to boot sequence simulator in Module 2
# =====================================================================
import os
import re
import subprocess

MULTI_OS_BOOT_HTML = """
      <div id="interactive-boot-simulator" style="margin: 32px 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <!-- Simulator Header -->
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 18px;">
          <div>
            <h3 style="margin: 0; color: #0284c7; font-size: 1.15rem;">Guided Walkthrough: System Boot Sequence</h3>
            <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Compare how Linux, Windows, and macOS execute the five universal bootstrap stages (Tanenbaum 1.3.6).</p>
          </div>

          <!-- OS Selector Toggle Group -->
          <div style="display: flex; align-items: center; gap: 6px; background: #f1f5f9; padding: 4px; border-radius: 8px; border: 1px solid #cbd5e1;">
            <span style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #475569; padding: 0 6px;">OS:</span>
            <button id="btn-os-linux" class="boot-os-btn active" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: #0284c7; color: #ffffff; cursor: pointer; transition: all 0.15s ease;">Linux</button>
            <button id="btn-os-windows" class="boot-os-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: transparent; color: #475569; cursor: pointer; transition: all 0.15s ease;">Windows</button>
            <button id="btn-os-macos" class="boot-os-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: transparent; color: #475569; cursor: pointer; transition: all 0.15s ease;">macOS</button>
          </div>
        </div>

        <!-- Instructions Guide -->
        <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px; margin-bottom: 16px;">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">How to Use This Simulator</div>
          <ol style="margin-left: 20px; margin-bottom: 0; color: #334155; font-size: 0.88rem; line-height: 1.5;">
            <li><strong>Toggle Operating Systems:</strong> Use the <code>Linux</code>, <code>Windows</code>, and <code>macOS</code> buttons above at any time to compare how each OS handles that specific boot stage.</li>
            <li><strong>Step Through the Hand-offs:</strong> Click <code>Next Step &rarr;</code> to step through each execution phase in sequence.</li>
            <li><strong>Inspect Hardware Transitions:</strong> Observe the <strong>Executing Entity</strong>, <strong>Active Program Counter</strong>, and the highlighted bus path in the architecture diagram.</li>
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
              The firmware will run the Power-On Self-Test (POST), initialize DRAM memory controllers, and probe buses for boot storage devices.
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
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Executing Entity</div>
            <div id="boot-status-target" style="font-weight: 700; color: #0f172a; margin-top: 2px;">CPU Hardware / Reset Vector</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Program Counter (PC)</div>
            <div id="boot-status-pc" style="font-weight: 700; color: #0369a1; margin-top: 2px;">0xFFFFFFF0 (Reset Vector)</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">CPU Mode</div>
            <div id="boot-status-mode" style="font-weight: 700; color: #166534; margin-top: 2px;">Raw Machine / Firmware Mode</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Active Code Binary</div>
            <div id="boot-status-media" style="font-weight: 700; color: #475569; margin-top: 2px;">Motherboard Flash ROM</div>
          </div>
        </div>

        <!-- Boot Sequence Interactive SVG -->
        <div style="display: flex; justify-content: center; margin-bottom: 20px; overflow-x: auto;">
          <svg id="boot-anim-svg" viewBox="0 0 860 300" width="100%" height="auto" style="max-width: 860px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
            <!-- Main System Interconnect Bus -->
            <rect x="30" y="130" width="800" height="22" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.5" />
            <text x="430" y="145" fill="#475569" font-size="10" font-weight="700" text-anchor="middle">SYSTEM INTERCONNECT BUS (Memory Channels &amp; Peripheral Buses)</text>

            <!-- Node 1: Power & Hardware Reset -->
            <g id="boot-node-power" transform="translate(30, 30)">
              <rect x="0" y="0" width="140" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text x="70" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">1. Power &amp; Reset</text>
              <text id="node-1-sub" x="70" y="42" fill="#64748b" font-size="9.5" text-anchor="middle">Voltages Stabilize</text>
              <text id="node-1-detail" x="70" y="56" fill="#0284c7" font-size="9" text-anchor="middle">PC &larr; Reset Vector</text>
            </g>

            <!-- Node 2: Firmware (BIOS/UEFI) -->
            <g id="boot-node-firmware" transform="translate(195, 30)">
              <rect x="0" y="0" width="145" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text id="node-2-title" x="72" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">2. Firmware (POST)</text>
              <text id="node-2-sub" x="72" y="42" fill="#64748b" font-size="9.5" text-anchor="middle">Checks RAM &amp; Disks</text>
              <text id="node-2-detail" x="72" y="56" fill="#0284c7" font-size="9" text-anchor="middle">Reads Boot Priority</text>
            </g>

            <!-- Node 3: Bootloader Storage -->
            <g id="boot-node-storage" transform="translate(365, 30)">
              <rect x="0" y="0" width="145" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text id="node-3-title" x="72" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">3. Boot Manager</text>
              <text id="node-3-sub" x="72" y="42" fill="#64748b" font-size="9.5" text-anchor="middle">ESP Partition</text>
              <text id="node-3-detail" x="72" y="56" fill="#0284c7" font-size="9" text-anchor="middle">Loads Bootloader</text>
            </g>

            <!-- Node 4: Kernel Relocation in RAM -->
            <g id="boot-node-ram" transform="translate(535, 30)">
              <rect x="0" y="0" width="145" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text id="node-4-title" x="72" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">4. Kernel Load</text>
              <text id="node-4-sub" x="72" y="42" fill="#64748b" font-size="9.5" text-anchor="middle">RAM Memory Setup</text>
              <text id="node-4-detail" x="72" y="56" fill="#0284c7" font-size="9" text-anchor="middle">MMU Paging Activated</text>
            </g>

            <!-- Node 5: Userspace Hand-off -->
            <g id="boot-node-kernel" transform="translate(705, 30)">
              <rect x="0" y="0" width="125" height="65" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
              <text id="node-5-title" x="62" y="24" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">5. Userspace Init</text>
              <text id="node-5-sub" x="62" y="42" fill="#64748b" font-size="9.5" text-anchor="middle">Initial System PID</text>
              <text id="node-5-detail" x="62" y="56" fill="#0284c7" font-size="9" text-anchor="middle">Drops to User Mode</text>
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
              <text x="20" y="26" fill="#0369a1" font-size="11" font-weight="700">ACTIVE BUS INTERCONNECT &amp; SYSTEM MAPPING</text>
              <text id="boot-flow-label" x="20" y="52" fill="#0f172a" font-size="11" font-family="var(--font-mono)">
                Hardware resets registers &rarr; CPU fetches first instruction from mapped ROM/Flash.
              </text>
              <text id="boot-flow-sublabel" x="20" y="74" fill="#64748b" font-size="10" font-family="var(--font-mono)">
                No RAM is initialized yet. Execution proceeds directly from non-volatile firmware storage.
              </text>
            </g>
          </svg>
        </div>

        <!-- Two-Pane Explanation Dashboard -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <!-- Current Action Pane -->
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0284c7; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #0284c7; text-transform: uppercase; letter-spacing: 0.03em;">Current State: What Is Happening</div>
            <div id="boot-desc-what" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;">
              Power stabilizes and the power supply asserts a hardware ready signal. The CPU resets its internal register state and sets the Program Counter to a hardwired physical address (the reset vector) mapped to non-volatile motherboard ROM/Flash.
            </div>
          </div>

          <!-- Rationale Pane -->
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #10b981; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 0.03em;">Why The System Does This</div>
            <div id="boot-desc-why" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;">
              Dynamic RAM (DRAM) is volatile and contains arbitrary noise at power-on. The CPU hardware must begin execution from an unchangeable non-volatile memory chip hardwired into the processor address space.
            </div>
          </div>
        </div>
      </div>

      <script>
        (function() {
          const osBootData = {
            linux: [
              {
                phase: "Stage 1 of 5: Power-On &amp; Reset Vector",
                target: "Motherboard ROM / SPI Flash",
                pc: "0xFFFFFFF0 (x86 Reset Vector)",
                mode: "Real Mode / Flat Protected",
                media: "Motherboard SPI Flash NVRAM",
                activeNode: "boot-node-power",
                activeLine: "boot-line-1",
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                inlineNext: "The UEFI / BIOS firmware will execute the POST, initialize DRAM memory channels, and scan NVRAM for boot drive entries.",
                flowTitle: "CPU RESET ASSERTION &rarr; Direct Flash ROM Instruction Fetch",
                flowSub: "No DRAM memory is initialized yet. The CPU fetches its first jump instruction directly from mapped flash storage.",
                node3Title: "3. GRUB / Systemd-boot",
                node3Sub: "ESP (/EFI/BOOT)",
                node3Detail: "Reads grub.cfg",
                node4Title: "4. vmlinuz &amp; initramfs",
                node4Sub: "Staged into RAM",
                node4Detail: "startup_64 entry",
                node5Title: "5. systemd / init",
                node5Sub: "PID 1 in User Space",
                node5Detail: "Target default.target",
                what: "On power stabilization, the motherboard asserts the reset line. The CPU initializes registers and vectors to <code>0xFFFFFFF0</code> in flash ROM, beginning execution in motherboard firmware (UEFI or legacy BIOS).",
                why: "DRAM is volatile and empty at power-on. The CPU requires a hardwired non-volatile address to begin instruction fetching without software dependencies."
              },
              {
                phase: "Stage 2 of 5: Hardware Self-Test &amp; Bus Discovery",
                target: "UEFI / BIOS Firmware Runtime",
                pc: "Firmware Entry Vector",
                mode: "Privileged Firmware Context",
                media: "Motherboard Flash ROM / NVRAM",
                activeNode: "boot-node-firmware",
                activeLine: "boot-line-2",
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                inlineNext: "The firmware will read the Linux EFI bootloader (GRUB or systemd-boot) from the EFI System Partition (ESP).",
                flowTitle: "POST &amp; BUS DISCOVERY &rarr; Memory Training &amp; NVRAM Lookup",
                flowSub: "Firmware verifies RAM chips, probes PCIe/NVMe storage controllers, and loads boot variables.",
                node3Title: "3. GRUB / Systemd-boot",
                node3Sub: "ESP (/EFI/BOOT)",
                node3Detail: "Reads grub.cfg",
                node4Title: "4. vmlinuz &amp; initramfs",
                node4Sub: "Staged into RAM",
                node4Detail: "startup_64 entry",
                node5Title: "5. systemd / init",
                node5Sub: "PID 1 in User Space",
                node5Detail: "Target default.target",
                what: "The firmware runs POST, trains the DRAM memory controller, scans PCIe/USB buses for devices, and queries UEFI NVRAM variables to identify the designated Linux boot disk.",
                why: "The operating system cannot run until physical memory and peripheral buses operate with stable electrical signaling."
              },
              {
                phase: "Stage 3 of 5: Linux Bootloader (GRUB / systemd-boot)",
                target: "ESP: /EFI/BOOT/grubx64.efi",
                pc: "0x00007C00 (MBR) or EFI Image Base",
                mode: "32/64-bit Protected Mode",
                media: "Storage Media (NVMe / SATA SSD)",
                activeNode: "boot-node-storage",
                activeLine: "boot-line-3",
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                inlineNext: "The bootloader will stage the compressed kernel image (vmlinuz) and initial ramdisk (initramfs) into physical memory.",
                flowTitle: "BOOTLOADER STAGING &rarr; Reading Kernel Images into RAM",
                flowSub: "GRUB displays boot menu, parses grub.cfg, and reads vmlinuz and initramfs from the filesystem.",
                node3Title: "3. GRUB / Systemd-boot",
                node3Sub: "ESP (/EFI/BOOT)",
                node3Detail: "Reads grub.cfg",
                node4Title: "4. vmlinuz &amp; initramfs",
                node4Sub: "Staged into RAM",
                node4Detail: "startup_64 entry",
                node5Title: "5. systemd / init",
                node5Sub: "PID 1 in User Space",
                node5Detail: "Target default.target",
                what: "Firmware loads <code>grubx64.efi</code> into RAM. GRUB reads its configuration file, mounts the ext4/Btrfs boot partition, and stages <code>vmlinuz</code> and <code>initramfs</code> into memory.",
                why: "UEFI firmware lacks deep knowledge of Linux file systems. A dedicated bootloader bridges firmware and the Linux kernel."
              },
              {
                phase: "Stage 4 of 5: Kernel Decompression &amp; Subsystem Init",
                target: "Linux Kernel (startup_64 in RAM)",
                pc: "0xFFFFFFFF81000000 (Kernel Virtual Base)",
                mode: "Kernel Mode (Ring 0 / Long Mode)",
                media: "System RAM (DRAM)",
                activeNode: "boot-node-ram",
                activeLine: "boot-line-4",
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                inlineNext: "The Linux kernel will mount the root filesystem, activate virtual memory paging, and spawn /sbin/init or systemd.",
                flowTitle: "KERNEL EXTRACTION &rarr; Hardware Takeover &amp; MMU Page Table Setup",
                flowSub: "Kernel initializes 4-level page tables, sets up IDT vectors, and loads built-in hardware drivers.",
                node3Title: "3. GRUB / Systemd-boot",
                node3Sub: "ESP (/EFI/BOOT)",
                node3Detail: "Reads grub.cfg",
                node4Title: "4. vmlinuz &amp; initramfs",
                node4Sub: "Staged into RAM",
                node4Detail: "startup_64 entry",
                node5Title: "5. systemd / init",
                node5Sub: "PID 1 in User Space",
                node5Detail: "Target default.target",
                what: "The kernel decompresses into memory, initializes MMU 4-level page tables, builds the IDT, and initializes device drivers using the temporary <code>initramfs</code> before mounting the real root filesystem.",
                why: "Firmware services are permanently discarded. The Linux kernel takes direct ownership of physical hardware and memory protection."
              },
              {
                phase: "Stage 5 of 5: Userspace Hand-off (PID 1: systemd)",
                target: "/sbin/init or /usr/lib/systemd/systemd",
                pc: "Userspace Program Entry",
                mode: "User Mode (Ring 3)",
                media: "Root Filesystem (ext4 / Btrfs / XFS)",
                activeNode: "boot-node-kernel",
                activeLine: "boot-line-5",
                btnNextText: "Restart Walkthrough &#8634;",
                btnPrevText: "&larr; Prev",
                inlineNext: "Boot sequence complete. Clicking restart will reset the walkthrough back to Stage 1.",
                flowTitle: "USERSPACE HAND-OFF &rarr; Execution of PID 1 in Ring 3",
                flowSub: "Kernel drops privileges, switches mode bit to 1, and systemd spawns login managers and daemons.",
                node3Title: "3. GRUB / Systemd-boot",
                node3Sub: "ESP (/EFI/BOOT)",
                node3Detail: "Reads grub.cfg",
                node4Title: "4. vmlinuz &amp; initramfs",
                node4Sub: "Staged into RAM",
                node4Detail: "startup_64 entry",
                node5Title: "5. systemd / init",
                node5Sub: "PID 1 in User Space",
                node5Detail: "Target default.target",
                what: "The kernel executes <code>/sbin/init</code> (typically symlinked to <code>systemd</code>) as PID 1, transitioning the CPU from Ring 0 to Ring 3 (User Mode). Systemd starts user services and the display manager.",
                why: "The system transitions to steady-state execution where all user software runs unprivileged and interacts with hardware solely via system calls."
              }
            ],
            windows: [
              {
                phase: "Stage 1 of 5: Power-On &amp; Reset Vector",
                target: "Motherboard ROM / SPI Flash",
                pc: "0xFFFFFFF0 (x86 Reset Vector)",
                mode: "Real Mode / Flat Protected",
                media: "Motherboard SPI Flash NVRAM",
                activeNode: "boot-node-power",
                activeLine: "boot-line-1",
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                inlineNext: "UEFI firmware will execute POST, train memory, and read the Windows Boot Manager entry in NVRAM.",
                flowTitle: "CPU RESET ASSERTION &rarr; Direct Flash ROM Instruction Fetch",
                flowSub: "Motherboard power circuitry stabilizes. CPU fetches first instruction from flash ROM.",
                node3Title: "3. bootmgfw.efi",
                node3Sub: "Windows Boot Manager",
                node3Detail: "Reads BCD Store",
                node4Title: "4. winload.efi &amp; ntoskrnl",
                node4Sub: "Staged into RAM",
                node4Detail: "KiSystemStartup",
                node5Title: "5. smss.exe &amp; csrss",
                node5Sub: "Session Manager Subsystem",
                node5Detail: "Spawns winlogon",
                what: "Voltages stabilize and the motherboard asserts the reset line. The CPU clears its registers and vectors to <code>0xFFFFFFF0</code> to begin execution in UEFI firmware.",
                why: "Main memory is volatile. The CPU requires a dedicated hardware address mapped to non-volatile flash ROM to execute instructions on power-on."
              },
              {
                phase: "Stage 2 of 5: Hardware Self-Test &amp; Bus Discovery",
                target: "UEFI Firmware Runtime",
                pc: "Firmware Entry Vector",
                mode: "Privileged Firmware Context",
                media: "Motherboard Flash ROM / NVRAM",
                activeNode: "boot-node-firmware",
                activeLine: "boot-line-2",
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                inlineNext: "Firmware will locate the Windows Boot Manager (bootmgfw.efi) in the EFI System Partition.",
                flowTitle: "POST &amp; BUS DISCOVERY &rarr; Memory Training &amp; BCD Entry Resolution",
                flowSub: "Firmware trains memory controllers, initializes PCIe storage buses, and selects Windows boot entry.",
                node3Title: "3. bootmgfw.efi",
                node3Sub: "Windows Boot Manager",
                node3Detail: "Reads BCD Store",
                node4Title: "4. winload.efi &amp; ntoskrnl",
                node4Sub: "Staged into RAM",
                node4Detail: "KiSystemStartup",
                node5Title: "5. smss.exe &amp; csrss",
                node5Sub: "Session Manager Subsystem",
                node5Detail: "Spawns winlogon",
                what: "UEFI firmware executes the Power-On Self-Test (POST), checks physical RAM, initializes NVMe/SATA storage controllers, and inspects NVRAM to find the Windows Boot Manager entry.",
                why: "Hardware initialization ensures DRAM timings and device buses are operating reliably before passing control to the Windows operating system loader."
              },
              {
                phase: "Stage 3 of 5: Windows Boot Manager &amp; OS Loader",
                target: "ESP: \\\\EFI\\\\Microsoft\\\\Boot\\\\bootmgfw.efi",
                pc: "UEFI Executable Entry",
                mode: "64-bit UEFI Protected Environment",
                media: "EFI System Partition (FAT32)",
                activeNode: "boot-node-storage",
                activeLine: "boot-line-3",
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                inlineNext: "winload.efi will read ntoskrnl.exe, hal.dll, and boot-start drivers into physical RAM.",
                flowTitle: "WINDOWS BOOT MANAGER &rarr; Reading BCD &amp; Invoking winload.efi",
                flowSub: "bootmgfw.efi reads the BCD registry hive, locates the Windows partition, and launches winload.efi.",
                node3Title: "3. bootmgfw.efi",
                node3Sub: "Windows Boot Manager",
                node3Detail: "Reads BCD Store",
                node4Title: "4. winload.efi &amp; ntoskrnl",
                node4Sub: "Staged into RAM",
                node4Detail: "KiSystemStartup",
                node5Title: "5. smss.exe &amp; csrss",
                node5Sub: "Session Manager Subsystem",
                node5Detail: "Spawns winlogon",
                what: "UEFI runs <code>bootmgfw.efi</code>, which reads the Boot Configuration Data (BCD) store. It identifies the Windows OS partition and launches the Windows OS Loader (<code>winload.efi</code>).",
                why: "The Windows Boot Manager isolates the firmware interface from the Windows kernel and allows multi-boot selection or recovery mode options."
              },
              {
                phase: "Stage 4 of 5: Kernel Staging &amp; Subsystem Init (ntoskrnl.exe)",
                target: "Windows NT Kernel (ntoskrnl.exe)",
                pc: "KiSystemStartup Entry Point",
                mode: "Kernel Mode (Ring 0 / 64-bit)",
                media: "System RAM (DRAM)",
                activeNode: "boot-node-ram",
                activeLine: "boot-line-4",
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                inlineNext: "The NT kernel will initialize the Object Manager, mount NTFS, and spawn the Session Manager (smss.exe).",
                flowTitle: "KERNEL INITIALIZATION &rarr; ntoskrnl.exe &amp; hal.dll Hardware Takeover",
                flowSub: "winload.efi enables paging, exits UEFI services, and transfers control to KiSystemStartup.",
                node3Title: "3. bootmgfw.efi",
                node3Sub: "Windows Boot Manager",
                node3Detail: "Reads BCD Store",
                node4Title: "4. winload.efi &amp; ntoskrnl",
                node4Sub: "Staged into RAM",
                node4Detail: "KiSystemStartup",
                node5Title: "5. smss.exe &amp; csrss",
                node5Sub: "Session Manager Subsystem",
                node5Detail: "Spawns winlogon",
                what: "<code>winload.efi</code> loads <code>ntoskrnl.exe</code>, the Hardware Abstraction Layer (<code>hal.dll</code>), and boot drivers. It sets up page tables, calls <code>ExitBootServices()</code>, and branches to <code>KiSystemStartup</code>.",
                why: "The Windows NT kernel takes complete control of the processor and establishes virtual memory translation, permanently discarding firmware runtimes."
              },
              {
                phase: "Stage 5 of 5: Userspace Hand-off (smss.exe &amp; csrss.exe)",
                target: "\\\\SystemRoot\\\\System32\\\\smss.exe",
                pc: "Userspace Process Entry",
                mode: "User Mode (Ring 3)",
                media: "Windows System Drive (NTFS)",
                activeNode: "boot-node-kernel",
                activeLine: "boot-line-5",
                btnNextText: "Restart Walkthrough &#8634;",
                btnPrevText: "&larr; Prev",
                inlineNext: "Boot sequence complete. Clicking restart will reset the walkthrough back to Stage 1.",
                flowTitle: "USERSPACE HAND-OFF &rarr; Spawning smss.exe &amp; Windows Subsystem",
                flowSub: "smss.exe starts csrss.exe (Win32), wininit.exe, and winlogon.exe to present the user login screen.",
                node3Title: "3. bootmgfw.efi",
                node3Sub: "Windows Boot Manager",
                node3Detail: "Reads BCD Store",
                node4Title: "4. winload.efi &amp; ntoskrnl",
                node4Sub: "Staged into RAM",
                node4Detail: "KiSystemStartup",
                node5Title: "5. smss.exe &amp; csrss",
                node5Sub: "Session Manager Subsystem",
                node5Detail: "Spawns winlogon",
                what: "The kernel executes the Session Manager Subsystem (<code>smss.exe</code>) in user mode (Ring 3). <code>smss.exe</code> creates environment variables, starts the Client/Server Runtime (<code>csrss.exe</code>), and launches <code>winlogon.exe</code>.",
                why: "The system reaches normal desktop state. All applications execute in isolated Ring 3 environments with mediated access through Win32/NT system calls."
              }
            ],
            macos: [
              {
                phase: "Stage 1 of 5: Power-On &amp; Reset Vector",
                target: "Apple Silicon Boot ROM / Flash",
                pc: "Hardware Reset Vector",
                mode: "Secure Boot Secure World / EL3",
                media: "On-Chip Secure Boot ROM",
                activeNode: "boot-node-power",
                activeLine: "boot-line-1",
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                inlineNext: "The Boot ROM will verify the cryptographic signature of the low-level bootloader (LLB / iBoot).",
                flowTitle: "HARDWARE RESET ASSERTION &rarr; On-Chip Boot ROM Execution",
                flowSub: "Apple Silicon chip powers on. Hardware starts execution from unchangeable internal Mask ROM.",
                node3Title: "3. iBoot / boot.efi",
                node3Sub: "Stage 2 Bootloader",
                node3Detail: "Verifies APFS Volume",
                node4Title: "4. XNU Kernel",
                node4Sub: "mach_kernel in RAM",
                node4Detail: "i386_init / arm_init",
                node5Title: "5. launchd (PID 1)",
                node5Sub: "Userspace Master Daemon",
                node5Detail: "Spawns WindowServer",
                what: "On power-on, the processor initializes and begins execution directly from immutable on-die Mask ROM (on Apple Silicon) or UEFI firmware (on Intel Macs).",
                why: "Establishing an unbroken cryptographic hardware Root of Trust requires the earliest instructions to reside in read-only silicon that cannot be tampered with."
              },
              {
                phase: "Stage 2 of 5: Hardware Self-Test &amp; Low-Level Boot",
                target: "Low-Level Bootloader (LLB / iBoot Stage 1)",
                pc: "Firmware Stage Entry",
                mode: "Privileged Firmware Context",
                media: "NAND Storage (SysCfg)",
                activeNode: "boot-node-firmware",
                activeLine: "boot-line-2",
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                inlineNext: "iBoot will initialize the memory controller, verify APFS seals, and locate the macOS boot kernelcache.",
                flowTitle: "POST &amp; MEMORY TRAINING &rarr; Hardware Signature Verification",
                flowSub: "iBoot calibrates unified memory, verifies hardware security certificates, and scans storage.",
                node3Title: "3. iBoot / boot.efi",
                node3Sub: "Stage 2 Bootloader",
                node3Detail: "Verifies APFS Volume",
                node4Title: "4. XNU Kernel",
                node4Sub: "mach_kernel in RAM",
                node4Detail: "i386_init / arm_init",
                node5Title: "5. launchd (PID 1)",
                node5Sub: "Userspace Master Daemon",
                node5Detail: "Spawns WindowServer",
                what: "The low-level firmware tests hardware components, initializes the unified memory architecture (UMA), interrogates attached NVMe storage, and validates cryptographic signatures.",
                why: "macOS enforces strict secure boot verification at every hand-off stage before granting access to unified memory or storage buses."
              },
              {
                phase: "Stage 3 of 5: Stage 2 Bootloader (iBoot / boot.efi)",
                target: "Apple File System (APFS Preboot Volume)",
                pc: "Bootloader Entry Address",
                mode: "Privileged Execution Environment",
                media: "APFS Preboot Container",
                activeNode: "boot-node-storage",
                activeLine: "boot-line-3",
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                inlineNext: "The bootloader will stage the authenticated kernelcache (XNU kernel, Mach, BSD, and I/O Kit) into memory.",
                flowTitle: "BOOTLOADER STAGING &rarr; Reading Sealed Kernel Collection into RAM",
                flowSub: "iBoot loads boot.efi, verifies the Sealed System Volume (SSV) hash, and prepares DeviceTree.",
                node3Title: "3. iBoot / boot.efi",
                node3Sub: "Stage 2 Bootloader",
                node3Detail: "Verifies APFS Volume",
                node4Title: "4. XNU Kernel",
                node4Sub: "mach_kernel in RAM",
                node4Detail: "i386_init / arm_init",
                node5Title: "5. launchd (PID 1)",
                node5Sub: "Userspace Master Daemon",
                node5Detail: "Spawns WindowServer",
                what: "The Stage 2 bootloader loads the Sealed System Volume cryptographic manifests, validates the macOS kernelcache (or boot collection), and stages it into system RAM alongside the Device Tree.",
                why: "macOS runs from an immutable, cryptographically signed snapshot of the system volume, preventing unauthorized modification."
              },
              {
                phase: "Stage 4 of 5: XNU Kernel Initialization (Mach + BSD)",
                target: "XNU Kernel (mach_kernel in RAM)",
                pc: "Kernel Entry Point",
                mode: "Kernel Mode (Ring 0 / EL1)",
                media: "Unified System RAM",
                activeNode: "boot-node-ram",
                activeLine: "boot-line-4",
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                inlineNext: "The XNU kernel will mount the read-only APFS system volume and spawn launchd as process ID 1.",
                flowTitle: "KERNEL TAKEOVER &rarr; Mach VM, BSD Subsystems, &amp; I/O Kit Drivers",
                flowSub: "Kernel enables MMU translation, starts task scheduling, and attaches C++ I/O Kit device drivers.",
                node3Title: "3. iBoot / boot.efi",
                node3Sub: "Stage 2 Bootloader",
                node3Detail: "Verifies APFS Volume",
                node4Title: "4. XNU Kernel",
                node4Sub: "mach_kernel in RAM",
                node4Detail: "i386_init / arm_init",
                node5Title: "5. launchd (PID 1)",
                node5Sub: "Userspace Master Daemon",
                node5Detail: "Spawns WindowServer",
                what: "Execution transfers to the XNU kernel. The Mach microkernel core activates virtual memory and threads, BSD layer sets up POSIX interfaces, and I/O Kit loads object-oriented device drivers.",
                why: "XNU combines Mach memory virtualization with BSD POSIX APIs to manage the complete unified hardware complex securely."
              },
              {
                phase: "Stage 5 of 5: Userspace Hand-off (launchd PID 1)",
                target: "/sbin/launchd",
                pc: "Userspace Program Entry",
                mode: "User Mode (Ring 3 / EL0)",
                media: "Sealed System Volume (APFS)",
                activeNode: "boot-node-kernel",
                activeLine: "boot-line-5",
                btnNextText: "Restart Walkthrough &#8634;",
                btnPrevText: "&larr; Prev",
                inlineNext: "Boot sequence complete. Clicking restart will reset the walkthrough back to Stage 1.",
                flowTitle: "USERSPACE HAND-OFF &rarr; launchd Daemon &amp; WindowServer",
                flowSub: "Kernel drops to User Mode, launchd manages daemons, and WindowServer presents the login screen.",
                node3Title: "3. iBoot / boot.efi",
                node3Sub: "Stage 2 Bootloader",
                node3Detail: "Verifies APFS Volume",
                node4Title: "4. XNU Kernel",
                node4Sub: "mach_kernel in RAM",
                node4Detail: "i386_init / arm_init",
                node5Title: "5. launchd (PID 1)",
                node5Sub: "Userspace Master Daemon",
                node5Detail: "Spawns WindowServer",
                what: "The kernel executes <code>/sbin/launchd</code> as PID 1 in user space (Ring 3 / EL0). <code>launchd</code> reads LaunchDaemons property lists, initializes system services, and starts <code>WindowServer</code>.",
                why: "The system reaches full graphical multi-user operation. User applications run unprivileged and access system services via POSIX and Mach system calls."
              }
            ]
          };

          let currentOS = "linux";
          let bootIndex = 0;

          function renderBootState() {
            const data = osBootData[currentOS][bootIndex];
            document.getElementById("boot-status-phase").innerHTML = data.phase;
            document.getElementById("boot-status-target").textContent = data.target;
            document.getElementById("boot-status-pc").textContent = data.pc;
            document.getElementById("boot-status-mode").textContent = data.mode;
            document.getElementById("boot-status-media").textContent = data.media;

            document.getElementById("boot-inline-next-desc").innerHTML = data.inlineNext;
            document.getElementById("boot-desc-what").innerHTML = data.what;
            document.getElementById("boot-desc-why").innerHTML = data.why;

            document.getElementById("boot-flow-label").textContent = data.flowTitle;
            document.getElementById("boot-flow-sublabel").textContent = data.flowSub;

            // Update dynamic SVG node labels
            document.getElementById("node-3-title").textContent = data.node3Title;
            document.getElementById("node-3-sub").textContent = data.node3Sub;
            document.getElementById("node-3-detail").textContent = data.node3Detail;

            document.getElementById("node-4-title").textContent = data.node4Title;
            document.getElementById("node-4-sub").textContent = data.node4Sub;
            document.getElementById("node-4-detail").textContent = data.node4Detail;

            document.getElementById("node-5-title").textContent = data.node5Title;
            document.getElementById("node-5-sub").textContent = data.node5Sub;
            document.getElementById("node-5-detail").textContent = data.node5Detail;

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

          function setOSSelection(osKey) {
            currentOS = osKey;
            const osButtons = {
              linux: document.getElementById("btn-os-linux"),
              windows: document.getElementById("btn-os-windows"),
              macos: document.getElementById("btn-os-macos")
            };
            Object.keys(osButtons).forEach(key => {
              const btn = osButtons[key];
              if (btn) {
                if (key === osKey) {
                  btn.style.background = "#0284c7";
                  btn.style.color = "#ffffff";
                } else {
                  btn.style.background = "transparent";
                  btn.style.color = "#475569";
                }
              }
            });
            renderBootState();
          }

          document.getElementById("btn-os-linux").addEventListener("click", () => setOSSelection("linux"));
          document.getElementById("btn-os-windows").addEventListener("click", () => setOSSelection("windows"));
          document.getElementById("btn-os-macos").addEventListener("click", () => setOSSelection("macos"));

          document.getElementById("boot-next-btn").addEventListener("click", function() {
            if (bootIndex < osBootData[currentOS].length - 1) {
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

def update_boot_simulator_with_os_toggle():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'<div id="interactive-boot-simulator".*?</script>'
    match = re.search(pattern, content, flags=re.DOTALL)
    if match:
        # Use substring slicing or a lambda to prevent Python regex template parser
        # from interpreting backslashes in Windows file paths as regex escapes
        start, end = match.span()
        content = content[:start] + MULTI_OS_BOOT_HTML.strip() + content[end:]
        print("--> Injected multi-OS toggle into boot sequence simulator.")
    else:
        print("--> Interactive boot simulator container not found.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Add multi-OS toggle (Linux, Windows, macOS) to boot sequence simulator\n\n"
            "Allow learners to switch between Linux, Windows, and macOS boot pipelines\n"
            "in week01-operating-system-concepts/02-hardware-review.html at any stage."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_boot_simulator_with_os_toggle()
