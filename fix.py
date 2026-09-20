#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix navigation header in 02-hardware-review.html
# =====================================================================
import os
import re
import subprocess

def fix_hardware_review_page():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    week_title = "Week 1: Operating System Concepts"
    pill_template = '<a href="index.html" style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155; text-decoration: none; font-weight: 600; font-size: 0.85rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: all 0.15s ease;">'
    styled_link = f'{pill_template}&#127968; {week_title}</a>'

    updated = False
    new_content = content

    # 1. Search for existing nav block
    nav_match = re.search(r'(<nav[^>]*>)(.*?)(</nav>)', new_content, flags=re.DOTALL | re.IGNORECASE)
    if nav_match:
        nav_open, nav_body, nav_close = nav_match.groups()
        print(f"--> Found <nav> block in {file_path}.")

        # Check for previous/next pagination buttons within nav
        btn_match = re.findall(r'(<a[^>]*class="[^"]*nav-btn[^"]*"[^>]*>.*?</a>)', nav_body, flags=re.DOTALL | re.IGNORECASE)
        if len(btn_match) >= 1:
            prev_btn = btn_match[0] if "larr" in btn_match[0] or "Prev" in btn_match[0] or "01" in btn_match[0] else ""
            next_btn = btn_match[1] if len(btn_match) > 1 else (btn_match[0] if btn_match[0] != prev_btn else "")

            new_nav_body = f'\n    {prev_btn}\n    {styled_link}\n    {next_btn}\n  '
            new_content = new_content.replace(nav_match.group(0), f'{nav_open}{new_nav_body}{nav_close}')
            updated = True
        else:
            new_content = new_content.replace(nav_match.group(0), f'{nav_open}\n    {styled_link}\n  {nav_close}')
            updated = True
    else:
        # Fallback: search for header tag
        header_match = re.search(r'(<header[^>]*>)(.*?)(</header>)', new_content, flags=re.DOTALL | re.IGNORECASE)
        if header_match:
            h_open, h_body, h_close = header_match.groups()
            new_content = new_content.replace(header_match.group(0), f'{h_open}\n    {styled_link}\n  {h_close}')
            updated = True
        else:
            # Last resort: prepend right after body tag opening
            body_match = re.search(r'(<body[^>]*>)', new_content, flags=re.IGNORECASE)
            if body_match:
                new_content = new_content.replace(body_match.group(1), f'{body_match.group(1)}\n  <nav style="display: flex; justify-content: space-between; align-items: center; padding: 16px 24px; background: #f8fafc; border-bottom: 1px solid #cbd5e1;">\n    <div></div>\n    {styled_link}\n    <div></div>\n  </nav>')
                updated = True

    if updated:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"--> Successfully injected home pill navigation header into {file_path}")

        try:
            subprocess.run(["git", "add", "fix.py", file_path], check=True)
            commit_msg = (
                "Fix navigation header in week01/02-hardware-review.html\n\n"
                "Target 02-hardware-review.html specifically and inject the styled\n"
                "home symbol pill button linking back to index.html."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully for 02-hardware-review.html!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> Error: Could not find any structural nav/header container in 02-hardware-review.html.")

if __name__ == "__main__":
    fix_hardware_review_page()
