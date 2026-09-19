#!/usr/bin/env python3
import os
import re

def main():
    target_html = "week09-memory-management/09-working-set.html"
    if os.path.exists(target_html):
        with open(target_html, "r", encoding="utf-8") as f:
            html = f.read()

        # Define CSS for true float: left with right-side text wrapping
        float_left_css = """
    .theory-section {
      line-height: 1.7;
      font-size: 0.95rem;
      color: #334155;
      display: block;
    }
    .bio-sidebar {
      float: left;
      width: 300px;
      background: #f8fafc;
      border: 1px solid var(--border);
      border-top: 4px solid var(--accent);
      border-radius: 6px;
      padding: 16px;
      margin-right: 24px;
      margin-bottom: 16px;
      margin-top: 4px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      font-size: 0.88rem;
      shape-outside: margin-box;
    }
    .bio-sidebar img {
      width: 100%;
      height: auto;
      border-radius: 4px;
      margin-bottom: 6px;
      border: 1px solid var(--border);
    }
    .photo-credit {
      font-size: 0.72rem;
      color: var(--text-muted);
      font-style: italic;
      margin-bottom: 8px;
    }"""

        # Remove existing .theory-grid or old styles
        html = re.sub(r'\.theory-grid\s*\{[^}]+\}', '', html)
        html = re.sub(r'\.bio-sidebar\s*\{[^}]+\}', '', html)
        html = html.replace("</style>", f"{float_left_css}\n  </style>")

        # Restructure HTML to use standard block theory-section with sidebar floated left at the top
        old_theory_grid = re.search(r'<div class="theory-grid">.*?</div>\s*</div>', html, re.DOTALL)

        standard_theory_block = """<div class="theory-section">
        <!-- Floating Sidebar on Left with text wrapping around right -->
        <aside class="bio-sidebar">
          <h3>Pioneer Profile</h3>
          <img src="assets/peter-denning.jpg" alt="Dr. Peter J. Denning">
          <div class="photo-credit">Photo by Louis Fabian Bachrach</div>
          <p><strong>Dr. Peter J. Denning</strong> (often referenced as Peter Jenning in informal notes) is an American computer scientist renowned for his foundational work on virtual memory.</p>
          <p>In 1968, while at MIT, he formulated the <strong>Working Set Model</strong> and program locality principles. Read more on his <a href="https://en.wikipedia.org/wiki/Peter_J._Denning" target="_blank">Wikipedia page</a>.</p>
        </aside>

        <h2>1. The Problem of Thrashing</h2>
        <p>
          In previous modules, demand paging allowed processes to run even if only a few of their pages were resident in physical RAM. However, if a process is allocated too few frames relative to its active needs, it will suffer continuous page faults. The CPU spends more time swapping pages between disk and RAM than executing actual instructions—a catastrophic state known as <strong>thrashing</strong>.
        </p>

        <h2>2. The Working Set Model Definition ($w(k, t)$)</h2>
        <p>
          To prevent thrashing, <a href="https://en.wikipedia.org/wiki/Peter_J._Denning" target="_blank" style="color: var(--accent); text-decoration: underline;">Peter Denning</a> introduced the <strong>Working Set Model</strong>. The working set is the set of pages referenced by a process during the last $k$ virtual memory references (or time window $\tau$).
        </p>
        <div class="theory-callout">
          <strong>Mathematical Formulation:</strong><br>
          Let $w(k, t)$ be the size of the working set (number of unique pages referenced in the window of the last $k$ memory references ending at virtual time $t$).<br>
          - As $k$ grows very small, $w(k, t)$ captures only the immediate instruction.<br>
          - As $k$ grows very large, $w(k, t)$ encompasses the entire program.<br>
          - The OS aims to load exactly $w(k, t)$ pages into physical RAM before letting the process execute.
        </div>

        <h2>3. Conceptually: A Resource-Allocation Optimization Problem</h2>
        <p>
          At its core, the goal of the Working Set model is to solve a classic economic trade-off between memory allocation and performance:
        </p>
        <ul style="padding-left: 20px; display: block; gap: 6px; margin-bottom: 10px;">
          <li><strong>The Cost of Too Little Memory:</strong> Allocating too few frames leads directly to a spike in page faults and catastrophic thrashing.</li>
          <li><strong>The Cost of Too Much Memory:</strong> Allocating an oversized window wastes physical RAM that other processes could use to execute concurrently, lowering the overall multiprogramming level.</li>
          <li><strong>The Knee of the Curve:</strong> The optimal window size (\\(\\tau\\) or $k$) shown in Figure 3-19 represents the "knee of the curve"—the sweet spot where adding more memory yields diminishing returns in page fault reduction.</li>
        </ul>
        <p>
          <strong>Why Calculus Isn't Used in the Kernel:</strong> While this is conceptually an optimization problem, operating systems do not use formal calculus (like derivatives) to solve it in real time. Program execution is discrete and non-differentiable, and computing derivatives on the fly for dozens of threads introduces unacceptable CPU overhead. Instead, kernels rely on lightweight empirical heuristics (like the WSClock algorithm) to approximate working sets dynamically.
        </p>

        <h2>4. Why You Should Care: Thrashing &amp; Load Control</h2>
        <p>
          Understanding the Working Set model is critical for systems architecture and exams because it solves fundamental flaws in reactive replacement policies:
        </p>
        <ul style="padding-left: 20px; display: block; gap: 6px; margin-bottom: 10px;">
          <li><strong>The Cure for Thrashing:</strong> Without a working set, allocating too few frames causes continuous page faults where the CPU spends 100% of its cycles waiting on disk I/O rather than executing instructions. The Working Set defines the exact memory floor a process needs to stay stable.</li>
          <li><strong>Proactive vs. Reactive:</strong> Algorithms like Clock and Aging are <em>reactive</em>—they wait until a page fault already occurs before evicting a frame. The Working Set model is <em>proactive</em>, tracking active footprints over time ($w(k, t)$) to ensure required pages are resident before execution.</li>
          <li><strong>System Load &amp; Admission Control:</strong> The OS sums the working sets of all active processes (\\(\\sum w\\)). If the sum exceeds total physical RAM, the OS uses admission control to suspend low-priority processes entirely, preventing system-wide thrashing.</li>
        </ul>
      </div>"""

        if old_theory_grid:
            html = html.replace(old_theory_grid.group(0), standard_theory_block)

        with open(target_html, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Successfully updated {target_html} with true float: left sidebar and text wrapping.")
    else:
        print(f"Error: {target_html} not found.")

if __name__ == "__main__":
    main()
