#!/usr/bin/env python3
# =====================================================================
# fix.py: Update heading and navigation bar in 04-os-structure.html
# =====================================================================
import os
import re
import subprocess

def update_os_structure_module():
    file_path = os.path.join("week01-operating-system-concepts", "04-os-structure.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    week_title = "Week 1: Operating System Concepts"
    pill_template = '<a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: all 0.15s ease;">'
    home_pill = f'{pill_template}&#127968; {week_title}</a>'

    # Standardized navigation bar for Module 4
    correct_nav = f'''<nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #cbd5e1;">
    <a href="03-os-concepts.html" class="module-nav-btn">&larr; Previous: 03. OS Concepts</a>
    {home_pill}
    <div></div>
  </nav>'''

    new_content = content

    # 1. Ensure heading reads "4. Operating System Structure" or similar
    heading_pattern = r'<h2>\s*(?:\d+\.\s*)?([^<]+)(</h2>)'
    if re.search(heading_pattern, new_content):
        new_content = re.sub(heading_pattern, r'<h2>4. Operating System Structure\2', new_content, count=1)

    # 2. Update navigation bar
    if '<nav class="module-nav-bar">' in new_content:
        start_idx = new_content.find('<nav class="module-nav-bar">')
        end_idx = new_content.find('</nav>', start_idx) + 6
        new_content = new_content[:start_idx] + correct_nav + new_content[end_idx:]
    else:
        # Prepend after body if no nav bar exists
        body_match = re.search(r'(<body[^>]*>)', new_content, flags=re.IGNORECASE)
        if body_match:
            new_content = new_content.replace(body_match.group(1), f'{body_match.group(1)}\n  {correct_nav}')

    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"--> Successfully updated {file_path}")

        try:
            subprocess.run(["git", "add", "fix.py", file_path], check=True)
            commit_msg = (
                "Update heading and navigation bar in week01/04-os-structure.html\n\n"
                "Ensure Module 4 has correct section numbering (4) and features the unified\n"
                "home symbol pill button linking back to the week index."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully for 04-os-structure.html!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> 04-os-structure.html is already up to date.")

if __name__ == "__main__":
    update_os_structure_module()
