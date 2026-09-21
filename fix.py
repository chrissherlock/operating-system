#!/usr/bin/env python3
# =====================================================================
# fix.py: Populate missing inlinePreview properties for 2m and swap modes
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def fix_undefined_previews():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Old 2m and swap arrays without inlinePreview keys
    old_2m_array = """            "2m": [
              {
                step: "Superpage Step 1: CR3 to PML4", phase: "1. CR3 Root Lookup", va: "0x00400000 (2MB)", vpn: "Superpage Root", offset: "0x000", pfn: "Pending...", pa: "Pending...",
                activeNodes: ["trans-node-cr3", "trans-node-pml4"], activePaths: ["trans-path-1"], bypassActive: false,
                consoleTop: "2 MiB SUPERPAGE WALK • STEP 1",
                what: "The MMU checks PML4 for a 2 MiB superpage mapping.",
                why: "Superpages reduce TLB pressure for large memory-intensive applications."
              },
              {
                step: "Superpage Step 2: Direct PDE Mapping", phase: "2. Direct Superpage Resolution", va: "0x00400000 (2MB)", vpn: "PDE Superpage Entry", offset: "0x000 (21 bits)", pfn: "0x04000 (2MB)", pa: "0x08000000",
                activeNodes: ["trans-node-pdpt", "trans-node-pd"], activePaths: ["trans-path-2", "trans-path-3"], bypassActive: true,
                consoleTop: "2 MiB SUPERPAGE WALK • STEP 2 (COMPLETE)",
                what: "The Page Directory Entry maps directly to a massive 2 MiB physical DRAM frame.",
                why: "Stopping the page walk early at Level 2 maximizes TLB efficiency."
              }
            ],
            "swap": [
              {
                step: "Swap Step 1: Page Table Walk to Swapped PTE", phase: "1. Swapped PTE Located", va: "0x00705020", vpn: "VPN 0x00705", offset: "0x020", pfn: "None (Present=0)", pa: "Page Fault!",
                activeNodes: ["trans-node-cr3", "trans-node-pml4", "trans-node-pdpt", "trans-node-pd", "trans-node-pt"], activePaths: ["trans-path-1", "trans-path-2", "trans-path-3", "trans-path-4"], bypassActive: false,
                consoleTop: "SWAPPED PAGE FAULT WALK • STEP 1",
                what: "The MMU completes the page table walk but discovers Present Bit = 0 in the leaf PTE.",
                why: "Demand paging allows systems to overcommit physical RAM by evicting inactive pages to disk."
              },
              {
                step: "Swap Step 2: Kernel Frame Allocation & Swap-In", phase: "2. Kernel Fault Resolution", va: "0x00705020", vpn: "VPN 0x00705", offset: "0x020", pfn: "0x09840", pa: "0x09840020",
                activeNodes: ["trans-node-pt"], activePaths: [], bypassActive: true,
                consoleTop: "SWAPPED PAGE FAULT WALK • STEP 2 (COMPLETE)",
                what: "The CPU traps into the page fault handler. The OS allocates frame 0x09840 and reads swap data.",
                why: "The application resumes execution seamlessly, unaware its memory page was on disk."
              }
            ]"""

    # Updated 2m and swap arrays including explicit inlinePreview fields
    new_2m_array = """            "2m": [
              {
                step: "Superpage Step 1: CR3 to PML4", phase: "1. CR3 Root Lookup", va: "0x00400000 (2MB)", vpn: "Superpage Root", offset: "0x000", pfn: "Pending...", pa: "Pending...",
                activeNodes: ["trans-node-cr3", "trans-node-pml4"], activePaths: ["trans-path-1"], bypassActive: false,
                consoleTop: "2 MiB SUPERPAGE WALK • STEP 1",
                inlinePreview: "The MMU queries the top-level PML4 table, checking for superpage flags before descending further into the table hierarchy.",
                what: "The MMU checks PML4 for a 2 MiB superpage mapping.",
                why: "Superpages reduce TLB pressure for large memory-intensive applications."
              },
              {
                step: "Superpage Step 2: Direct PDE Mapping", phase: "2. Direct Superpage Resolution", va: "0x00400000 (2MB)", vpn: "PDE Superpage Entry", offset: "0x000 (21 bits)", pfn: "0x04000 (2MB)", pa: "0x08000000",
                activeNodes: ["trans-node-pdpt", "trans-node-pd"], activePaths: ["trans-path-2", "trans-path-3"], bypassActive: true,
                consoleTop: "2 MiB SUPERPAGE WALK • STEP 2 (COMPLETE)",
                inlinePreview: "The Page Directory Entry asserts a 2 MiB superpage flag, bypassing lower page tables entirely and mapping straight to physical frame 0x04000.",
                what: "The Page Directory Entry maps directly to a massive 2 MiB physical DRAM frame.",
                why: "Stopping the page walk early at Level 2 maximizes TLB efficiency."
              }
            ],
            "swap": [
              {
                step: "Swap Step 1: Page Table Walk to Swapped PTE", phase: "1. Swapped PTE Located", va: "0x00705020", vpn: "VPN 0x00705", offset: "0x020", pfn: "None (Present=0)", pa: "Page Fault!",
                activeNodes: ["trans-node-cr3", "trans-node-pml4", "trans-node-pdpt", "trans-node-pd", "trans-node-pt"], activePaths: ["trans-path-1", "trans-path-2", "trans-path-3", "trans-path-4"], bypassActive: false,
                consoleTop: "SWAPPED PAGE FAULT WALK • STEP 1",
                inlinePreview: "The page table walk completes, but the leaf PTE reports Present Bit = 0, triggering an immediate hardware page fault trap to the kernel.",
                what: "The MMU completes the page table walk but discovers Present Bit = 0 in the leaf PTE.",
                why: "Demand paging allows systems to overcommit physical RAM by evicting inactive pages to disk."
              },
              {
                step: "Swap Step 2: Kernel Frame Allocation & Swap-In", phase: "2. Kernel Fault Resolution", va: "0x00705020", vpn: "VPN 0x00705", offset: "0x020", pfn: "0x09840", pa: "0x09840020",
                activeNodes: ["trans-node-pt"], activePaths: [], bypassActive: true,
                consoleTop: "SWAPPED PAGE FAULT WALK • STEP 2 (COMPLETE)",
                inlinePreview: "The kernel allocates a free physical frame (0x09840), reads the swapped page from disk into DRAM, updates the PTE, and restarts the instruction.",
                what: "The CPU traps into the page fault handler. The OS allocates frame 0x09840 and reads swap data.",
                why: "The application resumes execution seamlessly, unaware its memory page was on disk."
              }
            ]"""

    if old_2m_array in content:
        content = content.replace(old_2m_array, new_2m_array)
        print("--> Added inlinePreview text strings to 2m and swap modes.")
    else:
        print("--> Warning: 2m and swap arrays pattern not matched exact.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix undefined inlinePreview bugs across 2m and swap modes in Module 2\n\n"
            "Add missing inlinePreview text strings to the 2 MiB and swap storyline arrays\n"
            "within 02-hardware-review.html to prevent rendering 'undefined'."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for undefined preview bugfix!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    fix_undefined_previews()
