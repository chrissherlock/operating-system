#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand Linux lockdep & Windows Driver Verifier in Module 04
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "04-classic-synchronization-real-world-defenses.html"
)

REAL_WORLD_DEFENSES_EXPANDED = r"""      <h3>3. Real-World Kernel Defenses: Linux lockdep &amp; Driver Verifier</h3>
      <p>
        In modern enterprise operating system kernels, theoretical avoidance algorithms such as Dijkstra's Banker's Algorithm are practically unusable. The reasons are architectural: real-world kernels execute thousands of asynchronous device drivers and user threads simultaneously, resources cannot be enumerated in static vectors upfront, and the $\mathcal{O}(m \times n^2)$ latency overhead of running dynamic matrix verifications on every spinlock acquisition would decimate system throughput.
      </p>
      <p>
        Consequently, modern operating systems adopt a pragmatic, multi-tier strategy: they use fine-grained locking primitives for maximum concurrent performance, combined with <strong>aggressive runtime lock validation subsystems</strong> to identify potential deadlock patterns long before they manifest as unrecoverable production hangs.
      </p>

      <h4>1. Linux Kernel Lock Validator: <code>lockdep</code></h4>
      <p>
        Introduced by Ingo Molnar and Arjan van de Ven in Linux 2.6.17, <strong><code>lockdep</code></strong> is the Linux kernel's built-in runtime lock validation engine. Rather than detecting deadlocks after the system freezes, <code>lockdep</code> dynamically models the <em>rules</em> of lock acquisition to detect <strong>potential</strong> deadlocks during normal execution—even if the deadlocking race condition has not yet occurred.
      </p>

      <h5>Lock Classes vs. Lock Instances</h5>
      <p>
        A naive lock tracker that monitored every discrete lock instance would consume gigabytes of RAM. For example, a Linux filesystem might instantiate millions of distinct <code>struct inode</code> or <code>struct dentry</code> objects, each containing its own mutex.
      </p>
      <p>
        To solve this scaling problem, <code>lockdep</code> aggregates locks into <strong>Lock Classes</strong> using static identity keys (<code>struct lock_class_key</code>):
      </p>
      <ul>
        <li>
          <strong>Class-Based Mapping:</strong> All lock instances initialized at the same static code site belong to the exact same lock class. For instance, every <code>inode-&gt;i_rwsem</code> allocated across the ext4 filesystem shares a single lock class identity.
        </li>
        <li>
          <strong>Bounded Graph Complexity:</strong> Instead of tracking millions of nodes, <code>lockdep</code> maintains a directed dependency graph of only several thousand lock classes, reducing cycle detection to microseconds.
        </li>
      </ul>

      <h5>The Core Invariants Tracked by <code>lockdep</code></h5>
      <ol>
        <li>
          <strong>Lock Acquisition Ordering (Circular Dependency):</strong> If a thread acquires Class $A$ and then acquires Class $B$, <code>lockdep</code> inserts a directed edge $A \to B$ into its global Lock Dependency Graph. If any thread later attempts to acquire Class $A$ while already holding Class $B$ ($B \to A$), <code>lockdep</code> immediately identifies a directed cycle, prints a detailed warning splat to <code>dmesg</code>, and outputs the exact stack traces of both acquisition paths.
        </li>
        <li>
          <strong>Hardirq &amp; Softirq Context Inversion:</strong> A classic kernel deadlock occurs when a lock is acquired in process context with hardware interrupts enabled:
          $$ \text{Thread on CPU 0 acquires Lock } L \implies \text{Hardirq fires on CPU 0} \implies \text{ISR attempts to acquire Lock } L $$
          Because the interrupt service routine (ISR) interrupted the thread holding $L$, the thread cannot run to release $L$, while the ISR spins forever on the same CPU. <code>lockdep</code> tracks the interrupt state of every lock class and flags any lock taken in interrupt context that was previously acquired with interrupts enabled.
        </li>
      </ol>

      <h5>Anatomy of a <code>lockdep</code> Splat (Kernel Diagnostic)</h5>
      <p>
        When <code>lockdep</code> detects an invalid lock ordering, it produces a diagnostic report in the kernel log:
      </p>

      <!-- Syntax Highlighted Kernel Splat Box -->
      <div style="background: #0f172a; color: #f8fafc; border-radius: 8px; padding: 20px; font-family: var(--font-mono); font-size: 0.82rem; overflow-x: auto; margin: 16px 0; border: 1px solid var(--border);">
        <div style="color: #64748b; margin-bottom: 10px; font-size: 0.78rem; border-bottom: 1px solid #334155; padding-bottom: 6px;">
          dmesg &bull; lockdep_warning.log
        </div>
        <pre style="margin: 0; line-height: 1.5;"><span style="color: #f87171; font-weight: 700;">======================================================</span>
<span style="color: #f87171; font-weight: 700;">WARNING: possible circular locking dependency detected</span>
<span style="color: #94a3b8;">6.8.0-rc3-custom #1 Not tainted</span>
<span style="color: #f87171; font-weight: 700;">------------------------------------------------------</span>
<span style="color: #38bdf8;">kworker/u16:2/184</span> is trying to acquire lock:
ffff888102a3b040 (&amp;sb-&gt;s_type-&gt;i_mutex_key#3){++++}-{3:3}, at: ext4_evict_inode+0x12a

but task is already holding lock:
ffff888103c89120 (&amp;journal-&gt;j_trans_barrier){++++}-{0:0}, at: jbd2_journal_start+0x8f

<span style="color: #fbbf24;">which lock already depends on the new lock!</span>

the existing dependency chain (in reverse order) is:
-&gt; #1 (&amp;journal-&gt;j_trans_barrier){++++}-{0:0}:
       validate_chain+0x628/0x1030
       __lock_acquire+0x4c2/0x9a0
       lock_acquire+0xd8/0x310
       jbd2_journal_start+0x8f/0x230
-&gt; #0 (&amp;sb-&gt;s_type-&gt;i_mutex_key#3){++++}-{3:3}:
       validate_chain+0x628/0x1030
       __lock_acquire+0x4c2/0x9a0
       lock_acquire+0xd8/0x310
       ext4_evict_inode+0x12a/0x680</pre>
      </div>

      <h4>2. Windows Driver Verifier: Deadlock Detection Engine</h4>
      <p>
        On Microsoft Windows, the primary mechanism for defending the Executive and device subsystem against synchronization failures is <strong>Driver Verifier</strong>. Because third-party hardware device drivers execute in kernel mode with unrestricted hardware access, an unhandled lock deadlock in a driver halts the entire operating system.
      </p>

      <h5>Deadlock Detection Mechanics</h5>
      <p>
        When the <em>Deadlock Detection</em> option is enabled in Driver Verifier, the kernel intercepts and wraps all core synchronization APIs exposed by the Windows Kernel Executive:
      </p>
      <ul>
        <li>Executive Spinlocks (<code>KeAcquireSpinLock</code>, <code>KeReleaseSpinLock</code>, <code>KeAcquireInStackQueuedSpinLock</code>)</li>
        <li>Executive Fast Mutexes (<code>ExAcquireFastMutex</code>)</li>
        <li>Shared/Exclusive Executive Resources (<code>ERESOURCE</code>)</li>
      </ul>
      <p>
        Driver Verifier builds an internal Resource Hierarchy Graph tracking ownership topology. If Driver Verifier detects that Driver $X$ acquires Resource $A$ and waits on Resource $B$, while Driver $Y$ holds Resource $B$ and requests Resource $A$, the system will not wait for an indefinite freeze.
      </p>

      <h5>Enforcing Interrupt Request Level (IRQL) Rules</h5>
      <p>
        Windows synchronization primitives are tightly bound to the processor's <strong>IRQL (Interrupt Request Level)</strong>:
      </p>
      <ul>
        <li><strong><code>PASSIVE_LEVEL</code> (0):</strong> Normal user-thread execution. Paged memory access and blocking wait operations (e.g., <code>KeWaitForSingleObject</code>) are permitted.</li>
        <li><strong><code>APC_LEVEL</code> (1):</strong> Asynchronous Procedure Calls. Page faults are still allowed.</li>
        <li><strong><code>DISPATCH_LEVEL</code> (2):</strong> Thread scheduler and DPC execution. <em>Page faults and context-switch wait operations are strictly forbidden.</em> Only non-paged memory and non-sleeping spinlocks may be used.</li>
      </ul>
      <p>
        A frequent cause of Windows kernel deadlocks is acquiring a spinlock (which elevates the CPU to <code>DISPATCH_LEVEL</code>) and then attempting to access paged-pool memory. If that memory has been paged out to disk, the CPU triggers a page fault requiring disk I/O—which requires waiting for an I/O completion interrupt. But the thread scheduler cannot run on that CPU because it is locked at <code>DISPATCH_LEVEL</code>, causing an immediate deadlock. Driver Verifier traps this condition instantaneously.
      </p>

      <h5>BugCheck <code>0xC4</code>: <code>DRIVER_VERIFIER_DETECTED_VIOLATION</code></h5>
      <p>
        When Driver Verifier detects a deadlock cycle or fatal IRQL violation, it immediately halts execution with a Blue Screen of Death (BSOD) generating <strong>Stop Code <code>0xC4</code></strong>. Subcode <code>0x100</code> indicates a proven deadlock:
      </p>

      <div class="math-callout" style="background: #f8fafc; border-left: 4px solid var(--danger); padding: 16px; border-radius: 0 6px 6px 0; margin: 18px 0;">
        <strong style="color: var(--danger);">Windows Crash Dump Analysis:</strong>
        <br><br>
        <code>STOP 0x000000C4 (0x00000100, Resource1, Resource2, ThreadAddress)</code>
        <p style="margin: 8px 0 0 0; font-size: 0.88rem; color: var(--text);">
          Parameter 1 (<code>0x100</code>) confirms a circular lock dependency. Parameters 2 and 3 provide the kernel virtual memory addresses of the conflicting locks, enabling instant disassembly in WinDbg via <code>!deadlock</code>.
        </p>
      </div>

      <h4>3. Architectural Comparison: Linux vs. Windows</h4>
      <table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.88rem;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px; text-align: left; color: var(--primary);">Architectural Property</th>
            <th style="padding: 10px; text-align: left; color: var(--primary);">Linux <code>lockdep</code></th>
            <th style="padding: 10px; text-align: left; color: var(--primary);">Windows Driver Verifier</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px; font-weight: 600;">Primary Abstraction</td>
            <td style="padding: 10px;"><strong>Lock Classes</strong> (identifies code sites via static keys).</td>
            <td style="padding: 10px;"><strong>Resource Nodes</strong> (intercepts specific runtime object pointers).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px; font-weight: 600;">Trigger Timing</td>
            <td style="padding: 10px; color: #16a34a;">Predictive (warns when an unsafe order is theoretically possible).</td>
            <td style="padding: 10px; color: #0284c7;">Active runtime tracking (detects live circular wait chains).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px; font-weight: 600;">Default Action on Violation</td>
            <td style="padding: 10px;">Prints kernel warning splat to <code>dmesg</code>; disables itself to save system.</td>
            <td style="padding: 10px; color: #dc2626;">Immediate BugCheck <code>0xC4</code> (forces crash dump generation).</td>
          </tr>
          <tr>
            <td style="padding: 10px; font-weight: 600;">Production Viability</td>
            <td style="padding: 10px;">Disabled in production distro kernels; standard in debug/test kernels.</td>
            <td style="padding: 10px;">Selectively enabled per-driver by system administrators and QA labs.</td>
          </tr>
        </tbody>
      </table>"""

def expand_real_world_defenses():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>3. Real-World Kernel Defenses: Linux lockdep &amp; Driver Verifier</h3>"
    end_marker = "</div>\n\n    <nav class=\"nav-bar\">"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 3 boundaries in target file.")
        return False

    updated_content = content[:start_idx] + REAL_WORLD_DEFENSES_EXPANDED + "\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 3 in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if expand_real_world_defenses():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Deeply expand real-world kernel defenses section in Module 04\n\n"
                "Add architectural breakdowns of Linux lockdep lock classes and IRQ\n"
                "inversions, Windows Driver Verifier IRQL rules, and real panic splats."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
