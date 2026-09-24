#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 2.1 on the Three-Task Dependency Chain
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "01-concurrency-hazards-livelock-starvation.html"
)

# Read existing file, replace subsection 1, and write back
def expand_three_task_chain():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    old_sub_one = """      <h4>1. The Three-Task Dependency Chain</h4>
      <p>
        The classical priority inversion scenario involves three tasks across disparate priority levels (P_High &gt; P_Medium &gt; P_Low):
      </p>
      <ol>
        <li><strong>Resource Acquisition:</strong> The low-priority task (P_Low) acquires a shared mutual exclusion lock (mutex) protecting a hardware bus or memory region.</li>
        <li><strong>The Inversion Vector:</strong> While P_Low holds the mutex, a medium-priority task (P_Medium) becomes ready to run. Because P_Medium has a higher static priority than P_Low, the scheduler preempts P_Low.</li>
        <li><strong>The Indirect Blockade:</strong> High-priority task (P_High) preempts P_Medium when it requires execution, but immediately blocks when attempting to acquire the mutex held by P_Low. However, P_Low cannot finish its critical section because it is being continuously starved by P_Medium.</li>
        <li><strong>The Result:</strong> P_High is blocked by P_Low, which is preempted by P_Medium. The relative priorities are effectively inverted: P_Medium runs ahead of P_High despite having a lower nominal importance.</li>
      </ol>"""

    expanded_sub_one = """      <h4>1. The Three-Task Dependency Chain</h4>
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
      </p>"""

    if old_sub_one not in content:
        print("Warning: Exact old subsection string not found, attempting broader replacement.")
        return False

    new_content = content.replace(old_sub_one, expanded_sub_one)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"--> Successfully expanded Section 2.1 in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if expand_three_task_chain():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Expand Section 2.1 in Module 01 on the Three-Task Dependency Chain\n\n"
                "Provide deep microarchitectural breakdown of preemption states, semaphore\n"
                "queues, and register states during priority inversion."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
