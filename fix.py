#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Multi-Level Hierarchical Page Tables in Module 03
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week07-memory-management-virtual-memory",
    "03-virtual-memory-paging-tables.html"
)

EXPANDED_MULTILEVEL_SECTION = r"""      <h3>4. Multi-Level Hierarchical Page Tables</h3>
      <p>
        While simple single-level paging successfully eliminates external memory fragmentation, it introduces a severe secondary challenge: <strong>the scaling crisis of page table memory overhead</strong>.
      </p>

      <h4>1. The Linear Page Table Scaling Crisis</h4>
      <p>
        In a flat (single-level) paging design, the operating system maintains a single monolithic array where every possible virtual page number corresponds to a contiguous slot in physical RAM.
      </p>

      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--danger);">
        <strong style="color: var(--danger);">The 32-Bit Linear Table Footprint:</strong>
        <br><br>
        On a 32-bit processor ($2^{32}\text{ bytes} = 4\text{ GB}$ address space) with 4 KB ($2^{12}\text{ bytes}$) pages:
        $$ \text{Total Virtual Pages} = \frac{2^{32}}{2^{12}} = 2^{20} = 1{,}048{,}576\text{ pages} $$
        $$ \text{Page Table Size} = 2^{20}\text{ entries} \times 4\text{ bytes per PTE} = 4\text{ MB per process} $$
        <p style="margin: 8px 0 0 0; font-size: 0.88rem; color: var(--text);">
          If a system runs $100$ concurrent processes, $400\text{ MB}$ of physical RAM is consumed solely by page table metadata. Crucially, each 4 MB table must be stored in <strong>strictly contiguous physical memory</strong> so the MMU can perform simple array index lookups ($Base + p \times 4$), re-introducing the contiguous allocation problem.
        </p>
      </div>

      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--danger);">
        <strong style="color: var(--danger);">The 64-Bit Mathematical Impossibility:</strong>
        <br><br>
        On modern 64-bit architectures ($2^{64}\text{ bytes}$ address space) with 4 KB pages and 8-byte PTEs:
        $$ \text{Total Virtual Pages} = \frac{2^{64}}{2^{12}} = 2^{52} \approx 4.5 \times 10^{15}\text{ pages} $$
        $$ \text{Page Table Size} = 2^{52}\text{ entries} \times 8\text{ bytes} = 2^{55}\text{ bytes} = 33{,}554{,}432\text{ GB} = 33{,}554\text{ TB} \approx 33\text{ Petabytes!} $$
        <p style="margin: 8px 0 0 0; font-size: 0.88rem; color: var(--text);">
          Allocating a flat page table for a single 64-bit process would require millions of times more RAM than exists on entire enterprise servers.
        </p>
      </div>

      <h4>2. The Principle of Address Space Sparsity</h4>
      <p>
        The reason flat linear page tables are so catastrophically wasteful is that real-world programs exhibit extreme <strong>address space sparsity</strong>.
      </p>
      <p>
        A typical user application does not populate 4 GB or 16 Exabytes of memory continuously. Instead, its virtual layout consists of three small, isolated clusters:
      </p>
      <ul>
        <li><strong>Text &amp; Data Segments:</strong> A few megabytes mapped at low virtual memory.</li>
        <li><strong>Heap:</strong> Begins just above data and grows dynamically upward.</li>
        <li><strong>User Stack:</strong> Begins at high virtual memory and grows dynamically downward.</li>
      </ul>
      <p>
        The vast chasm between the top of the heap and the bottom of the stack—often spanning hundreds of gigabytes or terabytes—is completely empty and unmapped. A flat page table wastes over $99.9\%$ of its entries storing invalid PTEs ($P = 0$) for memory addresses the program never touches.
      </p>

      <h4>3. Two-Level Hierarchical Paging (32-Bit Systems)</h4>
      <p>
        To eliminate the storage overhead of unmapped address space, modern operating systems <strong>page the page table itself</strong>. In a two-level hierarchical paging scheme, the monolithic page table is broken into thousands of distinct 4 KB pages, coordinated by a top-level table called the <strong>Page Directory</strong>.
      </p>

      <h5>Address Bit Decomposition (10-10-12 Scheme)</h5>
      <p>
        A 32-bit virtual address is partitioned into three discrete fields:
      </p>
      <div style="background: #0f172a; color: #f8fafc; border-radius: 8px; padding: 18px; font-family: var(--font-mono); font-size: 0.88rem; margin: 16px 0; text-align: center;">
        Virtual Address (32b) = [ <span style="color: #38bdf8;">PDI (10 bits)</span> | <span style="color: #fbbf24;">PTI (10 bits)</span> | <span style="color: #6ee7b7;">Offset d (12 bits)</span> ]
      </div>
      <ul>
        <li>
          <strong>Page Directory Index (PDI, bits 31–22, 10 bits):</strong> Selects one of $2^{10} = 1024$ entries in the Page Directory. Each Page Directory Entry (PDE) contains the physical base frame of a second-level Page Table.
        </li>
        <li>
          <strong>Page Table Index (PTI, bits 21–12, 10 bits):</strong> Selects one of $2^{10} = 1024$ entries within the designated second-level Page Table. Each Page Table Entry (PTE) contains the physical frame number ($f$) of the actual data page in RAM.
        </li>
        <li>
          <strong>Byte Offset ($d$, bits 11–0, 12 bits):</strong> Addresses the specific byte within the 4 KB page ($2^{12} = 4096\text{ bytes}$).
        </li>
      </ul>

      <h5>How Hierarchical Paging Saves Memory</h5>
      <p>
        The architectural brilliance of multi-level paging lies in conditional allocation:
      </p>
      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--accent);">
        <strong style="color: var(--primary);">Conditional Sub-Tree Pruning:</strong>
        <br><br>
        If a $4\text{ MB}$ region of virtual memory contains no allocated pages, the corresponding Page Directory Entry is marked $\text{Present} = 0$.
        $$ \text{PDE.Present} = 0 \implies \text{Second-Level Page Table is NOT Allocated in RAM} $$
      </div>
      <p>
        Consider a minimal 32-bit program requiring only $12\text{ KB}$ of memory (one 4 KB page for code, one for data, one for stack):
      </p>
      <ul>
        <li><strong>Page Directory:</strong> Exactly one 4 KB frame ($1024\text{ entries} \times 4\text{ bytes} = 4\text{ KB}$). Always resident.</li>
        <li><strong>Low Memory Page Table:</strong> One 4 KB frame covering code and data (maps $0 \dots 4\text{ MB}$).</li>
        <li><strong>High Memory Page Table:</strong> One 4 KB frame covering the stack (maps top $4\text{ MB}$).</li>
        <li><strong>Remaining 1022 Page Tables:</strong> Never allocated! Marked $P = 0$ in the directory.</li>
      </ul>
      <p>
        Total memory consumed for page tables: $4\text{ KB} + 4\text{ KB} + 4\text{ KB} = \mathbf{12\text{ KB}}$, compared to $4096\text{ KB}$ ($4\text{ MB}$) for a flat table—a <strong>$99.7\%$ memory savings</strong>!
      </p>

      <h4>4. x86-64 4-Level Paging Architecture (IA-32e / Long Mode)</h4>
      <p>
        On modern 64-bit x86-64 processors, the hierarchical paging model is extended to four discrete levels. While pointers in x86-64 are 64 bits wide, current processor hardware implements a <strong>48-bit canonical virtual address space</strong> (capable of addressing 256 Terabytes).
      </p>

      <h5>Canonical Address Sign Extension</h5>
      <p>
        In a 48-bit virtual address, bits 47 through 0 define the address space, while bits 63 through 48 must be an identical copy of bit 47 (sign-extension rule):
      </p>
      <ul>
        <li><strong>User Space (Bit 47 = 0):</strong> Canonical range from <code>0x0000_0000_0000_0000</code> to <code>0x0000_7FFF_FFFF_FFFF</code> (lower 128 TB).</li>
        <li><strong>Kernel Space (Bit 47 = 1):</strong> Canonical range from <code>0xFFFF_8000_0000_0000</code> to <code>0xFFFF_FFFF_FFFF_FFFF</code> (upper 128 TB).</li>
        <li><strong>Non-Canonical Hole:</strong> Any address with mismatched upper bits generates a General Protection Fault (<code>#GP</code>).</li>
      </ul>

      <h5>The 9-9-9-9-12 Bit Decomposition</h5>
      <p>
        Because each Page Table Entry in 64-bit mode is 8 bytes wide, a single 4 KB page frame holds exactly $4096 / 8 = 512 = 2^9$ entries. Consequently, every level of the hierarchy indexes exactly <strong>9 bits</strong>:
      </p>

      <div style="background: #0f172a; color: #f8fafc; border-radius: 8px; padding: 18px; font-family: var(--font-mono); font-size: 0.85rem; margin: 16px 0; overflow-x: auto;">
        <div style="display: flex; gap: 6px; min-width: 650px; text-align: center;">
          <div style="flex: 1.2; background: #1e293b; padding: 8px; border-radius: 4px; border: 1px solid #38bdf8;">
            <div style="color: #38bdf8; font-weight: bold;">PML4</div>
            <div style="color: #94a3b8; font-size: 0.72rem;">Bits 47–39 (9b)</div>
            <div style="color: #e2e8f0; font-size: 0.72rem;">512 entries (512 GB each)</div>
          </div>
          <div style="flex: 1.2; background: #1e293b; padding: 8px; border-radius: 4px; border: 1px solid #818cf8;">
            <div style="color: #818cf8; font-weight: bold;">PDPT</div>
            <div style="color: #94a3b8; font-size: 0.72rem;">Bits 38–30 (9b)</div>
            <div style="color: #e2e8f0; font-size: 0.72rem;">512 entries (1 GB each)</div>
          </div>
          <div style="flex: 1.2; background: #1e293b; padding: 8px; border-radius: 4px; border: 1px solid #fbbf24;">
            <div style="color: #fbbf24; font-weight: bold;">PD</div>
            <div style="color: #94a3b8; font-size: 0.72rem;">Bits 29–21 (9b)</div>
            <div style="color: #e2e8f0; font-size: 0.72rem;">512 entries (2 MB each)</div>
          </div>
          <div style="flex: 1.2; background: #1e293b; padding: 8px; border-radius: 4px; border: 1px solid #34d399;">
            <div style="color: #34d399; font-weight: bold;">PT</div>
            <div style="color: #94a3b8; font-size: 0.72rem;">Bits 20–12 (9b)</div>
            <div style="color: #e2e8f0; font-size: 0.72rem;">512 entries (4 KB each)</div>
          </div>
          <div style="flex: 1; background: #1e293b; padding: 8px; border-radius: 4px; border: 1px solid #f43f5e;">
            <div style="color: #f43f5e; font-weight: bold;">Offset</div>
            <div style="color: #94a3b8; font-size: 0.72rem;">Bits 11–0 (12b)</div>
            <div style="color: #e2e8f0; font-size: 0.72rem;">4096 bytes</div>
          </div>
        </div>
      </div>

      <h5>The Hardware Table Walk Sequence</h5>
      <p>
        The CPU control register <strong><code>CR3</code></strong> stores the physical base address of the active process's root PML4 table. When translating address $VA$, the hardware MMU executes the following sequential steps:
      </p>
      <ol style="font-size: 0.92rem; line-height: 1.7;">
        <li>
          <strong>PML4 Lookup:</strong> Load entry at physical address $\text{CR3} + (\text{PML4\_Index} \times 8)$. If $P = 0$, raise Page Fault. Extract base address of PDPT.
        </li>
        <li>
          <strong>PDPT Lookup:</strong> Load entry at physical address $\text{PDPT\_Base} + (\text{PDPT\_Index} \times 8)$. If $P = 0$, raise Page Fault. Extract base address of PD.
        </li>
        <li>
          <strong>PD Lookup:</strong> Load entry at physical address $\text{PD\_Base} + (\text{PD\_Index} \times 8)$. If $P = 0$, raise Page Fault. Extract base address of PT.
        </li>
        <li>
          <strong>PT Lookup:</strong> Load entry at physical address $\text{PT\_Base} + (\text{PT\_Index} \times 8)$. If $P = 0$, raise Page Fault. Extract Physical Frame Number ($f$).
        </li>
        <li>
          <strong>Physical Address Assembly:</strong> Compute final physical address $\text{PA} = (f \ll 12) \mid \text{Offset}$.
        </li>
      </ol>

      <h4>5. Large Pages &amp; Huge Pages (Page Size Extensions)</h4>
      <p>
        Traversing four levels of page tables adds significant overhead. For database engines, virtual machine hypervisors (KVM), and scientific simulations with massive memory footprints, standard 4 KB pages cause severe TLB cache thrashing.
      </p>
      <p>
        Modern processors allow the MMU to terminate the tree walk early by setting the <strong>Page Size (PS) bit</strong> (bit 7) in intermediate table entries:
      </p>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
        <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 18px;">
          <strong style="color: var(--primary); font-size: 0.98rem;">2 MB Huge Pages (x86-64)</strong>
          <p style="font-size: 0.86rem; color: var(--text); margin-top: 8px; line-height: 1.5;">
            By setting the <strong>PS bit</strong> in a Page Directory (PD) entry, the PD entry points directly to a contiguous <strong>2 MB physical frame</strong>, completely bypassing the fourth-level Page Table (PT).
          </p>
          <div class="math-callout" style="margin: 10px 0 0 0; padding: 10px; font-size: 0.82rem;">
            Offset expands from 12 bits to 21 bits ($2^{21} = 2\text{ MB}$).
            <br>
            Virtual Address: 9b PML4 + 9b PDPT + 9b PD + 21b Offset.
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 8px;">
            A single TLB entry now maps 2 MB instead of 4 KB ($512\times$ greater cache coverage).
          </p>
        </div>

        <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 18px;">
          <strong style="color: var(--primary); font-size: 0.98rem;">1 GB Giant Pages (x86-64)</strong>
          <p style="font-size: 0.86rem; color: var(--text); margin-top: 8px; line-height: 1.5;">
            By setting the <strong>PS bit</strong> in a Page Directory Pointer Table (PDPT) entry, the entry points directly to a contiguous <strong>1 GB physical frame</strong>, bypassing both the PD and PT levels.
          </p>
          <div class="math-callout" style="margin: 10px 0 0 0; padding: 10px; font-size: 0.82rem;">
            Offset expands from 12 bits to 30 bits ($2^{30} = 1\text{ GB}$).
            <br>
            Virtual Address: 9b PML4 + 9b PDPT + 30b Offset.
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 8px;">
            Enables hypervisors to map hundreds of gigabytes of guest physical memory with negligible TLB misses.
          </p>
        </div>
      </div>

      <h4>6. Modern Scaling: 5-Level Paging (Paging57)</h4>
      <p>
        With high-performance cloud servers deploying hundreds of terabytes of physical memory, the 48-bit canonical limit (256 TB virtual space) has become an architectural bottleneck.
      </p>
      <p>
        Modern processors (Intel Ice Lake and newer, AMD Zen 4) introduce <strong>5-Level Paging (Paging57)</strong>:
      </p>
      <ul>
        <li>Expands the canonical virtual address from 48 bits to <strong>57 bits</strong> ($2^{57} = 128\text{ Petabytes}$).</li>
        <li>Introduces a fifth root level called <strong>PML5</strong> (bits 56–48, 9 bits).</li>
        <li>The full tree walk requires <strong>5 sequential memory accesses</strong>: PML5 &rarr; PML4 &rarr; PDPT &rarr; PD &rarr; PT &rarr; Physical Data.</li>
      </ul>

      <h4>7. The Memory Amplification Penalty &amp; The TLB Imperative</h4>
      <p>
        Hierarchical paging brilliantly solves the memory storage scaling crisis, but it introduces a severe hardware performance bottleneck:
      </p>

      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--danger);">
        <strong style="color: var(--danger);">The Memory Amplification Penalty:</strong>
        <br><br>
        In a 4-level paging system, fetching a single 8-byte variable from RAM requires:
        $$ 4 \text{ (Page Table Traversal Reads)} + 1 \text{ (Actual Data Read)} = \mathbf{5 \text{ Memory Access Cycles}} $$
        <p style="margin: 8px 0 0 0; font-size: 0.88rem; color: var(--text);">
          If a physical RAM access takes 50 nanoseconds, a simple memory read would take $250\text{ ns}$—a catastrophic <strong>$400\%$ hardware slowdown</strong> on every memory instruction.
        </p>
      </div>

      <p>
        Without specialized hardware caching, modern multi-level virtual memory would be unacceptably slow. In <strong>Module 04</strong>, we examine the critical hardware component that restores near-zero-latency translation: the <strong>Translation Lookaside Buffer (TLB)</strong>.
      </p>"""

def update_multilevel_section():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "      <h3>4. Multi-Level Hierarchical Page Tables</h3>"
    end_marker = "</div>\n\n    <nav class=\"nav-bar\">"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 4 boundaries in Module 03.")
        return False

    updated_content = content[:start_idx] + EXPANDED_MULTILEVEL_SECTION + "\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Multi-Level Page Tables in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if update_multilevel_section():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Deeply expand Multi-Level Hierarchical Page Tables in Week 7 Module 03\n\n"
                "Add mathematical proofs for 64-bit scaling, 10-10-12 and 9-9-9-9-12 bit\n"
                "decompositions, 2MB/1GB huge pages, CR3 walks, and 5-level paging."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
