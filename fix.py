#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix priority boost arrow trajectory in 03-interactive-scheduling.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week03-process-scheduling", "03-interactive-scheduling.html")

def repair_boost_arrow():
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

    # We construct a clean path that arches up and points cleanly UP into Queue Q0:
    # From right-side of Q2 (x=460, y=210), curves out to x=500, travels upwards,
    # and curves into Q0 terminating at (460, 46) pointing strictly LEFT into Q0,
    # OR terminating going strictly UPWARDS into Q0 at (460, 42).
    #
    # Let's make it an unmistakable UPWARD promotion arrow:
    # Starting at (475, 210), sweeping up through an arc, and rising straight UP into Q0:
    # "M 475 210 C 510 210, 510 80, 480 80 C 470 80, 470 65, 470 52"
    # Tangent at (470, 52) comes from (470, 65) -> dx=0, dy=-13 -> Angle is -90° (strictly UP).
    new_boost_block = r"""<g id="grp-mlfq-boost" style="display: none;">
            <!-- Upward promotional path: loops out from Q2, rises up, and vectors straight UP into Q0 -->
            <path d="M 465 210 C 505 210, 505 85, 475 85 C 465 85, 465 68, 465 52" fill="none" stroke="#059669" stroke-width="2.5" stroke-dasharray="4 3" marker-end="url(#m-arr-green)"/>
            <rect x="425" y="125" width="85" height="26" rx="3" fill="#dcfce7" stroke="#059669" stroke-width="1.2"/>
            <text x="467" y="138" text-anchor="middle" font-family="var(--font-mono)" font-size="8" font-weight="700" fill="#166534">&uarr; PRIORITY BOOST</text>
            <text x="467" y="147" text-anchor="middle" font-size="7.5" fill="#15803d">ALL QUEUES &rarr; Q0</text>
          </g>"""

    content = content[:start_idx] + new_boost_block + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully updated boost arrow trajectory in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix priority boost arrow trajectory and endpoint tangent in Module 03\n\n"
            "Adjust Bézier control points so the boost path terminates with a clear\n"
            "upward-pointing vector into Queue Q0, eliminating rotated marker skew."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if repair_boost_arrow():
        run_git_sync()
