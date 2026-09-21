#!/usr/bin/env python3
# =====================================================================
# fix.py: Center home navigation button in 01-what-is-an-os-and-history.html
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "01-what-is-an-os-and-history.html")

def align_home_button_center():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    week_title = "Week 1: Operating System Concepts"
    pill_style = (
        'display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; '
        'background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; '
        'color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem; '
        'box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: all 0.15s ease;'
    )
    home_pill = f'<a href="index.html" style="{pill_style}">&#127968; {week_title}</a>'
    next_btn = '<a href="02-hardware-review.html" class="module-nav-btn">Next: 02. Hardware Review &rarr;</a>'

    # Top nav bar (balanced 3-element flex container)
    top_nav = f'''<nav class="module-nav-bar" style="display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1100px; margin: 0 auto 16px auto;">
    <div style="visibility: hidden; flex: 1; text-align: left;">&larr; Placeholder</div>
    <div style="flex: 1; text-align: center;">
      {home_pill}
    </div>
    <div style="flex: 1; text-align: right;">
      {next_btn}
    </div>
  </nav>'''

    # Bottom nav bar (balanced 3-element flex container)
    bottom_nav = f'''<nav class="module-nav-bar bottom" style="display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1100px; margin: 24px auto 24px auto;">
    <div style="visibility: hidden; flex: 1; text-align: left;">&larr; Placeholder</div>
    <div style="flex: 1; text-align: center;">
      {home_pill}
    </div>
    <div style="flex: 1; text-align: right;">
      {next_btn}
    </div>
  </nav>'''

    new_content = content

    # Replace top nav if present, else prepend right after <body>
    top_nav_pattern = r'<nav\s+class=["\']module-nav-bar["\'][^>]*>.*?</nav>'
    match_top = re.search(top_nav_pattern, new_content, flags=re.DOTALL)
    if match_top:
        new_content = new_content[:match_top.start()] + top_nav + new_content[match_top.end():]
    else:
        body_match = re.search(r'(<body[^>]*>)', new_content, flags=re.IGNORECASE)
        if body_match:
            new_content = new_content.replace(body_match.group(1), f'{body_match.group(1)}\n  {top_nav}')

    # Replace bottom nav if present, else append right before </body>
    bottom_nav_pattern = r'<nav\s+class=["\']module-nav-bar\s+bottom["\'][^>]*>.*?</nav>'
    match_bottom = re.search(bottom_nav_pattern, new_content, flags=re.DOTALL)
    if match_bottom:
        new_content = new_content[:match_bottom.start()] + bottom_nav + new_content[match_bottom.end():]
    else:
        close_body_idx = new_content.rfind('</body>')
        if close_body_idx != -1:
            new_content = new_content[:close_body_idx] + f'  {bottom_nav}\n' + new_content[close_body_idx:]

    if new_content != content:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"--> Centered home navigation button in {TARGET_FILE}")

        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Center home navigation button in week01/01-what-is-an-os-and-history.html\n\n"
                "Update top and bottom navigation bars in 01-what-is-an-os-and-history.html\n"
                "to place the home pill button in the center using a balanced flex layout."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully for 01-what-is-an-os-and-history.html!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> Navigation bar in 01-what-is-an-os-and-history.html is already up to date.")

if __name__ == "__main__":
    align_home_button_center()
