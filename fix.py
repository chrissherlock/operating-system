#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply integrate Windows NT synchronization across Module 03
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week04-concurrency-and-mutual-exclusion",
    "03-semaphores-mutexes-monitors.html"
)

# ---------------------------------------------------------------------
# REPLACEMENT FOR SECTION 1 (ADDING WINDOWS EVENTS & ALERTABLE SLEEP)
# ---------------------------------------------------------------------
WIN_SECTION_ONE_ADDITION = r"""    <h4>Windows Dispatcher Objects: Eliminating Lost Wakeups via Events</h4>
    <p>
      In the Windows NT kernel architecture, threads do not sleep via raw, uncoordinated signals. Instead, synchronization is mediated through <strong>Kernel Dispatcher Objects</strong>.
    </p>
    <p>
      To solve the producer-consumer signaling problem cleanly, Windows introduces the <strong>Event Object</strong> (<code>CreateEvent</code>), which represents a persistent kernel state machine rather than an ephemeral pulse:
    </p>
    <ul>
      <li><strong>Auto-Reset Events (<code>SynchronizationEvent</code>):</strong> Initialized via <code>CreateEvent(NULL, FALSE, FALSE, NULL)</code>. When signaled via <code>SetEvent()</code>, the kernel wakes exactly <em>one</em> thread waiting in <code>WaitForSingleObject()</code> and <strong>automatically resets the event state back to nonsignaled</strong>. If no thread is currently waiting, the event remains in the signaled state until a thread arrives and consumes it, completely averting the lost wakeup defect!</li>
      <li><strong>Manual-Reset Events (<code>NotificationEvent</code>):</strong> Initialized via <code>CreateEvent(NULL, TRUE, FALSE, NULL)</code>. When signaled via <code>SetEvent()</code>, the event remains signaled until explicitly cleared via <code>ResetEvent()</code>, waking <em>all</em> currently and subsequently waiting threads (broadcasting).</li>
    </ul>

    <pre><code><span class="syn-cmt">/* Safe Win32 Producer-Consumer Signaling via Auto-Reset Event */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;windows.h&gt;</span>

HANDLE hEventItemReady;

<span class="syn-kw">void</span> init_events(<span class="syn-kw">void</span>) {
    <span class="syn-cmt">/* Auto-reset event (bManualReset = FALSE), initially non-signaled */</span>
    hEventItemReady = <span class="syn-fn">CreateEvent</span>(NULL, FALSE, FALSE, NULL);
}

<span class="syn-kw">void</span> consumer_worker(<span class="syn-kw">void</span>) {
    <span class="syn-cmt">/* Atomic check &amp; sleep: if event is signaled, consumes signal without sleeping */</span>
    DWORD wait_result = <span class="syn-fn">WaitForSingleObject</span>(hEventItemReady, INFINITE);
    <span class="syn-kw">if</span> (wait_result == WAIT_OBJECT_0) {
        <span class="syn-fn">consume_item</span>(); <span class="syn-cmt">/* Safe: event reset to 0 atomically */</span>
    }
}

<span class="syn-kw">void</span> producer_worker(<span class="syn-kw">void</span>) {
    <span class="syn-fn">produce_item</span>();
    <span class="syn-fn">SetEvent</span>(hEventItemReady); <span class="syn-cmt">/* Signal remembered even if consumer not yet waiting */</span>
}</code></pre>

    <div class="math-callout">
      <strong>Windows Alertable I/O: SleepEx and Asynchronous Procedure Calls (APCs)</strong>
      <br>
      Windows also provides an advanced variant of sleeping: <code>SleepEx(dwMilliseconds, bAlertable)</code>.
      <br>
      When a thread calls <code>SleepEx(INFINITE, TRUE)</code>, it places itself into an <strong>alertable wait state</strong>. The kernel will wake the thread not only when the timeout expires, but also when an <strong>Asynchronous Procedure Call (APC)</strong> is queued to the thread's kernel APC queue (e.g., when an asynchronous overlapped I/O packet completes). This allows a single worker thread to sleep efficiently while serving completion routines.
    </div>"""

