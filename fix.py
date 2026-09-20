#!/usr/bin/env python3
# =====================================================================
# fix.py: Transform Dual-Mode TRAP simulator into an active narrative
# =====================================================================
import os
import re
import subprocess

NARRATIVE_TRAP_HTML = """
      <div id="interactive-trap-simulator" style="margin: 32px 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
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
            <li><strong>Follow the Narrative Arc:</strong> Read each step as a chapter in the lifecycle of a disk read operation (<code>report.txt</code>).</li>
            <li><strong>Watch the Hardware Board:</strong> Notice when the CPU mode bit flips between unprivileged user code and privileged kernel supervision.</li>
            <li><strong>Compare Operating Systems:</strong> Toggle between <code>Linux / Unix</code> and <code>Windows NT</code> at any time to see how both OS designs navigate the same underlying hardware constraints.</li>
          </ol>
        </div>

        <!-- Action Controls & Inline Next Step Narrative Teaser -->
        <div style="display: grid; grid-template-columns: auto 1fr; gap: 16px; align-items: stretch; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px; margin-bottom: 20px;">
          <div style="display: flex; flex-direction: column; gap: 8px; justify-content: center; min-width: 170px;">
            <button id="step-next-btn" style="padding: 10px 16px; font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; border-radius: 6px; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; cursor: pointer; text-align: center; transition: all 0.15s ease;">Next Step &rarr;</button>
            <div style="display: flex; gap: 8px;">
              <button id="step-prev-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 600; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">&larr; Prev</button>
              <button id="step-reset-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #64748b; cursor: pointer;">Reset</button>
            </div>
          </div>

          <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-left: 4px solid #0284c7; border-radius: 0 6px 6px 0; padding: 10px 14px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: #0369a1; text-transform: uppercase; letter-spacing: 0.03em;">Next in the Story:</div>
            <div id="inline-next-desc" style="font-size: 0.88rem; color: #0c4a6e; line-height: 1.45; margin-top: 4px;">
              The program hits the hardware wall: it cannot talk to the disk drive directly, so it stages arguments into CPU registers to request OS assistance.
            </div>
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
            <div id="story-heading-what" style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #0284c7; text-transform: uppercase; letter-spacing: 0.03em;">The Current Story: What Is Happening</div>
            <div id="desc-what" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>

          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #10b981; padding: 16px; border-radius: 0 6px 6px 0;">
            <div id="story-heading-why" style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 0.03em;">Behind the Curtain: Why The Machine Behaves This Way</div>
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
                btnNextText: "Next: Invoke Runtime Wrapper &rarr;",
                btnPrevText: "&larr; Prev",
                node1Title: "Text Editor (PID 402)",
                node1Sub: "read(fd, buffer, 512)",
                node2Title: "C Library (glibc)",
                node2Sub: "Prepares Syscall",
                node4Title: "Syscall Table",
                node4Sub: "sys_call_table[__NR_read]",
                node5Title: "VFS &amp; NVMe Driver",
                node5Sub: "Reads Blocks from Disk",
                what: "Our story begins inside a user text editor running peacefully in User Space. The user hits 'Open File', and the application wants 512 bytes from <code>report.txt</code>. It calls the standard C function <code>read(fd, buffer, 512)</code>. Right now, the CPU is running in User Mode (Mode Bit = 1). The application cannot send electricity to the physical SSD pins or command the storage controller directly; doing so would immediately trigger a fatal General Protection Fault.",
                why: "Imagine if any running program could send raw signals across the PCIe bus: a buggy text editor could wipe your entire operating system or spy on another user's banking session. The hardware enforces a sandbox (Ring 3) where applications can compute, but cannot touch real physical reality without permission.",
                nextStep: "The text editor surrenders execution to the C standard library wrapper, which will stage the formal request into CPU registers."
              },
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x004085A0 (glibc syscall stub)",
                stack: "User Stack (RSP = 0x7FFF4FE0)",
                stepNum: "Chapter 2 of 6: Preparing the Magic Incantation (The TRAP)",
                activeNode: "node-trap-trigger",
                activeEdges: ["edge-1"],
                btnNextText: "Next: Hardware Mode Switch &rarr;",
                btnPrevText: "&larr; Prev: Application Call",
                node1Title: "Text Editor (PID 402)",
                node1Sub: "Waiting on I/O",
                node2Title: "glibc Syscall Stub",
                node2Sub: "RAX=0 (sys_read) &rarr; SYSCALL",
                node4Title: "Syscall Table",
                node4Sub: "sys_call_table[0]",
                node5Title: "VFS &amp; NVMe Driver",
                node5Sub: "Reads Blocks from Disk",
                what: "Execution steps into the C runtime library (glibc). The library sets up the rendezvous. It writes <code>0</code> into the <code>RAX</code> register—the universal Linux catalog number for <code>sys_read</code>. It places the file descriptor into <code>RDI</code>, the buffer address into <code>RSI</code>, and the byte count (512) into <code>RDX</code>. With all arguments staged, it executes the special machine instruction: <code>SYSCALL</code>.",
                why: "An unprivileged program cannot just flip its own mode bit from 1 to 0; the CPU hardware rejects any software attempt to elevate its own rank. The <code>SYSCALL</code> instruction is a controlled hardware gateway—a specialized architectural emergency brake designed into the silicon.",
                nextStep: "The CPU silicon intercepts the SYSCALL instruction, drops privileges to Ring 0, swaps stacks, and jumps into supervisor space."
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
                what: "At this exact microsecond, the CPU hardware takes total control. The CPU microcode instantly forces the Mode Bit in the processor flags from <code>1</code> to <code>0</code>. It saves the application's Program Counter and user Stack Pointer onto the process's private kernel stack. Then, the processor forces the Program Counter to jump directly to the kernel's hardened entry point registered in the CPU's Model-Specific Register (<code>MSR_LSTAR</code>).",
                why: "Why does the CPU automatically switch stacks to a secret kernel memory area? Because if the kernel used the user's stack, a malicious thread in another CPU core could rewrite return addresses while the kernel was running in Ring 0, hijacking the entire machine!",
                nextStep: "The kernel entry routine inspects the catalog number in RAX and vectors to the Virtual File System handler."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Supervisor Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFFFFF81B23040 (sys_call_table)",
                stack: "Kernel Stack (0xFFFFC900...)",
                stepNum: "Chapter 4 of 6: The Royal Guard Inspects the Credentials",
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
                what: "The kernel's syscall dispatcher looks at the <code>RAX</code> register. Seeing <code>0</code>, it knows the user wants <code>sys_read</code>. But before touching any files, the kernel acts with deep suspicion: it checks the destination buffer address in <code>RSI</code>. It verifies that this memory really belongs to the user application, and is not a clever trick pointing to secret kernel memory.",
                why: "This prevents the notorious 'confused deputy' attack. If the kernel blindly filled any memory address the user supplied, an unprivileged user could pass the memory address of the OS password table and trick the kernel into overwriting it with file data!",
                nextStep: "With pointers verified, the kernel invokes the physical storage driver to talk directly to the NVMe controller."
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
                what: "The kernel Virtual File System (VFS) resolves the file path to physical drive blocks. The NVMe device driver issues raw commands across the PCIe bus to the controller chip. The NVMe drive fires up Direct Memory Access (DMA) and writes the 512 bytes directly from flash storage into the application's buffer. The driver receives a completion interrupt and signals that the data is safely in memory.",
                why: "Only here, deep inside Ring 0, are the processor's I/O instructions unlocked. Because the operating system wrote the driver, it guarantees that only authorized sectors belonging to <code>report.txt</code> are read, leaving all other files untouched.",
                nextStep: "The kernel finishes the operation, puts the byte count into RAX, and prepares to drop privileges back to the application."
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
                what: "The kernel writes <code>512</code> into <code>RAX</code> (telling the user that 512 bytes were successfully read). It executes the <code>SYSRET</code> instruction. In a single clock cycle, the CPU restores the Mode Bit back to <code>1</code> (User Mode), restores the original user stack pointer, and jumps execution back to the text editor. The application wakes up, reads the buffer, and renders your document on screen.",
                why: "The circle is complete. The system returns to steady-state unprivileged execution. The application got its data, but at no moment was it ever allowed to break out of its sandbox or usurp processor authority.",
                nextStep: "The journey is complete. Click Replay to step through the story again from the beginning."
              }
            ],
            windows: [
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x00007FF710001200 (Notepad / Word)",
                stack: "User Stack (RSP = 0x00000080...)",
                stepNum: "Chapter 1 of 6: The Win32 Application Asks for Help",
                activeNode: "node-user-app",
                activeEdges: [],
                btnNextText: "Next: Enter Windows Subsystem DLLs &rarr;",
                btnPrevText: "&larr; Prev",
                node1Title: "Win32 App (Notepad)",
                node1Sub: "ReadFile(hFile, buf, 512)",
                node2Title: "kernel32 &rarr; ntdll",
                node2Sub: "Stages SSN in EAX",
                node4Title: "KiSystemCall64 / SSDT",
                node4Sub: "KeServiceDescriptorTable",
                node5Title: "I/O Manager &amp; Drivers",
                node5Sub: "Allocates IRP &rarr; NTFS",
                what: "Our Windows story begins inside Notepad running in User Space. The user opens <code>report.txt</code>. The application does not call the kernel directly; instead, it calls the friendly Win32 API function: <code>ReadFile()</code> exported by <code>kernel32.dll</code>. Notepad is running strictly in Ring 3 (Mode Bit = 1). If Notepad tried to talk directly to the storage disk or manipulate page tables, the CPU would throw an immediate hardware exception.",
                why: "Microsoft intentionally decouples software from raw system calls. Unlike Unix where syscall numbers are stable, Windows syscall numbers change with almost every Windows build and security patch! Win32 subsystem DLLs buffer applications from the shifting kernel underneath.",
                nextStep: "kernel32.dll hands the request down to ntdll.dll, the keeper of the raw Windows system service numbers."
              },
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x00007FFA300124A0 (ntdll.dll!NtReadFile)",
                stack: "User Stack (RSP = 0x00000080...)",
                stepNum: "Chapter 2 of 6: ntdll.dll and the Secret System Service Number",
                activeNode: "node-trap-trigger",
                activeEdges: ["edge-1"],
                btnNextText: "Next: Hardware Mode Switch &rarr;",
                btnPrevText: "&larr; Prev: Win32 Invocation",
                node1Title: "Win32 App (Notepad)",
                node1Sub: "Waiting on ReadFile()",
                node2Title: "ntdll.dll Stub",
                node2Sub: "EAX = 0x06 (NtReadFile) &rarr; syscall",
                node4Title: "KiSystemCall64 / SSDT",
                node4Sub: "KeServiceDescriptorTable",
                node5Title: "I/O Manager &amp; Drivers",
                node5Sub: "Allocates IRP &rarr; NTFS",
                what: "Inside <code>ntdll.dll</code>, the lowest user-mode library in Windows, sits the native stub for <code>NtReadFile</code>. This tiny stub moves the secret System Service Number (SSN, e.g. <code>0x06</code>) into the <code>EAX</code> register, stages the 64-bit parameters, and executes the CPU instruction: <code>syscall</code>.",
                why: "<code>ntdll.dll</code> is the only code in Windows that knows the true syscall numbers for the current OS version. By locking this knowledge inside <code>ntdll.dll</code>, Windows ensures your 15-year-old application runs without recompilation on Windows 11.",
                nextStep: "The CPU catches the syscall instruction, switches to Ring 0, swaps stacks, and jumps to KiSystemCall64 in ntoskrnl.exe."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Supervisor Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFF80020400000 (ntoskrnl.exe!KiSystemCall64)",
                stack: "Kernel Stack (KTHREAD.InitialStack)",
                stepNum: "Chapter 3 of 6: Crossing into ntoskrnl.exe (The Hardware Switch)",
                activeNode: "node-cpu-hw",
                activeEdges: ["edge-2"],
                btnNextText: "Next: Lookup in SSDT &rarr;",
                btnPrevText: "&larr; Prev: ntdll Syscall",
                node1Title: "Win32 App (Notepad)",
                node1Sub: "Suspended (State Saved)",
                node2Title: "ntdll.dll Stub",
                node2Sub: "Trapped into Hardware",
                node4Title: "KiSystemCall64",
                node4Sub: "Kernel Dispatcher",
                node5Title: "I/O Manager &amp; Drivers",
                node5Sub: "Allocates IRP &rarr; NTFS",
                what: "The CPU microcode catches the trap. It flips the hardware Mode Bit to <code>0</code> (Kernel Mode). The processor loads the privileged stack pointer stored in the thread's <code>KTHREAD</code> structure and branches directly to the entry point stored in the CPU's <code>MSR_LSTAR</code> register: <code>KiSystemCall64</code> inside the main Windows executive kernel (<code>ntoskrnl.exe</code>).",
                why: "Windows must execute this stack swap in hardware before touching a single line of C code. Running kernel code on an unverified user stack would allow user-space malware to hijack kernel control flow.",
                nextStep: "KiSystemCall64 extracts the SSN index from EAX and routes to the System Service Descriptor Table (SSDT)."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Supervisor Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFF80020521080 (ntoskrnl.exe SSDT)",
                stack: "Kernel Stack (KTHREAD)",
                stepNum: "Chapter 4 of 6: The SSDT Dispatch &amp; Parameter Probing",
                activeNode: "node-kernel-idt",
                activeEdges: ["edge-3"],
                btnNextText: "Next: Dispatch I/O Packet &rarr;",
                btnPrevText: "&larr; Prev: KiSystemCall64",
                node1Title: "Win32 App (Notepad)",
                node1Sub: "Suspended (State Saved)",
                node2Title: "ntdll.dll Stub",
                node2Sub: "Trapped into Hardware",
                node4Title: "SSDT Dispatcher",
                node4Sub: "ProbeForWrite() Check",
                node5Title: "I/O Manager &amp; Drivers",
                node5Sub: "Allocates IRP &rarr; NTFS",
                what: "<code>KiSystemCall64</code> indexes into the System Service Descriptor Table (SSDT) using the number in <code>EAX</code> to find <code>NtReadFile</code>. The kernel immediately calls <code>ProbeForWrite()</code> on the destination buffer. It ensures that the memory buffer truly belongs to user space and that memory protection flags permit writing.",
                why: "The kernel must rigorously protect itself against buffer overflow attacks and malicious kernel memory probes. If the destination pointer overlaps supervisor space, the call is terminated immediately with <code>STATUS_ACCESS_VIOLATION</code>.",
                nextStep: "The Windows I/O Manager wraps the read request into an I/O Request Packet (IRP) and sends it down the driver stack."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Supervisor Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFF80020684100 (ntfs.sys &rarr; stornvme.sys)",
                stack: "Kernel Stack (KTHREAD)",
                stepNum: "Chapter 5 of 6: The IRP Journey Down the Driver Stack",
                activeNode: "node-kernel-driver",
                activeEdges: ["edge-4"],
                btnNextText: "Next: Return to User Mode &rarr;",
                btnPrevText: "&larr; Prev: SSDT Dispatch",
                node1Title: "Win32 App (Notepad)",
                node1Sub: "Waiting on IRP Completion",
                node2Title: "ntdll.dll Stub",
                node2Sub: "Waiting for Bytes",
                node4Title: "I/O Manager",
                node4Sub: "Dispatches IRP",
                node5Title: "ntfs.sys &amp; stornvme.sys",
                node5Sub: "Executes DMA Transfer",
                what: "Here is the architectural genius of Windows: the I/O Manager creates a self-contained packet called an <strong>IRP (I/O Request Packet)</strong>. It passes this packet down a layered stack: from <code>ntfs.sys</code> (which looks up file clusters), down to <code>classpnp.sys</code>, down to <code>stornvme.sys</code>. The storage driver programs the NVMe controller registers, DMA transfers 512 bytes into RAM, and completes the IRP with <code>STATUS_SUCCESS</code>.",
                why: "Windows uses packet-driven I/O so that operations can be asynchronous, stacked, filtered (e.g. by antivirus drivers), and redirected without the filesystem knowing what kind of physical storage controller is connected.",
                nextStep: "The kernel finishes execution, puts the status code into EAX, and executes sysret to return to user mode."
              },
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x00007FF710001208 (Notepad Resumes)",
                stack: "Restored User Stack (RSP = 0x00000080...)",
                stepNum: "Chapter 6 of 6: Returning to User Space &amp; Subsystem Translation",
                activeNode: "node-user-app",
                activeEdges: ["edge-5"],
                btnNextText: "Replay the Journey &#8634;",
                btnPrevText: "&larr; Prev: IRP Processing",
                node1Title: "Win32 App (Notepad)",
                node1Sub: "ReadFile() returned TRUE!",
                node2Title: "kernel32 / ntdll",
                node2Sub: "Converts NTSTATUS &rarr; BOOL",
                node4Title: "KiSystemCall64",
                node4Sub: "sysret drops privilege",
                node5Title: "Driver Stack",
                node5Sub: "IRP Completed",
                what: "The kernel executes <code>sysret</code>. The CPU switches the Mode Bit back to <code>1</code> (User Mode), restores Notepad's stack pointer, and resumes execution in <code>ntdll.dll</code>. <code>ntdll.dll</code> passes the result back to <code>kernel32.dll</code>, which translates the raw <code>STATUS_SUCCESS</code> code into a standard Win32 <code>TRUE</code> boolean. Notepad receives its 512 bytes and displays your text.",
                why: "The boundary has been crossed and safely restored. Applications enjoy seamless file access while the hardware and kernel maintain absolute, unbroken protection over physical hardware.",
                nextStep: "The journey is complete. Click Replay to step through the story again from the beginning."
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
            document.getElementById("inline-next-desc").innerHTML = data.nextStep;

            // Update SVG node text
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
      </script>
"""

def update_trap_simulator_narrative():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'<div id="interactive-trap-simulator".*?</script>'
    match = re.search(pattern, content, flags=re.DOTALL)
    if match:
        start, end = match.span()
        content = content[:start] + NARRATIVE_TRAP_HTML.strip() + content[end:]
        print("--> Injected narrative storytelling into TRAP simulator.")
    else:
        print("--> Interactive TRAP simulator container not found.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Transform dual-mode TRAP walkthrough into an active narrative trace\n\n"
            "Revise week01-operating-system-concepts/02-hardware-review.html so each\n"
            "step chronicles the story of an unprivileged file read across silicon."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_trap_simulator_narrative()
