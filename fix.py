#!/usr/bin/env python3
# =====================================================================
# fix.py: Scope glossary strictly to architecture walkthrough terms
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

TARGETED_GLOSSARY_HTML = """        <!-- Dedicated Hardware Glossary: Walkthrough Architecture Terms Only -->
        <div style="margin-top: 16px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 14px 18px;">
          <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 8px;">
            Hardware Glossary: Architecture Terms Used in This Walkthrough
          </div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; font-size: 0.84rem; color: #334155; line-height: 1.5;">
            <div style="background: #f8fafc; border-left: 3px solid #10b981; padding: 8px 12px; border-radius: 0 4px 4px 0;">
              <strong style="color: #047857;">Pipeline Bubble (Stall / NOP)</strong>
              <p style="margin: 4px 0 0 0; color: #475569;">
                An idle clock cycle where a stage performs no useful operation. Bubbles occur naturally during pipeline warm-up/drain or when hardware must wait for unresolved data dependencies.
              </p>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #8b5cf6; padding: 8px 12px; border-radius: 0 4px 4px 0;">
              <strong style="color: #6d28d9;">Wide Instruction Fetch Unit</strong>
              <p style="margin: 4px 0 0 0; color: #475569;">
                A widened bus and buffer that pulls a wide block of machine code (e.g., 16 to 64 bytes) from L1 cache in a single cycle, supplying multiple instruction decoders simultaneously in superscalar cores.
              </p>
            </div>
            <div style="background: #f8fafc; border-left: 3px solid #0284c7; padding: 8px 12px; border-radius: 0 4px 4px 0;">
              <strong style="color: #0369a1;">Data Forwarding Bypass (Bypass Network)</strong>
              <p style="margin: 4px 0 0 0; color: #475569;">
                Dedicated multiplexer data paths routing an ALU result directly to an earlier stage's inputs, allowing a dependent instruction to execute immediately without waiting for register file writeback.
              </p>
            </div>
          </div>
        </div>"""

def filter_glossary_to_architecture_terms():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern targeting the glossary container block
    glossary_pattern = (
        r'<!-- Dedicated Hardware Glossary.*?-->\s*'
        r'<div style="margin-top: 16px; background: #ffffff; border: 1px solid #e2e8f0;.*?'
        r'</div>\s*</div>\s*</div>'
    )

    match = re.search(glossary_pattern, content, flags=re.DOTALL)
    if match:
        content = content[:match.start()] + TARGETED_GLOSSARY_HTML.strip() + content[match.end():]
        print("--> Successfully replaced glossary with architecture-specific terms.")
    else:
        # Fallback: search for header text
        alt_pattern = r'<div style="[^"]*">\s*Hardware Glossary:.*?</div>\s*</div>\s*</div>'
        match_alt = re.search(alt_pattern, content, flags=re.DOTALL)
        if match_alt:
            content = content[:match_alt.start()] + TARGETED_GLOSSARY_HTML.strip() + content[match_alt.end():]
            print("--> Replaced glossary via fallback pattern.")
        else:
            print("--> Could not locate existing glossary container to replace.")
            return

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Trim glossary to terms directly used in architecture walkthrough\n\n"
            "Retain only pipeline bubbles, wide instruction fetch units, and data\n"
            "forwarding bypasses in the silicon mechanics glossary in Module 2."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    filter_glossary_to_architecture_terms()
