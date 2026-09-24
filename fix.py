#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 2 in 03-semaphores-mutexes-monitors.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week04-concurrency-and-mutual-exclusion",
    "03-semaphores-mutexes-monitors.html"
)

EXPANDED_SECTION_TWO = r"""    <h3>2. Dijkstra's Semaphores (1965)</h3>
    <p>
      In 1965, Dutch computer scientist Edsger W. Dijkstra introduced the <strong>Semaphore</strong> in his pioneering work on the THE multiprogramming system. The semaphore permanently resolved the lost wakeup problem by replacing stateless signaling pulses with an <strong>atomic integer variable coupled with a sleep queue</strong>.
    </p>
    <p>
      A semaphore is not simply a flag; it is an abstract data type with historical memory. It maintains an integer counter that records wakeups sent in the past for consumption in the future.
    </p>

    <h4>The Fundamental Atomic Primitives: P() and V()</h4>
    <p>
      In Dijkstra's original Dutch notation, the two fundamental operations were named <strong>P</strong> and <strong>V</strong>:
    </p>
    <ul>
      <li><strong>P()</strong> (from <em>proberen</em>, "to test"): Often called <code>down()</code> or <code>wait()</code>. Decrements the semaphore value and blocks the calling thread if resources are unavailable.</li>
      <li><strong>V()</strong> (from <em>verhogen</em>, "to increment"): Often called <code>up()</code>, <code>signal()</code>, or <code>post()</code>. Increments the semaphore value and wakes a sleeping thread if any are queued.</li>
    </ul>

    <!-- Structural Diagram: Internal Architecture of a Semaphore -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 3.2: Internal Microarchitecture of an Operating System Semaphore</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How an internal spinlock protects the atomic integer counter and FIFO wait queue during down() and up() calls.</div>

      <svg viewBox="0 0 760 230" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="sem-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="sem-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
        </defs>

        <!-- Outer Semaphore Struct Boundary -->
        <rect x="20" y="20" width="720" height="190" rx="8" fill="#f8fafc" stroke="#0284c7" stroke-width="2"/>
        <text x="35" y="42" font-size="11" font-weight="700" fill="#0284c7">KERNEL DATA STRUCTURE: semaphore_t (Memory Object)</text>

        <!-- Component 1: Internal Spinlock -->
        <g transform="translate(40, 60)">
          <rect width="180" height="130" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="14" y="24" font-size="9.5" font-weight="700" fill="#0f172a">INTERNAL SPINLOCK</text>
          <rect x="14" y="36" width="152" height="42" rx="4" fill="#fee2e2" stroke="#dc2626"/>
          <text x="90" y="54" text-anchor="middle" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#991b1b">spinlock_t lock</text>
          <text x="90" y="68" text-anchor="middle" font-size="7.5" fill="#7f1d1d">Protects internal state</text>
          <text x="14" y="98" font-size="7.5" fill="#475569">&bull; Held for &sim;15 ns only</text>
          <text x="14" y="112" font-size="7.5" fill="#475569">&bull; Never held across sleep</text>
        </g>

        <!-- Component 2: Atomic Integer Counter -->
        <g transform="translate(245, 60)">
          <rect width="180" height="130" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="1.5"/>
          <text x="14" y="24" font-size="9.5" font-weight="700" fill="#0284c7">ATOMIC COUNTER</text>
          <rect x="14" y="36" width="152" height="42" rx="4" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="90" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="14" font-weight="700" fill="#0369a1">int count</text>
          <text x="14" y="98" font-size="7.5" fill="#475569">&bull; If &gt; 0: Available permits</text>
          <text x="14" y="112" font-size="7.5" fill="#475569">&bull; If &lt; 0: |count| threads asleep</text>
        </g>

        <!-- Component 3: FIFO Wait Queue -->
        <g transform="translate(450, 60)">
          <rect width="270" height="130" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="14" y="24" font-size="9.5" font-weight="700" fill="#0f172a">FIFO WAIT QUEUE (Sleeping PCBs)</text>

          <!-- Queue Nodes -->
          <rect x="14" y="38" width="70" height="40" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>
          <text x="49" y="56" text-anchor="middle" font-size="8" font-weight="700" fill="#334155">PCB #102</text>
          <text x="49" y="68" text-anchor="middle" font-size="7" fill="#64748b">T_BLOCKED</text>

          <line x1="84" y1="58" x2="98" y2="58" stroke="#0284c7" stroke-width="1.5" marker-end="url(#sem-arr-blue)"/>

          <rect x="100" y="38" width="70" height="40" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>
          <text x="135" y="56" text-anchor="middle" font-size="8" font-weight="700" fill="#334155">PCB #108</text>
          <text x="135" y="68" text-anchor="middle" font-size="7" fill="#64748b">T_BLOCKED</text>

          <line x1="170" y1="58" x2="184" y2="58" stroke="#0284c7" stroke-width="1.5" marker-end="url(#sem-arr-blue)"/>

          <rect x="186" y="38" width="70" height="40" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-dasharray="3 3"/>
          <text x="221" y="62" text-anchor="middle" font-size="8" fill="#94a3b8">[Tail]</text>

          <text x="14" y="98" font-size="7.5" fill="#475569">&bull; Threads suspended by scheduler</text>
          <text x="14" y="112" font-size="7.5" fill="#059669">&bull; Woken in strict FIFO order on up()</text>
        </g>
      </svg>
    </div>

    <h4>Mathematical Models: Classical Non-Negative vs. Signed Model</h4>
    <p>
      Operating system literature and production kernels define the integer counter behavior using two mathematical conventions:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0;">
      <div style="background: #ffffff; border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a;">1. Classical Non-Negative Model</h4>
        <p style="margin: 0; font-size: 0.88rem; color: #475569;">
          In Dijkstra's original specification:
          <ul style="margin: 8px 0 0 16px; padding: 0;">
            <li>The value of <code>s</code> is <strong>never negative</strong> (<i>s &ge; 0</i>).</li>
            <li>If <i>s &gt; 0</i>, <code>down()</code> decrements <i>s</i> and proceeds.</li>
            <li>If <i>s == 0</i>, <code>down()</code> suspends the thread on the wait queue <em>without decrementing</em>.</li>
            <li>The queue length is tracked as a separate count in the wait queue list.</li>
          </ul>
        </p>
      </div>

      <div style="background: #ffffff; border: 1px solid var(--border); border-left: 4px solid var(--success); border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a;">2. Modern Signed Model (Linux / POSIX)</h4>
        <p style="margin: 0; font-size: 0.88rem; color: #475569;">
          In modern operating system kernels:
          <ul style="margin: 8px 0 0 16px; padding: 0;">
            <li>The value of <code>s</code> can become <strong>negative</strong>.</li>
            <li><code>down()</code> always decrements <i>s</i> unconditionally. If <i>s &lt; 0</i>, the thread is enqueued and blocked.</li>
            <li><strong>The Mathematical Invariant:</strong> When <i>s &lt; 0</i>, the absolute value <strong>|s|</strong> represents the <em>exact number of threads currently sleeping on the wait queue</em>.</li>
            <li><code>up()</code> increments <i>s</i>. If <i>s &le; 0</i>, at least one thread is sleeping and must be awakened.</li>
          </ul>
        </p>
      </div>
    </div>

    <h4>The Implementation Paradox: Spinlocks Inside Sleep Locks</h4>
    <p>
      Students frequently encounter a conceptual puzzle: <em>"If semaphores exist to eliminate busy waiting, how do we make the semaphore's own <code>down()</code> and <code>up()</code> routines atomic without busy waiting?"</em>
    </p>
    <p>
      The answer reveals a fundamental engineering pattern in kernel design: <strong>we use a spinlock to implement a sleep lock</strong>.
    </p>

    <pre><code><span class="syn-cmt">/* Production Kernel Semaphore Implementation */</span>
<span class="syn-kw">typedef struct</span> {
    <span class="syn-kw">spinlock_t</span> lock;            <span class="syn-cmt">/* Hardware spinlock protecting this struct */</span>
    <span class="syn-kw">int</span> count;                  <span class="syn-cmt">/* Resource permit counter */</span>
    <span class="syn-kw">struct</span> list_head wait_list; <span class="syn-cmt">/* FIFO queue of sleeping task_struct PCBs */</span>
} semaphore_t;

<span class="syn-kw">void</span> down(semaphore_t *sem) {
    <span class="syn-fn">spin_lock</span>(&amp;sem-&gt;lock);      <span class="syn-cmt">/* 1. Acquire spinlock: protect counter and list */</span>

    sem-&gt;count--;
    <span class="syn-kw">if</span> (sem-&gt;count &lt; <span class="syn-num">0</span>) {
        <span class="syn-cmt">/* 2. Enqueue calling thread into semaphore wait list */</span>
        <span class="syn-fn">enqueue_current_task</span>(&amp;sem-&gt;wait_list);
        <span class="syn-fn">set_current_task_state</span>(TASK_UNINTERRUPTIBLE);

        <span class="syn-fn">spin_unlock</span>(&amp;sem-&gt;lock);<span class="syn-cmt">/* 3. RELEASE spinlock BEFORE invoking scheduler! */</span>
        <span class="syn-fn">schedule</span>();             <span class="syn-cmt">/* 4. Voluntary context switch: thread sleeps */</span>
        <span class="syn-kw">return</span>;
    }

    <span class="syn-fn">spin_unlock</span>(&amp;sem-&gt;lock);    <span class="syn-cmt">/* Resource acquired immediately; release spinlock */</span>
}

<span class="syn-kw">void</span> up(semaphore_t *sem) {
    <span class="syn-fn">spin_lock</span>(&amp;sem-&gt;lock);      <span class="syn-cmt">/* 1. Acquire spinlock */</span>

    sem-&gt;count++;
    <span class="syn-kw">if</span> (sem-&gt;count &le; <span class="syn-num">0</span>) {
        <span class="syn-cmt">/* 2. Dequeue first sleeping thread from FIFO list */</span>
        <span class="syn-kw">struct</span> task_struct *task = <span class="syn-fn">dequeue_task</span>(&amp;sem-&gt;wait_list);
        <span class="syn-fn">wake_up_task</span>(task);     <span class="syn-cmt">/* 3. Transition PCB to TASK_RUNNING */</span>
    }

    <span class="syn-fn">spin_unlock</span>(&amp;sem-&gt;lock);    <span class="syn-cmt">/* 4. Release spinlock */</span>
}</code></pre>

    <div class="math-callout">
      <strong>Why This Does Not Re-Introduce Busy Waiting Waste:</strong>
      <br>
      The internal spinlock (<code>sem-&gt;lock</code>) is held <strong>only for the dozens of nanoseconds required to decrement an integer and insert a pointer into a linked list</strong>. It is <em>never held across the <code>schedule()</code> system call</em>.
      <br>
      Therefore, competing cores spin for at most a few dozen clock cycles, rather than spinning for milliseconds while a thread performs disk I/O.
    </div>

    <h4>Taxonomy of Semaphore Use Cases</h4>
    <p>
      Depending on initial configuration, semaphores fulfill three distinct architectural roles:
    </p>

    <h5>1. Binary Semaphores (Mutexes)</h5>
    <ul>
      <li><strong>Initialization:</strong> Initialized to <code>1</code>.</li>
      <li><strong>Behavior:</strong> Constrained to values <code>1</code> (unlocked) and <code>0</code> (locked). Ensures that only one thread can execute within a critical section at any instant.</li>
      <li>
        <strong>Critical Architectural Distinction (Binary Semaphore vs. Mutex):</strong>
        In modern systems, a true <em>Mutex</em> has <strong>ownership semantics</strong>: only the thread that called <code>lock()</code> is legally allowed to call <code>unlock()</code>. If a thread attempts to unlock a mutex it does not own, the kernel throws an exception. Furthermore, mutexes support Priority Inheritance to eliminate priority inversion.
        <br>
        In contrast, a <strong>semaphore has no concept of ownership</strong>: any thread (or even an asynchronous hardware interrupt service routine) can call <code>up()</code> to signal and release a binary semaphore.
      </li>
    </ul>

    <h5>2. Counting Semaphores (Resource Pool Management)</h5>
    <ul>
      <li><strong>Initialization:</strong> Initialized to <i>N</i>, where <i>N &gt; 1</i> represents the total number of identical units in a shared resource pool.</li>
      <li><strong>Applications:</strong> Database connection pools (e.g., maximum 50 concurrent PostgreSQL connections), DMA buffer slots, or memory allocation pools. Each <code>down()</code> allocates a permit; each <code>up()</code> returns a permit to the pool. When all permits are exhausted, subsequent requesters block automatically.</li>
    </ul>

    <h5>3. Signaling &amp; Rendezvous Semaphores</h5>
    <ul>
      <li><strong>Initialization:</strong> Initialized to <code>0</code>.</li>
      <li><strong>Applications:</strong> Enforcing strict sequential ordering between asynchronous execution flows. Thread <i>B</i> calls <code>down()</code> and blocks immediately. Thread <i>A</i> carries out hardware initialization or loads data from disk, and then executes <code>up()</code>. This guarantees that Thread <i>B</i> cannot execute its post-requisite code until Thread <i>A</i> has completed its pre-requisite code.</li>
    </ul>"""

def update_section_two():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>2. Dijkstra's Semaphores (1965)</h3>"
    end_marker = "<h3>3. Kernel Sleep Queues &amp; Linux Futexes</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 2 boundaries in Module 03.")
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
            "Expand Section 2 in Module 03 with Dijkstra semaphores and SVG diagram\n\n"
            "Detail P() and V() semantics, signed vs. non-negative counter models,\n"
            "internal spinlock implementation, and add an internal queue SVG diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_two():
        run_git_sync()
