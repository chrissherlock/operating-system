#!/usr/bin/env python3
# =====================================================================
# fix.py: Integrate comprehensive RAG deadlock theory into Module 02
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

EXPANDED_SECTION_THREE = r"""      <h3>3. Resource Allocation Graphs (RAGs) &amp; Cycle Detection</h3>
      <p>
        To formally analyze and detect system deadlocks algorithmically, operating systems frequently model resource state as a directed graph known as a <strong>Resource Allocation Graph (RAG)</strong>. Invented by Holt (1972), RAGs provide a rigorous graphical and topological framework to visualize process dependencies and evaluate deadlock existence in real time.
      </p>

      <h4>1. From Hardware Contention to Graph Topology</h4>
      <p>
        When multiple concurrent processes execute, they constantly request, acquire, and release system resources (such as database locks, memory regions, file descriptors, or hardware devices). Without a global view, an operating system sees only isolated system calls (e.g., <code>lock()</code> or <code>wait()</code>). An RAG aggregates these discrete state transitions into a holistic directed graph $G = (V, E)$:
      </p>
      <ul>
        <li>
          <strong>Process Vertices ($P$):</strong> Represented as circles ($P_1, P_2, \dots, P_n$). These denote active execution entities competing for system resources.
        </li>
        <li>
          <strong>Resource Vertices ($R$):</strong> Represented as rectangular boxes ($R_1, R_2, \dots, R_m$). Each resource box may contain one or more black dots (tokens) representing identical available instances of that resource type.
        </li>
        <li>
          <strong>Directed Edge Semantics ($E$):</strong> Capture runtime allocation and waiting states via <em>Request Edges</em> ($P_i \to R_j$, signifying a blocked petitioner waiting for allocation) and <em>Assignment Edges</em> ($R_j \to P_i$, signifying active ownership).
        </li>
      </ul>
      <p>
        When a process issues a request for a resource it cannot immediately get, it transforms from a runnable entity into a trapped petitioner. The request edge is a graphical signature of <strong>Hold-and-Wait combined with Mutual Exclusion</strong>: the process is already holding resources elsewhere and is now indefinitely suspended.
      </p>

      <h4>2. The Anatomy of a Deadlock: Why Cycles Matter</h4>
      <p>
        The core reason RAGs are powerful for deadlock detection lies in the topological concept of a <strong>directed cycle</strong>. Imagine a circular chain of dependencies where Process $P_1$ holds Resource $R_1$ and requests $R_2$, while Process $P_2$ holds Resource $R_2$ and requests $R_1$:
      </p>
      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--accent);">
        <strong style="color: var(--primary);">Closed Dependency Cycle:</strong>
        <br><br>
        $$ P_1 \to R_2 \to P_2 \to R_1 \to P_1 $$
      </div>
      <p>
        In operating systems terms, <strong>a cycle represents a closed loop of unfulfilled mutual dependencies</strong>. Because every process in the cycle is waiting for a resource held by the next process in the ring, no process can ever release its hold. They are mutually holding each other hostage, entering a terminal fixed point where forward progress is impossible.
      </p>

      <h4>3. Single-Instance vs. Multi-Instance Deadlock Theorems</h4>
      <p>
        A common point of confusion is whether a cycle <em>always</em> means a deadlock. RAG graph theory answers this through two foundational theorems:
      </p>
      <ul>
        <li>
          <strong>The Single-Instance Theorem (Necessity &amp; Sufficiency):</strong> If every resource type in your system has only <strong>one</strong> instance (e.g., one exclusive printer or mutex lock), then <strong>a cycle in the RAG is both necessary and sufficient for deadlock</strong>. If you see a cycle, a deadlock is guaranteed.
        </li>
        <li>
          <strong>The Multi-Instance Theorem (Necessity Only):</strong> If resource types have multiple identical units (e.g., a pool of 4 identical database worker threads), a cycle is still <em>necessary</em> (no deadlock occurs without a cycle), but it is <strong>not sufficient</strong>. A process outside the cycle might eventually finish, release its resource instances into the pool, and break the deadlock chain for processes trapped inside the loop.
        </li>
      </ul>

      <!-- ================================================================= -->
      <!-- INTERACTIVE PEDAGOGICAL AID: RAG SIMULATION STEPPER WIDGET        -->
      <!-- ================================================================= -->
      <div class="aid-wrapper">
        <div class="aid-header">Interactive Walkthrough: RAG Construction &amp; Cycle Detection</div>
        <div class="aid-subtitle">Trace step-by-step how Resource Allocation Graph edges form dependency chains and trigger cycle detection.</div>

        <div class="aid-grid">
          <div class="controls-panel">
            <div class="preview-box" id="preview-text">
              <strong>Step 1: Mutual Exclusion &amp; Hold-and-Wait.</strong> Process P1 acquires Resource R1 non-shareably and requests Resource R2.
            </div>

            <div class="stepper-btns">
              <button class="step-btn" id="prev-btn" onclick="changeStep(-1)" disabled>&larr; Prev</button>
              <button class="step-btn" id="next-btn" onclick="changeStep(1)">Next &rarr;</button>
              <button class="step-btn" onclick="resetStepper()" style="background:#64748b;">Reset</button>
            </div>

            <div class="telemetry-bar" id="telemetry-bar" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px 12px; font-family: var(--font-mono); font-size: 0.75rem; background: #0f172a; color: #e2e8f0; padding: 10px 12px; border-radius: 6px;">
              <div><strong>Phase:</strong> <span id="tel-phase" style="color: #38bdf8;">1/4</span></div>
              <div><strong>Edges:</strong> <span id="tel-edges">P1&rarr;R2, R1&rarr;P1</span></div>
              <div><strong>Cycle:</strong> <span id="tel-cycle">None</span></div>
              <div><strong>State:</strong> <span id="tel-state" style="color: #4ade80; font-weight: 700;">Safe</span></div>
            </div>

            <div class="toggle-bar">
              <span style="font-size: 0.72rem; font-weight: 700; align-self: center; color: var(--text-muted);">TOPOLOGY:</span>
              <button class="toggle-btn active" onclick="setTopology('single')">Single-Instance</button>
              <button class="toggle-btn" onclick="setTopology('multi')">Multi-Instance</button>
            </div>
          </div>

          <div class="visual-canvas" style="display: flex; flex-direction: column; justify-content: space-between; height: 100%; background: #ffffff; border: 1px solid var(--border);">
            <div style="font-weight: 700; font-size: 0.82rem; margin-bottom: 6px; color: var(--primary); text-align: left;">Synchronized Visual Canvas &mdash; RAG State</div>

            <!-- Unified Interactive SVG Canvas (Light Theme, Expanded Fill) -->
            <svg viewBox="0 0 300 180" style="width: 100%; height: 100%; min-height: 180px; background: #f8fafc; border: 1px solid var(--border); border-radius: 6px; padding: 8px;">
              <defs>
                <marker id="arrow-std" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#94a3b8"/>
                </marker>
                <marker id="arrow-active" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#0284c7"/>
                </marker>
                <marker id="arrow-danger" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#dc2626"/>
                </marker>
              </defs>

              <!-- Edges (Rendered behind nodes) -->
              <!-- Edge 1: P1 -> R1 (Top horizontal) -->
              <line id="svg-edge-p1-r1" x1="75" y1="50" x2="205" y2="50" stroke="#cbd5e1" stroke-width="2.5" marker-end="url(#arrow-std)" />
              <text id="svg-txt-p1-r1" x="140" y="42" fill="#64748b" font-size="8" font-weight="600" text-anchor="middle" opacity="0">req</text>

              <!-- Edge 2: R1 -> P2 (Right vertical) -->
              <line id="svg-edge-r1-p2" x1="220" y1="65" x2="220" y2="115" stroke="#cbd5e1" stroke-width="2.5" marker-end="url(#arrow-std)" />
              <text id="svg-txt-r1-p2" x="234" y="94" fill="#64748b" font-size="8" font-weight="600" text-anchor="middle" opacity="0">alloc</text>

              <!-- Edge 3: P2 -> R2 (Bottom horizontal) -->
              <line id="svg-edge-p2-r2" x1="205" y1="130" x2="75" y2="130" stroke="#cbd5e1" stroke-width="2.5" marker-end="url(#arrow-std)" />
              <text id="svg-txt-p2-r2" x="140" y="142" fill="#64748b" font-size="8" font-weight="600" text-anchor="middle" opacity="0">req</text>

              <!-- Edge 4: R2 -> P1 (Left vertical) -->
              <line id="svg-edge-r2-p1" x1="60" y1="115" x2="60" y2="65" stroke="#cbd5e1" stroke-width="2.5" marker-end="url(#arrow-std)" />
              <text id="svg-txt-r2-p1" x="46" y="94" fill="#64748b" font-size="8" font-weight="600" text-anchor="middle" opacity="0">alloc</text>

              <!-- Nodes -->
              <!-- P1 Node (Top-Left) -->
              <circle id="svg-node-p1" cx="60" cy="50" r="18" fill="#ffffff" stroke="#0284c7" stroke-width="2.5" />
              <text x="60" y="54" fill="#0f172a" font-size="11" font-weight="bold" text-anchor="middle">P1</text>

              <!-- R1 Node (Top-Right) -->
              <rect id="svg-node-r1" x="205" y="35" width="30" height="30" rx="4" fill="#ffffff" stroke="#d97706" stroke-width="2.5" />
              <text x="220" y="54" fill="#d97706" font-size="10" font-weight="bold" text-anchor="middle">R1</text>

              <!-- P2 Node (Bottom-Right) -->
              <circle id="svg-node-p2" cx="220" cy="130" r="18" fill="#ffffff" stroke="#0284c7" stroke-width="2.5" />
              <text x="220" y="134" fill="#0f172a" font-size="11" font-weight="bold" text-anchor="middle">P2</text>

              <!-- R2 Node (Bottom-Left) -->
              <rect id="svg-node-r2" x="45" y="115" width="30" height="30" rx="4" fill="#ffffff" stroke="#d97706" stroke-width="2.5" />
              <text x="60" y="134" fill="#d97706" font-size="10" font-weight="bold" text-anchor="middle">R2</text>
            </svg>
          </div>
        </div>

        <div class="panes-grid">
          <div class="pane-box" style="border-left: 3px solid var(--success);">
            <div class="pane-title" style="color: var(--success);">&#128269; What Is Happening</div>
            <div id="pane-what" style="color: var(--text);">Process P1 acquires R1 and requests R2, establishing mutual exclusion and hold-and-wait semantics.</div>
          </div>
          <div class="pane-box" style="border-left: 3px solid var(--accent);">
            <div class="pane-title" style="color: var(--accent);">&#9881; Why The System Does This</div>
            <div id="pane-why" style="color: var(--text);">Hardware peripherals and database rows require exclusive locks to prevent data corruption during concurrent modification.</div>
          </div>
        </div>
      </div>

      <h4>4. How Operating System Kernels Use RAGs in Practice</h4>
      <p>
        Operating system kernels rarely draw full RAGs visually; instead, they maintain internal <strong>adjacency matrices</strong> or <strong>wait-for graphs</strong> (a compressed version where resource vertices are eliminated, leaving direct process-to-process dependency edges like $P_1 \to P_2$).
      </p>
      <p>
        Periodically or upon resource request failures, the OS deadlock-detection subsystem runs graph traversal algorithms (such as Depth-First Search with recursion stack tracking, as shown in the Python module below). If the algorithm detects a back-edge indicating a cycle, the kernel triggers its recovery protocol—aborting a deadlocked process or forcibly preempting a resource—to restore system liveness.
      </p>

      <h4>5. Algorithmic Cycle Detection (Python Implementation)</h4>
      <p>
        Below is a complete, syntax-highlighted Python module demonstrating directed graph representation and cycle detection:
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

def update_section_three():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>3. Resource Allocation Graphs (RAGs) &amp; Cycle Detection</h3>"
    if start_marker not in content:
        start_marker = "<h3>3. Resource Allocation Graphs (RAGs) & Cycle Detection</h3>"

    end_marker = "<h3>4. Banker's Algorithm</h3>"
    if end_marker not in content:
        # Fallback to navigation bar or end of card
        end_marker = '<nav class="nav-bar">'

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 3 boundaries in Module 02.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_THREE + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully integrated RAG deadlock theory into {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if update_section_three():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Incorporate comprehensive RAG deadlock theory into Module 02 Section 3\n\n"
                "Expand Section 3 with deep explanations connecting hardware contention,\n"
                "graph topology, cycle anatomy, single/multi-instance theorems, and kernels."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
