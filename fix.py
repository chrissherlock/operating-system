#!/usr/bin/env python3
# =====================================================================
# fix.py: Redesign glossary layout in 02-hardware-review.html
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

NEW_GLOSSARY_LAYOUT = """        <!-- Redesigned Hardware Architecture Glossary (Clean Reference Table) -->
        <div style="margin-top: 20px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; overflow: hidden;">
          <div style="background: #f8fafc; padding: 10px 16px; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: #334155; text-transform: uppercase; letter-spacing: 0.04em;">
              Quick Reference: Architecture Mechanics Used Above
            </span>
            <span style="font-size: 0.75rem; color: #64748b;">4 Key Concepts</span>
          </div>

          <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; line-height: 1.5;">
              <thead>
                <tr style="background: #f1f5f9; color: #475569; font-family: var(--font-mono); font-size: 0.75rem; text-transform: uppercase;">
                  <th style="padding: 8px 16px; border-bottom: 1px solid #cbd5e1; width: 25%;">Mechanism / Term</th>
                  <th style="padding: 8px 16px; border-bottom: 1px solid #cbd5e1; width: 30%;">Plain-English Concept</th>
                  <th style="padding: 8px 16px; border-bottom: 1px solid #cbd5e1; width: 45%;">Silicon Implementation</th>
                </tr>
              </thead>
              <tbody style="color: #334155;">
                <tr style="border-bottom: 1px solid #f1f5f9;">
                  <td style="padding: 10px 16px; font-weight: 700; color: #0284c7; font-family: var(--font-mono);">
                    Pipeline Bubble<br><span style="font-weight: 400; font-size: 0.75rem; color: #64748b;">(Stall / NOP)</span>
                  </td>
                  <td style="padding: 10px 16px; color: #475569;">
                    An empty conveyor belt station during warm-up or when waiting on a slow task.
                  </td>
                  <td style="padding: 10px 16px;">
                    Control signals disable register and memory writes for that stage. The CPU inserts an idle <code>NOP</code> so empty cycles cannot corrupt architectural state.
                  </td>
                </tr>
                <tr style="border-bottom: 1px solid #f1f5f9; background: #fafafa;">
                  <td style="padding: 10px 16px; font-weight: 700; color: #059669; font-family: var(--font-mono);">
                    Instructions Per Cycle<br><span style="font-weight: 400; font-size: 0.75rem; color: #64748b;">(IPC Throughput)</span>
                  </td>
                  <td style="padding: 10px 16px; color: #475569;">
                    How many finished items roll off the assembly line on each clock tick.
                  </td>
                  <td style="padding: 10px 16px;">
                    A single pipeline is physically capped at 1.0 IPC. Superscalar designs duplicate decoders and ALUs side-by-side to retire multiple instructions simultaneously (&gt; 1.0 IPC).
                  </td>
                </tr>
                <tr style="border-bottom: 1px solid #f1f5f9;">
                  <td style="padding: 10px 16px; font-weight: 700; color: #7c3aed; font-family: var(--font-mono);">
                    Wide Instruction Fetch
                  </td>
                  <td style="padding: 10px 16px; color: #475569;">
                    Scooping up a whole bucket of work at once instead of picking up one item.
                  </td>
                  <td style="padding: 10px 16px;">
                    A widened 16-to-64 byte cache bus fills an instruction buffer in a single cycle, supplying multiple instruction decoders simultaneously so ALUs never starve.
                  </td>
                </tr>
                <tr>
                  <td style="padding: 10px 16px; font-weight: 700; color: #d97706; font-family: var(--font-mono);">
                    Data Forwarding Bypass
                  </td>
                  <td style="padding: 10px 16px; color: #475569;">
                    Handing a freshly baked part directly to the next worker without putting it in storage first.
                  </td>
                  <td style="padding: 10px 16px;">
                    Multiplexer buses route ALU outputs directly back into the inputs of subsequent stages, allowing dependent math to proceed without waiting for register file writeback.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>"""

def replace_glossary_layout():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern capturing any existing glossary container
    glossary_pattern = (
        r'<!-- Dedicated Hardware Glossary.*?-->\s*'
        r'<div style="margin-top: 16px; background: #ffffff;.*?</div>\s*</div>\s*</div>'
    )

    match = re.search(glossary_pattern, content, flags=re.DOTALL)
    if match:
        content = content[:match.start()] + NEW_GLOSSARY_LAYOUT.strip() + content[match.end():]
        print("--> Replaced old card-grid glossary with clean reference table.")
    else:
        # Fallback: find the header text marker
        fallback_pattern = r'<div style="margin-top: 16px; background: #ffffff; border: 1px solid #e2e8f0;.*?</div>\s*</div>\s*</div>'
        match_fb = re.search(fallback_pattern, content, flags=re.DOTALL)
        if match_fb:
            content = content[:match_fb.start()] + NEW_GLOSSARY_LAYOUT.strip() + content[match_fb.end():]
            print("--> Replaced glossary via fallback pattern.")
        else:
            print("--> Could not locate existing glossary container.")
            return

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Redesign hardware glossary as a clean reference table in Module 2\n\n"
            "Replace multi-card grid with a compact, structured definition table\n"
            "under the pipeline analytical panes in 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    replace_glossary_layout()
