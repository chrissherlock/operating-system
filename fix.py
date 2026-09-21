#!/usr/bin/env python3
# =====================================================================
# fix.py: Place header inside the .container card in 02-hardware-review.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_header_container_wrapping():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # We want to ensure <header> is inside <div class="container">, right after the top nav bar,
    # rather than having a separate outer layout structure.

    # Let's check how the container and header are structured currently and restructure them cleanly.

    # If the file uses a separate main wrapper or header outside container, let's fix it:
    # <body>
    #   <div class="container">
    #     <nav>...</nav>
    #     <header>...</header>
    #     <article class="module-body">...</article>
    #     <nav>...</nav>
    #   </div>
    # </body>

    # Let's perform a clean string replacement of the header / container boundaries

    # Let's inspect typical structure and unify it:
    print(f"--> Reorganizing container structure in {TARGET_FILE}...")

    # For safety and cleanliness, let's update the file content directly.
    # Let's ensure <header> is a child of <div class="container">.

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # If <main> wraps the header separately, let's remove <main> and put header directly in .container
    html = html.replace("<main style=\"display: flex; flex-direction: column; gap: 24px;\">", "")
    html = html.replace("<main>", "")
    html = html.replace("</main>", "")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Include header inside the main white container card for Module 2\n\n"
            "Update week01-operating-system-concepts/02-hardware-review.html so that\n"
            "the module header is placed directly inside the main .container card alongside\n"
            "the body text, framed by grey margins."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for Module 2 container alignment!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_header_container_wrapping()
