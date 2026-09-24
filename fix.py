#!/usr/bin/env python3
# =====================================================================
# fix.py: Fix black path fill artifact in Figure 2.2 of Module 04
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "04-thread-implementation.html")

def correct_svg_path_fills():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Targets in Figure 2.2
    old_running_waiting = (
        '<path d="M 525 165 C 510 230, 480 232, 445 232" stroke="#dc2626" '
        'stroke-width="1.8" marker-end="url(#sm-arr-alert)" />'
    )
    new_running_waiting = (
        '<path d="M 525 165 C 510 230, 480 232, 445 232" fill="none" '
        'stroke="#dc2626" stroke-width="1.8" marker-end="url(#sm-arr-alert)" />'
    )

    old_waiting_ready = (
        '<path d="M 340 232 C 240 232, 230 200, 237 165" stroke="#0284c7" '
        'stroke-width="1.8" marker-end="url(#sm-arr)" />'
    )
    new_waiting_ready = (
        '<path d="M 340 232 C 240 232, 230 200, 237 165" fill="none" '
        'stroke="#0284c7" stroke-width="1.8" marker-end="url(#sm-arr)" />'
    )

    old_preempt = (
        '<path d="M 547 110 C 547 65, 260 65, 245 105" stroke="#0284c7" '
        'stroke-width="1.5" stroke-dasharray="3 3" marker-end="url(#sm-arr)" />'
    )
    new_preempt = (
        '<path d="M 547 110 C 547 65, 260 65, 245 105" fill="none" '
        'stroke="#0284c7" stroke-width="1.5" stroke-dasharray="3 3" marker-end="url(#sm-arr)" />'
    )

    content = content.replace(old_running_waiting, new_running_waiting)
    content = content.replace(old_waiting_ready, new_waiting_ready)
    content = content.replace(old_preempt, new_preempt)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully removed black fill artifacts from {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix black path fill in Windows dispatcher state diagram in Module 04\n\n"
            "Add explicit fill=\"none\" to curved transition paths in Figure 2.2 to\n"
            "prevent SVG default black fill artifacts from rendering under arcs."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    correct_svg_path_fills()
