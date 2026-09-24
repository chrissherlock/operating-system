#!/usr/bin/env python3
# =====================================================================
# fix.py: Replace YouTube iframe with clickable high-res thumbnail card
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "01-concurrency-hazards-livelock-starvation.html"
)

THUMBNAIL_SECTION = r"""    <h3>2. Priority Inversion and The Mars Pathfinder Anomaly</h3>
    <p>
      Priority inversion represents one of the most insidious architectural failures in preemptive priority-based operating systems. It occurs when a high-priority task is indirectly delayed or preempted by a lower-priority task, subverting the core scheduling contract.
    </p>

    <h4>1. The Three-Task Dependency Chain</h4>
    <p>
      The classical priority inversion scenario involves three tasks across disparate priority levels ($P_{\text{High}} &gt; P_{\text{Medium}} &gt; P_{\text{Low}}$):
    </p>
    <ol>
      <li><strong>Resource Acquisition:</strong> The low-priority task ($P_{\text{Low}}$) acquires a shared mutual exclusion lock (mutex) protecting a hardware bus or memory region.</li>
      <li><strong>The Inversion Vector:</strong> While $P_{\text{Low}}$ holds the mutex, a medium-priority task ($P_{\text{Medium}}$) becomes ready to run. Because $P_{\text{Medium}}$ has a higher static priority than $P_{\text{Low}}$, the scheduler preempts $P_{\text{Low}}$.</li>
      <li><strong>The Indirect Blockade:</strong> High-priority task ($P_{\text{High}}$) preempts $P_{\text{Medium}}$ when it requires execution, but immediately blocks when attempting to acquire the mutex held by $P_{\text{Low}}$. However, $P_{\text{Low}}$ cannot finish its critical section because it is being continuously starved by $P_{\text{Medium}}$.</li>
      <li><strong>The Result:</strong> $P_{\text{High}}$ is blocked by $P_{\text{Low}}$, which is preempted by $P_{\text{Medium}}$. The relative priorities are effectively inverted: $P_{\text{Medium}}$ runs ahead of $P_{\text{High}}$ despite having a lower nominal importance.</li>
    </ol>

    <div class="math-callout" style="background: #fef2f2; border-left-color: #dc2626;">
      <strong style="color: #991b1b;">Priority Inversion Inequality:</strong>
      <br>
      Nominal Priority Ordering: <code>P_High &gt; P_Medium &gt; P_Low</code>
      <br>
      Effective Execution Order under Inversion: <code>P_Medium runs while P_High starves</code>
    </div>

    <h4>2. The Mars Pathfinder Mission Failure (July 1997)</h4>
    <p>
      Days after landing on Mars, the spacecraft running the VxWorks real-time operating system began experiencing sporadic, unexplained total system resets that delayed daily science operations:
    </p>
    <ul>
      <li><strong>The Culprits:</strong> An infrequent, low-priority meteorological data-gathering task ($L$) held a mutex protecting the shared "information bus" memory. A high-priority information bus management task ($H$) needed this mutex frequently. A medium-priority communications and science data task ($M$) handled continuous background data transfers.</li>
      <li><strong>The Failure Cascade:</strong> When $L$ held the mutex, $M$ would preempt it. $H$ would then attempt to read the bus, block on $L$, and starve because $M$ consumed available CPU cycles.</li>
      <li><strong>The Watchdog Trigger:</strong> An onboard watchdog timer noticed that high-priority communications task $H$ had failed to check in within its allotted window, assumed a fatal kernel lockup, and commanded a hard system reboot.</li>
    </ul>

    <h4>3. The Priority Inheritance Protocol (PIP) Solution</h4>
    <p>
      Engineers diagnosed and fixed the bug remotely from Earth by uploading a one-line C patch via the onboard debugging interpreter to enable <strong>Priority Inheritance</strong>:
    </p>
    <ul>
      <li>Under PIP, when a high-priority task blocks on a mutex held by a low-priority task, the kernel <strong>temporarily boosts the low-priority task's priority</strong> to match $P_{\text{High}}$.</li>
      <li>This prevents medium-priority tasks ($M$) from preempting $L$. $L$ finishes its critical section rapidly, releases the mutex, drops back to its base priority, and allows $H$ to execute immediately.</li>
    </ul>

    <p style="margin-top: 24px; font-weight: 600; color: var(--primary);">
      Visual Walkthrough &mdash; Priority Inversion &amp; Mars Pathfinder Analysis:
    </p>

    <!-- YouTube Thumbnail Card -->
    <a href="https://www.youtube.com/watch?v=gpttZW2hBMM" target="_blank" style="display: block; position: relative; max-width: 640px; border-radius: 8px; overflow: hidden; border: 1px solid var(--border); box-shadow: 0 4px 12px rgba(0,0,0,0.06); text-decoration: none; background: #000; margin: 16px 0; transition: transform 0.15s ease, box-shadow 0.15s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 20px rgba(0,0,0,0.12)';" onmouseout="this.style.transform='none'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.06)';">
      <img src="https://img.youtube.com/vi/gpttZW2hBMM/hqdefault.jpg" alt="Priority Inversion Explained Thumbnail" style="width: 100%; display: block; opacity: 0.9; transition: opacity 0.15s;" onmouseover="this.style.opacity='1';" onmouseout="this.style.opacity='0.9';">
      <!-- Play Button Overlay -->
      <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 68px; height: 48px; background: rgba(23, 23, 23, 0.85); border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
        <div style="width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-left: 18px solid #ffffff; margin-left: 3px;"></div>
      </div>
      <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 10px 14px; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: #fff; font-size: 0.88rem; font-weight: 600;">
        Watch Video: Priority Inversion &amp; Mars Pathfinder Analysis &rarr;
      </div>
    </a>"""

def apply_thumbnail_fix():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>2. Priority Inversion and The Mars Pathfinder Anomaly</h3>"
    end_marker = "<nav class=\"nav-bar\">"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Markers not found.")
        return False

    updated = content[:start_idx] + THUMBNAIL_SECTION + "\n\n    <nav class=\"nav-bar\">" + content[end_idx + len(end_marker):]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"--> Successfully replaced iframe with thumbnail card in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if apply_thumbnail_fix():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Replace YouTube iframe with responsive thumbnail link in Module 01\n\n"
                "Swap out embedded iframe for a high-res thumbnail preview card linking\n"
                "directly to the YouTube video in a new tab, completely resolving Error 153."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
