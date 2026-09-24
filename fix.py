#!/usr/bin/env python3
# =====================================================================
# fix.py: Refactor SVG canvas styling and layout in Module 02 interactive aid
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "02-deadlock-characterization-coffman-conditions.html"
)

def upgrade_canvas_styling():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace visual-canvas container and SVG markup within aid-wrapper
    old_visual_canvas = """          <div class="visual-canvas">
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

    new_visual_canvas = """          <div class="visual-canvas" style="display: flex; flex-direction: column; justify-content: space-between; height: 100%; background: #ffffff; border: 1px solid var(--border);">
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
          </div>"""

    if old_visual_canvas in content:
        content = content.replace(old_visual_canvas, new_visual_canvas)
    else:
        print("Warning: Exact visual-canvas block not found, check markup.")

    # Also adjust stroke colors in updateUI for light theme
    old_svg_reset_js = """      // Reset all edges to default inactive state
      [e1, e2, e3, e4].forEach(e => {
        e.setAttribute('stroke', '#334155');
        e.setAttribute('stroke-width', '2');
        e.setAttribute('marker-end', 'url(#arrow-std)');
      });"""

    new_svg_reset_js = """      // Reset all edges to default inactive state
      [e1, e2, e3, e4].forEach(e => {
        e.setAttribute('stroke', '#cbd5e1');
        e.setAttribute('stroke-width', '2.5');
        e.setAttribute('marker-end', 'url(#arrow-std)');
      });"""

    if old_svg_reset_js in content:
        content = content.replace(old_svg_reset_js, new_svg_reset_js)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully upgraded canvas styling in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if upgrade_canvas_styling():
        try:
            # Note use of /usr/bin/env python3 per repository guidelines
            with open("fix.py", "r") as check_f:
                script_text = check_f.read()
            if "#!/usr/bin/env python3" in script_text:
                script_text = script_text.replace("#!/usr/bin/env python3", "#!/usr/bin/env python3")
                with open("fix.py", "w") as check_f:
                    check_f.write(script_text)

            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Remove dark SVG background and expand visual canvas to fill space\n\n"
                "Replace dark SVG container background with a clean light theme surface,\n"
                "and adjust CSS flex properties to fill available vertical space."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
