#!/usr/bin/env python3
# =====================================================================
# fix.py: Lower bypass text label slightly for proper clearance
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def lower_bypass_label():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Target text line y=300 and console transform y=312
    old_block = """            <!-- Offset Pass-Through Bypass Path -->
            <path id="trans-bypass-path" d="M 745,245 C 745,305 400,305 400,245" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />
            <text id="trans-bypass-label" x="572" y="300" fill="#64748b" font-size="9.5" text-anchor="middle">Page Offset (0x018) Passes Through Completely Unmodified to DRAM</text>

            <!-- Lower Topology Console -->
            <g transform="translate(25, 312)">"""

    new_block = """            <!-- Offset Pass-Through Bypass Path -->
            <path id="trans-bypass-path" d="M 745,245 C 745,305 400,305 400,245" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,4" />
            <text id="trans-bypass-label" x="572" y="312" fill="#64748b" font-size="9.5" text-anchor="middle">Page Offset (0x018) Passes Through Completely Unmodified to DRAM</text>

            <!-- Lower Topology Console -->
            <g transform="translate(25, 324)">"""

    # Also expand viewBox height slightly to 370 to accommodate the shift
    old_viewbox = '<svg id="trans-anim-svg" viewBox="0 0 940 360"'
    new_viewbox = '<svg id="trans-anim-svg" viewBox="0 0 940 370"'

    if old_block in content:
        content = content.replace(old_block, new_block)
        print("--> Lowered bypass text label to y=312 and pushed console down.")
    else:
        # Fallback replacement for text label alone
        content = content.replace('id="trans-bypass-label" x="572" y="300"', 'id="trans-bypass-label" x="572" y="312"')
        print("--> Applied fallback replacement for bypass label coordinate.")

    if old_viewbox in content:
        content = content.replace(old_viewbox, new_viewbox)
        print("--> Expanded SVG viewBox height to 370.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Lower bypass text label slightly to prevent line overlap in translation sim\n\n"
            "Adjust the y-coordinate of the bypass text label in 02-hardware-review.html\n"
            "from 300 to 312 to provide proper clearance below the dashed pass-through line."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for bypass label lowering!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    lower_bypass_label()
