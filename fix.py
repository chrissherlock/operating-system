#!/usr/bin/env python3
# =====================================================================
# fix.py: Style module navigation buttons with white background
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def style_nav_buttons_white():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Old navigation button styling block
    old_nav_css = """    .module-nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      font-family: var(--font-mono);
      text-decoration: none;
      color: #0284c7;
      background-color: #f0f9ff;
      border: 1px solid #bae6fd;
      padding: 6px 12px;
      border-radius: 6px;
      transition: all 0.15s ease;
    }
    .module-nav-btn:hover {
      background-color: #f1f5f9;
      color: #0f172a; border-color: #94a3b8;
    }"""

    # New navigation button styling with white background and dark/accent text
    new_nav_css = """    .module-nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      font-family: var(--font-mono);
      text-decoration: none;
      color: #0f172a;
      background-color: #ffffff;
      border: 1px solid #cbd5e1;
      padding: 6px 12px;
      border-radius: 6px;
      transition: all 0.15s ease;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }
    .module-nav-btn:hover {
      background-color: #f8fafc;
      color: #0284c7;
      border-color: #0284c7;
    }"""

    if old_nav_css in content:
        content = content.replace(old_nav_css, new_nav_css)
        print("--> Successfully updated .module-nav-btn styles to white background.")
    else:
        print("--> Warning: Exact navigation CSS block not matched. Searching for individual rules...")
        # Fallback if minor differences exist
        if "background-color: #f0f9ff;" in content:
            content = content.replace("background-color: #f0f9ff;", "background-color: #ffffff;")
        if "color: #0284c7;" in content and ".module-nav-btn {" in content:
            # Replace nav button text color specifically
            content = content.replace(".module-nav-btn {\n      display: inline-flex;", ".module-nav-btn {\n      display: inline-flex;\n      color: #0f172a;")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Style module navigation buttons with white background and dark text\n\n"
            "Update the .module-nav-btn class styling in 02-hardware-review.html\n"
            "so navigation buttons feature a clean white background with dark text."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for navigation button styling!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    style_nav_buttons_white()
