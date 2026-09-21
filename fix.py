#!/usr/bin/env python3
# =====================================================================
# fix.py: Add PFN definition to hardware terminology glossary
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def add_pfn_definition():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Old glossary card HTML block without PFN definition card
    old_glossary = """          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-size: 0.83rem; color: #334155;">
            <div>
              <strong style="color: #0284c7; font-family: var(--font-mono);">Root Register</strong>
              <div style="color: #64748b; margin-top: 2px;">The top-level CPU architectural pointer (such as CR3 on x86 or TTBR0 on ARM) anchoring the execution context by storing the physical base address of the active process's top-level translation table.</div>
            </div>
            <div>
              <strong style="color: #0284c7; font-family: var(--font-mono);">CR3 Register</strong>
              <div style="color: #64748b; margin-top: 2px;">The specific x86 root register storing the physical base address of the top-level page table (PML4).</div>
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
          </div>"""

    # Updated glossary card HTML including PFN definition
    new_glossary = """          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-size: 0.83rem; color: #334155;">
            <div>
              <strong style="color: #0284c7; font-family: var(--font-mono);">Root Register</strong>
              <div style="color: #64748b; margin-top: 2px;">The top-level CPU architectural pointer (such as CR3 on x86 or TTBR0 on ARM) anchoring the execution context by storing the physical base address of the active process's top-level translation table.</div>
            </div>
            <div>
              <strong style="color: #0284c7; font-family: var(--font-mono);">CR3 Register</strong>
              <div style="color: #64748b; margin-top: 2px;">The specific x86 root register storing the physical base address of the top-level page table (PML4).</div>
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
              <strong style="color: #059669; font-family: var(--font-mono);">PFN (Physical Frame Number)</strong>
              <div style="color: #64748b; margin-top: 2px;">The upper address bits of a physical memory address identifying a specific 4 KiB page frame in DRAM; combined with the page offset during translation.</div>
            </div>
            <div>
              <strong style="color: #059669; font-family: var(--font-mono);">PTE (Page Table Entry)</strong>
              <div style="color: #64748b; margin-top: 2px;">Leaf entry containing the physical frame number (PFN) and protection flags.</div>
            </div>
          </div>"""

    if old_glossary in content:
        content = content.replace(old_glossary, new_glossary)
        print("--> Added PFN definition to the hardware glossary card.")
    else:
        print("--> Warning: Glossary grid pattern not matched exactly.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add PFN definition to translation simulator key definitions glossary\n\n"
            "Define 'PFN (Physical Frame Number)' in the hardware terminology card\n"
            "within 02-hardware-review.html to explain physical frame identification."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for PFN addition!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    add_pfn_definition()
