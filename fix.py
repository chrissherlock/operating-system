#!/usr/bin/env python3
# =====================================================================
# fix.py: Force injection of home pill link into 01-what-is-an-os-and-history.html
# =====================================================================
import os
import re
import subprocess

def force_fix_history_page():
    file_path = os.path.join("week01-operating-system-concepts", "01-what-is-an-os-and-history.html")
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

    # 1. Search for any existing nav or header tag
    nav_match = re.search(r'(<nav[^>]*>)(.*?)(</nav>)', new_content, flags=re.DOTALL | re.IGNORECASE)
    if nav_match:
        nav_open, nav_body, nav_close = nav_match.groups()
        # If there's already an anchor or span inside, let's replace the middle contents or wrap it
        # Let's see if we can find a span or div or just replace the inner body of nav with [Prev] [Home Pill] [Next]
        # Or let's target any existing center element in nav
        print(f"--> Found <nav> block in {file_path}.")

        # Check if previous/next buttons are present
        btn_match = re.findall(r'(<a[^>]*class="[^"]*nav-btn[^"]*"[^>]*>.*?</a>)', nav_body, flags=re.DOTALL | re.IGNORECASE)
        if len(btn_match) >= 1:
            # Construct a clean standardized nav bar with Previous, Home Pill, and Next
            # Let's extract prev and next buttons if possible
            prev_btn = btn_match[0] if "larr" in btn_match[0] or "Prev" in btn_match[0] or "03" in btn_match[0] else ""
            next_btn = btn_match[1] if len(btn_match) > 1 else (btn_match[0] if btn_match[0] != prev_btn else "")

            # If we couldn't reliably distinguish, let's just replace the center text/span between buttons
            new_nav_body = f'\n    {prev_btn}\n    {styled_link}\n    {next_btn}\n  '
            new_content = new_content.replace(nav_match.group(0), f'{nav_open}{new_nav_body}{nav_close}')
            updated = True
        else:
            # Just inject styled link into nav
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
                "Fix navigation header in week01/01-what-is-an-os-and-history.html\n\n"
                "Locate navigation container in 01-what-is-an-os-and-history.html and "
                "force-inject the styled home symbol pill button linking to index.html."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully for 01-what-is-an-os-and-history.html!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> Error: Could not find any structural nav/header container in 01-what-is-an-os-and-history.html.")

if __name__ == "__main__":
    force_fix_history_page()
