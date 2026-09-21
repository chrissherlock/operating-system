#!/usr/bin/env python3
# =====================================================================
# fix.py: Prevent text overflow across container boxes in Module 2
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_text_overflow():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Inject global overflow safety rules into the main style block
    overflow_css = """    * { box-sizing: border-box; margin: 0; padding: 0; overflow-wrap: break-word; word-break: break-word; }"""

    # Check if we can patch the universal selector rule
    old_universal = "* { box-sizing: border-box; margin: 0; padding: 0; }"
    if old_universal in content:
        content = content.replace(old_universal, overflow_css)
        print("--> Added overflow-wrap and word-break rules to universal selector.")
    else:
        # Fallback: append inside main <style> block
        style_marker = "<style>"
        if style_marker in content:
            content = content.replace(style_marker, style_marker + "\n    * { overflow-wrap: break-word; word-break: break-word; }")
            print("--> Added overflow rules via style marker fallback.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix text overflow bugs across card containers in Module 2\n\n"
            "Add word-break and flexible container rules in 02-hardware-review.html\n"
            "to prevent long technical strings and text from overflowing boxes."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for text overflow fix!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_text_overflow()
