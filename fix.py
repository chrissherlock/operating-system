#!/usr/bin/env python3
# =====================================================================
# fix.py: Align Syscall Story preview card with current situation arc
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

TRAP_SIM_REPLACEMENT = """      <div id="interactive-trap-simulator" style="margin: 32px 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <!-- Header -->
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 18px;">
          <div>
            <h3 style="margin: 0; color: #0284c7; font-size: 1.15rem;">The Journey Across the Silicon Wall: A Syscall Story</h3>
            <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Follow a user application's request as it breaches hardware protection boundaries to read data from disk.</p>
          </div>

          <!-- Platform Selector -->
          <div style="display: flex; align-items: center; gap: 6px; background: #f1f5f9; padding: 4px; border-radius: 8px; border: 1px solid #cbd5e1;">
            <span style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #475569; padding: 0 6px;">Storyline:</span>
            <button id="btn-trap-unix" class="trap-os-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: #0284c7; color: #ffffff; cursor: pointer; transition: all 0.15s ease;">Linux / Unix</button>
            <button id="btn-trap-win" class="trap-os-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: transparent; color: #475569; cursor: pointer; transition: all 0.15s ease;">Windows NT</button>
          </div>
        </div>

        <!-- Instructions Guide -->
        <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px; margin-bottom: 16px;">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">How to Experience This Walkthrough</div>
          <ol style="margin-left: 20px; margin-bottom: 0; color: #334155; font-size: 0.88rem; line-height: 1.5;">
            <li><strong>Follow the Story Arc:</strong> The top card frames where we are in the story right now and what objective needs to happen next.</li>
            <li><strong>Step Forward to Advance:</strong> Click <code>Next Step &rarr;</code> to resolve that objective and enter the next chapter of the journey.</li>
            <li><strong>Compare Operating Systems:</strong> Toggle between <code>Linux / Unix</code> and <code>Windows NT</code> to observe how both designs tackle the exact same silicon boundary.</li>
          </ol>
        </div>

        <!-- Action Controls & Situation + Objective Card -->
        <div style="display: grid; grid-template-columns: auto 1fr; gap: 16px; align-items: stretch; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px; margin-bottom: 20px;">
          <div style="display: flex; flex-direction: column; gap: 8px; justify-content: center; min-width: 170px;">
            <button id="step-next-btn" style="padding: 10px 16px; font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; border-radius: 6px; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; cursor: pointer; text-align: center; transition: all 0.15s ease;">Next Step &rarr;</button>
            <div style="display: flex; gap: 8px;">
              <button id="step-prev-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 600; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">&larr; Prev</button>
              <button id="step-reset-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #64748b; cursor: pointer;">Reset</button>
            </div>
          </div>

          <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-left: 4px solid #0284c7; border-radius: 0 6px 6px 0; padding: 10px 14px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: #0369a1; text-transform: uppercase; letter-spacing: 0.03em;">Where We Are in the Story &amp; What Needs to Happen:</div>
            <div id="inline-next-desc" style="font-size: 0.88rem; color: #0c4a6e; line-height: 1.45; margin-top: 4px;">Loading chapter details...</div>
          </div>
        </div>

        <!-- Hardware State Bar -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin-bottom: 20px; font-family: var(--font-mono); font-size: 0.8rem;">
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">CPU Mode</div>
            <div id="status-cpu-mode" style="font-weight: 700; color: #dc2626; margin-top: 2px;">USER (Ring 3)</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Hardware Mode Bit</div>
            <div id="status-mode-bit" style="font-weight: 700; color: #dc2626; margin-top: 2px;">1 (Unprivileged)</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Instruction Pointer (PC)</div>
            <div id="status-pc-reg" style="font-weight: 700; color: #0284c7; margin-top: 2px;">0x00401140 (App)</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Active Stack</div>
            <div id="status-stack" style="font-weight: 700; color: #0284c7; margin-top: 2px;">User Stack (RSP)</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Chapter</div>
            <div id="status-step-num" style="font-weight: 700; color: #0f172a; margin-top: 2px;">Chapter 1 of 6</div>
          </div>
        </div>

        <!-- Interactive Vector Visualisation -->
        <div style="display: flex; justify-content: center; margin-bottom: 20px; overflow-x: auto;">
          <svg id="trap-anim-svg" viewBox="0 0 860 280" width="100%" height="auto" style="max-width: 860px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <marker id="marker-blue" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto">
                <path d="M0,0 L6,3 L0,6 Z" fill="#0284c7" />
              </marker>
            </defs>

            <!-- User Space Band -->
            <rect x="20" y="20" width="820" height="105" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="6,4" />
            <text x="35" y="42" fill="#64748b" font-size="11" font-weight="700">USER ADDRESS SPACE (Ring 3 - Sandbox)</text>

            <!-- Kernel Space Band -->
            <rect x="20" y="155" width="820" height="105" rx="6" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.5" />
            <text x="35" y="177" fill="#0369a1" font-size="11" font-weight="700">KERNEL ADDRESS SPACE (Ring 0 - Supervisor)</text>

            <!-- Node 1: User App -->
            <rect id="node-user-app" x="45" y="55" width="180" height="52" rx="5" fill="#ffffff" stroke="#0284c7" stroke-width="2" />
            <text id="trap-node1-title" x="135" y="78" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">User Application</text>
            <text id="trap-node1-sub" x="135" y="94" fill="#64748b" font-size="10" text-anchor="middle">Reads "report.txt"</text>

            <!-- Node 2: Library Stub / Trap Invocation -->
            <rect id="node-trap-trigger" x="280" y="55" width="190" height="52" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
            <text id="trap-node2-title" x="375" y="78" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">Runtime Stub</text>
            <text id="trap-node2-sub" x="375" y="94" fill="#64748b" font-size="10" text-anchor="middle">Stages Call &amp; Traps</text>

            <!-- Node 3: CPU Hardware Switch -->
            <rect id="node-cpu-hw" x="535" y="105" width="195" height="60" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="632" y="130" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">CPU Hardware Engine</text>
            <text x="632" y="148" fill="#64748b" font-size="10" text-anchor="middle">Mode: 1 &rarr; 0 | Stack Swapped</text>

            <!-- Node 4: Kernel Dispatcher -->
            <rect id="node-kernel-idt" x="280" y="185" width="190" height="52" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
            <text id="trap-node4-title" x="375" y="208" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">Kernel Dispatcher</text>
            <text id="trap-node4-sub" x="375" y="224" fill="#64748b" font-size="10" text-anchor="middle">Validates Pointers</text>

            <!-- Node 5: Kernel Service / Device -->
            <rect id="node-kernel-driver" x="45" y="185" width="180" height="52" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
            <text id="trap-node5-title" x="135" y="208" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">Storage Driver</text>
            <text id="trap-node5-sub" x="135" y="224" fill="#64748b" font-size="10" text-anchor="middle">Commands NVMe Bus</text>

            <!-- Connecting Flows -->
            <line id="edge-1" x1="225" y1="81" x2="275" y2="81" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />
            <path id="edge-2" d="M 470,81 L 530,125" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />
            <path id="edge-3" d="M 535,145 L 475,200" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />
            <line id="edge-4" x1="280" y1="211" x2="230" y2="211" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />
            <path id="edge-5" d="M 135,185 C 135,145 135,120 135,113" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#marker-blue)" />
          </svg>
        </div>

        <!-- Two-Pane Story Dashboard -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 20px;">
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0284c7; padding: 16px; border-radius: 0 6px 6px 0;">
            <div id="story-heading-what" style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #0284c7; text-transform: uppercase; letter-spacing: 0.03em;">Detailed Mechanics: Active Chapter</div>
            <div id="desc-what" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>

          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #10b981; padding: 16px; border-radius: 0 6px 6px 0;">
            <div id="story-heading-why" style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 0.03em;">Behind the Curtain: Architectural Rationale</div>
            <div id="desc-why" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>
        </div>
      </div>

      <script>
        (function() {
          const trapStorylines = {
            unix: [
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x00401140 (App Text Editor)",
                stack: "User Stack (RSP = 0x7FFF5000)",
                stepNum: "Chapter 1 of 6: The Unprivileged Application Reaches a Wall",
                activeNode: "node-user-app",
                activeEdges: [],
                btnNextText: "Next: Enter Library Wrapper &rarr;",
                btnPrevText: "&larr; Prev",
                node1Title: "Text Editor (PID 402)",
                node1Sub: "read(fd, buffer, 512)",
                node2Title: "C Library (glibc)",
                node2Sub: "Prepares Syscall",
                node4Title: "Syscall Table",
                node4Sub: "sys_call_table[__NR_read]",
                node5Title: "VFS &amp; NVMe Driver",
                node5Sub: "Reads Blocks from Disk",
                what: "Our Unix story begins inside a text editor running in User Space. The user opens <code>report.txt</code>, and the program needs 512 bytes from disk. It calls <code>read(fd, buffer, 512)</code>. The CPU is running in User Mode (Mode Bit = 1). The application cannot send voltage pulses across the storage bus or touch physical disk sectors directly; doing so would trigger an immediate General Protection Fault.",
                why: "If any running application could manipulate the storage bus directly, a buggy program could corrupt files belonging to other users or read password hashes straight off the disk platters. The CPU hardware enforces a strict sandbox (Ring 3) to protect system integrity.",
                situationObj: "<strong>Where we are:</strong> We are in the initial unprivileged state. The text editor wants to read 512 bytes from <code>report.txt</code>, but it cannot touch the physical disk directly without crashing.<br><br><strong>What we need to do next:</strong> We need the application to call the runtime library wrapper (<code>glibc</code>) to stage the system call arguments into CPU registers. Click <strong>Next Step</strong> to proceed."
              },
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x004085A0 (glibc syscall stub)",
                stack: "User Stack (RSP = 0x7FFF4FE0)",
                stepNum: "Chapter 2 of 6: Staging Registers &amp; The Trap Invocation",
                activeNode: "node-trap-trigger",
                activeEdges: ["edge-1"],
                btnNextText: "Next: Trigger Hardware Trap &rarr;",
                btnPrevText: "&larr; Prev: Application Call",
                node1Title: "Text Editor (PID 402)",
                node1Sub: "Waiting on I/O",
                node2Title: "glibc Syscall Stub",
                node2Sub: "RAX=0 (sys_read) &rarr; SYSCALL",
                node4Title: "Syscall Table",
                node4Sub: "sys_call_table[0]",
                node5Title: "VFS &amp; NVMe Driver",
                node5Sub: "Reads Blocks from Disk",
                what: "Execution is currently inside the C runtime library (glibc). The library stub has staged the parameters: <code>RAX = 0</code> (Linux syscall number for <code>sys_read</code>), <code>RDI = fd</code>, <code>RSI = buffer pointer</code>, and <code>RDX = 512</code>. The CPU is paused right on the <code>SYSCALL</code> instruction, ready to trigger the boundary cross.",
                why: "An unprivileged program cannot modify its own privilege level; the CPU hardware rejects any software instruction attempting to clear the mode bit. The <code>SYSCALL</code> instruction acts as a controlled gateway—an intentional architectural escape hatch into the supervisor.",
                situationObj: "<strong>Where we are:</strong> The C library has loaded the request details into registers, but execution is still trapped in User Space.<br><br><strong>What we need to do next:</strong> We need to breach the silicon boundary by executing the <code>SYSCALL</code> instruction so hardware can elevate privilege to Ring 0. Click <strong>Next Step</strong> to trigger the hardware trap."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Supervisor Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFFFFF81A00000 (MSR_LSTAR Entry)",
                stack: "Switched to Kernel Stack (SS:RSP)",
                stepNum: "Chapter 3 of 6: The Silicon Gate Snaps Shut (Hardware Takeover)",
                activeNode: "node-cpu-hw",
                activeEdges: ["edge-2"],
                btnNextText: "Next: Route in Syscall Table &rarr;",
                btnPrevText: "&larr; Prev: SYSCALL Trigger",
                node1Title: "Text Editor (PID 402)",
                node1Sub: "Suspended (State Saved)",
                node2Title: "glibc Syscall Stub",
                node2Sub: "Trapped into Hardware",
                node4Title: "entry_SYSCALL_64",
                node4Sub: "Validates Registers",
                node5Title: "VFS &amp; NVMe Driver",
                node5Sub: "Reads Blocks from Disk",
                what: "The CPU microcode has taken control and crossed the silicon wall. It has cleared the Mode Bit from <code>1</code> to <code>0</code>, saved the user Program Counter and Stack Pointer onto the process's private kernel stack, and branched to the entry point stored in the CPU's Model-Specific Register (<code>MSR_LSTAR</code>).",
                why: "The CPU switches to a private kernel stack because user-space memory is untrusted. If the kernel used the user's stack, a malicious concurrent thread could rewrite return addresses while the kernel was running in Ring 0, hijacking the supervisor.",
                situationObj: "<strong>Where we are:</strong> The CPU hardware has switched to Ring 0, swapped to the isolated kernel stack, and jumped to <code>MSR_LSTAR</code>. We are inside the kernel, but the file read has not been started.<br><br><strong>What we need to do next:</strong> We need the kernel entry handler to inspect the syscall catalog number in <code>RAX</code> and route execution through the system call table. Click <strong>Next Step</strong> to route the call."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Supervisor Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFFFFF81B23040 (sys_call_table)",
                stack: "Kernel Stack (0xFFFFC900...)",
                stepNum: "Chapter 4 of 6: The Royal Guard Inspects Credentials",
                activeNode: "node-kernel-idt",
                activeEdges: ["edge-3"],
                btnNextText: "Next: Command the Hardware &rarr;",
                btnPrevText: "&larr; Prev: Hardware Switch",
                node1Title: "Text Editor (PID 402)",
                node1Sub: "Suspended (State Saved)",
                node2Title: "glibc Syscall Stub",
                node2Sub: "Trapped into Hardware",
                node4Title: "Syscall Dispatcher",
                node4Sub: "Verifies Buffer Pointers",
                node5Title: "VFS &amp; NVMe Driver",
                node5Sub: "Dispatches Disk Command",
                what: "The kernel dispatcher has read <code>RAX = 0</code> and indexed into <code>sys_call_table</code> to locate <code>sys_read</code>. It is currently validating the buffer address in <code>RSI</code> to ensure the entire destination range resides inside unprivileged user memory and is writable.",
                why: "This prevents 'confused deputy' exploits: if the kernel blindly accepted any memory pointer without checking, a malicious program could pass a pointer to the kernel's own page tables and trick the kernel into overwriting its own security structures with file data.",
                situationObj: "<strong>Where we are:</strong> We have reached the system call table. The kernel knows a read was requested, but user-space pointers cannot be trusted blindly.<br><br><strong>What we need to do next:</strong> We need to verify that the destination buffer is safe and writable, then command the physical storage driver. Click <strong>Next Step</strong> to dispatch the disk command."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Supervisor Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFFFFF81C84100 (nvme_queue_rq)",
                stack: "Kernel Stack (0xFFFFC900...)",
                stepNum: "Chapter 5 of 6: Touching Reality (Privileged I/O)",
                activeNode: "node-kernel-driver",
                activeEdges: ["edge-4"],
                btnNextText: "Next: Return to User Mode &rarr;",
                btnPrevText: "&larr; Prev: Syscall Dispatch",
                node1Title: "Text Editor (PID 402)",
                node1Sub: "Waiting on I/O Sleep",
                node2Title: "glibc Syscall Stub",
                node2Sub: "Waiting for Bytes",
                node4Title: "Syscall Dispatcher",
                node4Sub: "VFS &rarr; Block Layer",
                node5Title: "NVMe Device Driver",
                node5Sub: "Issues DMA Command",
                what: "The Virtual File System (VFS) has mapped the file offset to physical storage blocks. The NVMe device driver has programmed the controller registers across the PCIe bus. Direct Memory Access (DMA) has streamed the 512 bytes directly into RAM, and a hardware interrupt has just signaled transfer completion.",
                why: "Only in Ring 0 are hardware I/O ports and device memory maps accessible. Because device drivers run inside the kernel, the OS ensures programs only access disk sectors allocated to their own authorized open files.",
                situationObj: "<strong>Where we are:</strong> The storage driver has completed the DMA block read and the 512 bytes now sit in memory. We are finished executing in supervisor mode.<br><br><strong>What we need to do next:</strong> We need to load the byte count into <code>RAX</code> and return execution back across the silicon wall into unprivileged User Space. Click <strong>Next Step</strong> to execute the return instruction."
              },
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x00401148 (Resumed App Code)",
                stack: "Restored User Stack (RSP = 0x7FFF5000)",
                stepNum: "Chapter 6 of 6: The Return Home (Dropping Privilege)",
                activeNode: "node-user-app",
                activeEdges: ["edge-5"],
                btnNextText: "Replay the Journey &#8634;",
                btnPrevText: "&larr; Prev: Driver Execution",
                node1Title: "Text Editor (PID 402)",
                node1Sub: "512 Bytes Ready in Memory!",
                node2Title: "glibc Syscall Stub",
                node2Sub: "read() Returned 512",
                node4Title: "Syscall Dispatcher",
                node4Sub: "sys_read Complete",
                node5Title: "NVMe Device Driver",
                node5Sub: "I/O Transfer Finished",
                what: "The journey is complete. The kernel wrote <code>512</code> into <code>RAX</code> and executed <code>SYSRET</code>. In a single clock cycle, the CPU hardware restored Mode Bit = 1, reloaded the user stack pointer, and resumed application execution. The text editor now has the file contents in its local buffer.",
                why: "The system returns to steady-state unprivileged execution. The application received its file data without ever being granted supervisor authority or breaking out of its hardware sandbox.",
                situationObj: "<strong>Where we are:</strong> We have returned home safely to User Space. The text editor has its 512 bytes, the file content is displayed, and the application resumes normal execution in Ring 3.<br><br><strong>What we need to do next:</strong> The story has concluded. Click <strong>Replay</strong> if you wish to reset and experience the walkthrough from the beginning."
              }
            ],
            windows: [
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x00007FF710001200 (Notepad.exe)",
                stack: "User Stack (RSP = 0x00000080...)",
                stepNum: "Chapter 1 of 6: The Win32 Application Requests Help",
                activeNode: "node-user-app",
                activeEdges: [],
                btnNextText: "Next: Enter Subsystem DLLs &rarr;",
                btnPrevText: "&larr; Prev",
                node1Title: "Notepad (PID 1024)",
                node1Sub: "ReadFile(hFile, buf, 512)",
                node2Title: "kernel32 &rarr; ntdll",
                node2Sub: "Prepares Syscall",
                node4Title: "KiSystemCall64 / SSDT",
                node4Sub: "KeServiceDescriptorTable",
                node5Title: "I/O Manager &amp; Drivers",
                node5Sub: "Allocates IRP &rarr; NTFS",
                what: "Our Windows story begins inside Notepad running in User Space. The user opens <code>report.txt</code>. Notepad calls the standard Win32 API function <code>ReadFile()</code> in <code>kernel32.dll</code> / <code>kernelbase.dll</code>. Notepad runs in Ring 3 (Mode Bit = 1). If it attempted to issue raw storage commands, the processor would throw a hardware exception.",
                why: "Microsoft intentionally isolates user applications behind subsystem DLLs. While Unix syscall numbers remain stable across releases, Windows system service numbers change between builds and security updates! The Win32 subsystem shields applications from changes in the underlying kernel.",
                situationObj: "<strong>Where we are:</strong> We are in the initial unprivileged state. Notepad wants to read 512 bytes, but Win32 applications never call kernel trap instructions directly.<br><br><strong>What we need to do next:</strong> We need <code>kernelbase.dll</code> to forward the request to <code>ntdll.dll</code> to identify the native system service number. Click <strong>Next Step</strong> to enter the subsystem."
              },
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x00007FFA300124A0 (ntdll.dll!NtReadFile)",
                stack: "User Stack (RSP = 0x00000080...)",
                stepNum: "Chapter 2 of 6: Staging the System Service Number (SSN)",
                activeNode: "node-trap-trigger",
                activeEdges: ["edge-1"],
                btnNextText: "Next: Trigger Hardware Trap &rarr;",
                btnPrevText: "&larr; Prev: Win32 Invocation",
                node1Title: "Notepad (PID 1024)",
                node1Sub: "Waiting on ReadFile()",
                node2Title: "ntdll.dll Native Stub",
                node2Sub: "EAX = 0x06 (NtReadFile) &rarr; syscall",
                node4Title: "KiSystemCall64 / SSDT",
                node4Sub: "KeServiceDescriptorTable",
                node5Title: "I/O Manager &amp; Drivers",
                node5Sub: "Allocates IRP &rarr; NTFS",
                what: "Execution is currently inside <code>ntdll.dll</code>, the lowest user-mode layer in Windows. The assembly stub has loaded the System Service Number for <code>NtReadFile</code> (e.g., <code>0x06</code>) into <code>EAX</code> and aligned arguments into registers. The CPU stands poised on the <code>syscall</code> instruction.",
                why: "Because <code>ntdll.dll</code> is updated alongside the kernel with each Windows update, it is the only user-mode binary that knows the correct System Service Numbers for the active kernel build. This design allows decades-old Windows binaries to continue working on modern versions of Windows without recompilation.",
                situationObj: "<strong>Where we are:</strong> <code>ntdll.dll</code> has staged the System Service Number into <code>EAX</code>, but we are still executing in unprivileged User Space.<br><br><strong>What we need to do next:</strong> We need to execute the <code>syscall</code> instruction so CPU hardware can elevate to Ring 0 and enter the Windows kernel. Click <strong>Next Step</strong> to trigger the hardware trap."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Supervisor Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFF80020400000 (ntoskrnl.exe!KiSystemCall64)",
                stack: "Kernel Stack (KTHREAD.InitialStack)",
                stepNum: "Chapter 3 of 6: Crossing the Threshold into ntoskrnl.exe",
                activeNode: "node-cpu-hw",
                activeEdges: ["edge-2"],
                btnNextText: "Next: Lookup in SSDT &rarr;",
                btnPrevText: "&larr; Prev: ntdll Syscall",
                node1Title: "Notepad (PID 1024)",
                node1Sub: "Suspended (State Saved)",
                node2Title: "ntdll.dll Native Stub",
                node2Sub: "Trapped into Hardware",
                node4Title: "KiSystemCall64",
                node4Sub: "Kernel Dispatcher",
                node5Title: "I/O Manager &amp; Drivers",
                node5Sub: "Allocates IRP &rarr; NTFS",
                what: "The CPU hardware has caught the trap. It has set Mode Bit = 0, loaded the privileged kernel stack pointer from the active thread's <code>KTHREAD</code> structure, and branched directly to the entry point stored in <code>MSR_LSTAR</code>: <code>KiSystemCall64</code> inside <code>ntoskrnl.exe</code>.",
                why: "Switching to an isolated kernel stack in silicon ensures that user-mode code cannot tamper with execution context while running in supervisor mode. The processor hardware enforces this boundary before executing any kernel instructions.",
                situationObj: "<strong>Where we are:</strong> The CPU has swapped to the privileged <code>KTHREAD</code> kernel stack and branched to <code>KiSystemCall64</code> in <code>ntoskrnl.exe</code>.<br><br><strong>What we need to do next:</strong> We need the dispatcher to use the index in <code>EAX</code> to look up <code>NtReadFile</code> in the System Service Descriptor Table (SSDT). Click <strong>Next Step</strong> to route the service."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Supervisor Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFF80020521080 (ntoskrnl.exe SSDT)",
                stack: "Kernel Stack (KTHREAD)",
                stepNum: "Chapter 4 of 6: The SSDT Dispatch &amp; Memory Validation",
                activeNode: "node-kernel-idt",
                activeEdges: ["edge-3"],
                btnNextText: "Next: Dispatch I/O Packet &rarr;",
                btnPrevText: "&larr; Prev: KiSystemCall64",
                node1Title: "Notepad (PID 1024)",
                node1Sub: "Suspended (State Saved)",
                node2Title: "ntdll.dll Native Stub",
                node2Sub: "Trapped into Hardware",
                node4Title: "SSDT Dispatcher",
                node4Sub: "ProbeForWrite() Check",
                node5Title: "I/O Manager &amp; Drivers",
                node5Sub: "Allocates IRP &rarr; NTFS",
                what: "<code>KiSystemCall64</code> has indexed into the System Service Descriptor Table (SSDT) using <code>EAX = 0x06</code> to locate <code>NtReadFile</code>. The kernel is currently running <code>ProbeForWrite()</code> across the destination buffer to confirm it belongs entirely to user space and has write permissions.",
                why: "The kernel must rigorously validate memory boundaries. If an unprivileged application could pass a pointer to kernel memory, it could trick supervisor routines into overwriting security descriptors or page tables, compromising system security.",
                situationObj: "<strong>Where we are:</strong> The kernel has matched the service number in the SSDT, but cannot touch storage until it verifies the caller's buffer.<br><br><strong>What we need to do next:</strong> We need the kernel to validate the pointer with <code>ProbeForWrite()</code> and construct an I/O Request Packet (IRP). Click <strong>Next Step</strong> to build and send the IRP."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Supervisor Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFF80020684100 (ntfs.sys &rarr; stornvme.sys)",
                stack: "Kernel Stack (KTHREAD)",
                stepNum: "Chapter 5 of 6: The IRP Travels the Driver Stack",
                activeNode: "node-kernel-driver",
                activeEdges: ["edge-4"],
                btnNextText: "Next: Return to User Mode &rarr;",
                btnPrevText: "&larr; Prev: SSDT Dispatch",
                node1Title: "Notepad (PID 1024)",
                node1Sub: "Waiting on IRP Completion",
                node2Title: "ntdll.dll Native Stub",
                node2Sub: "Waiting for Bytes",
                node4Title: "I/O Manager",
                node4Sub: "Dispatches IRP",
                node5Title: "ntfs.sys &amp; stornvme.sys",
                node5Sub: "Executes DMA Transfer",
                what: "The Windows I/O Manager has dispatched an <strong>IRP (I/O Request Packet)</strong> down the driver stack: <code>ntfs.sys</code> mapped clusters, and <code>stornvme.sys</code> programmed the NVMe hardware. DMA has streamed the 512 bytes directly into RAM, and the driver has completed the IRP with <code>STATUS_SUCCESS</code>.",
                why: "Windows relies on packet-driven I/O so requests can be processed asynchronously, queued, filtered by antivirus filter drivers, or redirected over networks without the caller needing to know the physical storage device type.",
                situationObj: "<strong>Where we are:</strong> The driver stack completed the IRP, and the disk data is resident in memory. We are finished running in supervisor mode.<br><br><strong>What we need to do next:</strong> We need the kernel to execute <code>sysret</code> to return to User Mode and let <code>kernel32.dll</code> translate <code>STATUS_SUCCESS</code> into a Win32 boolean. Click <strong>Next Step</strong> to return."
              },
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x00007FF710001208 (Notepad.exe)",
                stack: "Restored User Stack (RSP = 0x00000080...)",
                stepNum: "Chapter 6 of 6: Returning to User Space &amp; Subsystem Translation",
                activeNode: "node-user-app",
                activeEdges: ["edge-5"],
                btnNextText: "Replay the Journey &#8634;",
                btnPrevText: "&larr; Prev: IRP Processing",
                node1Title: "Notepad (PID 1024)",
                node1Sub: "ReadFile() returned TRUE!",
                node2Title: "kernel32 / ntdll",
                node2Sub: "Converts NTSTATUS &rarr; BOOL",
                node4Title: "KiSystemCall64",
                node4Sub: "sysret drops privilege",
                node5Title: "Driver Stack",
                node5Sub: "IRP Completed",
                what: "The journey is complete. The kernel executed <code>sysret</code>. The CPU restored Mode Bit = 1, reloaded Notepad's stack pointer, and returned to <code>ntdll.dll</code>. <code>kernel32.dll</code> translated <code>STATUS_SUCCESS</code> into Win32 <code>TRUE</code>, and Notepad now displays the 512 bytes.",
                why: "Privilege is safely dropped back to User Mode. The Win32 subsystem translates internal NT kernel status codes into standard Windows API return values, preserving consistency and stability for desktop applications.",
                situationObj: "<strong>Where we are:</strong> We have returned to User Space. Notepad has received its file data without ever gaining kernel privileges, and execution resumes safely in Ring 3.<br><br><strong>What we need to do next:</strong> The story has concluded. Click <strong>Replay</strong> to reset the walkthrough back to Chapter 1."
              }
            ]
          };

          let currentTrapPlatform = "unix";
          let trapIndex = 0;

          function renderTrapState() {
            const data = trapStorylines[currentTrapPlatform][trapIndex];
            document.getElementById("status-cpu-mode").textContent = data.mode;
            document.getElementById("status-cpu-mode").style.color = data.modeColor;
            document.getElementById("status-mode-bit").textContent = data.modeBit;
            document.getElementById("status-mode-bit").style.color = data.modeColor;
            document.getElementById("status-pc-reg").textContent = data.pc;
            document.getElementById("status-stack").textContent = data.stack;
            document.getElementById("status-step-num").innerHTML = data.stepNum;
            document.getElementById("desc-what").innerHTML = data.what;
            document.getElementById("desc-why").innerHTML = data.why;
            document.getElementById("inline-next-desc").innerHTML = data.situationObj;

            // Update SVG node labels dynamically
            document.getElementById("trap-node1-title").textContent = data.node1Title;
            document.getElementById("trap-node1-sub").textContent = data.node1Sub;
            document.getElementById("trap-node2-title").textContent = data.node2Title;
            document.getElementById("trap-node2-sub").textContent = data.node2Sub;
            document.getElementById("trap-node4-title").textContent = data.node4Title;
            document.getElementById("trap-node4-sub").textContent = data.node4Sub;
            document.getElementById("trap-node5-title").textContent = data.node5Title;
            document.getElementById("trap-node5-sub").textContent = data.node5Sub;

            const nextBtn = document.getElementById("step-next-btn");
            const prevBtn = document.getElementById("step-prev-btn");

            if (nextBtn) nextBtn.innerHTML = data.btnNextText;
            if (prevBtn) {
              prevBtn.innerHTML = data.btnPrevText;
              prevBtn.style.opacity = trapIndex === 0 ? "0.5" : "1.0";
              prevBtn.style.cursor = trapIndex === 0 ? "not-allowed" : "pointer";
            }

            const allNodes = ["node-user-app", "node-trap-trigger", "node-cpu-hw", "node-kernel-idt", "node-kernel-driver"];
            allNodes.forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                el.setAttribute("stroke", "#cbd5e1");
                el.setAttribute("stroke-width", "1.5");
                el.setAttribute("fill", "#ffffff");
              }
            });

            const allEdges = ["edge-1", "edge-2", "edge-3", "edge-4", "edge-5"];
            allEdges.forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                el.setAttribute("stroke", "#cbd5e1");
                el.setAttribute("stroke-width", "2");
              }
            });

            const activeNodeEl = document.getElementById(data.activeNode);
            if (activeNodeEl) {
              activeNodeEl.setAttribute("stroke", data.modeColor === "#0284c7" ? "#0284c7" : "#dc2626");
              activeNodeEl.setAttribute("stroke-width", "2.5");
              activeNodeEl.setAttribute("fill", data.modeColor === "#0284c7" ? "#f0f9ff" : "#fef2f2");
            }

            data.activeEdges.forEach(id => {
              const edgeEl = document.getElementById(id);
              if (edgeEl) {
                edgeEl.setAttribute("stroke", "#0284c7");
                edgeEl.setAttribute("stroke-width", "3");
              }
            });
          }

          function setTrapPlatform(platformKey) {
            currentTrapPlatform = platformKey;
            const btnUnix = document.getElementById("btn-trap-unix");
            const btnWin = document.getElementById("btn-trap-win");
            if (platformKey === "unix") {
              btnUnix.style.background = "#0284c7";
              btnUnix.style.color = "#ffffff";
              btnWin.style.background = "transparent";
              btnWin.style.color = "#475569";
            } else {
              btnWin.style.background = "#0284c7";
              btnWin.style.color = "#ffffff";
              btnUnix.style.background = "transparent";
              btnUnix.style.color = "#475569";
            }
            renderTrapState();
          }

          document.getElementById("btn-trap-unix").addEventListener("click", () => setTrapPlatform("unix"));
          document.getElementById("btn-trap-win").addEventListener("click", () => setTrapPlatform("windows"));

          document.getElementById("step-next-btn").addEventListener("click", function() {
            if (trapIndex < trapStorylines[currentTrapPlatform].length - 1) {
              trapIndex++;
            } else {
              trapIndex = 0;
            }
            renderTrapState();
          });

          document.getElementById("step-prev-btn").addEventListener("click", function() {
            if (trapIndex > 0) {
              trapIndex--;
              renderTrapState();
            }
          });

          document.getElementById("step-reset-btn").addEventListener("click", function() {
            trapIndex = 0;
            renderTrapState();
          });

          renderTrapState();
        })();
      </script>"""

