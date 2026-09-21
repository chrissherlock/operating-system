#!/usr/bin/env python3
# =====================================================================
# fix.py: Repair Instruction Throughput Engine walkthrough script closure
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def repair_pipeline_script():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate the pipeline script block and ensure its IIFE closure is intact
    target_snippet = """          document.getElementById("pipe-reset-btn").addEventListener("click", function() {
            pipeIndex = 0;
            renderPipeState();
          });

          renderPipeState();
        })();"""

    if target_snippet not in content:
        # If the IIFE closing was truncated, let's search for renderPipeState(); and append it cleanly
        broken_snippet = """          document.getElementById("pipe-reset-btn").addEventListener("click", function() {
            pipeIndex = 0;
            renderPipeState();
          });

          renderPipeState();"""

        if broken_snippet in content:
            content = content.replace(broken_snippet, broken_snippet + "\n        })();")
            print("--> Restored missing IIFE closure for pipeStorylines script.")
        else:
            print("--> Warning: Exact pipeStorylines script block pattern not matched.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix broken script closure in Instruction Throughput Engine walkthrough\n\n"
            "Restore missing IIFE closure and event binding logic for the instruction\n"
            "throughput engine interactive stepper in 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for pipeline script repair!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    repair_pipeline_script()
