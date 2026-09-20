#!/usr/bin/env python3
# =====================================================================
# fix.py: Add Windows NT vs Unix toggle to the Dual-Mode TRAP simulator
# =====================================================================
import os
import re
import subprocess

TRAP_SIMULATOR_HTML = """
      <div id="interactive-trap-simulator" style="margin: 32px 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 18px;">
          <div>
            <h3 style="margin: 0; color: #0284c7; font-size: 1.15rem;">Guided Walkthrough: Dual-Mode TRAP &amp; Syscall Lifecycle</h3>
            <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Compare how Unix and Windows NT bridge the user-to-kernel boundary during hardware traps.</p>
          </div>

          <!-- OS Selector Toggle Group -->
          <div style="display: flex; align-items: center; gap: 6px; background: #f1f5f9; padding: 4px; border-radius: 8px; border: 1px solid #cbd5e1;">
            <span style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #475569; padding: 0 6px;">Platform:</span>
            <button id="btn-trap-unix" class="trap-os-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: #0284c7; color: #ffffff; cursor: pointer; transition: all 0.15s ease;">Linux / Unix</button>
            <button id="btn-trap-win" class="trap-os-btn" style="padding: 5px 12px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; border-radius: 5px; border: none; background: transparent; color: #475569; cursor: pointer; transition: all 0.15s ease;">Windows NT</button>
          </div>
        </div>

        <!-- Instructions Guide -->
        <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px; margin-bottom: 16px;">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">How to Use This Simulator</div>
          <ol style="margin-left: 20px; margin-bottom: 0; color: #334155; font-size: 0.88rem; line-height: 1.5;">
            <li><strong>Switch Architectures:</strong> Use the <code>Linux / Unix</code> and <code>Windows NT</code> buttons above at any time to compare how each OS structures system call dispatching.</li>
            <li><strong>Step Through the Lifecycle:</strong> Click <code>Next Step &rarr;</code> to follow the control path across privilege boundaries.</li>
            <li><strong>Notice the Subsystem Abstraction:</strong> Pay special attention to how Windows interposes <code>kernel32.dll</code> and <code>ntdll.dll</code> before reaching the hardware trap.</li>
          </ol>
        </div>

        <!-- Action Controls & Inline Next Step Explanation -->
        <div style="display: grid; grid-template-columns: auto 1fr; gap: 16px; align-items: stretch; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px; margin-bottom: 20px;">
          <div style="display: flex; flex-direction: column; gap: 8px; justify-content: center; min-width: 170px;">
            <button id="step-next-btn" style="padding: 10px 16px; font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; border-radius: 6px; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; cursor: pointer; text-align: center; transition: all 0.15s ease;">Next Step &rarr;</button>
            <div style="display: flex; gap: 8px;">
              <button id="step-prev-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 600; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">&larr; Prev</button>
              <button id="step-reset-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #64748b; cursor: pointer;">Reset</button>
            </div>
          </div>

          <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-left: 4px solid #0284c7; border-radius: 0 6px 6px 0; padding: 10px 14px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: #0369a1; text-transform: uppercase; letter-spacing: 0.03em;">Upcoming Action When You Click Next:</div>
            <div id="inline-next-desc" style="font-size: 0.88rem; color: #0c4a6e; line-height: 1.45; margin-top: 4px;">
              The runtime wrapper stages system call arguments into CPU registers and issues the hardware TRAP instruction.
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
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Mode Bit</div>
            <div id="status-mode-bit" style="font-weight: 700; color: #dc2626; margin-top: 2px;">1 (Unprivileged)</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Program Counter</div>
            <div id="status-pc-reg" style="font-weight: 700; color: #0284c7; margin-top: 2px;">0x00401140 (App)</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Stack In Use</div>
            <div id="status-stack" style="font-weight: 700; color: #0284c7; margin-top: 2px;">User Stack (RSP)</div>
          </div>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
            <div style="color: #64748b; font-size: 0.72rem; text-transform: uppercase;">Current Step</div>
            <div id="status-step-num" style="font-weight: 700; color: #0f172a; margin-top: 2px;">Step 1 of 6</div>
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
            <text x="35" y="42" fill="#64748b" font-size="11" font-weight="700">USER ADDRESS SPACE (Ring 3)</text>

            <!-- Kernel Space Band -->
            <rect x="20" y="155" width="820" height="105" rx="6" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.5" />
            <text x="35" y="177" fill="#0369a1" font-size="11" font-weight="700">KERNEL ADDRESS SPACE (Ring 0)</text>

            <!-- Node 1: User App -->
            <rect id="node-user-app" x="45" y="55" width="180" height="52" rx="5" fill="#ffffff" stroke="#0284c7" stroke-width="2" />
            <text id="trap-node1-title" x="135" y="78" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">User Process</text>
            <text id="trap-node1-sub" x="135" y="94" fill="#64748b" font-size="10" text-anchor="middle">read(fd, buf, len)</text>

            <!-- Node 2: Library Stub / Trap Invocation -->
            <rect id="node-trap-trigger" x="280" y="55" width="190" height="52" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
            <text id="trap-node2-title" x="375" y="78" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">C Runtime Stub</text>
            <text id="trap-node2-sub" x="375" y="94" fill="#64748b" font-size="10" text-anchor="middle">SYSCALL / INT 0x80</text>

            <!-- Node 3: CPU Hardware Switch -->
            <rect id="node-cpu-hw" x="535" y="105" width="195" height="60" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="632" y="130" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">CPU Hardware Engine</text>
            <text x="632" y="148" fill="#64748b" font-size="10" text-anchor="middle">Mode: 1 &rarr; 0 | Save SP/PC</text>

            <!-- Node 4: Kernel Dispatcher -->
            <rect id="node-kernel-idt" x="280" y="185" width="190" height="52" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
            <text id="trap-node4-title" x="375" y="208" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">IDT / Syscall Entry</text>
            <text id="trap-node4-sub" x="375" y="224" fill="#64748b" font-size="10" text-anchor="middle">sys_call_table[]</text>

            <!-- Node 5: Kernel Service / Device -->
            <rect id="node-kernel-driver" x="45" y="185" width="180" height="52" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
            <text id="trap-node5-title" x="135" y="208" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">VFS &amp; Disk Driver</text>
            <text id="trap-node5-sub" x="135" y="224" fill="#64748b" font-size="10" text-anchor="middle">Execute Privileged I/O</text>

            <!-- Connecting Flows -->
            <line id="edge-1" x1="225" y1="81" x2="275" y2="81" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />
            <path id="edge-2" d="M 470,81 L 530,125" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />
            <path id="edge-3" d="M 535,145 L 475,200" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />
            <line id="edge-4" x1="280" y1="211" x2="230" y2="211" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />
            <path id="edge-5" d="M 135,185 C 135,145 135,120 135,113" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#marker-blue)" />
          </svg>
        </div>

        <!-- Two-Pane Pedagogical Dashboard -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 20px;">
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0284c7; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #0284c7; text-transform: uppercase; letter-spacing: 0.03em;">Current State: What Is Happening</div>
            <div id="desc-what" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>

          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #10b981; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 0.03em;">Why The System Does This</div>
            <div id="desc-why" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>
        </div>
      </div>

      <script>
        (function() {
          const trapPlatforms = {
            unix: [
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x00401140 (App Code)",
                stack: "User Stack (RSP)",
                stepNum: "Step 1 of 6: Application Invocation",
                activeNode: "node-user-app",
                activeEdges: [],
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                node1Title: "User Process",
                node1Sub: "read(fd, buffer, 512)",
                node2Title: "C Runtime Stub",
                node2Sub: "SYSCALL (RAX = 0)",
                node4Title: "IDT / Syscall Entry",
                node4Sub: "sys_call_table[0]",
                node5Title: "VFS &amp; Disk Driver",
                node5Sub: "sys_read() &rarr; NVMe",
                what: "The user program calls <code>read(fd, buffer, 512)</code> in standard C library space.",
                why: "User processes cannot manipulate storage hardware directly. The CPU mode bit (Ring 3) ensures rogue programs cannot read or write arbitrary disk sectors.",
                nextStep: "The C library wrapper places the syscall number (RAX = 0) into registers and executes <code>SYSCALL</code> / <code>TRAP</code>."
              },
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x004085A0 (glibc stub)",
                stack: "User Stack (RSP)",
                stepNum: "Step 2 of 6: Staging Arguments &amp; Hardware TRAP",
                activeNode: "node-trap-trigger",
                activeEdges: ["edge-1"],
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                node1Title: "User Process",
                node1Sub: "read(fd, buffer, 512)",
                node2Title: "C Runtime Stub",
                node2Sub: "SYSCALL (RAX = 0)",
                node4Title: "IDT / Syscall Entry",
                node4Sub: "sys_call_table[0]",
                node5Title: "VFS &amp; Disk Driver",
                node5Sub: "sys_read() &rarr; NVMe",
                what: "The library stub loads the system call number (e.g. RAX = 0 for <code>sys_read</code>) and parameter registers (RDI, RSI, RDX), then issues the <code>SYSCALL</code> instruction.",
                why: "User code cannot change its own privilege bit. It must execute a designated hardware instruction that vectors control through a CPU-managed gate.",
                nextStep: "The CPU microcode catches the TRAP, clears the Mode Bit to 0 (Kernel Mode), switches to the kernel stack, and jumps to the entry point."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Privileged Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFFFFF81A00000 (Hardware Gate)",
                stack: "Kernel Stack (SS:RSP)",
                stepNum: "Step 3 of 6: Hardware Mode Switch &amp; Context Save",
                activeNode: "node-cpu-hw",
                activeEdges: ["edge-2"],
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                node1Title: "User Process",
                node1Sub: "read(fd, buffer, 512)",
                node2Title: "C Runtime Stub",
                node2Sub: "SYSCALL (RAX = 0)",
                node4Title: "IDT / Syscall Entry",
                node4Sub: "sys_call_table[0]",
                node5Title: "VFS &amp; Disk Driver",
                node5Sub: "sys_read() &rarr; NVMe",
                what: "The CPU microcode flips the Mode Bit to 0, saves user RIP and RSP onto the per-thread kernel stack, and transfers execution to the kernel syscall handler.",
                why: "Saving the execution state on a secure kernel stack prevents user code from forging return addresses or hijacking supervisor execution.",
                nextStep: "The kernel dispatcher indexes into <code>sys_call_table</code> to locate the implementation of <code>sys_read</code>."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Privileged Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFFFFF81B23040 (Syscall Table)",
                stack: "Kernel Stack (SS:RSP)",
                stepNum: "Step 4 of 6: Syscall Table Dispatching",
                activeNode: "node-kernel-idt",
                activeEdges: ["edge-3"],
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                node1Title: "User Process",
                node1Sub: "read(fd, buffer, 512)",
                node2Title: "C Runtime Stub",
                node2Sub: "SYSCALL (RAX = 0)",
                node4Title: "IDT / Syscall Entry",
                node4Sub: "sys_call_table[0]",
                node5Title: "VFS &amp; Disk Driver",
                node5Sub: "sys_read() &rarr; NVMe",
                what: "The kernel validates the destination buffer pointer to ensure it lies within user space, then routes the request through the Virtual File System (VFS) to the storage driver.",
                why: "Pointer validation prevents 'confused deputy' exploits where a user process tricks the kernel into overwriting protected supervisor structures.",
                nextStep: "The storage device driver programs the device controller and initiates physical disk I/O."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Privileged Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFFFFF81C84100 (Disk Driver)",
                stack: "Kernel Stack (SS:RSP)",
                stepNum: "Step 5 of 6: Privileged Device Execution",
                activeNode: "node-kernel-driver",
                activeEdges: ["edge-4"],
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                node1Title: "User Process",
                node1Sub: "read(fd, buffer, 512)",
                node2Title: "C Runtime Stub",
                node2Sub: "SYSCALL (RAX = 0)",
                node4Title: "IDT / Syscall Entry",
                node4Sub: "sys_call_table[0]",
                node5Title: "VFS &amp; Disk Driver",
                node5Sub: "sys_read() &rarr; NVMe",
                what: "The disk driver programs NVMe controller registers or schedules a DMA transfer to move the requested 512 bytes into memory.",
                why: "Only Ring 0 code has the architectural privilege to execute I/O instructions or access memory-mapped hardware controller registers.",
                nextStep: "The kernel places the read byte count into RAX and executes <code>SYSRET</code> to return to user space."
              },
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x00401148 (Resumed App Code)",
                stack: "Restored User Stack (RSP)",
                stepNum: "Step 6 of 6: Return to User Space (SYSRET / IRET)",
                activeNode: "node-user-app",
                activeEdges: ["edge-5"],
                btnNextText: "Restart Walkthrough &#8634;",
                btnPrevText: "&larr; Prev",
                node1Title: "User Process",
                node1Sub: "read() Returned 512",
                node2Title: "C Runtime Stub",
                node2Sub: "SYSCALL (RAX = 0)",
                node4Title: "IDT / Syscall Entry",
                node4Sub: "sys_call_table[0]",
                node5Title: "VFS &amp; Disk Driver",
                node5Sub: "sys_read() &rarr; NVMe",
                what: "The kernel executes <code>SYSRET</code>. The CPU restores the Mode Bit to 1, reloads the user stack pointer, and returns execution to the application.",
                why: "Dropping privileges back to Ring 3 guarantees normal application code cannot maintain supervisor authority after its requested I/O is complete.",
                nextStep: "Lifecycle complete. Click Restart to replay the sequence from Step 1."
              }
            ],
            windows: [
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x00007FF710001200 (App Code)",
                stack: "User Stack (RSP)",
                stepNum: "Step 1 of 6: Win32 API Call (kernel32 / kernelbase)",
                activeNode: "node-user-app",
                activeEdges: [],
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                node1Title: "Win32 Application",
                node1Sub: "ReadFile(hFile, buf, 512)",
                node2Title: "ntdll.dll (Native Stub)",
                node2Sub: "NtReadFile (SSN in EAX)",
                node4Title: "SSDT / KiSystemCall64",
                node4Sub: "KeServiceDescriptorTable",
                node5Title: "I/O Manager &amp; Drivers",
                node5Sub: "IRP &rarr; ntfs.sys &rarr; NVMe",
                what: "The application calls the Win32 API <code>ReadFile()</code> in <code>kernel32.dll</code> / <code>kernelbase.dll</code>.",
                why: "Unlike Unix, Windows user applications almost never invoke system calls directly. Windows insulates applications behind Win32 subsystem DLLs to preserve backward compatibility.",
                nextStep: "<code>kernelbase.dll</code> forwards the call to the native system stub <code>NtReadFile</code> in <code>ntdll.dll</code>."
              },
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x00007FFA300124A0 (ntdll.dll)",
                stack: "User Stack (RSP)",
                stepNum: "Step 2 of 6: Native Stub &amp; System Service Number (SSN)",
                activeNode: "node-trap-trigger",
                activeEdges: ["edge-1"],
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                node1Title: "Win32 Application",
                node1Sub: "ReadFile(hFile, buf, 512)",
                node2Title: "ntdll.dll (Native Stub)",
                node2Sub: "NtReadFile (SSN in EAX)",
                node4Title: "SSDT / KiSystemCall64",
                node4Sub: "KeServiceDescriptorTable",
                node5Title: "I/O Manager &amp; Drivers",
                node5Sub: "IRP &rarr; ntfs.sys &rarr; NVMe",
                what: "<code>ntdll.dll</code> loads the System Service Number (SSN) for <code>NtReadFile</code> into <code>EAX</code>, stages arguments into registers, and executes the <code>syscall</code> instruction.",
                why: "Windows System Service Numbers change between Windows versions and builds. <code>ntdll.dll</code> isolates user binaries from shifting kernel call indexes.",
                nextStep: "The CPU executes <code>syscall</code>, vectors to the address stored in MSR_LSTAR (<code>KiSystemCall64</code>), and enters Ring 0."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Privileged Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFF80020400000 (KiSystemCall64)",
                stack: "Kernel Stack (KTHREAD.InitialStack)",
                stepNum: "Step 3 of 6: CPU Mode Transition to KiSystemCall64",
                activeNode: "node-cpu-hw",
                activeEdges: ["edge-2"],
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                node1Title: "Win32 Application",
                node1Sub: "ReadFile(hFile, buf, 512)",
                node2Title: "ntdll.dll (Native Stub)",
                node2Sub: "NtReadFile (SSN in EAX)",
                node4Title: "SSDT / KiSystemCall64",
                node4Sub: "KeServiceDescriptorTable",
                node5Title: "I/O Manager &amp; Drivers",
                node5Sub: "IRP &rarr; ntfs.sys &rarr; NVMe",
                what: "The CPU microcode sets the Mode Bit to 0, switches to the kernel stack pointed to by the active <code>KTHREAD</code>, and vectors to <code>KiSystemCall64</code> in <code>ntoskrnl.exe</code>.",
                why: "Hardware-enforced stack swapping guarantees that unprivileged user threads cannot corrupt internal kernel execution state.",
                nextStep: "<code>KiSystemCall64</code> uses the SSN in EAX to index into the System Service Descriptor Table (SSDT)."
              },
              {
                phase: "Step 4 of 6",
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Privileged Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFF80020521080 (ntoskrnl.exe SSDT)",
                stack: "Kernel Stack (KTHREAD)",
                stepNum: "Step 4 of 6: SSDT Lookup &amp; Parameter Validation",
                activeNode: "node-kernel-idt",
                activeEdges: ["edge-3"],
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                node1Title: "Win32 Application",
                node1Sub: "ReadFile(hFile, buf, 512)",
                node2Title: "ntdll.dll (Native Stub)",
                node2Sub: "NtReadFile (SSN in EAX)",
                node4Title: "SSDT / KiSystemCall64",
                node4Sub: "KeServiceDescriptorTable",
                node5Title: "I/O Manager &amp; Drivers",
                node5Sub: "IRP &rarr; ntfs.sys &rarr; NVMe",
                what: "The kernel dispatcher indexes into <code>KeServiceDescriptorTable</code> to locate <code>NtReadFile</code>. It probes user buffer pointers via <code>ProbeForWrite()</code> to verify accessibility.",
                why: "The kernel must rigorously validate memory ranges to prevent malicious applications from tricking supervisor code into reading or writing kernel memory.",
                nextStep: "The Windows I/O Manager allocates an I/O Request Packet (IRP) and routes it to the filesystem and disk driver stack."
              },
              {
                mode: "KERNEL (Ring 0)",
                modeBit: "0 (Privileged Mode)",
                modeColor: "#0284c7",
                pc: "0xFFFFF80020684100 (Driver Stack)",
                stack: "Kernel Stack (KTHREAD)",
                stepNum: "Step 5 of 6: IRP Processing &amp; Storage Drivers",
                activeNode: "node-kernel-driver",
                activeEdges: ["edge-4"],
                btnNextText: "Next Step &rarr;",
                btnPrevText: "&larr; Prev",
                node1Title: "Win32 Application",
                node1Sub: "ReadFile(hFile, buf, 512)",
                node2Title: "ntdll.dll (Native Stub)",
                node2Sub: "NtReadFile (SSN in EAX)",
                node4Title: "SSDT / KiSystemCall64",
                node4Sub: "KeServiceDescriptorTable",
                node5Title: "I/O Manager &amp; Drivers",
                node5Sub: "IRP &rarr; ntfs.sys &rarr; NVMe",
                what: "The I/O Manager allocates an IRP and passes it down the driver stack (<code>ntfs.sys</code> &rarr; <code>classpnp.sys</code> &rarr; <code>stornvme.sys</code>), which commands the hardware to fetch data.",
                why: "The packet-driven IRP model decouples high-level filesystems from physical bus architectures, supporting asynchronous non-blocking I/O across heterogeneous storage devices.",
                nextStep: "The driver completes the IRP, returns an NTSTATUS code (STATUS_SUCCESS), and executes <code>sysret</code> to return to Ring 3."
              },
              {
                mode: "USER (Ring 3)",
                modeBit: "1 (Unprivileged)",
                modeColor: "#dc2626",
                pc: "0x00007FF710001208 (Resumed App Code)",
                stack: "Restored User Stack (RSP)",
                stepNum: "Step 6 of 6: Return to User Mode (sysret / Status Translation)",
                activeNode: "node-user-app",
                activeEdges: ["edge-5"],
                btnNextText: "Restart Walkthrough &#8634;",
                btnPrevText: "&larr; Prev",
                node1Title: "Win32 Application",
                node1Sub: "ReadFile() returns TRUE",
                node2Title: "ntdll.dll (Native Stub)",
                node2Sub: "NtReadFile (SSN in EAX)",
                node4Title: "SSDT / KiSystemCall64",
                node4Sub: "KeServiceDescriptorTable",
                node5Title: "I/O Manager &amp; Drivers",
                node5Sub: "IRP &rarr; ntfs.sys &rarr; NVMe",
                what: "The kernel executes <code>sysret</code>. The CPU returns to Ring 3 in <code>ntdll.dll</code>, which passes the <code>NTSTATUS</code> back to <code>kernelbase.dll</code>. The Win32 API converts it to <code>TRUE</code> and the application resumes.",
                why: "Privilege is safely dropped back to user mode. Subsystem DLLs translate internal NT status codes into user-friendly Win32 return conventions.",
                nextStep: "Lifecycle complete. Click Restart to replay the sequence from Step 1."
              }
            ]
          };

          let currentTrapPlatform = "unix";
          let trapIndex = 0;

          function renderTrapState() {
            const data = trapPlatforms[currentTrapPlatform][trapIndex];
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
            if (trapIndex < trapPlatforms[currentTrapPlatform].length - 1) {
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

def update_trap_simulator():
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
        content = content[:start] + TRAP_SIMULATOR_HTML.strip() + content[end:]
        print("--> Injected Unix vs Windows toggle into TRAP simulator.")
    else:
        print("--> Interactive TRAP simulator container not found.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Add Windows NT vs Unix toggle to dual-mode TRAP simulator in Module 2\n\n"
            "Enable comparative walkthrough of Windows Win32/ntdll/SSDT/IRP pipeline\n"
            "versus Unix syscall mechanisms in 02-hardware-review.html via fix.py."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_trap_simulator()
