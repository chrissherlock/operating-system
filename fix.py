#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand RAGs & Cycle Detection section with syntax highlighting
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

RAG_SECTION_CONTENT = r"""    <h3>3. Resource Allocation Graphs (RAGs) &amp; Cycle Detection</h3>
    <p>
      To formally analyze and detect system deadlocks algorithmically, operating systems frequently model resource state as a directed graph known as a <strong>Resource Allocation Graph (RAG)</strong>. Invented by Holt (1972), RAGs provide a rigorous graphical and topological framework to visualize process dependencies and evaluate deadlock existence in real time.
    </p>

    <h4>1. Formal Graph Structure &amp; Vertex Types</h4>
    <p>
      Mathematically, a Resource Allocation Graph is defined as a directed graph $G = (V, E)$ where the vertex set $V$ is partitioned into two disjoint subsets representing processes and resources:
    </p>
    <ul>
      <li>
        <strong>Process Vertices ($P$):</strong> Represented as circles ($P_1, P_2, \dots, P_n$). These denote active execution entities competing for system resources.
      </li>
      <li>
        <strong>Resource Vertices ($R$):</strong> Represented as rectangular boxes ($R_1, R_2, \dots, R_m$). Each resource box may contain one or more black dots (tokens) representing identical available instances of that resource type.
      </li>
    </ul>

    <h4>2. Directed Edge Semantics</h4>
    <p>
      The edge set $E$ consists of two distinct directed edge types that capture runtime allocation and waiting states:
    </p>
    <ul>
      <li>
        <strong>Request Edge ($P_i \to R_j$):</strong> A directed edge originating from process $P_i$ and pointing to resource type $R_j$. This signifies that process $P_i$ has requested an instance of resource $R_j$ and is currently blocked waiting for allocation.
      </li>
      <li>
        <strong>Assignment Edge ($R_j \to P_i$):</strong> A directed edge originating from a specific resource instance within box $R_j$ and pointing to process $P_i$. This signifies that an instance of resource $R_j$ has been allocated to process $P_i$.
      </li>
    </ul>

    <div class="math-callout" style="background: #f8fafc; border-left-color: var(--accent);">
      <strong style="color: var(--primary);">Graph Reduction &amp; Deadlock Theorems:</strong>
      <br><br>
      <ul>
        <li><strong>Single-Instance Theorem:</strong> If a resource allocation graph contains <em>only single-instance resource types</em>, then a directed cycle in the graph is a <strong>necessary and sufficient condition</strong> for deadlock.</li>
        <li><strong>Multi-Instance Theorem:</strong> If resource types contain multiple instances, a cycle is a <em>necessary</em> condition for deadlock, but <em>not sufficient</em>, because other non-deadlocked processes may release instances to break the wait chain.</li>
      </ul>
    </div>

    <h4>3. Algorithmic Cycle Detection (Python Implementation)</h4>
    <p>
      Operating systems kernels implement cycle detection algorithms (such as Depth-First Search with recursion stack tracking) to inspect RAG adjacency lists periodically. Below is a complete, syntax-highlighted Python module demonstrating directed graph representation and cycle detection:
    </p>

    <!-- Syntax Highlighted Code Box -->
    <div style="background: #0f172a; color: #f8fafc; border-radius: 8px; padding: 20px; font-family: var(--font-mono); font-size: 0.85rem; overflow-x: auto; margin: 20px 0; border: 1px solid var(--border);">
      <div style="color: #64748b; margin-bottom: 10px; font-size: 0.78rem; border-bottom: 1px solid #334155; padding-bottom: 6px;">
        python &bull; rag_detector.py
      </div>
      <pre style="margin: 0; line-height: 1.5;"><span style="color: #94a3b8;">#!/usr/bin/env python3</span>
<span style="color: #c084fc;">class</span> <span style="color: #6ee7b7;">ResourceAllocationGraph</span>:
    <span style="color: #c084fc;">def</span> <span style="color: #60a5fa;">__init__</span>(<span style="color: #f43f5e;">self</span>):
        <span style="color: #f43f5e;">self</span>.adjacency_list = {}

    <span style="color: #c084fc;">def</span> <span style="color: #60a5fa;">add_edge</span>(<span style="color: #f43f5e;">self</span>, source, destination):
        <span style="color: #c084fc;">if</span> source <span style="color: #e2e8f0;">not in</span> <span style="color: #f43f5e;">self</span>.adjacency_list:
            <span style="color: #f43f5e;">self</span>.adjacency_list[source] = []
        <span style="color: #f43f5e;">self</span>.adjacency_list[source].append(destination)

    <span style="color: #c084fc;">def</span> <span style="color: #60a5fa;">detect_cycle_util</span>(<span style="color: #f43f5e;">self</span>, node, visited, recursion_stack):
        visited.add(node)
        recursion_stack.add(node)

        <span style="color: #c084fc;">for</span> neighbor <span style="color: #e2e8f0;">in</span> <span style="color: #f43f5e;">self</span>.adjacency_list.get(node, []):
            <span style="color: #c084fc;">if</span> neighbor <span style="color: #e2e8f0;">not in</span> visited:
                <span style="color: #c084fc;">if</span> <span style="color: #f43f5e;">self</span>.detect_cycle_util(neighbor, visited, recursion_stack):
                    <span style="color: #c084fc;">return</span> <span style="color: #fbbf24;">True</span>
            <span style="color: #c084fc;">elif</span> neighbor <span style="color: #e2e8f0;">in</span> recursion_stack:
                <span style="color: #c084fc;">return</span> <span style="color: #fbbf24;">True</span>

        recursion_stack.remove(node)
        <span style="color: #c084fc;">return</span> <span style="color: #fbbf24;">False</span>

    <span style="color: #c084fc;">def</span> <span style="color: #60a5fa;">contains_deadlock</span>(<span style="color: #f43f5e;">self</span>):
        visited = <span style="color: #6ee7b7;">set</span>()
        recursion_stack = <span style="color: #6ee7b7;">set</span>()
        <span style="color: #c084fc;">for</span> node <span style="color: #e2e8f0;">in</span> <span style="color: #f43f5e;">self</span>.adjacency_list:
            <span style="color: #c084fc;">if</span> node <span style="color: #e2e8f0;">not in</span> visited:
                <span style="color: #c084fc;">if</span> <span style="color: #f43f5e;">self</span>.detect_cycle_util(node, visited, recursion_stack):
                    <span style="color: #c084fc;">return</span> <span style="color: #fbbf24;">True</span>
        <span style="color: #c084fc;">return</span> <span style="color: #fbbf24;">False</span>

<span style="color: #c084fc;">if</span> __name__ == <span style="color: #34d399;">"__main__"</span>:
    rag = <span style="color: #6ee7b7;">ResourceAllocationGraph</span>()
    rag.add_edge(<span style="color: #34d399;">"P1"</span>, <span style="color: #34d399;">"R1"</span>)
    rag.add_edge(<span style="color: #34d399;">"R1"</span>, <span style="color: #34d399;">"P2"</span>)
    rag.add_edge(<span style="color: #34d399;">"P2"</span>, <span style="color: #34d399;">"R2"</span>)
    rag.add_edge(<span style="color: #34d399;">"R2"</span>, <span style="color: #34d399;">"P1"</span>)

    <span style="color: #c084fc;">print</span>(<span style="color: #34d399;">"Deadlock Detected:"</span>, rag.contains_deadlock())</pre>
    </div>"""

def update_rag_section():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>3. Resource Allocation Graphs (RAGs) &amp; Cycle Detection</h3>"
    end_marker = "<h3>4. Banker's Algorithm</h3>" # Or end of file / next section marker

    start_idx = content.find(start_marker)
    if start_idx == -1:
        # Fallback search without entity escaping
        start_marker = "<h3>3. Resource Allocation Graphs (RAGs) & Cycle Detection</h3>"
        start_idx = content.find(start_marker)

    if start_idx == -1:
        print("Error: Could not locate Section 3 in Module 02.")
        return False

    # Find next section or end of content card
    end_idx = content.find("<h3>4.", start_idx)
    if end_idx == -1:
        end_idx = content.find("<nav class=\"nav-bar\">", start_idx)

    if end_idx == -1:
        print("Error: Could not determine end boundary for Section 3.")
        return False

    updated_content = content[:start_idx] + RAG_SECTION_CONTENT + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 3 in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if update_rag_section():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Expand Section 3 on Resource Allocation Graphs and add syntax-highlighted code\n\n"
                "Provide rigorous graph theory formulations, single/multi-instance theorems,\n"
                "and a fully syntax-highlighted Python DFS cycle detection implementation."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
