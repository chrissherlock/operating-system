#!/usr/bin/env python3
# =====================================================================
# fix.py: Add wide instruction fetch unit definition to silicon glossary
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

WIDE_FETCH_CARD = """            <div style="background: #f8fafc; border-left: 3px solid #8b5cf6; padding: 8px 12px; border-radius: 0 4px 4px 0;">
              <strong style="color: #6d28d9;">What is a "Wide Instruction Fetch Unit"?</strong>
              <p style="margin: 4px 0 0 0; color: #475569;">
                A widened memory bus that grabs a large chunk of cache memory (e.g., 16 to 64 bytes) in a single clock cycle instead of reading one instruction at a time. This floods the instruction queue so multiple decoders and ALUs can fire in parallel (superscalar execution) without waiting on memory.
              </p>
            </div>"""

def add_wide_fetch_definition():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if already added
    if "What is a \"Wide Instruction Fetch Unit\"?" in content:
        print("--> Definition for Wide Instruction Fetch Unit already present.")
        return

    # Find the closing tag of the third card (Pipeline Bubble)
    bubble_marker = '<strong style="color: #047857;">What is a "Pipeline Bubble"?</strong>'
    if bubble_marker in content:
        idx = content.find(bubble_marker)
        # Find closing </div> of this card
        card_end = content.find('</div>', idx) + 6
        content = content[:card_end] + "\n" + WIDE_FETCH_CARD + content[card_end:]
        print("--> Added Wide Instruction Fetch Unit card to silicon mechanics glossary.")
    else:
        print("--> Error: Could not locate Pipeline Bubble card in glossary.")
        return

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add wide instruction fetch unit definition to Module 2 glossary\n\n"
            "Define wide instruction fetch units in the beginner silicon mechanics\n"
            "glossary within 02-hardware-review.html to support superscalar concepts."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    add_wide_fetch_definition()
