#!/usr/bin/env python3
# =====================================================================
# fix.py: Repair interactive walkthroughs and position definitions under mechanics
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def repair_and_fix_layout():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove any misplaced standalone glossary box from the briefing card area
    misplaced_glossary = """        <!-- Glossary Definitions: CR Registers & Table Structures -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 12px 16px; margin-top: 12px;">
          <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #7c3aed; text-transform: uppercase; margin-bottom: 6px;">Key Definitions &amp; Hardware Terminology</div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px; font-size: 0.83rem; color: #334155;">
            <div>
              <strong style="color: #0284c7; font-family: var(--font-mono);">CR3 (Control Register 3)</strong>
              <div style="color: #64748b; margin-top: 2px;">The processor root register storing the physical base address of the current process's top-level page table (PML4). Context switching updates CR3.</div>
            </div>
            <div>
              <strong style="color: #0284c7; font-family: var(--font-mono);">CR4 (Control Register 4)</strong>
              <div style="color: #64748b; margin-top: 2px;">Extended control register enabling advanced CPU features such as Physical Address Extension (PAE), page size extensions, and virtualization support.</div>
            </div>
            <div>
              <strong style="color: #0284c7; font-family: var(--font-mono);">PML4 (Page Map Level 4)</strong>
              <div style="color: #64748b; margin-top: 2px;">The top-level 4 KiB table in x86-64 4-level paging, containing 512 entries that point to Page Directory Pointer Tables (PDPTs).</div>
            </div>
            <div>
              <strong style="color: #059669; font-family: var(--font-mono);">PTE (Page Table Entry)</strong>
              <div style="color: #64748b; margin-top: 2px;">The leaf entry in a page table containing the physical frame number (PFN) and control flags (Present, R/W, User/Supervisor, NX).</div>
            </div>
          </div>
        </div>"""

    if misplaced_glossary in content:
        content = content.replace(misplaced_glossary, "")
        print("--> Removed misplaced glossary box from briefing card.")

    # 2. Place the Key Definitions box directly underneath the analytical panes / detailed mechanics
    definitions_under_mechanics = """        <!-- Paired Analytical Panes -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 16px;">
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0284c7; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #0284c7; text-transform: uppercase; letter-spacing: 0.03em;">Detailed Mechanics: What Is Happening</div>
            <div id="trans-desc-what" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>

          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #10b981; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 0.03em;">Why The System Does This</div>
            <div id="trans-desc-why" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>
        </div>

        <!-- Key Definitions & Hardware Terminology (Placed under Detailed Mechanics) -->
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px;">
          <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #7c3aed; text-transform: uppercase; margin-bottom: 8px;">Key Definitions &amp; Hardware Terminology</div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; font-size: 0.83rem; color: #334155;">
            <div>
              <strong style="color: #0284c7; font-family: var(--font-mono);">CR3 Register</strong>
              <div style="color: #64748b; margin-top: 2px;">Processor root register storing the physical base address of the current process top-level page table (PML4).</div>
            </div>
            <div>
              <strong style="color: #0284c7; font-family: var(--font-mono);">CR4 Register</strong>
              <div style="color: #64748b; margin-top: 2px;">Extended control register enabling PAE, page size extensions, and virtualization features.</div>
            </div>
            <div>
              <strong style="color: #0284c7; font-family: var(--font-mono);">PML4 Table</strong>
              <div style="color: #64748b; margin-top: 2px;">Top-level 4 KiB table in x86-64 4-level paging containing entries pointing to PDPTs.</div>
            </div>
            <div>
              <strong style="color: #059669; font-family: var(--font-mono);">PTE (Page Table Entry)</strong>
              <div style="color: #64748b; margin-top: 2px;">Leaf entry in a page table containing the physical frame number (PFN) and protection flags.</div>
            </div>
          </div>
        </div>"""

    # Replace old analytical panes block with the new layout placing definitions underneath
    old_panes_block = """        <!-- Paired Analytical Panes -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0284c7; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #0284c7; text-transform: uppercase; letter-spacing: 0.03em;">Detailed Mechanics: What Is Happening</div>
            <div id="trans-desc-what" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>

          <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #10b981; padding: 16px; border-radius: 0 6px 6px 0;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 0.03em;">Why The System Does This</div>
            <div id="trans-desc-why" style="font-size: 0.9rem; color: #1e293b; line-height: 1.55; margin-top: 8px;"></div>
          </div>
        </div>"""

    if old_panes_block in content:
        content = content.replace(old_panes_block, definitions_under_mechanics)
        print("--> Successfully moved Key Definitions underneath Detailed Mechanics analytical panes.")
    else:
        print("--> Warning: Analytical panes block not found exact; performing structural check.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Move Key Definitions under Detailed Mechanics and repair walkthrough\n\n"
            "Relocate the Key Definitions glossary box underneath the analytical panes\n"
            "and ensure proper DOM event binding in 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for definitions layout & repair!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    repair_and_fix_layout()
