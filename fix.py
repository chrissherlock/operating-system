#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Half-Block Rule & OS Page Size Trade-offs in Module 01
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week07-memory-management-virtual-memory",
    "01-physical-memory-abstractions.html"
)

EXPANDED_HALF_BLOCK_SECTION = r"""      <h5>Statistical Expectation: The Half-Block Rule</h5>
      <p>
        A central sizing question in operating system engineering is: <em>If memory is allocated in fixed-size blocks of size $S$ (such as 4 KB paging frames), how much physical memory is wasted on average across all running applications?</em>
      </p>
      <p>
        Notice that when a process or thread allocates contiguous memory spanning multiple blocks, <strong>all blocks except the last one are 100% utilized</strong>:
      </p>
      <ul>
        <li>Block $1, 2, \dots, (k-1)$: Completely saturated with application data (0% waste).</li>
        <li>Block $k$ (Terminal Block): Contains the remaining spill payload, leaving internal slack space.</li>
      </ul>
      <p>
        Internal fragmentation therefore exists <strong>exclusively in the final allocated block</strong> of each memory segment.
      </p>

      <h6>1. The Intuitive Symmetric Distribution Argument</h6>
      <p>
        Consider a standard 4 KB ($S = 4096\text{ bytes}$) page. The amount of data spilling into the final page depends on the requested size modulo $S$:
      </p>
      <ul>
        <li>If the spill is $4095\text{ bytes}$, the process fills nearly the entire page:
          $$ W_{\text{internal}} = 4096 - 4095 = 1\text{ byte} $$
        </li>
        <li>If the spill is $1\text{ byte}$, the OS must allocate a full 4096-byte page just for that single byte:
          $$ W_{\text{internal}} = 4096 - 1 = 4095\text{ bytes} $$
        </li>
        <li>If the spill is $2048\text{ bytes}$, exactly half the page is wasted:
          $$ W_{\text{internal}} = 4096 - 2048 = 2048\text{ bytes} $$
        </li>
      </ul>
      <p>
        Across thousands of varied application allocations, these residual payloads are uniformly distributed across the interval $(0, S]$. Because every near-empty page ($4095\text{ B}$ waste) is statistically paired with a corresponding near-full page ($1\text{ B}$ waste), the expected mean converges symmetrically:
      </p>
      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--primary);">
        $$ \mathbb{E}[W_{\text{internal}}] = \frac{\text{Min Waste} + \text{Max Waste}}{2} = \frac{0 + S}{2} = \frac{S}{2} $$
      </div>

      <h6>2. Continuous Calculus Derivation</h6>
      <p>
        Formally, let $x$ be a continuous random variable representing the bytes used in the final block ($0 < x \le S$). Assuming a uniform probability distribution $x \sim U(0, S)$, the constant probability density function is $f(x) = \frac{1}{S}$.
      </p>
      <p>
        The expected internal slack $\mathbb{E}[W]$ is computed by integrating the waste function $W(x) = S - x$ over the entire block:
      </p>
      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--accent);">
        <strong style="color: var(--primary);">Derivation of Expected Internal Slack:</strong>
        <br><br>
        $$ \mathbb{E}[W_{\text{internal}}] = \int_0^S (S - x) \cdot f(x) \, dx = \frac{1}{S} \int_0^S (S - x) \, dx $$
        $$ = \frac{1}{S} \left[ S x - \frac{x^2}{2} \right]_0^S = \frac{1}{S} \left( S^2 - \frac{S^2}{2} \right) = \frac{1}{S} \left( \frac{S^2}{2} \right) = \frac{S}{2} $$
      </div>

      <h6>3. Architectural Trade-offs: Choosing Block Size ($S$)</h6>
      <p>
        The Half-Block Rule exposes an unavoidable architectural tension when operating system designers select hardware page sizes:
      </p>
      <table style="width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.88rem;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px; text-align: left; color: var(--primary);">Design Dimension</th>
            <th style="padding: 10px; text-align: left; color: var(--primary);">Small Pages (e.g., 1 KB)</th>
            <th style="padding: 10px; text-align: left; color: var(--primary);">Large Pages (e.g., 64 KB or 2 MB)</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px; font-weight: 600;">Average Internal Slack</td>
            <td style="padding: 10px; color: #16a34a;">Low: $\frac{1024}{2} = 512\text{ bytes}$ per segment.</td>
            <td style="padding: 10px; color: #dc2626;">High: $\frac{65536}{2} = 32\text{ KB}$ (or 1 MB for huge pages).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px; font-weight: 600;">Page Table Memory Footprint</td>
            <td style="padding: 10px; color: #dc2626;">Massive: Requires $4\times$ more Page Table Entries (PTEs) to map the same RAM.</td>
            <td style="padding: 10px; color: #16a34a;">Compact: Drastically fewer PTEs required in physical memory.</td>
          </tr>
          <tr>
            <td style="padding: 10px; font-weight: 600;">TLB Cache Coverage</td>
            <td style="padding: 10px; color: #dc2626;">Poor: TLB misses skyrocket due to narrow spatial range.</td>
            <td style="padding: 10px; color: #16a34a;">Superior: A single TLB entry covers large contiguous regions.</td>
          </tr>
        </tbody>
      </table>

      <h6>4. System-Wide Memory Slack Calculation</h6>
      <p>
        In an operating system executing $N$ concurrent processes where each process maintains distinct segments for Code (text), Data/Heap, and Stack, there are $3$ terminal pages per process ($3N$ terminal pages system-wide).
      </p>
      <p>
        The total physical memory consumed purely by internal fragmentation across the system is:
      </p>
      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--primary);">
        $$ \text{Total System Slack} \approx 3N \times \frac{S}{2} $$
        <p style="margin: 8px 0 0 0; font-size: 0.88rem; color: var(--text);">
          For $N = 500$ processes on a Linux kernel with standard 4 KB ($S = 4096$) pages:
          $$ \text{Total Waste} \approx 3(500) \times 2048\text{ bytes} \approx 3{,}072{,}000\text{ bytes} \approx 3.07\text{ MB} $$
        </p>
      </div>
      <p>
        On a modern machine with 16 GB to 64 GB of physical RAM, sacrificing $\approx 3\text{ MB}$ to internal slack is an extraordinarily small price to pay for the enormous speed and protection benefits of fixed-page hardware memory management.
      </p>"""

def update_half_block_rule():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "      <h5>Statistical Expectation: The Half-Block Rule</h5>"
    end_marker = "      <h4>2. External Fragmentation: Checkerboard Hole Formation</h4>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 5.1 boundaries in target file.")
        return False

    updated_content = content[:start_idx] + EXPANDED_HALF_BLOCK_SECTION + "\n\n" + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Half-Block Rule in {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if update_half_block_rule():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Expand Half-Block Rule derivation and OS page size trade-offs in Module 01\n\n"
                "Add intuitive symmetry argument, calculus expectation derivation, system-wide\n"
                "segment waste calculations, and page size architectural trade-offs."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
