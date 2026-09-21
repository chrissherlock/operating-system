#!/usr/bin/env python3
# =====================================================================
# fix.py: Align navigation font-family with Module 3 styling
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def align_nav_font():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # In 02-hardware-review.html, .module-nav-btn was explicitly styled with:
    #   font-family: var(--font-mono);
    # In 03-os-concepts.html, it inherits the body sans-serif font family.
    old_nav_css = """    .module-nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #334155;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.85rem;
      font-family: var(--font-mono);
      transition: all 0.15s ease;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }"""

    new_nav_css = """    .module-nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #334155;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.85rem;
      font-family: var(--font-sans);
      transition: all 0.15s ease;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }"""

    if old_nav_css in content:
        content = content.replace(old_nav_css, new_nav_css)
        print("--> Successfully updated .module-nav-btn to use var(--font-sans).")
    else:
        # Fallback inline replacement if formatting has slight spacing differences
        content = content.replace("font-family: var(--font-mono);", "font-family: var(--font-sans);", 1)
        print("--> Replaced first occurrence of mono font in navigation CSS.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Unify font family across navigation elements in Module 2\n\n"
            "Update .module-nav-btn font-family in 02-hardware-review.html to use the\n"
            "primary sans-serif font stack, matching Module 3's navigation styling."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for navigation font consistency!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    align_nav_font()
