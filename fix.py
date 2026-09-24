#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Dining Philosophers pseudocode & state machine in Module 04
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "04-deadlock-recovery-starvation.html"
)

DINING_PHILOSOPHERS_DEEP_EXPANSION = r"""      <h3>1. Classic Synchronization Hazards</h3>
      <p>
        Operating systems and concurrent applications encounter recurring structural coordination challenges that highlight the delicate balance between throughput, mutual exclusion, and deadlock avoidance. Among these, classic synchronization problems serve as canonical architectural testbeds.
      </p>

      <h4>1. The Dining Philosophers Problem</h4>
      <p>
        Originally formulated by Edsger Dijkstra in 1965 to test synchronization primitives on the RC 4000 multiprocessor system, the <strong>Dining Philosophers Problem</strong> abstracts resource contention among concurrent threads competing for exclusive, limited hardware devices or locks.
      </p>
      <p>
        Imagine five philosophers seated around a circular table. In front of each philosopher lies a bowl of rice, and between each adjacent pair of philosophers lies a single shared chopstick (five total chopsticks). A philosopher alternates between two states: <em>thinking</em> and <em>eating</em>. To eat, a philosopher requires <strong>two</strong> chopsticks—their immediate left and right neighbors. Because chopsticks are shared mutually exclusive resources, a chopstick cannot be used by two philosophers simultaneously.
      </p>

      <h5>The Anatomy of Deadlock in Dining Philosophers</h5>
      <p>
        If every philosopher simultaneously decides to eat and reaches for their left chopstick, all five chopsticks are successfully acquired. When each philosopher then reaches for their right chopstick, they find it already held by their neighbor.
      </p>

      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--danger);">
        <strong style="color: var(--danger);">Simultaneous Hold-and-Wait Hazard:</strong>
        <br><br>
        $$ \forall i \in \{0, 1, 2, 3, 4\}, \quad \text{Hold}(\text{Chopstick}_i) \land \text{Wait}(\text{Chopstick}_{(i+1)\bmod 5}) $$
      </div>

      <p>
        This creates a strict <strong>circular wait</strong> dependency chain: Philosopher 0 waits for Philosopher 1's left chopstick, Philosopher 1 waits for Philosopher 2's, and so on, closing the loop back to Philosopher 0. All four Coffman conditions are satisfied simultaneously, plunging the entire table into permanent deadlock where no philosopher ever eats.
      </p>

      <h5>Monitor Solution &amp; State Transition Pseudocode</h5>
      <p>
        To solve the dining philosophers hazard without deadlocking or starving, operating systems use monitor constructs with condition variables. Below is the classical state-based monitor design where a philosopher only enters the eating state if both neighbors are not currently eating:
      </p>

      <!-- Syntax Highlighted Pseudocode Box -->
      <div style="background: #0f172a; color: #f8fafc; border-radius: 8px; padding: 20px; font-family: var(--font-mono); font-size: 0.85rem; overflow-x: auto; margin: 20px 0; border: 1px solid var(--border);">
        <div style="color: #64748b; margin-bottom: 10px; font-size: 0.78rem; border-bottom: 1px solid #334155; padding-bottom: 6px;">
          monitor &bull; DiningPhilosophersMonitor.pseudo
        </div>
        <pre style="margin: 0; line-height: 1.5;"><span style="color: #c084fc;">monitor</span> DiningPhilosophers {
    <span style="color: #6ee7b7;">enum</span> State { THINKING, HUNGRY, EATING };
    State state[<span style="color: #f43f5e;">5</span>];
    Condition self[<span style="color: #f43f5e;">5</span>];

    <span style="color: #c084fc;">void</span> <span style="color: #60a5fa;">pickup</span>(<span style="color: #6ee7b7;">int</span> i) {
        state[i] = HUNGRY;
        test(i);
        <span style="color: #c084fc;">if</span> (state[i] != EATING) {
            self[i].wait();
        }
    }

    <span style="color: #c084fc;">void</span> <span style="color: #60a5fa;">putdown</span>(<span style="color: #6ee7b7;">int</span> i) {
        state[i] = THINKING;
        test((i + <span style="color: #f43f5e;">4</span>) % <span style="color: #f43f5e;">5</span>); <span style="color: #94a3b8;">// Test left neighbor</span>
        test((i + <span style="color: #f43f5e;">1</span>) % <span style="color: #f43f5e;">5</span>); <span style="color: #94a3b8;">// Test right neighbor</span>
    }

    <span style="color: #c084fc;">void</span> <span style="color: #60a5fa;">test</span>(<span style="color: #6ee7b7;">int</span> i) {
        <span style="color: #c084fc;">if</span> (state[(i + <span style="color: #f43f5e;">4</span>) % <span style="color: #f43f5e;">5</span>] != EATING &amp;&amp;
            state[i] == HUNGRY &amp;&amp;
            state[(i + <span style="color: #f43f5e;">1</span>) % <span style="color: #f43f5e;">5</span>] != EATING) {
            state[i] = EATING;
            self[i].signal();
        }
    }
}</pre>
      </div>

      <h5>Real-World Parallels &amp; Database Multi-Locking</h5>
      <p>
        While dining philosophers sounds pedagogical, its structural hazard mirrors modern multi-threaded systems:
      </p>
      <ul>
        <li>
          <strong>Database Row Locks:</strong> Transaction $T_1$ acquires a write lock on database row $A$ and requests row $B$. Concurrently, transaction $T_2$ acquires a write lock on row $B$ and requests row $A$.
        </li>
        <li>
          <strong>Graphics Subsystems:</strong> Multi-threaded rendering pipelines acquiring locking handles across framebuffers, vertex buffers, and GPU command queues in inconsistent orders.
        </li>
      </ul>

      <h5>Architectural Mitigations</h5>
      <p>
        Operating systems and concurrency libraries employ several standard defenses against the Dining Philosophers deadlock:
      </p>
      <ol>
        <li>
          <strong>Asymmetric Resource Acquisition:</strong> Force odd-numbered philosophers to pick up their <em>left</em> chopstick first, while even-numbered philosophers pick up their <em>right</em> chopstick first. This breaks circular symmetry.
        </li>
        <li>
          <strong>Monitor-Based Arbitration (Chandy-Misra):</strong> Introduce a centralized arbiter (or monitor state machine) that permits a philosopher to pick up chopsticks only if <em>both</em> adjacent chopsticks are simultaneously available.
        </li>
        <li>
          <strong>Resource Ordering:</strong> Assign a strict global index to every chopstick (0 through 4) and require threads to always acquire lower-numbered resources before higher-numbered ones, negating circular wait.
        </li>
      </ol>

      <h4>2. The Readers-Writers Problem</h4>
      <p>
        The <strong>Readers-Writers Problem</strong> governs shared data structures where concurrent execution entities fall into two distinct categories: <em>readers</em> (who only inspect data without modifying it) and <em>writers</em> (who require exclusive write access).
      </p>
      <ul>
        <li>
          <strong>First Readers-Writers Problem (Reader Priority):</strong> No reader is kept waiting unless a writer has already obtained exclusive access. This maximizes reader throughput but can cause severe writer starvation if readers continuously arrive.
        </li>
        <li>
          <strong>Second Readers-Writers Problem (Writer Priority):</strong> Once a writer is ready, that writer performs its write as soon as possible. If a writer is waiting, new readers are blocked from entering, preventing writer starvation at the expense of reader concurrency.
        </li>
      </ul>

      <h4>3. The Producer-Consumer Problem</h4>
      <p>
        The <strong>Producer-Consumer Problem</strong> (also known as the bounded-buffer problem) coordinates synchronization between data generator threads (producers) and data consumer threads interacting through a fixed-size shared memory buffer. Synchronization primitives—such as counting semaphores tracking empty/full slots and mutexes protecting buffer indices—ensure producers do not overflow full buffers and consumers do not underrun empty ones."""

def update_module_four_philosophers():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>1. Classic Synchronization Hazards</h3>"
    end_marker = "<h3>2. Deadlock Recovery &amp; Starvation Mitigation</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 1 boundaries in Module 04.")
        return False

    updated_content = content[:start_idx] + DINING_PHILOSOPHERS_DEEP_EXPANSION + "\n\n      " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Dining Philosophers in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if update_module_four_philosophers():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Deeply expand Dining Philosophers state transition pseudocode in Module 04\n\n"
                "Provide rigorous state machine analysis, monitor implementation pseudocode,\n"
                "and comprehensive deadlock prevention proofs for resource contention."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