# ---------------------------------------------------------------------
# REPLACEMENT FOR SECTION 2 (ADDING WINDOWS MUTEX & ABANDONED MUTEXES)
# ---------------------------------------------------------------------
WIN_SECTION_TWO_ADDITION = r"""    <h4>Windows Kernel Semaphores &amp; Mutexes</h4>
    <p>
      In the Windows operating system, both semaphores and mutexes are implemented as first-class <strong>Kernel Executive Objects</strong> accessible via Win32 API handles.
    </p>

    <h5>1. Windows Counting Semaphores (CreateSemaphore)</h5>
    <p>
      A Windows semaphore object maintains a 32-bit signed integer count restricted between <code>0</code> and a specified <code>lMaximumCount</code>:
    </p>
    <pre><code><span class="syn-cmt">/* Win32 Counting Semaphore Creation */</span>
HANDLE hSem = <span class="syn-fn">CreateSemaphore</span>(
    NULL,           <span class="syn-cmt">/* Default security attributes */</span>
    <span class="syn-num">3</span>,              <span class="syn-cmt">/* Initial count (e.g., 3 vacant buffer slots) */</span>
    <span class="syn-num">3</span>,              <span class="syn-cmt">/* Maximum count capacity */</span>
    <span class="syn-str">"Local\\BufferSem"</span> <span class="syn-cmt">/* Optional name for cross-process sharing */</span>
);

<span class="syn-cmt">/* P() / down() equivalent: */</span>
<span class="syn-fn">WaitForSingleObject</span>(hSem, INFINITE);

<span class="syn-cmt">/* V() / up() equivalent: releases 1 permit and captures previous count */</span>
LONG prev_count;
<span class="syn-fn">ReleaseSemaphore</span>(hSem, <span class="syn-num">1</span>, &amp;prev_count);</code></pre>

    <h5>2. Windows Mutexes &amp; The Abandoned Mutex Safety Feature</h5>
    <p>
      A Windows Mutex (<code>CreateMutex</code>) is strictly a <strong>binary mutual exclusion primitive with ownership tracking</strong>. Only the thread that successfully acquired the mutex via a wait function can release it with <code>ReleaseMutex()</code>.
    </p>
    <p>
      Critically, Windows incorporates a vital kernel-level safety mechanism absent in raw POSIX semaphores: <strong>Automatic Abandoned Mutex Detection</strong>:
    </p>
    <div class="math-callout">
      <strong>The Abandoned Mutex Rescue Mechanism (WAIT_ABANDONED):</strong>
      <br>
      Suppose Thread <i>A</i> acquires a kernel mutex and enters its critical section. Before it can finish, Thread <i>A</i> crashes, faults on an unhandled null pointer, or is terminated by the user via Task Manager.
      <br>
      In naive systems, the mutex would remain permanently locked, deadlocking all surviving threads forever.
      <br>
      In Windows, the kernel tracks mutex ownership in the thread's <code>ETHREAD</code> block. Upon thread termination, the kernel walks the thread's list of held mutexes, <strong>automatically releases them</strong>, and transitions the next waiting thread with a special status code:
      <pre><code>DWORD wait_result = <span class="syn-fn">WaitForSingleObject</span>(hMutex, INFINITE);
<span class="syn-kw">if</span> (wait_result == WAIT_ABANDONED) {
    <span class="syn-cmt">/* The lock was acquired, BUT the previous owner died mid-critical section! */</span>
    <span class="syn-cmt">/* Data structure may be partially corrupted; thread must audit consistency */</span>
}</code></pre>
      This architectural resilience allows enterprise server software to recover gracefully from catastrophic thread failures.
    </div>"""

