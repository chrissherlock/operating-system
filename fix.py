#!/usr/bin/env python3
# =====================================================================
# fix.py: Highlight active node in Syscall Story diagram in orange
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def apply_orange_active_highlight():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate the activeNode styling logic in renderTrapState
    old_highlight_pattern = r'const activeNodeEl = document\.getElementById\(data\.activeNode\);[\s\S]*?activeNodeEl\.setAttribute\("fill",.*?\);[\s\S]*?}'

    new_highlight_snippet = """const activeNodeEl = document.getElementById(data.activeNode);
            if (activeNodeEl) {
              activeNodeEl.setAttribute("stroke", "#ea580c");
              activeNodeEl.setAttribute("stroke-width", "3");
              activeNodeEl.setAttribute("fill", "#fff7ed");
              activeNodeEl.style.filter = "drop-shadow(0 0 6px rgba(234, 88, 12, 0.45))";
            }"""

    # Also make sure other inactive nodes reset their filter
    old_reset_pattern = r'(el\.setAttribute\("fill", "#ffffff"\);)'
    new_reset_snippet = r'\1\n                el.style.filter = "none";'

    modified_content = re.sub(old_highlight_pattern, new_highlight_snippet, content)
    modified_content = re.sub(old_reset_pattern, new_reset_snippet, modified_content)

    if modified_content != content:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(modified_content)
        print("--> Updated active diagram node to vivid orange styling.")

        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Highlight active stage in Syscall Story SVG diagram in orange\n\n"
                "Update renderTrapState in 02-hardware-review.html to apply vivid orange\n"
                "stroke and background to the active node for clear visual emphasis."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully for 02-hardware-review.html!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> Warning: Target pattern not matched in 02-hardware-review.html.")

if __name__ == "__main__":
    apply_orange_active_highlight()
