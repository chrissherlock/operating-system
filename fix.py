#!/usr/bin/env python3
# =====================================================================
# fix.py: Correct arrow marker orientations in 03-interactive-scheduling.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week03-process-scheduling", "03-interactive-scheduling.html")

def fix_mlfq_arrows():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate defs block inside the MLFQ canvas
    defs_start = content.find("<defs>", content.find('class="mlfq-canvas"'))
    defs_end = content.find("</defs>", defs_start) + len("</defs>")

    clean_defs = r"""<defs>
            <!-- Standard horizontal right-pointing markers (orient="auto" handles all curve tangents accurately) -->
            <marker id="m-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
            </marker>
            <marker id="m-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
            </marker>
            <marker id="m-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
            </marker>
          </defs>"""

    content = content[:defs_start] + clean_defs + content[defs_end:]

    # Replace the demote and boost path elements with clean coordinates and correct markers
    old_paths_start = '<path id="path-mlfq-demote"'
    paths_end = content.find("</svg>", content.find(old_paths_start))

    new_paths = r"""<!-- Dynamic Demotion & Priority Boost Pathways -->
          <g id="grp-mlfq-demote" style="display: none;">
            <line x1="315" y1="80" x2="315" y2="103" stroke="#dc2626" stroke-width="2.5" marker-end="url(#m-arr-red)"/>
            <rect x="325" y="84" width="90" height="18" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="1"/>
            <text x="370" y="96" text-anchor="middle" font-family="var(--font-mono)" font-size="8" font-weight="700" fill="#991b1b">DEMOTE Q0&rarr;Q1</text>
          </g>

          <g id="grp-mlfq-boost" style="display: none;">
            <!-- Smooth upward curved path from bottom queue Q2 (y=220) to top queue Q0 (y=50) -->
            <path d="M 470 220 C 510 220, 510 50, 483 50" fill="none" stroke="#059669" stroke-width="2.5" stroke-dasharray="4 3" marker-end="url(#m-arr-green)"/>
            <rect x="425" y="125" width="85" height="24" rx="3" fill="#dcfce7" stroke="#059669" stroke-width="1"/>
            <text x="467" y="137" text-anchor="middle" font-family="var(--font-mono)" font-size="8" font-weight="700" fill="#166534">PRIORITY BOOST</text>
            <text x="467" y="145" text-anchor="middle" font-size="7.5" fill="#15803d">ALL QUEUES&rarr;Q0</text>
          </g>
        """

    content = content[:content.find(old_paths_start)] + new_paths + content[paths_end:]

    # Update the JS toggle from path-mlfq-demote to grp-mlfq-demote
    content = content.replace('document.getElementById("path-mlfq-demote").style.display', 'document.getElementById("grp-mlfq-demote").style.display')
    content = content.replace('document.getElementById("path-mlfq-boost").style.display', 'document.getElementById("grp-mlfq-boost").style.display')

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully corrected MLFQ arrowheads and paths in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix marker orientations and arrowpaths in Module 03 MLFQ stepper\n\n"
            "Standardize markers to right-pointing base vectors with orient=\"auto\"\n"
            "and align demotion and boost trajectory vectors cleanly between queues."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_mlfq_arrows()
