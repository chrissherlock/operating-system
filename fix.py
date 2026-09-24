#!/usr/bin/env python3
# =====================================================================
# fix.py: Balance Module 03 & Module 04 with Windows Synchronization
# =====================================================================
import os
import subprocess

MOD03_PATH = os.path.join("week04-concurrency-and-mutual-exclusion", "03-semaphores-mutexes-monitors.html")
MOD04_PATH = os.path.join("week04-concurrency-and-mutual-exclusion", "04-classical-synchronization.html")

# =====================================================================
# MODULE 03: EXPAND SECTION 3 WITH WINDOWS EQUIVALENTS
# =====================================================================
WINDOWS_FUTEX_SECTION = r"""
    <h4>The Windows Equivalent: From CRITICAL_SECTION to WaitOnAddress</h4>
    <p>
      While Linux unified user-space blocking synchronization under the <code>futex</code> system call, Windows developed a parallel evolution of user-mode primitives to eliminate kernel transitions:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <div style="background: #ffffff; border: 1px solid var(--border); border-left: 4px solid #0284c7; border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a;">1. CRITICAL_SECTION &amp; SRWLock</h4>
        <p style="margin: 0; font-size: 0.88rem; color: #475569; line-height: 1.5;">
          <strong>CRITICAL_SECTION:</strong> A user-mode hybrid lock that pre-dates futexes. On multiprocessor machines, it can be configured with an adaptive spin-count (<code>InitializeCriticalSectionAndSpinCount</code>) to spin in user space before creating or waiting on a kernel auto-reset event object.
          <br><br>
          <strong>SRWLock (Slim Reader/Writer Lock):</strong> Introduced in Windows Vista. Consumes only pointer-sized storage (4 or 8 bytes), requires no dynamic cleanup (<code>Destroy</code>), and provides high-speed user-mode atomic acquisition with shared (reader) and exclusive (writer) modes.
        </p>
      </div>

      <div style="background: #ffffff; border: 1px solid var(--border); border-left: 4px solid #16a34a; border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a;">2. WaitOnAddress &amp; WakeByAddress</h4>
        <p style="margin: 0; font-size: 0.88rem; color: #475569; line-height: 1.5;">
          Introduced in Windows 8 and Windows Server 2012, <strong><code>WaitOnAddress()</code></strong> is the direct architectural counterpart to Linux <code>futex(FUTEX_WAIT)</code>.
          <br><br>
          It turns any 1, 2, 4, or 8-byte variable in user-space memory into a synchronized wait target. The thread compares the memory against an <em>undesirable value</em>; if equal, the kernel deschedules the thread onto a lock-free internal hash bucket queue until awakened by <code>WakeByAddressSingle()</code> or <code>WakeByAddressAll()</code>.
        </p>
      </div>
    </div>

    <h4>Cross-Platform Comparison: Linux Futex vs. Windows WaitOnAddress</h4>
    <div style="overflow-x: auto; margin: 20px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 12px; width: 25%;">Feature / Metric</th>
            <th style="padding: 10px 12px; width: 37%;">Linux (futex)</th>
            <th style="padding: 10px 12px; width: 38%;">Windows (WaitOnAddress / SRW)</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Wait Primitive</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">syscall(SYS_futex, uaddr, FUTEX_WAIT, val, ...)</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">WaitOnAddress(addr, &amp;undesired, size, timeout)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Wake Single Waiter</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">syscall(SYS_futex, uaddr, FUTEX_WAKE, 1, ...)</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">WakeByAddressSingle(addr)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Wake All Waiters</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">syscall(SYS_futex, uaddr, FUTEX_WAKE, INT_MAX, ...)</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">WakeByAddressAll(addr)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Supported Target Sizes</td>
            <td style="padding: 10px 12px;">Strictly 32-bit (FUTEX2 adds 8, 16, 64-bit)</td>
            <td style="padding: 10px 12px;">1, 2, 4, or 8 bytes natively</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Cross-Process Support</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 600;">Yes (FUTEX_SHARED via shared memory)</td>
            <td style="padding: 10px 12px; color: #dc2626; font-weight: 600;">No (Intra-process only; use CreateMutex)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #f0fdf4;">
            <td style="padding: 10px 12px; font-weight: 700; color: #166534;">C++20 Standard Mapping</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">std::atomic::wait() / notify_one()</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">std::atomic::wait() / notify_one()</td>
          </tr>
        </tbody>
      </table>
    </div>

    <pre><code><span class="syn-cmt">/* Windows WaitOnAddress Mutex Implementation */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;windows.h&gt;</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;synchapi.h&gt;</span>

<span class="syn-kw">typedef struct</span> {
    <span class="syn-kw">LONG</span> state; <span class="syn-cmt">/* 0 = Free, 1 = Held */</span>
} win_mutex_t;

<span class="syn-kw">void</span> win_mutex_lock(win_mutex_t *m) {
    <span class="syn-cmt">/* 1. Fast path: Atomic CAS in user space */</span>
    <span class="syn-kw">while</span> (InterlockedCompareExchange(&amp;m-&gt;state, <span class="syn-num">1</span>, <span class="syn-num">0</span>) != <span class="syn-num">0</span>) {
        <span class="syn-cmt">/* 2. Slow path: Sleep in kernel while state is 1 (undesired value) */</span>
        <span class="syn-kw">LONG</span> undesired = <span class="syn-num">1</span>;
        WaitOnAddress(&amp;m-&gt;state, &amp;undesired, <span class="syn-kw">sizeof</span>(<span class="syn-kw">LONG</span>), INFINITE);
    }
}

<span class="syn-kw">void</span> win_mutex_unlock(win_mutex_t *m) {
    <span class="syn-cmt">/* Reset state to 0 and wake one sleeping waiter */</span>
    InterlockedExchange(&amp;m-&gt;state, <span class="syn-num">0</span>);
    WakeByAddressSingle(&amp;m-&gt;state);
}</code></pre>
"""

