#!/usr/bin/env python3
# =====================================================================
# fix.py: Update forward navigation labels in Week 6 Hub
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week06-synchronization-and-deadlock",
    "index.html"
)

def update_week6_nav_label():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace variations of Week 9 Hub label with full descriptive title
    old_labels = [
        '<a href="../week09-memory-management/index.html" class="nav-btn">Week 9 Hub &rarr;</a>',
        '<a href="../week09-memory-management/index.html" class="nav-btn">Week 9 Hub →</a>'
    ]

    target_replacement = '<a href="../week09-memory-management/index.html" class="nav-btn">Week 9: Memory Management &rarr;</a>'

    updated = False
    for old in old_labels:
        if old in content:
            content = content.replace(old, target_replacement)
            updated = True

    if not updated:
        # Fallback regex-style string search if spacing varied
        import re
        pattern = r'<a\s+href="\.\./week09-memory-management/index\.html"\s+class="nav-btn">[^<]*</a>'
        new_content = re.sub(pattern, target_replacement, content)
        if new_content != content:
            content = new_content
            updated = True

    if not updated:
        print("Notice: No matching 'Week 9 Hub' nav buttons found to replace.")
        return True

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully updated navigation labels in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if update_week6_nav_label():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Align Week 6 hub navigation label to Week 9 Memory Management\n\n"
                "Update next-navigation buttons in top and bottom nav bars to display\n"
                "Week 9: Memory Management instead of generic hub wording."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
