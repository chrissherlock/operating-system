#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand Section 3 in 01-race-conditions-critical-regions.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week04-concurrency-and-mutual-exclusion", "01-race-conditions-critical-regions.html")

EXPANDED_SECTION_THREE = r"""    <h3>3. Critical Regions &amp; Mutual Exclusion</h3>
    <p>
      The discovery of non-atomic assembly execution reveals an unavoidable systems dilemma: to avoid race hazards, concurrent execution flows must be prevented from reading or writing shared mutable data simultaneously.
    </p>
    <p>
      This requirement leads directly to the core abstraction of concurrent programming: the <strong>Critical Region</strong> (often termed the <em>Critical Section</em>).
    </p>

    <h4>Formal Definition: The Critical Region</h4>
    <p>
      A <strong>Critical Region</strong> is a contiguous segment of code in which a thread or process accesses one or more shared mutable resources&mdash;such as global variables, heap structures, hardware device registers, or shared file pointers&mdash;whose consistency depends on atomic execution.
    </p>
    <p>
      The operational objective of synchronization is to enforce <strong>Mutual Exclusion</strong>:
    </p>
    <blockquote style="border-left: 4px solid var(--accent); padding: 8px 16px; margin: 16px 0; background: #f8fafc; color: #334155; font-style: italic;">
      <strong>The Mutual Exclusion Invariant:</strong> At any physical instant in time <i>t</i>, if Process <i>A</i> is executing within its critical region, all other processes must be strictly barred from entering their critical regions for that same shared resource.
    </blockquote>

    <h4>The Canonical Four-Stage Execution Lifecycle</h4>
    <p>
      Any concurrent thread accessing shared state can be decomposed into four distinct execution phases:
    </p>

    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 20px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 1.3: The Canonical Four-Stage Synchronization Lifecycle</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">The mandatory gating sequence surrounding any operation on shared mutable state.</div>

      <svg viewBox="0 0 760 130" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="cs-arr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
        </defs>

        <!-- 1. Entry Section -->
        <rect x="15" y="30" width="165" height="60" rx="5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="97" y="52" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0f172a">1. ENTRY SECTION</text>
        <text x="97" y="68" text-anchor="middle" font-size="8" fill="#64748b">acquire(&amp;lock)</text>
        <text x="97" y="80" text-anchor="middle" font-size="7.5" fill="#0284c7">Requests permission</text>

        <line x1="180" y1="60" x2="208" y2="60" stroke="#0284c7" stroke-width="2" marker-end="url(#cs-arr)"/>

        <!-- 2. Critical Region -->
        <rect x="210" y="24" width="180" height="72" rx="6" fill="#fef2f2" stroke="#dc2626" stroke-width="2.5"/>
        <text x="300" y="50" text-anchor="middle" font-size="10.5" font-weight="700" fill="#991b1b">2. CRITICAL REGION</text>
        <text x="300" y="68" text-anchor="middle" font-family="var(--font-mono)" font-size="8.5" fill="#dc2626">balance += 100;</text>
        <text x="300" y="82" text-anchor="middle" font-size="7.5" font-weight="700" fill="#991b1b">[EXCLUSIVE ACCESS]</text>

        <line x1="390" y1="60" x2="418" y2="60" stroke="#0284c7" stroke-width="2" marker-end="url(#cs-arr)"/>

        <!-- 3. Exit Section -->
        <rect x="420" y="30" width="165" height="60" rx="5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="502" y="52" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0f172a">3. EXIT SECTION</text>
        <text x="502" y="68" text-anchor="middle" font-size="8" fill="#64748b">release(&amp;lock)</text>
        <text x="502" y="80" text-anchor="middle" font-size="7.5" fill="#059669">Signals waiting threads</text>

        <line x1="585" y1="60" x2="613" y2="60" stroke="#0284c7" stroke-width="2" marker-end="url(#cs-arr)"/>

        <!-- 4. Remainder Section -->
        <rect x="615" y="30" width="130" height="60" rx="5" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
        <text x="680" y="52" text-anchor="middle" font-size="9.5" font-weight="700" fill="#166534">4. REMAINDER</text>
        <text x="680" y="68" text-anchor="middle" font-size="8" fill="#15803d">Non-critical work</text>
        <text x="680" y="80" text-anchor="middle" font-size="7.5" fill="#64748b">Local computations</text>
      </svg>
    </div>

    <ol>
      <li>
        <strong>The Entry Section:</strong> The gateway protocol where a thread requests permission to access the shared resource. If another thread currently holds the critical region, the entry section must block the requesting thread (suspending it on a wait queue) or spin until the lock is vacated.
      </li>
      <li>
        <strong>The Critical Section:</strong> The isolated execution block containing the actual read-modify-write operations on the shared resource. While a thread is here, mutual exclusion is active.
      </li>
      <li>
        <strong>The Exit Section:</strong> The exit protocol executed immediately upon finishing shared state mutations. It releases ownership of the critical region, unblocks waiting threads, and updates internal lock metadata.
      </li>
      <li>
        <strong>The Remainder Section:</strong> The remainder of the program's code, performing independent computations on local variables, private stack memory, or unshared resources.
      </li>
    </ol>

    <h4>The Principle of Minimal Critical Section Scope</h4>
    <p>
      A cardinal rule of operating system engineering is to keep the critical section <strong>as small as humanly possible</strong>.
    </p>
    <p>
      Critical sections serialize execution: while Thread <i>A</i> is inside, no other core can make progress on that shared data. If an application holds a lock while performing disk I/O, network requests, or heavy cryptographic hashing:
    </p>
    <ul>
      <li>All other execution cores stall or sleep waiting for the lock, destroying multicore parallelism.</li>
      <li>According to <strong>Amdahl's Law</strong>, the maximum theoretical speedup of a program on an infinite number of processor cores is strictly limited by the fraction of execution time spent inside serialized critical sections:
        <pre><code>Speedup &le; 1 / Serial_Fraction</code></pre>
      </li>
      <li><strong>Engineering Invariant:</strong> Never perform I/O, allocate system memory, or execute long-running loops inside a critical section unless that exact I/O channel is the shared resource being protected.</li>
    </ul>

    <h4>The Naive Software Lock Paradox</h4>
    <p>
      Why can't we solve mutual exclusion with a simple software integer flag?
    </p>
    <p>
      Consider the most intuitive attempt by a programmer to protect a critical region using a shared variable <code>lock</code> (initialized to <code>0</code>, meaning unlocked):
    </p>

    <pre><code><span class="syn-cmt">/* NAIVE ATTEMPT: Flawed Software Lock Variable */</span>
<span class="syn-kw">int</span> lock = <span class="syn-num">0</span>; <span class="syn-cmt">/* 0 = unlocked, 1 = locked */</span>

<span class="syn-kw">void</span> worker() {
    <span class="syn-cmt">/* Entry Section */</span>
    <span class="syn-kw">while</span> (lock == <span class="syn-num">1</span>) {
        <span class="syn-cmt">/* Spin and wait until lock becomes 0 */</span>
    }
    lock = <span class="syn-num">1</span>; <span class="syn-cmt">/* Claim the lock */</span>

    <span class="syn-cmt">/* Critical Section */</span>
    balance += <span class="syn-num">100</span>;

    <span class="syn-cmt">/* Exit Section */</span>
    lock = <span class="syn-num">0</span>; <span class="syn-cmt">/* Release the lock */</span>
}</code></pre>

    <div class="math-callout">
      <strong>Why This Flawed Attempt Fails Catastrophically:</strong>
      <br>
      Notice the fatal circular dependency: <strong>the lock variable itself is a shared mutable resource!</strong>
      <br>
      Look at the preemption window between the <code>while</code> check and setting <code>lock = 1</code>:
      <ol>
        <li>Thread 1 checks <code>lock == 1</code>. It evaluates to <code>false</code> (lock is <code>0</code>).</li>
        <li><strong>Context Switch:</strong> Right before Thread 1 can execute <code>lock = 1</code>, the timer interrupt fires and deschedules Thread 1.</li>
        <li>Thread 2 is dispatched. It checks <code>lock == 1</code>. Because Thread 1 was preempted before setting the flag, <code>lock</code> is <em>still 0</em>!</li>
        <li>Thread 2 proceeds past the <code>while</code> loop, sets <code>lock = 1</code>, and enters the Critical Section.</li>
        <li>Thread 1 is rescheduled. It resumes execution at the instruction immediately following the <code>while</code> loop. It executes <code>lock = 1</code> and enters the Critical Section.</li>
      </ol>
      <strong>Result:</strong> Both Thread 1 and Thread 2 are now executing inside the Critical Section simultaneously! The flawed software lock suffers from the exact same race condition it was designed to prevent.
    </div>
    <p>
      This fundamental bootstrapping problem proves that software flags alone cannot guarantee mutual exclusion without underlying <strong>hardware atomic primitives</strong> or formal coordination algorithms (such as Peterson's Algorithm).
    </p>"""

def update_section_three():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>3. Critical Regions &amp; Mutual Exclusion</h3>"
    end_marker = "<h3>4. The Four Mandatory Conditions for Mutual Exclusion</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 3 markers.")
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
            "Expand Section 3 in Module 01 with critical region lifecycle and locks\n\n"
            "Detail the four-stage execution lifecycle, the minimal critical region\n"
            "principle, the flawed software lock paradox, and add a timeline diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_three():
        run_git_sync()
