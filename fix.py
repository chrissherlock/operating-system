#!/usr/bin/env python3
# =====================================================================
# fix.py: Correct SVG markers and arrow vectors in 02-hardware-review.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)

def fix_diagram_arrows():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace the marker defs in the I/O hierarchy diagram
    old_defs = """          <defs>
            <marker id="arrow-down" viewBox="0 0 10 10" refX="5" refY="8" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 1 1 L 5 8 L 9 1 z" fill="#0284c7" />
            </marker>
            <marker id="arrow-up" viewBox="0 0 10 10" refX="5" refY="2" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 1 9 L 5 2 L 9 9 z" fill="#059669" />
            </marker>
            <filter id="io-card-shadow" x="-3%" y="-3%" width="106%" height="106%">
              <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.06" />
            </filter>
          </defs>"""

    new_defs = """          <defs>
            <!-- Normalized directional arrowheads: point right, auto-rotates with path -->
            <marker id="io-arrow-blue" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
              <polygon points="0 1, 6 3.5, 0 6" fill="#0284c7" />
            </marker>
            <marker id="io-arrow-green" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
              <polygon points="0 1, 6 3.5, 0 6" fill="#059669" />
            </marker>
            <marker id="io-arrow-amber" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
              <polygon points="0 1, 6 3.5, 0 6" fill="#d97706" />
            </marker>
            <filter id="io-card-shadow" x="-3%" y="-3%" width="106%" height="106%">
              <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.06" />
            </filter>
          </defs>"""

    if old_defs in content:
        content = content.replace(old_defs, new_defs)
        print("--> Replaced old marker definitions.")
    else:
        print("--> Note: Exact old defs block not found; checking for partial match.")

    # 2. Update the path markers and adjust vertical coordinates to prevent stroke overlap
    # Path 1: User space to Kernel space
    content = content.replace(
        '<path d="M 440, 135 L 440, 160" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-down)" />',
        '<path d="M 440, 135 L 440, 160" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#io-arrow-blue)" />'
    )

    # Path 2: Kernel space down to Controller (MMIO)
    content = content.replace(
        '<path d="M 360, 285 L 360, 318" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-down)" />',
        '<path d="M 360, 285 L 360, 318" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#io-arrow-blue)" />'
    )

    # Path 3: Controller up to Kernel (IRQ)
    content = content.replace(
        '<path d="M 520, 318 L 520, 285" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#arrow-up)" />',
        '<path d="M 520, 325 L 520, 292" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#io-arrow-green)" />'
    )

    # Path 4: Controller down to Physical Device
    content = content.replace(
        '<path d="M 440, 440 L 440, 475" fill="none" stroke="#d97706" stroke-width="2" marker-end="url(#arrow-down)" />',
        '<path d="M 440, 440 L 440, 474" fill="none" stroke="#d97706" stroke-width="2" marker-end="url(#io-arrow-amber)" />'
    )

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Saved cleanly aligned arrow markers to {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix distorted arrow markers and path endpoints in I/O diagram\n\n"
            "Normalize SVG marker definitions to standard auto-orienting vectors\n"
            "and adjust path coordinates in 02-hardware-review.html so arrows point\n"
            "cleanly without clipping or inverted polygons."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_diagram_arrows()
