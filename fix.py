#!/usr/bin/env python3
# =====================================================================
# fix.py: Add instructions and guidance to Module 2 interactive widget
# =====================================================================
import os
import re
import subprocess

INSTRUCTIONS_HTML = """
        <!-- Instructions & Learner Guide -->
        <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px; margin-bottom: 20px;">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">How to Use This Simulator</div>
          <ol style="margin-left: 20px; margin-bottom: 0; color: #334155; font-size: 0.88rem; line-height: 1.5;">
            <li><strong>Step Through the Lifecycle:</strong> Click <code>Next Step &rarr;</code> to step sequentially through each phase of the system call. Click <code>&larr; Prev</code> to review previous states, or <code>Reset</code> to return to the beginning.</li>
            <li><strong>Observe the Hardware State Bar:</strong> Notice how the <strong>CPU Mode</strong> changes color between red (User Mode / Ring 3) and blue (Kernel Mode / Ring 0), and how the <strong>Program Counter (PC)</strong> shifts between user space addresses and high kernel memory.</li>
            <li><strong>Track Data and Privilege Flow:</strong> The highlighted vector path and active nodes below show exactly which hardware component is executing instructions at each stage.</li>
          </ol>
        </div>
"""

def inject_simulator_instructions():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Place the instructions right above the Hardware State Bar inside the interactive widget
    target_marker = '<!-- Hardware State Bar -->'
    if 'How to Use This Simulator' not in content and target_marker in content:
        content = content.replace(target_marker, f"{INSTRUCTIONS_HTML}\n        {target_marker}")
        print("--> Successfully added user instructions to interactive simulator.")
    else:
        print("--> Instructions already exist or target marker not found.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Add explicit instructions and learner guidance to Module 2 simulator\n\n"
            "Update week01-operating-system-concepts/02-hardware-review.html to provide\n"
            "clear operational instructions and learning goals for the TRAP widget."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    inject_simulator_instructions()