BOTTOM_NAV_REPLACEMENT = """  <nav class="module-nav-bar bottom">
    <a href="01-what-is-an-os-and-history.html" class="module-nav-btn">&larr; Previous: 01. What Is an OS &amp; History</a>
    <a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: all 0.15s ease;">&#127968; Week 1: Operating System Concepts</a>
    <a href="03-os-concepts.html" class="module-nav-btn">Next: 03. OS Concepts &rarr;</a>
  </nav>"""

def update_hardware_review_page():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace the TRAP simulator component
    trap_pattern = r'<div id="interactive-trap-simulator".*?</script>'
    match = re.search(trap_pattern, content, flags=re.DOTALL)
    if match:
        start, end = match.span()
        content = content[:start] + TRAP_SIM_REPLACEMENT.strip() + content[end:]
        print("--> Injected updated situation-and-objective narrative in TRAP simulator.")
    else:
        print("--> Warning: interactive-trap-simulator block not found.")

    # 2. Update the bottom navigation bar to use the styled home icon pill button
    bottom_nav_pattern = r'<nav class="module-nav-bar bottom">.*?</nav>'
    match_nav = re.search(bottom_nav_pattern, content, flags=re.DOTALL)
    if match_nav:
        start_nav, end_nav = match_nav.span()
        content = content[:start_nav] + BOTTOM_NAV_REPLACEMENT.strip() + content[end_nav:]
        print("--> Updated bottom navigation bar with home pill.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Align Syscall Story preview panel with situation-and-objective arc\n\n"
            "Update 02-hardware-review.html so the story panel frames the current\n"
            "state and the next objective before advancing to the next chapter."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for 02-hardware-review.html!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_hardware_review_page()
