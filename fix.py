#!/usr/bin/env python3
# =====================================================================
# fix.py: Normalize Butler Lampson image filename and path reference
# =====================================================================
import os
import shutil
import subprocess

TARGET_HTML = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)
IMAGES_DIR = "images"
DESIRED_FILENAME = "butler-lampson.jpg"
DESIRED_PATH = os.path.join(IMAGES_DIR, DESIRED_FILENAME)

def normalize_lampson_asset():
    print("--> Checking local image assets in root 'images/' directory...")

    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR, exist_ok=True)
        print(f"--> Created missing '{IMAGES_DIR}' directory.")

    # Check if target image already exists
    if not os.path.exists(DESIRED_PATH):
        # Search for potential unnormalized variants
        candidates = [
            "Butler Lampson Royal Society (cropped).jpg",
            "Butler_Lampson_Royal_Society_(cropped).jpg",
            "ButlerLampson.jpg",
            "lampson.jpg"
        ]
        found = False
        for candidate in candidates:
            candidate_path = os.path.join(IMAGES_DIR, candidate)
            if os.path.exists(candidate_path):
                shutil.copy(candidate_path, DESIRED_PATH)
                print(f"--> Copied '{candidate}' to normalized filename '{DESIRED_FILENAME}'.")
                found = True
                break
        if not found:
            print(f"--> Notice: '{DESIRED_FILENAME}' not found in '{IMAGES_DIR}/'. Please place the image there if missing.")
    else:
        print(f"--> Confirmed: '{DESIRED_FILENAME}' exists in root images folder.")

    if os.path.exists(TARGET_HTML):
        with open(TARGET_HTML, "r", encoding="utf-8") as f:
            content = f.read()

        # Ensure correct relative path reference
        correct_src = 'src="../images/butler-lampson.jpg"'
        if correct_src not in content:
            # Replace any variant src path
            import re
            content = re.sub(r'src="[^"]*butler-lampson\.jpg"', correct_src, content)
            content = re.sub(r'src="[^"]*Butler[^"]*\.jpg"', correct_src, content)

            with open(TARGET_HTML, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"--> Updated image src reference in {TARGET_HTML}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_HTML], check=True)
        if os.path.exists(DESIRED_PATH):
            subprocess.run(["git", "add", DESIRED_PATH], check=True)

        commit_msg = (
            "Normalize Butler Lampson image filename and reference in Module 2\n\n"
            "Ensure images/butler-lampson.jpg exists under the expected lowercase\n"
            "hyphenated name in the root images folder and update references."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    normalize_lampson_asset()
