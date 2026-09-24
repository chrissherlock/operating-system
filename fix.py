#!/usr/bin/env python3
# =====================================================================
# fix.py: Clarify Internal Slack formula with intuitive walkthrough
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week07-memory-management-virtual-memory",
    "01-physical-memory-abstractions.html"
)

UPDATED_INTERNAL_FRAG_SECTION = r"""      <h4>1. Internal Fragmentation: Allocation Quantum Slack</h4>
      <p>
        <strong>Internal fragmentation</strong> occurs when memory is assigned in fixed-size allocation quanta or granularity blocks (such as fixed partition slots, power-of-two blocks in buddy allocators, or 4 KB paging frames). When an application's requested memory footprint does not align perfectly with the hardware or allocator's unit size, the system must round up to the nearest whole block.
      </p>

      <!-- Intuitive Analogy Callout -->
      <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid var(--success); padding: 14px 18px; border-radius: 0 6px 6px 0; margin: 16px 0;">
        <strong style="color: #15803d; font-size: 0.92rem;">The Intuitive Analogy: Fixed Egg Cartons</strong>
        <p style="font-size: 0.86rem; color: #166534; margin: 6px 0 0 0; line-height: 1.5;">
          Imagine eggs are sold strictly in fixed cartons of a dozen ($S = 12$). If a recipe requires <strong>14 eggs</strong> ($R = 14$), the supermarket will not sell you 1.16 cartons. You are forced to purchase <strong>2 whole cartons (24 eggs)</strong>. The 10 empty egg slots sitting in your fridge represent <em>internal slack</em>: space you paid for and occupy, but cannot use or share with anyone else.
        </p>
      </div>

      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--accent);">
        <strong style="color: var(--primary);">Mathematical Definition of Internal Slack:</strong>
        <br><br>
        Let $S$ be the fixed hardware block size, and let $R$ be the requested payload size ($R > 0$). The allocated memory $A$ and internal slack $W_{\text{internal}}$ are given by:
        $$ A = \lceil R / S \rceil \times S $$
        $$ W_{\text{internal}} = A - R $$
        <p style="margin: 8px 0 0 0; font-size: 0.85rem; color: var(--text-muted);">
          <em>Note:</em> The ceiling brackets $\lceil x \rceil$ denote the ceiling function, which always rounds up to the next integer (e.g., $\lceil 1.22 \rceil = 2$).
        </p>
      </div>

      <h5>Step-by-Step Numeric Walkthrough</h5>
      <p>
        Consider a standard operating system allocating memory in standard <strong>4 KB (4096-byte)</strong> pages:
      </p>
      <ol style="font-size: 0.92rem; line-height: 1.6;">
        <li><strong>Program Request ($R$):</strong> Your application requests $5000\text{ bytes}$ ($R = 5000$, $S = 4096$).</li>
        <li><strong>Divide by Block Size:</strong> $R / S = 5000 / 4096 \approx 1.2207\text{ blocks}$.</li>
        <li><strong>Apply Ceiling Rounding ($\lceil \dots \rceil$):</strong> Because the hardware MMU cannot allocate fractions of a page, the OS rounds up to $\lceil 1.2207 \rceil = 2\text{ full blocks}$.</li>
        <li><strong>Compute Total Memory Allocated ($A$):</strong> $A = 2 \times 4096 = 8192\text{ bytes}$.</li>
        <li><strong>Determine Internal Slack ($W_{\text{internal}}$):</strong>
          $$ W_{\text{internal}} = A - R = 8192 - 5000 = 3192\text{ bytes} $$
        </li>
      </ol>
      <p>
        These $3192\text{ bytes}$ are trapped <em>inside</em> the boundary of the second page allocated to your process. Because that physical page belongs exclusively to your process, the kernel cannot lend those remaining 3192 bytes to any other program.
      </p>

      <h5>Statistical Expectation: The Half-Block Rule</h5>
      <p>
        What is the average waste across thousands of processes? If program memory requests are uniformly distributed, the wasted space in the final page ranges from $1\text{ byte}$ (if requesting 4095 bytes) to $4095\text{ bytes}$ (if requesting 4097 bytes). Averaged across all random allocations, the expected waste per segment is exactly half an allocation block:
      </p>
      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--primary);">
        $$ \mathbb{E}[W_{\text{internal}}] = \frac{0 + S}{2} = \frac{S}{2} $$
      </div>
      <p>
        In a system with $N$ active allocations and a 4 KB allocation granularity ($S = 4096$), the kernel wastes approximately $N \times 2048$ bytes of physical RAM simply through internal block rounding.
      </p>"""

def update_internal_fragmentation_section():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "      <h4>1. Internal Fragmentation: Allocation Quantum Slack</h4>"
    end_marker = "      <h4>2. External Fragmentation: Checkerboard Hole Formation</h4>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 5.1 boundaries in target file.")
        return False

    updated_content = content[:start_idx] + UPDATED_INTERNAL_FRAG_SECTION + "\n\n" + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully updated Internal Fragmentation section in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if update_internal_fragmentation_section():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Add intuitive egg-carton analogy and walkthrough to Internal Slack math\n\n"
                "Clarify ceiling notation in Week 7 Module 01 with a concrete 4 KB numeric\n"
                "example and intuitive explanation of the half-block expectation rule."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
