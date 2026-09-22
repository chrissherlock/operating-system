#!/usr/bin/env python3
# =====================================================================
# fix.py: Update Manchester Atlas image caption with full attribution
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)

UPDATED_ATLAS_IMAGE_HTML = """        <div style="margin-top: 14px; display: flex; justify-content: center;">
          <div class="image-card" style="max-width: 380px; width: 100%;">
            <img src="../images/university-of-manchester-atlas.jpg" alt="University of Manchester Atlas Computer, January 1963">
            <span>
              <strong>University of Manchester Atlas (January 1963)</strong><br>
              Pioneered virtual memory paging and hardware interrupts.<br>
              <small><a href="https://en.wikipedia.org/wiki/Atlas_(computer)" target="_blank" rel="noopener">Wikipedia: Atlas Computer</a></small><br>
              <small><a href="https://commons.wikimedia.org/w/index.php?title=File:University_of_Manchester_Atlas,_January_1963.JPG&oldid=1143384475" target="_blank" rel="noopener">Wikimedia Commons File Record</a></small><br>
              <small>Author: Iain MacCallum / Wikimedia Commons contributors</small>
            </span>
          </div>
        </div>"""

def update_atlas_attribution():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if "university-of-manchester-atlas.jpg" not in content:
        print("Error: Manchester Atlas image card not found in Module 2.")
        return

    # Replace the existing image block with the fully attributed version
    # We locate the card container for this image
    old_block_start = '<div style="margin-top: 14px; display: flex; justify-content: center;">'
    if old_block_start in content:
        parts = content.split(old_block_start)
        # Find the specific part containing the atlas image
        for i, part in enumerate(parts):
            if "university-of-manchester-atlas.jpg" in part:
                # Reconstruct up to this block, insert updated HTML, and append remainder
                remainder = part.split("</div>\n          </div>\n        </div>", 1)[1]
                parts[i] = f"{UPDATED_ATLAS_IMAGE_HTML}{remainder}"
                content = old_block_start.join(parts)
                break

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully updated Manchester Atlas attribution in {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Update Manchester Atlas image caption with complete Wikimedia attribution\n\n"
            "Revise the image card caption in 02-hardware-review.html to include\n"
            "author attribution (Iain MacCallum), source, and permanent Wikimedia URL."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_atlas_attribution()
