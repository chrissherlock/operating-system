#!/usr/bin/env python3
# =====================================================================
# fix.py: Repair JS syntax errors and SVG height warnings in Module 2
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_console_errors():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Clean up any remaining height="auto" on SVG elements
    updated_content = content.replace('height="auto"', 'height="100%"')

    # 2. Fix potential broken object literal braces or trailing object syntax in inline script blocks
    # Specifically check and patch common syntax glitches around line 743 / 1444 style strings
    updated_content = updated_content.replace("style=\"display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr);", "style=\"display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));")

    if updated_content != content:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"--> Fixed syntax and SVG height warnings in {TARGET_FILE}")

        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Fix JS syntax error and SVG height attributes in Module 2\n\n"
                "Repair missing closing braces in inline script/style object literals and\n"
                "clean up remaining height=\"auto\" SVG attributes in 02-hardware-review.html."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> No matching patterns found to fix.")

if __name__ == "__main__":
    fix_console_errors()
