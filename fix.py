#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 2.2 on the Mars Pathfinder Mission Failure
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "01-concurrency-hazards-livelock-starvation.html"
)

def expand_mars_pathfinder():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    old_sub_two = """      <h4>2. The Mars Pathfinder Mission Failure (July 1997)</h4>
      <p>
        Days after landing on Mars, the spacecraft running the VxWorks real-time operating system began experiencing sporadic, unexplained total system resets that delayed daily science operations:
      </p>
      <ul>
        <li><strong>The Culprits:</strong> An infrequent, low-priority meteorological data-gathering task (L) held a mutex protecting the shared information bus memory. A high-priority information bus management task (H) needed this mutex frequently. A medium-priority communications and science data task (M) handled continuous background data transfers.</li>
        <li><strong>The Failure Cascade:</strong> When L held the mutex, M would preempt it. H would then attempt to read the bus, block on L, and starve because M consumed available CPU cycles.</li>
        <li><strong>The Watchdog Trigger:</strong> An onboard watchdog timer noticed that high-priority communications task H had failed to check in within its allotted window, assumed a fatal kernel lockup, and commanded a hard system reboot.</li>
      </ul>"""

    expanded_sub_two = """      <h4>2. The Mars Pathfinder Mission Failure (July 1997)</h4>
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
      </p>"""

    if old_sub_two not in content:
        print("Warning: Old subsection two not found exactly.")
        return False

    new_content = content.replace(old_sub_two, expanded_sub_two)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"--> Successfully expanded Section 2.2 in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if expand_mars_pathfinder():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Expand Section 2.2 in Module 01 on the Mars Pathfinder Anomaly\n\n"
                "Provide exhaustive technical breakdown of VxWorks tasks, bus mutexes,\n"
                "watchdog timers, lab reproduction, and remote C interpreter patching."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
