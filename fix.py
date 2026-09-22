#!/usr/bin/env python3
# =====================================================================
# fix.py: Add introductory paragraph to 02-hardware-review.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)

INTRO_PARAGRAPH = """    <article class="module-body">
      <p>
        An operating system does not exist in an abstract mathematical vacuum; it is fundamentally shaped and constrained by the physical silicon it commands. At its core, the OS acts as both a resource manager and an extended virtual machine, turning raw hardware into a safe, programmable execution environment. However, software alone cannot enforce memory protection boundaries or wrest control back from an errant program—it requires direct hardware cooperation through privileged CPU execution modes, timer interrupts, Memory Management Units (MMUs), and DMA controllers. Understanding these physical hardware building blocks is the indispensable foundation for studying how operating systems virtualize the CPU and memory, coordinate concurrent threads, and persist data to non-volatile storage.
      </p>"""

def insert_intro_paragraph():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    target_tag = '<article class="module-body">'
    if target_tag not in content:
        print(f"Error: Could not locate '{target_tag}' in {TARGET_FILE}.")
        return

    # Check if intro text is already present
    if "An operating system does not exist in an abstract mathematical vacuum" in content:
        print("Notice: Introductory paragraph already present.")
        return

    # Replace the opening <article class="module-body"> with tag + intro paragraph
    updated_content = content.replace(target_tag, INTRO_PARAGRAPH, 1)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully added introductory paragraph to {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add introductory conceptual paragraph to Module 2 hardware review\n\n"
            "Insert an architectural introductory paragraph at the top of the body\n"
            "in 02-hardware-review.html framing physical hardware mechanisms as the\n"
            "substrate for operating system virtualization, protection, and I/O."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    insert_intro_paragraph()
