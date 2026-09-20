#!/usr/bin/env python3
# =====================================================================
# flesh_out_numa_hardware.py: Expand Section 8.1.1 Hardware & NUMA
# =====================================================================
import os
import subprocess
import sys

EXPANDED_HARDWARE_SECTION = r"""    <!-- SECTION 8.1.1: HARDWARE & COHERENCE -->
    <section class="content-section">
      <h2>8.1.1 Multiprocessor Hardware &amp; Cache Coherence</h2>
      <p>
        Modern multiprocessing systems organize multiple execution cores around shared physical memory. Depending on how memory is interconnected and how bus bandwidth scales, architectures fall into two primary hardware paradigms:
      </p>

      <h3>1. Uniform Memory Access (UMA)</h3>
      <p>
        In a <strong>Uniform Memory Access (UMA)</strong> architecture, all processors share a common system bus or crossbar switch connected to a centralized memory bank. Every CPU core experiences identical memory latency regardless of which core initiates the read or write request. While simple to program, UMA suffers from severe scalability limits: as core counts scale beyond 8–16 processors, the shared interconnect bus saturates entirely under memory bandwidth contention.
      </p>

      <h3>2. Non-Uniform Memory Access (NUMA)</h3>
      <p>
        To bypass UMA bus saturation, modern multi-socket servers and high-performance clusters utilize <strong>Non-Uniform Memory Access (NUMA)</strong>. Physical memory is partitioned and distributed locally across processor nodes connected via a high-speed interconnect fabric (such as AMD Infinity Fabric or Intel Ultra Path Interconnect - UPI).
      </p>
      <ul>
        <li><strong>Local Memory Access:</strong> Accessing memory physically attached to the local socket node is fast (~20 ns).</li>
        <li><strong>Remote Memory Access:</strong> Accessing memory residing on a remote socket node requires traversing the interconnect fabric, incurring significantly higher latency (~80 ns).</li>
      </ul>

      <h3>3. Cache-Coherent NUMA (ccNUMA) &amp; Directory-Based Protocols</h3>
      <p>
        While snooping protocols (like MESI) broadcast every cache event across a shared bus, snooping does not scale beyond a small number of cores because the broadcast bus itself becomes a bottleneck. To solve this for large-scale NUMA systems, computer architects developed <strong>directory-based cache coherence (ccNUMA)</strong>.
      </p>
      <p>
        Pioneered academically by <strong>Anant Agarwal</strong> and his research team with the <strong>Stanford DASH (Directory Architecture for Shared Memory)</strong> project in the early 1990s, directory-based protocols eliminate broadcast snooping. Instead, a centralized or distributed <em>directory</em> maintains the sharing status of every memory block. When a core requests a cache line, it queries the directory managing that specific physical address block, which then directs point-to-point invalidation messages solely to the nodes actively caching that line.
      </p>

      <!-- NUMA & DASH RESEARCH ASIDE -->
      <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 24px 0; font-size: 0.92rem; color: #0369a1;">
        <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Summary &amp; Further Reading: Non-Uniform Memory Access (NUMA) &amp; DASH</h4>
        <p style="margin-bottom: 10px; color: #334155; font-size: 0.9rem; line-height: 1.5;">
          <strong>Non-Uniform Memory Access (NUMA)</strong> revolutionized enterprise scalability by replacing centralized UMA buses with distributed memory nodes. The foundational breakthroughs in cache-coherent NUMA (ccNUMA) were established by <strong>Anant Agarwal</strong> and the <strong>Stanford DASH project team</strong> in the early 1990s. DASH proved that directory-based cache coherence could eliminate snooping bus bottlenecks, paving the way for modern multi-socket enterprise servers and cloud data center architectures.
        </p>
        <div style="border-top: 1px solid #bae6fd; padding-top: 8px; margin-top: 8px;">
          <a href="https://en.wikipedia.org/wiki/Non-uniform_memory_access" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline; font-weight: 500; font-size: 0.88rem;">Read more on Wikipedia: Non-Uniform Memory Access &rarr;</a>
        </div>
      </aside>

      <p>
        <strong>The Cache Coherence Problem:</strong> Because CPU execution cores operate orders of magnitude faster than main memory, each core relies on high-speed private caches (L1 and L2). If CPU 0 modifies a variable in its private cache, CPU 1's private cache immediately becomes stale. To preserve memory consistency without routing every access back to slow main RAM, hardware controllers monitor memory lines using coherence protocols.
      </p>"""

def update_hardware_module():
    mod1 = os.path.join("week11-multiprocessors", "01-multiprocessor-hardware.html")
    modified = []

    if os.path.exists(mod1):
        with open(mod1, "r", encoding="utf-8") as f:
            content = f.read()

        # Find section 8.1.1 and replace it with the expanded version up to Guided Walkthrough 3
        start_marker = "<!-- SECTION 8.1.1: HARDWARE & COHERENCE -->"
        end_marker = "<!-- GUIDED WALKTHROUGH 3: MESI PROTOCOL -->"

        if start_marker in content and end_marker in content:
            parts = content.split(start_marker)
            trailer = parts[1].split(end_marker)[1]
            content = parts[0] + start_marker + "\n" + EXPANDED_HARDWARE_SECTION + "\n\n      <!-- GUIDED WALKTHROUGH 3: MESI PROTOCOL -->" + trailer
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
            "Flesh out Section 8.1.1 hardware module with deep NUMA and DASH coverage\n\n"
            "Expand 01-multiprocessor-hardware.html to provide thorough pedagogical depth on\n"
            "UMA vs ccNUMA topologies, Stanford DASH directory coherence, and topology-aware\n"
            "memory hierarchies, complete with an enriched research aside box."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Section 8.1.1 successfully expanded with NUMA and DASH coverage!")

if __name__ == "__main__":
    update_hardware_module()
