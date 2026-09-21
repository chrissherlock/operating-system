#!/usr/bin/env python3
# =====================================================================
# fix.py: Refine translation simulator narrative to remove meta-talk
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def refine_pure_narrative():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Pure narrative replacement for the 4k translation steps
    old_4k_array = """            "4k": [
              {
                step: "Step 1: CR3 Root Lookup & PML4 Table", phase: "1. CR3 &rarr; PML4 Lookup", va: "0x00403018", vpn: "CR3 Root Lookup", offset: "0x018", pfn: "Pending...", pa: "Pending...",
                activeNodes: ["trans-node-cr3", "trans-node-pml4"], activePaths: ["trans-path-1"], bypassActive: false,
                consoleTop: "TRANSLATION STEP 1 • CR3 ROOT REGISTER TO PML4 TABLE",
                inlinePreview: "<strong>Chapter 1 -- Unlocking the Vault:</strong> The CPU's CR3 register presents the physical base address of the active process table. <em>Next plot point:</em> Indexing into the PML4 table to locate the PDPT base. Click Next to advance.",
                what: "The MMU reads the root page table physical address 0x1A4000 from control register CR3. It indexes into the top-level PML4 table.",
                why: "CR3 anchors the process's complete virtual address space, ensuring complete memory isolation."
              },
              {
                step: "Step 2: PDPT Table Traversal", phase: "2. PML4 &rarr; PDPT Traversal", va: "0x00403018", vpn: "PDPT Indexing", offset: "0x018", pfn: "Pending...", pa: "Pending...",
                activeNodes: ["trans-node-pml4", "trans-node-pdpt"], activePaths: ["trans-path-2"], bypassActive: false,
                consoleTop: "TRANSLATION STEP 2 • PML4 ENTRY TO PDPT TABLE",
                inlinePreview: "<strong>Chapter 2 -- Traversing the Directory Pointer:</strong> The MMU accesses the PDPT in DRAM using upper virtual bits. <em>Next plot point:</em> Resolving the Page Directory entry. Click Next to advance.",
                what: "Using the address found in PML4, the MMU accesses the PDPT in DRAM, selecting Entry 3.",
                why: "Multi-level hierarchies allow operating systems to omit unused memory regions entirely."
              },
              {
                step: "Step 3: Page Directory Traversal", phase: "3. PDPT &rarr; Page Directory", va: "0x00403018", vpn: "Page Directory Indexing", offset: "0x018", pfn: "Pending...", pa: "Pending...",
                activeNodes: ["trans-node-pdpt", "trans-node-pd"], activePaths: ["trans-path-3"], bypassActive: false,
                consoleTop: "TRANSLATION STEP 3 • PDPT ENTRY TO PAGE DIRECTORY",
                inlinePreview: "<strong>Chapter 3 -- Entering the Page Directory:</strong> The hardware inspects the Page Directory to find the exact Page Table base. <em>Next plot point:</em> Locating the leaf Page Table Entry (PTE). Click Next to advance.",
                what: "The MMU accesses the Page Directory in DRAM, reading Entry 3 which points to the Page Table.",
                why: "Staging memory lookups keeps individual page tables compact (4 KiB per table)."
              },
              {
                step: "Step 4: Page Table Leaf Resolution", phase: "4. Page Directory &rarr; Page Table Leaf", va: "0x00403018", vpn: "VPN 0x00403 Resolved", offset: "0x018", pfn: "0x07B40", pa: "0x07B40018",
                activeNodes: ["trans-node-pd", "trans-node-pt"], activePaths: ["trans-path-4"], bypassActive: true,
                consoleTop: "TRANSLATION STEP 4 • PAGE TABLE LEAF PTE RESOLUTION",
                inlinePreview: "<strong>Chapter 4 -- Reaching the Leaf PTE:</strong> The MMU reads the leaf Page Table Entry, extracting Physical Frame Number 0x07B40. <em>Next plot point:</em> Combining PFN with the unmodified page offset. Click Next to advance.",
                what: "The MMU reads the final Page Table, indexing VPN 0x00403 to yield Physical Frame Number 0x07B40.",
                why: "The leaf PTE encodes permission metadata alongside the physical frame number."
              },
              {
                step: "Step 5: Offset Pass-Through & Assembly", phase: "5. Physical Address Assembled", va: "0x00403018", vpn: "VPN 0x00403", offset: "0x018 (Unmodified)", pfn: "0x07B40", pa: "0x07B40018 (Complete)",
                activeNodes: ["trans-node-pt"], activePaths: [], bypassActive: true,
                consoleTop: "TRANSLATION STEP 5 • OFFSET PASS-THROUGH & DRAM BUS ISSUE",
                inlinePreview: "<strong>Chapter 5 -- Reaching Destination DRAM:</strong> The page offset 0x018 passes through untouched, yielding final address 0x07B40018. <em>Next plot point:</em> Walkthrough complete! Click Restart or switch granularity.",
                what: "The lowest 12 bits (0x018) pass through unmodified, combining with PFN 0x07B40000 to issue 0x07B40018.",
                why: "Intra-page byte offsets remain 100% identical in physical memory."
              }
            ],"""

    new_4k_array = """            "4k": [
              {
                step: "Step 1: CR3 Root Lookup & PML4 Table", phase: "1. CR3 &rarr; PML4 Lookup", va: "0x00403018", vpn: "CR3 Root Lookup", offset: "0x018", pfn: "Pending...", pa: "Pending...",
                activeNodes: ["trans-node-cr3", "trans-node-pml4"], activePaths: ["trans-path-1"], bypassActive: false,
                consoleTop: "TRANSLATION STEP 1 • CR3 ROOT REGISTER TO PML4 TABLE",
                inlinePreview: "The processor's root register, CR3, presents the physical base address of the active process table, allowing the MMU to index directly into the top-level PML4 table.",
                what: "The MMU reads the root page table physical address 0x1A4000 from control register CR3. It indexes into the top-level PML4 table.",
                why: "CR3 anchors the process's complete virtual address space, ensuring complete memory isolation."
              },
              {
                step: "Step 2: PDPT Table Traversal", phase: "2. PML4 &rarr; PDPT Traversal", va: "0x00403018", vpn: "PDPT Indexing", offset: "0x018", pfn: "Pending...", pa: "Pending...",
                activeNodes: ["trans-node-pml4", "trans-node-pdpt"], activePaths: ["trans-path-2"], bypassActive: false,
                consoleTop: "TRANSLATION STEP 2 • PML4 ENTRY TO PDPT TABLE",
                inlinePreview: "Using the upper bits of the virtual address, the MMU traverses into the Page Directory Pointer Table residing in DRAM to locate the next hierarchical layer.",
                what: "Using the address found in PML4, the MMU accesses the PDPT in DRAM, selecting Entry 3.",
                why: "Multi-level hierarchies allow operating systems to omit unused memory regions entirely."
              },
              {
                step: "Step 3: Page Directory Traversal", phase: "3. PDPT &rarr; Page Directory", va: "0x00403018", vpn: "Page Directory Indexing", offset: "0x018", pfn: "Pending...", pa: "Pending...",
                activeNodes: ["trans-node-pdpt", "trans-node-pd"], activePaths: ["trans-path-3"], bypassActive: false,
                consoleTop: "TRANSLATION STEP 3 • PDPT ENTRY TO PAGE DIRECTORY",
                inlinePreview: "The hardware inspects the Page Directory in DRAM, resolving the specific entry that points directly to the base of the Page Table.",
                what: "The MMU accesses the Page Directory in DRAM, reading Entry 3 which points to the Page Table.",
                why: "Staging memory lookups keeps individual page tables compact (4 KiB per table)."
              },
              {
                step: "Step 4: Page Table Leaf Resolution", phase: "4. Page Directory &rarr; Page Table Leaf", va: "0x00403018", vpn: "VPN 0x00403 Resolved", offset: "0x018", pfn: "0x07B40", pa: "0x07B40018",
                activeNodes: ["trans-node-pd", "trans-node-pt"], activePaths: ["trans-path-4"], bypassActive: true,
                consoleTop: "TRANSLATION STEP 4 • PAGE TABLE LEAF PTE RESOLUTION",
                inlinePreview: "The MMU reaches the leaf Page Table Entry (PTE), reading the physical frame number (PFN) and validating permission flags.",
                what: "The MMU reads the final Page Table, indexing VPN 0x00403 to yield Physical Frame Number 0x07B40.",
                why: "The leaf PTE encodes permission metadata alongside the physical frame number."
              },
              {
                step: "Step 5: Offset Pass-Through & Assembly", phase: "5. Physical Address Assembled", va: "0x00403018", vpn: "VPN 0x00403", offset: "0x018 (Unmodified)", pfn: "0x07B40", pa: "0x07B40018 (Complete)",
                activeNodes: ["trans-node-pt"], activePaths: [], bypassActive: true,
                consoleTop: "TRANSLATION STEP 5 • OFFSET PASS-THROUGH & DRAM BUS ISSUE",
                inlinePreview: "The lower 12 bits (the page offset) bypass translation completely and combine with the resolved PFN, issuing the final physical address to DRAM.",
                what: "The lowest 12 bits (0x018) pass through unmodified, combining with PFN 0x07B40000 to issue 0x07B40018.",
                why: "Intra-page byte offsets remain 100% identical in physical memory."
              }
            ],"""

    if old_4k_array in content:
        content = content.replace(old_4k_array, new_4k_array)
        print("--> Refined translation steps into a clean narrative story.")
    else:
        print("--> Warning: 4k array pattern not matched exact.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Refine translation simulator narrative to remove meta-talk\n\n"
            "Replace mechanical plot points in 02-hardware-review.html with a pure,\n"
            "uninterrupted narrative explaining the virtual memory translation journey."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for pure narrative refinement!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    refine_pure_narrative()
