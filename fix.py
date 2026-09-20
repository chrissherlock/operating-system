#!/usr/bin/env python3
# =====================================================================
# fix.py: Add explicit next-step previews and dynamic button labels
# =====================================================================
import os
import re
import subprocess

REVISED_SCRIPT_LOGIC = """
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
              btnNextText: "Next: Invoke SYSCALL Instruction &rarr;",
              btnPrevText: "&larr; Prev",
              upcoming: "Up next: C library stub sets registers and issues the hardware TRAP instruction.",
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
              btnNextText: "Next: CPU Hardware Mode Switch &rarr;",
              btnPrevText: "&larr; Prev: App Invocation",
              upcoming: "Up next: CPU hardware catches the TRAP, flips the privilege bit to 0, and switches stacks.",
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
              btnNextText: "Next: Vector to IDT Syscall Dispatcher &rarr;",
              btnPrevText: "&larr; Prev: SYSCALL Trigger",
              upcoming: "Up next: Execution jumps to the kernel Interrupt Descriptor Table (IDT) to look up the syscall routine.",
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
              btnNextText: "Next: Execute Privileged Storage Driver &rarr;",
              btnPrevText: "&larr; Prev: Hardware Switch",
              upcoming: "Up next: Kernel routes to the device driver to send read commands to the storage controller.",
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
              btnNextText: "Next: Return to User Mode (SYSRET) &rarr;",
              btnPrevText: "&larr; Prev: IDT Dispatcher",
              upcoming: "Up next: Kernel finishes I/O and executes SYSRET to drop privileges back to user space.",
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
              btnNextText: "Restart Walkthrough &#8634;",
              btnPrevText: "&larr; Prev: Driver Execution",
              upcoming: "Lifecycle complete. Click Restart to replay the sequence from Step 1.",
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

            // Update interactive button text and preview ticker
            const nextBtn = document.getElementById("step-next-btn");
            const prevBtn = document.getElementById("step-prev-btn");
            const upcomingEl = document.getElementById("step-upcoming-preview");

            if (nextBtn) nextBtn.innerHTML = data.btnNextText;
            if (prevBtn) {
              prevBtn.innerHTML = data.btnPrevText;
              prevBtn.style.opacity = currentIndex === 0 ? "0.5" : "1.0";
              prevBtn.style.cursor = currentIndex === 0 ? "not-allowed" : "pointer";
            }
            if (upcomingEl) upcomingEl.innerHTML = data.upcoming;

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
            } else {
              currentIndex = 0;
            }
            renderTraceState();
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

def inject_upcoming_preview_and_script():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add upcoming action ticker beneath instructions box if not present
    if 'id="step-upcoming-preview"' not in content:
        ticker_html = """        <div style="display: flex; align-items: center; gap: 8px; background: #e0f2fe; border: 1px solid #bae6fd; border-radius: 6px; padding: 10px 14px; margin-bottom: 16px; font-family: var(--font-mono); font-size: 0.82rem;">
          <span style="font-weight: 700; color: #0369a1; text-transform: uppercase;">Upcoming Action:</span>
          <span id="step-upcoming-preview" style="color: #0c4a6e;">Up next: C library stub sets registers and issues the hardware TRAP instruction.</span>
        </div>"""
        target_pos = content.find('<!-- Hardware State Bar -->')
        if target_pos != -1:
            content = content[:target_pos] + ticker_html + "\n\n        " + content[target_pos:]
            print("--> Added dynamic upcoming action ticker.")

    # 2. Replace simulator script block with revised logic
    script_pattern = r"<script>\s*\(function\(\)\s*\{\s*const steps = \[.*?\];\s*let currentIndex = 0;.*?</script>"
    if re.search(script_pattern, content, flags=re.DOTALL):
        content = re.sub(script_pattern, REVISED_SCRIPT_LOGIC.strip(), content, flags=re.DOTALL)
        print("--> Updated interactive script logic with dynamic next step names.")
    else:
        print("--> Script pattern match not found; check script boundaries.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Add dynamic next-action previews and descriptive button labels to simulator\n\n"
            "Update week01-operating-system-concepts/02-hardware-review.html so the next\n"
            "step button explicitly names the upcoming hardware event before clicking."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    inject_upcoming_preview_and_script()
