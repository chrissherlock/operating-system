#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 2 in 02-hardware-primitives-spinlocks.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week04-concurrency-and-mutual-exclusion",
    "02-hardware-primitives-spinlocks.html"
)

EXPANDED_SECTION_TWO = r"""    <h3>2. Peterson's Algorithm (Software-Only Coordination)</h3>
    <p>
      In the early decades of computing, hardware designers did not provide atomic instructions like Test-and-Set or Compare-and-Swap. Computer scientists were faced with a profound theoretical and engineering challenge: <em>Can provably correct mutual exclusion be achieved using only ordinary reads and writes to shared memory?</em>
    </p>

    <h4>The Evolution of Software Synchronization</h4>
    <p>
      Before Gary Peterson published his breakthrough in 1981, researchers explored several flawed software approaches:
    </p>
    <ul>
      <li>
        <strong>Attempt 1 (The Turn Variable / Strict Alternation):</strong> A single shared variable <code>turn</code> dictated who could enter. While this guaranteed mutual exclusion (Condition 1), it failed Condition 3 (Progress): if Process 0 was idle in its remainder section, Process 1 was blocked from entering even though the critical section was completely empty.
      </li>
      <li>
        <strong>Attempt 2 (State Flags Without a Turn Variable):</strong> An array <code>bool flag[2]</code> recorded intent.
        <br>
        If processes checked the flag before setting their own (<em>"If you're not in, I will go in"</em>), a context switch between the check and the set allowed both processes to enter simultaneously, violating mutual exclusion.
        <br>
        If processes set their own flag before checking their competitor's (<em>"I want in; are you in?"</em>), both could set <code>flag[0] = true</code> and <code>flag[1] = true</code> simultaneously. When both reached the while loop, each waited for the other to drop their flag, creating a permanent <strong>deadlock</strong> (or an infinite polite dance known as <strong>livelock</strong>).
      </li>
      <li>
        <strong>Dekker's Algorithm (1965):</strong> The Dutch mathematician Theodorus Dekker designed the first provably correct two-process solution. However, Dekker's algorithm was notoriously complex, requiring nested conditional loops and dynamic priority back-off logic.
      </li>
    </ul>

    <h4>Peterson's Insight (1981)</h4>
    <p>
      Gary L. Peterson published a remarkably compact two-process mutual exclusion algorithm that united the <strong>intent array</strong> (from Attempt 2) with a <strong>polite tie-breaker scalar</strong> (from Attempt 1):
    </p>

    <pre><code><span class="syn-cmt">/* Peterson's Two-Process Mutual Exclusion Algorithm */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;stdbool.h&gt;</span>

<span class="syn-kw">static volatile bool</span> flag[<span class="syn-num">2</span>] = {<span class="syn-kw">false</span>, <span class="syn-kw">false</span>}; <span class="syn-cmt">/* flag[i] == true: Process i wants to enter */</span>
<span class="syn-kw">static volatile int</span> turn = <span class="syn-num">0</span>;                  <span class="syn-cmt">/* Whose turn is it to yield in a tie? */</span>

<span class="syn-kw">void</span> enter_region(<span class="syn-kw">int</span> process) {
    <span class="syn-kw">int</span> other = <span class="syn-num">1</span> - process;     <span class="syn-cmt">/* The competing process ID (0 or 1) */</span>
    flag[process] = <span class="syn-kw">true</span>;        <span class="syn-cmt">/* 1. Declare intent to enter */</span>
    turn = other;                <span class="syn-cmt">/* 2. Politely yield tie-breaker priority to peer */</span>

    <span class="syn-cmt">/* 3. Wait while peer wants to enter AND peer holds the priority */</span>
    <span class="syn-kw">while</span> (flag[other] == <span class="syn-kw">true</span> &amp;&amp; turn == other) {
        <span class="syn-cmt">/* Busy wait (spin) */</span>
    }
}

<span class="syn-kw">void</span> leave_region(<span class="syn-kw">int</span> process) {
    flag[process] = <span class="syn-kw">false</span>;       <span class="syn-cmt">/* Withdraw intent upon exit */</span>
}</code></pre>

    <p>
      The genius of Peterson's algorithm lies in line 2: <code>turn = other;</code>. Rather than selfishly claiming <em>"It is my turn!"</em>, each process politely declares <em>"I grant you the turn!"</em>. The process that executes this assignment <strong>last</strong> overwrites the <code>turn</code> variable, effectively surrendering priority and forcing itself to wait while the earlier process proceeds into the critical region.
    </p>

    <!-- Structural Diagram: Peterson's Protocol & Memory State -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 2.2: Peterson's Tie-Breaker Arbitration Flow</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How the combination of intent flags and the polite turn variable resolves simultaneous contention.</div>

      <svg viewBox="0 0 760 210" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="pet-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="pet-arr-amber" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#d97706" />
          </marker>
          <marker id="pet-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
        </defs>

        <!-- Process 0 Column -->
        <g transform="translate(20, 15)">
          <rect width="210" height="180" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="14" y="24" font-size="10" font-weight="700" fill="#0284c7">PROCESS 0 (T0)</text>

          <rect x="12" y="36" width="186" height="38" rx="4" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="20" y="52" font-size="8" font-weight="700" fill="#0369a1">1. SET INTENT:</text>
          <text x="20" y="66" font-family="var(--font-mono)" font-size="9" fill="#0f172a">flag[0] = true</text>

          <rect x="12" y="82" width="186" height="38" rx="4" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="20" y="98" font-size="8" font-weight="700" fill="#0369a1">2. YIELD TURN (First):</text>
          <text x="20" y="112" font-family="var(--font-mono)" font-size="9" fill="#0f172a">turn = 1</text>

          <rect x="12" y="128" width="186" height="52" rx="4" fill="#dcfce7" stroke="#16a34a"/>
          <text x="20" y="146" font-size="8" font-weight="700" fill="#166534">3. TEST WHILE CONDITION:</text>
          <text x="20" y="160" font-family="var(--font-mono)" font-size="8" fill="#166534">turn == 1 is FALSE (overwritten!)</text>
          <text x="20" y="172" font-size="8" font-weight="700" fill="#059669">&check; ENTERS CRITICAL SECTION</text>
        </g>

        <!-- Shared Memory Central Panel -->
        <g transform="translate(255, 15)">
          <rect width="250" height="180" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <text x="125" y="24" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0f172a">SHARED PHYSICAL MEMORY</text>

          <!-- Flag Array Box -->
          <rect x="15" y="38" width="220" height="52" rx="4" fill="#f0f9ff" stroke="#bae6fd"/>
          <text x="24" y="54" font-size="8.5" font-weight="700" fill="#0369a1">INTENT ARRAY: flag[2]</text>
          <text x="24" y="74" font-family="var(--font-mono)" font-size="11" font-weight="700" fill="#0f172a">flag[0]=true &nbsp;|&nbsp; flag[1]=true</text>

          <!-- Turn Variable Box -->
          <rect x="15" y="98" width="220" height="82" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="24" y="116" font-size="8.5" font-weight="700" fill="#475569">TIE-BREAKER SCALAR: turn</text>
          <text x="24" y="136" font-family="var(--font-mono)" font-size="8.5" fill="#64748b">1. P0 writes: turn = 1</text>
          <text x="24" y="152" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#d97706">2. P1 writes: turn = 0 (FINAL)</text>
          <text x="24" y="170" font-size="8" font-weight="700" fill="#059669">Winner: turn == 0 forces P1 to wait!</text>
        </g>

        <!-- Process 1 Column -->
        <g transform="translate(530, 15)">
          <rect width="210" height="180" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="14" y="24" font-size="10" font-weight="700" fill="#d97706">PROCESS 1 (T1)</text>

          <rect x="12" y="36" width="186" height="38" rx="4" fill="#fef3c7" stroke="#d97706"/>
          <text x="20" y="52" font-size="8" font-weight="700" fill="#92400e">1. SET INTENT:</text>
          <text x="20" y="66" font-family="var(--font-mono)" font-size="9" fill="#0f172a">flag[1] = true</text>

          <rect x="12" y="82" width="186" height="38" rx="4" fill="#fef3c7" stroke="#d97706"/>
          <text x="20" y="98" font-size="8" font-weight="700" fill="#92400e">2. YIELD TURN (Second):</text>
          <text x="20" y="112" font-family="var(--font-mono)" font-size="9" fill="#0f172a">turn = 0</text>

          <rect x="12" y="128" width="186" height="52" rx="4" fill="#fee2e2" stroke="#dc2626"/>
          <text x="20" y="146" font-size="8" font-weight="700" fill="#991b1b">3. TEST WHILE CONDITION:</text>
          <text x="20" y="160" font-family="var(--font-mono)" font-size="8" fill="#991b1b">turn == 0 is TRUE &amp; flag[0]==true</text>
          <text x="20" y="172" font-size="8" font-weight="700" fill="#dc2626">&times; SPINS UNTIL P0 LEAVES</text>
        </g>
      </svg>
    </div>

    <h4>Formal Mathematical Proof of Correctness</h4>
    <p>
      We prove that Peterson's algorithm satisfies all criteria for mutual exclusion:
    </p>

    <h5>1. Proof of Mutual Exclusion (Safety)</h5>
    <p>
      We prove Condition 1 by contradiction. Assume both Process 0 and Process 1 are simultaneously inside their critical sections at time <i>t</i>:
    </p>
    <ul>
      <li>For Process 0 to enter, its while condition must have evaluated to false:
        <br>
        <code>flag[1] == false &nbsp;||&nbsp; turn == 0</code>
      </li>
      <li>For Process 1 to enter, its while condition must have evaluated to false:
        <br>
        <code>flag[0] == false &nbsp;||&nbsp; turn == 1</code>
      </li>
      <li>Both processes are inside the critical section, which requires that both set their intent flags: <code>flag[0] == true</code> and <code>flag[1] == true</code>. Therefore, the false conditions depend entirely on <code>turn</code>:
        <br>
        Process 0 required: <code>turn == 0</code>
        <br>
        Process 1 required: <code>turn == 1</code>
      </li>
      <li>However, <code>turn</code> is an atomic scalar in physical RAM. At any discrete instant <i>t</i>, <code>turn</code> can be either <code>0</code> or <code>1</code>; it <strong>cannot be both</strong>.</li>
      <li>Whichever process wrote to <code>turn</code> last overwrote the previous write. If Process 1 wrote <code>turn = 0</code> last, then <code>turn == 0</code>. This satisfied Process 0's entry condition while keeping Process 1 spinning in its while loop.</li>
      <li><strong>Contradiction:</strong> It is mathematically impossible for both processes to observe their exit condition simultaneously. Mutual exclusion is preserved.</li>
    </ul>

    <h5>2. Proof of Progress (Non-Interference)</h5>
    <p>
      Suppose Process 1 is in its remainder section and has no desire to enter. By definition, <code>flag[1] == false</code>.
    </p>
    <p>
      When Process 0 arrives at <code>enter_region(0)</code>, it sets <code>flag[0] = true</code> and <code>turn = 1</code>. It evaluates:
    </p>
    <pre><code><span class="syn-kw">while</span> (flag[<span class="syn-num">1</span>] == <span class="syn-kw">true</span> &amp;&amp; turn == <span class="syn-num">1</span>)</code></pre>
    <p>
      Because <code>flag[1]</code> is <code>false</code>, the compound expression evaluates to <code>false</code> immediately. Process 0 enters the critical region with <strong>zero delay</strong>. Process 1 running outside its critical section cannot block Process 0. Condition 3 is satisfied.
    </p>

    <h5>3. Proof of Bounded Waiting (Starvation Immunity)</h5>
    <p>
      Suppose Process 0 is waiting in its while loop while Process 1 is inside the critical region.
    </p>
    <p>
      When Process 1 exits, it sets <code>flag[1] = false</code> in <code>leave_region(1)</code>. This immediately unblocks Process 0, allowing it to enter.
    </p>
    <p>
      Even if Process 1 immediately loops around and attempts to re-enter, its entry protocol executes:
    </p>
    <pre><code>flag[<span class="syn-num">1</span>] = <span class="syn-kw">true</span>;
turn = <span class="syn-num">0</span>; <span class="syn-cmt">/* Process 1 yields turn to Process 0! */</span></code></pre>
    <p>
      By setting <code>turn = 0</code>, Process 1 surrenders priority. Because <code>flag[0]</code> is still <code>true</code>, Process 1 blocks on its own while loop, guaranteeing that Process 0 enters next. Process 0 can be bypassed at most <strong>once</strong>. Starvation is impossible. Condition 4 is satisfied.
    </p>

    <h4>The Modern Silicon Reality: Store Buffers &amp; Memory Fences</h4>
    <p>
      Despite its mathematical elegance, <strong>Peterson's algorithm fails completely on modern processors</strong> (x86, ARM, Apple Silicon, RISC-V) if implemented naively in C or C++.
    </p>
    <p>
      Why does a mathematically proven algorithm fail in practice? Because Peterson assumed <strong>Sequential Consistency (SC)</strong>: the hardware assumption that all reads and writes across all cores execute in the exact linear order specified by the programmer.
    </p>

    <h5>The Hardware Reordering Hazard</h5>
    <p>
      Modern CPUs achieve extraordinary performance by utilizing <strong>Store Buffers</strong> and <strong>Out-of-Order (OOO) execution</strong>:
    </p>
    <ul>
      <li>When Core 0 executes <code>flag[0] = true</code>, the write does not immediately update DRAM or even the L1 cache. It sits in Core 0's private FIFO <strong>Store Buffer</strong> to avoid stalling the CPU execution pipeline.</li>
      <li>When Core 0 proceeds to evaluate the while loop, it must read <code>flag[1]</code> from memory.</li>
      <li>To hide memory latency, the processor pipeline allows subsequent reads (Load) to bypass pending writes (Store). This hardware optimization is known as <strong>Store-Load Reordering</strong>.</li>
      <li>As a result, Core 0 reads <code>flag[1]</code> (which is still <code>false</code> in DRAM) <em>before its own write to <code>flag[0]</code> has drained to the cache!</em></li>
      <li>Simultaneously, Core 1 does the exact same thing: it reads <code>flag[0]</code> as <code>false</code> before its write to <code>flag[1]</code> drains.</li>
      <li><strong>The Crash:</strong> Both cores observe their competitor's flag as <code>false</code>, exit their while loops, and simultaneously enter the Critical Section, causing data corruption!</li>
    </ul>

    <h5>The Solution: Explicit Memory Barriers (Fences)</h5>
    <p>
      To restore correctness on modern hardware, we must insert architectural <strong>Memory Barriers</strong> (or compile with strict atomic acquire-release semantics) to force the CPU store buffer to drain before the load executes:
    </p>

    <pre><code><span class="syn-cmt">/* Correct Peterson's Algorithm on Modern Out-of-Order Silicon */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;stdatomic.h&gt;</span>

<span class="syn-kw">atomic_bool</span> flag[<span class="syn-num">2</span>];
<span class="syn-kw">atomic_int</span> turn;

<span class="syn-kw">void</span> enter_region(<span class="syn-kw">int</span> process) {
    <span class="syn-kw">int</span> other = <span class="syn-num">1</span> - process;
    <span class="syn-fn">atomic_store_explicit</span>(&amp;flag[process], <span class="syn-kw">true</span>, memory_order_relaxed);
    <span class="syn-fn">atomic_store_explicit</span>(&amp;turn, other, memory_order_relaxed);

    <span class="syn-cmt">/* Full hardware memory barrier (x86 'mfence', ARM 'dmb ish') */</span>
    <span class="syn-fn">atomic_thread_fence</span>(memory_order_seq_cst);

    <span class="syn-kw">while</span> (<span class="syn-fn">atomic_load_explicit</span>(&amp;flag[other], memory_order_relaxed) &amp;&amp;
           <span class="syn-fn">atomic_load_explicit</span>(&amp;turn, memory_order_relaxed) == other) {
        <span class="syn-cmt">/* Busy wait */</span>
    }
}

<span class="syn-kw">void</span> leave_region(<span class="syn-kw">int</span> process) {
    <span class="syn-fn">atomic_store_explicit</span>(&amp;flag[process], <span class="syn-kw">false</span>, memory_order_release);
}</code></pre>

    <p>
      The <code>memory_order_seq_cst</code> fence emits an architectural fence instruction (such as <code>mfence</code> on x86 or <code>dmb ish</code> on ARM) that stalls the core until all pending stores in the store buffer have been committed to cache and made visible to all other cores.
    </p>"""

def update_section_two():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>2. Peterson's Algorithm (Software-Only Coordination)</h3>"
    end_marker = "<h3>3. Hardware-Assisted Atomic Instructions</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 2 boundaries in Module 02.")
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
            "Expand Section 2 in Module 02 with Peterson's algorithm and memory models\n\n"
            "Detail historical software attempts, Dekker's precursor, formal proofs,\n"
            "modern store-buffer reordering hazards, and add an arbitration diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_two():
        run_git_sync()
