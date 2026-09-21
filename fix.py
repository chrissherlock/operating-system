#!/usr/bin/env python3
# =====================================================================
# fix.py: Add IPC definition to glossary and walkthrough text
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

IPC_GLOSSARY_CARD = """            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 8px 12px; border-radius: 0 4px 4px 0;">
              <strong style="color: #0369a1;">Instructions Per Cycle (IPC)</strong>
              <p style="margin: 4px 0 0 0; color: #475569;">
                The average number of instructions completed (retired) on every clock tick. A single pipeline can finish at most 1 instruction per tick (the 1.0 IPC ceiling). Superscalar cores run parallel pipelines side-by-side to complete 2 or more instructions simultaneously (IPC &gt; 1.0).
              </p>
            </div>"""

def update_ipc_explanations():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update the Superscalar Cycle 1 "why" explanation in JavaScript
    old_superscalar_why = (
        'why: "A single pipeline is bound by the theoretical ceiling of 1.0 IPC. '
        'Superscalar designs duplicate execution paths to fetch, decode, and issue multiple '
        'instructions per cycle, achieving IPC &gt; 1.0."'
    )

    new_superscalar_why = (
        'why: "<strong>What is IPC?</strong> <em>Instructions Per Cycle</em> measures how many instructions '
        'the CPU finishes on each clock tick. A standard single pipeline is like a single assembly line: '
        'even when completely full, it can only pop out at most 1 finished instruction per tick (the 1.0 IPC ceiling). '
        'Superscalar processors build parallel pipelines side-by-side, allowing the core to fetch, execute, and retire '
        '2 or more instructions on the exact same tick (achieving IPC &gt; 1.0)."'
    )

    content = content.replace(old_superscalar_why, new_superscalar_why)

    # 2. Add IPC card to the Hardware Glossary grid
    if 'Instructions Per Cycle (IPC)' not in content:
        # Insert right after the opening grid div in the glossary
        glossary_grid_marker = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; font-size: 0.84rem; color: #334155; line-height: 1.5;">'
        if glossary_grid_marker in content:
            content = content.replace(
                glossary_grid_marker,
                glossary_grid_marker + "\n" + IPC_GLOSSARY_CARD
            )
            print("--> Added IPC definition card to Hardware Glossary.")
        else:
            print("--> Warning: Glossary grid marker not matched.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Updated IPC explanations in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add IPC definition to Module 2 glossary and superscalar narrative\n\n"
            "Define Instructions Per Cycle (IPC) in the silicon glossary and clarify\n"
            "the 1.0 IPC ceiling in the superscalar walkthrough in 02-hardware-review."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_ipc_explanations()
