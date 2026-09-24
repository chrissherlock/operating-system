#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 4 in 03-semaphores-mutexes-monitors.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week04-concurrency-and-mutual-exclusion",
    "03-semaphores-mutexes-monitors.html"
)

EXPANDED_SECTION_FOUR = r"""    <h3>4. Monitors &amp; Condition Variables</h3>
    <p>
      While semaphores and futexes provide powerful low-level primitives for operating system kernels, building large-scale, correct multi-threaded applications using unstructured semaphores is notoriously error-prone.
    </p>
    <p>
      Consider the fragility of semaphore code in production systems:
    </p>
    <ul>
      <li><strong>Omission Defects:</strong> A developer who writes <code>down(&amp;mutex)</code> but omits <code>up(&amp;mutex)</code> due to an early <code>return</code> or uncaught exception leaves the critical region permanently locked, deadlocking the application.</li>
      <li><strong>Inversion Hazards:</strong> Swapping the sequence of two semaphores (e.g., acquiring a resource lock before checking buffer bounds) introduces catastrophic circular wait deadlocks.</li>
      <li><strong>Scattered Invariants:</strong> Semaphore operations are dispersed across disparate functions and files, making formal verification of program correctness nearly impossible.</li>
    </ul>
    <p>
      To resolve these architectural weaknesses, C. A. R. Hoare (1974) and Per Brinch Hansen (1975) pioneered the <strong>Monitor</strong>: a high-level programming language construct that encapsulates shared variables, access procedures, and synchronization gates into a unified, compiler-enforced boundary.
    </p>

    <h4>The Anatomy of a Monitor</h4>
    <p>
      A monitor is an object-oriented or module-level abstraction consisting of:
    </p>
    <ol>
      <li><strong>Private Shared State:</strong> Internal variables (buffers, counters, queues) that can <em>only</em> be accessed by procedures defined inside the monitor. External threads cannot read or write them directly.</li>
      <li><strong>Public Interface Procedures:</strong> Methods that external threads call to interact with the shared data.</li>
      <li>
        <strong>Compiler-Enforced Mutual Exclusion:</strong> The language compiler automatically injects synchronization guards at procedure entry and exit. <strong>At most one thread may be actively executing inside any procedure of the monitor at any given instant.</strong>
      </li>
    </ol>

    <!-- Structural Diagram: Monitor Internal Architecture -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 3.4: Internal Architecture of a Monitor with Condition Variables</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How the external entry queue, active monitor lock, and internal condition variable sleep queues coordinate threads.</div>

      <svg viewBox="0 0 760 260" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="mon-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="mon-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
          <marker id="mon-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
        </defs>

        <!-- External Entry Queue (Left) -->
        <g transform="translate(20, 20)">
          <rect width="170" height="220" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="14" y="24" font-size="9.5" font-weight="700" fill="#0f172a">EXTERNAL ENTRY QUEUE</text>
          <text x="14" y="38" font-size="7.5" fill="#64748b">Threads waiting to enter</text>

          <rect x="12" y="50" width="146" height="38" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="85" y="68" text-anchor="middle" font-size="8" font-weight="700" fill="#334155">Thread #4 (Blocked)</text>
          <text x="85" y="80" text-anchor="middle" font-size="7" fill="#64748b">Awaiting Monitor Lock</text>

          <rect x="12" y="96" width="146" height="38" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="85" y="114" text-anchor="middle" font-size="8" font-weight="700" fill="#334155">Thread #5 (Blocked)</text>
          <text x="85" y="126" text-anchor="middle" font-size="7" fill="#64748b">Awaiting Monitor Lock</text>

          <text x="14" y="160" font-size="7.5" fill="#475569">&bull; Enqueued automatically</text>
          <text x="14" y="174" font-size="7.5" fill="#475569">&bull; Mutex held by active thread</text>
        </g>

        <!-- Entry Gate Vector -->
        <line x1="190" y1="120" x2="225" y2="120" stroke="#0284c7" stroke-width="2" marker-end="url(#mon-arr-blue)"/>

        <!-- Monitor Enclosure Boundary -->
        <g transform="translate(230, 20)">
          <rect width="510" height="220" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <text x="20" y="26" font-size="11" font-weight="700" fill="#0284c7">MONITOR ENCAPSULATION BOUNDARY (Single Active Thread Invariant)</text>

          <!-- Active Execution Zone -->
          <g transform="translate(15, 40)">
            <rect width="210" height="165" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
            <text x="14" y="22" font-size="9" font-weight="700" fill="#166534">ACTIVE EXECUTION REGION</text>
            <rect x="12" y="34" width="186" height="50" rx="4" fill="#ffffff" stroke="#86efac"/>
            <text x="20" y="52" font-size="8.5" font-weight="700" fill="#15803d">Thread #1 [HOLDS LOCK]</text>
            <text x="20" y="68" font-family="var(--font-mono)" font-size="8" fill="#166534">Executing: insert_item()</text>

            <rect x="12" y="94" width="186" height="58" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
            <text x="20" y="112" font-size="7.5" font-weight="700" fill="#334155">PRIVATE MONITOR STATE:</text>
            <text x="20" y="126" font-family="var(--font-mono)" font-size="8" fill="#0284c7">int count = 100 (Full)</text>
            <text x="20" y="140" font-family="var(--font-mono)" font-size="8" fill="#64748b">buffer[0..N-1]</text>
          </g>

          <!-- Wait / Condition Variable Queues -->
          <g transform="translate(245, 40)">
            <rect width="250" height="165" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
            <text x="14" y="22" font-size="9" font-weight="700" fill="#0f172a">INTERNAL CONDITION QUEUES</text>

            <!-- Condition Variable 1 -->
            <rect x="12" y="34" width="226" height="54" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="20" y="50" font-size="8" font-weight="700" fill="#0284c7">cond_t not_full (Wait Queue)</text>
            <rect x="20" y="58" width="80" height="22" rx="3" fill="#fee2e2" stroke="#dc2626"/>
            <text x="60" y="73" text-anchor="middle" font-size="7.5" font-weight="700" fill="#991b1b">Thread #2 (Wait)</text>
            <text x="110" y="73" font-size="7" fill="#64748b">&larr; Slept on full buffer</text>

            <!-- Condition Variable 2 -->
            <rect x="12" y="98" width="226" height="54" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="20" y="114" font-size="8" font-weight="700" fill="#0284c7">cond_t not_empty (Wait Queue)</text>
            <rect x="20" y="122" width="80" height="22" rx="3" fill="#fee2e2" stroke="#dc2626"/>
            <text x="60" y="137" text-anchor="middle" font-size="7.5" font-weight="700" fill="#991b1b">Thread #3 (Wait)</text>
            <text x="110" y="137" font-size="7" fill="#64748b">&larr; Slept on empty buffer</text>
          </g>
        </g>
      </svg>
    </div>

    <h4>Condition Variables: Solving the In-Monitor Sleep Problem</h4>
    <p>
      Compiler-enforced mutual exclusion creates a critical synchronization dilemma:
    </p>
    <blockquote style="border-left: 4px solid var(--danger); padding: 8px 16px; margin: 16px 0; background: #fef2f2; color: #991b1b;">
      <strong>The In-Monitor Sleep Dilemma:</strong> If Thread 1 enters a monitor method and discovers that a necessary condition is not met (e.g., the bounded buffer is full), it cannot simply execute a standard <code>sleep()</code> system call. If Thread 1 went to sleep while holding the monitor's mutual exclusion lock, <strong>no other thread could ever enter the monitor</strong>. A consumer could never enter to extract an item, and the producer would sleep forever, freezing the application permanently.
    </blockquote>
    <p>
      To resolve this, monitors introduce <strong>Condition Variables</strong> (e.g., <code>cond_t</code> in C/POSIX, <code>Condition</code> in Java/C#):
    </p>
    <ul>
      <li><code>wait(&amp;cond, &amp;mutex)</code>: <strong>Atomically releases the monitor lock and suspends the calling thread</strong> on the condition variable's wait queue. Because the monitor lock is released, other threads can now enter the monitor to mutate state. When the sleeping thread is eventually signaled and awakened, it <strong>automatically re-acquires the monitor lock</strong> before <code>wait()</code> returns to user code.</li>
      <li><code>signal(&amp;cond)</code>: Wakes up exactly one thread waiting on the condition variable. If no threads are waiting, the signal is quietly discarded with zero side effects.</li>
      <li><code>broadcast(&amp;cond)</code>: Wakes up <em>all</em> threads currently waiting on the condition variable.</li>
    </ul>

    <div class="math-callout">
      <strong>Semaphores vs. Condition Variables &mdash; The Vital Difference:</strong>
      <br>
      A common student misconception is confusing semaphores with condition variables:
      <ul>
        <li><strong>Semaphores Have Memory:</strong> A semaphore has an internal integer counter. If an <code>up()</code> is called when no threads are waiting, the counter increments to <code>1</code>. A subsequent <code>down()</code> consumes that saved permit without sleeping.</li>
        <li><strong>Condition Variables Are Stateless:</strong> A condition variable has <strong>no integer counter and zero memory</strong>. If a thread calls <code>signal(&amp;cond)</code> when no threads are currently suspended in <code>wait()</code>, the signal vanishes completely into the ether. It does <em>not</em> save credit for a future <code>wait()</code>.</li>
      </ul>
    </div>

    <h4>Canonical Bounded-Buffer Monitor Implementation</h4>
    <p>
      Below is the classical bounded-buffer implemented via an explicit monitor pattern in C using POSIX threads:
    </p>

    <pre><code><span class="syn-cmt">/* Thread-Safe Bounded-Buffer Monitor using POSIX Threads */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;pthread.h&gt;</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;stdbool.h&gt;</span>

<span class="syn-kw">#define</span> BUFFER_SIZE <span class="syn-num">100</span>

<span class="syn-kw">typedef struct</span> {
    <span class="syn-kw">int</span> buffer[BUFFER_SIZE];
    <span class="syn-kw">int</span> count;                  <span class="syn-cmt">/* Number of populated slots */</span>
    <span class="syn-kw">int</span> head;                   <span class="syn-cmt">/* Write index pointer */</span>
    <span class="syn-kw">int</span> tail;                   <span class="syn-cmt">/* Read index pointer */</span>
    <span class="syn-kw">pthread_mutex_t</span> lock;       <span class="syn-cmt">/* Monitor entry gatekeeper */</span>
    <span class="syn-kw">pthread_cond_t</span> not_full;    <span class="syn-cmt">/* Condition: buffer has room for insert */</span>
    <span class="syn-kw">pthread_cond_t</span> not_empty;   <span class="syn-cmt">/* Condition: buffer has item for removal */</span>
} bounded_buffer_monitor_t;

<span class="syn-kw">void</span> monitor_insert(bounded_buffer_monitor_t *m, <span class="syn-kw">int</span> item) {
    <span class="syn-fn">pthread_mutex_lock</span>(&amp;m-&gt;lock); <span class="syn-cmt">/* 1. Enter Monitor (Acquire Mutex) */</span>

    <span class="syn-cmt">/* 2. Wait while condition is not met (MESA INVARIANT: while loop!) */</span>
    <span class="syn-kw">while</span> (m-&gt;count == BUFFER_SIZE) {
        <span class="syn-fn">pthread_cond_wait</span>(&amp;m-&gt;not_full, &amp;m-&gt;lock); <span class="syn-cmt">/* Releases lock &amp; sleeps */</span>
    }

    <span class="syn-cmt">/* 3. Mutate private state (Guaranteed Exclusive Access) */</span>
    m-&gt;buffer[m-&gt;head] = item;
    m-&gt;head = (m-&gt;head + <span class="syn-num">1</span>) % BUFFER_SIZE;
    m-&gt;count++;

    <span class="syn-cmt">/* 4. Signal waiting consumers that buffer is no longer empty */</span>
    <span class="syn-fn">pthread_cond_signal</span>(&amp;m-&gt;not_empty);

    <span class="syn-fn">pthread_mutex_unlock</span>(&amp;m-&gt;lock); <span class="syn-cmt">/* 5. Exit Monitor (Release Mutex) */</span>
}

<span class="syn-kw">int</span> monitor_remove(bounded_buffer_monitor_t *m) {
    <span class="syn-fn">pthread_mutex_lock</span>(&amp;m-&gt;lock); <span class="syn-cmt">/* 1. Enter Monitor */</span>

    <span class="syn-kw">while</span> (m-&gt;count == <span class="syn-num">0</span>) {
        <span class="syn-fn">pthread_cond_wait</span>(&amp;m-&gt;not_empty, &amp;m-&gt;lock);
    }

    <span class="syn-kw">int</span> item = m-&gt;buffer[m-&gt;tail];
    m-&gt;tail = (m-&gt;tail + <span class="syn-num">1</span>) % BUFFER_SIZE;
    m-&gt;count--;

    <span class="syn-fn">pthread_cond_signal</span>(&amp;m-&gt;not_full); <span class="syn-cmt">/* Signal waiting producers */</span>

    <span class="syn-fn">pthread_mutex_unlock</span>(&amp;m-&gt;lock); <span class="syn-cmt">/* Exit Monitor */</span>
    <span class="syn-kw">return</span> item;
}</code></pre>

    <h4>Signaling Semantics: Hoare vs. Mesa vs. Brinch Hansen</h4>
    <p>
      When a thread inside a monitor calls <code>signal(&amp;cond)</code> and wakes a suspended thread, a fundamental concurrency question arises: <strong>Which thread is allowed to execute next?</strong> Both the signaling thread and the awakened thread now demand access to the monitor, but the monitor invariant permits only <em>one</em> thread inside!
    </p>
    <p>
      This problem divided computer scientists into three distinct schools of monitor semantics:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; margin: 20px 0;">
      <!-- Hoare Semantics -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--accent); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Hoare Semantics</h4>
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--accent); text-transform: uppercase; margin-bottom: 8px;">Signal-and-Wait</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          The signaling thread <strong>immediately yields the monitor lock and CPU</strong> to the awakened thread.
          <br><br>
          The awakened thread runs instantaneously. Because no intervening thread could run, the predicate condition is <strong>guaranteed to be strictly true</strong>.
          <br><br>
          <em>Code Pattern:</em> Simple <code>if</code> checks are theoretically valid:
          <pre style="margin: 6px 0 0 0; padding: 6px; font-size: 0.75rem;"><code><span class="syn-kw">if</span> (count == N)
    <span class="syn-fn">wait</span>(&amp;cond);</code></pre>
          <br>
          <em>Drawback:</em> Forces two immediate, costly CPU context switches.
        </p>
      </div>

      <!-- Mesa Semantics -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Mesa Semantics</h4>
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--success); text-transform: uppercase; margin-bottom: 8px;">Signal-and-Continue</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Developed at Xerox PARC (Lampson &amp; Redell, 1980). The signaling thread <strong>retains the lock and continues running</strong> until it leaves the monitor.
          <br><br>
          The awakened thread is moved to the monitor's entry queue. When it finally reacquires the lock, <em>another thread may have sneaked in and invalidated the condition</em>!
          <br><br>
          <em>The Invariant:</em> <strong>Threads MUST re-check conditions in a <code>while</code> loop</strong>:
          <pre style="margin: 6px 0 0 0; padding: 6px; font-size: 0.75rem;"><code><span class="syn-kw">while</span> (count == N)
    <span class="syn-fn">wait</span>(&amp;cond);</code></pre>
          <br>
          <em>Standard:</em> Universal standard in POSIX (pthreads), Java, C++, and Go.
        </p>
      </div>

      <!-- Brinch Hansen -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid #7c3aed; border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Brinch Hansen</h4>
        <div style="font-size: 0.75rem; font-weight: 700; color: #7c3aed; text-transform: uppercase; margin-bottom: 8px;">Signal-and-Exit</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          A compromise design: a thread is permitted to call <code>signal()</code> <strong>only as the very final instruction</strong> before returning from the monitor procedure.
          <br><br>
          Because the signaler exits immediately, lock ownership transfers cleanly to the awakened thread without creating two active contenders.
          <br><br>
          <em>Drawback:</em> Restrictive programming model; prevents sending signals mid-calculation.
        </p>
      </div>
    </div>

    <h4>Why You Must Always Use a WHILE Loop (Spurious Wakeups)</h4>
    <p>
      In production systems programming, replacing <code>while (!condition)</code> with <code>if (!condition)</code> around a condition wait is considered a <strong>critical bug</strong>. There are three distinct engineering reasons why threads must always re-check conditions in a loop:
    </p>
    <ol>
      <li>
        <strong>Mesa Semantics (Intervening Threads):</strong> Under Mesa semantics, signaling only makes the waiter runnable. By the time the awakened thread is scheduled and regains the monitor lock, a third thread may have entered the monitor and consumed the available resource.
      </li>
      <li>
        <strong>Broadcast Waking (Thundering Herd):</strong> If a thread calls <code>pthread_cond_broadcast()</code>, multiple sleeping threads wake up. The first thread to acquire the lock claims the available slot; all subsequent threads awaken to find the condition false once again.
      </li>
      <li>
        <strong>Spurious Wakeups (Kernel Micro-architecture):</strong> Under POSIX specifications and operating system implementations (Linux, macOS, Windows), <strong>a condition variable wait can return successfully even if NO thread signaled the condition variable</strong>!
        <br>
        Spurious wakeups occur due to low-level kernel implementation constraints: OS signals (such as <code>SIGINT</code> or <code>SIGALRM</code>) interrupting a sleep primitive, multi-core cache invalidation races in the futex hash table, or context switch preemption during wait queue rebalancing.
      </li>
    </ol>
    <div class="math-callout">
      <strong>The Immutable Rule of Condition Variables:</strong>
      <pre><code><span class="syn-cmt">/* NEVER WRITE THIS (BUG): */</span>
<span class="syn-kw">if</span> (!condition_is_met) {
    <span class="syn-fn">pthread_cond_wait</span>(&amp;cond, &amp;mutex);
}

<span class="syn-cmt">/* ALWAYS WRITE THIS (CORRECT &amp; SAFE): */</span>
<span class="syn-kw">while</span> (!condition_is_met) {
    <span class="syn-fn">pthread_cond_wait</span>(&amp;cond, &amp;mutex);
}</code></pre>
    </div>"""

def update_section_four():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Ensure CSS definitions exist in <style>
    if ".syn-kw" not in content:
        style_end = content.find("</style>")
        if style_end != -1:
            content = content[:style_end] + "\n" + SYNTAX_CSS + "\n  " + content[style_end:]

    # 2. Locate Section 4 boundaries
    start_marker = "<h3>4. Monitors &amp; Condition Variables</h3>"
    end_marker = '<nav class="nav-bar" style="margin-top: 36px;'

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 4 boundaries in Module 03.")
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
            "Expand Section 4 of Module 03 with monitor mechanics and signaling models\n\n"
            "Detail Hoare vs. Mesa semantics, condition variable wait/signal atomicity,\n"
            "spurious wakeups, the while-loop invariant, and add an SVG monitor diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_four():
        run_git_sync()
