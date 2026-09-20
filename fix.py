#!/usr/bin/env python3
# =====================================================================
# fix.py: Add dedicated Next Step explanation pane to Module 2
# =====================================================================
import os
import re
import subprocess

THREE_PANE_DASHBOARD_HTML = """
        <!-- Three-Pane Pedagogical Dashboard -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin-top: 20px;">
          <!-- Current Action Pane -->
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0284c7; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #0284c7; text-transform: uppercase; letter-spacing: 0.03em;">Current State: What Is Happening</div>
            <div id="desc-what" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;">
              The user program needs to read 512 bytes from a file. It calls <code>read(fd, buffer, 512)</code> in standard C library space.
            </div>
          </div>

          <!-- Rationale Pane -->
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #10b981; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 0.03em;">Why The System Does This</div>
            <div id="desc-why" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;">
              User-level isolation ensures no application can directly manipulate physical hardware sectors or issue raw disk commands without operating system supervision.
            </div>
          </div>

          <!-- Dedicated Next Step Pane -->
          <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-left: 4px solid #0369a1; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #0369a1; text-transform: uppercase; letter-spacing: 0.03em;">Next Step: What To Expect</div>
            <div id="desc-next" style="font-size: 0.9rem; color: #0c4a6e; line-height: 1.55; margin-top: 8px;">
              The C runtime wrapper will place system call arguments into CPU registers (e.g., RAX = 0 for sys_read) and issue the <code>SYSCALL</code> / <code>TRAP</code> assembly instruction.
            </div>
          </div>
        </div>
"""

REVISED_SCRIPT = """
      <script>
        (function() {
          const steps = [
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
              what: "The user program needs to read 512 bytes from a file. It calls <code>read(fd, buffer, 512)</code> in standard user space.",
              why: "User-level isolation ensures no application can directly manipulate physical hardware sectors without operating system supervision.",
              nextStep: "The C runtime wrapper will stage system call arguments into CPU registers (e.g., RAX = 0 for sys_read) and issue the <code>SYSCALL</code> / <code>TRAP</code> assembly instruction."
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
              btnNextText: "Next Step &rarr;",
              btnPrevText: "&larr; Prev",
              what: "The library stub populates the register parameters and executes the <code>SYSCALL</code> / <code>TRAP</code> instruction to trigger a hardware trap.",
              why: "User code cannot change the CPU mode bit on its own. It must execute a designated hardware instruction to request kernel entry.",
              nextStep: "The CPU microcode will intercept the TRAP, switch the CPU Mode Bit from 1 to 0 (Kernel Mode), swap the user stack pointer to the kernel stack, and jump to the IDT."
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
              btnNextText: "Next Step &rarr;",
              btnPrevText: "&larr; Prev",
              what: "The CPU switches into Ring 0, saves the user Program Counter and Stack Pointer onto the kernel stack, and transfers control to the kernel vector.",
              why: "Saving user execution state on a kernel-protected stack guarantees that unprivileged code cannot alter return addresses while running supervisor routines.",
              nextStep: "The kernel Interrupt Descriptor Table (IDT) dispatcher will inspect RAX and index into <code>sys_call_table</code> to locate the file read handler."
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
              btnNextText: "Next Step &rarr;",
              btnPrevText: "&larr; Prev",
              what: "The kernel verifies pointer boundaries to confirm that the destination buffer is writable, then invokes the Virtual File System (VFS) read handler.",
              why: "Kernel verification ensures malicious or buggy user pointers cannot trick supervisor routines into overwriting protected memory.",
              nextStep: "The filesystem driver will program the storage controller registers and initiate a DMA or interrupt-driven block read from the disk drive."
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
              btnNextText: "Next Step &rarr;",
              btnPrevText: "&larr; Prev",
              what: "The device driver issues privileged hardware commands to the storage controller across the system bus, reading data into memory.",
              why: "Only kernel mode code has the hardware authorization to communicate with device controllers across system buses without triggering an exception.",
              nextStep: "The kernel will store the byte count result into RAX and execute <code>SYSRET</code> or <code>IRET</code> to drop privileges back to user space."
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
              what: "The kernel executes <code>SYSRET</code>. The CPU restores the user mode bit to 1, reloads the user stack pointer, and returns execution to the application.",
              why: "Dropping privileges back to Ring 3 ensures normal applications never remain in supervisor mode after their requested work is complete.",
              nextStep: "Lifecycle complete. Clicking restart will reset the simulator back to Step 1."
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
            document.getElementById("desc-next").innerHTML = data.nextStep;

            const nextBtn = document.getElementById("step-next-btn");
            const prevBtn = document.getElementById("step-prev-btn");

            if (nextBtn) nextBtn.innerHTML = data.btnNextText;
            if (prevBtn) {
              prevBtn.innerHTML = data.btnPrevText;
              prevBtn.style.opacity = currentIndex === 0 ? "0.5" : "1.0";
              prevBtn.style.cursor = currentIndex === 0 ? "not-allowed" : "pointer";
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

def replace_with_three_pane_dashboard():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove obsolete single-line upcoming action ticker if present
    content = re.sub(
        r'<div style="display: flex; align-items: center; gap: 8px; background: #e0f2fe;.*?</div>\s*',
        '',
        content,
        flags=re.DOTALL
    )

    # 2. Replace old two-column explanation cards with the new 3-pane dashboard
    old_explanation_cards = re.search(
        r'<!-- Dynamic Pedagogical Explanation Cards -->.*?</div>\s*</div>\s*</div>',
        content,
        flags=re.DOTALL
    )
    if old_explanation_cards:
        content = content.replace(old_explanation_cards.group(0), THREE_PANE_DASHBOARD_HTML.strip() + "\n      </div>")
        print("--> Replaced two-column explanation cards with 3-pane dashboard.")
    else:
        # Fallback: search by ID desc-what container
        pattern_fallback = r'<div style="display: grid; grid-template-columns: 1fr 1fr;.*?</div>\s*</div>\s*</div>'
        if re.search(pattern_fallback, content, flags=re.DOTALL):
            content = re.sub(pattern_fallback, THREE_PANE_DASHBOARD_HTML.strip() + "\n      </div>", content, flags=re.DOTALL)
            print("--> Replaced explanation cards via fallback pattern.")

    # 3. Replace script logic to populate desc-next
    script_pattern = r"<script>\s*\(function\(\)\s*\{\s*const steps = \[.*?\];\s*let currentIndex = 0;.*?</script>"
    if re.search(script_pattern, content, flags=re.DOTALL):
        content = re.sub(script_pattern, REVISED_SCRIPT.strip(), content, flags=re.DOTALL)
        print("--> Injected updated script supporting desc-next pane.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Add dedicated Next Step explanation pane to Module 2 interactive widget\n\n"
            "Update week01-operating-system-concepts/02-hardware-review.html to replace\n"
            "the ticker with a persistent three-pane dashboard detailing the next step."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    replace_with_three_pane_dashboard()
