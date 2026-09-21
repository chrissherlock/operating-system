#!/usr/bin/env python3
# =====================================================================
# fix.py: Neutralize navigation button palette in 01-what-is-an-os-and-history.html
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "01-what-is-an-os-and-history.html")

def update_navigation_button_colors():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update CSS rules using exact group indexing (\g<2>) to avoid ambiguous \21 digit parsing
    old_css_pattern = r'(\.module-nav-btn\s*\{[^}]*background-color:\s*)[^;]+(;[^}]*border:\s*)[^;]+(;[^}]*color:\s*)[^;]+;'
    new_css = r'\g<1>#ffffff\g<2>1px solid #cbd5e1\g<3>#334155;'
    content = re.sub(old_css_pattern, new_css, content)

    old_hover_pattern = r'(\.module-nav-btn:hover\s*\{[^}]*background-color:\s*)[^;]+(;[^}]*color:\s*)[^;]+;'
    new_hover = r'\g<1>#f1f5f9\g<2>#0f172a; border-color: #94a3b8;'
    content = re.sub(old_hover_pattern, new_hover, content)

    # 2. Build clean, neutral navigation elements
    pill_style = (
        'display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; '
        'background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; '
        'color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem; '
        'box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: all 0.15s ease;'
    )

    next_btn_style = (
        'display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; '
        'background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; '
        'color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem; '
        'box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: all 0.15s ease;'
    )

    week_title = "Week 1: Operating System Concepts"
    home_pill = f'<a href="index.html" style="{pill_style}">&#127968; {week_title}</a>'
    next_btn = f'<a href="02-hardware-review.html" style="{next_btn_style}">Next: 02. Hardware Review &rarr;</a>'

    top_nav = f'''<nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1100px; margin: 0 auto 16px auto;">
    <div style="visibility: hidden; flex: 1; text-align: left;">&larr; Placeholder</div>
    <div style="flex: 1; text-align: center;">
      {home_pill}
    </div>
    <div style="flex: 1; text-align: right;">
      {next_btn}
    </div>
  </nav>'''

    bottom_nav = f'''<nav class="module-nav-bar bottom" style="display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1100px; margin: 24px auto 24px auto;">
    <div style="visibility: hidden; flex: 1; text-align: left;">&larr; Placeholder</div>
    <div style="flex: 1; text-align: center;">
      {home_pill}
    </div>
    <div style="flex: 1; text-align: right;">
      {next_btn}
    </div>
  </nav>'''

    # 3. Replace navigation bars cleanly
    content = re.sub(r'<nav\s+class=["\']module-nav-bar["\'][^>]*>.*?</nav>', top_nav, content, flags=re.DOTALL)
    content = re.sub(r'<nav\s+class=["\']module-nav-bar\s+bottom["\'][^>]*>.*?</nav>', bottom_nav, content, flags=re.DOTALL)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully neutralized navigation buttons in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix regex backreference error and neutralize navigation button styling\n\n"
            "Avoid ambiguous \\21 backreference syntax when updating CSS rules for\n"
            "navigation buttons in week01/01-what-is-an-os-and-history.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_navigation_button_colors()
