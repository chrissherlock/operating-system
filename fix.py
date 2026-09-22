#!/usr/bin/env python3
# =====================================================================
# fix.py: Normalize paragraph and heading vertical spacing in modules
# =====================================================================
import os
import re
import subprocess

TARGET_FILES = [
    os.path.join("week01-operating-system-concepts", "01-what-is-an-os-and-history.html"),
    os.path.join("week01-operating-system-concepts", "02-hardware-review.html"),
    os.path.join("week01-operating-system-concepts", "03-os-concepts.html"),
    os.path.join("week01-operating-system-concepts", "04-os-structure.html"),
]

def adjust_spacing_rules(file_path):
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}: file not found.")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # 1. Neutralize flex-direction column gap in article.module-body if present
    content = re.sub(
        r"article\.module-body\s*\{[^}]*\}",
        "article.module-body {\n      display: block;\n    }",
        content
    )

    # 2. Adjust h2 margin-top (reduce from 36px to 28px)
    content = re.sub(r"h2\s*\{([^}]*?)margin-top:\s*36px;", r"h2 {\1margin-top: 28px;", content)

    # 3. Adjust h3 margin-top (reduce from 24px/28px to 20px)
    content = re.sub(r"h3\s*\{([^}]*?)margin-top:\s*(?:24px|28px);", r"h3 {\1margin-top: 20px;", content)

    # 4. Adjust h4 margin-top if present
    content = re.sub(r"h4\s*\{([^}]*?)margin-top:\s*20px;", r"h4 {\1margin-top: 16px;", content)

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"--> Successfully tightened spacing in {file_path}")
        return True
    else:
        print(f"--> No spacing changes needed in {file_path}")
        return False

def run_spacing_update():
    modified = []
    for file_path in TARGET_FILES:
        if adjust_spacing_rules(file_path):
            modified.append(file_path)

    if modified:
        try:
            subprocess.run(["git", "add", "fix.py"] + modified, check=True)
            commit_msg = (
                "Normalize paragraph and heading vertical spacing across Week 1 modules\n\n"
                "Remove flex column gaps on article containers to restore standard CSS\n"
                "margin collapsing and reduce excessive margin-top on h2, h3, and h4 tags."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git execution note: {e}")

if __name__ == "__main__":
    run_spacing_update()
