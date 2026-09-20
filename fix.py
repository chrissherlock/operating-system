#!/usr/bin/env python3
import os
import re
import subprocess
import sys

def modify_aging_file():
    path = os.path.join("week09-memory-management", "08-aging-algorithm.html")
    if not os.path.exists(path):
        print(f"Error: Could not find {path}", file=sys.stderr)
        return False

    print(f"--> Reading {path}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex targeting the exact snippet identified by inspection
    pattern = r"ticks ago and 4 ticks ago\.\s*A value of `00000001`\s*\(1 decimal\)\s*means it was only referenced 1 tick ago\."
    replacement = "ticks ago and 4 ticks ago. A value of `10000000` (128 decimal) indicates a reference at the most recent interval (shifted into the MSB), while `00000001` (1 decimal) indicates a reference at the oldest tracked interval."

    new_content, count = re.subn(pattern, replacement, content)
    if count == 0:
        print("Warning: Aging snippet pattern did not match.", file=sys.stderr)
        return False

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"--> Updated aging bit interpretation in {path} ({count} replacement).")
    return True

def modify_emat_file():
    path = os.path.join("week09-memory-management", "02b-paging-hardware-dilemma.html")
    if not os.path.exists(path):
        print(f"Error: Could not find {path}", file=sys.stderr)
        return False

    print(f"--> Reading {path}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex targeting the LaTeX display equation identified by inspection
    pattern = r"\$\$EAT\s*=\s*\(h\s*\\times\s*t_\{tlb\}\)\s*\+\s*\(1\s*-\s*h\)\s*\\times\s*\(t_\{tlb\}\s*\+\s*t_\{ram\\_table\}\s*\+\s*t_\{ram\\_data\}\)\$\$"
    replacement = r"$$EAT = h \times (t_{tlb} + t_{ram\_data}) + (1 - h) \times (t_{tlb} + t_{ram\_table} + t_{ram\_data})$$"

    new_content, count = re.subn(pattern, replacement, content)
    if count == 0:
        # Fallback to a broader regex match on the EAT formula line
        broad_pattern = r"\$\$EAT\s*=.*?t_\{ram\\_data\}\)\$\$"
        new_content, count = re.subn(broad_pattern, replacement, content)

    if count == 0:
        print("Warning: EAT LaTeX formula pattern did not match.", file=sys.stderr)
        return False

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"--> Updated EAT equation in {path} ({count} replacement).")
    return True

def run_git_deployment():
    aging_path = os.path.join("week09-memory-management", "08-aging-algorithm.html")
    emat_path = os.path.join("week09-memory-management", "02b-paging-hardware-dilemma.html")

    print("--> Staging modified HTML files...")
    subprocess.run(["git", "add", aging_path, emat_path], check=True)

    status_res = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if status_res.returncode == 0:
        print("--> No staged changes detected. Exiting without commit.")
        return

    print("--> Committing changes...")
    commit_msg = (
        "Fix aging bit interpretation and EAT hit latency equation in week 9\n\n"
        "Update 08-aging-algorithm.html so MSB indicates the most recent tick,\n"
        "and update the EAT formula in 02b-paging-hardware-dilemma.html to include\n"
        "data access latency on a TLB hit."
    )

    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("--> Changes committed and pushed successfully!")

if __name__ == "__main__":
    ok_aging = modify_aging_file()
    ok_emat = modify_emat_file()
    if ok_aging or ok_emat:
        run_git_deployment()
    else:
        print("--> No modifications applied. Aborting git operations.", file=sys.stderr)
        sys.exit(1)