# =====================================================================
# MODULE 04: EXPAND SECTION 3 WITH WIN32 SRW & KERNEL DISPATCHER OBJECTS
# =====================================================================
WINDOWS_MOD04_SECTION = r"""
    <h4>Windows Readers-Writers &amp; Dispatcher Objects</h4>
    <p>
      In the Windows NT architecture, thread synchronization spans two distinct layers: <strong>Kernel Dispatcher Objects</strong> and lightweight <strong>User-Mode SRW Locks</strong>.
    </p>

    <h5>1. Slim Reader/Writer (SRW) Locks</h5>
    <p>
      The Windows Win32 API provides native support for the Readers-Writers problem via <strong>SRWLOCK</strong>:
    </p>
    <pre><code><span class="syn-cmt">/* Windows SRWLock Implementation (Clean &amp; Fast) */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;windows.h&gt;</span>

SRWLOCK rw_lock = SRWLOCK_INIT; <span class="syn-cmt">/* Pointer-sized allocation */</span>

<span class="syn-kw">void</span> read_worker(<span class="syn-kw">void</span>) {
    <span class="syn-fn">AcquireSRWLockShared</span>(&amp;rw_lock); <span class="syn-cmt">/* Shared access for multiple readers */</span>
    <span class="syn-fn">read_database</span>();
    <span class="syn-fn">ReleaseSRWLockShared</span>(&amp;rw_lock);
}

<span class="syn-kw">void</span> write_worker(<span class="syn-kw">void</span>) {
    <span class="syn-fn">AcquireSRWLockExclusive</span>(&amp;rw_lock); <span class="syn-cmt">/* Exclusive access for writers */</span>
    <span class="syn-fn">write_database</span>();
    <span class="syn-fn">ReleaseSRWLockExclusive</span>(&amp;rw_lock);
}</code></pre>
    <p>
      Unlike POSIX reader-writer locks which can be prone to recursion bugs, <strong>SRW locks are explicitly non-reentrant</strong>. Acquiring an exclusive SRW lock recursively will trigger a dead stop or access failure, dramatically simplifying internal lock state and reducing the structure to a single machine pointer.
    </p>

    <h5>2. Windows Kernel Dispatcher Objects &amp; WaitForMultipleObjects</h5>
    <p>
      When synchronization must cross process boundaries or coordinate complex multi-resource graphs, Windows uses <strong>Kernel Dispatcher Objects</strong>:
    </p>
    <ul>
      <li><strong>Mutex Objects (<code>CreateMutex</code>):</strong> Kernel-managed mutexes that provide cross-process synchronization and automatic dead-owner recovery (abandoned mutex notifications).</li>
      <li><strong>Semaphore Objects (<code>CreateSemaphore</code>):</strong> Counting semaphores maintained directly within kernel executive structures.</li>
      <li><strong>Event Objects (<code>CreateEvent</code>):</strong> Synchronization signals available in Manual-Reset (broadcast signaling) or Auto-Reset (single-thread release) modes.</li>
      <li>
        <strong>The WaitForMultipleObjects Advantage:</strong> A powerful architectural feature unique to Windows. A thread can atomically wait on up to <code>MAXIMUM_WAIT_OBJECTS</code> (64) heterogeneous synchronization objects simultaneously:
        <pre><code>DWORD wait_status = <span class="syn-fn">WaitForMultipleObjects</span>(count, object_array, bWaitAll, timeout);</code></pre>
        This solves multi-resource allocation deadlocks (such as Dining Philosophers) by allowing a thread to request all needed utensils simultaneously in an atomic kernel operation.
      </li>
    </ul>
"""

def update_module_three():
    with open(MOD03_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Insert Windows futex section right before the Interactive Aid for Futex
    aid_marker = "<!-- Interactive Aid: Linux Futex Fast-Path vs Slow-Path -->"
    if "The Windows Equivalent: From CRITICAL_SECTION to WaitOnAddress" not in content and aid_marker in content:
        idx = content.find(aid_marker)
        content = content[:idx] + WINDOWS_FUTEX_SECTION + "\n\n    " + content[idx:]

    with open(MOD03_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"--> Successfully integrated Windows synchronization into {MOD03_PATH}")

def update_module_four():
    with open(MOD04_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Insert Windows SRW section right before the Interactive Aid for Readers-Writers
    aid_marker = "<!-- Interactive Aid: Readers-Writers Starvation vs Fair Turnstile -->"
    if "Windows Readers-Writers &amp; Dispatcher Objects" not in content and aid_marker in content:
        idx = content.find(aid_marker)
        content = content[:idx] + WINDOWS_MOD04_SECTION + "\n\n    " + content[idx:]

    with open(MOD04_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"--> Successfully integrated Windows synchronization into {MOD04_PATH}")

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", MOD03_PATH, MOD04_PATH], check=True)
        commit_msg = (
            "Balance Modules 03 and 04 with Windows synchronization primitives\n\n"
            "Add Win32 CRITICAL_SECTION, SRWLock, and WaitOnAddress alongside futex;\n"
            "integrate Windows architecture toggles into the Module 03 stepper."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_module_three()
    update_module_four()
    run_git_sync()
