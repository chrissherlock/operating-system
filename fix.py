#!/usr/bin/env python3
# =====================================================================
# fix.py: Correct bounding boxes and spacing in Figure 2.2 of Module 02
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week04-concurrency-and-mutual-exclusion",
    "02-hardware-primitives-spinlocks.html"
)

NEW_FIGURE_2_2 = r"""    <!-- Structural Diagram: Peterson's Protocol & Memory State -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 2.2: Peterson's Tie-Breaker Arbitration Flow</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">Accurate bounding boxes showing how intent flags and the polite turn variable resolve contention in physical memory.</div>

      <svg viewBox="0 0 760 250" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="pet-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="pet-arr-amber" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#d97706" />
          </marker>
          <marker id="pet-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
        </defs>

        <!-- Process 0 Column (Left) -->
        <g transform="translate(20, 15)">
          <rect width="215" height="220" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="16" y="26" font-size="10.5" font-weight="700" fill="#0284c7">PROCESS 0 (T0)</text>

          <!-- Step 1 -->
          <rect x="12" y="38" width="191" height="42" rx="5" fill="#e0f2fe" stroke="#0284c7" stroke-width="1"/>
          <text x="20" y="54" font-size="8" font-weight="700" fill="#0369a1">1. SET INTENT</text>
          <text x="20" y="70" font-family="var(--font-mono)" font-size="9.5" font-weight="600" fill="#0f172a">flag[0] = true</text>

          <!-- Step 2 -->
          <rect x="12" y="88" width="191" height="44" rx="5" fill="#e0f2fe" stroke="#0284c7" stroke-width="1"/>
          <text x="20" y="104" font-size="8" font-weight="700" fill="#0369a1">2. YIELD PRIORITY (First)</text>
          <text x="20" y="121" font-family="var(--font-mono)" font-size="9.5" font-weight="600" fill="#0f172a">turn = 1</text>

          <!-- Step 3 -->
          <rect x="12" y="140" width="191" height="66" rx="5" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
          <text x="20" y="157" font-size="8" font-weight="700" fill="#166534">3. WHILE CONDITION EVALUATION</text>
          <text x="20" y="173" font-family="var(--font-mono)" font-size="8" fill="#166534">turn == 1 is FALSE (overwritten!)</text>
          <text x="20" y="191" font-size="8.5" font-weight="700" fill="#059669">&#10003; ENTERS CRITICAL REGION</text>
        </g>

        <!-- Shared Physical Memory (Center) -->
        <g transform="translate(255, 15)">
          <rect width="250" height="220" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <text x="125" y="26" text-anchor="middle" font-size="11" font-weight="700" fill="#0f172a">SHARED PHYSICAL MEMORY</text>

          <!-- Intent Array Box -->
          <rect x="14" y="38" width="222" height="52" rx="5" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.5"/>
          <text x="22" y="55" font-size="8.5" font-weight="700" fill="#0369a1">INTENT ARRAY: flag[2]</text>
          <text x="22" y="74" font-family="var(--font-mono)" font-size="11" font-weight="700" fill="#0f172a">flag[0]=true &nbsp;|&nbsp; flag[1]=true</text>

          <!-- Turn Variable Box -->
          <rect x="14" y="98" width="222" height="108" rx="5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
          <text x="22" y="116" font-size="8.5" font-weight="700" fill="#475569">TIE-BREAKER SCALAR: turn</text>
          <text x="22" y="136" font-family="var(--font-mono)" font-size="8.5" fill="#64748b">1. P0 writes: turn = 1</text>
          <text x="22" y="154" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#d97706">2. P1 writes: turn = 0 (FINAL)</text>
          <line x1="22" y1="166" x2="226" y2="166" stroke="#e2e8f0" stroke-width="1"/>
          <text x="125" y="184" text-anchor="middle" font-size="8" font-weight="700" fill="#059669">Winner: turn == 0 satisfies P0</text>
          <text x="125" y="196" text-anchor="middle" font-size="7.5" fill="#dc2626">turn == 0 forces P1 to spin!</text>
        </g>

        <!-- Process 1 Column (Right) -->
        <g transform="translate(525, 15)">
          <rect width="215" height="220" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="16" y="26" font-size="10.5" font-weight="700" fill="#d97706">PROCESS 1 (T1)</text>

          <!-- Step 1 -->
          <rect x="12" y="38" width="191" height="42" rx="5" fill="#fef3c7" stroke="#d97706" stroke-width="1"/>
          <text x="20" y="54" font-size="8" font-weight="700" fill="#92400e">1. SET INTENT</text>
          <text x="20" y="70" font-family="var(--font-mono)" font-size="9.5" font-weight="600" fill="#0f172a">flag[1] = true</text>

          <!-- Step 2 -->
          <rect x="12" y="88" width="191" height="44" rx="5" fill="#fef3c7" stroke="#d97706" stroke-width="1"/>
          <text x="20" y="104" font-size="8" font-weight="700" fill="#92400e">2. YIELD PRIORITY (Second)</text>
          <text x="20" y="121" font-family="var(--font-mono)" font-size="9.5" font-weight="600" fill="#0f172a">turn = 0</text>

          <!-- Step 3 -->
          <rect x="12" y="140" width="191" height="66" rx="5" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
          <text x="20" y="157" font-size="8" font-weight="700" fill="#991b1b">3. WHILE CONDITION EVALUATION</text>
          <text x="20" y="173" font-family="var(--font-mono)" font-size="8" fill="#991b1b">turn == 0 is TRUE &amp; flag[0]==true</text>
          <text x="20" y="191" font-size="8.5" font-weight="700" fill="#dc2626">&#10005; SPINS UNTIL P0 LEAVES</text>
        </g>
      </svg>
    </div>"""

def fix_figure_bounding_boxes():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- Structural Diagram: Peterson's Protocol & Memory State -->"
    end_marker = "<h4>Formal Mathematical Proof of Correctness</h4>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Figure 2.2 markers in Module 02.")
        return False

    updated_content = content[:start_idx] + NEW_FIGURE_2_2 + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully aligned Figure 2.2 bounding boxes in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix SVG bounding boxes and layout margins in Figure 2.2 of Module 02\n\n"
            "Adjust viewBox dimensions, vertically space step boxes, and align\n"
            "Process 0, Shared Memory, and Process 1 bounding boxes in Peterson SVG."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if fix_figure_bounding_boxes():
        run_git_sync()
