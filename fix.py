#!/usr/bin/env python3
# =====================================================================
# fix.py: Add introductory paragraph to 01-what-is-an-os-and-history.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "01-what-is-an-os-and-history.html"
)

INTRO_PARAGRAPH = """    <article class="module-body">
      <p>
        A computer without software is little more than a collection of silicon gates, metal traces, and magnetic or solid-state cells incapable of meaningful work on its own. While user applications perform specific end-user tasks—compiling code, serving web traffic, or rendering graphics—they cannot safely or conveniently manipulate bare physical hardware directly. The <strong>operating system</strong> is the foundational system software that bridges this divide. Sitting directly between application programs and underlying physical hardware, the OS provides clean, uniform abstractions while arbitrating scarce hardware resources across multiple competing tasks. Tracing how operating systems evolved from early operator-driven batch pipelines into modern preemptive, networked kernels reveals the core engineering trade-offs that govern all computing systems today.
      </p>"""

def insert_module_one_intro():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    target_tag = '<article class="module-body">'
    if target_tag not in content:
        print(f"Error: Could not locate '{target_tag}' in {TARGET_FILE}.")
        return

    # Check if intro text already exists
    if "A computer without software is little more than a collection of silicon gates" in content:
        print("Notice: Introductory paragraph already present in Module 1.")
        return

    # Replace the opening <article class="module-body"> with tag + intro paragraph
    updated_content = content.replace(target_tag, INTRO_PARAGRAPH, 1)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully added introductory paragraph to {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add introductory conceptual paragraph to Module 1 overview\n\n"
            "Insert a foundational introductory paragraph at the start of the body\n"
            "in 01-what-is-an-os-and-history.html to motivate the role of operating\n"
            "systems before examining core paradigms and computing generations."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    insert_module_one_intro()
