#!/usr/bin/env python3
# =====================================================================
# fix.py: Add historical footnote about Rings 1 and 2 to Module 2
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

RINGS_FOOTNOTE_HTML = """        <div style="margin-top: 12px; background: #ffffff; border: 1px solid #d8b4te; border-left: 3px solid #7c3aed; padding: 10px 14px; border-radius: 0 4px 4px 0; font-size: 0.85rem;">
          <strong style="color: #6d28d9;">Historical Footnote: What Happened to Rings 1 and 2?</strong>
          <p style="margin: 4px 0 0 0; color: #475569; line-height: 1.5;">
            While Intel's hardware design originally defined 4 rings—with <strong>Ring 1</strong> intended for device drivers and <strong>Ring 2</strong> for system services—mainstream operating systems like Linux and Windows chose to ignore them, using only **Ring 0 (Kernel)** and **Ring 3 (User)**. Running drivers in Ring 1 or 2 provided little real-world security protection because a driver bug could still compromise the kernel, and managing four hardware rings added unnecessary architectural complexity.
          </p>
        </div>"""

def add_rings_footnote():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if "Historical Footnote: What Happened to Rings 1 and 2?" in content:
        print("--> Rings 1 and 2 footnote already present.")
        return

    # Find the closing div of the privilege hierarchies deep dive box
    target_marker = 'Regardless of nomenclature, the hardware state machine enforces identical safety guarantees: unprivileged instructions cannot manipulate page tables, modify control registers, or execute raw I/O without trapping through a controlled supervisor gateway.\n        </p>\n      </div>'

    if target_marker in content:
        replacement = target_marker.replace('\n      </div>', '\n' + RINGS_FOOTNOTE_HTML + '\n      </div>')
        content = content.replace(target_marker, replacement)
        print("--> Added Rings 1 and 2 historical footnote inside privilege deep dive box.")
    else:
        # Fallback target matching end of privilege deep dive box
        fallback = 'Regardless of nomenclature, the hardware state machine enforces identical safety guarantees'
        if fallback in content:
            # Append before closing div of aside-box
            idx = content.find(fallback)
            end_div = content.find('</div>', idx)
            # Find the second closing div or end of aside-box
            aside_end = content.find('</div>\n\n      <h2>3.', idx)
            if aside_end != -1:
                content = content[:aside_end] + RINGS_FOOTNOTE_HTML + "\n      " + content[aside_end:]
                print("--> Added Rings 1 and 2 footnote via fallback position.")
            else:
                print("--> Error: Could not locate exact insertion point for footnote.")
                return
        else:
            print("--> Error: Could not find privilege deep dive container.")
            return

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add historical footnote on Rings 1 and 2 to Module 2 privilege deep dive\n\n"
            "Insert an explanatory note detailing the original design intent of x86\n"
            "Rings 1 and 2 and why modern operating systems use a flat 2-ring model."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for Rings 1 & 2 footnote!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    add_rings_footnote()