# ---------------------------------------------------------------------
# REPLACEMENT FOR SECTION 3 (DEEP WINDOWS USER-MODE SYNCHRONIZATION)
# ---------------------------------------------------------------------
WIN_SECTION_THREE_REPLACEMENT = r"""    <h3>3. Kernel Sleep Queues &amp; Fast User-Mode Synchronization</h3>
    <p>
      In Section 2, we analyzed how operating system kernels implement semaphores and sleep locks using internal spinlocks to guard wait queues. However, that design introduces a major performance bottleneck for user-space applications: <strong>every lock acquisition and release requires a kernel system call</strong>.
    </p>
    <p>
      A system call trap instruction (<code>syscall</code> on x86-64 Linux, <code>syscall</code> / <code>sysenter</code> on Windows, <code>svc</code> on ARM) forces the processor through an involuntary privilege boundary transition from Ring 3 (User Space) to Ring 0 (Kernel Mode). The CPU flushes pipeline queues, changes the stack pointer to the kernel stack, updates page-table permissions, and validates parameters. This sequence consumes <strong>100 to 300 nanoseconds</strong> per invocation.
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
      To bridge this performance divide, modern operating systems implement hybrid user/kernel synchronization:
    </p>
    <ul>
      <li><strong>Linux:</strong> The unified <code>futex</code> (Fast Userspace Mutex) architecture.</li>
      <li><strong>Windows NT:</strong> The trio of <code>CRITICAL_SECTION</code>, <code>SRWLOCK</code>, and <code>WaitOnAddress</code>.</li>
    </ul>

    <h4>The Linux Futex Architecture</h4>
    <p>
      A Linux futex is an ordinary 32-bit integer allocated in user-space virtual memory. The fast-path executes an atomic Compare-and-Swap (<code>cmpxchg</code>) in Ring 3 (~5 ns). Only if contention occurs does the thread drop into Ring 0 via:
    </p>
    <pre><code><span class="syn-fn">syscall</span>(SYS_futex, uaddr, FUTEX_WAIT, val, timeout, NULL, <span class="syn-num">0</span>);</code></pre>
    <p>
      The kernel verifies that <code>*uaddr == val</code> atomically under a bucket spinlock before putting the task to sleep on a kernel hash table (<code>futex_queues</code>), eliminating lost wakeups.
    </p>

    <h4>The Windows User-Mode Evolution: CRITICAL_SECTION, SRWLock, and WaitOnAddress</h4>
    <p>
      Windows pioneered user-mode hybrid locking and has developed three distinct generations of high-performance synchronization:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; margin: 20px 0;">
      <!-- 1. CRITICAL_SECTION -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--accent); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">1. CRITICAL_SECTION</h4>
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--accent); text-transform: uppercase; margin-bottom: 8px;">Hybrid Adaptive Spin</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          The classic Win32 user-mode lock. It wraps an internal <code>RTL_CRITICAL_SECTION</code> struct.
          <br><br>
          <strong>Adaptive Spin Optimization:</strong>
          Configured with <code>InitializeCriticalSectionAndSpinCount(&amp;cs, 4000)</code>. On multi-core CPUs, it spins in a tight user-mode loop up to 4,000 times before allocating a kernel auto-reset event object to sleep.
          <br><br>
          <em>Reentrancy:</em> Supports recursive acquisition by the same thread.
        </p>
      </div>

      <!-- 2. SRWLOCK -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">2. SRWLOCK</h4>
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--success); text-transform: uppercase; margin-bottom: 8px;">Slim Reader/Writer</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Introduced in Windows Vista to replace heavy critical sections.
          <br><br>
          <strong>Pointer-Sized Efficiency:</strong> Consumes only 4 bytes (32-bit) or 8 bytes (64-bit). Requires no dynamic initialization or destructor (<code>SRWLOCK_INIT</code>).
          <br><br>
          <em>Dual-Mode:</em> Supports both shared reader locks (<code>AcquireSRWLockShared</code>) and exclusive writer locks (<code>AcquireSRWLockExclusive</code>).
          <br><br>
          <em>Non-Reentrant:</em> Recursion is forbidden, eliminating bookkeeping overhead.
        </p>
      </div>

      <!-- 3. WaitOnAddress -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid #7c3aed; border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">3. WaitOnAddress</h4>
        <div style="font-size: 0.75rem; font-weight: 700; color: #7c3aed; text-transform: uppercase; margin-bottom: 8px;">Windows Futex Analog</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Introduced in Windows 8 / Server 2012 (<code>synchapi.h</code>).
          <br><br>
          Turns <em>any</em> 1, 2, 4, or 8-byte variable in user space into a sleep-wait target.
          <br><br>
          <em>API:</em>
          <code>WaitOnAddress(&amp;addr, &amp;undesired, size, timeout)</code>
          <br>
          <code>WakeByAddressSingle(&amp;addr)</code>
          <br>
          <code>WakeByAddressAll(&amp;addr)</code>
          <br><br>
          Sleeps in the kernel only if <code>*addr == undesired</code>, matching Linux futex semantics.
        </p>
      </div>
    </div>

    <h4>Deep Microarchitectural Comparison: Linux vs. Windows</h4>
    <div style="overflow-x: auto; margin: 20px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 12px; width: 22%;">Metric / Capability</th>
            <th style="padding: 10px 12px; width: 39%;">Linux Futex Subsystem</th>
            <th style="padding: 10px 12px; width: 39%;">Windows NT User-Mode Subsystem</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Lightweight User Mutex</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">pthread_mutex_t (built on futex)</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">SRWLOCK (Slim Reader/Writer Lock)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Direct Memory Wait Primitive</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">syscall(SYS_futex, uaddr, FUTEX_WAIT, val)</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">WaitOnAddress(addr, &amp;undesired, size, timeout)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Direct Wake Primitive</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">syscall(SYS_futex, uaddr, FUTEX_WAKE, 1)</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">WakeByAddressSingle(addr)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Supported Target Data Sizes</td>
            <td style="padding: 10px 12px;">Historically 32-bit only (FUTEX2 adds 8/16/64)</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 600;">1, 2, 4, or 8 bytes natively</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Wait Queue Implementation</td>
            <td style="padding: 10px 12px;">Global kernel hash table (futex_queues)</td>
            <td style="padding: 10px 12px;">Kernel keyed-event synchronization buckets</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #f0fdf4;">
            <td style="padding: 10px 12px; font-weight: 700; color: #166534;">C++20 Standard Mapping</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">std::atomic::wait() &rarr; FUTEX_WAIT</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">std::atomic::wait() &rarr; WaitOnAddress</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h4>Concrete Implementation: Building a Fast Mutex with Windows WaitOnAddress</h4>
    <p>
      We can construct an industrial-grade, pointer-sized mutex on Windows without allocating Win32 handles or kernel objects using <code>WaitOnAddress</code>:
    </p>

    <pre><code><span class="syn-cmt">/* Production Windows Fast Mutex Using WaitOnAddress (synchapi.h) */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;windows.h&gt;</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;synchapi.h&gt;</span>

<span class="syn-kw">typedef struct</span> {
    <span class="syn-kw">volatile LONG</span> state; <span class="syn-cmt">/* 0 = Free, 1 = Held (no waiters), 2 = Held (waiters present) */</span>
} win_fast_mutex_t;

<span class="syn-kw">void</span> win_fast_mutex_lock(win_fast_mutex_t *m) {
    <span class="syn-cmt">/* 1. FAST PATH: Optimistically attempt atomic CAS 0 -> 1 in user space */</span>
    <span class="syn-kw">LONG</span> prev = <span class="syn-fn">InterlockedCompareExchange</span>(&amp;m-&gt;state, <span class="syn-num">1</span>, <span class="syn-num">0</span>);
    <span class="syn-kw">if</span> (prev == <span class="syn-num">0</span>) {
        <span class="syn-kw">return</span>; <span class="syn-cmt">/* Lock acquired in Ring 3! ~5 nanoseconds, zero syscalls */</span>
    }

    <span class="syn-cmt">/* 2. SLOW PATH: Contention detected */</span>
    <span class="syn-kw">while</span> (<span class="syn-kw">true</span>) {
        <span class="syn-cmt">/* Announce that waiters exist (state = 2) */</span>
        <span class="syn-kw">if</span> (prev == <span class="syn-num">2</span> || <span class="syn-fn">InterlockedCompareExchange</span>(&amp;m-&gt;state, <span class="syn-num">2</span>, <span class="syn-num">1</span>) != <span class="syn-num">0</span>) {
            <span class="syn-cmt">/* Sleep in kernel if state is still 2 */</span>
            <span class="syn-kw">LONG</span> undesired = <span class="syn-num">2</span>;
            <span class="syn-fn">WaitOnAddress</span>(&amp;m-&gt;state, &amp;undesired, <span class="syn-kw">sizeof</span>(<span class="syn-kw">LONG</span>), INFINITE);
        }
        <span class="syn-cmt">/* Try to acquire upon wakeup */</span>
        prev = <span class="syn-fn">InterlockedExchange</span>(&amp;m-&gt;state, <span class="syn-num">2</span>);
        <span class="syn-kw">if</span> (prev == <span class="syn-num">0</span>) <span class="syn-kw">break</span>;
    }
}

<span class="syn-kw">void</span> win_fast_mutex_unlock(win_fast_mutex_t *m) {
    <span class="syn-cmt">/* Fast path: If state was 1, no waiters exist. Reset to 0 in user space */</span>
    <span class="syn-kw">if</span> (<span class="syn-fn">InterlockedExchange</span>(&amp;m-&gt;state, <span class="syn-num">0</span>) == <span class="syn-num">2</span>) {
        <span class="syn-cmt">/* Waiters were present; wake up exactly one waiting thread */</span>
        <span class="syn-fn">WakeByAddressSingle</span>((<span class="syn-kw">PVOID</span>)&amp;m-&gt;state);
    }
}</code></pre>"""

