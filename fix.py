#!/usr/bin/env python3
# =====================================================================
# fix.py: Place next step buttons under simulator guide with adjacent explanation
# =====================================================================
import os
import re
import subprocess

RESTRUCTURED_SIMULATOR_TOP = """
        <!-- Simulator Title Header -->
        <div style="border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 18px;">
          <h3 style="margin: 0; color: #0284c7; font-size: 1.15rem;">Guided Walkthrough: The Dual-Mode TRAP &amp; Syscall Lifecycle</h3>
          <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Step through how hardware enforces isolation when an application requests privileged OS services.</p>
        </div>

        <!-- Instructions Guide -->
        <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px; margin-bottom: 16px;">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">How to Use This Simulator</div>
          <ol style="margin-left: 20px; margin-bottom: 0; color: #334155; font-size: 0.88rem; line-height: 1.5;">
            <li><strong>Step Through the Lifecycle:</strong> Use the controls below to step through each execution phase in sequence.</li>
            <li><strong>Observe the Hardware State Bar:</strong> Notice the <strong>CPU Mode</strong> color switch between red (User Mode) and blue (Kernel Mode), and watch the <strong>Program Counter (PC)</strong> move between user addresses and kernel routines.</li>
            <li><strong>Follow Active Nodes &amp; Buses:</strong> The highlighted vector path shows which hardware unit has execution priority at each step.</li>
          </ol>
        </div>

        <!-- Action Controls & Inline Next Step Explanation -->
        <div style="display: grid; grid-template-columns: auto 1fr; gap: 16px; align-items: stretch; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px; margin-bottom: 20px;">
          <!-- Buttons Stack -->
          <div style="display: flex; flex-direction: column; gap: 8px; justify-content: center; min-width: 170px;">
            <button id="step-next-btn" style="padding: 10px 16px; font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; border-radius: 6px; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; cursor: pointer; text-align: center; transition: all 0.15s ease;">Next Step &rarr;</button>
            <div style="display: flex; gap: 8px;">
              <button id="step-prev-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; font-weight: 600; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">&larr; Prev</button>
              <button id="step-reset-btn" style="flex: 1; padding: 6px 10px; font-family: var(--font-mono); font-size: 0.8rem; border-radius: 6px; border: 1px solid #cbd5e1; background: #ffffff; color: #64748b; cursor: pointer;">Reset</button>
            </div>
          </div>

          <!-- Inline Next Step Explanation Pane -->
          <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-left: 4px solid #0284c7; border-radius: 0 6px 6px 0; padding: 10px 14px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: #0369a1; text-transform: uppercase; letter-spacing: 0.03em;">Upcoming Action When You Click Next:</div>
            <div id="inline-next-desc" style="font-size: 0.88rem; color: #0c4a6e; line-height: 1.45; margin-top: 4px;">
              The C runtime wrapper will stage system call arguments into CPU registers (e.g., RAX = 0 for sys_read) and issue the <code>SYSCALL</code> / <code>TRAP</code> assembly instruction.
            </div>
          </div>
        </div>
"""

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
            document.getElementById("inline-next-desc").innerHTML = data.nextStep;

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

def reposition_controls():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match everything from the start of #interactive-trap-simulator to the start of the Hardware State Bar
    pattern_top = r'<div id="interactive-trap-simulator"[^>]*>.*?<!-- Hardware State Bar -->'
    if re.search(pattern_top, content, flags=re.DOTALL):
        replacement = f'<div id="interactive-trap-simulator" style="margin: 32px 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">' + "\n" + RESTRUCTURED_SIMULATOR_TOP + "\n        <!-- Hardware State Bar -->"
        content = re.sub(pattern_top, replacement, content, flags=re.DOTALL)
        print("--> Repositioned simulator buttons and explanation under the how-to guide.")

    # Update bottom dashboard to two cards (What Is Happening, Why The System Does This) since Next is now inline above
    two_pane_dashboard = """        <!-- Two-Pane Pedagogical Dashboard -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 20px;">
          <!-- Current Action Pane -->
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0284c7; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #0284c7; text-transform: uppercase; letter-spacing: 0.03em;">Current State: What Is Happening</div>
            <div id="desc-what" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;">
              The user program needs to read 512 bytes from a file. It calls <code>read(fd, buffer, 512)</code> in standard user space.
            </div>
          </div>

          <!-- Rationale Pane -->
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #10b981; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 0.03em;">Why The System Does This</div>
            <div id="desc-why" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;">
              User-level isolation ensures no application can directly manipulate physical hardware sectors without operating system supervision.
            </div>
          </div>
        </div>"""

    pattern_bottom = r'<!-- Three-Pane Pedagogical Dashboard -->.*?</div>\s*</div>\s*</div>'
    if re.search(pattern_bottom, content, flags=re.DOTALL):
        content = re.sub(pattern_bottom, two_pane_dashboard + "\n      </div>", content, flags=re.DOTALL)
        print("--> Updated bottom dashboard to clean 2-card layout.")

    # Update script logic
    script_pattern = r"<script>\s*\(function\(\)\s*\{\s*const steps = \[.*?\];\s*let currentIndex = 0;.*?</script>"
    if re.search(script_pattern, content, flags=re.DOTALL):
        content = re.sub(script_pattern, REVISED_SCRIPT_LOGIC.strip(), content, flags=re.DOTALL)
        print("--> Updated script logic to target #inline-next-desc.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Relocate simulator controls beneath instructions with adjacent next step guide\n\n"
            "Move navigation buttons below the usage guide in 02-hardware-review.html\n"
            "with an inline pane detailing the upcoming step right next to the controls."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    reposition_controls()
