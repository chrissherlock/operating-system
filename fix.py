#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand Section 2 in 01-race-conditions-critical-regions.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week04-concurrency-and-mutual-exclusion", "01-race-conditions-critical-regions.html")

EXPANDED_SECTION_TWO = r"""    <h3>2. Assembly-Level Non-Atomicity</h3>
    <p>
      At the high-level language level (C, C++, Rust, Java, or Python), statements like <code>counter++</code> or <code>balance += 100</code> appear as single, indivisible operations. This syntactic simplicity fosters a dangerous cognitive trap: programmers assume that because an operation occupies a single line of code, the hardware executes it as an indivisible, atomic transaction.
    </p>
    <p>
      In physical computer hardware, this assumption is false. Central Processing Units (CPUs) do not perform arithmetic directly across silicon DRAM capacitors. Arithmetic Logic Units (ALUs) operate strictly on internal registers located within the processor core. Consequently, every mutation of shared memory requires a multi-stage <strong>Load-Modify-Store</strong> sequence.
    </p>

    <h4>The Anatomy of the Load-Modify-Store Sequence</h4>
    <p>
      When an optimizing compiler lowers <code>counter++</code> into target machine code, it decomposes the operation into three distinct assembly instructions:
    </p>

    <pre><code><span class="syn-cmt">; --- Disassembly of counter++ (x86-64 Architecture) ---</span>
<span class="syn-kw">mov</span> eax, [<span class="syn-num">0x7fff0040</span>]   <span class="syn-cmt">; 1. LOAD: Read 32 bits from shared memory address into register EAX</span>
<span class="syn-kw">add</span> eax, <span class="syn-num">1</span>              <span class="syn-cmt">; 2. MODIFY: ALU increments the private value in EAX by 1</span>
<span class="syn-kw">mov</span> [<span class="syn-num">0x7fff0040</span>], eax   <span class="syn-cmt">; 3. STORE: Write the updated EAX register back across the bus to RAM</span></code></pre>

    <p>
      Each of these three instructions executes at a distinct point in physical time:
    </p>
    <ol>
      <li><strong>The Load Phase (<code>mov eax, [addr]</code>):</strong> The CPU core issues a read request across the system interconnect. The memory controller fetches the cache line containing the target address into the core's private L1/L2 data cache, and the 32-bit integer is loaded into the general-purpose register <code>%eax</code>.</li>
      <li><strong>The Modify Phase (<code>add eax, 1</code>):</strong> The core's execution unit passes the contents of <code>%eax</code> through the ALU, computes the addition, and latches the incremented result back into <code>%eax</code>. At this instant, the updated value exists <em>only inside the core's private register</em>. Physical RAM still holds the old, unincremented value.</li>
      <li><strong>The Store Phase (<code>mov [addr], eax</code>):</strong> The core issues a write request, flushing the contents of <code>%eax</code> through its internal store buffer into the L1 cache, eventually writing it back to shared physical memory.</li>
    </ol>

    <!-- Structural Diagram: CPU Core Pipeline & Shared Memory Bus -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 20px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 1.2: Microarchitectural State During Load-Modify-Store Interleaving</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">The vulnerable window between register modification inside the core and retirement to shared RAM.</div>

      <svg viewBox="0 0 760 220" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="asm-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="asm-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
        </defs>

        <!-- CPU Core 0 Box -->
        <g transform="translate(20, 15)">
          <rect width="330" height="190" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="14" y="24" font-size="10.5" font-weight="700" fill="#0f172a">CPU CORE 0 (Thread 1 Context)</text>

          <!-- Register File -->
          <rect x="15" y="38" width="140" height="60" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="22" y="54" font-size="8.5" font-weight="700" fill="#64748b">REGISTER FILE</text>
          <text x="22" y="74" font-family="var(--font-mono)" font-size="11" font-weight="700" fill="#0284c7">%eax = 1000</text>
          <text x="22" y="88" font-size="7.5" fill="#94a3b8">Private to Core 0</text>

          <!-- ALU -->
          <polygon points="175,40 245,40 255,65 245,90 175,90 185,65" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
          <text x="215" y="68" text-anchor="middle" font-size="9" font-weight="700" fill="#0369a1">ALU (+100)</text>

          <!-- Timer Interrupt Trap -->
          <rect x="15" y="115" width="295" height="55" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
          <text x="24" y="133" font-size="9.5" font-weight="700" fill="#991b1b">&times; TIMER INTERRUPT FIRES HERE!</text>
          <text x="24" y="148" font-size="8" fill="#7f1d1d">&bull; Involuntary Context Switch triggered by Local APIC timer.</text>
          <text x="24" y="159" font-size="8" fill="#7f1d1d">&bull; EAX (1100) saved to PCB; Shared RAM remains stale at 1000!</text>
        </g>

        <!-- Interconnect Bus Vectors -->
        <g transform="translate(360, 40)">
          <!-- Load Path -->
          <line x1="85" y1="25" x2="5" y2="25" stroke="#0284c7" stroke-width="2" marker-end="url(#asm-arr-blue)"/>
          <text x="45" y="18" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#0284c7">1. LOAD (1000)</text>

          <!-- Interrupted Store Path -->
          <line x1="5" y1="90" x2="80" y2="90" stroke="#dc2626" stroke-width="2" stroke-dasharray="3 3"/>
          <text x="45" y="82" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#dc2626">3. STORE (BLOCKED)</text>
          <circle cx="85" cy="90" r="4" fill="#dc2626"/>
        </g>

        <!-- Physical Memory Box -->
        <g transform="translate(460, 15)">
          <rect width="280" height="190" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="14" y="24" font-size="10.5" font-weight="700" fill="#0284c7">SHARED PHYSICAL RAM</text>

          <!-- Address Cell -->
          <rect x="15" y="42" width="250" height="75" rx="4" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <text x="25" y="62" font-size="8.5" font-weight="700" fill="#64748b">PHYSICAL ADDRESS: 0x7FFF0040</text>
          <text x="25" y="80" font-family="var(--font-mono)" font-size="8" fill="#475569">Variable: balance</text>
          <text x="25" y="104" font-family="var(--font-mono)" font-size="18" font-weight="700" fill="#0f172a">Value: $1000</text>

          <rect x="15" y="130" width="250" height="42" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>
          <text x="25" y="148" font-size="8" font-weight="700" fill="#475569">Cache Line State: Shared</text>
          <text x="25" y="160" font-size="7.5" fill="#64748b">Vulnerable to uncoordinated reads from Core 1</text>
        </g>
      </svg>
    </div>

    <h4>Hardware Context Switching Across Instruction Boundaries</h4>
    <p>
      An operating system's preemptive scheduler uses a hardware timer (such as the x86 Local APIC timer) programmed to generate periodic interrupts at fixed frequencies (typically 100 Hz to 1000 Hz).
    </p>
    <p>
      When the timer interrupt fires, the CPU hardware completes whichever single assembly instruction is currently in-flight, saves the current Instruction Pointer (<code>%rip</code>) and Processor Flags (<code>%rflags</code>) onto the kernel stack, and transfers execution to the kernel interrupt handler.
    </p>
    <div class="math-callout">
      <strong>The Preemption Vulnerability Window:</strong>
      <br>
      The scheduler has zero knowledge of program semantics. It cannot know that instructions 1, 2, and 3 form a logically atomic transaction. If the interrupt fires:
      <ul>
        <li><strong>Between Instruction 1 and 2:</strong> <code>%eax</code> holds the old value. The thread is descheduled before the ALU can even compute the update.</li>
        <li><strong>Between Instruction 2 and 3:</strong> <code>%eax</code> holds the newly calculated value, but physical RAM has not been updated. The kernel saves <code>%eax</code> to the thread's PCB. If a second thread is dispatched and reads the same memory address, it reads the <em>stale, pre-incremented</em> value from RAM.</li>
      </ul>
    </div>

    <h4>Why Single CISC Instructions Are Still Non-Atomic</h4>
    <p>
      Students often point out that the x86 architecture features CISC instructions that operate directly on memory addresses, such as:
    </p>
    <pre><code><span class="syn-kw">add</span> dword ptr [counter], <span class="syn-num">1</span>   <span class="syn-cmt">; Single x86 instruction increments memory directly!</span></code></pre>
    <p>
      <em>Is this single instruction atomic?</em> <strong>No.</strong>
    </p>
    <p>
      Even though it appears as a single assembly line, the CPU microarchitecture decodes this instruction into multiple <strong>micro-operations (&mu;ops)</strong>:
    </p>
    <ol>
      <li><code>&mu;op 1:</code> Memory read (Load into internal micro-register).</li>
      <li><code>&mu;op 2:</code> ALU addition.</li>
      <li><code>&mu;op 3:</code> Memory write (Store).</li>
    </ol>
    <p>
      On a single-core system, a timer interrupt will not interrupt a single instruction midway through its micro-operations. <strong>However, on modern multi-core SMP systems, multiple execution cores share the same memory bus.</strong> Core 1 can execute a memory read simultaneously while Core 0 is between &mu;op 1 and &mu;op 3, reading stale data.
    </p>
    <p>
      To make even a single instruction atomic across multiple hardware cores, the instruction must be explicitly prefixed with the x86 hardware bus lock:
    </p>
    <pre><code><span class="syn-kw">lock add</span> dword ptr [counter], <span class="syn-num">1</span>   <span class="syn-cmt">; ATOMIC: Locks cache line across all CPU cores</span></code></pre>
    <p>
      The <code>lock</code> prefix asserts a hardware lock on the processor's memory cache line (via cache coherency protocols like MESI), forcing all other CPU cores to stall if they attempt to access that memory line until the entire Load-Modify-Store operation completes.
    </p>

    <h4>Atomicity vs. Memory Visibility</h4>
    <p>
      Writing correct concurrent systems requires understanding two distinct hardware properties:
    </p>
    <ul>
      <li><strong>Atomicity:</strong> Guarantees that a series of operations execute as an all-or-nothing unit. Intermediate states cannot be observed or interrupted by any concurrent thread.</li>
      <li><strong>Visibility:</strong> Guarantees that when one thread modifies shared state, the new value is immediately committed through private core store buffers and visible to caches on other physical cores (governed by <em>memory barriers</em> and <em>memory consistency models</em>).</li>
    </ul>"""

def update_section_two():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>2. Assembly-Level Non-Atomicity</h3>"
    end_marker = "<!-- Directed Narrative Stepper: Assembly Interleaving -->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 2 markers.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_TWO + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 2 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 2 in Module 01 with x86 assembly and hardware atomicity\n\n"
            "Break down Load-Modify-Store sequences, x86 lock prefix semantics, CPU\n"
            "core pipeline state during context switches, and add an ALU/bus diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_two():
        run_git_sync()
