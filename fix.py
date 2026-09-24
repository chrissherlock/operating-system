#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 3 in 03-semaphores-mutexes-monitors.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week04-concurrency-and-mutual-exclusion",
    "03-semaphores-mutexes-monitors.html"
)

EXPANDED_SECTION_THREE = r"""    <h3>3. Kernel Sleep Queues &amp; Linux Futexes</h3>
    <p>
      In Section 2, we analyzed how the operating system kernel implements semaphores and sleep locks using internal spinlocks to guard wait queues. However, that design introduces a major performance bottleneck for user-space applications: <strong>every lock acquisition and release requires a kernel system call</strong>.
    </p>
    <p>
      A system call trap instruction (<code>syscall</code> on x86-64, <code>svc</code> on ARM) forces the processor through an involuntary privilege boundary transition from Ring 3 (User Space) to Ring 0 (Kernel Mode). The CPU flushes pipeline queues, changes the stack pointer to the kernel stack, updates page-table permissions, and validates parameters. This sequence consumes <strong>100 to 300 nanoseconds</strong> per invocation.
    </p>

    <h4>The Empirical Uncontended Invariant</h4>
    <p>
      Extensive benchmarking of production software (databases, web servers, GUI toolkits) reveals a universal concurrency profile:
    </p>
    <div class="math-callout">
      <strong>The 90-99% Uncontended Rule:</strong>
      <br>
      In well-architected multi-threaded programs, <strong>over 90% to 99% of all mutex lock acquisitions encounter zero contention</strong>. The lock is free when the thread requests it, and no other thread is attempting to acquire it at that exact instant.
    </div>
    <p>
      Paying a 200 ns system call penalty millions of times per second just to set an uncontended integer flag in memory is an immense waste of CPU cycles. Conversely, relying purely on spinlocks in user space wastes entire scheduling quanta when a lock is contended.
    </p>
    <p>
      To bridge this performance divide, Rusty Russell, Ulrich Drepper, and Ingo Molnar engineered the <strong>Futex</strong> (<em>Fast Userspace Mutex</em>) for the Linux kernel.
    </p>

    <h4>The Futex Architecture: Fast-Path vs. Slow-Path</h4>
    <p>
      A futex is not an individual kernel object created with an explicit allocation API; it is an ordinary <strong>32-bit integer variable allocated directly in the application's user-space virtual memory</strong>.
    </p>
    <p>
      The core philosophy of the futex subsystem is strict separation of concerns:
    </p>
    <ol>
      <li>
        <strong>The Fast Path (Uncontended &mdash; Pure User Space):</strong>
        When a thread wants to acquire a lock, it executes an atomic Compare-and-Swap (<code>cmpxchg</code>) directly on the 32-bit integer in user memory. If the lock was free (<code>0</code>), CAS sets it to <code>1</code> (held) and returns immediately.
        <br>
        <strong>Zero system calls, zero kernel entries, executing in ~5 nanoseconds.</strong>
      </li>
      <li>
        <strong>The Slow Path (Contended &mdash; Kernel Fallback):</strong>
        Only if the atomic CAS fails (because the lock is already held) does the thread fall back to the kernel. The thread invokes the <code>futex()</code> system call, asking the kernel to suspend the calling thread on a sleep queue until the lock holder wakes it.
      </li>
      <li>
        <strong>The Unlock Path:</strong>
        When unlocking, the thread atomically decrements or clears the integer. If no other threads are waiting, the unlock finishes in user space (~5 ns). If waiting threads are detected, the thread issues a <code>futex()</code> system call instructing the kernel to wake the sleeping threads.
      </li>
    </ol>

    <!-- Structural Diagram: Futex Dual-Domain Architecture -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 3.3: The Linux Futex Dual-Domain Architecture</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How user-space atomic CAS handles uncontended paths in nanoseconds while kernel hash buckets manage sleeping threads.</div>

      <svg viewBox="0 0 760 250" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="fx-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="fx-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
          <marker id="fx-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
        </defs>

        <!-- User Space Chamber -->
        <g transform="translate(20, 15)">
          <rect width="720" height="95" rx="6" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5"/>
          <text x="16" y="22" font-size="10" font-weight="700" fill="#0284c7">RING 3: USER-SPACE VIRTUAL ADDRESS SPACE</text>

          <!-- Fast Path Box -->
          <rect x="15" y="32" width="225" height="52" rx="4" fill="#dcfce7" stroke="#16a34a"/>
          <text x="25" y="48" font-size="8" font-weight="700" fill="#166534">FAST PATH: UNCONTENDED</text>
          <text x="25" y="62" font-family="var(--font-mono)" font-size="8" fill="#14532d">atomic_cmpxchg(uaddr, 0, 1)</text>
          <text x="25" y="74" font-size="7.5" font-weight="700" fill="#059669">&#10003; 5 ns | ZERO Syscalls</text>

          <!-- Futex Memory Word -->
          <rect x="255" y="32" width="210" height="52" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
          <text x="265" y="48" font-size="8" font-weight="700" fill="#475569">USER WORD: uint32_t *uaddr</text>
          <text x="265" y="64" font-family="var(--font-mono)" font-size="11" font-weight="700" fill="#0284c7">0=Free | 1=Held | 2=Contended</text>
          <text x="265" y="76" font-size="7.5" fill="#64748b">Shared variable in user heap/mmap</text>

          <!-- Slow Path Trigger -->
          <rect x="480" y="32" width="225" height="52" rx="4" fill="#fee2e2" stroke="#dc2626"/>
          <text x="490" y="48" font-size="8" font-weight="700" fill="#991b1b">SLOW PATH: CONTENTION</text>
          <text x="490" y="62" font-family="var(--font-mono)" font-size="8" fill="#7f1d1d">syscall(SYS_futex, uaddr, ...)</text>
          <text x="490" y="74" font-size="7.5" font-weight="700" fill="#dc2626">&darr; Drops into Ring 0 Kernel</text>
        </g>

        <!-- Privilege Transition Line -->
        <line x1="20" y1="122" x2="740" y2="122" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4 4"/>
        <text x="380" y="126" text-anchor="middle" font-size="7.5" font-weight="700" fill="#64748b">PRIVILEGE BOUNDARY (syscall / sysret)</text>

        <!-- Kernel Space Chamber -->
        <g transform="translate(20, 136)">
          <rect width="720" height="100" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="16" y="20" font-size="10" font-weight="700" fill="#0f172a">RING 0: KERNEL SPACE (futex_queues Hash Buckets)</text>

          <!-- Hash Function -->
          <rect x="15" y="30" width="160" height="58" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="25" y="46" font-size="8" font-weight="700" fill="#334155">1. PIN MEMORY &amp; HASH</text>
          <text x="25" y="60" font-family="var(--font-mono)" font-size="7.5" fill="#0284c7">key = hash(phys_addr)</text>
          <text x="25" y="74" font-size="7" fill="#64748b">Locates global bucket</text>

          <line x1="175" y1="58" x2="195" y2="58" stroke="#0284c7" stroke-width="1.5" marker-end="url(#fx-arr-blue)"/>

          <!-- Hash Bucket Queue -->
          <rect x="200" y="30" width="290" height="58" rx="4" fill="#ffffff" stroke="#0284c7" stroke-width="1.5"/>
          <text x="210" y="46" font-size="8" font-weight="700" fill="#0284c7">2. BUCKET SPINLOCK &amp; QUEUE</text>
          <text x="210" y="60" font-family="var(--font-mono)" font-size="7.5" fill="#334155">spin_lock(&amp;bucket-&gt;lock);</text>
          <text x="210" y="74" font-family="var(--font-mono)" font-size="7.5" fill="#dc2626">enqueue(current); *uaddr == val check</text>

          <line x1="490" y1="58" x2="510" y2="58" stroke="#0284c7" stroke-width="1.5" marker-end="url(#fx-arr-blue)"/>

          <!-- Context Switch / Sleep -->
          <rect x="515" y="30" width="190" height="58" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="525" y="46" font-size="8" font-weight="700" fill="#334155">3. SCHEDULER</text>
          <text x="525" y="60" font-family="var(--font-mono)" font-size="7.5" fill="#0284c7">schedule();</text>
          <text x="525" y="74" font-size="7" fill="#166534">Thread enters TASK_BLOCKED</text>
        </g>
      </svg>
    </div>

    <h4>The Multiplexed System Call: FUTEX_WAIT and FUTEX_WAKE</h4>
    <p>
      The Linux kernel exposes the futex subsystem through a single multiplexed system call:
    </p>
    <pre><code><span class="syn-kw">#include</span> <span class="syn-str">&lt;linux/futex.h&gt;</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;sys/syscall.h&gt;</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;unistd.h&gt;</span>

<span class="syn-kw">long</span> syscall(SYS_futex, <span class="syn-kw">uint32_t</span> *uaddr, <span class="syn-kw">int</span> futex_op, <span class="syn-kw">uint32_t</span> val,
             <span class="syn-kw">const struct</span> timespec *timeout, <span class="syn-kw">uint32_t</span> *uaddr2, <span class="syn-kw">uint32_t</span> val3);</code></pre>

    <p>
      The two most critical operations defined by <code>futex_op</code> are:
    </p>

    <h5>1. FUTEX_WAIT: The Atomic Check-and-Sleep Primitive</h5>
    <pre><code>syscall(SYS_futex, uaddr, FUTEX_WAIT, val, timeout, NULL, <span class="syn-num">0</span>);</code></pre>
    <p>
      This command asks the kernel: <em>"If the integer at <code>*uaddr</code> still equals <code>val</code>, put my thread to sleep. If <code>*uaddr != val</code>, do not sleep; return immediately."</em>
    </p>

    <div class="math-callout">
      <strong>How FUTEX_WAIT Completely Eliminates the Lost Wakeup Defect:</strong>
      <br>
      Recall from Section 1 that primitive <code>sleep()</code> caused lost wakeups because a thread could be preempted between checking the condition and sleeping.
      <br>
      The kernel's implementation of <code>FUTEX_WAIT</code> guarantees <strong>atomicity between checking memory and sleeping</strong>:
      <ol>
        <li>The kernel pins the physical memory page backing <code>uaddr</code> and hashes the physical address to find the corresponding kernel wait bucket.</li>
        <li>The kernel acquires the bucket's internal spinlock: <code>spin_lock(&amp;bucket-&gt;lock)</code>.</li>
        <li>While holding the spinlock, the kernel dereferences <code>uaddr</code>. If another thread unlocked the mutex in user space while the calling thread was entering the kernel (such that <code>*uaddr != val</code>), the kernel <strong>aborts the sleep operation immediately</strong>, unlocks the bucket, and returns <code>-EWOULDBLOCK</code>.</li>
        <li>If and only if <code>*uaddr == val</code>, the calling thread is added to the bucket's wait queue, its state is changed to <code>TASK_INTERRUPTIBLE</code>, the bucket spinlock is released, and <code>schedule()</code> is invoked.</li>
      </ol>
      A wakeup signal can never be lost because the check and the enqueue occur atomically under the kernel bucket lock!
    </div>

    <h5>2. FUTEX_WAKE: Waking Waiters</h5>
    <pre><code>syscall(SYS_futex, uaddr, FUTEX_WAKE, val, NULL, NULL, <span class="syn-num">0</span>);</code></pre>
    <p>
      This command instructs the kernel to look up the bucket associated with <code>uaddr</code>, dequeue up to <code>val</code> threads (typically <code>val = 1</code> for mutexes, or <code>val = INT_MAX</code> for broadcast signals), and transition them to <code>TASK_RUNNING</code>.
    </p>

    <h4>Building a Minimal Production Futex Mutex</h4>
    <p>
      Using <code>FUTEX_WAIT</code> and <code>FUTEX_WAKE</code>, we can construct an industrial-grade user-space mutex using a tri-state integer protocol:
    </p>
    <ul>
      <li><code>0</code>: Lock is free (unlocked).</li>
      <li><code>1</code>: Lock is held by a thread, and <em>no other threads are waiting</em>.</li>
      <li><code>2</code>: Lock is held by a thread, and <em>one or more threads are sleeping in the kernel</em>.</li>
    </ul>

    <pre><code><span class="syn-kw">typedef struct</span> {
    <span class="syn-kw">uint32_t</span> val; <span class="syn-cmt">/* 0 = Free, 1 = Held (no waiters), 2 = Held (waiters exist) */</span>
} futex_mutex_t;

<span class="syn-kw">void</span> futex_mutex_lock(futex_mutex_t *m) {
    <span class="syn-kw">uint32_t</span> c;

    <span class="syn-cmt">/* 1. FAST PATH: Attempt to atomically transition 0 -> 1 */</span>
    <span class="syn-kw">if</span> (__atomic_compare_exchange_n(&amp;m-&gt;val, &amp;(c = <span class="syn-num">0</span>), <span class="syn-num">1</span>, <span class="syn-kw">false</span>,
                                    __ATOMIC_ACQUIRE, __ATOMIC_RELAXED)) {
        <span class="syn-kw">return</span>; <span class="syn-cmt">/* Acquired immediately in user space! ~5 ns */</span>
    }

    <span class="syn-cmt">/* 2. SLOW PATH: Contention detected */</span>
    <span class="syn-kw">do</span> {
        <span class="syn-cmt">/* If already 2, or if we transition 1 -> 2: announce waiters exist */</span>
        <span class="syn-kw">if</span> (c == <span class="syn-num">2</span> || __atomic_compare_exchange_n(&amp;m-&gt;val, &amp;(c = <span class="syn-num">1</span>), <span class="syn-num">2</span>, <span class="syn-kw">false</span>,
                                                   __ATOMIC_ACQUIRE, __ATOMIC_RELAXED)) {
            <span class="syn-cmt">/* Sleep in the kernel only if value is still 2 */</span>
            <span class="syn-fn">syscall</span>(SYS_futex, &amp;m-&gt;val, FUTEX_WAIT, <span class="syn-num">2</span>, NULL, NULL, <span class="syn-num">0</span>);
        }
        <span class="syn-cmt">/* Upon wakeup, attempt to claim the lock while setting state to 2 */</span>
    } <span class="syn-kw">while</span> (__atomic_exchange_n(&amp;m-&gt;val, <span class="syn-num">2</span>, __ATOMIC_ACQUIRE) != <span class="syn-num">0</span>);
}

<span class="syn-kw">void</span> futex_mutex_unlock(futex_mutex_t *m) {
    <span class="syn-cmt">/* 1. FAST PATH: If value was 1, no waiters exist. Atomically set to 0 */</span>
    <span class="syn-kw">if</span> (__atomic_exchange_n(&amp;m-&gt;val, <span class="syn-num">0</span>, __ATOMIC_RELEASE) == <span class="syn-num">1</span>) {
        <span class="syn-kw">return</span>; <span class="syn-cmt">/* Released in user space! Zero system calls */</span>
    }

    <span class="syn-cmt">/* 2. SLOW PATH: Value was 2 (waiters exist). Wake up 1 sleeping thread */</span>
    <span class="syn-fn">syscall</span>(SYS_futex, &amp;m-&gt;val, FUTEX_WAKE, <span class="syn-num">1</span>, NULL, NULL, <span class="syn-num">0</span>);
}</code></pre>

    <h4>Advanced Futex Primitives: Requeueing and Priority Inheritance</h4>
    <p>
      Modern implementations of <code>pthread_mutex_t</code> and <code>pthread_cond_t</code> rely on two specialized extensions to the futex system call:
    </p>

    <h5>1. The Thundering Herd &amp; FUTEX_REQUEUE</h5>
    <p>
      When multiple threads are waiting on a condition variable (e.g. <code>pthread_cond_broadcast()</code>), waking all 100 threads simultaneously causes a <strong>thundering herd storm</strong>: all 100 threads wake up, enter user space, and immediately contend for the associated mutex. Exactly one thread acquires the mutex, and the remaining 99 threads are immediately forced to issue <code>FUTEX_WAIT</code> to go back to sleep!
    </p>
    <p>
      To prevent this, Linux provides <strong><code>FUTEX_CMP_REQUEUE</code></strong>:
    </p>
    <pre><code><span class="syn-fn">syscall</span>(SYS_futex, cond_uaddr, FUTEX_CMP_REQUEUE, <span class="syn-num">1</span>, (void*)INT_MAX, mutex_uaddr, expected_val);</code></pre>
    <p>
      The kernel wakes exactly <strong>one</strong> thread on <code>cond_uaddr</code>, and directly shifts all other 99 waiting threads from the condition variable's hash bucket queue over to the mutex's hash bucket queue <em>inside the kernel without waking them into user space</em>.
    </p>

    <h5>2. Priority Inheritance Futexes (FUTEX_LOCK_PI)</h5>
    <p>
      For real-time systems vulnerable to priority inversion (as explored in Module 02), the Linux kernel provides <strong>PI-futexes</strong>:
    </p>
    <ul>
      <li>The lower 29 bits of <code>uaddr</code> store the Thread ID (TID) of the lock-owning task.</li>
      <li>If a high-priority thread blocks on <code>FUTEX_LOCK_PI</code>, the kernel inspects the TID in <code>uaddr</code> and temporarily boosts the scheduling priority of the owner task to match the waiter's priority.</li>
      <li>Once the owner releases the lock via <code>FUTEX_UNLOCK_PI</code>, the kernel drops the owner's priority back to its nominal level.</li>
    </ul>"""

def update_section_three():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Ensure CSS definitions exist in <style>
    if ".syn-kw" not in content:
        style_end = content.find("</style>")
        if style_end != -1:
            content = content[:style_end] + "\n" + SYNTAX_CSS + "\n  " + content[style_end:]

    # 2. Locate Section 3 boundaries
    start_marker = "<h3>3. Kernel Sleep Queues &amp; Linux Futexes</h3>"
    end_marker = "<!-- Interactive Aid: Linux Futex Fast-Path vs Slow-Path -->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 3 boundaries in Module 03.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_THREE + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 3 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 3 in Module 03 with Linux futex architecture and hash queues\n\n"
            "Detail fast/slow path mechanics, FUTEX_WAIT check-and-sleep validation,\n"
            "global hash bucket wait queues, FUTEX_REQUEUE, and add an SVG diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_three():
        run_git_sync()
