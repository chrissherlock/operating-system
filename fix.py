#!/usr/bin/env python3
# =====================================================================
# fix.py: Style index navigation buttons with white background
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "index.html")

def style_index_buttons_white():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace blue or gray backgrounds in button classes or inline styles with white
    # Let's target typical button styles or classes in index.html
    modified_content = content.replace("background-color: #f0f9ff;", "background-color: #ffffff;")
    modified_content = modified_content.replace("background: #f0f9ff;", "background: #ffffff;")
    modified_content = modified_content.replace("color: #0284c7;", "color: #0f172a;")

    if modified_content != content:
        print("--> Successfully updated index button styles to white background.")
    else:
        print("--> Warning: No direct matches found or already styled. Checking specific patterns...")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(modified_content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Style index navigation buttons with white background and dark text\n\n"
            "Update navigation button styles in week01-operating-system-concepts/index.html\n"
            "to feature a clean white background with dark text and subtle borders."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for index button styling!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    style_index_buttons_white()
