#!/usr/bin/env python3
# =====================================================================
# fix.py: Give concrete numeric examples for memory terms A and B
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def clarify_memory_operands():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update the Scenario briefing box to include concrete numbers
    old_scenario_snippet = (
        'We are computing one single term of a vector dot product: <strong><code>sum = sum + (A &times; B)</code></strong>. '
        'This Multiply-Accumulate operation is the foundational math kernel used in 3D graphics transforms, '
        'audio DSP filters, and machine learning tensor operations:'
    )

    new_scenario_snippet = (
        'We are computing one single term of a vector dot product: <strong><code>sum = sum + (A &times; B)</code></strong> '
        '(for example: <code>0 + (3 &times; 5) = 15</code>, where <code>[A]</code> and <code>[B]</code> are memory addresses '
        'holding the input numbers <strong>3</strong> and <strong>5</strong>). This Multiply-Accumulate operation is the '
        'foundational math kernel used in 3D graphics, audio filters, and machine learning:'
    )

    content = content.replace(old_scenario_snippet, new_scenario_snippet)

    # 2. Update Cycle 3 superscalar text to reference the concrete example
    old_cycle3_what = (
        'what: "Because the L1 cache has dual memory read channels (\\"load ports\\"), the CPU retrieves '
        'both numbers <em>A</em> and <em>B</em> from memory at the exact same moment.'
    )

    new_cycle3_what = (
        'what: "Because the L1 cache has dual memory read channels (\\"load ports\\"), the CPU retrieves '
        'both input numbers from memory addresses <code>[A]</code> and <code>[B]</code> (e.g., values 3 and 5) '
        'at the exact same moment.'
    )

    content = content.replace(old_cycle3_what, new_cycle3_what)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Updated concrete values for A and B in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Clarify memory variables A and B with concrete values in Module 2\n\n"
            "Give concrete numeric examples (A=3, B=5) for vector memory terms in the\n"
            "pipeline and superscalar walkthrough within 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    clarify_memory_operands()
