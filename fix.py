#!/usr/bin/env python3
# =====================================================================
# fix.py: Expand PML4 definition to define Page Map Level in glossary
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def update_pml4_definition():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Old PML4 definition text block
    old_pml4_block = """            <div>
              <strong style="color: #0284c7; font-family: var(--font-mono);">PML4 Table</strong>
              <div style="color: #64748b; margin-top: 2px;">Top-level 4 KiB table in x86-64 4-level paging containing entries pointing to PDPTs.</div>
            </div>"""

    # Updated PML4 definition text block explicitly defining Page Map Level
    new_pml4_block = """            <div>
              <strong style="color: #0284c7; font-family: var(--font-mono);">PML4 Table</strong>
              <div style="color: #64748b; margin-top: 2px;">Top-level 4 KiB table in x86-64 4-level paging (where <strong>PML</strong> stands for <em>Page Map Level</em>) containing entries pointing to PDPTs.</div>
            </div>"""

    if old_pml4_block in content:
        content = content.replace(old_pml4_block, new_pml4_block)
        print("--> Updated PML4 definition with Page Map Level expansion.")
    else:
        print("--> Warning: Exact PML4 definition block pattern not matched.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand PML4 definition to define Page Map Level in glossary\n\n"
            "Update the PML4 terminology card within 02-hardware-review.html to explicitly\n"
            "define that PML stands for Page Map Level."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for PML4 expansion!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_pml4_definition()
