#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Dining Philosophers section in Module 04
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "04-deadlock-recovery-starvation.html"
)

DINING_PHILOSOPHERS_MASSIVE = r"""      <h3>1. Classic Synchronization Hazards</h3>
      <p>
        Operating systems and concurrent applications encounter recurring structural coordination challenges that highlight the delicate balance between throughput, mutual exclusion, and deadlock avoidance. Among these, classic synchronization problems serve as canonical architectural testbeds to prove that concurrency primitives do not introduce deadlocks, livelocks, or starvation.
      </p>

      <h4>1. The Dining Philosophers Problem</h4>
      <p>
        Originally formulated by Edsger Dijkstra in 1965 to test synchronization primitives on the RC 4000 multiprogramming system, the <strong>Dining Philosophers Problem</strong> is the foundational archetype for multi-resource allocation among competing processes. It abstracts the challenges of allocating shared, mutually exclusive devices (such as I/O channels, memory banks, or database table locks) without causing deadlock or starvation.
      </p>

      <h5>1. Problem Geometry &amp; Mathematical Formulation</h5>
      <p>
        Consider five philosophers sitting around a circular table. In front of each philosopher is a plate of noodles. Between each pair of adjacent plates lies a single shared chopstick (five total chopsticks). Each philosopher alternates between two primary states: <em>thinking</em> and <em>eating</em>.
      </p>
      <ul>
        <li>Let the philosophers be indexed as $P_0, P_1, P_2, P_3, P_4$.</li>
        <li>Let the chopsticks be modeled as binary mutual exclusion locks $C_0, C_1, C_2, C_3, C_4$.</li>
        <li>A philosopher $P_i$ sits between chopstick $C_i$ (to their left) and chopstick $C_{(i+1) \bmod 5}$ (to their right).</li>
      </ul>
      <p>
        A philosopher can only eat when holding <strong>both</strong> their immediate left and right chopsticks simultaneously. Because each chopstick is a strictly non-shareable resource ($C_k \in \{0, 1\}$), adjacent philosophers cannot eat concurrently:
      </p>

      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--accent);">
        <strong style="color: var(--primary);">Concurrency Invariant:</strong>
        <br><br>
        $$ \text{State}(P_i) = \text{EATING} \implies \text{State}(P_{(i+4)\bmod 5}) \neq \text{EATING} \quad \land \quad \text{State}(P_{(i+1)\bmod 5}) \neq \text{EATING} $$
        <p style="margin: 8px 0 0 0; font-size: 0.88rem; color: var(--text);">
          At most $\lfloor 5/2 \rfloor = 2$ non-adjacent philosophers can eat simultaneously in an optimal schedule.
        </p>
      </div>

      <h5>2. Failure Mode 1: Deadlock via Lockstep Contention</h5>
      <p>
        Consider the naive concurrency implementation where each philosopher executes the following routine:
      </p>
      <pre><code>// Naive Philosopher Routine (Deadlock Prone)
void philosopher(int i) {
    while (true) {
        think();
        wait(chopstick[i]);                 // Grab left chopstick
        wait(chopstick[(i + 1) % 5]);       // Grab right chopstick
        eat();
        signal(chopstick[i]);              // Release left chopstick
        signal(chopstick[(i + 1) % 5]);     // Release right chopstick
    }
}</code></pre>
      <p>
        If all five philosophers simultaneously decide to eat and invoke <code>wait(chopstick[i])</code>, each philosopher successfully claims their left chopstick. When each philosopher subsequently issues <code>wait(chopstick[(i + 1) % 5])</code>, every right chopstick is already locked by their clockwise neighbor.
      </p>
      <p>
        Every philosopher is permanently blocked. The system satisfies all <strong>Four Coffman Conditions</strong> simultaneously:
      </p>
      <ol>
        <li><strong>Mutual Exclusion:</strong> Chopsticks are exclusive locks; no two threads share a chopstick.</li>
        <li><strong>Hold and Wait:</strong> Every philosopher $P_i$ holds $C_i$ while waiting to acquire $C_{(i+1)\bmod 5}$.</li>
        <li><strong>No Preemption:</strong> A chopstick cannot be forcibly taken from a waiting philosopher.</li>
        <li><strong>Circular Wait:</strong> A closed directed cycle exists in the Resource Allocation Graph:
          $$ P_0 \to C_1 \to P_1 \to C_2 \to P_2 \to C_3 \to P_3 \to C_4 \to P_4 \to C_0 \to P_0 $$
        </li>
      </ol>

      <h5>3. Failure Mode 2: Livelock via Naive Preemption</h5>
      <p>
        A naive attempt to prevent deadlock is to eliminate the <em>Hold-and-Wait</em> condition using non-blocking lock acquisition (such as <code>pthread_mutex_trylock()</code>). If a philosopher acquires their left chopstick but finds their right chopstick busy, they release the left chopstick, sleep for a moment, and retry:
      </p>
      <pre><code>// Livelock Hazard
void philosopher_trylock(int i) {
    while (true) {
        think();
        acquire(chopstick[i]);
        if (!try_acquire(chopstick[(i + 1) % 5])) {
            release(chopstick[i]);          // Back off to prevent deadlock
            continue;                       // Retry from the start
        }
        eat();
        release(chopstick[i]);
        release(chopstick[(i + 1) % 5]);
    }
}</code></pre>
      <p>
        While this technically eliminates static deadlock, it introduces a dangerous <strong>livelock</strong> hazard. If all five philosophers pick up their left chopstick simultaneously, fail to acquire their right chopstick, release their left chopstick in unison, and immediately retry at identical intervals, the threads enter a synchronized polite-retreat loop. The system consumes 100% CPU time executing state transitions without any philosopher ever eating.
      </p>

      <h5>4. Failure Mode 3: Starvation via Neighbor Collusion</h5>
      <p>
        Even if deadlock and livelock are avoided, a concurrency protocol may still suffer from <strong>starvation (indefinite deferral)</strong>. Consider an asymmetric or priority-based scheduler where Philosopher $P_0$ and Philosopher $P_2$ eat alternately. Whenever $P_0$ finishes, $P_2$ starts; whenever $P_2$ finishes, $P_0$ starts.
      </p>
      <p>
        Philosopher $P_1$ (sitting between $P_0$ and $P_2$) requires $C_1$ and $C_2$. Because either $C_1$ or $C_2$ is continuously held by $P_0$ or $P_2$, $P_1$ never finds both chopsticks free simultaneously. Although the system as a whole exhibits liveness (throughput &gt; 0), thread $P_1$ starves indefinitely.
      </p>

      <h5>5. Four Rigorous Architectural Mitigations</h5>
      <p>
        Operating systems and distributed systems employ four standard strategies to solve the Dining Philosophers problem cleanly:
      </p>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
        <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 16px;">
          <strong style="color: var(--primary); font-size: 0.95rem;">1. Asymmetric Acquisition (Dijkstra)</strong>
          <p style="font-size: 0.85rem; color: var(--text); margin-top: 8px; line-height: 1.5;">
            Break circular symmetry by requiring odd-numbered philosophers to pick up their <em>left</em> chopstick first and then their right, while even-numbered philosophers pick up their <em>right</em> chopstick first.
          </p>
          <div style="font-size: 0.8rem; font-family: var(--font-mono); background: #ffffff; border: 1px solid var(--border); border-radius: 4px; padding: 6px 10px;">
            Odd: Left &rarr; Right<br>
            Even: Right &rarr; Left
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 6px;">
            <strong>Proof:</strong> At least one adjacent pair of philosophers will compete for the exact same chopstick first, preventing all five from acquiring one chopstick simultaneously.
          </p>
        </div>

        <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 16px;">
          <strong style="color: var(--primary); font-size: 0.95rem;">2. Global Resource Hierarchy (Havender)</strong>
          <p style="font-size: 0.85rem; color: var(--text); margin-top: 8px; line-height: 1.5;">
            Assign a global monotonic index $0 \dots 4$ to all chopsticks. Every philosopher must always acquire their lower-numbered chopstick before requesting their higher-numbered one.
          </p>
          <div style="font-size: 0.8rem; font-family: var(--font-mono); background: #ffffff; border: 1px solid var(--border); border-radius: 4px; padding: 6px 10px;">
            P4 requests C0 before C4<br>
            (since 0 &lt; 4)
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 6px;">
            <strong>Proof:</strong> Imposes a strict partial order on lock acquisition, mathematically proving that no directed cycle can ever form in the RAG.
          </p>
        </div>

        <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 16px;">
          <strong style="color: var(--primary); font-size: 0.95rem;">3. Bounded Room Capacity (Counting Semaphore)</strong>
          <p style="font-size: 0.85rem; color: var(--text); margin-top: 8px; line-height: 1.5;">
            Use a counting semaphore initialized to $N - 1 = 4$ to restrict access to the dining room. At most four philosophers may sit at the table at any given time.
          </p>
          <div style="font-size: 0.8rem; font-family: var(--font-mono); background: #ffffff; border: 1px solid var(--border); border-radius: 4px; padding: 6px 10px;">
            Semaphore table = 4;<br>
            wait(table); ... signal(table);
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 6px;">
            <strong>Proof:</strong> By Pigeonhole Principle, with at most 4 philosophers and 5 chopsticks, at least one philosopher is guaranteed to obtain two chopsticks and eat.
          </p>
        </div>

        <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 16px;">
          <strong style="color: var(--primary); font-size: 0.95rem;">4. Monitor State Machine (Chandy-Misra)</strong>
          <p style="font-size: 0.85rem; color: var(--text); margin-top: 8px; line-height: 1.5;">
            Encapsulate the state of each philosopher in a synchronized monitor. A philosopher transitions to <code>EATING</code> only if neither neighbor is currently eating.
          </p>
          <div style="font-size: 0.8rem; font-family: var(--font-mono); background: #ffffff; border: 1px solid var(--border); border-radius: 4px; padding: 6px 10px;">
            test(i): (left != EATING) &amp;&amp;<br>
            (right != EATING) &amp;&amp; (self == HUNGRY)
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 6px;">
            <strong>Proof:</strong> Atomically evaluates and commits two-lock acquisition within a critical section, making partial hold-and-wait impossible.
          </p>
        </div>
      </div>

      <h5>Monitor Solution: Complete Implementation</h5>
      <p>
        The monitor-based solution represents the standard modern approach to multi-resource synchronization. Below is the complete state-based monitor implementation with condition variables:
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
            self[i].wait();             <span style="color: #94a3b8;">// Suspend until both neighbors finish</span>
        }
    }

    <span style="color: #c084fc;">void</span> <span style="color: #60a5fa;">putdown</span>(<span style="color: #6ee7b7;">int</span> i) {
        state[i] = THINKING;
        test((i + <span style="color: #f43f5e;">4</span>) % <span style="color: #f43f5e;">5</span>);            <span style="color: #94a3b8;">// Test left neighbor ((i-1) mod 5)</span>
        test((i + <span style="color: #f43f5e;">1</span>) % <span style="color: #f43f5e;">5</span>);            <span style="color: #94a3b8;">// Test right neighbor ((i+1) mod 5)</span>
    }

    <span style="color: #c084fc;">void</span> <span style="color: #60a5fa;">test</span>(<span style="color: #6ee7b7;">int</span> i) {
        <span style="color: #c084fc;">if</span> (state[(i + <span style="color: #f43f5e;">4</span>) % <span style="color: #f43f5e;">5</span>] != EATING &amp;&amp;
            state[i] == HUNGRY &amp;&amp;
            state[(i + <span style="color: #f43f5e;">1</span>) % <span style="color: #f43f5e;">5</span>] != EATING) {
            state[i] = EATING;
            self[i].signal();           <span style="color: #94a3b8;">// Awaken philosopher if waiting</span>
        }
    }

    <span style="color: #c084fc;">void</span> <span style="color: #60a5fa;">init</span>() {
        <span style="color: #c084fc;">for</span> (<span style="color: #6ee7b7;">int</span> i = <span style="color: #f43f5e;">0</span>; i &lt; <span style="color: #f43f5e;">5</span>; i++) {
            state[i] = THINKING;
        }
    }
}</pre>
      </div>

      <h5>6. Real-World Systems Parallels</h5>
      <p>
        The Dining Philosophers problem maps directly to practical architectural challenges across systems programming:
      </p>
      <ul>
        <li>
          <strong>Relational Database Multi-Row Locking:</strong> When two transactions require write access to overlapping sets of rows across separate tables, unordered lock acquisition immediately recreates the circular wait condition. Databases enforce strict global lock ordering (or implement wait-for-graph cycle detection with transaction aborts) to recover.
        </li>
        <li>
          <strong>Dual-Ported RAM &amp; Memory Banks:</strong> In multi-core DSPs and GPU execution units, shared memory banks can service only one access per clock cycle. Cross-thread access patterns that demand dual-bank ownership must be scheduled asymmetrically to prevent pipeline stalling.
        </li>
      </ul>"""

def apply_dining_philosophers_expansion():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>1. Classic Synchronization Hazards</h3>"
    end_marker = "<h4>2. The Readers-Writers Problem</h4>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 1 / Subsection 2 boundaries in Module 04.")
        return False

    updated_content = content[:start_idx] + DINING_PHILOSOPHERS_MASSIVE + "\n\n      " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Dining Philosophers in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if apply_dining_philosophers_expansion():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Exhaustively expand Dining Philosophers theory and hazards in Module 04\n\n"
                "Add mathematical circular graph modeling, livelock/starvation traces,\n"
                "four structural mitigation proofs, and real-world DBMS lock parallels."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
