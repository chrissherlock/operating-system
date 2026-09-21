#!/usr/bin/env python3
# =====================================================================
# fix.py: Clarify dual load ports and crossbar jargon in Module 2
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def clarify_superscalar_cycle3():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Target the jargon-heavy text in Superscalar Cycle 3
    old_text = (
        'what: "<code>I1</code> and <code>I2</code> execute in parallel on separate memory load ports. '
        'Their loaded values are forwarded immediately across an internal bypass crossbar into the integer '
        'execution units for <code>I3</code> and <code>I4</code>."'
    )

    new_text = (
        'what: "Because the L1 cache has dual memory read channels (\\"load ports\\"), the CPU retrieves '
        'both numbers <em>A</em> and <em>B</em> from memory at the exact same moment. Instead of making '
        'downstream instructions wait for those values to be saved to registers first, direct internal bypass wires '
        '(an internal crossbar network) route the loaded numbers straight into the math units so <code>I3</code> '
        'can start multiplying immediately."'
    )

    # Also make the "why" pane friendlier
    old_why = (
        'why: "Superscalar architectures use dual-ported or banked L1 data caches so two distinct memory '
        'loads can be serviced simultaneously without causing a cache port structural hazard."'
    )

    new_why = (
        'why: "Standard caches only allow one read at a time. To execute two loads simultaneously, the Level 1 '
        'cache is partitioned into multiple banks (or \\"dual-ported\\") like having two grocery checkout registers open '
        'at once. This prevents a memory bottleneck from forcing parallel pipelines to wait."'
    )

    if old_text in content:
        content = content.replace(old_text, new_text)
        if old_why in content:
            content = content.replace(old_why, new_why)

        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"--> Successfully clarified superscalar Cycle 3 mechanics in {TARGET_FILE}")

        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Clarify dual load ports and bypass crossbars in superscalar walkthrough\n\n"
                "Replace dense microarchitecture jargon with clear plain-English\n"
                "explanations for Cycle 3 superscalar execution in 02-hardware-review.html."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> Warning: Target text in Cycle 3 superscalar not matched.")

if __name__ == "__main__":
    clarify_superscalar_cycle3()
