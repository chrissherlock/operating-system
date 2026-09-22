#!/usr/bin/env python3
# =====================================================================
# fix.py: Embed Manchester Atlas image into Module 2 historical aside
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)

ATLAS_IMAGE_HTML = """        <div style="margin-top: 14px; display: flex; justify-content: center;">
          <div class="image-card" style="max-width: 380px; width: 100%;">
            <img src="../images/university-of-manchester-atlas.jpg" alt="University of Manchester Atlas Computer">
            <span>
              <strong>University of Manchester Atlas (1962)</strong><br>
              Pioneered virtual memory paging and hardware interrupts.<br>
              <small><a href="https://en.wikipedia.org/wiki/Atlas_(computer)" target="_blank" rel="noopener">Wikipedia: Atlas Computer</a></small>
            </span>
          </div>
        </div>"""

def insert_atlas_image():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    target_anchor = "Pioneer Insight: The Manchester Atlas &amp; The Invention of the Hardware Trap</strong>"
    if target_anchor not in content:
        print("Error: Could not locate Manchester Atlas aside anchor in Module 2.")
        return

    # Check if image is already embedded
    if "university-of-manchester-atlas.jpg" in content:
        print("Notice: Manchester Atlas image is already embedded.")
        return

    # Find the closing </div> of the Atlas aside paragraph and insert the image HTML right before it
    parts = content.split(target_anchor, 1)
    # Find the end of the first paragraph inside this aside box
    aside_content_parts = parts[1].split("</p>", 1)

    updated_aside_content = f"{aside_content_parts[0]}</p>\n{ATLAS_IMAGE_HTML}\n{aside_content_parts[1]}"
    updated_full_content = f"{parts[0]}{target_anchor}{updated_aside_content}"

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_full_content)

    print(f"--> Successfully embedded Manchester Atlas image into {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add Manchester Atlas computer image to historical aside in Module 2\n\n"
            "Embed images/university-of-manchester-atlas.jpg into the Manchester Atlas\n"
            "research aside box in 02-hardware-review.html with clean card styling."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    insert_atlas_image()
