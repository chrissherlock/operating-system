#!/usr/bin/env python3
# =====================================================================
# fix.py: Add scenario briefing card to Address Translation simulator
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

TRANSLATION_GUIDE_CARD = """        <!-- Instructions & Scenario Guide -->
        <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px; margin-bottom: 16px;">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">The Scenario: Tracing a 4 KiB Virtual-to-Physical Translation</div>
          <p style="margin: 0 0 8px 0; color: #1e293b; font-size: 0.9rem; line-height: 1.5;">
            We are tracing how the MMU translates virtual address <strong><code>0x00403018</code></strong> into physical DRAM address <strong><code>0x07B40018</code></strong>. This walkthrough demonstrates the foundational mechanics of virtual memory:
          </p>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px; margin-bottom: 10px;">
            <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px 10px; font-size: 0.82rem;">
              <strong style="color: #0284c7; font-family: var(--font-mono);">1. Bit-Slicing (VPN)</strong>
              <div style="color: #64748b; margin-top: 2px;">Upper address bits identify the Virtual Page Number (<code>0x00403</code>) for page table walks.</div>
            </div>
            <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px 10px; font-size: 0.82rem;">
              <strong style="color: #059669; font-family: var(--font-mono);">2. Offset Pass-Through</strong>
              <div style="color: #64748b; margin-top: 2px;">Lower 12 bits (<code>0x018</code>) bypass translation entirely, passing through unmodified.</div>
            </div>
            <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px 10px; font-size: 0.82rem;">
              <strong style="color: #7c3aed; font-family: var(--font-mono);">3. Frame Assembly (PFN)</strong>
              <div style="color: #64748b; margin-top: 2px;">Combined with Physical Frame Number (<code>0x07B40</code>) to form the final physical address.</div>
            </div>
          </div>
          <ol style="margin-left: 20px; margin-bottom: 0; color: #334155; font-size: 0.84rem; line-height: 1.5;">
            <li><strong>Why Offset Passes Through:</strong> Because virtual page size (4 KiB) matches physical frame size ($2^{12} = 4096$ bytes), intra-page byte offsets remain identical in physical RAM.</li>
            <li><strong>Granularity Toggles:</strong> Switch between <code>4 KiB Standard Page</code>, <code>2 MiB Superpage</code>, and <code>Swapped Page</code> modes to observe different MMU behaviors.</li>
          </ol>
        </div>"""

def add_translation_guide_card():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if "The Scenario: Tracing a 4 KiB Virtual-to-Physical Translation" in content:
        print("--> Translation guide card already present.")
        return

    # Target the opening div of the translation simulator
    sim_marker = '<div id="interactive-translation-simulator" style="margin: 32px 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">'
    header_marker = '<!-- Header & Dimension Toggles -->'

    target_pos = content.find(sim_marker)
    if target_pos != -1:
        header_pos = content.find(header_marker, target_pos)
        if header_pos != -1:
            content = content[:header_pos] + TRANSLATION_GUIDE_CARD + "\n        " + content[header_pos:]
            print("--> Successfully injected scenario briefing card into translation simulator.")
        else:
            print("--> Error: Could not locate header marker inside translation simulator.")
            return
    else:
        print("--> Error: Could not locate interactive translation simulator element.")
        return

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add scenario briefing card to Address Translation walkthrough\n\n"
            "Insert a structured instructional guide card above the address translation\n"
            "simulator in 02-hardware-review.html to frame the learning objectives."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for translation guide card!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    add_translation_guide_card()
