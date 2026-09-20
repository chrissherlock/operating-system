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
        if 'href="02-hardware-review.html"' in content:
            print(f'--> Verification passed: {module_path} points to 02-hardware-review.html.')
        else:
            print(f'--> Warning: {module_path} does not point to 02-hardware-review.html.')
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

            commit_msg = (
                'Update navigation link to 02-hardware-review.html and run fix.py\n\n'
                'Ensure Module 1 history page points to 02-hardware-review.html in the bottom navigation bar\n'
                'and complete verification checks via fix.py.'
            )

            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            print('--> Git sync completed successfully via fix.py!')
    except Exception as e:
        print(f'Error during git execution: {e}')

if __name__ == '__main__':
    verify_and_sync()
