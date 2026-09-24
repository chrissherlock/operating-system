#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 4 in 01-race-conditions-critical-regions.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week04-concurrency-and-mutual-exclusion", "01-race-conditions-critical-regions.html")

EXPANDED_SECTION_FOUR = r"""    <h3>4. The Four Mandatory Conditions for Mutual Exclusion</h3>
    <p>
      Designing a mechanism to prevent race conditions is deceivingly difficult. A naive synchronization protocol might successfully keep two processes from colliding inside a critical region, but introduce subtle pathologies: deadlocking the system, freezing fast processes while slow processes compute unrelated code, or starving a process indefinitely.
    </p>
    <p>
      To be considered correct, robust, and general-purpose, any candidate solution to the mutual exclusion problem must satisfy <strong>all four of the following mandatory conditions</strong>:
    </p>

    <!-- Structural Diagram: The 4 Failure Modes -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 1.4: The Four Pathological Failure Modes of Broken Synchronization</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How flawed synchronization algorithms fail when any single condition is compromised.</div>

      <svg viewBox="0 0 760 210" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <!-- Panel 1: Condition 1 Violation (Safety Failure) -->
        <g transform="translate(15, 10)">
          <rect width="170" height="185" rx="5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
          <text x="12" y="24" font-size="9" font-weight="700" fill="#dc2626">1. SAFETY VIOLATION</text>
          <text x="12" y="38" font-size="8" fill="#64748b">Mutual Exclusion Failure</text>
          <rect x="15" y="52" width="140" height="70" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
          <text x="85" y="78" text-anchor="middle" font-size="9" font-weight="700" fill="#991b1b">COLLISION!</text>
          <text x="85" y="94" text-anchor="middle" font-size="8" fill="#7f1d1d">P1 &amp; P2 inside CS</text>
          <text x="85" y="108" text-anchor="middle" font-size="7.5" font-weight="700" fill="#dc2626">SIMULTANEOUSLY</text>
          <text x="12" y="146" font-size="7.5" fill="#475569">&bull; Memory corrupted.</text>
          <text x="12" y="160" font-size="7.5" fill="#475569">&bull; Non-atomic interleaved stores.</text>
        </g>

        <!-- Panel 2: Condition 2 Violation (Hardware Assumption) -->
        <g transform="translate(200, 10)">
          <rect width="170" height="185" rx="5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
          <text x="12" y="24" font-size="9" font-weight="700" fill="#d97706">2. HARDWARE ASSUMPTION</text>
          <text x="12" y="38" font-size="8" fill="#64748b">Speed / Clock Dependency</text>
          <rect x="15" y="52" width="140" height="70" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
          <text x="85" y="76" text-anchor="middle" font-size="8.5" font-weight="700" fill="#92400e">CLOCK DRIFT</text>
          <text x="85" y="92" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#b45309">delay(1000)</text>
          <text x="85" y="106" text-anchor="middle" font-size="7.5" fill="#78350f">Fails on faster CPU</text>
          <text x="12" y="146" font-size="7.5" fill="#475569">&bull; CPU GHz mismatch.</text>
          <text x="12" y="160" font-size="7.5" fill="#475569">&bull; Out-of-order reordering.</text>
        </g>

        <!-- Panel 3: Condition 3 Violation (Progress Failure) -->
        <g transform="translate(385, 10)">
          <rect width="170" height="185" rx="5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
          <text x="12" y="24" font-size="9" font-weight="700" fill="#0284c7">3. PROGRESS VIOLATION</text>
          <text x="12" y="38" font-size="8" fill="#64748b">Remainder Interference</text>
          <rect x="15" y="52" width="140" height="70" rx="4" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5"/>
          <text x="85" y="76" text-anchor="middle" font-size="8.5" font-weight="700" fill="#0369a1">STRICT ALTERNATION</text>
          <text x="85" y="92" text-anchor="middle" font-size="8" fill="#0284c7">P0 idle in remainder</text>
          <text x="85" y="106" text-anchor="middle" font-size="7.5" font-weight="700" fill="#0c4a6e">BLOCKS ready P1!</text>
          <text x="12" y="146" font-size="7.5" fill="#475569">&bull; Critical region is empty.</text>
          <text x="12" y="160" font-size="7.5" fill="#475569">&bull; Yet waiting process blocked.</text>
        </g>

        <!-- Panel 4: Condition 4 Violation (Starvation) -->
        <g transform="translate(570, 10)">
          <rect width="175" height="185" rx="5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
          <text x="12" y="24" font-size="9" font-weight="700" fill="#7c3aed">4. BOUNDED WAITING</text>
          <text x="12" y="38" font-size="8" fill="#64748b">Starvation / Livelock</text>
          <rect x="15" y="52" width="145" height="70" rx="4" fill="#f5f3ff" stroke="#7c3aed" stroke-width="1.5"/>
          <text x="87" y="76" text-anchor="middle" font-size="8.5" font-weight="700" fill="#5b21b6">STARVATION</text>
          <text x="87" y="92" text-anchor="middle" font-size="8" fill="#6d28d9">P1 bypassed forever</text>
          <text x="87" y="106" text-anchor="middle" font-size="7.5" fill="#4c1d95">By P2, P3, P4...</text>
          <text x="12" y="146" font-size="7.5" fill="#475569">&bull; No upper bound on waits.</text>
          <text x="12" y="160" font-size="7.5" fill="#475569">&bull; P1 hangs indefinitely.</text>
        </g>
      </svg>
    </div>

    <h4>Condition 1: Mutual Exclusion (Safety)</h4>
    <blockquote style="border-left: 4px solid var(--danger); padding: 8px 16px; margin: 12px 0; background: #fef2f2; color: #991b1b; font-weight: 600;">
      "No two processes may be simultaneously inside their critical regions."
    </blockquote>
    <p>
      This is the fundamental <strong>safety property</strong> of synchronization: <em>nothing bad happens</em>.
    </p>
    <ul>
      <li>If Process <i>P</i><sub>1</sub> has entered the critical region for a resource, Process <i>P</i><sub>2</sub> must be prevented from entering until <i>P</i><sub>1</sub> leaves.</li>
      <li><strong>Violation Failure Mode:</strong> If Condition 1 fails, concurrent threads interleave Load-Modify-Store sequences across shared variables, causing race conditions, corrupted pointer metadata, and permanent state destruction.</li>
    </ul>

    <h4>Condition 2: Hardware Independence</h4>
    <blockquote style="border-left: 4px solid var(--warning); padding: 8px 16px; margin: 12px 0; background: #fffbeb; color: #92400e; font-weight: 600;">
      "No assumptions may be made about speeds or the number of CPUs."
    </blockquote>
    <p>
      The synchronization algorithm must be mathematically invariant to hardware performance:
    </p>
    <ul>
      <li><strong>Clock Frequency Invariance:</strong> You cannot assume that Process <i>A</i> executes at the same instruction rate as Process <i>B</i>. One core may run at 3.5 GHz while another is throttled to 800 MHz to conserve power.</li>
      <li><strong>Topology Invariance:</strong> The protocol must function identically whether executed on a single uniprocessor CPU with preemptive time-slicing, a symmetric multicore processor (SMP) with 128 cores, or an asymmetric system with heterogeneous cores (e.g., performance vs. efficiency cores).</li>
      <li><strong>Violation Failure Mode (Timing Delay Loops):</strong> Programmers occasionally write delay loops like <code>for (int i = 0; i &lt; 100000; i++);</code> expecting another thread to finish an operation. On a faster processor or under heavy interrupt load, the delay finishes too early, causing the synchronization barrier to collapse.</li>
    </ul>

    <h4>Condition 3: Progress (Non-Interference)</h4>
    <blockquote style="border-left: 4px solid var(--accent); padding: 8px 16px; margin: 12px 0; background: #f0f9ff; color: #0369a1; font-weight: 600;">
      "No process running outside its critical region may block other processes."
    </blockquote>
    <p>
      This is a foundational <strong>liveness property</strong>: <em>if no process is currently in the critical region, and some processes want to enter, only those processes competing to enter may participate in the decision, and the selection cannot be postponed indefinitely.</em>
    </p>

    <h5>The Classic Failure: Strict Alternation (Turn Variable)</h5>
    <p>
      To understand how Condition 3 is violated, examine the classic flawed attempt known as <strong>Strict Alternation</strong>:
    </p>

    <pre><code><span class="syn-cmt">/* FLAWED ATTEMPT: Strict Alternation via Turn Variable */</span>
<span class="syn-kw">int</span> turn = <span class="syn-num">0</span>; <span class="syn-cmt">/* turn == 0 -&gt; P0 runs; turn == 1 -&gt; P1 runs */</span>

<span class="syn-cmt">/* --- Process 0 Code --- */</span>
<span class="syn-kw">while</span> (<span class="syn-kw">true</span>) {
    <span class="syn-kw">while</span> (turn != <span class="syn-num">0</span>);      <span class="syn-cmt">/* Entry section: wait for turn */</span>
    <span class="syn-fn">critical_region</span>();
    turn = <span class="syn-num">1</span>;               <span class="syn-cmt">/* Exit section: pass turn to P1 */</span>
    <span class="syn-fn">remainder_section</span>();    <span class="syn-cmt">/* Remainder: non-critical work */</span>
}

<span class="syn-cmt">/* --- Process 1 Code --- */</span>
<span class="syn-kw">while</span> (<span class="syn-kw">true</span>) {
    <span class="syn-kw">while</span> (turn != <span class="syn-num">1</span>);      <span class="syn-cmt">/* Entry section: wait for turn */</span>
    <span class="syn-fn">critical_region</span>();
    turn = <span class="syn-num">0</span>;               <span class="syn-cmt">/* Exit section: pass turn to P0 */</span>
    <span class="syn-fn">remainder_section</span>();    <span class="syn-cmt">/* Remainder: non-critical work */</span>
}</code></pre>

    <div class="math-callout">
      <strong>Why Strict Alternation Violates Condition 3:</strong>
      <ol>
        <li>Suppose <strong>Process 0</strong> is very fast: it enters the critical region, leaves, sets <code>turn = 1</code>, and enters its long <code>remainder_section()</code> to compute complex physics equations.</li>
        <li><strong>Process 1</strong> enters the critical region, completes its work, sets <code>turn = 0</code>, finishes its short remainder section, and loops back to enter the critical region a second time.</li>
        <li>Process 1 checks <code>while (turn != 1)</code>. Because Process 0 is still busy in its remainder section, <code>turn</code> is <strong>still 0</strong>!</li>
        <li><strong>The Violation:</strong> Process 1 is <strong>blocked</strong> from entering the critical region&mdash;<em>even though the critical region is completely empty!</em></li>
      </ol>
      Process 0 is running <em>outside</em> its critical region, yet it is actively preventing Process 1 from entering. This is a catastrophic violation of Condition 3.
    </div>

    <h4>Condition 4: Bounded Waiting (Starvation Immunity)</h4>
    <blockquote style="border-left: 4px solid #7c3aed; padding: 8px 16px; margin: 12px 0; background: #f5f3ff; color: #5b21b6; font-weight: 600;">
      "No process should have to wait forever to enter its critical region."
    </blockquote>
    <p>
      A process requesting entry to a critical region must eventually be granted admission. There must exist a deterministic upper bound on the number of times other processes are allowed to enter their critical sections after a process has declared its intent to enter:
    </p>
    <ul>
      <li><strong>Livelock:</strong> Two or more processes continuously change their state in response to each other without making actual progress (e.g., both politely backing off and re-requesting a lock in exact lockstep).</li>
      <li><strong>Starvation:</strong> A process waits indefinitely because the arbitration policy consistently favors newly arriving processes or higher-priority threads (e.g., an uncoordinated spinlock where a thread on a remote NUMA node consistently loses bus arbitration to local cores).</li>
    </ul>

    <h4>Comprehensive Criteria Comparison Matrix</h4>
    <div style="overflow-x: auto; margin: 20px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 12px; width: 25%;">Synchronization Candidate</th>
            <th style="padding: 10px 12px; width: 18%;">Cond 1: Mutex</th>
            <th style="padding: 10px 12px; width: 18%;">Cond 2: Hardware Ind.</th>
            <th style="padding: 10px 12px; width: 18%;">Cond 3: Progress</th>
            <th style="padding: 10px 12px; width: 21%;">Cond 4: Bounded Wait</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Disabling Interrupts</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 600;">Yes (Uniprocessor only)</td>
            <td style="padding: 10px 12px; color: #dc2626; font-weight: 700;">NO (Fails on SMP)</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 600;">Yes</td>
            <td style="padding: 10px 12px; color: #dc2626; font-weight: 700;">NO (User code can hang OS)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Naive Lock Variable</td>
            <td style="padding: 10px 12px; color: #dc2626; font-weight: 700;">NO (Race on lock itself)</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 600;">Yes</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 600;">Yes</td>
            <td style="padding: 10px 12px; color: #dc2626; font-weight: 700;">NO (Unbounded race)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Strict Alternation</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 600;">Yes</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 600;">Yes</td>
            <td style="padding: 10px 12px; color: #dc2626; font-weight: 700;">NO (Remainder blocks entry)</td>
            <td style="padding: 10px 12px; color: #dc2626; font-weight: 700;">NO (Blocked if peer halts)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #f0fdf4;">
            <td style="padding: 10px 12px; font-weight: 700; color: #166534;">Peterson's Algorithm</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 700;">Yes</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 700;">Yes</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 700;">Yes</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 700;">Yes</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #f0fdf4;">
            <td style="padding: 10px 12px; font-weight: 700; color: #166534;">Hardware TSL / CAS</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 700;">Yes</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 700;">Yes</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 700;">Yes</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 700;">Yes (With fair queueing)</td>
          </tr>
        </tbody>
      </table>
    </div>"""

def update_section_four():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>4. The Four Mandatory Conditions for Mutual Exclusion</h3>"
    end_marker = '<nav class="nav-bar" style="margin-top: 36px;'

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 4 boundaries.")
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
            "Expand Section 4 in Module 01 with four conditions for mutual exclusion\n\n"
            "Detail each condition with formal definitions, failure mode traces,\n"
            "strict alternation analysis, a comparison matrix, and an SVG diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_four():
        run_git_sync()
