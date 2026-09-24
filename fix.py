#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 1 of 01-concurrency-hazards-livelock-starvation.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "01-concurrency-hazards-livelock-starvation.html"
)

EXPANDED_SECTION_ONE = r"""    <h3>1. The Spectrum of Concurrency Hazards</h3>
    <p>
      When designing concurrent multithreaded systems, preventing race conditions via mutexes and semaphores is only the first hurdle. Even when mutual exclusion is correctly implemented, thread interactions can lead to systemic operational failures where tasks fail to make forward progress.
    </p>
    <p>
      Operating systems theory classifies these failures into three distinct concurrency hazards: <strong>Deadlock</strong>, <strong>Livelock</strong>, and <strong>Starvation</strong>. While superficially similar because all three prevent threads from completing, their underlying microarchitectural mechanics and CPU utilization profiles are fundamentally different.
    </p>

    <!-- Structural Comparison Table -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0; overflow-x: auto;">
      <div style="font-weight: 700; font-size: 0.95ln; color: #0f172a; margin-bottom: 4px;">Table 1.1: Microarchitectural Comparison of Concurrency Failure Modes</div>
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
            <td style="padding: 10px; border: 1px solid var(--border);">Blocked / Sleeping (<code style="font-size: 0.78rem;">TASK_UNINTERRUPTIBLE</code>)</td>
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

    <h4>1. Detailed Mechanics of Livelock</h4>
    <p>
      Livelock occurs when two or more processes continuously change their internal states in response to changes in the other processes without doing any useful work. The classic real-world analogue is two polite people walking toward each other in a narrow corridor: both step to the left at the same time, then both step to the right at the same time, blocking each other indefinitely while actively moving back and forth.
    </p>
    <div class="math-callout" style="background: #fef2f2; border-left-color: #d97706;">
      <strong style="color: #b45309;">Why Livelock Burns CPU Cycles:</strong>
      <br>
      Unlike deadlocked threads that yield the CPU and sleep, livelocked threads are fully active. A thread caught in a livelock executes lock acquisition attempts, fails due to contention, catches the failure exception, yields or backs off briefly, and immediately loops to retry. The OS scheduler continuously schedules these threads because they remain in the <code>RUNNABLE</code> state, driving core CPU utilization to 100% while accomplishing zero computational progress.
    </div>

    <h5>Real-World Architectural Examples of Livelock</h5>
    <ul>
      <li>
        <strong>Network Collision Backoff Livelock:</strong>
        In decentralized Ethernet or wireless collision domains, if two nodes transmit packets simultaneously, a collision occurs. If both nodes implement naive deterministic backoff algorithms (waiting an identical fixed interval before retransmitting), they will collide again in lockstep, oscillating forever between transmission and collision states. <em>Defense:</em> Implementing randomized exponential backoff (e.g., Ethernet CSMA/CD).
      </li>
      <li>
        <strong>Optimistic Concurrency Control (OCC) Database Livelock:</strong>
        In database management systems utilizing optimistic locking, two transactions read the same record, compute modifications, and attempt to commit. The DBMS validates that neither record was modified in the interim. Finding a conflict, the DBMS aborts Transaction A, rolls back, and restarts it. Simultaneously, Transaction B aborts, rolls back, and restarts. If their execution cadences overlap perfectly, they will abort and restart each other in an infinite livelock loop.
      </li>
    </ul>

    <h4>2. Starvation vs. Deadlock</h4>
    <p>
      A common point of confusion in systems engineering is distinguishing between deadlock and starvation:
    </p>
    <ul>
      <li><strong>Deadlock is a group pathology:</strong> A deadlocked thread can never escape its blocked state on its own; it requires external intervention (killing a process, force-releasing a lock, or rebooting). Furthermore, deadlock involves a closed set of interacting processes.</li>
      <li><strong>Starvation is a scheduling injustice:</strong> A starved thread is fully capable of running and is not part of a circular wait dependency. It remains unexecuted simply because the CPU scheduler's priority heuristics continuously favor other tasks. If the higher-priority load subsides, the starved thread will eventually execute normally.</li>
    </ul>"""

def update_section_one():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>1. The Spectrum of Concurrency Hazards</h3>"
    end_marker = "<!-- Directed Narrative Stepper"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 1 boundaries in Module 01.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_ONE + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 1 in {TARGET_FILE}")
    return True

def run_git_sync():
    status = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
    if not status:
        print("--> Working tree is clean. Nothing to commit.")
        return

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 1 in Module 01 on Concurrency Hazards and Livelock\n\n"
            "Detail formal state machine contrasts between deadlock, livelock, and\n"
            "starvation, including network protocol and database OCC livelock examples."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_one():
        run_git_sync()
