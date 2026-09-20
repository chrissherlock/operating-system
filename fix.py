#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix next link in 02-hardware-review.html navigation bar
# =====================================================================
import os
import subprocess

def fix_hardware_review_nav_bar():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    week_title = "Week 1: Operating System Concepts"
    pill_template = '<a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: all 0.15s ease;">'
    home_pill = f'{pill_template}&#127968; {week_title}</a>'

    correct_nav = f'''<nav class="module-nav-bar">    <a href="01-what-is-an-os-and-history.html" class="module-nav-btn">&larr; Previous: 01. What Is an OS &amp; History</a>    {home_pill}    <a href="03-os-concepts.html" class="module-nav-btn">Next: 03. OS Concepts &rarr;</a>  </nav>'''

    # Replace existing malformed nav bar
    if '<nav class="module-nav-bar">' in content:
        # Find start and end of nav tag
        start_idx = content.find('<nav class="module-nav-bar">')
        end_idx = content.find('</nav>', start_idx) + 6
        content = content[:start_idx] + correct_nav + content[end_idx:]
    else:
        print("--> <nav class=\"module-nav-bar\"> not found.")
        return

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully updated navigation bar in {file_path}")

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Fix navigation next link in week01/02-hardware-review.html\n\n"
            "Update the navigation bar in 02-hardware-review.html so the right-hand button\n"
            "points to 03-os-concepts.html instead of duplicate index.html links."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for 02-hardware-review.html!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_hardware_review_nav_bar()
