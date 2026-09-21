#!/usr/bin/env python3
# =====================================================================
# fix.py: Demystify "pipeline bubbles" in 02-hardware-review.html
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def update_bubble_explanations():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update the Cycle 1 "what" explanation in JavaScript
    old_cycle1_what = (
        'what: "The CPU begins execution by asserting Program Counter <code>0x00401000</code> on the '
        'instruction bus. The machine code for <code>I1: LOAD R1, [A]</code> is latched into the '
        'Instruction Fetch (IF) register. Hardware automatically increments <code>PC &larr; PC + 4</code>. '
        'The Decode, Execute, and Writeback stages hold uninitialized bubbles."'
    )

    new_cycle1_what = (
        'what: "The CPU begins execution by asserting Program Counter <code>0x00401000</code> on the '
        'instruction bus. The machine code for <code>I1: LOAD R1, [A]</code> is latched into the '
        'Instruction Fetch (IF) register, and the hardware increments <code>PC &larr; PC + 4</code>.<br><br>'
        '<strong>What is a \\"Bubble\\"?</strong> In CPU design, a <em>bubble</em> is jargon for an '
        'idle stage that does no useful work—essentially an enforced <code>NOP</code> (No Operation). '
        'Think of an automated car wash: when the first car enters the Soap bay, the Scrub, Rinse, '
        'and Dry bays downstream are completely empty. Because our conveyor belt just turned on, '
        'Decode, Execute, and Writeback hold inactive control bits until <code>I1</code> physically shifts '
        'into them over the next few cycles."'
    )

    # 2. Update Cycle 1 "why" explanation in JavaScript
    old_cycle1_why = (
        'why: "Dividing instruction processing into discrete stages decoupled by edge-triggered D flip-flops '
        'isolates path delays. The clock frequency only needs to accommodate the propagation delay of the '
        'longest individual stage rather than the entire instruction execution cycle."'
    )

    new_cycle1_why = (
        'why: "A pipeline requires a brief \\"fill latency\\" ($k-1$ cycles) before all stages are populated. '
        'During this warm-up, the control unit explicitly disables write-enable flags for downstream stages '
        'so empty bubbles cannot accidentally corrupt register values or trip spurious hardware faults. '
        'Once <code>I1</code> reaches Writeback at Cycle 4, every bubble will have drained and the pipeline '
        'reaches steady-state 1.0 IPC."'
    )

    # 3. Update preview text for Cycle 1
    old_cycle1_preview = (
        'inlinePreview: "We are at Cycle 1. I1 has been fetched into the core. Next, I1 moves into the '
        'Decode stage while the Fetch stage retrieves I2. Click Next to advance to Cycle 2."'
    )

    new_cycle1_preview = (
        'inlinePreview: "We are at Cycle 1 (Pipeline Priming). I1 is entering the Fetch bay while downstream '
        'stages sit idle as bubbles. Next, I1 advances to Decode while I2 enters Fetch. Click Next to advance to Cycle 2."'
    )

    content = content.replace(old_cycle1_what, new_cycle1_what)
    content = content.replace(old_cycle1_why, new_cycle1_why)
    content = content.replace(old_cycle1_preview, new_cycle1_preview)

    # 4. Make SVG stage labels friendlier when empty
    content = content.replace('decode: "Empty (Bubble)"', 'decode: "Idle (Bubble: No Op)"')
    content = content.replace('exec: "Empty (Bubble)"', 'exec: "Idle (Bubble: No Op)"')
    content = content.replace('wb: "Empty (Bubble)"', 'wb: "Idle (Bubble: No Op)"')
    content = content.replace('>Empty (Bubble)<', '>Idle (Bubble: No Op)<')

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Updated pipeline bubble explanations in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Clarify pipeline bubble terminology and mechanics in Module 2 simulator\n\n"
            "Add plain-English explanations and the assembly line analogy for pipeline\n"
            "bubbles in cycle 1 of the instruction throughput walkthrough."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for pipeline bubble clarification!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_bubble_explanations()