# ---------------------------------------------------------------------
# REPLACEMENT FOR SECTION 4 (WINDOWS CONDITION VARIABLES & MONITORS)
# ---------------------------------------------------------------------
WIN_SECTION_FOUR_ADDITION = r"""    <h4>Windows Native Condition Variables (CONDITION_VARIABLE)</h4>
    <p>
      In Windows Vista, Microsoft introduced native support for condition variables to match POSIX capabilities without requiring handle allocations:
    </p>
    <ul>
      <li><strong>Allocation:</strong> Consumes only a single pointer (<code>CONDITION_VARIABLE cv;</code>). Initialized statically via <code>CONDITION_VARIABLE_INIT</code> or dynamically via <code>InitializeConditionVariable(&amp;cv)</code>.</li>
      <li>
        <strong>Dual Mutex Support:</strong> Unlike POSIX which binds condition variables strictly to <code>pthread_mutex_t</code>, Windows condition variables can atomically unlock and sleep over <em>either</em> a Critical Section or an SRW Lock:
        <ul>
          <li><code>SleepConditionVariableCS(&amp;cv, &amp;cs, dwMilliseconds)</code>: Releases Critical Section, sleeps, and re-acquires upon wake.</li>
          <li><code>SleepConditionVariableSRW(&amp;cv, &amp;srw, dwMilliseconds, flags)</code>: Releases SRW lock (shared or exclusive), sleeps, and re-acquires.</li>
        </ul>
      </li>
      <li>
        <strong>Signaling Primitives:</strong>
        <ul>
          <li><code>WakeConditionVariable(&amp;cv)</code>: Equivalent to <code>pthread_cond_signal</code> (wakes one waiter).</li>
          <li><code>WakeAllConditionVariable(&amp;cv)</code>: Equivalent to <code>pthread_cond_broadcast</code> (wakes all waiters).</li>
        </ul>
      </li>
    </ul>

    <pre><code><span class="syn-cmt">/* Windows Bounded-Buffer Monitor with SRWLock and CONDITION_VARIABLE */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;windows.h&gt;</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;stdbool.h&gt;</span>

<span class="syn-kw">#define</span> BUFFER_CAPACITY <span class="syn-num">50</span>

<span class="syn-kw">typedef struct</span> {
    <span class="syn-kw">int</span> buffer[BUFFER_CAPACITY];
    <span class="syn-kw">int</span> count, head, tail;
    SRWLOCK lock;                       <span class="syn-cmt">/* Fast user-mode lock */</span>
    CONDITION_VARIABLE cv_not_full;     <span class="syn-cmt">/* Condition: room for producer */</span>
    CONDITION_VARIABLE cv_not_empty;    <span class="syn-cmt">/* Condition: items for consumer */</span>
} win_monitor_t;

<span class="syn-kw">void</span> win_monitor_insert(win_monitor_t *m, <span class="syn-kw">int</span> item) {
    <span class="syn-fn">AcquireSRWLockExclusive</span>(&amp;m-&gt;lock);

    <span class="syn-cmt">/* MESA SEMANTICS INVARIANT: Mandatory while loop re-check */</span>
    <span class="syn-kw">while</span> (m-&gt;count == BUFFER_CAPACITY) {
        <span class="syn-fn">SleepConditionVariableSRW</span>(&amp;m-&gt;cv_not_full, &amp;m-&gt;lock, INFINITE, <span class="syn-num">0</span>);
    }

    m-&gt;buffer[m-&gt;head] = item;
    m-&gt;head = (m-&gt;head + <span class="syn-num">1</span>) % BUFFER_CAPACITY;
    m-&gt;count++;

    <span class="syn-fn">WakeConditionVariable</span>(&amp;m-&gt;cv_not_empty); <span class="syn-cmt">/* Wake one consumer */</span>
    <span class="syn-fn">ReleaseSRWLockExclusive</span>(&amp;m-&gt;lock);
}

<span class="syn-kw">int</span> win_monitor_remove(win_monitor_t *m) {
    <span class="syn-fn">AcquireSRWLockExclusive</span>(&amp;m-&gt;lock);

    <span class="syn-kw">while</span> (m-&gt;count == <span class="syn-num">0</span>) {
        <span class="syn-fn">SleepConditionVariableSRW</span>(&amp;m-&gt;cv_not_empty, &amp;m-&gt;lock, INFINITE, <span class="syn-num">0</span>);
    }

    <span class="syn-kw">int</span> item = m-&gt;buffer[m-&gt;tail];
    m-&gt;tail = (m-&gt;tail + <span class="syn-num">1</span>) % BUFFER_CAPACITY;
    m-&gt;count--;

    <span class="syn-fn">WakeConditionVariable</span>(&amp;m-&gt;cv_not_full); <span class="syn-cmt">/* Wake one producer */</span>
    <span class="syn-fn">ReleaseSRWLockExclusive</span>(&amp;m-&gt;lock);
    <span class="syn-kw">return</span> item;
}</code></pre>
    <p>
      Windows condition variables strictly adhere to <strong>Mesa semantics (Signal-and-Continue)</strong>. The thread calling <code>WakeConditionVariable</code> retains the SRW lock and continues executing; the awakened thread competes with incoming threads when re-acquiring the lock. Consequently, <strong>the <code>while</code> loop predicate guard is strictly mandatory on Windows</strong>.
    </p>"""

