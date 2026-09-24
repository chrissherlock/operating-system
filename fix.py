#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Memory Fragmentation in Week 7 Module 01
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week07-memory-management-virtual-memory",
    "01-physical-memory-abstractions.html"
)

FRAGMENTATION_EXPANSION = r"""      <h3>5. Memory Fragmentation: Internal vs. External</h3>
      <p>
        In any dynamic storage allocation system, memory fragmentation is the inevitable systemic inefficiency that arises as processes are allocated, expanded, and released over time. Understanding the exact mechanical distinction between <strong>Internal Fragmentation</strong> and <strong>External Fragmentation</strong> is fundamental to OS memory architecture.
      </p>

      <h4>1. Internal Fragmentation: Allocation Quantum Slack</h4>
      <p>
        <strong>Internal fragmentation</strong> occurs when memory is assigned in fixed-size allocation quanta or granularity blocks (such as fixed partition slots, power-of-two blocks in buddy allocators, or 4 KB paging frames). When an application's requested memory footprint does not align perfectly with the hardware or allocator's unit size, the system must round up to the nearest whole block.
      </p>

      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--accent);">
        <strong style="color: var(--primary);">Mathematical Definition of Internal Slack:</strong>
        <br><br>
        Let $S$ be the fixed allocation block size, and let $R$ be the requested payload size ($R > 0$). The allocated memory $A$ and internal slack $W_{\text{internal}}$ are given by:
        $$ A = \lceil R / S \rceil \times S $$
        $$ W_{\text{internal}} = A - R $$
      </div>

      <p>
        Because this slack space lies <em>inside</em> the boundary of an allocated region, the kernel's memory allocator cannot assign it to any other process. It remains completely unusable for the entire lifetime of the process.
      </p>

      <h5>Statistical Expectation: The Half-Block Rule</h5>
      <p>
        If process payload requests $R$ are uniformly distributed across the interval $(k \cdot S, (k + 1) \cdot S]$, the expected amount of internal fragmentation per allocated segment is exactly half a block:
      </p>
      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--primary);">
        $$ \mathbb{E}[W_{\text{internal}}] = \frac{1}{S} \int_0^S (S - x) \, dx = \frac{S}{2} $$
      </div>
      <p>
        In a system with $N$ active allocations and a 4 KB allocation granularity ($S = 4096$), the kernel wastes approximately $N \times 2048$ bytes of physical RAM simply through internal block rounding.
      </p>

      <h4>2. External Fragmentation: Checkerboard Hole Formation</h4>
      <p>
        <strong>External fragmentation</strong> emerges in variable-sized contiguous allocation schemes (such as dynamic partitioning with Base and Limit registers). As processes of varying sizes enter and terminate at arbitrary times, free contiguous memory is fragmented into a scattered collection of small, non-contiguous "holes."
      </p>
      <p>
        A system suffers from external fragmentation when the <strong>sum total of all free memory holes is sufficient</strong> to satisfy a process allocation request, but <strong>no single contiguous hole is large enough</strong> to hold the process.
      </p>

      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--danger);">
        <strong style="color: var(--danger);">External Fragmentation Condition:</strong>
        <br><br>
        $$ \sum_{k=1}^{M} \text{Size}(\text{Hole}_k) \ge \text{RequestedSize} \quad \land \quad \max_{1 \le k \le M} \big(\text{Size}(\text{Hole}_k)\big) < \text{RequestedSize} $$
      </div>

      <h5>Knuth's 50% Rule of Allocation</h5>
      <p>
        In <em>The Art of Computer Programming</em> (Vol. 1), Donald Knuth proved a fundamental statistical theorem governing contiguous dynamic storage allocation under steady-state conditions:
      </p>
      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--accent);">
        <strong style="color: var(--primary);">Knuth's 50% Rule:</strong>
        <br><br>
        $$ M \approx \frac{1}{2} N $$
        <p style="margin: 8px 0 0 0; font-size: 0.88rem; color: var(--text);">
          In steady state, if $N$ blocks are actively allocated, the number of isolated free holes $M$ tends asymptotically toward $N / 2$, regardless of whether First-Fit or Best-Fit allocation is used.
        </p>
      </div>
      <p>
        <strong>Consequence:</strong> If each hole is approximately the same average size as an allocated block, approximately <strong>one-third of all physical memory is rendered unusable</strong> due to external fragmentation:
        $$ \text{Fraction of Memory in Holes} \approx \frac{M}{N + M} = \frac{0.5 N}{N + 0.5 N} = \frac{0.5}{1.5} \approx 33.3\% $$

      <h4>3. Resolving External Fragmentation: Memory Compaction</h4>
      <p>
        To reclaim checkerboarded free memory in a contiguous system, the operating system must execute <strong>Memory Compaction</strong> (relocation defragmentation). The kernel shifts all active processes toward one end of physical memory (usually toward address $0$), coalescing all isolated holes into a single contiguous pool.
      </p>

      <h5>Compaction Mechanics &amp; Algorithms</h5>
      <ul>
        <li>
          <strong>Sliding Compaction:</strong> Active segments are slid downward toward low memory while preserving their original relative ordering. This minimizes displacement distance and preserves data cache spatial locality.
        </li>
        <li>
          <strong>Two-Finger Compaction (LISP-style):</strong> Uses two pointers moving toward each other: a free-space scanner starting at memory zero and a process scanner starting at high memory. Processes from the top are moved into free slots at the bottom. While faster, it scrambles process ordering.
        </li>
      </ul>

      <h5>The Cost of Compaction</h5>
      <p>
        Compaction imposes severe architectural performance penalties:
      </p>
      <ol>
        <li>
          <strong>Bus Saturation &amp; Latency:</strong> Compacting 16 GB of active RAM across memory channels at 25 GB/s stalls the system for over 600 milliseconds—an unacceptable latency spike for interactive and real-time operating systems.
        </li>
        <li>
          <strong>Hardware Prerequisite:</strong> Compaction is <em>impossible</em> under static relocation. It requires hardware-assisted dynamic relocation (Base and Limit registers), because every moved process must have its Base Register updated to reflect its new physical offset.
        </li>
        <li>
          <strong>Direct Memory Access (DMA) Lockout:</strong> If a network card or disk controller is currently executing a DMA transfer into a process's buffer, that process cannot be moved until the hardware I/O finishes, locking memory in place.
        </li>
      </ol>

      <h4>4. Summary Comparison</h4>
      <table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.88rem;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px; text-align: left; color: var(--primary);">Attribute</th>
            <th style="padding: 10px; text-align: left; color: var(--primary);">Internal Fragmentation</th>
            <th style="padding: 10px; text-align: left; color: var(--primary);">External Fragmentation</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px; font-weight: 600;">Location of Wasted Space</td>
            <td style="padding: 10px;"><em>Inside</em> the allocated partition or page boundary.</td>
            <td style="padding: 10px;"><em>Between</em> distinct allocated partitions (holes in RAM).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px; font-weight: 600;">Root Cause</td>
            <td style="padding: 10px;">Fixed-size allocation granularity (quanta rounding).</td>
            <td style="padding: 10px;">Variable-sized allocations combined with dynamic allocation/freeing.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px; font-weight: 600;">Typical Occurrences</td>
            <td style="padding: 10px;">Paging systems (4 KB pages), Buddy allocators.</td>
            <td style="padding: 10px;">Base/Limit dynamic partitioning, unpaged heap managers.</td>
          </tr>
          <tr>
            <td style="padding: 10px; font-weight: 600;">Architectural Solution</td>
            <td style="padding: 10px;">Smaller allocation quanta (e.g., fine-grained slab allocators).</td>
            <td style="padding: 10px;"><strong>Paging:</strong> Decouple contiguous virtual space from physical frames.</td>
          </tr>
        </tbody>
      </table>"""

def expand_memory_fragmentation():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>5. Memory Fragmentation: Internal vs. External</h3>"
    end_marker = "</div>\n\n    <nav class=\"nav-bar\">"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 5 boundaries in target file.")
        return False

    updated_content = content[:start_idx] + FRAGMENTATION_EXPANSION + "\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Memory Fragmentation in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if expand_memory_fragmentation():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Deeply expand Memory Fragmentation section in Week 7 Module 01\n\n"
                "Add formal internal slack expectation, Knuth 50% rule of allocation,\n"
                "sliding compaction mechanics, and memory bus bandwidth trade-offs."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
