#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand Section 4 in 02-hardware-primitives-spinlocks.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week04-concurrency-and-mutual-exclusion",
    "02-hardware-primitives-spinlocks.html"
)

EXPANDED_SECTION_FOUR = r"""    <h3>4. Spinlocks &amp; Microarchitectural Costs</h3>
    <p>
      Equipped with hardware atomic primitives like <code>TSL</code>, <code>XCHG</code>, and <code>CMPXCHG</code>, we can construct the simplest and most fundamental locking primitive in computer systems: the <strong>Spinlock</strong>.
    </p>
    <p>
      A spinlock operates on a straightforward principle: when a thread attempts to enter a critical region and discovers that the lock is already held, it does not yield the CPU or enter a sleep state. Instead, it executes an active, tight polling loop (it <em>spins</em>) repeatedly testing the lock variable until it becomes free.
    </p>

    <pre><code><span class="syn-cmt">/* Fundamental Spinlock Implementation (Test-and-Set) */</span>
<span class="syn-kw">typedef struct</span> {
    <span class="syn-kw">volatile int</span> lock; <span class="syn-cmt">/* 0 = Unlocked, 1 = Locked */</span>
} spinlock_t;

<span class="syn-kw">void</span> spin_lock(spinlock_t *sl) {
    <span class="syn-cmt">/* Atomically swap 1 into sl-&gt;lock; spin while previous value was 1 */</span>
    <span class="syn-kw">while</span> (__atomic_test_and_set(&amp;sl-&gt;lock, __ATOMIC_ACQUIRE)) {
        <span class="syn-cmt">/* Active busy-wait loop */</span>
        <span class="syn-kw">asm volatile</span>(<span class="syn-str">"pause"</span>); <span class="syn-cmt">/* Architectural spin-wait hint */</span>
    }
}

<span class="syn-kw">void</span> spin_unlock(spinlock_t *sl) {
    <span class="syn-cmt">/* Release lock with release memory ordering */</span>
    __atomic_clear(&amp;sl-&gt;lock, __ATOMIC_RELEASE);
}</code></pre>

    <h4>The Fundamental Trade-Off: Spinning vs. Blocking</h4>
    <p>
      Why would an operating system designer intentionally choose busy waiting over putting a thread to sleep? The answer lies in the microsecond latency cost of <strong>context switches</strong>:
    </p>
    <ul>
      <li>
        <strong>The Cost of Sleeping:</strong> When a thread calls a blocking synchronization primitive (like a POSIX mutex or semaphore) and goes to sleep, the kernel must execute an involuntary context switch: save CPU registers to the thread's PCB, flush hardware queues, invoke the scheduler, switch the page table base pointer (<code>CR3</code>), and warm up the cold cache on the new thread. On modern x86 hardware, a context switch consumes <strong>1,000 to 3,000 CPU cycles (&sim;1 to 3 &mu;s)</strong>.
      </li>
      <li>
        <strong>The Efficiency Threshold:</strong> Let <i>T</i><sub>cs</sub> represent the expected duration of the critical section, and let <i>T</i><sub>switch</sub> represent the round-trip latency of suspending and rescheduling a thread:
        <div class="math-callout" style="margin: 10px 0;">
          <strong>Spinning vs. Blocking Decision Invariant:</strong>
          <pre><code>If T<sub>cs</sub> &lt; 2 &times; T<sub>switch</sub> &rarr; <strong>Spinning burns fewer CPU cycles than sleeping.</strong>
If T<sub>cs</sub> &gt; 2 &times; T<sub>switch</sub> &rarr; <strong>Sleeping conserves cycles and frees the core.</strong></code></pre>
        </div>
      </li>
      <li>
        <strong>The Uniprocessor Disaster:</strong> On a single-core computer, spinning is <strong>always irrational</strong>. If Thread 0 holds the lock and Thread 1 spins on the only available CPU core, Thread 0 cannot execute to make progress or release the lock! Thread 1 burns 100% of its time slice in complete futility until the timer interrupt forces a context switch. Consequently, production OS kernels strictly disable local preemption or prohibit spinlocks on uniprocessors.
      </li>
    </ul>

    <!-- Structural Diagram: Cacheline Bouncing Storm -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 2.4: The Microarchitectural Cacheline Bouncing Storm</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How naive spinlocks flood the multi-core interconnect with MESI invalidation broadcasts, destroying bus throughput.</div>

      <svg viewBox="0 0 760 240" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="cb-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
          <marker id="cb-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
        </defs>

        <!-- Core 0 (Lock Holder) -->
        <g transform="translate(15, 20)">
          <rect width="165" height="195" rx="5" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="12" y="24" font-size="9" font-weight="700" fill="#059669">CORE 0 [Lock Holder]</text>
          <rect x="10" y="36" width="145" height="50" rx="3" fill="#dcfce7" stroke="#16a34a"/>
          <text x="20" y="54" font-size="8" font-weight="700" fill="#166534">CRITICAL SECTION</text>
          <text x="20" y="70" font-family="var(--font-mono)" font-size="8" fill="#14532d">balance += 100;</text>

          <rect x="10" y="96" width="145" height="50" rx="3" fill="#fee2e2" stroke="#dc2626"/>
          <text x="20" y="114" font-size="7.5" font-weight="700" fill="#991b1b">L1 CACHE INVAL!</text>
          <text x="20" y="130" font-size="7" fill="#7f1d1d">Stalled by peer writes</text>

          <text x="12" y="165" font-size="7.5" fill="#475569">&bull; Needs to write release</text>
          <text x="12" y="178" font-size="7.5" fill="#dc2626">&bull; Bus saturated by spinners</text>
        </g>

        <!-- Interconnect Ring / Bus (Center) -->
        <g transform="translate(195, 20)">
          <rect width="365" height="195" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <text x="182" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="#0f172a">SHARED INTERCONNECT BUS (RING / MESH)</text>

          <!-- Storm Message Box -->
          <rect x="15" y="38" width="335" height="60" rx="4" fill="#fee2e2" stroke="#dc2626"/>
          <text x="182" y="56" text-anchor="middle" font-size="8.5" font-weight="700" fill="#991b1b">&times; CACHELINE BOUNCING SATURATION</text>
          <text x="182" y="72" text-anchor="middle" font-size="7.5" fill="#7f1d1d">Every atomic XCHG broadcasts Read-For-Ownership (RFO) requests</text>
          <text x="182" y="86" text-anchor="middle" font-size="7.5" font-weight="700" fill="#dc2626">Bus Latency Jumps from 10ns &rarr; 250ns+</text>

          <!-- Invalidation Traffic Lines -->
          <line x1="30" y1="125" x2="335" y2="125" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="4 3"/>
          <text x="182" y="118" text-anchor="middle" font-family="var(--font-mono)" font-size="8" font-weight="700" fill="#dc2626">&harr; Contended 64-byte Cacheline [0x80001000] &harr;</text>

          <rect x="25" y="140" width="315" height="42" rx="3" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="35" y="156" font-size="7.5" font-weight="700" fill="#334155">MESI Coherence Overhead:</text>
          <text x="35" y="170" font-size="7.5" fill="#64748b">O(N&sup2;) bus transactions with N spinning cores!</text>
        </g>

        <!-- Core 1 & Core 2 (Spinners) -->
        <g transform="translate(575, 20)">
          <rect width="170" height="195" rx="5" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="12" y="24" font-size="9" font-weight="700" fill="#d97706">CORES 1 &amp; 2 [Spinning]</text>

          <rect x="10" y="36" width="150" height="65" rx="3" fill="#fef3c7" stroke="#d97706"/>
          <text x="18" y="52" font-size="8" font-weight="700" fill="#92400e">SPIN LOOP (Active):</text>
          <text x="18" y="66" font-family="var(--font-mono)" font-size="7.5" fill="#b45309">while (xchg(&amp;lock, 1))</text>
          <text x="18" y="80" font-size="7.5" font-weight="700" fill="#b45309">&bull; Atomic write every loop</text>
          <text x="18" y="92" font-size="7.5" font-weight="700" fill="#dc2626">&bull; Invalidates peer caches!</text>

          <rect x="10" y="112" width="150" height="70" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="18" y="128" font-size="7.5" font-weight="700" fill="#475569">Cacheline Ping-Pong:</text>
          <text x="18" y="142" font-size="7" fill="#64748b">Core 1 snatches line (M)</text>
          <text x="18" y="154" font-size="7" fill="#64748b">Core 2 snatches line (M)</text>
          <text x="18" y="168" font-size="7" fill="#dc2626">Caches thrash continuously</text>
        </g>
      </svg>
    </div>

    <h4>Microarchitectural Contention: Cacheline Bouncing</h4>
    <p>
      On modern multi-core processors, CPU cores communicate over a shared high-speed interconnect bus or mesh network using a <strong>cache coherency protocol (such as MESI or MOESI)</strong>.
    </p>
    <p>
      When a thread uses a basic Test-and-Set spinlock:
    </p>
    <ul>
      <li>Every execution of <code>xchg</code> or <code>test_and_set</code> is an <strong>atomic write</strong> operation.</li>
      <li>To perform an atomic write, the core must obtain exclusive ownership of the cache line containing <code>sl-&gt;lock</code>. The hardware sends an <strong>Invalidate Broadcast</strong> to all other cores.</li>
      <li>If 16 cores are spinning on the same lock, Core 1 claims the line and invalidates Cores 2&ndash;16. An instant later, Core 2 issues an atomic write, snatching the line and invalidating Cores 1 and 3&ndash;16.</li>
      <li><strong>The Resulting Storm:</strong> The 64-byte cache line bounces perpetually back and forth between core caches. This phenomenon&mdash;<strong>Cacheline Bouncing</strong>&mdash;completely saturates the inter-socket interconnect, creating memory bus congestion that degrades the performance of unrelated threads across the entire computer.</li>
    </ul>

    <h4>Algorithmic Optimization 1: Test-and-Test-and-Set (TTAS)</h4>
    <p>
      To eliminate the cacheline bouncing storm, computer scientists developed the <strong>Test-and-Test-and-Set (TTAS)</strong> optimization.
    </p>
    <p>
      The core insight is simple: <strong>reading memory does not invalidate other cores' caches</strong>. Under the MESI protocol, multiple cores can simultaneously hold a cache line in the <strong>Shared (S)</strong> state without issuing any bus transactions.
    </p>

    <pre><code><span class="syn-cmt">/* Optimized Test-and-Test-and-Set (TTAS) Lock */</span>
<span class="syn-kw">void</span> spin_lock_ttas(spinlock_t *sl) {
    <span class="syn-kw">while</span> (<span class="syn-num">1</span>) {
        <span class="syn-cmt">/* Phase 1: Spin locally on shared read-only cache line (ZERO bus traffic!) */</span>
        <span class="syn-kw">while</span> (sl-&gt;lock == <span class="syn-num">1</span>) {
            <span class="syn-kw">asm volatile</span>(<span class="syn-str">"pause"</span>); <span class="syn-cmt">/* De-pipeline &amp; reduce core power */</span>
        }

        <span class="syn-cmt">/* Phase 2: Attempt atomic acquisition ONLY when lock appears free */</span>
        <span class="syn-kw">if</span> (__atomic_test_and_set(&amp;sl-&gt;lock, __ATOMIC_ACQUIRE) == <span class="syn-num">0</span>) {
            <span class="syn-kw">break</span>; <span class="syn-cmt">/* Successfully acquired lock! */</span>
        }
        <span class="syn-cmt">/* If acquisition failed, loop back to read-only spinning */</span>
    }
}</code></pre>

    <p>
      In TTAS, while the lock is held, all spinning cores read from their local L1/L2 caches in the Shared state. <strong>Bus traffic drops to zero.</strong> Only when the lock holder writes <code>0</code> (unlock) is an invalidation sent, signaling the waiting cores to attempt a single atomic acquisition.
    </p>

    <h4>Algorithmic Optimization 2: The x86 PAUSE Instruction</h4>
    <p>
      Inside modern spin loops, compilers emit the architectural <code>pause</code> instruction (or <code>yield</code> on ARM). The <code>pause</code> instruction solves two critical hardware problems:
    </p>
    <ol>
      <li>
        <strong>Pipeline Flush Prevention on Loop Exit:</strong> Modern out-of-order processors aggressively speculate down the loop branch. When the lock is finally freed, the processor detects a memory order violation in its speculative load queue, forcing a massive <strong>pipeline flush</strong> that wastes &sim;40 clock cycles. The <code>pause</code> instruction introduces a brief sub-nanosecond architectural delay that prevents speculative pipeline overrun.
      </li>
      <li>
        <strong>SMT / Hyper-Threading Resource Sharing:</strong> On processors with Simultaneous Multithreading (Intel Hyper-Threading / AMD SMT), two logical threads share the execution units of a single physical core. A thread in a naked spin loop monopolizes the execution pipeline. The <code>pause</code> instruction yields core execution slots to the sibling hardware thread, allowing the thread doing real work to run faster.
      </li>
    </ol>

    <h4>Algorithmic Optimization 3: Exponential Backoff</h4>
    <p>
      When a TTAS lock is released, all spinning cores detect the free state simultaneously and rush to execute <code>atomic_test_and_set</code>. This creates a temporary <strong>Thundering Herd</strong> problem, where <i>N</i> cores flood the bus at the exact same instant.
    </p>
    <p>
      To smooth out contention, algorithms incorporate <strong>Exponential Backoff</strong>: if a thread fails an atomic acquisition, it pauses for a delay that doubles on each successive failure:
    </p>
    <pre><code><span class="syn-cmt">/* Exponential Backoff Loop */</span>
<span class="syn-kw">int</span> delay = <span class="syn-num">1</span>;
<span class="syn-kw">while</span> (atomic_acquire(&amp;lock) == FAILED) {
    <span class="syn-kw">for</span> (<span class="syn-kw">int</span> i = <span class="syn-num">0</span>; i &lt; delay; i++) {
        <span class="syn-kw">asm volatile</span>(<span class="syn-str">"pause"</span>);
    }
    <span class="syn-kw">if</span> (delay &lt; MAX_BACKOFF) delay *= <span class="syn-num">2</span>;
}</code></pre>

    <h4>Scalable Queued Spinlocks (Ticket Locks and MCS Locks)</h4>
    <p>
      Basic spinlocks have no concept of fairness. A newly arrived core might snatch a released lock immediately, while another core has been spinning for millions of cycles. This lack of FIFO ordering violates Condition 4 (Bounded Waiting) and can lead to starvation.
    </p>
    <ul>
      <li>
        <strong>Ticket Spinlocks:</strong> Analogous to taking a numbered ticket at a deli. Two counters coordinate threads: <code>next_ticket</code> (incremented atomically via <code>fetch_and_add</code>) and <code>now_serving</code>. Threads spin until <code>my_ticket == now_serving</code>. While fair and starvation-free, releasing the lock requires writing to <code>now_serving</code>, which still invalidates the cache lines of all waiting cores (<i>O(N)</i> bus traffic).
      </li>
      <li>
        <strong>MCS Locks (Mellor-Crummey and Scott) &amp; Linux qspinlocks:</strong> The ultimate evolution of the spinlock. Instead of all cores spinning on a single shared memory address, each thread allocates a node in a distributed linked list. <strong>Each core spins exclusively on its own private, local per-CPU cache line.</strong> When a thread unlocks, it modifies only the successor node's private variable. Bus traffic drops from <i>O(N)</i> to <strong><i>O(1)</i></strong>, enabling spinlocks to scale cleanly across supercomputers with thousands of cores.
      </li>
    </ul>

    <h4>The Priority Inversion Disaster</h4>
    <p>
      Spinlocks introduce a notorious systems failure when combined with priority-based preemptive scheduling: <strong>Priority Inversion</strong>.
    </p>

    <div style="background: #ffffff; border: 1px solid var(--border); border-left: 4px solid var(--danger); border-radius: 8px; padding: 18px; margin: 16px 0;">
      <div style="font-weight: 700; color: #991b1b; margin-bottom: 6px;">The Classical Mars Pathfinder / Real-Time Priority Inversion Failure:</div>
      <ol style="margin: 0; padding-left: 20px; font-size: 0.88rem; color: #334155;">
        <li>A low-priority thread <i>L</i> enters a critical region and acquires a spinlock.</li>
        <li>A high-priority thread <i>H</i> wakes up (e.g., in response to an urgent sensor interrupt). The scheduler preempts <i>L</i> and dispatches <i>H</i>.</li>
        <li>Thread <i>H</i> attempts to acquire the spinlock held by <i>L</i>. Finding it locked, <i>H</i> begins busy waiting (spinning).</li>
        <li><strong>The Inversion Trap:</strong> Because <i>H</i> has higher priority than <i>L</i>, the scheduler guarantees <i>H</i> 100% of CPU execution time. Thread <i>L</i> is never scheduled to run.</li>
        <li>Because <i>L</i> never runs, it can <strong>never finish its critical section and can never release the lock</strong>.</li>
        <li><strong>Result: Immediate System Hang.</strong> Thread <i>H</i> spins forever waiting for <i>L</i>, while <i>L</i> is prevented from running by <i>H</i>. If a medium-priority thread <i>M</i> exists, it can preempt <i>L</i> as well, delaying the high-priority task indefinitely.</li>
      </ol>
    </div>

    <p>
      <strong>The Solution:</strong> Operating systems resolve this pathology through two strict design mandates:
    </p>
    <ol>
      <li>
        <strong>Disabling Local Preemption During Spinlocks:</strong> In the Linux kernel, calling <code>spin_lock()</code> automatically increments the thread's preemption disable counter (<code>preempt_disable()</code>). The local CPU scheduler is forbidden from preempting the lock holder until <code>spin_unlock()</code> is executed.
      </li>
      <li>
        <strong>Priority Inheritance Protocol (PIP):</strong> If a high-priority thread <i>H</i> blocks on a lock held by a low-priority thread <i>L</i>, the operating system temporarily elevates <i>L</i>'s priority to match <i>H</i>'s priority. This ensures that medium-priority threads cannot preempt <i>L</i>, allowing <i>L</i> to finish its critical section rapidly, release the lock, and drop back to its original priority.
      </li>
    </ol>"""

def update_section_four():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>4. Spinlocks &amp; Microarchitectural Costs</h3>"
    end_marker = '<nav class="nav-bar" style="margin-top: 36px;'

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 4 boundaries in Module 02.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_FOUR + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 4 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 4 in Module 02 with spinlocks and microarchitectural costs\n\n"
            "Detail TTAS cache dynamics, CPU pause semantics, ticket/MCS locks,\n"
            "priority inversion failure models, and add a cacheline bouncing diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_four():
        run_git_sync()
