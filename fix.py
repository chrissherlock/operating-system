#!/usr/bin/env python3
# =====================================================================
# fix.py: Deepen bypass curve and lower text label for clean separation
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_curve_text_separation():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Old SVG block with overlapping coordinates
    old_svg_block = """            <!-- Offset Pass-Through Bypass Path -->
            <path id="trans-bypass-path" d="M 745,245 C 745,305 400,305 400,245" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />
            <text id="trans-bypass-label" x="572" y="312" fill="#64748b" font-size="9.5" text-anchor="middle">Page Offset (0x018) Passes Through Completely Unmodified to DRAM</text>

            <!-- Lower Topology Console -->
            <g transform="translate(25, 324)">"""

    # New SVG block with separated coordinates (curve dips to 330, text sits at 345, console at 360)
    new_svg_block = """            <!-- Offset Pass-Through Bypass Path -->
            <path id="trans-bypass-path" d="M 745,245 C 745,330 400,330 400,245" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />
            <text id="trans-bypass-label" x="572" y="348" fill="#64748b" font-size="9.5" text-anchor="middle">Page Offset (0x018) Passes Through Completely Unmodified to DRAM</text>

            <!-- Lower Topology Console -->
            <g transform="translate(25, 362)">"""

    # Update viewBox height to 400
    old_viewbox = '<svg id="trans-anim-svg" viewBox="0 0 940 370"'
    new_viewbox = '<svg id="trans-anim-svg" viewBox="0 0 940 410"'

    if old_svg_block in content:
        content = content.replace(old_svg_block, new_svg_block)
        print("--> Updated bypass path curve depth and text label placement.")
    else:
        # Fallback coordinate replacements
        content = content.replace('C 745,305 400,305', 'C 745,330 400,330')
        content = content.replace('y="312"', 'y="348"')
        print("--> Applied fallback coordinate adjustments.")

    if old_viewbox in content:
        content = content.replace(old_viewbox, new_viewbox)
    else:
        content = content.replace('viewBox="0 0 940 370"', 'viewBox="0 0 940 410"')
        content = content.replace('viewBox="0 0 940 360"', 'viewBox="0 0 940 410"')

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix SVG line and text overlap by deepening bypass curve and lowering text\n\n"
            "Adjust cubic bezier control points and text y-coordinates within\n"
            "02-hardware-review.html to create clean vertical separation."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for curve/text separation fix!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_curve_text_separation()
