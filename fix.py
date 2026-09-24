#!/usr/bin/env python3
# =====================================================================
# fix.py: Upgrade RAG visual canvas to a single unified dynamic SVG
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

UNIFIED_CANVAS_HTML = r"""          <div class="visual-canvas">
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
          </div>"""

# Script update for updateUI()
NEW_UPDATE_UI_JS = """    function updateUI() {
      const data = stepsData[currentStep - 1];
      document.getElementById('preview-text').innerHTML = data.preview;

      document.getElementById('tel-phase').innerText = data.phase;
      document.getElementById('tel-edges').innerHTML = data.edges;
      document.getElementById('tel-cycle').innerText = data.cycle;

      const stateEl = document.getElementById('tel-state');
      stateEl.innerText = data.state;
      stateEl.style.color = data.stateColor;

      document.getElementById('pane-what').innerText = data.what;
      document.getElementById('pane-why').innerText = data.why;

      // Dynamic Unified SVG Canvas State Updates
      const e1 = document.getElementById('svg-edge-p1-r1');
      const e2 = document.getElementById('svg-edge-r1-p2');
      const e3 = document.getElementById('svg-edge-p2-r2');
      const e4 = document.getElementById('svg-edge-r2-p1');

      const t1 = document.getElementById('svg-txt-p1-r1');
      const t2 = document.getElementById('svg-txt-r1-p2');
      const t3 = document.getElementById('svg-txt-p2-r2');
      const t4 = document.getElementById('svg-txt-r2-p1');

      // Reset all edges to default inactive state
      [e1, e2, e3, e4].forEach(e => {
        e.setAttribute('stroke', '#334155');
        e.setAttribute('stroke-width', '2');
        e.setAttribute('marker-end', 'url(#arrow-std)');
      });
      [t1, t2, t3, t4].forEach(t => t.style.opacity = '0');

      if (currentStep === 1) {
        // P1 -> R1
        e1.setAttribute('stroke', '#38bdf8');
        e1.setAttribute('stroke-width', '2.5');
        e1.setAttribute('marker-end', 'url(#arrow-active)');
        t1.style.opacity = '1';
      } else if (currentStep === 2) {
        // P1 -> R1 and R1 -> P2
        e1.setAttribute('stroke', '#38bdf8');
        e1.setAttribute('stroke-width', '2.5');
        e1.setAttribute('marker-end', 'url(#arrow-active)');
        t1.style.opacity = '1';

        e2.setAttribute('stroke', '#38bdf8');
        e2.setAttribute('stroke-width', '2.5');
        e2.setAttribute('marker-end', 'url(#arrow-active)');
        t2.style.opacity = '1';
      } else if (currentStep === 3 || currentStep === 4) {
        // Full closed cycle: P1 -> R1 -> P2 -> R2 -> P1 (Illuminated in danger/red)
        [e1, e2, e3, e4].forEach(e => {
          e.setAttribute('stroke', '#ef4444');
          e.setAttribute('stroke-width', '3');
          e.setAttribute('marker-end', 'url(#arrow-danger)');
        });
        [t1, t2, t3, t4].forEach(t => {
          t.style.opacity = '1';
          t.style.fill = '#fca5a5';
        });
      }

      document.getElementById('prev-btn').disabled = (currentStep === 1);
      document.getElementById('next-btn').disabled = (currentStep === totalSteps);
    }"""

def upgrade_rag_canvas():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Find visual-canvas div block
    start_canvas = content.find('<div class="visual-canvas">')
    end_canvas = content.find('</div>\n        </div>', start_canvas)

    if start_canvas == -1 or end_canvas == -1:
        print("Error: Could not locate visual-canvas block in Module 02.")
        return False

    end_canvas_full = end_canvas + len('</div>\n        </div>')

    # Replace old canvas with unified dynamic canvas
    content = content[:start_canvas] + UNIFIED_CANVAS_HTML + content[end_canvas_full:]

    # Replace updateUI function
    old_update_ui_marker = "    function updateUI() {"
    idx_update = content.find(old_update_ui_marker)
    if idx_update != -1:
        idx_end_update = content.find("    }", idx_update)
        # Find the closing brace of updateUI
        # Let's search for the next function declaration or script end after idx_update
        idx_next_fn = content.find("    function ", idx_update + len(old_update_ui_marker))
        if idx_next_fn != -1:
            content = content[:idx_update] + NEW_UPDATE_UI_JS + "\n\n" + content[idx_next_fn:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully upgraded RAG canvas and updateUI in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if upgrade_rag_canvas():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Upgrade RAG visual canvas to unified dynamic SVG with live edge highlighting\n\n"
                "Consolidate separate SVG fragments into a single continuous canvas where\n"
                "active request/assignment edges and node boundaries illuminate in lockstep."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
