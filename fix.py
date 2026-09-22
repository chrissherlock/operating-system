#!/usr/bin/env python3
# =====================================================================
# fix.py: Clean unrendered LaTeX delimiters from 04-os-structure.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "04-os-structure.html"
)

def strip_latex_delimiters():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace raw LaTeX in Section 2 prose
    replacements = [
        ("$0$", "0"),
        ("$N$", "N"),
        ("layer $M$", "layer <em>M</em>"),
        ("layer $M-1$", "layer <em>M</em> &minus; 1"),
        ("layer $M+1$", "layer <em>M</em> + 1"),
        ("$M$", "<em>M</em>"),
    ]

    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"--> Replaced '{old}' with '{new}'")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully cleaned LaTeX formatting from {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Remove unrendered LaTeX delimiters from Module 4 prose\n\n"
            "Replace raw dollar-delimited LaTeX variables ($0$, $N$, $M-1$, etc.) in\n"
            "Section 2 of 04-os-structure.html with standard HTML entities and text."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    strip_latex_delimiters()
