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

def expand_three_task_chain_fully():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    old_sub_one = """      <h4>1. The Three-Task Dependency Chain</h4>
      <p>
        The classical priority inversion scenario involves three tasks across disparate static priority levels (P_High &gt; P_Medium &gt; P_Low):
      </p>
      <ol>
        <li><strong>Resource Acquisition:</strong> The low-priority task (P_Low) acquires a shared mutual exclusion lock (mutex) protecting a hardware bus or memory region.</li>
        <li><strong>The Inversion Vector:</strong> While P_Low holds the mutex, a medium-priority task (P_Medium) becomes ready to run. Because P_Medium has a higher static priority than P_Low, the scheduler preempts P_Low.</li>
        <li><strong>The Indirect Blockade:</strong> High-priority task (P_High) preempts P_Medium when it requires execution, but immediately blocks when attempting to acquire the mutex held by P_Low. However, P_Low cannot finish its critical section because it is being continuously starved by P_Medium.</li>
        <li><strong>The Result:</strong> P_High is blocked by P_Low, which is preempted by P_Medium. The relative priorities are effectively inverted: P_Medium runs ahead of P_High despite having a lower nominal importance.</li>
      </ol>"""

    expanded_sub_one = """      <h4>1. The Three-Task Dependency Chain &amp; Execution Timeline</h4>
      <p>
        The classical priority inversion scenario involves three concurrent threads or tasks operating across disparate static priority levels (<code>P_High &gt; P_Medium &gt; P_Low</code>). To fully understand why this creates a systemic vulnerability, we must trace the precise microarchitectural interactions between the OS scheduler's runqueue, CPU register contexts, and mutex wait queues step by step across a strict chronological timeline:
      </p>

      <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 20px 0;">
        <div style="font-weight: 700; color: var(--primary); margin-bottom: 12px; font-size: 0.95rem;">Chronological Timeline of Priority Inversion (T<sub>0</sub> &rarr; T<sub>4</sub>)</div>

        <ul style="margin: 0; padding-left: 18px; font-size: 0.9rem; line-height: 1.6;">
          <li>
            <strong>T<sub>0</sub> (Mutex Lock Acquisition):</strong>
            The low-priority task (<code>P_Low</code>) is scheduled by the kernel, enters its designated critical section, and successfully acquires mutual exclusion lock <code>M</code> protecting a shared resource (e.g., hardware bus registers). While executing inside the critical section, its time slice elapses or an asynchronous event occurs.
          </li>
          <li>
            <strong>T<sub>1</sub> (Medium-Priority Preemption):</strong>
            An unrelated medium-priority task (<code>P_Medium</code>) becomes runnable (triggered by an I/O completion or network packet). Because <code>P_Medium &gt; P_Low</code>, the OS scheduler immediately preempts <code>P_Low</code>, saves its register context to its Thread Control Block (TCB), and places <code>P_Medium</code> onto the active CPU runqueue.
            <br>
            <em>Crucial State:</em> <code>P_Low</code> is suspended mid-critical section while actively holding lock <code>M</code>.
          </li>
          <li>
            <strong>T<sub>2</sub> (High-Priority Blockade):</strong>
            A critical high-priority task (<code>P_High</code>) wakes up to process time-sensitive data. Because <code>P_High &gt; P_Medium</code>, the scheduler preempts <code>P_Medium</code> and allocates the CPU to <code>P_High</code>. <code>P_High</code> begins execution, but immediately encounters a synchronization barrier when attempting to acquire lock <code>M</code>.
            <br>
            Per kernel synchronization semantics, <code>P_High</code> is blocked (moved from the active runqueue to lock <code>M</code>'s wait queue), and a context switch returns the CPU back to <code>P_Medium</code>.
          </li>
          <li>
            <strong>T<sub>3</sub> (The Inversion Lockup):</strong>
            <code>P_Medium</code> resumes execution on the CPU. Because <code>P_High</code> is blocked waiting for lock <code>M</code>, and <code>P_Low</code> cannot be scheduled because <code>P_Medium</code> outranks it, <code>P_Medium</code> runs continuously. <code>P_Low</code> remains starved of CPU time and cannot finish its critical section to release lock <code>M</code>.
          </li>
          <li>
            <strong>T<sub>4</sub> (The Scheduling Contract Violation):</strong>
            The system reaches a state where <code>P_Medium</code> (medium priority) executes indefinitely ahead of <code>P_High</code> (high priority). The nominal priority ordering is completely inverted in practice, violating real-time execution guarantees.
          </li>
        </ul>
      </div>

      <p>
        This microarchitectural dead-end exposes a foundational flaw in naive priority schedulers: static priority checks are completely blind to dynamic data dependencies managed through synchronization primitives. Without runtime feedback mechanisms, intermediate tasks can inadvertently starve critical operations for arbitrary durations.
      </p>"""

    if old_sub_one not in content:
        print("Warning: Old subsection one string not found exactly.")
        return False

    new_content = content.replace(old_sub_one, expanded_sub_one)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"--> Successfully expanded Section 2.1 in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if expand_three_task_chain_fully():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Expand Section 2.1 in Module 01 on the Three-Task Dependency Chain\n\n"
                "Provide exhaustive microarchitectural breakdown of task timelines (T0 to T4),\n"
                "runqueue transitions, and mutex wait queue mechanics during priority inversion."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
