#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Readers-Writers Starvation & 2PL in Module 04
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "04-classic-synchronization-real-world-defenses.html"
)

READERS_WRITERS_2PL_EXPANSION = r"""      <h3>2. Readers-Writers Starvation &amp; Database 2PL</h3>
      <p>
        In concurrent database engines, file systems, and operating system memory caches, access patterns exhibit an asymmetric read-heavy bias. The <strong>Readers-Writers Problem</strong> formalizes synchronization protocols for shared state accessed by two distinct classes of concurrent threads:
      </p>
      <ul>
        <li><strong>Readers ($R$):</strong> Inspect state without mutation. Multiple readers may access the critical section concurrently ($R_1 \parallel R_2$).</li>
        <li><strong>Writers ($W$):</strong> Mutate state. A writer requires exclusive, non-shareable access; no other reader or writer may occupy the critical section ($W_1 \perp R_1$, $W_1 \perp W_2$).</li>
      </ul>

      <div class="math-callout" style="background: #f8fafc; border-left: 4px solid var(--accent); padding: 16px; border-radius: 0 6px 6px 0; margin: 18px 0;">
        <strong style="color: var(--primary);">Mutual Exclusion Invariant:</strong>
        <br><br>
        $$ \text{ActiveWriters} \le 1 \quad \land \quad (\text{ActiveWriters} = 1 \implies \text{ActiveReaders} = 0) $$
      </div>

      <h4>1. The Triad of Readers-Writers Variants</h4>
      <p>
        The primary challenge in designing readers-writers locks (<code>rwlock</code>) lies in arbitrating queue priorities without causing <strong>starvation (indefinite deferral)</strong>:
      </p>
      <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; margin: 20px 0;">
        <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 16px;">
          <strong style="color: var(--primary); font-size: 0.92rem;">First Variant: Reader-Preference</strong>
          <p style="font-size: 0.82rem; color: var(--text); margin-top: 8px; line-height: 1.5;">
            No reader is kept waiting unless a writer already holds the lock. Incoming readers join active readers immediately, even if a writer is queued.
          </p>
          <div style="font-size: 0.78rem; font-weight: 700; color: #dc2626; margin-top: 8px;">
            Hazard: Writer Starvation
          </div>
          <p style="font-size: 0.78rem; color: var(--text-muted); margin-top: 4px;">
            A continuous cascade of overlapping readers permanently blocks writers.
          </p>
        </div>

        <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 16px;">
          <strong style="color: var(--primary); font-size: 0.92rem;">Second Variant: Writer-Preference</strong>
          <p style="font-size: 0.82rem; color: var(--text); margin-top: 8px; line-height: 1.5;">
            Once a writer signals intent to write, new incoming readers are queued behind it. Active readers drain, and the queued writer executes next.
          </p>
          <div style="font-size: 0.78rem; font-weight: 700; color: #d97706; margin-top: 8px;">
            Hazard: Reader Starvation
          </div>
          <p style="font-size: 0.78rem; color: var(--text-muted); margin-top: 4px;">
            In write-intensive workloads, continuous writer arrivals lock out all readers.
          </p>
        </div>

        <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 16px;">
          <strong style="color: var(--primary); font-size: 0.92rem;">Third Variant: Fair / FIFO Order</strong>
          <p style="font-size: 0.82rem; color: var(--text); margin-top: 8px; line-height: 1.5;">
            Requests are processed in strict arrival order using a synchronization <strong>turnstile</strong>. Neither readers nor writers can starve.
          </p>
          <div style="font-size: 0.78rem; font-weight: 700; color: #16a34a; margin-top: 8px;">
            Guaranteed: Starvation-Free
          </div>
          <p style="font-size: 0.78rem; color: var(--text-muted); margin-top: 4px;">
            Preserves reader concurrency while bounding waiting time to $O(N)$.
          </p>
        </div>
      </div>

      <h4>2. Starvation-Free Turnstile Implementation (C Pseudocode)</h4>
      <p>
        To eliminate starvation, a binary semaphore named <code>turnstile</code> acts as an entry barrier. When a writer queues at the turnstile, subsequent readers are held behind it until the writer completes:
      </p>

      <!-- Syntax Highlighted Code Box: Fair RW-Lock -->
      <div style="background: #0f172a; color: #f8fafc; border-radius: 8px; padding: 20px; font-family: var(--font-mono); font-size: 0.85rem; overflow-x: auto; margin: 16px 0; border: 1px solid var(--border);">
        <div style="color: #64748b; margin-bottom: 10px; font-size: 0.78rem; border-bottom: 1px solid #334155; padding-bottom: 6px;">
          c &bull; fair_rwlock.c
        </div>
        <pre style="margin: 0; line-height: 1.5;"><span style="color: #94a3b8;">// Shared Synchronization State</span>
<span style="color: #6ee7b7;">int</span> read_count = <span style="color: #f43f5e;">0</span>;
<span style="color: #6ee7b7;">semaphore</span> turnstile = <span style="color: #f43f5e;">1</span>;     <span style="color: #94a3b8;">// Preserves FIFO arrival order</span>
<span style="color: #6ee7b7;">semaphore</span> count_mutex = <span style="color: #f43f5e;">1</span>;   <span style="color: #94a3b8;">// Protects read_count updates</span>
<span style="color: #6ee7b7;">semaphore</span> resource = <span style="color: #f43f5e;">1</span>;      <span style="color: #94a3b8;">// Exclusive data lock</span>

<span style="color: #c084fc;">void</span> <span style="color: #60a5fa;">reader</span>() {
    <span style="color: #60a5fa;">wait</span>(turnstile);         <span style="color: #94a3b8;">// Pass through turnstile gate</span>
    <span style="color: #60a5fa;">signal</span>(turnstile);

    <span style="color: #60a5fa;">wait</span>(count_mutex);
    read_count++;
    <span style="color: #c084fc;">if</span> (read_count == <span style="color: #f43f5e;">1</span>) {
        <span style="color: #60a5fa;">wait</span>(resource);      <span style="color: #94a3b8;">// First reader claims exclusive resource lock</span>
    }
    <span style="color: #60a5fa;">signal</span>(count_mutex);

    <span style="color: #60a5fa;">read_data</span>();             <span style="color: #94a3b8;">// Concurrent read section</span>

    <span style="color: #60a5fa;">wait</span>(count_mutex);
    read_count--;
    <span style="color: #c084fc;">if</span> (read_count == <span style="color: #f43f5e;">0</span>) {
        <span style="color: #60a5fa;">signal</span>(resource);    <span style="color: #94a3b8;">// Last reader releases exclusive lock</span>
    }
    <span style="color: #60a5fa;">signal</span>(count_mutex);
}

<span style="color: #c084fc;">void</span> <span style="color: #60a5fa;">writer</span>() {
    <span style="color: #60a5fa;">wait</span>(turnstile);         <span style="color: #94a3b8;">// Block incoming readers from passing gate</span>
    <span style="color: #60a5fa;">wait</span>(resource);          <span style="color: #94a3b8;">// Wait for active readers to drain</span>

    <span style="color: #60a5fa;">write_data</span>();            <span style="color: #94a3b8;">// Exclusive write section</span>

    <span style="color: #60a5fa;">signal</span>(turnstile);       <span style="color: #94a3b8;">// Open gate for next queued thread</span>
    <span style="color: #60a5fa;">signal</span>(resource);        <span style="color: #94a3b8;">// Release exclusive lock</span>
}</pre>
      </div>

      <h4>3. Database Concurrency: Two-Phase Locking (2PL)</h4>
      <p>
        In relational database engines (such as PostgreSQL, MySQL InnoDB, and Oracle), concurrency control cannot rely on ad-hoc mutexes. Databases must guarantee <strong>Serializability</strong>—the highest isolation level, ensuring concurrent execution produces the exact same state as some serial execution order.
      </p>
      <p>
        The mathematical foundation of serializability is <strong>Two-Phase Locking (2PL)</strong>:
      </p>
      <ol>
        <li>
          <strong>Growing Phase (Lock Acquisition):</strong> The transaction may acquire shared locks (<code>S-lock</code>) or exclusive locks (<code>X-lock</code>) as needed. <em>The transaction is strictly forbidden from releasing any lock during this phase.</em>
        </li>
        <li>
          <strong>Shrinking Phase (Lock Release):</strong> The transaction begins releasing locks. <em>Once the transaction releases its first lock, it enters the shrinking phase and is strictly forbidden from acquiring any further locks.</em>
        </li>
      </ol>

      <div class="math-callout" style="background: #f8fafc; border-left: 4px solid var(--accent); padding: 16px; border-radius: 0 6px 6px 0; margin: 18px 0;">
        <strong style="color: var(--primary);">2PL Serializability Theorem:</strong>
        <br><br>
        $$ \text{Any schedule produced by a 2PL scheduler is conflict-serializable (acyclic serialization graph).} $$
      </div>

      <h5>Strict 2PL (S2PL) vs. Rigorous 2PL (SS2PL)</h5>
      <p>
        Basic 2PL guarantees serializability, but it suffers from <strong>cascading aborts</strong>. If transaction $T_1$ releases an exclusive lock on row $A$ during its shrinking phase and later encounters a disk fault and aborts, any concurrent transaction $T_2$ that read uncommitted row $A$ must also be aborted.
      </p>
      <table style="width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.88rem;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px; text-align: left; color: var(--primary);">Protocol Variant</th>
            <th style="padding: 10px; text-align: left; color: var(--primary);">Release Invariant</th>
            <th style="padding: 10px; text-align: left; color: var(--primary);">Guarantees &amp; Trade-offs</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px; font-weight: 600;">Basic 2PL</td>
            <td style="padding: 10px;">Locks released incrementally during shrinking phase.</td>
            <td style="padding: 10px; color: #dc2626;">Serializability guaranteed, but vulnerable to cascading aborts.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px; font-weight: 600;">Strict 2PL (S2PL)</td>
            <td style="padding: 10px;">All <strong>Exclusive (X)</strong> locks held until transaction commits or aborts.</td>
            <td style="padding: 10px; color: #16a34a;">Eliminates cascading aborts (prevents dirty reads). Industry standard.</td>
          </tr>
          <tr>
            <td style="padding: 10px; font-weight: 600;">Rigorous / Strong Strict 2PL (SS2PL)</td>
            <td style="padding: 10px;"><strong>All</strong> locks (both Shared S and Exclusive X) held until commit/abort.</td>
            <td style="padding: 10px; color: #0284c7;">Serial execution order matches commit order; lowers reader throughput.</td>
          </tr>
        </tbody>
      </table>

      <h4>4. DBMS Deadlock Resolution via Wait-For-Graphs</h4>
      <p>
        While 2PL guarantees serializability, it <strong>does not prevent deadlock</strong>. In fact, aggressive lock acquisition makes deadlocks inevitable. For example:
      </p>
      <ul>
        <li>Transaction $T_1$ holds exclusive lock $X(A)$ and requests $X(B)$.</li>
        <li>Transaction $T_2$ holds exclusive lock $X(B)$ and requests $X(A)$.</li>
      </ul>
      <p>
        Modern database engines handle this through active <strong>deadlock detection and victim selection</strong>:
      </p>
      <ul>
        <li>
          <strong>Wait-For-Graph (WFG) Construction:</strong> The DBMS lock manager maintains a background thread running every 50&ndash;500ms. It constructs a directed graph where nodes represent active transactions and edges represent pending lock requests ($T_i \to T_j$).
        </li>
        <li>
          <strong>Cycle Detection:</strong> The lock manager runs Depth-First Search (DFS) over the WFG. A cycle indicates an unresolvable circular wait.
        </li>
        <li>
          <strong>Victim Selection Criteria:</strong> Upon detecting a cycle, the engine selects a "victim" transaction to abort and roll back based on:
          <ol>
            <li><strong>Fewest Locks Held:</strong> Minimizes the volume of undo log records to process.</li>
            <li><strong>Youngest Elapsed Time:</strong> Minimizes discarded user computation.</li>
            <li><strong>Rollback Cost:</strong> Prefers read-heavy transactions over transactions with heavy physical disk writes.</li>
          </ol>
        </li>
      </ul>"""

def expand_readers_writers_2pl():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>2. Readers-Writers Starvation &amp; Database 2PL</h3>"
    end_marker = "<h3>3. Real-World Kernel Defenses: Linux lockdep &amp; Driver Verifier</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 2 boundaries in Module 04.")
        return False

    updated_content = content[:start_idx] + READERS_WRITERS_2PL_EXPANSION + "\n\n      " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Readers-Writers & 2PL in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if expand_readers_writers_2pl():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Expand Readers-Writers starvation and Database 2PL in Module 04\n\n"
                "Add 3-variant Readers-Writers taxonomy, fair turnstile lock implementation,\n"
                "Strict/Rigorous 2PL invariants, and DBMS Wait-For-Graph deadlock resolution."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
