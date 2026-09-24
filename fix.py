#!/usr/bin/env python3
# =====================================================================
# fix.py: Reroute Priority Boost arrow directly into Queue Q0
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week03-process-scheduling", "03-interactive-scheduling.html")

def fix_boost_target():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate the grp-mlfq-boost SVG block
    old_boost_start = '<g id="grp-mlfq-boost"'
    old_boost_end = '</g>'

    start_idx = content.find(old_boost_start)
    if start_idx == -1:
        print("Error: Could not find grp-mlfq-boost block.")
        return False

    end_idx = content.find(old_boost_end, start_idx) + len(old_boost_end)

    # Queue Q0 is at y=20 to 80 (Height=60)
    # Queue Q1 is at y=105 to 165
    # Queue Q2 is at y=190 to 250
    #
    # We route a dedicated upward promotion conduit along x = 430
    # rising straight up from the top edge of Q2 (y=190) through the gap,
    # right past Q1, and terminating cleanly at the bottom edge of Q0 (y=84).
    #
    # With orient="auto" and a line from (430, 190) to (430, 84), dy < 0:
    # The arrow points strictly straight UP, terminating right against Q0's border!
    new_boost_block = r"""<g id="grp-mlfq-boost" style="display: none;">
            <!-- Vertical promotion shaft: rises from Q2 (y=190) directly UP into Q0 (y=84) -->
            <line x1="435" y1="190" x2="435" y2="84" stroke="#059669" stroke-width="3" stroke-dasharray="4 3" marker-end="url(#m-arr-green)"/>

            <!-- Clarifying text badge pinned to the shaft -->
            <rect x="360" y="122" width="150" height="26" rx="4" fill="#dcfce7" stroke="#059669" stroke-width="1.5"/>
            <text x="435" y="135" text-anchor="middle" font-family="var(--font-mono)" font-size="8.5" font-weight="700" fill="#166534">&uarr; PRIORITY BOOST</text>
            <text x="435" y="144" text-anchor="middle" font-size="7.5" fill="#15803d">PROMOTED: Q2 &amp; Q1 &rarr; Q0</text>
          </g>"""

    content = content[:start_idx] + new_boost_block + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully rerouted priority boost arrow in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix priority boost arrow routing and destination target in Module 03\n\n"
            "Route the promotional boost path directly from Queue Q2 vertically up\n"
            "into the entrance of Queue Q0 so the destination target is unambiguous."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if fix_boost_target():
        run_git_sync()
