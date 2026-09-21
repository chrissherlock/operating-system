#!/usr/bin/env python3
# =====================================================================
# fix.py: Clean up mechanics panes and add dedicated hardware glossary
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

GLOSSARY_HTML = """        <!-- Dedicated Hardware Glossary & Core Concepts Box -->
        <div style="margin-top: 16px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 14px 18px;">
          <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 8px;">
            Hardware Glossary: Beginner Guide to Silicon Mechanics
          </div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; font-size: 0.84rem; color: #334155; line-height: 1.5;">
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 8px 12px; border-radius: 0 4px 4px 0;">
              <strong style="color: #0369a1;">What does "Latched" mean?</strong>
              <p style="margin: 4px 0 0 0; color: #475569;">
                <strong>Captured and locked in place.</strong> Voltages on memory buses drift and fluctuate. When the register clock triggers, storage circuits (flip-flops) snap shut like a camera shutter, freezing those electrical 1s and 0s rock-solid so downstream stages read an unchanging value.
              </p>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #f59e0b; padding: 8px 12px; border-radius: 0 4px 4px 0;">
              <strong style="color: #b45309;">What is the "Rising Clock Edge"?</strong>
              <p style="margin: 4px 0 0 0; color: #475569;">
                The CPU clock is a square wave oscillating between 0V (low) and ~1V (high). The <strong>rising edge</strong> is the exact instantaneous transition when voltage jumps from 0 to 1. Like a conductor's baton downbeat, this single moment tells all registers across the chip to advance together.
              </p>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #10b981; padding: 8px 12px; border-radius: 0 4px 4px 0;">
              <strong style="color: #047857;">What is a "Pipeline Bubble"?</strong>
              <p style="margin: 4px 0 0 0; color: #475569;">
                An idle cycle where a stage does no useful work—an enforced <code>NOP</code> (No Operation). Just like empty wash bays when an automated car wash first starts up, downstream stages sit idle until the first real instruction shifts into them.
              </p>
            </div>
          </div>
        </div>"""

def update_walkthrough_layout():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Streamline the Cycle 1 "what" string so it focuses cleanly on mechanics
    clean_cycle1_what = (
        'what: "The CPU begins execution by asserting Program Counter <code>0x00401000</code> on the '
        'instruction bus. On the rising clock edge, the machine code for <code>I1: LOAD R1, [A]</code> is '
        'latched into the Instruction Fetch (IF) register, and the hardware increments <code>PC &larr; PC + 4</code>. '
        'Because the pipeline has just started, the Decode, Execute, and Writeback stages hold idle bubbles '
        'and perform no operations."'
    )

    # Replace verbose inline definition in Cycle 1
    cycle1_what_regex = r'what:\s*"The CPU begins execution by asserting Program Counter <code>0x00401000.*?and perform no operations\."'
    match = re.search(cycle1_what_regex, content, flags=re.DOTALL)
    if match:
        content = content[:match.start()] + clean_cycle1_what + content[match.end():]
        print("--> Cleaned Cycle 1 mechanics description.")
    else:
        # Broader pattern matching if previous text was slightly different
        fallback_pattern = r'what:\s*"The CPU begins execution by asserting Program Counter.*?What is a \\"Bubble\\".*?over the next few cycles\."'
        match_fb = re.search(fallback_pattern, content, flags=re.DOTALL)
        if match_fb:
            content = content[:match_fb.start()] + clean_cycle1_what + content[match_fb.end():]
            print("--> Cleaned Cycle 1 mechanics description via fallback.")

    # 2. Insert the Hardware Glossary box right after the Paired Analytical Panes container
    if "Hardware Glossary: Beginner Guide to Silicon Mechanics" not in content:
        # Locate the end of the paired analytical panes container
        panes_marker = '<div id="pipe-desc-why" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>\n          </div>\n        </div>'
        if panes_marker in content:
            content = content.replace(panes_marker, panes_marker + "\n\n" + GLOSSARY_HTML)
            print("--> Injected Hardware Glossary panel under analytical panes.")
        else:
            # Fallback insertion before closing </div> of interactive-pipeline-simulator
            sim_end_pattern = r'(\s*</div>\s*<script>\s*\(function\(\)\s*\{\s*const pipeStorylines)'
            match_end = re.search(sim_end_pattern, content)
            if match_end:
                content = content[:match_end.start()] + "\n\n" + GLOSSARY_HTML + content[match_end.start():]
                print("--> Injected Hardware Glossary panel before simulator script.")
            else:
                print("--> Warning: Could not locate insertion point for Hardware Glossary.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add hardware glossary panel below analytical panes in Module 2\n\n"
            "Move definitions of latched, rising clock edge, and pipeline bubbles\n"
            "into a dedicated reference box below the walkthrough analytical panes."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_walkthrough_layout()
