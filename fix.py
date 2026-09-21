#!/usr/bin/env python3
# =====================================================================
# fix.py: Replace raw LaTeX markup with clean HTML in 02-hardware-review.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def sanitize_latex_in_simulator():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replacements for escaped LaTeX strings inside JavaScript data objects
    replacements = [
        (
            '($k-1$ cycles)',
            '(<em>k</em> - 1 cycles, where <em>k</em> = 4 stages, requiring 3 warm-up cycles)'
        ),
        (
            '($k = 4$)',
            '(<em>k</em> = 4 stages)'
        ),
        (
            '($k=4$)',
            '(<em>k</em> = 4 stages)'
        ),
        (
            '($N \\to \\infty$)',
            '(as instruction count <em>N</em> grows large)'
        ),
        (
            '($N \\\\to \\\\infty$)',
            '(as instruction count <em>N</em> grows large)'
        ),
        (
            '($4 \\times 4$)',
            '(4 instructions &times; 4 stages)'
        ),
        (
            '($4 \\\\times 4$)',
            '(4 instructions &times; 4 stages)'
        ),
        (
            '$IPC > 1.0$',
            'IPC &gt; 1.0'
        ),
        (
            '$k-1$',
            '<em>k</em> - 1'
        )
    ]

    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)

    if new_content != content:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"--> Successfully replaced escaped LaTeX with clean HTML in {TARGET_FILE}")

        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Replace escaped LaTeX math markup with standard HTML in Module 2\n\n"
                "Convert raw LaTeX ($k-1$, $k=4$, $IPC > 1.0$) inside simulator strings\n"
                "in 02-hardware-review.html into clean, semantic HTML formatting."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully for LaTeX markup cleanup!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> No raw LaTeX instances found to replace.")

if __name__ == "__main__":
    sanitize_latex_in_simulator()
