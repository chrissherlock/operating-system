#!/usr/bin/env python3
# =====================================================================
# fix.py: Maintenance, verification, and git synchronization script
# =====================================================================
import os
import subprocess

def verify_and_sync():
    module_path = os.path.join('week01-operating-system-concepts', '01-what-is-an-os-and-history.html')
    if os.path.exists(module_path):
        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()

        top_nav_pattern = '<div class="nav-back">'
        if top_nav_pattern in content and '02-hardware-review.html' not in content[:content.find('</header>')]:
            new_top_nav = (
                '<div class="nav-back" style="display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1100px; margin: 0 auto;">\n'
                '    <a href="index.html">&larr; Back to Chapter 1 Index</a>\n'
                '    <a href="02-hardware-review.html" style="display: inline-flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600; font-family: var(--font-mono); text-decoration: none; color: #0284c7; background-color: #f0f9ff; border: 1px solid #bae6fd; padding: 6px 12px; border-radius: 6px;">Next Article: 02. Computer Hardware Review &rarr;</a>\n'
                '  </div>'
            )
            start_nav = content.find('<div class="nav-back">')
            end_nav = content.find('</div>', start_nav) + 6
            content = content[:start_nav] + new_top_nav + content[end_nav:]
            print("--> Added top navigation next article link.")

        if 'href="02-hardware-review.html"' in content:
            print(f'--> Verification passed: {module_path} contains the next article link.')
        else:
            print(f'--> Warning: {module_path} missing next article link.')

        with open(module_path, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print(f'--> Warning: {module_path} missing.')

    potential_files = [
        'fix.py',
        'week01-operating-system-concepts/01-what-is-an-os-and-history.html'
    ]
    files_to_stage = [f for f in potential_files if os.path.exists(f)]
    print(f'--> Staging files: {files_to_stage}')

    try:
        if files_to_stage:
            subprocess.run(['git', 'add'] + files_to_stage, check=True)
            commit_msg = "Add top and bottom navigation links to next module in 01-what-is-an-os-and-history.html"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            print('--> Git sync completed successfully via fix.py!')
    except Exception as e:
        print(f'Error during git execution: {e}')

if __name__ == '__main__':
    verify_and_sync()