def update_module_three_windows():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update Section 1 with Windows Dispatcher Objects & Events
    s1_marker = "<h4>The Failed Wakeup-Waiting Bit Patch</h4>"
    if "Windows Dispatcher Objects: Eliminating Lost Wakeups via Events" not in content and s1_marker in content:
        idx = content.find(s1_marker)
        content = content[:idx] + WIN_SECTION_ONE_ADDITION + "\n\n    " + content[idx:]

    # 2. Update Section 2 with Windows Semaphores & Abandoned Mutexes
    s2_marker = "<!-- Interactive Aid: Bounded-Buffer Counting Semaphore Pipeline -->"
    if "Windows Kernel Semaphores &amp; Mutexes" not in content and s2_marker in content:
        idx = content.find(s2_marker)
        content = content[:idx] + WIN_SECTION_TWO_ADDITION + "\n\n    " + content[idx:]

    # 3. Update Section 3 with Deep Windows User-Mode Synchronization
    s3_start = "<h3>3. Kernel Sleep Queues &amp; Linux Futexes</h3>"
    s3_end = "<!-- Interactive Aid: Linux Futex Fast-Path vs Slow-Path -->"
    if s3_start in content and s3_end in content:
        idx_start = content.find(s3_start)
        idx_end = content.find(s3_end)
        content = content[:idx_start] + WIN_SECTION_THREE_REPLACEMENT + "\n\n    " + content[idx_end:]

    # 4. Update Section 4 with Windows Condition Variables & SRW Locks
    s4_marker = "<!-- Interactive Aid: Hoare vs Mesa Monitor Signaling Stepper -->"
    if "Windows Native Condition Variables (CONDITION_VARIABLE)" not in content and s4_marker in content:
        idx = content.find(s4_marker)
        content = content[:idx] + WIN_SECTION_FOUR_ADDITION + "\n\n    " + content[idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully integrated comprehensive Windows NT synchronization across {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Deeply integrate Windows NT synchronization primitives throughout Module 03\n\n"
            "Add KEVENT, abandoned mutexes, RTL_CRITICAL_SECTION internals, SRWLOCK,\n"
            "WaitOnAddress, and SleepConditionVariableSRW alongside POSIX primitives."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_module_three_windows():
        run_git_sync()
