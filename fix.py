#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 2 of 01-scheduling-introduction.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week03-process-scheduling", "01-scheduling-introduction.html")

def build_expanded_content():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # The new expanded Section 2 text and SVG diagram
    new_section_two = r"""    <h3>2. The Scheduler vs. The Dispatcher</h3>
    <p>
      In operating system architecture, execution scheduling is cleanly partitioned according to the fundamental computer science principle of <strong>separating policy from mechanism</strong>:
    </p>
    <ul>
      <li><strong>Policy (The CPU Scheduler):</strong> Determines <em>which</em> task runs next and <em>for how long</em>. It is an algorithmic decision engine that balances competing performance goals (fairness, throughput, latency) by organizing processes across priority queues, computing dynamic decay factors, and maintaining run-time accounting data.</li>
      <li><strong>Mechanism (The Dispatcher):</strong> Executes <em>how</em> the selected process is loaded onto the hardware execution pipeline. It is a highly optimized, hardware-dependent assembly-language routine invoked on every context switch to alter CPU register states, switch memory mappings, and drop processor privilege levels.</li>
    </ul>

    <div style="overflow-x: auto; margin: 18px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 14px; width: 20%;">Component</th>
            <th style="padding: 10px 14px; width: 25%;">Domain &amp; Layer</th>
            <th style="padding: 10px 14px; width: 30%;">Core Responsibilities</th>
            <th style="padding: 10px 14px; width: 25%;">Execution Invariants</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700; color: #0284c7;">CPU Scheduler</td>
            <td style="padding: 10px 14px;"><strong>Policy Layer</strong><br>(Abstract algorithmic logic)</td>
            <td style="padding: 10px 14px;">
              &bull; Evaluates Ready queue state<br>
              &bull; Computes dynamic priority boosts<br>
              &bull; Decrements remaining time quantums<br>
              &bull; Selects the next <code>task_struct</code> / <code>KTHREAD</code>
            </td>
            <td style="padding: 10px 14px; color: var(--text-muted);">
              Runs inside kernel mode; may execute concurrently on multi-core systems with per-CPU runqueue spinlocks.
            </td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 14px; font-weight: 700; color: #059669;">The Dispatcher</td>
            <td style="padding: 10px 14px;"><strong>Mechanism Layer</strong><br>(Silicon-level control)</td>
            <td style="padding: 10px 14px;">
              &bull; Saves outgoing registers &amp; stack pointer<br>
              &bull; Updates MMU address mapping (CR3)<br>
              &bull; Configures hardware TLS registers<br>
              &bull; Drops privilege: Ring 0 &rarr; Ring 3
            </td>
            <td style="padding: 10px 14px; color: var(--text-muted);">
              Must execute with local interrupts disabled (CLI); must never block or page-fault during a switch.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <h4>1. Low-Level Execution Sequence of a Dispatch Cycle</h4>
    <p>
      Whenever the scheduler decides to replace Outgoing Process <i>A</i> with Incoming Process <i>B</i>, the dispatcher executes an exacting, deterministic sequence of machine-level operations:
    </p>

    <ol>
      <li>
        <strong>Interrupt Trapping &amp; Mode Transition (Ring 3 &rarr; Ring 0):</strong>
        The CPU transitions from unprivileged User Mode to supervisor Kernel Mode via a hardware interrupt (e.g., local APIC timer tick) or an explicit software trap (e.g., synchronous <code>syscall</code> instruction). The CPU hardware automatically pushes the User Stack Pointer (<code>RSP</code>), Program Counter (<code>RIP</code>), and Flags register (<code>RFLAGS</code>) onto the process's private kernel stack.
      </li>
      <li>
        <strong>Hardware Context Preservation:</strong>
        The kernel pushes all remaining general-purpose registers (RAX, RBX, RCX, RDX, RSI, RDI, RBP, R8&ndash;R15) onto the kernel stack, assembling a complete hardware trap frame (<code>struct pt_regs</code> in Linux, <code>KTRAP_FRAME</code> in Windows). The resulting stack pointer is written into Outgoing Task <i>A</i>'s Thread Control Block.
      </li>
      <li>
        <strong>Task State Accounting &amp; Scheduler Invocation:</strong>
        The kernel dispatcher records the consumed CPU cycles in Task <i>A</i>'s execution counter. If Task <i>A</i> blocked on I/O, its state is set to <code>TASK_INTERRUPTIBLE</code> and it is placed into a wait queue. If its quantum expired, its state remains <code>TASK_RUNNING</code> and it is enqueued at the tail of the Ready list. The scheduler then selects Incoming Task <i>B</i>.
      </li>
      <li>
        <strong>Virtual Memory Context Switch (MMU CR3 Reloading):</strong>
        If Task <i>B</i> belongs to a different process than Task <i>A</i>, the dispatcher reloads the CPU's <strong>CR3 control register</strong> (or <code>TTBR0</code> on ARM) with the physical base address of Task <i>B</i>'s page table root:
        <pre><code><span class="syn-cmt">/* Low-level x86-64 assembly in kernel dispatcher: */</span>
<span class="syn-fn">movq</span>  <span class="syn-var">%rax</span><span class="syn-punc">,</span> <span class="syn-var">%cr3</span>   <span class="syn-cmt">/* Loads new page table directory; invalidates non-global TLB entries */</span></code></pre>
        <em>Note on Thread Switching:</em> If Task <i>A</i> and Task <i>B</i> are two threads within the <em>same process</em>, they share the identical memory descriptor (<code>task->mm</code>). The dispatcher detects this identity and completely bypasses reloading CR3, preserving warm Translation Lookaside Buffer entries.
      </li>
      <li>
        <strong>Hardware TLS Segment Register Reconfiguration:</strong>
        The dispatcher updates the architecture-specific segment register base address pointing to the thread's user-mode Thread Control Block (writing to Model-Specific Register <code>IA32_FS_BASE</code> via <code>WRMSR</code> on Linux, or <code>IA32_GS_BASE</code> on Windows).
      </li>
      <li>
        <strong>Kernel Stack Pointer Swap (TSS Update):</strong>
        The CPU's stack pointer register (<code>RSP</code>) is updated to point to Incoming Task <i>B</i>'s saved kernel stack. Simultaneously, the kernel updates the privileged Task State Segment (TSS) so that future hardware interrupts while Task <i>B</i> runs in user mode will automatically vector to Task <i>B</i>'s kernel stack rather than Task <i>A</i>'s.
      </li>
      <li>
        <strong>Hardware Context Restoration:</strong>
        The dispatcher executes a sequence of <code>POPQ</code> assembly instructions, loading Task <i>B</i>'s saved general-purpose registers from its kernel stack back into the silicon register files.
      </li>
      <li>
        <strong>Privilege Drop and Instruction Jump (Ring 0 &rarr; Ring 3):</strong>
        The dispatcher executes the <code>IRETQ</code> (interrupt return) or <code>SYSRETQ</code> instruction. This atomically restores the user instruction pointer (<code>RIP</code>), user stack pointer (<code>RSP</code>), user execution flags (<code>RFLAGS</code>), and drops the hardware privilege level back to Ring 3. Incoming Task <i>B</i> resumes execution at the exact instruction it was executing when previously suspended.
      </li>
    </ol>

    <!-- Structural SVG Diagram: The Dispatcher Cycle -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 1.2: Anatomical Breakdown of the Scheduler &amp; Dispatcher Execution Cycle</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 16px;">Tracing the privilege transitions, policy evaluation, and silicon-level context swap between Outgoing Task A and Incoming Task B.</div>

      <svg viewBox="0 0 820 400" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="dc-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 0 2 L 8 5 L 0 8 z" fill="#0284c7" />
          </marker>
          <marker id="dc-arr-down" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 0 2 L 8 5 L 0 8 z" fill="#dc2626" />
          </marker>
          <marker id="dc-arr-up" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 0 2 L 8 5 L 0 8 z" fill="#059669" />
          </marker>
        </defs>

        <!-- USER SPACE BAND (Top) -->
        <rect x="20" y="15" width="780" height="90" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4 4" />
        <text x="35" y="38" font-size="11" font-weight="700" fill="#475569">USER MODE (Ring 3) &mdash; Applications &amp; Threads</text>

        <!-- Task A Box (Left) -->
        <g transform="translate(45, 48)">
          <rect width="190" height="46" rx="6" fill="#ffffff" stroke="#dc2626" stroke-width="2" />
          <text x="12" y="20" font-size="11" font-weight="700" fill="#0f172a">Task A (Outgoing)</text>
          <text x="12" y="35" font-family="var(--font-mono)" font-size="9" fill="#dc2626">RIP: 0x4010a2 | Ring 3</text>
        </g>

        <!-- Task B Box (Right) -->
        <g transform="translate(585, 48)">
          <rect width="190" height="46" rx="6" fill="#ffffff" stroke="#059669" stroke-width="2" />
          <text x="12" y="20" font-size="11" font-weight="700" fill="#0f172a">Task B (Incoming)</text>
          <text x="12" y="35" font-family="var(--font-mono)" font-size="9" fill="#059669">RIP: 0x4087fe | Ring 3</text>
        </g>

        <!-- KERNEL SPACE BAND (Bottom) -->
        <rect x="20" y="125" width="780" height="255" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
        <text x="35" y="148" font-size="11" font-weight="700" fill="#0f172a">KERNEL MODE (Ring 0) &mdash; Supervisor Execution</text>

        <!-- Step 1: Hardware Trap Box -->
        <g transform="translate(45, 165)">
          <rect width="210" height="90" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
          <text x="12" y="20" font-size="10" font-weight="700" fill="#dc2626">1. Trap &amp; Register Save</text>
          <rect x="10" y="28" width="190" height="24" rx="3" fill="#fef2f2" stroke="#fca5a5" />
          <text x="16" y="44" font-family="var(--font-mono)" font-size="9" fill="#b91c1c">APIC Timer Tick / Syscall</text>
          <text x="12" y="66" font-size="9" fill="#475569">&bull; Push RIP, RSP, RFLAGS</text>
          <text x="12" y="80" font-size="9" fill="#475569">&bull; Assemble struct pt_regs</text>
        </g>

        <!-- Step 2: Scheduler Policy Box -->
        <g transform="translate(300, 165)">
          <rect width="220" height="90" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2" />
          <text x="12" y="20" font-size="10" font-weight="700" fill="#0284c7">2. CPU Scheduler (Policy)</text>
          <rect x="10" y="28" width="200" height="24" rx="3" fill="#f0f9ff" stroke="#bae6fd" />
          <text x="16" y="44" font-family="var(--font-mono)" font-size="9" fill="#0369a1">pick_next_task() Evaluation</text>
          <text x="12" y="66" font-size="9" fill="#475569">&bull; Priority sorting &amp; time accounting</text>
          <text x="12" y="80" font-size="9" fill="#475569">&bull; Selects Task B from Ready queue</text>
        </g>

        <!-- Step 3: Dispatcher Mechanism Box (Lower Row) -->
        <g transform="translate(180, 275)">
          <rect width="460" height="90" rx="6" fill="#ffffff" stroke="#059669" stroke-width="2" />
          <text x="15" y="20" font-size="11" font-weight="700" fill="#059669">3. Dispatcher (Low-Level Hardware Mechanism)</text>
          <g transform="translate(15, 30)">
            <rect width="135" height="48" rx="4" fill="#f0fdf4" stroke="#86efac" />
            <text x="8" y="18" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#166534">MMU Switch</text>
            <text x="8" y="32" font-size="8" fill="#334155">Reload CR3 if process</text>
            <text x="8" y="42" font-size="8" fill="#334155">changes (TLB Flush)</text>
          </g>
          <g transform="translate(160, 30)">
            <rect width="135" height="48" rx="4" fill="#f0fdf4" stroke="#86efac" />
            <text x="8" y="18" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#166534">Kernel Stack</text>
            <text x="8" y="32" font-size="8" fill="#334155">Swap RSP to Task B;</text>
            <text x="8" y="42" font-size="8" fill="#334155">Update TSS descriptor</text>
          </g>
          <g transform="translate(305, 30)">
            <rect width="140" height="48" rx="4" fill="#f0fdf4" stroke="#86efac" />
            <text x="8" y="18" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#166534">TLS &amp; Restore</text>
            <text x="8" y="32" font-size="8" fill="#334155">Set %fs/%gs MSR;</text>
            <text x="8" y="42" font-size="8" fill="#334155">Pop general registers</text>
          </g>
        </g>

        <!-- Downward Trap Path: Task A into Kernel -->
        <path d="M 140 94 L 140 165" fill="none" stroke="#dc2626" stroke-width="2" marker-end="url(#dc-arr-down)" />
        <text x="148" y="118" font-size="9" font-weight="700" fill="#dc2626">Trap / IRQ</text>

        <!-- Step 1 to Step 2 Horizontal Connector -->
        <path d="M 255 210 L 300 210" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#dc-arr)" />

        <!-- Step 2 to Step 3 Downward Connector -->
        <path d="M 410 255 L 410 275" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#dc-arr)" />

        <!-- Upward Return Path: Step 3 into Task B -->
        <path d="M 680 275 L 680 94" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#dc-arr-up)" />
        <text x="688" y="118" font-size="9" font-weight="700" fill="#059669">IRETQ / SYSRETQ</text>
        <text x="688" y="132" font-size="8" fill="#64748b">(Ring 0 &rarr; Ring 3)</text>
      </svg>
    </div>

    <h4>2. Deconstructing Dispatch Latency: Direct vs. Indirect Costs</h4>
    <p>
      The total computational penalty incurred by a dispatch cycle is split between <strong>direct hardware overhead</strong> and <strong>indirect memory hierarchy penalties</strong>:
    </p>
    <ul>
      <li>
        <strong>Direct Dispatch Latency (1 to 3 microseconds):</strong>
        The non-negotiable instruction execution cost of saving registers to the trap frame, updating internal scheduler linked lists, executing the context switch assembly, reloading segment descriptors, and executing the privilege return instruction.
      </li>
      <li>
        <strong>Indirect Dispatch Latency (The "Invisible Tax", 10 to 50 microseconds):</strong>
        The substantial hardware performance degradation that occurs immediately after Incoming Task <i>B</i> resumes execution:
        <ul>
          <li><em>TLB Invalidation:</em> If the switch crossed process boundaries, clearing the Translation Lookaside Buffer forces subsequent memory references to execute expensive 4-level page table walks in main memory (adding ~200 CPU cycles per translation). Modern processors mitigate this using <strong>PCID (Process Context Identifiers)</strong> on x86 or <strong>ASID (Address Space Identifiers)</strong> on ARM, tagging TLB lines with process IDs to avoid full flushes.</li>
          <li><em>Hardware Cache Eviction (Cache Pollution):</em> As Task <i>B</i> runs, its memory footprints overwrite the L1 Instruction, L1 Data, and L2 caches previously warmed by Task <i>A</i>. Task <i>B</i> suffers a storm of cache misses until its active working set is fetched back from slower L3 cache or DRAM.</li>
          <li><em>Branch Target Buffer (BTB) Disruption:</em> The CPU hardware branch predictors must clear and retrain branch history patterns for the new code stream, causing repeated instruction pipeline flushes during the first several thousand instructions.</li>
        </ul>
      </li>
    </ul>"""

    # Replace the old Section 2 block cleanly
    start_tag = "<h3>2. The Scheduler vs. The Dispatcher</h3>"
    end_tag = "<h3>3. When to Schedule: Trigger Points &amp; Preemption</h3>"

    start_pos = content.find(start_tag)
    end_pos = content.find(end_tag)

    if start_pos == -1 or end_pos == -1:
        print("Error: Could not locate section markers in target file.")
        return False

    updated_content = content[:start_pos] + new_section_two + "\n\n    " + content[end_pos:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 2 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 2 in 01-scheduling-introduction.html with dispatch cycle\n\n"
            "Detail policy vs mechanism, CR3/PCID memory switching, TSS stack swaps,\n"
            "register restoration, direct/indirect latency, and add an SVG diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if build_expanded_content():
        run_git_sync()
