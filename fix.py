#!/usr/bin/env python3
# =====================================================================
# fix.py: Correct the position of analytical panes in Module 02 stepper
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

def fix_panes_position():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Re-structure the aid-grid markup to include panes correctly
    old_aid_grid_section = """        <div class="aid-grid">
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

          <div class="visual-canvas">
            <div style="font-weight: 700; font-size: 0.82rem; margin-bottom: 8px; color: var(--primary);">Synchronized Visual Canvas &mdash; RAG State</div>

            <!-- Unified Interactive SVG Canvas -->
            <svg viewBox="0 0 300 180" style="width: 100%; max-width: 280px; height: auto; background: #0f172a; border-radius: 8px; padding: 10px;">
              <defs>
                <marker id="arrow-std" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#64748b"/>
                </marker>
                <marker id="arrow-active" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#38bdf8"/>
                </marker>
                <marker id="arrow-danger" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#ef4444"/>
                </marker>
              </defs>

              <!-- Edges (Rendered behind nodes) -->
              <!-- Edge 1: P1 -> R1 (Top horizontal) -->
              <line id="svg-edge-p1-r1" x1="75" y1="50" x2="205" y2="50" stroke="#334155" stroke-width="2" marker-end="url(#arrow-std)" />
              <text id="svg-txt-p1-r1" x="140" y="42" fill="#64748b" font-size="8" text-anchor="middle" opacity="0">req</text>

              <!-- Edge 2: R1 -> P2 (Right vertical) -->
              <line id="svg-edge-r1-p2" x1="220" y1="65" x2="220" y2="115" stroke="#334155" stroke-width="2" marker-end="url(#arrow-std)" />
              <text id="svg-txt-r1-p2" x="232" y="94" fill="#64748b" font-size="8" text-anchor="middle" opacity="0">alloc</text>

              <!-- Edge 3: P2 -> R2 (Bottom horizontal) -->
              <line id="svg-edge-p2-r2" x1="205" y1="130" x2="75" y2="130" stroke="#334155" stroke-width="2" marker-end="url(#arrow-std)" />
              <text id="svg-txt-p2-r2" x="140" y="142" fill="#64748b" font-size="8" text-anchor="middle" opacity="0">req</text>

              <!-- Edge 4: R2 -> P1 (Left vertical) -->
              <line id="svg-edge-r2-p1" x1="60" y1="115" x2="60" y2="65" stroke="#334155" stroke-width="2" marker-end="url(#arrow-std)" />
              <text id="svg-txt-r2-p1" x="48" y="94" fill="#64748b" font-size="8" text-anchor="middle" opacity="0">alloc</text>

              <!-- Nodes -->
              <!-- P1 Node (Top-Left) -->
              <circle id="svg-node-p1" cx="60" cy="50" r="18" fill="#1e293b" stroke="#475569" stroke-width="2" />
              <text x="60" y="54" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">P1</text>

              <!-- R1 Node (Top-Right) -->
              <rect id="svg-node-r1" x="205" y="35" width="30" height="30" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2" />
              <text x="220" y="54" fill="#fbbf24" font-size="10" font-weight="bold" text-anchor="middle">R1</text>

              <!-- P2 Node (Bottom-Right) -->
              <circle id="svg-node-p2" cx="220" cy="130" r="18" fill="#1e293b" stroke="#475569" stroke-width="2" />
              <text x="220" y="134" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">P2</text>

              <!-- R2 Node (Bottom-Left) -->
              <rect id="svg-node-r2" x="45" y="115" width="30" height="30" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2" />
              <text x="60" y="134" fill="#fbbf24" font-size="10" font-weight="bold" text-anchor="middle">R2</text>
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
        </div>"""

    new_aid_grid_section = """        <div class="aid-grid">
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

          <div class="visual-canvas">
            <div style="font-weight: 700; font-size: 0.82rem; margin-bottom: 8px; color: var(--primary);">Synchronized Visual Canvas &mdash; RAG State</div>

            <!-- Unified Interactive SVG Canvas -->
            <svg viewBox="0 0 300 180" style="width: 100%; max-width: 280px; height: auto; background: #0f172a; border-radius: 8px; padding: 10px;">
              <defs>
                <marker id="arrow-std" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#64748b"/>
                </marker>
                <marker id="arrow-active" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#38bdf8"/>
                </marker>
                <marker id="arrow-danger" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#ef4444"/>
                </marker>
              </defs>

              <!-- Edges (Rendered behind nodes) -->
              <!-- Edge 1: P1 -> R1 (Top horizontal) -->
              <line id="svg-edge-p1-r1" x1="75" y1="50" x2="205" y2="50" stroke="#334155" stroke-width="2" marker-end="url(#arrow-std)" />
              <text id="svg-txt-p1-r1" x="140" y="42" fill="#64748b" font-size="8" text-anchor="middle" opacity="0">req</text>

              <!-- Edge 2: R1 -> P2 (Right vertical) -->
              <line id="svg-edge-r1-p2" x1="220" y1="65" x2="220" y2="115" stroke="#334155" stroke-width="2" marker-end="url(#arrow-std)" />
              <text id="svg-txt-r1-p2" x="232" y="94" fill="#64748b" font-size="8" text-anchor="middle" opacity="0">alloc</text>

              <!-- Edge 3: P2 -> R2 (Bottom horizontal) -->
              <line id="svg-edge-p2-r2" x1="205" y1="130" x2="75" y2="130" stroke="#334155" stroke-width="2" marker-end="url(#arrow-std)" />
              <text id="svg-txt-p2-r2" x="140" y="142" fill="#64748b" font-size="8" text-anchor="middle" opacity="0">req</text>

              <!-- Edge 4: R2 -> P1 (Left vertical) -->
              <line id="svg-edge-r2-p1" x1="60" y1="115" x2="60" y2="65" stroke="#334155" stroke-width="2" marker-end="url(#arrow-std)" />
              <text id="svg-txt-r2-p1" x="48" y="94" fill="#64748b" font-size="8" text-anchor="middle" opacity="0">alloc</text>

              <!-- Nodes -->
              <!-- P1 Node (Top-Left) -->
              <circle id="svg-node-p1" cx="60" cy="50" r="18" fill="#1e293b" stroke="#475569" stroke-width="2" />
              <text x="60" y="54" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">P1</text>

              <!-- R1 Node (Top-Right) -->
              <rect id="svg-node-r1" x="205" y="35" width="30" height="30" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2" />
              <text x="220" y="54" fill="#fbbf24" font-size="10" font-weight="bold" text-anchor="middle">R1</text>

              <!-- P2 Node (Bottom-Right) -->
              <circle id="svg-node-p2" cx="220" cy="130" r="18" fill="#1e293b" stroke="#475569" stroke-width="2" />
              <text x="220" y="134" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">P2</text>

              <!-- R2 Node (Bottom-Left) -->
              <rect id="svg-node-r2" x="45" y="115" width="30" height="30" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2" />
              <text x="60" y="134" fill="#fbbf24" font-size="10" font-weight="bold" text-anchor="middle">R2</text>
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
          </div>"""

    # Wait, let's look at where panes-grid should be. Per the Interactive Pedagogical Aid Standard:
    # "Navigation: Position stepper controls (Next/Prev/Reset) beside a dedicated inline preview panel giving a basic summary of what is currently happening..."
    # "Paired Analytical Panes: Provide two distinct explanation panels for every step: 1. 'What Is Happening' ... 2. 'Why The System Does This' ..."
    # Usually within the aid-grid or right below the visual canvas inside the aid wrapper. Let's place the panes-grid inside the aid-wrapper beneath the aid-grid (or spanning full width inside aid-wrapper).

    corrected_aid_wrapper = """      <div class="aid-wrapper">
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

          <div class="visual-canvas">
            <div style="font-weight: 700; font-size: 0.82rem; margin-bottom: 8px; color: var(--primary);">Synchronized Visual Canvas &mdash; RAG State</div>

            <!-- Unified Interactive SVG Canvas -->
            <svg viewBox="0 0 300 180" style="width: 100%; max-width: 280px; height: auto; background: #0f172a; border-radius: 8px; padding: 10px;">
              <defs>
                <marker id="arrow-std" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#64748b"/>
                </marker>
                <marker id="arrow-active" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#38bdf8"/>
                </marker>
                <marker id="arrow-danger" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 2 L 10 5 L 0 8 z" fill="#ef4444"/>
                </marker>
              </defs>

              <!-- Edges (Rendered behind nodes) -->
              <!-- Edge 1: P1 -> R1 (Top horizontal) -->
              <line id="svg-edge-p1-r1" x1="75" y1="50" x2="205" y2="50" stroke="#334155" stroke-width="2" marker-end="url(#arrow-std)" />
              <text id="svg-txt-p1-r1" x="140" y="42" fill="#64748b" font-size="8" text-anchor="middle" opacity="0">req</text>

              <!-- Edge 2: R1 -> P2 (Right vertical) -->
              <line id="svg-edge-r1-p2" x1="220" y1="65" x2="220" y2="115" stroke="#334155" stroke-width="2" marker-end="url(#arrow-std)" />
              <text id="svg-txt-r1-p2" x="232" y="94" fill="#64748b" font-size="8" text-anchor="middle" opacity="0">alloc</text>

              <!-- Edge 3: P2 -> R2 (Bottom horizontal) -->
              <line id="svg-edge-p2-r2" x1="205" y1="130" x2="75" y2="130" stroke="#334155" stroke-width="2" marker-end="url(#arrow-std)" />
              <text id="svg-txt-p2-r2" x="140" y="142" fill="#64748b" font-size="8" text-anchor="middle" opacity="0">req</text>

              <!-- Edge 4: R2 -> P1 (Left vertical) -->
              <line id="svg-edge-r2-p1" x1="60" y1="115" x2="60" y2="65" stroke="#334155" stroke-width="2" marker-end="url(#arrow-std)" />
              <text id="svg-txt-r2-p1" x="48" y="94" fill="#64748b" font-size="8" text-anchor="middle" opacity="0">alloc</text>

              <!-- Nodes -->
              <!-- P1 Node (Top-Left) -->
              <circle id="svg-node-p1" cx="60" cy="50" r="18" fill="#1e293b" stroke="#475569" stroke-width="2" />
              <text x="60" y="54" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">P1</text>

              <!-- R1 Node (Top-Right) -->
              <rect id="svg-node-r1" x="205" y="35" width="30" height="30" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2" />
              <text x="220" y="54" fill="#fbbf24" font-size="10" font-weight="bold" text-anchor="middle">R1</text>

              <!-- P2 Node (Bottom-Right) -->
              <circle id="svg-node-p2" cx="220" cy="130" r="18" fill="#1e293b" stroke="#475569" stroke-width="2" />
              <text x="220" y="134" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">P2</text>

              <!-- R2 Node (Bottom-Left) -->
              <rect id="svg-node-r2" x="45" y="115" width="30" height="30" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2" />
              <text x="60" y="134" fill="#fbbf24" font-size="10" font-weight="bold" text-anchor="middle">R2</text>
            </svg>
          </div>
        </div>

        <!-- Paired Analytical Panes positioned correctly at the bottom of the aid wrapper -->
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
      </div>"""

    # Locate aid-wrapper in content and replace it
    start_aid = content.find('<div class="aid-wrapper">')
    if start_aid == -1:
        print("Error: aid-wrapper not found.")
        return False

    # Find corresponding closing div of aid-wrapper. We can search for the start of section 4 or nav-bar following aid-wrapper
    end_aid_marker = "<h4>3. Algorithmic Cycle Detection"
    end_aid = content.find(end_aid_marker, start_aid)

    if end_aid == -1:
        print("Error: Could not find section 4 marker after aid-wrapper.")
        return False

    content = content[:start_aid] + corrected_aid_wrapper + "\n\n      " + content[end_aid:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully corrected analytical panes position in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if fix_panes_position():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Fix position of paired analytical panes in RAG interactive stepper\n\n"
                "Move 'What Is Happening' and 'Why The System Does This' panes into the\n"
                "correct grid layout alongside the controls and visual canvas."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
