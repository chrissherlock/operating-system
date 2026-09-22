#!/usr/bin/env python3
# =====================================================================
# fix.py: Correct SVG markers in Anatomy of a Process in Memory diagram
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "03-os-concepts.html"
)

def fix_process_memory_arrows():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Old defs and path snippet in Diagram 1
    old_snippet = """        <defs>
          <marker id="arrowUp" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
            <path d="M3,6 L0,0 L6,0 Z" fill="#0284c7" />
          </marker>
          <marker id="arrowDown" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
            <path d="M3,0 L0,6 L6,6 Z" fill="#0284c7" />
          </marker>
        </defs>"""

    new_snippet = """        <defs>
          <marker id="mem-arrow-red" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#ef4444" />
          </marker>
          <marker id="mem-arrow-blue" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#0284c7" />
          </marker>
        </defs>"""

    if old_snippet in content:
        content = content.replace(old_snippet, new_snippet)
        print("--> Updated marker definitions in memory layout diagram.")
    else:
        print("--> Note: Exact old marker block not found; replacing individually if present.")
        content = content.replace('marker id="arrowUp"', 'marker id="mem-arrow-blue"')
        content = content.replace('marker id="arrowDown"', 'marker id="mem-arrow-red"')

    # Update the path usages for Stack and Heap growth
    content = content.replace(
        '<path d="M 340,78 L 340,94" fill="none" stroke="#ef4444" stroke-width="2" marker-end="url(#arrowDown)" />',
        '<path d="M 340,76 L 340,96" fill="none" stroke="#ef4444" stroke-width="2" marker-end="url(#mem-arrow-red)" />'
    )
    content = content.replace(
        '<path d="M 340,186 L 340,170" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowUp)" />',
        '<path d="M 340,190 L 340,170" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#mem-arrow-blue)" />'
    )

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Saved corrected memory arrows to {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix distorted arrows and marker colors in process memory diagram\n\n"
            "Normalize SVG marker definitions to standard auto-orienting vectors and\n"
            "separate stack (red) and heap (blue) marker IDs in 03-os-concepts.html\n"
            "so directional arrows render straight and cleanly aligned."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_process_memory_arrows()
