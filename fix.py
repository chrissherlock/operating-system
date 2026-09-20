#!/usr/bin/env python3
# =====================================================================
# fix.py: Inject interactive guided pedagogical widget into Module 2
# =====================================================================
import os
import re
import subprocess

INTERACTIVE_WIDGET_HTML = """
      <div id="interactive-trap-simulator" style="margin: 32px 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 18px;">
          <div>
            <h3 style="margin: 0; color: #0284c7; font-size: 1.15rem;">Guided Walkthrough: The Dual-Mode TRAP &amp; Syscall Lifecycle</h3>
            <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Step through how hardware enforces isolation when an application requests privileged OS services.</p>
          </div>
          <div style="display: flex; gap: 8px; align-items: center;">
            <button id="step-prev-btn" style="padding: 6px 14px; font-family: var(--font-mono); font-size: 0.82rem; font-weight: 600; border-radius: 6px; border: 1px solid #cbd5e1; background: #f8fafc; color: #475569; cursor: pointer;">&larr; Prev</button>
            <button id="step-next-btn" style="padding: 6px 14px; font-family: var(--font-mono); font-size: 0.82rem; font-weight: 600; border-radius: 6px; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; cursor: pointer;">Next Step &rarr;</button>
            <button id="step-reset-btn" style="padding: 6px 10px; font-family: var(--font-mono); font-size: 0.82rem; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #64748b; cursor: pointer;">Reset</button>
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
          <svg id="trap-anim-svg" viewBox="0 0 820 280" width="100%" height="auto" style="max-width: 820px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <marker id="marker-blue" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto">
                <path d="M0,0 L6,3 L0,6 Z" fill="#0284c7" />
              </marker>
              <marker id="marker-red" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto">
                <path d="M0,0 L6,3 L0,6 Z" fill="#dc2626" />
              </marker>
            </defs>

            <!-- User Space Band -->
            <rect x="20" y="20" width="780" height="105" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="6,4" />
            <text x="35" y="42" fill="#64748b" font-size="11" font-weight="700">USER ADDRESS SPACE (Ring 3)</text>

            <!-- Kernel Space Band -->
            <rect x="20" y="155" width="780" height="105" rx="6" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.5" />
            <text x="35" y="177" fill="#0369a1" font-size="11" font-weight="700">KERNEL ADDRESS SPACE (Ring 0)</text>

            <!-- Node 1: User App -->
            <rect id="node-user-app" x="45" y="55" width="170" height="52" rx="5" fill="#ffffff" stroke="#0284c7" stroke-width="2" />
            <text x="130" y="78" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">User Process</text>
            <text x="130" y="94" fill="#64748b" font-size="10" text-anchor="middle">read(fd, buf, len)</text>

            <!-- Node 2: Library Stub / Trap Invocation -->
            <rect id="node-trap-trigger" x="270" y="55" width="170" height="52" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="355" y="78" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">Syscall Instruction</text>
            <text x="355" y="94" fill="#64748b" font-size="10" text-anchor="middle">TRAP / SYSCALL</text>

            <!-- Node 3: CPU Hardware Switch -->
            <rect id="node-cpu-hw" x="510" y="105" width="180" height="60" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="600" y="130" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">CPU Hardware Engine</text>
            <text x="600" y="148" fill="#64748b" font-size="10" text-anchor="middle">Mode: 1 &rarr; 0 | Save SP/PC</text>

            <!-- Node 4: IDT Handler -->
            <rect id="node-kernel-idt" x="270" y="185" width="170" height="52" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="355" y="208" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">IDT Dispatcher</text>
            <text x="355" y="224" fill="#64748b" font-size="10" text-anchor="middle">sys_call_table[__NR_read]</text>

            <!-- Node 5: Kernel Service / Device -->
            <rect id="node-kernel-driver" x="45" y="185" width="170" height="52" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
            <text x="130" y="208" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">VFS &amp; Disk Driver</text>
            <text x="130" y="224" fill="#64748b" font-size="10" text-anchor="middle">Execute Privileged I/O</text>

            <!-- Connecting Flows -->
            <line id="edge-1" x1="215" y1="81" x2="265" y2="81" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />
            <path id="edge-2" d="M 440,81 L 505,125" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />
            <path id="edge-3" d="M 505,145 L 445,200" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />
            <line id="edge-4" x1="270" y1="211" x2="220" y2="211" stroke="#cbd5e1" stroke-width="2" marker-end="url(#marker-blue)" />
            <path id="edge-5" d="M 130,185 C 130,145 130,120 130,113" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#marker-blue)" />
          </svg>
        </div>

        <!-- Dynamic Pedagogical Explanation Cards -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div style="background: #f8fafc; border-left: 4px solid #0284c7; padding: 14px 18px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #0284c7; text-transform: uppercase;">What Is Happening</div>
            <div id="desc-what" style="font-size: 0.92rem; color: #1e293b; line-height: 1.5; margin-top: 6px;">
              The user application is running in user space (Ring 3). It prepares arguments for a file read and executes a library wrapper call.
            </div>
          </div>
          <div style="background: #f8fafc; border-left: 4px solid #10b981; padding: 14px 18px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase;">Pedagogical Insight (Why This Matters)</div>
            <div id="desc-why" style="font-size: 0.92rem; color: #1e293b; line-height: 1.5; margin-top: 6px;">
              User applications cannot execute raw CPU I/O instructions (like <code>IN</code>/<code>OUT</code>) or modify device controllers directly. Enforcing user mode prevents buggy or malicious software from wiping the disk.
            </div>
          </div>
        </div>
      </div>

      <script>
        (function() {
          const steps = [
            {
              mode: "USER (Ring 3)",
              modeBit: "1 (Unprivileged)",
              modeColor: "#dc2626",
              pc: "0x00401140 (App Code)",
              stack: "User Stack (RSP)",
              stepNum: "Step 1 of 6: Application Invocations",
              activeNode: "node-user-app",
              activeEdges: [],
              what: "The user program needs to read 512 bytes from a file. It calls <code>read(fd, buffer, 512)</code> in standard C library space.",
              why: "User-level isolation ensures no user program can directly read or write physical hardware sectors without operating system intervention."
            },
            {
              mode: "USER (Ring 3)",
              modeBit: "1 (Unprivileged)",
              modeColor: "#dc2626",
              pc: "0x004085A0 (Syscall Wrapper)",
              stack: "User Stack (RSP)",
              stepNum: "Step 2 of 6: Preparing System Call &amp; TRAP",
              activeNode: "node-trap-trigger",
              activeEdges: ["edge-1"],
              what: "The C library wrapper places the system call identifier for read (e.g., RAX = 0 on x86-64) into registers and issues the <code>SYSCALL</code> or <code>TRAP</code> machine instruction.",
              why: "A special hardware instruction is mandatory because user mode software cannot arbitrarily change its own privilege register without an immediate hardware fault."
            },
            {
              mode: "KERNEL (Ring 0)",
              modeBit: "0 (Privileged Mode)",
              modeColor: "#0284c7",
              pc: "0xFFFFFFFF81A00000 (Hardware Switch)",
              stack: "Switched to Kernel Stack (SS:RSP)",
              stepNum: "Step 3 of 6: Hardware Mode Switch &amp; Context Save",
              activeNode: "node-cpu-hw",
              activeEdges: ["edge-2"],
              what: "The CPU microcode immediately flips the mode bit in the Program Status Word from 1 to 0, saves the user Program Counter and Stack Pointer onto the process's secure kernel stack, and vectors to the kernel entry point.",
              why: "The hardware automatically saves the return location on a kernel-protected stack so user code cannot tamper with return addresses while in supervisor mode."
            },
            {
              mode: "KERNEL (Ring 0)",
              modeBit: "0 (Privileged Mode)",
              modeColor: "#0284c7",
              pc: "0xFFFFFFFF81B23040 (Syscall Dispatcher)",
              stack: "Kernel Stack (SS:RSP)",
              stepNum: "Step 4 of 6: Kernel IDT Dispatching",
              activeNode: "node-kernel-idt",
              activeEdges: ["edge-3"],
              what: "The kernel checks the system call number in RAX against its syscall dispatch table, verifies that user buffer pointers are valid, and routes to the Virtual File System (VFS).",
              why: "All parameter boundaries must be thoroughly vetted in kernel space to prevent user programs from passing invalid kernel memory addresses to trick the OS."
            },
            {
              mode: "KERNEL (Ring 0)",
              modeBit: "0 (Privileged Mode)",
              modeColor: "#0284c7",
              pc: "0xFFFFFFFF81C84100 (Disk Driver)",
              stack: "Kernel Stack (SS:RSP)",
              stepNum: "Step 5 of 6: Privileged Driver Execution",
              activeNode: "node-kernel-driver",
              activeEdges: ["edge-4"],
              what: "The storage device driver issues privileged commands directly to the NVMe or SATA controller (or initiates a DMA transfer) to read the requested sectors.",
              why: "Only kernel mode code possesses the hardware privileges required to communicate over system buses with peripheral device controllers."
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
              what: "The kernel places the read byte count into RAX, executes <code>SYSRET</code> (or <code>IRET</code>), restoring the CPU mode bit to 1, restoring the user stack pointer, and resuming application execution.",
              why: "Execution control is safely returned to unprivileged mode with zero exposure of internal kernel memory or device control structures."
            }
          ];

          let currentIndex = 0;

          function renderTraceState() {
            const data = steps[currentIndex];
            document.getElementById("status-cpu-mode").textContent = data.mode;
            document.getElementById("status-cpu-mode").style.color = data.modeColor;
            document.getElementById("status-mode-bit").textContent = data.modeBit;
            document.getElementById("status-mode-bit").style.color = data.modeColor;
            document.getElementById("status-pc-reg").textContent = data.pc;
            document.getElementById("status-stack").textContent = data.stack;
            document.getElementById("status-step-num").innerHTML = data.stepNum;
            document.getElementById("desc-what").innerHTML = data.what;
            document.getElementById("desc-why").innerHTML = data.why;

            // Reset all nodes
            const allNodes = ["node-user-app", "node-trap-trigger", "node-cpu-hw", "node-kernel-idt", "node-kernel-driver"];
            allNodes.forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                el.setAttribute("stroke", "#cbd5e1");
                el.setAttribute("stroke-width", "1.5");
                el.setAttribute("fill", "#ffffff");
              }
            });

            // Reset all edges
            const allEdges = ["edge-1", "edge-2", "edge-3", "edge-4", "edge-5"];
            allEdges.forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                el.setAttribute("stroke", "#cbd5e1");
                el.setAttribute("stroke-width", "2");
              }
            });

            // Highlight active node
            const activeNodeEl = document.getElementById(data.activeNode);
            if (activeNodeEl) {
              activeNodeEl.setAttribute("stroke", data.modeColor === "#0284c7" ? "#0284c7" : "#dc2626");
              activeNodeEl.setAttribute("stroke-width", "2.5");
              activeNodeEl.setAttribute("fill", data.modeColor === "#0284c7" ? "#f0f9ff" : "#fef2f2");
            }

            // Highlight active edges
            data.activeEdges.forEach(id => {
              const edgeEl = document.getElementById(id);
              if (edgeEl) {
                edgeEl.setAttribute("stroke", "#0284c7");
                edgeEl.setAttribute("stroke-width", "3");
              }
            });
          }

          document.getElementById("step-next-btn").addEventListener("click", function() {
            if (currentIndex < steps.length - 1) {
              currentIndex++;
              renderTraceState();
            }
          });

          document.getElementById("step-prev-btn").addEventListener("click", function() {
            if (currentIndex > 0) {
              currentIndex--;
              renderTraceState();
            }
          });

          document.getElementById("step-reset-btn").addEventListener("click", function() {
            currentIndex = 0;
            renderTraceState();
          });

          renderTraceState();
        })();
      </script>
"""

def inject_interactive_element():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Place interactive simulator in Section 2 (Privilege Modes & Hardware Protection)
    if 'id="interactive-trap-simulator"' not in content:
        # Insert right after the static TRAP diagram
        target_marker = '</h2>\n      <p>\n        To prevent rogue or faulty user software'
        if '</svg>\n      </div>' in content:
            # Locate the TRAP diagram container and insert after it
            pos_trap = content.find('USER SPACE (User Mode / Ring 3)')
            if pos_trap != -1:
                end_trap_container = content.find('</div>', content.find('</svg>', pos_trap)) + 6
                content = content[:end_trap_container] + "\n" + INTERACTIVE_WIDGET_HTML + content[end_trap_container:]
                print("--> Successfully inserted interactive simulator after TRAP diagram.")
        else:
            print("--> Could not locate exact insertion marker.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Add interactive guided system call stepper widget to Module 2\n\n"
            "Inject pedagogical step-by-step dual-mode TRAP lifecycle simulator into\n"
            "week01-operating-system-concepts/02-hardware-review.html via fix.py."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    inject_interactive_element()
