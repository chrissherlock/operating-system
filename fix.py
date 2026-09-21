#!/usr/bin/env python3
# =====================================================================
# fix.py: Add beginner-friendly explanation of "latched" to Module 2
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def update_latch_explanation():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Target the Cycle 1 "what" string in JavaScript
    old_target = (
        'what: "The CPU begins execution by asserting Program Counter <code>0x00401000</code> on the '
        'instruction bus. The machine code for <code>I1: LOAD R1, [A]</code> is latched into the '
        'Instruction Fetch (IF) register, and the hardware increments <code>PC &larr; PC + 4</code>.<br><br>'
        '<strong>What is a \\"Bubble\\"?</strong>'
    )

    new_replacement = (
        'what: "The CPU begins execution by asserting Program Counter <code>0x00401000</code> on the '
        'instruction bus. The machine code for <code>I1: LOAD R1, [A]</code> is <strong>latched</strong> '
        '(captured and locked in place) into the Instruction Fetch (IF) register, and the hardware '
        'increments <code>PC &larr; PC + 4</code>.<br><br>'
        '<strong>What does \\"Latched\\" mean?</strong> Think of a camera shutter snapping a photo: '
        'voltages on the memory wires constantly fluctuate, but when the CPU clock ticks, internal storage '
        'circuits (latches) snap shut to freeze those electrical 1s and 0s rock-solid. This guarantees that '
        'the Decode stage sees a stable, unchanging copy of <code>I1</code> even when the bus starts fetching '
        'the next instruction.<br><br>'
        '<strong>What is a \\"Bubble\\"?</strong>'
    )

    if old_target in content:
        content = content.replace(old_target, new_replacement)
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"--> Successfully integrated beginner-friendly latch explanation in {TARGET_FILE}")

        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Clarify register latching terminology in Module 2 pipeline walkthrough\n\n"
                "Add a concise, beginner-friendly explanation of hardware register latching\n"
                "using the camera snapshot analogy in cycle 1 of 02-hardware-review.html."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully for latch explanation update!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> Warning: Target substring for Cycle 1 explanation not found.")

if __name__ == "__main__":
    update_latch_explanation()
