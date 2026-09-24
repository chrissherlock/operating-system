#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand Section 2 on Dijkstra's Banker's Algorithm in Module 03
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "03-deadlock-handling-bankers-algorithm.html"
)

BANKERS_ALGORITHM_EXPANDED = r"""      <h3>2. Dijkstra's Banker's Algorithm</h3>
      <p>
        Formulated by Edsger Dijkstra in 1965 for the THE multiprogramming system, the <strong>Banker's Algorithm</strong> is the classical resource allocation and deadlock avoidance method. The algorithm is metaphorically named after a small-town banker who must allocate cash liquidity among clients while ensuring the bank never exhausts its reserves in a way that leaves clients unable to complete their financial projects.
      </p>

      <h4>1. Core Mathematical Data Structures</h4>
      <p>
        Let <i>n</i> be the total number of concurrent execution threads in the system, and let <i>m</i> be the total number of distinct resource types. The operating system kernel maintains four primary data structures in protected memory:
      </p>
      <ul>
        <li>
          <strong>Available Vector ($Available$):</strong> A vector of length <i>m</i>. If $Available[j] = k$, there are <i>k</i> identical instances of resource type $R_j$ currently unallocated and free in the system.
        </li>
        <li>
          <strong>Maximum Matrix ($Max$):</strong> An $n \times m$ matrix defining the lifetime maximum resource demand of each thread. If $Max[i][j] = k$, thread $P_i$ may request at most <i>k</i> instances of resource type $R_j$ during its execution.
        </li>
        <li>
          <strong>Allocation Matrix ($Allocation$):</strong> An $n \times m$ matrix tracking resources currently held by active threads. If $Allocation[i][j] = k$, thread $P_i$ currently holds <i>k</i> instances of resource type $R_j$.
        </li>
        <li>
          <strong>Need Matrix ($Need$):</strong> An $n \times m$ matrix representing the remaining resource potential required by each thread to finish its task:
          $$ Need[i][j] = Max[i][j] - Allocation[i][j] $$
        </li>
      </ul>

      <h4>2. The Safety Algorithm</h4>
      <p>
        The kernel executes the <strong>Safety Algorithm</strong> to determine whether the system is currently in a safe state. A state is safe if there exists a safe execution sequence $\langle P_0, P_1, \dots, P_{n-1} \rangle$ such that every thread's maximum resource demands can be satisfied using currently available resources plus the resources released by preceding threads.
      </p>
      <ol>
        <li>
          Let $Work$ be a vector of length <i>m</i> initialized to $Available$, and let $Finish$ be a boolean vector of length <i>n</i> initialized to <code>false</code> for all threads.
        </li>
        <li>
          Find an index <i>i</i> such that:
          $$ Finish[i] == \text{false} \quad \land \quad Need_i \le Work $$
          If no such index <i>i</i> exists, proceed to Step 4.
        </li>
        <li>
          If an eligible thread <i>i</i> is found, simulate its successful completion by returning its held resources to the working pool:
          $$ Work = Work + Allocation_i $$
          $$ Finish[i] = \text{true} $$
          Return to Step 2 to inspect remaining unfinished threads.
        </li>
        <li>
          If $Finish[i] == \text{true}$ for all threads <i>i</i>, the system is in a <strong>safe state</strong>, and the sequence of discovered indices forms a valid safe execution path. Otherwise, the system is unsafe.
        </li>
      </ol>

      <h4>3. The Resource-Request Algorithm</h4>
      <p>
        When thread $P_i$ issues a dynamic request vector $Request_i$ for additional resources, the kernel evaluates the request before modifying allocation tables:
      </p>
      <ol>
        <li>
          <strong>Claim Validation:</strong> Verify that $Request_i \le Need_i$. If a thread requests more than its declared maximum claim, raise a hardware fault.
        </li>
        <li>
          <strong>Availability Check:</strong> Verify that $Request_i \le Available$. If sufficient instances are free, the thread must wait.
        </li>
        <li>
          <strong>State Simulation:</strong> Temporarily assume the kernel grants the request by updating system state vectors:
          $$ Available = Available - Request_i $$
          $$ Allocation_i = Allocation_i + Request_i $$
          $$ Need_i = Need_i - Request_i $$
        </li>
        <li>
          <strong>Safety Audit:</strong> Run the Safety Algorithm on the hypothetical state. If the resulting state is <strong>safe</strong>, the resource allocation is finalized and granted to $P_i$. If unsafe, the state is rolled back, and $P_i$ is suspended until resources can be allocated safely.
        </li>
      </ol>

      <h4>4. Algorithmic Complexity &amp; Python Implementation</h4>
      <p>
        The Banker's Algorithm safety check requires inspecting an $n \times m$ matrix across multiple passes, yielding a time complexity of $\mathcal{O}(m \times n^2)$. Below is a complete, syntax-highlighted Python implementation of the safety verifier:
      </p>

      <!-- Syntax Highlighted Code Box -->
      <div style="background: #0f172a; color: #f8fafc; border-radius: 8px; padding: 20px; font-family: var(--font-mono); font-size: 0.85rem; overflow-x: auto; margin: 20px 0; border: 1px solid var(--border);">
        <div style="color: #64748b; margin-bottom: 10px; font-size: 0.78rem; border-bottom: 1px solid #334155; padding-bottom: 6px;">
          python &bull; bankers_verifier.py
        </div>
        <pre style="margin: 0; line-height: 1.5;"><span style="color: #94a3b8;">#!/usr/bin/env python3</span>
<span style="color: #c084fc;">def</span> <span style="color: #60a5fa;">evaluate_safety</span>(available, allocation, max_matrix):
    num_threads = <span style="color: #6ee7b7;">len</span>(allocation)
    num_resources = <span style="color: #6ee7b7;">len</span>(available)

    need = [
        [max_matrix[i][j] - allocation[i][j] <span style="color: #c084fc;">for</span> j <span style="color: #e2e8f0;">in</span> <span style="color: #6ee7b7;">range</span>(num_resources)]
        <span style="color: #c084fc;">for</span> i <span style="color: #e2e8f0;">in</span> <span style="color: #6ee7b7;">range</span>(num_threads)
    ]

    work = <span style="color: #6ee7b7;">list</span>(available)
    finish = [<span style="color: #fbbf24;">False</span>] * num_threads
    safe_sequence = []

    <span style="color: #c084fc;">while</span> <span style="color: #6ee7b7;">len</span>(safe_sequence) < num_threads:
        found_eligible = <span style="color: #fbbf24;">False</span>
        <span style="color: #c084fc;">for</span> i <span style="color: #e2e8f0;">in</span> <span style="color: #6ee7b7;">range</span>(num_threads):
            <span style="color: #c084fc;">if</span> <span style="color: #e2e8f0;">not</span> finish[i] <span style="color: #e2e8f0;">and</span> <span style="color: #e2e8f0;">all</span>(need[i][j] &lt;= work[j] <span style="color: #c084fc;">for</span> j <span style="color: #e2e8f0;">in</span> <span style="color: #6ee7b7;">range</span>(num_resources)):
                work = [work[j] + allocation[i][j] <span style="color: #c084fc;">for</span> j <span style="color: #c084fc;">in</span> <span style="color: #6ee7b7;">range</span>(num_resources)]
                finish[i] = <span style="color: #fbbf24;">True</span>
                safe_sequence.append(i)
                found_eligible = <span style="color: #fbbf24;">True</span>
                <span style="color: #c084fc;">break</span>
        <span style="color: #c084fc;">if</span> <span style="color: #e2e8f0;">not</span> found_eligible:
            <span style="color: #c084fc;">return</span> <span style="color: #fbbf24;">False</span>, []

    <span style="color: #c084fc;">return</span> <span style="color: #fbbf24;">True</span>, safe_sequence

<span style="color: #c084fc;">if</span> __name__ == <span style="color: #34d399;">"__main__"</span>:
    avail = [<span style="color: #f43f5e;">3</span>, <span style="color: #f43f5e;">3</span>, <span style="color: #f43f5e;">2</span>]
    alloc = [[<span style="color: #f43f5e;">0</span>,<span style="color: #f43f5e;">1</span>,<span style="color: #f43f5e;">0</span>], [<span style="color: #f43f5e;">2</span>,<span style="color: #f43f5e;">0</span>,<span style="color: #f43f5e;">0</span>], [<span style="color: #f43f5e;">3</span>,<span style="color: #f43f5e;">0</span>,<span style="color: #f43f5e;">2</span>], [<span style="color: #f43f5e;">2</span>,<span style="color: #f43f5e;">1</span>,<span style="color: #f43f5e;">1</span>], [<span style="color: #f43f5e;">0</span>,<span style="color: #f43f5e;">0</span>,<span style="color: #f43f5e;">2</span>]]
    max_mat = [[<span style="color: #f43f5e;">7</span>,<span style="color: #f43f5e;">5</span>,<span style="color: #f43f5e;">3</span>], [<span style="color: #f43f5e;">3</span>,<span style="color: #f43f5e;">2</span>,<span style="color: #f43f5e;">2</span>], [<span style="color: #f43f5e;">9</span>,<span style="color: #f43f5e;">0</span>,<span style="color: #f43f5e;">2</span>], [<span style="color: #f43f5e;">2</span>,<span style="color: #f43f5e;">2</span>,<span style="color: #f43f5e;">2</span>], [<span style="color: #f43f5e;">4</span>,<span style="color: #f43f5e;">3</span>,<span style="color: #f43f5e;">3</span>]]

    is_safe, seq = evaluate_safety(avail, alloc, max_mat)
    <span style="color: #c084fc;">print</span>(<span style="color: #34d399;">"System Safe:"</span>, is_safe, <span style="color: #34d399;">"Safe Sequence:"</span>, seq)</pre>
      </div>"""

def update_section_two():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>2. Dijkstra's Banker's Algorithm</h3>"
    end_marker = "<!-- ================================================================= -->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 2 boundaries in Module 03.")
        return False

    updated_content = content[:start_idx] + BANKERS_ALGORITHM_EXPANDED + "\n\n      " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 2 in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if update_section_two():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Expand Section 2 on Dijkstra's Banker's Algorithm in Module 03\n\n"
                "Provide rigorous mathematical vector definitions, the Safety and Resource-Request\n"
                "algorithms, complexity analysis, and a syntax-highlighted Python implementation."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
