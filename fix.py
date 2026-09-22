#!/usr/bin/env python3
# =====================================================================
# fix.py: Place contextual definitions in dedicated section below panes
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "03-os-concepts.html"
)

REVISED_STEPPER_BLOCK = r"""    <!-- INTERACTIVE PEDAGOGICAL AID: DIRECTED NARRATIVE STEPPER -->
    <div id="interactive-process-stepper" style="margin: 36px 0; border: 1px solid #cbd5e1; border-radius: 8px; background: #ffffff; padding: 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 16px;">
        <div>
          <h3 style="margin: 0; color: #0284c7; font-size: 1.25rem;">Interactive Simulator: Process Lifecycle Walkthrough</h3>
          <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Scenario: Database query report execution (PID 4092) under severe memory contention and storage I/O.</p>
        </div>

        <!-- Comparative Dimension Toggles -->
        <div style="display: flex; gap: 6px;">
          <button type="button" class="model-toggle active" data-model="3" style="padding: 6px 12px; font-size: 0.8rem; font-weight: 700; border-radius: 4px; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; cursor: pointer;">3-State</button>
          <button type="button" class="model-toggle" data-model="5" style="padding: 6px 12px; font-size: 0.8rem; font-weight: 700; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">5-State</button>
          <button type="button" class="model-toggle" data-model="7" style="padding: 6px 12px; font-size: 0.8rem; font-weight: 700; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">7-State</button>
        </div>
      </div>

      <!-- Live State Telemetry Status Bar -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 14px; margin-bottom: 18px; font-family: var(--font-mono); font-size: 0.8rem;">
        <div><span style="color: #64748b;">CURRENT STATE:</span> <strong id="telemetry-state" style="color: #0284c7;">READY</strong></div>
        <div><span style="color: #64748b;">RESIDENCE:</span> <strong id="telemetry-residence" style="color: #059669;">PHYSICAL DRAM</strong></div>
        <div><span style="color: #64748b;">ACTIVE CPU:</span> <strong id="telemetry-cpu" style="color: #475569;">NONE (IN QUEUE)</strong></div>
        <div><span style="color: #64748b;">PENDING I/O:</span> <strong id="telemetry-io" style="color: #475569;">NONE</strong></div>
      </div>

      <!-- Synchronized Visual Canvas -->
      <div style="display: flex; justify-content: center; background: #ffffff; border: 1px solid #f1f5f9; border-radius: 6px; padding: 12px; margin-bottom: 18px;">
        <svg id="stepper-svg" viewBox="0 0 820 340" width="100%" height="100%" style="max-width: 820px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="step-arrow-default" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
              <polygon points="0 1, 6 3.5, 0 6" fill="#94a3b8" />
            </marker>
            <marker id="step-arrow-active" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
              <polygon points="0 1, 6 3.5, 0 6" fill="#0284c7" />
            </marker>
            <filter id="active-glow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#0284c7" flood-opacity="0.6" />
            </filter>
          </defs>

          <!-- Bounds Guide -->
          <rect id="dram-zone" x="10" y="20" width="800" height="175" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-dasharray="4,4" />
          <text id="dram-label" x="25" y="38" fill="#94a3b8" font-size="8.5" font-weight="700">PRIMARY MEMORY (PHYSICAL RAM)</text>

          <rect id="disk-zone" x="10" y="215" width="800" height="110" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-dasharray="4,4" style="display: none;" />
          <text id="disk-label" x="25" y="232" fill="#94a3b8" font-size="8.5" font-weight="700" style="display: none;">SECONDARY STORAGE (SWAPFILE ON DISK)</text>

          <!-- Clean Tangential Vector Paths -->
          <path id="path-admit" d="M 106,105 L 170,105" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#step-arrow-default)" style="display: none;" />
          <path id="path-dispatch" d="M 245,90 C 315,55 410,55 478,90" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#step-arrow-default)" />
          <path id="path-preempt" d="M 480,122 C 410,155 315,155 246,122" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#step-arrow-default)" />
          <path id="path-block" d="M 554,105 L 660,105" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#step-arrow-default)" />
          <path id="path-event" d="M 690,70 C 640,30 280,30 220,70" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#step-arrow-default)" />
          <path id="path-exit" d="M 535,74 C 585,35 710,35 750,75" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#step-arrow-default)" style="display: none;" />

          <path id="path-swapout-ready" d="M 200,144 L 218,232" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#step-arrow-default)" style="display: none;" />
          <path id="path-swapin-ready" d="M 235,232 L 217,146" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#step-arrow-default)" style="display: none;" />
          <path id="path-swapout-blocked" d="M 690,144 L 690,232" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#step-arrow-default)" style="display: none;" />
          <path id="path-swapin-blocked" d="M 712,232 L 712,146" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#step-arrow-default)" style="display: none;" />
          <path id="path-event-disk" d="M 662,270 L 268,270" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#step-arrow-default)" style="display: none;" />

          <!-- Circular State Nodes -->
          <g id="node-NEW" transform="translate(70, 105)" style="display: none;">
            <circle cx="0" cy="0" r="35" fill="#ffffff" stroke="#94a3b8" stroke-width="2" />
            <text x="0" y="-3" fill="#334155" font-size="10.5" font-weight="700" text-anchor="middle">NEW</text>
            <text x="0" y="11" fill="#64748b" font-size="7.5" text-anchor="middle">Creating</text>
          </g>

          <g id="node-READY" transform="translate(210, 105)">
            <circle cx="0" cy="0" r="38" fill="#eff6ff" stroke="#0284c7" stroke-width="2" />
            <text x="0" y="-3" fill="#0369a1" font-size="11" font-weight="700" text-anchor="middle">READY</text>
            <text x="0" y="11" fill="#64748b" font-size="7.5" text-anchor="middle">Run Queue</text>
          </g>

          <g id="node-RUNNING" transform="translate(515, 105)">
            <circle cx="0" cy="0" r="38" fill="#ecfdf5" stroke="#059669" stroke-width="2" />
            <text x="0" y="-3" fill="#065f46" font-size="11" font-weight="700" text-anchor="middle">RUNNING</text>
            <text x="0" y="11" fill="#047857" font-size="7.5" text-anchor="middle">CPU Core 1</text>
          </g>

          <g id="node-BLOCKED" transform="translate(700, 105)">
            <circle cx="0" cy="0" r="38" fill="#fef2f2" stroke="#ef4444" stroke-width="2" />
            <text x="0" y="-3" fill="#991b1b" font-size="11" font-weight="700" text-anchor="middle">BLOCKED</text>
            <text x="0" y="11" fill="#b91c1c" font-size="7.5" text-anchor="middle">Wait on I/O</text>
          </g>

          <g id="node-TERMINATED" transform="translate(770, 105)" style="display: none;">
            <circle cx="0" cy="0" r="32" fill="#fffbeb" stroke="#d97706" stroke-width="2" />
            <text x="0" y="-2" fill="#92400e" font-size="9.5" font-weight="700" text-anchor="middle">EXIT</text>
            <text x="0" y="10" fill="#78350f" font-size="7" text-anchor="middle">Zombie</text>
          </g>

          <g id="node-READY_SUSP" transform="translate(230, 270)" style="display: none;">
            <circle cx="0" cy="0" r="36" fill="#faf5ff" stroke="#9333ea" stroke-width="2" />
            <text x="0" y="-6" fill="#7e22ce" font-size="8" font-weight="700" text-anchor="middle">READY /</text>
            <text x="0" y="6" fill="#7e22ce" font-size="8" font-weight="700" text-anchor="middle">SUSPENDED</text>
          </g>

          <g id="node-BLOCKED_SUSP" transform="translate(700, 270)" style="display: none;">
            <circle cx="0" cy="0" r="36" fill="#fff1f2" stroke="#e11d48" stroke-width="2" />
            <text x="0" y="-6" fill="#be123c" font-size="8" font-weight="700" text-anchor="middle">BLOCKED /</text>
            <text x="0" y="6" fill="#be123c" font-size="8" font-weight="700" text-anchor="middle">SUSPENDED</text>
          </g>
        </svg>
      </div>

      <!-- Foreshadowed Navigation & Controls -->
      <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 20px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 16px;">
        <div style="display: flex; gap: 8px;">
          <button type="button" id="btn-prev-step" style="padding: 6px 14px; font-weight: 600; font-size: 0.85rem; border: 1px solid #cbd5e1; background: #ffffff; color: #334155; border-radius: 5px; cursor: pointer;">&larr; Prev</button>
          <button type="button" id="btn-next-step" style="padding: 6px 14px; font-weight: 600; font-size: 0.85rem; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; border-radius: 5px; cursor: pointer;">Next Step &rarr;</button>
          <button type="button" id="btn-reset-step" style="padding: 6px 12px; font-size: 0.85rem; border: 1px solid #cbd5e1; background: #ffffff; color: #64748b; border-radius: 5px; cursor: pointer;">Reset</button>
        </div>

        <!-- Inline Preview of Next Action -->
        <div style="font-size: 0.85rem; color: #334155;">
          <span style="color: #64748b; font-weight: 600;">UPCOMING TRANSITION:</span> <span id="preview-text" style="font-weight: 700; color: #0284c7;">Scheduler dispatches PID 4092 onto CPU Core 1</span>
        </div>
      </div>

      <!-- Paired Analytical Panes (Strict Mechanics vs. Rationale) -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
        <!-- Pane 1: Mechanics -->
        <div style="border: 1px solid #bae6fd; background: #f0f9ff; border-radius: 6px; padding: 16px;">
          <div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.85rem; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">1. What Is Happening (Low-Level Mechanics)</div>
          <div id="pane-mechanics" style="font-size: 0.9rem; color: #1e293b; line-height: 1.5;"></div>
        </div>

        <!-- Pane 2: Rationale -->
        <div style="border: 1px solid #fde68a; background: #fffbeb; border-radius: 6px; padding: 16px;">
          <div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.85rem; color: #92400e; text-transform: uppercase; margin-bottom: 6px;">2. Why The System Does This (Design Rationale)</div>
          <div id="pane-rationale" style="font-size: 0.9rem; color: #78350f; line-height: 1.5;"></div>
        </div>
      </div>

      <!-- Dedicated Contextual Definitions Section (Underneath on its own) -->
      <div style="border: 1px solid #e2e8f0; background: #f8fafc; border-radius: 6px; padding: 16px;">
        <div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.85rem; color: #475569; text-transform: uppercase; margin-bottom: 8px;">Contextual Definitions &amp; System Concepts</div>
        <div id="pane-definitions" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 12px;"></div>
      </div>
    </div>

    <!-- Stepper Logic Script -->
    <script>
      (function() {
        const scenarios = {
          "3": [
            {
              state: "READY",
              residence: "PHYSICAL DRAM",
              cpu: "NONE (IN QUEUE)",
              io: "NONE",
              node: "node-READY",
              activePath: "path-dispatch",
              preview: "Scheduler allocates time slice on CPU Core 1",
              mechanics: "PID 4092 resides in the kernel run queue. The scheduler selects it, loads its saved registers (RIP, RSP, RAX) from its Process Control Block into the CPU, and executes return-from-trap.",
              rationale: "Separates policy (which job to schedule) from mechanism (context switch execution). Allows CPU time-sharing among multiple resident tasks without program modification.",
              definitions: [
                { term: "Context Switch", desc: "Low-level assembly procedure that saves hardware CPU registers of the interrupted process and restores the register state of the scheduled process." },
                { term: "Policy vs. Mechanism", desc: "A foundational OS design rule: mechanisms specify 'how' a task is executed, while policies determine 'which' decisions are made." }
              ]
            },
            {
              state: "RUNNING",
              residence: "PHYSICAL DRAM",
              cpu: "CORE 1 (EXECUTING)",
              io: "NONE",
              node: "node-RUNNING",
              activePath: "path-block",
              preview: "Database query issues read() for table index on NVMe SSD",
              mechanics: "The program executes user-space arithmetic until encountering an un-cached database index. It invokes the read() system call, executing a trap instruction to switch from user mode to kernel mode.",
              rationale: "Limited Direct Execution guarantees native hardware execution speed while preventing unprivileged software from issuing arbitrary commands directly to raw hardware devices.",
              definitions: [
                { term: "Trap Instruction", desc: "A privileged hardware instruction that elevates CPU privilege from Ring 3 (User) to Ring 0 (Kernel) and jumps to a pre-registered trap table address." },
                { term: "Limited Direct Execution (LDE)", desc: "The operating system runs programs directly on the bare CPU hardware while maintaining strict control via hardware trap tables and timer interrupts." }
              ]
            },
            {
              state: "BLOCKED",
              residence: "PHYSICAL DRAM",
              cpu: "NONE (YIELDED)",
              io: "PENDING (NVMe READ)",
              node: "node-BLOCKED",
              activePath: "path-event",
              preview: "Storage controller raises interrupt upon finishing data transfer",
              mechanics: "The kernel marks PID 4092 as BLOCKED, moves its PCB from the active run queue into the NVMe controller's wait queue, and triggers a context switch to run another ready process.",
              rationale: "Maximizes CPU utilization. Reading from storage takes thousands to millions of CPU clock cycles; yielding the core prevents the processor from stalling on idle wait loops.",
              definitions: [
                { term: "Device Wait Queue", desc: "An in-kernel linked list tracking blocked processes awaiting hardware signals from a specific peripheral controller." },
                { term: "I/O Overlapping", desc: "Maximizing system efficiency by interleaving CPU computation of ready tasks with asynchronous hardware transfers of blocked tasks." }
              ]
            },
            {
              state: "READY",
              residence: "PHYSICAL DRAM",
              cpu: "NONE (IN QUEUE)",
              io: "COMPLETED",
              node: "node-READY",
              activePath: "path-dispatch",
              preview: "Scheduler picks PID 4092 to resume processing the read buffer",
              mechanics: "The NVMe controller asserts an interrupt line. The kernel's Interrupt Service Routine (ISR) copies data into the buffer and transitions PID 4092 back to the READY run queue.",
              rationale: "Interrupt-driven event loops eliminate busy-waiting polling, allowing the OS to wake only the exact processes whose prerequisite events have finished.",
              definitions: [
                { term: "Interrupt Service Routine (ISR)", desc: "A pre-compiled kernel handler invoked directly by hardware interrupts to service asynchronous peripheral events." },
                { term: "Asynchronous Notification", desc: "Hardware event signalling that wakes waiting tasks without demanding constant CPU polling." }
              ]
            }
          ],
          "5": [
            {
              state: "NEW",
              residence: "PHYSICAL DRAM",
              cpu: "NONE (CREATING)",
              io: "NONE",
              node: "node-NEW",
              activePath: "path-admit",
              preview: "Kernel admits initialized process into scheduler run queue",
              mechanics: "Parent process calls fork()/CreateProcess(). The OS allocates a new PCB (PID 4092), initializes virtual memory page tables, loads the binary executable header, but has not yet placed it on the run queue.",
              rationale: "Prevents half-initialized tasks from being picked by the dispatcher before address bounds and security tokens are fully established.",
              definitions: [
                { term: "Process Control Block (PCB)", desc: "The central kernel data structure holding process identification, register context, memory root pointers, and open file tables." },
                { term: "Admission Control", desc: "The policy phase governing when a newly constructed task is permitted to compete for system resources." }
              ]
            },
            {
              state: "READY",
              residence: "PHYSICAL DRAM",
              cpu: "NONE (IN QUEUE)",
              io: "NONE",
              node: "node-READY",
              activePath: "path-dispatch",
              preview: "Scheduler dispatches PID 4092 onto CPU Core 1",
              mechanics: "The process is admitted to the run queue. The scheduler selects PID 4092 and switches the MMU CR3 pointer to its page table root.",
              rationale: "Ensures uniform scheduling competition alongside other active system tasks.",
              definitions: [
                { term: "Page Table Base (CR3/TTBR0)", desc: "The hardware register storing the physical base address of the active virtual-to-physical memory mapping hierarchy." },
                { term: "Address Space Virtualization", desc: "Presenting each process with an illusion of contiguous private memory while sharing underlying physical RAM." }
              ]
            },
            {
              state: "RUNNING",
              residence: "PHYSICAL DRAM",
              cpu: "CORE 1 (EXECUTING)",
              io: "NONE",
              node: "node-RUNNING",
              activePath: "path-exit",
              preview: "Report finishes and process executes exit(0) system call",
              mechanics: "Query processes all database records, formats the text report to standard output, and executes the exit() system call.",
              rationale: "Explicit exit boundaries allow applications to signal completion and return numeric status codes to the parent process.",
              definitions: [
                { term: "exit() System Call", desc: "The termination entrypoint where an application requests kernel deallocation of its execution context." },
                { term: "Lifecycle Finalization", desc: "Structured teardown that ensures shared locks, memory, and devices are reliably recovered." }
              ]
            },
            {
              state: "TERMINATED",
              residence: "RELEASED (DRAM FREED)",
              cpu: "NONE (DEAD)",
              io: "NONE",
              node: "node-TERMINATED",
              activePath: "",
              preview: "Parent calls wait() to reap zombie PCB entry",
              mechanics: "The OS deallocates virtual address space pages, closes open file descriptors, and retains only the PCB entry (Zombie state) containing the exit status until parent reaps it.",
              rationale: "Preserves the exit return code until the creator process can collect it; prevents leaking PID table slots once wait() completes.",
              definitions: [
                { term: "Zombie / Defunct Process", desc: "A terminated process whose address space is freed but whose PCB remains to store the exit status code." },
                { term: "Parent Synchronization", desc: "Enabling ancestor tasks to verify child job success or failure before finalizing accounting records." }
              ]
            }
          ],
          "7": [
            {
              state: "RUNNING",
              residence: "PHYSICAL DRAM",
              cpu: "CORE 1 (EXECUTING)",
              io: "NONE",
              node: "node-RUNNING",
              activePath: "path-block",
              preview: "Task issues blocking I/O while system memory reaches 99% capacity",
              mechanics: "PID 4092 issues an I/O request. Simultaneously, severe system-wide memory exhaustion triggers the Medium-Term Scheduler (Swapper).",
              rationale: "Operating systems must actively protect against memory thrashing when total active working sets exceed physical RAM.",
              definitions: [
                { term: "Medium-Term Scheduler", desc: "The kernel subsystem responsible for moving entire process working sets between physical DRAM and backing storage." },
                { term: "Memory Overcommitment", desc: "Allocating more virtual memory than physically exists, relying on swapping to handle peaks." }
              ]
            },
            {
              state: "BLOCKED",
              residence: "PHYSICAL DRAM",
              cpu: "NONE (BLOCKED)",
              io: "PENDING",
              node: "node-BLOCKED",
              activePath: "path-swapout-blocked",
              preview: "Swapper selects dormant blocked task and migrates memory to disk",
              mechanics: "Because PID 4092 is blocked waiting on I/O, the swapper writes its private heap and stack pages out to the swap partition, reclaiming DRAM frames for active tasks.",
              rationale: "Swapping out a blocked process frees RAM immediately without hurting current throughput, since the task cannot execute anyway until I/O completes.",
              definitions: [
                { term: "Swap Space / Backing Store", desc: "A dedicated raw disk partition or filesystem pagefile allocated for paging out process frames." },
                { term: "Working-Set Eviction", desc: "Paging out memory of idle or waiting processes to prioritize resident space for CPU-active tasks." }
              ]
            },
            {
              state: "BLOCKED / SUSPENDED",
              residence: "SECONDARY DISK",
              cpu: "NONE (SWAPPED)",
              io: "PENDING (ON DISK)",
              node: "node-BLOCKED_SUSP",
              activePath: "path-event-disk",
              preview: "Storage I/O completes while process memory is still on disk",
              mechanics: "The storage controller asserts an interrupt signaling completion. The kernel marks the I/O as done in the PCB without paging memory back into RAM immediately.",
              rationale: "Prevents wasteful premature page-ins. The kernel simply transitions the process from Blocked/Suspended to Ready/Suspended.",
              definitions: [
                { term: "Asynchronous Event Resolution", desc: "Updating kernel PCB metadata to reflect device completion without requiring memory restoration." },
                { term: "Deferred Allocation", desc: "Avoiding expensive I/O transfers until the target resource is strictly guaranteed to run." }
              ]
            },
            {
              state: "READY / SUSPENDED",
              residence: "SECONDARY DISK",
              cpu: "NONE (READY ON DISK)",
              io: "COMPLETED",
              node: "node-READY_SUSP",
              activePath: "path-swapin-ready",
              preview: "Memory pressure eases; swapper pages working set back to DRAM",
              mechanics: "Another high-memory job terminates. The medium-term scheduler detects available physical RAM and pages PID 4092's working set back into physical DRAM.",
              rationale: "Balances memory allocation demand, moving the process to in-memory Ready so the short-term dispatcher can schedule it.",
              definitions: [
                { term: "Demand Page-In", desc: "Reading process frames back from swap disk into newly allocated physical DRAM page frames." },
                { term: "Two-Tier Scheduling", desc: "Separating long-term memory residence control from millisecond-level CPU quantum dispatching." }
              ]
            },
            {
              state: "READY",
              residence: "PHYSICAL DRAM",
              cpu: "NONE (IN QUEUE)",
              io: "COMPLETED",
              node: "node-READY",
              activePath: "path-dispatch",
              preview: "Scheduler dispatches reloaded process to complete calculation",
              mechanics: "PID 4092 is fully restored in physical RAM and queued on the active run queue.",
              rationale: "Completes the medium-term scheduling recovery loop with zero data loss or application crashes.",
              definitions: [
                { term: "Run Queue Enqueue", desc: "Appending a fully resident task structure to the active per-CPU scheduler run list." },
                { term: "Fault Transparency", desc: "Providing the application with the complete illusion of uninterrupted execution despite memory paging." }
              ]
            }
          ]
        };

        let currentModel = "3";
        let currentStep = 0;

        function refreshView() {
          const modelData = scenarios[currentModel];
          if (currentStep >= modelData.length) currentStep = 0;
          const stepData = modelData[currentStep];

          // 1. Update Telemetry
          document.getElementById("telemetry-state").textContent = stepData.state;
          document.getElementById("telemetry-residence").textContent = stepData.residence;
          document.getElementById("telemetry-cpu").textContent = stepData.cpu;
          document.getElementById("telemetry-io").textContent = stepData.io;

          // 2. Update Narrative Panes
          document.getElementById("preview-text").textContent = stepData.preview;
          document.getElementById("pane-mechanics").textContent = stepData.mechanics;
          document.getElementById("pane-rationale").textContent = stepData.rationale;

          // 3. Render Dedicated Definitions Container
          const defsContainer = document.getElementById("pane-definitions");
          defsContainer.innerHTML = "";
          stepData.definitions.forEach(item => {
            const card = document.createElement("div");
            card.style.background = "#ffffff";
            card.style.border = "1px solid #cbd5e1";
            card.style.borderRadius = "4px";
            card.style.padding = "10px 12px";
            card.innerHTML = `<div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.85rem; color: #0284c7; margin-bottom: 4px;">${item.term}</div><div style="font-size: 0.85rem; color: #475569; line-height: 1.4;">${item.desc}</div>`;
            defsContainer.appendChild(card);
          });

          // 4. Update Model Specific Elements Visibility
          const is7 = currentModel === "7";
          const is5or7 = currentModel === "5" || currentModel === "7";

          document.getElementById("disk-zone").style.display = is7 ? "block" : "none";
          document.getElementById("disk-label").style.display = is7 ? "block" : "none";
          document.getElementById("node-NEW").style.display = is5or7 ? "block" : "none";
          document.getElementById("node-TERMINATED").style.display = is5or7 ? "block" : "none";
          document.getElementById("path-admit").style.display = is5or7 ? "block" : "none";
          document.getElementById("path-exit").style.display = is5or7 ? "block" : "none";

          document.getElementById("node-READY_SUSP").style.display = is7 ? "block" : "none";
          document.getElementById("node-BLOCKED_SUSP").style.display = is7 ? "block" : "none";
          document.getElementById("path-swapout-ready").style.display = is7 ? "block" : "none";
          document.getElementById("path-swapin-ready").style.display = is7 ? "block" : "none";
          document.getElementById("path-swapout-blocked").style.display = is7 ? "block" : "none";
          document.getElementById("path-swapin-blocked").style.display = is7 ? "block" : "none";
          document.getElementById("path-event-disk").style.display = is7 ? "block" : "none";

          // 5. Highlight Active Node
          const allNodes = ["node-NEW", "node-READY", "node-RUNNING", "node-BLOCKED", "node-TERMINATED", "node-READY_SUSP", "node-BLOCKED_SUSP"];
          allNodes.forEach(nid => {
            const el = document.getElementById(nid);
            if (el) {
              const circle = el.querySelector("circle");
              if (circle) {
                circle.removeAttribute("filter");
                circle.style.strokeWidth = "2px";
              }
            }
          });

          const activeNodeEl = document.getElementById(stepData.node);
          if (activeNodeEl) {
            const circle = activeNodeEl.querySelector("circle");
            if (circle) {
              circle.setAttribute("filter", "url(#active-glow)");
              circle.style.strokeWidth = "3.5px";
            }
          }

          // 6. Highlight Active Transition Path & Marker
          const allPaths = [
            "path-admit", "path-dispatch", "path-preempt", "path-block", "path-event", "path-exit",
            "path-swapout-ready", "path-swapin-ready", "path-swapout-blocked", "path-swapin-blocked", "path-event-disk"
          ];
          allPaths.forEach(pid => {
            const pel = document.getElementById(pid);
            if (pel) {
              pel.style.stroke = "#cbd5e1";
              pel.style.strokeWidth = "2px";
              pel.setAttribute("marker-end", "url(#step-arrow-default)");
            }
          });

          if (stepData.activePath) {
            const activePathEl = document.getElementById(stepData.activePath);
            if (activePathEl) {
              activePathEl.style.stroke = "#0284c7";
              activePathEl.style.strokeWidth = "3.5px";
              activePathEl.setAttribute("marker-end", "url(#step-arrow-active)");
            }
          }
        }

        // Event Listeners for Model Toggles
        document.querySelectorAll(".model-toggle").forEach(btn => {
          btn.addEventListener("click", function() {
            document.querySelectorAll(".model-toggle").forEach(b => {
              b.style.background = "#ffffff";
              b.style.color = "#475569";
              b.style.borderColor = "#cbd5e1";
            });
            this.style.background = "#0284c7";
            this.style.color = "#ffffff";
            this.style.borderColor = "#0284c7";
            currentModel = this.getAttribute("data-model");
            currentStep = 0;
            refreshView();
          });
        });

        // Navigation Stepper Buttons
        document.getElementById("btn-next-step").addEventListener("click", function() {
          currentStep = (currentStep + 1) % scenarios[currentModel].length;
          refreshView();
        });

        document.getElementById("btn-prev-step").addEventListener("click", function() {
          currentStep = (currentStep - 1 + scenarios[currentModel].length) % scenarios[currentModel].length;
          refreshView();
        });

        document.getElementById("btn-reset-step").addEventListener("click", function() {
          currentStep = 0;
          refreshView();
        });

        // Initial render
        refreshView();
      })();
    </script>
"""

def apply_definitions_layout_fix():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- INTERACTIVE PEDAGOGICAL AID: DIRECTED NARRATIVE STEPPER -->"
    end_tag = "<h3>2. Address Spaces &amp; Virtual Memory"

    if start_tag not in content or end_tag not in content:
        print("--> Error: Could not locate interactive stepper boundaries.")
        return

    part_before = content.split(start_tag)[0]
    part_after = content.split(end_tag)[1]

    updated_content = f"{part_before}{REVISED_STEPPER_BLOCK}\n\n    {end_tag}{part_after}"

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully moved contextual definitions to dedicated section in {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Move contextual definitions to dedicated section in process stepper\n\n"
            "Restructure the interactive process stepper in 03-os-concepts.html so\n"
            "that context-based definitions render in an independent full-width\n"
            "container directly beneath the paired analytical panes."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    apply_definitions_layout_fix()
