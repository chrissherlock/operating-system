#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix SVG line and text overlap with precise coordinate baselines
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_baseline_overlap():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Old block with overlapping or misaligned coordinates
    old_block = """            <!-- Offset Pass-Through Bypass Path -->
            <path id="trans-bypass-path" d="M 745,240 C 745,290 400,290 400,240" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />
            <text id="trans-bypass-label" x="572" y="310" fill="#64748b" font-size="9.5" text-anchor="middle">Page Offset (0x018) Passes Through Completely Unmodified to DRAM</text>

            <!-- Lower Topology Console -->
            <g transform="translate(25, 322)">
              <rect x="0" y="0" width="890" height="34" rx="6" fill="#f8fafc" stroke="#cbd5e1" />
              <text id="trans-console-top" x="15" y="22" fill="#0369a1" font-size="11" font-weight="700">TRANSLATION ENGINE STATUS: READY</text>
            </g>
          </svg>"""

    # New block with precise baseline separation: curve trough at 265, text baseline at 295, console at 310
    new_block = """            <!-- Offset Pass-Through Bypass Path -->
            <path id="trans-bypass-path" d="M 745,240 C 745,265 400,265 400,240" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />
            <text id="trans-bypass-label" x="572" y="295" fill="#64748b" font-size="9.5" text-anchor="middle">Page Offset (0x018) Passes Through Completely Unmodified to DRAM</text>

            <!-- Lower Topology Console -->
            <g transform="translate(25, 310)">
              <rect x="0" y="0" width="890" height="36" rx="6" fill="#f8fafc" stroke="#cbd5e1" />
              <text id="trans-console-top" x="15" y="23" fill="#0369a1" font-size="11" font-weight="700">TRANSLATION ENGINE STATUS: READY</text>
            </g>
          </svg>"""

    content = content.replace('viewBox="0 0 940 365"', 'viewBox="0 0 940 360"')
    content = content.replace('viewBox="0 0 940 340"', 'viewBox="0 0 940 360"')

    if old_block in content:
        content = content.replace(old_block, new_block)
        print("--> Updated bypass curve and text baseline coordinates.")
    else:
        # Fallback coordinate replacements
        content = content.replace('C 745,290 400,290', 'C 745,265 400,265')
        content = content.replace('y="310"', 'y="295"')
        print("--> Applied fallback coordinate adjustments.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix SVG line and text overlap by separating coordinate baselines\n\n"
            "Adjust the cubic bezier trough and text baseline y-coordinates within\n"
            "02-hardware-review.html to guarantee strict vertical separation."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for baseline separation fix!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_baseline_overlap()
