#!/usr/bin/env python3
# =====================================================================
# fix.py: Replace leaked HTML entities with UTF-8 in Module 01 stepper
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week04-concurrency-and-mutual-exclusion", "01-race-conditions-critical-regions.html")

def fix_entity_leaks():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace leaked entities inside the JavaScript stepper definition
    replacements = [
        ("&mu;s", "μs"),
        ("&times;", "×"),
        ("&check;", "✓"),
        ("&rarr;", "→"),
        ("&larr;", "←"),
    ]

    for entity, char in replacements:
        content = content.replace(entity, char)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully cleaned entity encoding leaks in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Replace escaped HTML entities with UTF-8 characters in Module 01 JS\n\n"
            "Convert &mu;, &times;, &check;, and &rarr; entity strings in stepper\n"
            "data objects to native Unicode to prevent literal display in SVG text."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_entity_leaks()
