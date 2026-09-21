#!/usr/bin/env python3
# =====================================================================
# fix.py: Optimize SVG vertical layout for address translation bypass
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def optimize_svg_layout():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace the oversized spacing block with tight, correct SVG positioning
    old_block = """            <!-- Offset Pass-Through Bypass Path -->
            <path id="trans-bypass-path" d="M 745,245 C 745,330 400,330 400,245" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />
            <text id="trans-bypass-label" x="572" y="348" fill="#64748b" font-size="9.5" text-anchor="middle">Page Offset (0x018) Passes Through Completely Unmodified to DRAM</text>

            <!-- Lower Topology Console -->
            <g transform="translate(25, 362)">
              <rect x="0" y="0" width="890" height="40" rx="6" fill="#f8fafc" stroke="#cbd5e1" />
              <text id="trans-console-top" x="15" y="25" fill="#0369a1" font-size="11" font-weight="700">TRANSLATION ENGINE STATUS: READY</text>
            </g>
          </svg>"""

    new_block = """            <!-- Offset Pass-Through Bypass Path -->
            <path id="trans-bypass-path" d="M 745,240 C 745,290 400,290 400,240" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />
            <text id="trans-bypass-label" x="572" y="310" fill="#64748b" font-size="9.5" text-anchor="middle">Page Offset (0x018) Passes Through Completely Unmodified to DRAM</text>

            <!-- Lower Topology Console -->
            <g transform="translate(25, 322)">
              <rect x="0" y="0" width="890" height="34" rx="6" fill="#f8fafc" stroke="#cbd5e1" />
              <text id="trans-console-top" x="15" y="22" fill="#0369a1" font-size="11" font-weight="700">TRANSLATION ENGINE STATUS: READY</text>
            </g>
          </svg>"""

    # Set viewBox height back to 365
    content = content.replace('viewBox="0 0 940 410"', 'viewBox="0 0 940 365"')
    content = content.replace('viewBox="0 0 940 370"', 'viewBox="0 0 940 365"')

    if old_block in content:
        content = content.replace(old_block, new_block)
        print("--> Adjusted curve, text label, and console positions.")
    else:
        # Fallback coordinate adjustments
        content = content.replace('C 745,330 400,330', 'C 745,290 400,290')
        content = content.replace('y="348"', 'y="310"')
        print("--> Applied fallback coordinate adjustments.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Optimize SVG vertical layout for address translation bypass path\n\n"
            "Position the bypass text label correctly beneath the curve and restore\n"
            "compact viewBox height in 02-hardware-review.html to eliminate excess spacing."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for layout optimization!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    optimize_svg_layout()
