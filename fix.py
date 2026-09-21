#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix python string syntax error and apply definitions
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_syntax_and_apply():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Cleanly update step 1 mechanics with properly escaped/structured quotes
    old_step1_what = 'what: "The MMU reads the root page table physical address <code>0x1A4000</code> from control register <strong>CR3</strong>. It indexes into the PML4 table, locating entry 2 which points to the PDPT table at <code>0x2B100</code>."'

    new_step1_what = (
        'what: "The MMU reads the root page table physical address <code>0x1A4000</code> '
        'from control register <strong>CR3</strong>. <em>Definition: CR3 is the processor '
        'root register storing the physical base address of the current process top-level '
        'page table (PML4).</em> It indexes into the top-level <strong>PML4 (Page Map Level 4)</strong> '
        'table (containing 512 entries pointing to PDPTs), locating entry 2 which points to the '
        'PDPT table at <code>0x2B100</code>."'
    )

    if old_step1_what in content:
        content = content.replace(old_step1_what, new_step1_what)
        print("--> Updated Step 1 mechanics with clean string literal.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix python string literal syntax error in fix.py\n\n"
            "Use clean string literal structure for the process description\n"
            "within the translation simulator mechanics update in fix.py."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for syntax fix!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_syntax_and_apply()
