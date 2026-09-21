#!/usr/bin/env python3
# =====================================================================
# fix.py: Replace raw LaTeX markup with HTML superscripts
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_latex_markup():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace raw LaTeX exponent expression with HTML superscripts
    old_expr = "$2^{12} = 4096$"
    new_expr = "2<sup>12</sup> = 4096"

    if old_expr in content:
        content = content.replace(old_expr, new_expr)
        print("--> Replaced raw LaTeX math with clean HTML superscripts.")
    else:
        print("--> Target LaTeX expression not found exactly; searching for variants.")
        content = content.replace("$2^{12}$", "2<sup>12</sup>")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Replace raw LaTeX markup with HTML superscripts in Module 2 guide card\n\n"
            "Substitute `$2^{12} = 4096$` with `2<sup>12</sup> = 4096` in the scenario\n"
            "briefing card within 02-hardware-review.html to prevent raw markup leak."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for LaTeX markup fix!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_latex_markup()
