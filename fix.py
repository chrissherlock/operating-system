#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix SVG text overlapping line in address translation bypass path
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_svg_text_overlap():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Old SVG markup for translation simulator canvas & bypass path
    old_svg_block = """            <!-- Offset Pass-Through Bypass Path -->
            <path id="trans-bypass-path" d="M 745,245 C 745,290 400,290 400,245" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />
            <text id="trans-bypass-label" x="572" y="278" fill="#64748b" font-size="9.5" text-anchor="middle">Page Offset (0x018) Passes Through Completely Unmodified to DRAM</text>

            <!-- Lower Topology Console -->
            <g transform="translate(25, 290)">
              <rect x="0" y="0" width="890" height="40" rx="6" fill="#f8fafc" stroke="#cbd5e1" />
              <text id="trans-console-top" x="15" y="25" fill="#0369a1" font-size="11" font-weight="700">TRANSLATION ENGINE STATUS: READY</text>
            </g>
          </svg>"""

    # Updated SVG markup with adjusted vertical spacing and viewBox
    new_svg_block = """            <!-- Offset Pass-Through Bypass Path -->
            <path id="trans-bypass-path" d="M 745,245 C 745,305 400,305 400,245" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />
            <text id="trans-bypass-label" x="572" y="300" fill="#64748b" font-size="9.5" text-anchor="middle">Page Offset (0x018) Passes Through Completely Unmodified to DRAM</text>

            <!-- Lower Topology Console -->
            <g transform="translate(25, 312)">
              <rect x="0" y="0" width="890" height="40" rx="6" fill="#f8fafc" stroke="#cbd5e1" />
              <text id="trans-console-top" x="15" y="25" fill="#0369a1" font-size="11" font-weight="700">TRANSLATION ENGINE STATUS: READY</text>
            </g>
          </svg>"""

    # Also update viewBox height from 340 to 360
    old_viewbox = '<svg id="trans-anim-svg" viewBox="0 0 940 340"'
    new_viewbox = '<svg id="trans-anim-svg" viewBox="0 0 940 360"'

    if old_svg_block in content:
        content = content.replace(old_svg_block, new_svg_block)
        print("--> Updated bypass path curve and label coordinates.")
    else:
        print("--> Warning: Exact bypass path block pattern not matched.")

    if old_viewbox in content:
        content = content.replace(old_viewbox, new_viewbox)
        print("--> Expanded SVG viewBox height to 360.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix SVG text and line overlap in address translation bypass path\n\n"
            "Adjust SVG viewBox height, curve coordinates, and text label positioning\n"
            "within 02-hardware-review.html to prevent the bypass label from overlapping the line."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for SVG overlap fix!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_svg_text_overlap()
