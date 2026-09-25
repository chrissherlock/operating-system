#!/usr/bin/env python3
# =====================================================================
# fix.py: Add accessible Deadlock explanation to Module 02
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

NEW_SECTION_1_AND_2 = r"""      <!-- ================================================================= -->
      <!-- SECTION 1: INTUITIVE FOUNDATIONS & WHAT IS DEADLOCK                -->
      <!-- ================================================================= -->
      <h3>1. What Is Deadlock? The Intuitive Foundation</h3>
      <p>
        In multi-threaded programming, threads pause and wait all the time. When a thread requests disk I/O, waits for a network packet, or sleeps on a timer, waiting is normal, safe, and temporary. The operating system places the thread in a <code>BLOCKED</code> queue, and when the hardware finishes the transfer, an interrupt fires and the thread transitions back to <code>READY</code>.
      </p>
      <p>
        <strong>Deadlock is fundamentally different.</strong> Deadlock is not long waiting or slow performance—it is a condition of <strong>permanent, unrecoverable system arrest</strong>. A set of threads is deadlocked when every thread in the set is waiting for a resource that can only be released by another thread in that exact same set.
      </p>
      <p>
        Because every thread in the circle is asleep waiting for someone else, none of them can ever run to execute the unlock call. Without external intervention from the kernel or an administrator killing a process, the threads will remain frozen forever.
      </p>

      <!-- Physical Gridlock Analogy -->
      <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid var(--success); padding: 16px 20px; border-radius: 0 8px 8px 0; margin: 20px 0;">
        <strong style="color: #15803d; font-size: 0.95rem;">The Physical Intuition: Four-Way Traffic Gridlock</strong>
        <p style="font-size: 0.88rem; color: #166534; margin: 8px 0 0 0; line-height: 1.55;">
          Picture four cars arriving at the exact same moment at an unmarked, narrow four-way intersection from the North, East, South, and West. Each driver creeps forward into their quadrant of the intersection:
        </p>
        <ul style="font-size: 0.85rem; color: #166534; margin: 8px 0 0 0; padding-left: 20px; line-height: 1.5;">
          <li>Car 1 (North) enters the intersection, but cannot proceed South because Car 2 blocks the lane.</li>
          <li>Car 2 (East) enters, but cannot proceed West because Car 3 blocks the lane.</li>
          <li>Car 3 (South) enters, but cannot proceed North because Car 4 blocks the lane.</li>
          <li>Car 4 (West) enters, but cannot proceed East because Car 1 blocks the lane.</li>
        </ul>
        <p style="font-size: 0.86rem; color: #166534; margin: 8px 0 0 0; line-height: 1.55;">
          No car can move forward because its target lane is occupied. No car can reverse because the cars behind them block any retreat (<em>no preemption</em>). Every driver is waiting for the driver ahead to move first. The result is total gridlock: no driver can ever proceed under their own power.
        </p>
      </div>

      <h4>The Classic Software Example: Lock Ordering Inversion</h4>
      <p>
        In operating systems and application code, deadlocks arise when multiple concurrent threads request the same locks in conflicting orders:
      </p>

      <!-- Syntax-Highlighted Code Comparison -->
      <div style="background: #0f172a; color: #f8fafc; border-radius: 8px; padding: 18px; font-family: var(--font-mono); font-size: 0.84rem; overflow-x: auto; margin: 16px 0;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
          <div>
            <span style="color: #38bdf8; font-weight: bold;">Thread 1: Transfer(Account A &rarr; B)</span>
            <pre style="margin: 8px 0 0 0; padding: 0; background: none; color: #e2e8f0; line-height: 1.5;">pthread_mutex_lock(&lock_A);
<span style="color: #64748b;">// <-- Preemption / context switch!</span>
pthread_mutex_lock(&lock_B);

balance_A -= amount;
balance_B += amount;

pthread_mutex_unlock(&lock_B);
pthread_mutex_unlock(&lock_A);</pre>
          </div>
          <div>
            <span style="color: #fbbf24; font-weight: bold;">Thread 2: Transfer(Account B &rarr; A)</span>
            <pre style="margin: 8px 0 0 0; padding: 0; background: none; color: #e2e8f0; line-height: 1.5;">pthread_mutex_lock(&lock_B);
<span style="color: #64748b;">// <-- Preemption / context switch!</span>
pthread_mutex_lock(&lock_A);

balance_B -= amount;
balance_A += amount;

pthread_mutex_unlock(&lock_A);
pthread_mutex_unlock(&lock_B);</pre>
          </div>
        </div>
      </div>

      <p>
        Consider what happens during concurrent execution:
      </p>
      <ol style="font-size: 0.92rem; line-height: 1.65;">
        <li>Thread 1 executes and successfully locks <code>lock_A</code>.</li>
        <li>The operating system preempts Thread 1 and switches to Thread 2.</li>
        <li>Thread 2 executes and successfully locks <code>lock_B</code>.</li>
        <li>Thread 2 attempts to lock <code>lock_A</code>. Because Thread 1 already holds it, Thread 2 is put to sleep.</li>
        <li>The OS switches back to Thread 1. Thread 1 attempts to lock <code>lock_B</code>. Because Thread 2 holds it, Thread 1 is also put to sleep.</li>
      </ol>
      <p>
        Both threads are now asleep waiting for each other. Neither thread will ever wake up on its own.
      </p>

      <h4>Formal Mathematical Definition</h4>
      <p>
        Let $P = \{P_1, P_2, \dots, P_n\}$ be a finite set of concurrent processes, and let $R = \{R_1, R_2, \dots, R_m\}$ represent the available resource types in the operating system.
      </p>
      <p>
        A subset of processes $P' \subset P$ is in a <strong>deadlock state</strong> if and only if every process in $P'$ is waiting for an event that only another process in $P'$ can cause:
      </p>

      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--accent);">
        <strong style="color: var(--primary);">Closed-Set Deadlock Condition:</strong>
        <br><br>
        $$\forall P_i \in P', \quad \text{State}(P_i) = \text{BLOCKED} \quad (\text{waiting on resource } R_j \text{ held by } P_k \in P')$$
      </div>

      <!-- ================================================================= -->
      <!-- SECTION 2: THE FOUR COFFMAN CONDITIONS                             -->
      <!-- ================================================================= -->
      <h3>2. The Four Coffman Conditions</h3>"""

def rewrite_module_content():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "      <h3>1. Formal Definition of System Deadlock</h3>"
    end_marker = "      <h3>2. The Four Coffman Conditions</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate boundary markers in target file.")
        return False

    # Replace old Section 1 with the comprehensive intuitive explanation and formal definition
    updated_content = content[:start_idx] + NEW_SECTION_1_AND_2 + content[end_idx + len(end_marker):]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully integrated intuitive explanation into {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if rewrite_module_content():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Add intuitive deadlock primer and lock inversion to Week 6 Module 02\n\n"
                "Prepend four-way intersection analogy, lock inversion walkthrough, and\n"
                "intuitive framing before formal set definition and Coffman conditions."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
