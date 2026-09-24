#!/usr/bin/env python3
# =====================================================================
# fix.py: Insert Mars Pathfinder panorama image and attribution into Section 2
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "01-concurrency-hazards-livelock-starvation.html"
)

PATHFINDER_SECTION_WITH_IMAGE = r"""    <h3>2. Priority Inversion and The Mars Pathfinder Anomaly</h3>
    <p>
      Priority inversion represents one of the most insidious architectural failures in preemptive priority-based operating systems. It occurs when a high-priority task is indirectly delayed or preempted by a lower-priority task, subverting the core scheduling contract.
    </p>

    <!-- Mars Pathfinder Panorama Illustration -->
    <div style="margin: 20px 0; background: #ffffff; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
      <img src="../images/Mars-Pathfinder-panorama-large.jpg" alt="Mars Pathfinder Sagan Memorial Station Panorama" style="width: 100%; height: auto; display: block;">
      <div style="padding: 12px 16px; font-size: 0.82rem; color: var(--text-muted); background: #f8fafc; border-top: 1px solid var(--border); line-height: 1.5;">
        <strong style="color: var(--primary);">Figure 2.1:</strong> Panoramic view of the Martian surface from the Sagan Memorial Station (Mars Pathfinder landing site).
        <br>
        <em>Attribution:</em> <a href="https://commons.wikimedia.org/w/index.php?title=File:Mars_Pathfinder_panorama_large.jpg&oldid=1121259465" target="_blank" style="color: var(--accent); text-decoration: none;">Wikimedia Commons contributors</a> (Publisher: Wikimedia Commons; Page Version ID: 1121259465). Retrieved September 24, 2026.
      </div>
    </div>

    <h4>1. The Three-Task Dependency Chain</h4>
    <p>
      The classical priority inversion scenario involves three tasks across disparate static priority levels (<code>P_High &gt; P_Medium &gt; P_Low</code>). Understanding how these tasks interact requires tracing the OS scheduler's runqueue mechanics and mutex wait queues step by step:
    </p>
    <ol>
      <li>
        <strong>Initial State &amp; Resource Acquisition (T<sub>0</sub>):</strong>
        The low-priority task (<code>P_Low</code>) is scheduled and successfully acquires a shared mutual exclusion lock (mutex) protecting a critical resource (e.g., a shared hardware telemetry bus). While executing inside its critical section, <code>P_Low</code> is interrupted or its time slice expires.
      </li>
      <li>
        <strong>The Medium-Priority Preemption (T<sub>1</sub>):</strong>
        A medium-priority task (<code>P_Medium</code>), which does not require the shared mutex, becomes runnable (triggered by an I/O event or timer). Because <code>P_Medium</code> possesses a higher static priority than <code>P_Low</code> (<code>P_Medium &gt; P_Low</code>), the OS scheduler immediately preempts <code>P_Low</code>, saving its register context and placing <code>P_Medium</code> on the CPU. <code>P_Low</code> is now halted mid-critical section while still holding the lock.
      </li>
      <li>
        <strong>The High-Priority Blockade (T<sub>2</sub>):</strong>
        A critical high-priority task (<code>P_High</code>) becomes runnable. Because <code>P_High &gt; P_Medium</code>, the scheduler preempts <code>P_Medium</code> and allocates the CPU to <code>P_High</code>. <code>P_High</code> begins execution, but immediately encounters a synchronization barrier when attempting to acquire the mutex currently held by <code>P_Low</code>.
        <br><br>
        Per POSIX and real-time kernel semantics, <code>P_High</code> is blocked (moved from the active runqueue to the mutex's wait queue), and a context switch returns the CPU to <code>P_Medium</code>.
      </li>
      <li>
        <strong>The Inversion Lockup (T<sub>3</sub>):</strong>
        With <code>P_High</code> blocked waiting for the mutex, and <code>P_Low</code> unable to run because it lacks CPU time, <code>P_Medium</code> resumes execution and continues running indefinitely as long as it has compute-bound work.
        <br><br>
        <em>The Inversion Paradox:</em> <code>P_Medium</code> (medium priority) executes ahead of <code>P_High</code> (high priority) because <code>P_High</code> is indirectly dependent on <code>P_Low</code>, which is actively suppressed by <code>P_Medium</code>. The nominal priority ordering is completely inverted in practice.
      </li>
    </ol>
    <p style="margin-top: 12px;">
      This blockade can persist arbitrarily long—bounded only by the execution duration of <code>P_Medium</code>—frequently violating hard real-time deadlines and triggering watchdog timeouts in safety-critical embedded systems.
    </p>

    <h4>2. The Mars Pathfinder Priority Inversion Anomaly (July 1997)</h4>
    <p>
      Days after landing successfully on the Martian surface in July 1997, the Mars Pathfinder spacecraft—running the VxWorks preemptive priority-based real-time operating system—began experiencing sporadic, unexplained total system resets. While no scientific or telemetry data was permanently lost, each reset triggered a hard reboot that suspended data collection and delayed daily rover operations for hours.
    </p>
    <p>
      Contrary to dramatic popular accounts portraying the spacecraft as moments from catastrophic destruction, Pathfinder was functioning precisely as its defensive systems engineering intended. Its onboard watchdog timer noticed that core software tasks were stalling and executed clean reboots to clear the digital jam. However, isolating the root cause required forensic analysis of a classic priority inversion trap.
    </p>

    <h5>Architectural Context &amp; The Information Bus</h5>
    <p>
      Pathfinder utilized an internal <strong>"information bus"</strong>—a shared memory and communication region used to pass telemetry and sensor data between disparate instrument subsystems and lander components. Access to this bus was strictly synchronized using mutual exclusion semaphores (mutexes) to prevent race conditions during concurrent reads and writes.
    </p>
    <p>
      Three specific software tasks interacted across competing priority levels:
    </p>
    <ul>
      <li>
        <strong>The Meteorological Task (<code>P_Low</code> / <code>L</code>):</strong> An infrequent, low-priority background thread responsible for gathering atmospheric pressure, temperature, and wind data. When publishing its telemetry records, it acquired the information bus mutex, performed memory writes, and released the mutex.
      </li>
      <li>
        <strong>The Communications &amp; Science Data Task (<code>P_Medium</code> / <code>M</code>):</strong> A heavy, medium-priority task handling continuous background data formatting and radio transmission streams. Because it did not require the information bus mutex, it had no synchronization dependencies on <code>L</code>.
      </li>
      <li>
        <strong>The Information Bus Management Task (<code>P_High</code> / <code>H</code>):</strong> A critical, high-priority thread that ran frequently to move time-sensitive guidance and instrument data in and out of the information bus. It required frequent acquisition of the information bus mutex.
      </li>
    </ul>

    <h5>The Failure Cascade &amp; Watchdog Trigger</h5>
    <p>
      The anomalous execution sequence unfolded through an unfortunate alignment of task cadences:
    </p>
    <ol>
      <li>
        <strong>Step 1 (Mutex Lock):</strong> The low-priority meteorological task (<code>L</code>) scheduled and acquired the information bus mutex to write atmospheric sensor data.
      </li>
      <li>
        <strong>Step 2 (Preemption):</strong> Before <code>L</code> could finish its writes and release the mutex, an interrupt triggered the medium-priority communications task (<code>M</code>). Because <code>M &gt; L</code>, the scheduler preempted <code>L</code> and allocated the CPU to <code>M</code>. <code>L</code> remained suspended mid-critical section while holding the bus mutex.
      </li>
      <li>
        <strong>Step 3 (High-Priority Blockade):</strong> The high-priority information bus task (<code>H</code>) became runnable. Because <code>H &gt; M</code>, the scheduler preempted <code>M</code> and gave the CPU to <code>H</code>. <code>H</code> attempted to read the information bus, encountered the mutex held by <code>L</code>, and blocked—waiting for <code>L</code> to release it.
      </li>
      <li>
        <strong>Step 4 (Starvation &amp; System Reset):</strong> Control returned to <code>M</code> (the medium-priority task) because <code>H</code> was blocked and <code>L</code> was suppressed. <code>M</code> ran continuously, starving <code>L</code> of any CPU time. Because <code>L</code> could never run, it could never release the mutex. <code>H</code> remained blocked indefinitely.
      </li>
    </ol>
    <p>
      After a predetermined duration, the spacecraft's hardware <strong>watchdog timer</strong> noticed that the high-priority bus management task (<code>H</code>) had failed to check in within its mandated execution window. Assuming a fatal software deadlock or hardware lockup, the watchdog issued a hard reset command, rebooting the lander safely.
    </p>

    <h5>Debugging on Earth &amp; The Remote Patch</h5>
    <p>
      Back at NASA's Jet Propulsion Laboratory (JPL), engineers recreated the exact mission workload on a spacecraft replica rig in their lab with kernel event tracing enabled. After hours of tracing, an engineer running tests late into the night reproduced the system reset, confirming the priority inversion deadlock.
    </p>
    <p>
      The fix was exceptionally elegant. VxWorks mutex objects accept an initialization parameter determining whether <strong>Priority Inheritance</strong> should be enforced. When created, this parameter had been left disabled (set to <code>FALSE</code>) for performance optimization.
    </p>
    <p>
      Rather than attempting to recompile and re-flash the flight software stack across 100 million miles of interplanetary space, JPL engineers exploited a built-in feature: VxWorks included an online <strong>C language interpreter</strong> compiled directly into the launch image for debugging. Because the initialization symbols were preserved in the spacecraft's global symbol table, engineers uploaded a short C script that changed the mutex configuration variables from <code>FALSE</code> to <code>TRUE</code>.
    </p>
    <p>
      Once priority inheritance was active, whenever high-priority task <code>H</code> blocked on the mutex held by <code>L</code>, the kernel temporarily elevated <code>L</code>'s priority to match <code>H</code>. This prevented medium-priority task <code>M</code> from preempting <code>L</code>, allowing <code>L</code> to finish its critical section immediately, release the mutex, and unblock <code>H</code>. Zero further system resets occurred for the remainder of the mission.
    </p>

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

def insert_pathfinder_image():
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

    updated = content[:start_idx] + PATHFINDER_SECTION_WITH_IMAGE + "\n\n    <nav class=\"nav-bar\">" + content[end_idx + len(end_marker):]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"--> Successfully inserted Mars Pathfinder panorama and attribution into {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if insert_pathfinder_image():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Add Mars Pathfinder panorama image and citation to Module 01\n\n"
                "Insert responsive landscape panorama of Mars Pathfinder at the top of Section 2\n"
                "with full Wikimedia Commons bibliographic attribution metadata."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
