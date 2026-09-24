#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 1 in 01-race-conditions-critical-regions.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week04-concurrency-and-mutual-exclusion", "01-race-conditions-critical-regions.html")

EXPANDED_SECTION_ONE = r"""    <h3>1. The Shared State Hazard</h3>
    <p>
      In preceding modules, we explored how the operating system virtualizes physical memory to give each running program its own isolated address space. When processes run in complete isolation, one program cannot corrupt another's memory lines.
    </p>
    <p>
      However, modern operating systems are inherently collaborative and concurrent. Multi-threaded applications share a single unified address space (heap, global variables, open file descriptors), while cooperating processes frequently map shared memory segments (via POSIX <code>shmget(2)</code> or <code>mmap(2)</code>) or coordinate via kernel buffers.
    </p>
    <p>
      The moment multiple concurrent execution flows share <strong>mutable state</strong> without deterministic synchronization, the execution outcome becomes a function of physical thread interleaving, interrupt timings, and core bus arbitration. This non-deterministic vulnerability is a <strong>race condition</strong>.
    </p>

    <h4>The Classical Print Spooler Directory Hazard</h4>
    <p>
      A foundational model of race conditions is the <strong>print spooler directory</strong>:
    </p>
    <ul>
      <li>When a process wants to print a document, it enters the file name into a shared spooler directory.</li>
      <li>The spooler directory is conceptually a circular array of file slots: <code>spool_dir[0], spool_dir[1], ..., spool_dir[N-1]</code>.</li>
      <li>Two global variables coordinate access:
        <ul>
          <li><code>out</code>: points to the next file slot to be printed by the printer daemon.</li>
          <li><code>in</code>: points to the next available empty slot where a client process may deposit a file name.</li>
        </ul>
      </li>
    </ul>

    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 20px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 1.1: The Print Spooler Directory Race Condition</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">Process A and Process B read the same slot index, causing Process A to silently obliterate Process B's print job.</div>

      <svg viewBox="0 0 760 210" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="sp-arr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
          <marker id="sp-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
        </defs>

        <!-- Spooler Slots Array -->
        <g transform="translate(40, 50)">
          <!-- Slot 5 (Printed) -->
          <rect x="0" y="0" width="120" height="55" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>
          <text x="60" y="24" text-anchor="middle" font-size="9" font-weight="700" fill="#64748b">Slot 5</text>
          <text x="60" y="42" text-anchor="middle" font-family="var(--font-mono)" font-size="8.5" fill="#94a3b8">doc_old.pdf</text>

          <!-- Slot 6 (Printed) -->
          <rect x="130" y="0" width="120" height="55" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>
          <text x="190" y="24" text-anchor="middle" font-size="9" font-weight="700" fill="#64748b">Slot 6 (out)</text>
          <text x="190" y="42" text-anchor="middle" font-family="var(--font-mono)" font-size="8.5" fill="#94a3b8">report.ps</text>

          <!-- Slot 7: THE CONFLICT SLOT -->
          <rect x="260" y="0" width="150" height="55" rx="4" fill="#fef2f2" stroke="#dc2626" stroke-width="2"/>
          <text x="335" y="22" text-anchor="middle" font-size="9.5" font-weight="700" fill="#991b1b">Slot 7 (in = 7)</text>
          <text x="335" y="38" text-anchor="middle" font-family="var(--font-mono)" font-size="8" fill="#dc2626">Proc B: "thesis.pdf"</text>
          <text x="335" y="48" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#991b1b">&larr; OVERWRITTEN BY A!</text>

          <!-- Slot 8 (Empty) -->
          <rect x="420" y="0" width="120" height="55" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-dasharray="3 3"/>
          <text x="480" y="24" text-anchor="middle" font-size="9" font-weight="700" fill="#94a3b8">Slot 8 (in becomes 8)</text>
          <text x="480" y="42" text-anchor="middle" font-size="8" fill="#cbd5e1">[Unused / Skipped]</text>

          <!-- Slot 9 (Empty) -->
          <rect x="550" y="0" width="120" height="55" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-dasharray="3 3"/>
          <text x="610" y="32" text-anchor="middle" font-size="9" font-weight="700" fill="#cbd5e1">Slot 9</text>
        </g>

        <!-- Process A Vector -->
        <g transform="translate(100, 140)">
          <rect width="240" height="50" rx="4" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="12" y="20" font-size="9" font-weight="700" fill="#0369a1">Process A</text>
          <text x="12" y="34" font-family="var(--font-mono)" font-size="8" fill="#334155">1. Reads in = 7</text>
          <text x="12" y="44" font-family="var(--font-mono)" font-size="8" fill="#0284c7">3. Resumes: writes slot 7, in=8</text>
          <path d="M 170 0 C 170 -20, 260 -10, 260 -30" fill="none" stroke="#0284c7" stroke-width="1.8" marker-end="url(#sp-arr-blue)"/>
        </g>

        <!-- Process B Vector -->
        <g transform="translate(420, 140)">
          <rect width="240" height="50" rx="4" fill="#fef3c7" stroke="#d97706"/>
          <text x="12" y="20" font-size="9" font-weight="700" fill="#b45309">Process B</text>
          <text x="12" y="34" font-family="var(--font-mono)" font-size="8" fill="#334155">2. Reads in = 7, writes "thesis.pdf"</text>
          <text x="12" y="44" font-family="var(--font-mono)" font-size="8" fill="#d97706">Updates in = 8 &amp; completes</text>
          <path d="M 30 0 C 30 -20, -60 -10, -60 -30" fill="none" stroke="#dc2626" stroke-width="1.8" marker-end="url(#sp-arr)"/>
        </g>
      </svg>
    </div>

    <h5>Step-by-Step Interleaving Breakdown</h5>
    <ol>
      <li><strong>T = 0:</strong> Process <i>A</i> decides to print <code>"annual_report.pdf"</code>. It reads the shared variable <code>in</code> (which currently equals <code>7</code>) and stores <code>next_free_slot = 7</code> in its private local register.</li>
      <li><strong>T = 1 (Preemption):</strong> Before Process <i>A</i> can write its file name to <code>spool_dir[7]</code>, its time quantum expires. The kernel context-switches from Process <i>A</i> to Process <i>B</i>.</li>
      <li><strong>T = 2:</strong> Process <i>B</i> decides to print <code>"thesis.pdf"</code>. It reads the shared variable <code>in</code>, which is <em>still</em> <code>7</code> (because <i>A</i> never updated it).</li>
      <li><strong>T = 3:</strong> Process <i>B</i> writes <code>spool_dir[7] = "thesis.pdf"</code>, increments <code>in</code> from <code>7</code> to <code>8</code>, updates the shared variable in memory, and terminates its request.</li>
      <li><strong>T = 4 (The Disaster):</strong> Process <i>A</i> is rescheduled. It resumes execution right where it was paused. Its local register still holds <code>next_free_slot = 7</code>. Process <i>A</i> blindly executes <code>spool_dir[7] = "annual_report.pdf"</code>, completely <strong>overwriting Process B's file name</strong>. Process <i>A</i> then calculates <code>7 + 1 = 8</code> and writes <code>in = 8</code> back to memory.</li>
    </ol>

    <div class="math-callout">
      <strong>Operational Consequences of the Race Condition:</strong>
      <ul>
        <li><strong>Data Loss Without Warning:</strong> Process <i>B</i>'s print job is erased from existence. Neither process crashed, and no error status was returned by the kernel.</li>
        <li><strong>Permanent Deadlock / Starvation:</strong> The printer daemon reads slots up to <code>out</code>, prints Process <i>A</i>'s file at slot 7, advances to slot 8, and never sees Process <i>B</i>'s job. Process <i>B</i> sits waiting indefinitely for output that will never emerge.</li>
      </ul>
    </div>

    <h4>The Shared Bank Balance Anomaly</h4>
    <p>
      The same hazard manifests in financial transaction systems, database row updates, and operating system kernel accounting tables.
    </p>
    <p>
      Consider two concurrent threads executing in a banking daemon sharing an account variable initialized to <code>$1000</code>:
    </p>
    <ul>
      <li><strong>Thread 1 (Deposit):</strong> <code>balance += 100;</code></li>
      <li><strong>Thread 2 (Withdrawal):</strong> <code>balance -= 50;</code></li>
    </ul>
    <p>
      Under serial execution, addition and subtraction are commutative:
    </p>
    <pre><code>Balance<sub>initial</sub> = $1000
Order 1 (T1 then T2): $1000 + $100 = $1100 &rarr; $1100 &minus; $50 = <strong>$1050</strong>
Order 2 (T2 then T1): $1000 &minus; $50 = $950  &rarr; $950 + $100  = <strong>$1050</strong></code></pre>
    <p>
      Yet under concurrent multi-threaded execution, if a context switch intervenes between reading <code>balance</code> and storing the result, the ledger balance can permanently end up as <strong>$1100</strong> (the withdrawal is lost) or <strong>$950</strong> (the deposit is lost).
    </p>

    <h4>Why Compiler Optimizations Amplify the Hazard</h4>
    <p>
      A common student question is: <em>"If modern multi-core processors have gigabytes of RAM, why can't the compiler just keep shared variables synchronized automatically?"</em>
    </p>
    <p>
      Optimizing compilers make the problem <strong>significantly worse</strong> unless explicitly instructed otherwise:
    </p>
    <ul>
      <li><strong>Register Caching:</strong> Compilers assume single-threaded execution semantics (the <em>As-If rule</em>). If a loop reads a variable 1,000 times, the compiler hoists the load out of the loop and caches the value in a CPU register (like <code>%ebx</code>). Any modifications made by another core in physical RAM are completely ignored by the loop.</li>
      <li><strong>Instruction Reordering:</strong> Compilers and modern out-of-order execution pipelines reorder memory loads and stores to maximize pipeline throughput and hide memory latency. An initialization write like <code>data = 42; ready = 1;</code> may be retired by the processor as <code>ready = 1; data = 42;</code>, exposing partially constructed memory to other threads.</li>
      <li><strong>The <code>volatile</code> Misconception:</strong> In C and C++, the <code>volatile</code> keyword tells the compiler not to optimize away reads and writes to a memory location. <em>However, <code>volatile</code> does NOT provide atomic synchronization, does NOT issue CPU memory bus locks, and does NOT prevent hardware core reordering.</em> True synchronization requires mutual exclusion primitives.</li>
    </ul>"""

def update_section_one():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>1. The Shared State Hazard</h3>"
    end_marker = "<h3>2. Assembly-Level Non-Atomicity</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 1 markers.")
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
            "Expand Section 1 of Module 01 with spooler hazard and memory models\n\n"
            "Detail the classic print spooler directory race, register caching\n"
            "effects, lost update anomalies, and add an SVG spooler slot diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_one():
        run_git_sync()
