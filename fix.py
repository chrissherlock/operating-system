#!/usr/bin/env python3
# =====================================================================
# fix_agarwal_filename.py: Correct image filename to agarwal.jpeg
# =====================================================================
import os
import subprocess
import sys

WIKI_ASIDE_NUMA_AGARWAL_CORRECT = r"""
        <!-- NUMA & DASH RESEARCH ASIDE WITH CORRECT FILENAME -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 24px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Summary &amp; Further Reading: Non-Uniform Memory Access (NUMA) &amp; DASH</h4>

          <div style="display: flex; gap: 16px; align-items: flex-start; margin-bottom: 12px;">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; flex-shrink: 0;">
              <div style="width: 120px; height: 150px; background: #e2e8f0; border-radius: 4px; overflow: hidden; border: 1px solid #bae6fd;">
                <img src="../images/agarwal.jpeg" alt="Anant Agarwal Portrait" style="width: 100%; height: 100%; object-fit: cover;">
              </div>
              <span style="font-size: 0.72rem; color: #64748b; text-align: center; line-height: 1.2;">Photo by New America<br>(2015 Conference)</span>
            </div>

            <div style="display: flex; flex-direction: column; gap: 10px; flex-grow: 1;">
              <p style="color: #334155; font-size: 0.9rem; line-height: 1.5; margin: 0;">
                <strong>Non-Uniform Memory Access (NUMA)</strong> revolutionized enterprise scalability by replacing centralized UMA buses with distributed memory nodes. The foundational breakthroughs in cache-coherent NUMA (ccNUMA) were established by <a href="https://en.wikipedia.org/wiki/Anant_Agarwal" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline; font-weight: 600;">Anant Agarwal</a> and the <strong>Stanford DASH project team</strong> in the early 1990s. DASH proved that directory-based cache coherence could eliminate snooping bus bottlenecks, paving the way for modern multi-socket enterprise servers and cloud data center architectures.
              </p>
              <div>
                <a href="https://en.wikipedia.org/wiki/Non-uniform_memory_access" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline; font-weight: 500; font-size: 0.88rem;">Read more on Wikipedia: Non-Uniform Memory Access &rarr;</a>
              </div>
            </div>
          </div>
        </aside>"""

def fix_filename():
    mod1 = os.path.join("week11-multiprocessors", "01-multiprocessor-hardware.html")
    modified = []

    if os.path.exists(mod1):
        with open(mod1, "r", encoding="utf-8") as f:
            content = f.read()

        if "Historical Summary &amp; Further Reading: Non-Uniform Memory Access (NUMA)" in content:
            parts = content.split("<!-- NUMA & DASH RESEARCH ASIDE")
            content = parts[0] + parts[1].split("</aside>", 1)[1]

        target = "<!-- GUIDED WALKTHROUGH 3: MESI PROTOCOL -->"
        if target in content:
            content = content.replace(target, WIKI_ASIDE_NUMA_AGARWAL_CORRECT + "\n\n      " + target, 1)
            with open(mod1, "w", encoding="utf-8") as f:
                f.write(content)
            modified.append(mod1)

    fix_path = "fix.py"
    if os.path.exists(fix_path):
        modified.append(fix_path)

    if not modified:
        print("--> No files modified.")
        return

    print(f"--> Staging modified files: {modified}")
    try:
        subprocess.run(["git", "add"] + modified, check=True)
        commit_msg = (
            "Correct image filename reference from argawal.jpeg to agarwal.jpeg\n\n"
            "Update 01-multiprocessor-hardware.html to reference the correct asset filename\n"
            "images/agarwal.jpeg in the Anant Agarwal NUMA research aside box."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Image filename correction successfully deployed!")

if __name__ == "__main__":
    fix_filename()
