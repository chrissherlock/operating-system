#!/usr/bin/env python3
# =====================================================================
# add_next_article_nav.py: Add next article navigation footer
# =====================================================================
import os
import subprocess

def execute_nav_addition():
    file_path = os.path.join("week01-operating-system-concepts", "01-what-is-an-os-and-history.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    target_str = "</main>"
    pos = content.find(target_str)
    if pos != -1:
        nav_footer = """
    <div style="display: flex; justify-content: flex-end; margin-top: 10px; margin-bottom: 20px;">
      <a href="02-computer-hardware-review.html" style="display: inline-flex; align-items: center; gap: 6px; font-size: 0.88rem; font-weight: 600; font-family: var(--font-mono); text-decoration: none; color: #0284c7; background-color: #f0f9ff; border: 1px solid #bae6fd; padding: 8px 14px; border-radius: 6px;">
        Next Article: 02. Computer Hardware Review &rarr;
      </a>
    </div>
"""
        content = content[:pos] + nav_footer + content[pos:]
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("--> Next article navigation successfully added.")

    try:
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", "Add navigation link pointing to 02. Computer Hardware Review in Module 1"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git note: {e}")

if __name__ == "__main__":
    execute_nav_addition()
