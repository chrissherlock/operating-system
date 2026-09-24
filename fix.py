#!/usr/bin/env python3
# =====================================================================
# fix.py: Integrate Priority Inheritance Protocol section into Mars Pathfinder
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "01-concurrency-hazards-livelock-starvation.html"
)

RESTRUCTURED_MODULE_01 = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Module 01: Concurrency Hazards, Livelock, Starvation &amp; PIP - COSC240</title>
  <style>
    :root {
      --primary: #0f172a;
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --border: #e2e8f0;
      --card-bg: #ffffff;
      --text: #334155;
      --text-muted: #64748b;
      --bg: #f8fafc;
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: var(--font-sans);
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 24px;
    }
    .container { max-width: 1040px; margin: 0 auto; }
    .nav-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #ffffff;
      border: 1px solid var(--border);
      padding: 12px 20px;
      border-radius: 8px;
      margin-bottom: 24px;
    }
    .nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--accent);
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 6px;
      transition: background 0.15s ease;
    }
    .nav-btn:hover { background: #f0f9ff; }
    .content-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 36px;
      margin-bottom: 28px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    h1 { margin: 0 0 12px 0; font-size: 1.85rem; color: var(--primary); letter-spacing: -0.02em; }
    h3 { font-size: 1.25rem; color: var(--primary); margin-top: 32px; border-bottom: 2px solid var(--border); padding-bottom: 8px; }
    h4 { font-size: 1.05rem; color: var(--primary); margin-top: 24px; }
    h5 { font-size: 0.95rem; color: var(--primary); margin-top: 18px; }
    p, li { font-size: 0.95rem; color: var(--text); }
    .math-callout {
      background: #f8fafc;
      border-left: 4px solid var(--accent);
      padding: 16px;
      margin: 20px 0;
      border-radius: 0 8px 8px 0;
      font-size: 0.9rem;
    }
    code { font-family: var(--font-mono); font-size: 0.88rem; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; color: #0f172a; }
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="index.html" class="nav-btn">&larr; Week 6 Hub</a>
      <a href="index.html" class="nav-btn">&#127968; Week 6 Hub</a>
      <a href="02-deadlock-characterization-coffman-conditions.html" class="nav-btn">Module 02 &rarr;</a>
    </nav>

    <div class="content-card">
      <span style="font-size: 0.75rem; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.05em;">Module 01 &bull; COSC240</span>
      <h1>Concurrency Hazards: Livelock, Starvation, and Priority Inversion</h1>
      <p style="font-size: 1.05rem; color: var(--text-muted); margin-bottom: 24px;">
        Explore the spectrum of concurrent failure modes. Contrast CPU-burning livelock with blocking deadlocks, study scheduling starvation, and analyze Priority Inheritance Protocols (PIP) using the Mars Pathfinder anomaly.
      </p>

      <h3>1. The Spectrum of Concurrency Hazards</h3>
      <p>
        When designing concurrent multithreaded systems, preventing race conditions via mutexes and semaphores is only the first hurdle. Even when mutual exclusion is correctly implemented, thread interactions can lead to systemic operational failures where tasks fail to make forward progress.
      </p>
      <p>
        Operating systems theory classifies these failures into three distinct concurrency hazards: <strong>Deadlock</strong>, <strong>Livelock</strong>, and <strong>Starvation</strong>. While superficially similar because all three prevent threads from completing, their underlying microarchitectural mechanics and CPU utilization profiles are fundamentally different.
      </p>

      <!-- Structural Comparison Table -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0; overflow-x: auto;">
        <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Table 1.1: Microarchitectural Comparison of Concurrency Failure Modes</div>
        <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">Contrasting thread execution states, CPU consumption, and recovery triggers across system anomalies.</div>

        <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem;">
          <thead>
            <tr style="background: #f1f5f9; text-align: left;">
              <th style="padding: 10px; border: 1px solid var(--border);">Hazard Type</th>
              <th style="padding: 10px; border: 1px solid var(--border);">Thread Execution State</th>
              <th style="padding: 10px; border: 1px solid var(--border);">CPU Utilization</th>
              <th style="padding: 10px; border: 1px solid var(--border);">Root System Cause</th>
              <th style="padding: 10px; border: 1px solid var(--border);">Remediation Strategy</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="padding: 10px; border: 1px solid var(--border); font-weight: 700; color: #dc2626;">Deadlock</td>
              <td style="padding: 10px; border: 1px solid var(--border);">Blocked / Sleeping (TASK_UNINTERRUPTIBLE)</td>
              <td style="padding: 10px; border: 1px solid var(--border); color: #16a34a; font-weight: 600;">0% (Zero Burn)</td>
              <td style="padding: 10px; border: 1px solid var(--border);">Simultaneous satisfaction of the Four Coffman Conditions.</td>
              <td style="padding: 10px; border: 1px solid var(--border);">Lock ordering, Banker's Algorithm, or process termination.</td>
            </tr>
            <tr style="background: #f8fafc;">
              <td style="padding: 10px; border: 1px solid var(--border); font-weight: 700; color: #d97706;">Livelock</td>
              <td style="padding: 10px; border: 1px solid var(--border);">Active / Running (Executing instructions continuously)</td>
              <td style="padding: 10px; border: 1px solid var(--border); color: #dc2626; font-weight: 600;">100% (Busy Waiting / Burn)</td>
              <td style="padding: 10px; border: 1px solid var(--border);">Overly polite error-recovery logic causing continuous state oscillation.</td>
              <td style="padding: 10px; border: 1px solid var(--border);">Randomized exponential backoff or lock relinquishment jitter.</td>
            </tr>
            <tr>
              <td style="padding: 10px; border: 1px solid var(--border); font-weight: 700; color: #0284c7;">Starvation</td>
              <td style="padding: 10px; border: 1px solid var(--border);">Ready / Runnable (Willing to run, but bypassed by scheduler)</td>
              <td style="padding: 10px; border: 1px solid var(--border); color: #475569; font-weight: 600;">Near 0% (For starved thread)</td>
              <td style="padding: 10px; border: 1px solid var(--border);">Unfair scheduling heuristics prioritizing high-priority threads indefinitely.</td>
              <td style="padding: 10px; border: 1px solid var(--border);">Aging algorithms, priority boosting, and fair queueing (CFS).</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h4>Detailed Mechanics of Livelock</h4>
      <p>
        Livelock occurs when two or more processes continuously change their internal states in response to changes in the other processes without doing any useful work. The classic real-world analogue is two polite people walking toward each other in a narrow corridor: both step to the left at the same time, then both step to the right at the same time, blocking each other indefinitely while actively moving back and forth.
      </p>
      <div class="math-callout" style="background: #fef2f2; border-left-color: #d97706;">
        <strong style="color: #b45309;">Why Livelock Burns CPU Cycles:</strong>
        <br>
        Unlike deadlocked threads that yield the CPU and sleep, livelocked threads are fully active. A thread caught in a livelock executes lock acquisition attempts, fails due to contention, catches the failure exception, yields or backs off briefly, and immediately loops to retry. The OS scheduler continuously schedules these threads because they remain in the RUNNABLE state, driving core CPU utilization to 100% while accomplishing zero computational progress.
      </div>

      <h4>Real-World Architectural Examples of Livelock</h4>
      <ul>
        <li>
          <strong>Network Collision Backoff Livelock:</strong>
          In decentralized Ethernet or wireless collision domains, if two nodes transmit packets simultaneously, a collision occurs. If both nodes implement deterministic backoff algorithms (waiting an identical fixed interval before retransmitting), they will collide again in lockstep, oscillating forever between transmission and collision states. <em>Defense:</em> Implementing randomized exponential backoff (e.g., Ethernet CSMA/CD).
        </li>
        <li>
          <strong>Optimistic Concurrency Control (OCC) Database Livelock:</strong>
          In database management systems utilizing optimistic locking, two transactions read the same record, compute modifications, and attempt to commit. The DBMS validates that neither record was modified in the interim. Finding a conflict, the DBMS aborts Transaction A, rolls back, and restarts it. Simultaneously, Transaction B aborts, rolls back, and restarts. If their execution cadences overlap perfectly, they will abort and restart each other in an infinite livelock loop.
        </li>
      </ul>

      <h3>2. Priority Inversion and The Mars Pathfinder Anomaly</h3>
      <p>
        Priority inversion represents one of the most insidious architectural failures in preemptive priority-based operating systems. It occurs when a high-priority task is indirectly delayed or preempted by a lower-priority task, subverting the core scheduling contract.
      </p>

      <h4>1. The Three-Task Dependency Chain</h4>
      <p>
        The classical priority inversion scenario involves three tasks across disparate static priority levels (P_High &gt; P_Medium &gt; P_Low):
      </p>
      <ol>
        <li><strong>Resource Acquisition:</strong> The low-priority task (P_Low) acquires a shared mutual exclusion lock (mutex) protecting a hardware bus or memory region.</li>
        <li><strong>The Inversion Vector:</strong> While P_Low holds the mutex, a medium-priority task (P_Medium) becomes ready to run. Because P_Medium has a higher static priority than P_Low, the scheduler preempts P_Low.</li>
        <li><strong>The Indirect Blockade:</strong> High-priority task (P_High) preempts P_Medium when it requires execution, but immediately blocks when attempting to acquire the mutex held by P_Low. However, P_Low cannot finish its critical section because it is being continuously starved by P_Medium.</li>
        <li><strong>The Result:</strong> P_High is blocked by P_Low, which is preempted by P_Medium. The relative priorities are effectively inverted: P_Medium runs ahead of P_High despite having a lower nominal importance.</li>
      </ol>

      <div class="math-callout" style="background: #fef2f2; border-left-color: #dc2626;">
        <strong style="color: #991b1b;">Priority Inversion Inequality:</strong>
        <br>
        Nominal Priority Ordering: <code>P_High &gt; P_Medium &gt; P_Low</code>
        <br>
        Effective Execution Order under Inversion: <code>P_Medium runs while P_High starves</code>
      </div>

      <h4>2. The Mars Pathfinder Priority Inversion Anomaly (July 1997)</h4>

      <!-- Mars Pathfinder Panorama Illustration -->
      <div style="margin: 20px 0; background: #ffffff; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
        <img src="../images/Mars-Pathfinder-panorama-large.jpg" alt="Mars Pathfinder Sagan Memorial Station Panorama" style="width: 100%; height: auto; display: block;">
        <div style="padding: 12px 16px; font-size: 0.82rem; color: var(--text-muted); background: #f8fafc; border-top: 1px solid var(--border); line-height: 1.5;">
          <strong style="color: var(--primary);">Figure 2.1:</strong> Panoramic view of the Martian surface from the Sagan Memorial Station (Mars Pathfinder landing site).
          <br>
          <em>Attribution:</em> <a href="https://commons.wikimedia.org/w/index.php?title=File:Mars_Pathfinder_panorama_large.jpg&oldid=1121259465" target="_blank" style="color: var(--accent); text-decoration: none;">Wikimedia Commons contributors</a> (Publisher: Wikimedia Commons; Page Version ID: 1121259465). Retrieved September 24, 2026.
        </div>
      </div>

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

      <h5>Debugging on Earth &amp; The Remote Patch (The PIP Solution)</h5>
      <p>
        Back at NASA's Jet Propulsion Laboratory (JPL), engineers recreated the exact mission workload on a spacecraft replica rig in their lab with kernel event tracing enabled. After hours of tracing, an engineer running tests late into the night reproduced the system reset, confirming the priority inversion deadlock.
      </p>
      <p>
        The solution implemented was the <strong>Priority Inheritance Protocol (PIP)</strong>. VxWorks mutex objects accept an initialization parameter determining whether priority inheritance should be enforced. When created, this parameter had been left disabled (set to <code>FALSE</code>) for performance optimization.
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
      </a>
    </div>

    <nav class="nav-bar">
      <a href="index.html" class="nav-btn">&larr; Week 6 Hub</a>
      <a href="index.html" class="nav-btn">&#127968; Week 6 Hub</a>
      <a href="02-deadlock-characterization-coffman-conditions.html" class="nav-btn">Module 02 &rarr;</a>
    </nav>
  </div>
</body>
</html>
"""

def update_module_file():
    os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(RESTRUCTURED_MODULE_01.strip() + "\n")
    print(f"--> Successfully restructured Module 01 at {TARGET_FILE}")

if __name__ == "__main__":
    update_module_file()
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Integrate Priority Inheritance Protocol section into Mars Pathfinder case study\n\n"
            "Fold Section 3 (PIP Solution) directly into the Mars Pathfinder anomaly\n"
            "subsection as its concluding architectural analysis."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git note: {e}")
