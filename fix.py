#!/usr/bin/env python3
# =====================================================================
# fix.py: Transform foreshadowed navigation panels into a true story arc
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def upgrade_to_narrative_story_arc():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace dry preview labels with true story-driven narrative prompts across the walkthroughs
    content = content.replace(
        'Where We Are &amp; What Happens Next Click:',
        'Active Story Chapter &amp; Next Plot Point:'
    )
    content = content.replace(
        'Where We Are & What Happens Next Click:',
        'Active Story Chapter & Next Plot Point:'
    )

    # Enhance pipeline storyline inline previews to read like narrative story beats
    pipeline_updates = {
        'inlinePreview: "We are at Cycle 1 (Pipeline Priming). I1 is entering the Fetch bay while downstream stages sit idle as bubbles. Next, I1 advances to Decode while I2 enters Fetch. Click Next to advance to Cycle 2.",':
            'inlinePreview: "<strong>Chapter 1 -- The Awakening:</strong> I1 enters the Fetch bay while the execution units wait in silence. <em>Next plot point:</em> I1 shifts into Decode as I2 joins the pipeline queue. Click Next to advance.",',
        'inlinePreview: "We are at Cycle 2. I1 is decoding and I2 is fetching. Next, I1 executes its memory address calculation, I2 decodes, and I3 (MUL) is fetched. Click Next to advance to Cycle 3.",':
            'inlinePreview: "<strong>Chapter 2 -- Parallel Motion:</strong> I1 decodes its opcode while I2 enters Fetch. <em>Next plot point:</em> I1 calculates memory addresses in the ALU. Click Next to advance.",',
        'inlinePreview: "We are at Cycle 3. I1 is executing and I3 detects a data dependency on R1. Next, the pipeline fills completely, I1 completes writeback, and data forwarding provides R1 to I3 without stalling. Click Next to advance to Cycle 4.",':
            'inlinePreview: "<strong>Chapter 3 -- The Hazard Arrives:</strong> I3 halts momentarily, spotting an unfulfilled dependency on R1. <em>Next plot point:</em> The data forwarding bypass activates to bridge the gap. Click Next to advance.",',
        'inlinePreview: "We are at Cycle 4. All four stages are occupied and I1 has retired. Next, I2 writes back R2 and I3 enters the ALU for multiplication. Click Next to advance to Cycle 5.",':
            'inlinePreview: "<strong>Chapter 4 -- Steady State &amp; First Retirement:</strong> The assembly line hums at 1.0 IPC as I1 officially retires. <em>Next plot point:</em> Multiplication begins. Click Next to advance.",'
    }

    for old_p, new_p in pipeline_updates.items():
        content = content.replace(old_p, new_p)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print("--> Upgraded foreshadowed preview panels to a true narrative story arc.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Transform preview panel into a true narrative story arc in Module 2\n\n"
            "Update inline preview labels and text in 02-hardware-review.html to frame\n"
            "each step as a chapter in an end-to-end silicon journey."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for narrative upgrade!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    upgrade_to_narrative_story_arc()
