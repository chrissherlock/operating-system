#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand Section 1 in 02-hardware-primitives-spinlocks.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week04-concurrency-and-mutual-exclusion",
    "02-hardware-primitives-spinlocks.html"
)

# Syntax CSS rules to ensure colors render
SYNTAX_CSS = r"""    /* Syntax Highlighting */
    .syn-kw { color: #38bdf8; font-weight: 600; }
    .syn-fn { color: #60a5fa; font-weight: 600; }
    .syn-num { color: #f59e0b; }
    .syn-str { color: #34d399; }
    .syn-cmt { color: #64748b; font-style: italic; }"""

EXPANDED_SECTION_ONE = r"""    <h3>1. Disabling Interrupts (Hardware Masking)</h3>
    <p>
      The earliest and most straightforward technique devised to guarantee mutual exclusion on single-core computer systems was to eliminate the source of preemption at the hardware level: <strong>masking the CPU's interrupt mechanism</strong>.
    </p>
    <p>
      An operating system's scheduler cannot preempt a thread on its own initiative. The CPU is purely an instruction-execution engine; it switches control to the operating system dispatcher only when an external hardware interrupt (such as the periodic timer interrupt) or a software trap (such as a system call or page fault) forces the processor into privileged supervisor mode. If hardware interrupts are disabled, the scheduler cannot gain control of the CPU.
    </p>

    <h4>Microarchitectural Mechanics: The EFLAGS Register</h4>
    <p>
      On x86 and x86-64 architectures, maskable hardware interrupts are gated by a single bit within the CPU's architectural status register: the <strong>Interrupt Flag (<code>IF</code>)</strong>, located at bit position 9 of the <code>EFLAGS</code> / <code>RFLAGS</code> register.
    </p>
    <ul>
      <li><code>cli</code> (Clear Interrupts): Clears bit 9 (<code>IF = 0</code>). The core's execution unit ignores all signals arriving on the external <code>INTR</code> pin or from the Local Advanced Programmable Interrupt Controller (APIC).</li>
      <li><code>sti</code> (Set Interrupts): Sets bit 9 (<code>IF = 1</code>). Re-enables maskable hardware interrupts (with an architectural shadow delay of one subsequent instruction).</li>
    </ul>

    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 2.1: Hardware Interrupt Gating via the EFLAGS Register</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How the CLI instruction isolates the execution core from timer ticks, and why it fails to protect shared RAM on multi-core systems.</div>

      <svg viewBox="0 0 760 230" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="int-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="int-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
        </defs>

        <!-- CPU Core 0 -->
        <g transform="translate(20, 15)">
          <rect width="330" height="200" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="14" y="24" font-size="10.5" font-weight="700" fill="#0284c7">CPU CORE 0 (CLI Executed)</text>

          <!-- Local APIC Timer -->
          <rect x="15" y="40" width="130" height="50" rx="4" fill="#fee2e2" stroke="#dc2626"/>
          <text x="80" y="58" text-anchor="middle" font-size="8.5" font-weight="700" fill="#991b1b">LOCAL APIC TIMER</text>
          <text x="80" y="74" text-anchor="middle" font-family="var(--font-mono)" font-size="8" fill="#dc2626">1000 Hz Ticks</text>

          <!-- Gate (EFLAGS IF Bit) -->
          <rect x="180" y="40" width="130" height="50" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
          <text x="245" y="58" text-anchor="middle" font-size="8.5" font-weight="700" fill="#991b1b">EFLAGS.IF = 0</text>
          <text x="245" y="74" text-anchor="middle" font-size="8" font-weight="700" fill="#dc2626">[INTERRUPTS MASKED]</text>

          <line x1="145" y1="65" x2="175" y2="65" stroke="#dc2626" stroke-width="2" stroke-dasharray="3 3"/>
          <circle x="175" y="65" r="3" fill="#dc2626"/>

          <!-- Core Execution Unit -->
          <rect x="15" y="110" width="295" height="75" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="25" y="130" font-size="9" font-weight="700" fill="#0f172a">EXECUTION CORE (Ring 0)</text>
          <text x="25" y="148" font-family="var(--font-mono)" font-size="8.5" fill="#0284c7">cli; /* IF cleared */</text>
          <text x="25" y="162" font-family="var(--font-mono)" font-size="8.5" fill="#166534">critical_section(); /* Preemption impossible */</text>
          <text x="25" y="176" font-family="var(--font-mono)" font-size="8.5" fill="#0284c7">sti; /* IF set */</text>
        </g>

        <!-- System Bus & Memory -->
        <g transform="translate(375, 40)">
          <rect width="365" height="150" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="14" y="24" font-size="10.5" font-weight="700" fill="#0f172a">CPU CORE 1 &amp; SHARED DRAM INTERCONNECT</text>

          <!-- Core 1 -->
          <rect x="15" y="38" width="155" height="95" rx="4" fill="#fef3c7" stroke="#d97706"/>
          <text x="24" y="56" font-size="8.5" font-weight="700" fill="#92400e">CPU CORE 1 (Active)</text>
          <text x="24" y="72" font-size="7.5" fill="#78350f">EFLAGS.IF = 1 (Unchanged!)</text>
          <text x="24" y="90" font-family="var(--font-mono)" font-size="8" fill="#b45309">mov eax, [shared_mem]</text>
          <text x="24" y="104" font-size="7.5" font-weight="700" fill="#dc2626">&times; Bypasses Core 0 CLI!</text>

          <!-- Shared RAM -->
          <rect x="195" y="38" width="155" height="95" rx="4" fill="#f0f9ff" stroke="#0284c7" stroke-width="2"/>
          <text x="205" y="56" font-size="8.5" font-weight="700" fill="#0369a1">SHARED MEMORY</text>
          <text x="205" y="74" font-family="var(--font-mono)" font-size="8" fill="#64748b">Addr: 0x7FFF0040</text>
          <text x="205" y="96" font-size="8" font-weight="700" fill="#dc2626">RACE HAZARD ACTIVE</text>
          <text x="205" y="110" font-size="7.5" fill="#475569">Core 1 reads concurrently</text>
        </g>
      </svg>
    </div>

    <h4>The Reentrancy &amp; Nesting Defect (pushf / popf)</h4>
    <p>
      In production operating system kernels, synchronization functions are frequently nested. A naive implementation that simply executes <code>cli</code> on entry and <code>sti</code> on exit introduces a severe bug:
    </p>

    <pre><code><span class="syn-cmt">/* BROKEN: Naive CLI/STI Fails Under Nesting */</span>
<span class="syn-kw">void</span> update_queue() {
    <span class="syn-kw">asm volatile</span>(<span class="syn-str">"cli"</span>);     <span class="syn-cmt">/* Interrupts disabled */</span>
    <span class="syn-fn">log_event</span>();             <span class="syn-cmt">/* Calls helper function */</span>
    <span class="syn-cmt">/* BUG: Interrupts are now ENABLED here prematurely! */</span>
    queue_head = queue_head-&gt;next; <span class="syn-cmt">/* Vulnerable to preemption! */</span>
    <span class="syn-kw">asm volatile</span>(<span class="syn-str">"sti"</span>);
}

<span class="syn-kw">void</span> log_event() {
    <span class="syn-kw">asm volatile</span>(<span class="syn-str">"cli"</span>);     <span class="syn-cmt">/* Disables interrupts */</span>
    <span class="syn-fn">write_log_buffer</span>();
    <span class="syn-kw">asm volatile</span>(<span class="syn-str">"sti"</span>);     <span class="syn-cmt">/* Blindly re-enables interrupts! */</span>
}</code></pre>

    <p>
      When <code>log_event()</code> returns, it blindly executes <code>sti</code>, enabling interrupts before <code>update_queue()</code> has completed its critical queue manipulation.
    </p>
    <p>
      To support safe nesting, the kernel must <strong>save the previous interrupt flag state</strong> onto the stack before disabling interrupts, and restore the saved state upon exit:
    </p>

    <pre><code><span class="syn-cmt">/* CORRECT: Nested Interrupt Preservation (x86 pushf / popf) */</span>
<span class="syn-kw">static inline unsigned long</span> save_flags_and_cli() {
    <span class="syn-kw">unsigned long</span> flags;
    <span class="syn-kw">asm volatile</span>(
        <span class="syn-str">"pushf\n\t"</span>           <span class="syn-cmt">/* Push EFLAGS onto architectural stack */</span>
        <span class="syn-str">"pop %0\n\t"</span>          <span class="syn-cmt">/* Pop EFLAGS value into C variable 'flags' */</span>
        <span class="syn-str">"cli"</span>                 <span class="syn-cmt">/* Clear IF bit: mask interrupts */</span>
        : <span class="syn-str">"=r"</span>(flags)
        :
        : <span class="syn-str">"memory"</span>
    );
    <span class="syn-kw">return</span> flags;
}

<span class="syn-kw">static inline void</span> restore_flags(<span class="syn-kw">unsigned long</span> flags) {
    <span class="syn-kw">asm volatile</span>(
        <span class="syn-str">"push %0\n\t"</span>         <span class="syn-cmt">/* Push saved flags onto architectural stack */</span>
        <span class="syn-str">"popf"</span>                <span class="syn-cmt">/* Restore previous IF state to EFLAGS */</span>
        :
        : <span class="syn-str">"r"</span>(flags)
        : <span class="syn-str">"memory"</span>
    );
}</code></pre>

    <p>
      This matches the canonical Linux kernel pattern: <code>local_irq_save(flags)</code> and <code>local_irq_restore(flags)</code>.
    </p>

    <h4>The Two Fatal Architectural Flaws</h4>
    <p>
      Despite its elegance on simple hardware, disabling interrupts is fundamentally inadequate as a general-purpose synchronization mechanism:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <div style="background: #ffffff; border: 1px solid var(--border); border-left: 4px solid var(--danger); border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a;">1. Protection Ring Violation</h4>
        <p style="margin: 0; font-size: 0.88rem; color: #475569;">
          If user-space processes (Ring 3) were permitted to execute <code>cli</code>, an untrusted program could enter an infinite loop (<code>while(1);</code>) with interrupts masked.
          <br><br>
          Because the timer interrupt could never fire, the OS scheduler would be completely powerless to regain control. The entire physical system would freeze instantly.
          <br><br>
          Consequently, hardware architectures enforce that <code>cli</code> and <code>sti</code> are <strong>privileged instructions</strong>; attempting to execute them in user mode raises a General Protection Fault (<code>#GP(0)</code>).
        </p>
      </div>

      <div style="background: #ffffff; border: 1px solid var(--border); border-left: 4px solid var(--danger); border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a;">2. Multiprocessor (SMP) Ineffectiveness</h4>
        <p style="margin: 0; font-size: 0.88rem; color: #475569;">
          The <code>cli</code> instruction affects <strong>only the specific execution core running the instruction</strong>.
          <br><br>
          On a modern 8-core or 64-core symmetric multiprocessor (SMP), Core 0 clearing its local <code>IF</code> bit does nothing to interrupt controllers on Core 1 through Core 63.
          <br><br>
          Threads executing concurrently on other physical cores continue fetching, modifying, and retiring memory lines across the shared interconnect bus, completely bypassing the attempted lock and corrupting shared state.
        </p>
      </div>
    </div>"""

def update_section_one():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Ensure CSS definitions exist in <style>
    if ".syn-kw" not in content:
        style_end = content.find("</style>")
        if style_end != -1:
            content = content[:style_end] + "\n" + SYNTAX_CSS + "\n  " + content[style_end:]

    # 2. Locate Section 1 boundaries
    start_marker = "<h3>1. Disabling Interrupts (Hardware Masking)</h3>"
    end_marker = "<h3>2. Peterson's Algorithm (Software-Only Coordination)</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 1 boundaries in Module 02.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_ONE + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 1 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 1 in Module 02 with interrupt masking and syntax tokens\n\n"
            "Detail EFLAGS IF bit mechanics, pushf/popf nested state preservation,\n"
            "SMP core bypass failures, and add an SVG interrupt gating diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_one():
        run_git_sync()
