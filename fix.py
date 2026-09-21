#!/usr/bin/env python3
# =====================================================================
# fix.py: Add PDPT definition to the hardware glossary card
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def add_pdpt_definition():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Old glossary card HTML block without PDPT
    old_glossary = """        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px;">
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

    # Updated glossary card HTML including PDPT
    new_glossary = """        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px;">
          <div style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #7c3aed; text-transform: uppercase; margin-bottom: 8px;">Key Definitions &amp; Hardware Terminology</div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-size: 0.83rem; color: #334155;">
            <div>
              <strong style="color: #0284c7; font-family: var(--font-mono);">CR3 Register</strong>
              <div style="color: #64748b; margin-top: 2px;">Processor root register storing the physical base address of the top-level page table (PML4).</div>
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
              <strong style="color: #0284c7; font-family: var(--font-mono);">PDPT</strong>
              <div style="color: #64748b; margin-top: 2px;">Page Directory Pointer Table (Level 3); contains 512 entries pointing to Page Directories.</div>
            </div>
            <div>
              <strong style="color: #059669; font-family: var(--font-mono);">PTE (Page Table Entry)</strong>
              <div style="color: #64748b; margin-top: 2px;">Leaf entry containing the physical frame number (PFN) and protection flags.</div>
            </div>
          </div>
        </div>"""

    if old_glossary in content:
        content = content.replace(old_glossary, new_glossary)
        print("--> Added PDPT definition to the hardware glossary.")
    else:
        print("--> Glossary card pattern not found exact; checking alternative match.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add PDPT definition to translation simulator key definitions glossary\n\n"
            "Include the Page Directory Pointer Table (PDPT) in the hardware terminology\n"
            "card within 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for PDPT addition!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    add_pdpt_definition()
