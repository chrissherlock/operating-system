#!/usr/bin/env python3
# =====================================================================
# update_aside_placement.py: Place enriched aside boxes below sections
# =====================================================================
import os
import subprocess
import sys

WIKI_ASIDE_SMP = r"""
        <!-- WIKIPEDIA ASIDE BOX -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 24px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Summary &amp; Further Reading: Symmetric Multiprocessing (SMP)</h4>
          <p style="margin-bottom: 8px; color: #334155; font-size: 0.9rem; line-height: 1.5;">
            Symmetric Multiprocessing (SMP) evolved from early mainframe architectures such as the Burroughs D825 (1962) into commercial open-systems hardware pioneered by Sequent Computer Systems in the 1980s. Unlike asynchronous master-slave models where one CPU monopolizes kernel execution, SMP allows any processor to execute kernel code, service hardware interrupts, and schedule threads concurrently across a unified shared physical memory space.
          </p>
          <ul style="margin-left: 20px; display: flex; flex-direction: column; gap: 4px;">
            <li><a href="https://en.wikipedia.org/wiki/Symmetric_multiprocessing" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Symmetric Multiprocessing on Wikipedia</a></li>
          </ul>
        </aside>"""

WIKI_ASIDE_GANG = r"""
        <!-- WIKIPEDIA ASIDE BOX -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 24px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Summary &amp; Further Reading: Gang Scheduling</h4>
          <p style="margin-bottom: 8px; color: #334155; font-size: 0.9rem; line-height: 1.5;">
            Gang scheduling was pioneered by John Ousterhout in 1982 to address the coordination failure of independent thread schedulers on parallel hardware. By scheduling related threads across multiple cores simultaneously (a two-dimensional matrix of Cores $\times$ Time Quanta), gang scheduling prevents preemption delays and blocking when cooperating threads communicate.
          </p>
          <ul style="margin-left: 20px; display: flex; flex-direction: column; gap: 4px;">
            <li><a href="https://en.wikipedia.org/wiki/Gang_scheduling" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Gang Scheduling on Wikipedia</a></li>
          </ul>
        </aside>"""

WIKI_ASIDE_RPC_DSM = r"""
        <!-- WIKIPEDIA ASIDE BOX -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 24px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Summary &amp; Further Reading: RPC &amp; DSM</h4>
          <p style="margin-bottom: 8px; color: #334155; font-size: 0.9rem; line-height: 1.5;">
            Remote Procedure Calls (RPC), introduced by Birrell and Nelson in 1984, abstract network messaging into transparent local subroutine calls. Distributed Shared Memory (DSM), pioneered by Kai Li with the Ivy system in 1986, bridges multicomputer hardware by emulating a single shared virtual address space across physically disjoint nodes using MMU page faults and network replication.
          </p>
          <ul style="margin-left: 20px; display: flex; flex-direction: column; gap: 4px;">
            <li><a href="https://en.wikipedia.org/wiki/Remote_procedure_call" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Remote Procedure Call on Wikipedia</a></li>
            <li><a href="https://en.wikipedia.org/wiki/Distributed_shared_memory" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Distributed Shared Memory on Wikipedia</a></li>
          </ul>
        </aside>"""

def update_asides():
    mod1 = os.path.join("week11-multiprocessors", "01-multiprocessor-hardware.html")
    mod2 = os.path.join("week11-multiprocessors", "02-multiprocessor-scheduling.html")
    mod4 = os.path.join("week11-multiprocessors", "04-rpc-dsm-load-balancing.html")

    modified = []

    # Clean existing asides across all files first
    for path in [mod1, mod2, mod4]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if "<!-- WIKIPEDIA ASIDE BOX -->" in content:
                # Strip out existing asides
                parts = content.split("<!-- WIKIPEDIA ASIDE BOX -->")
                cleaned = parts[0] + "\n".join([p.split("</aside>", 1)[1] for p in parts[1:]])
                with open(path, "w", encoding="utf-8") as f:
                    f.write(cleaned)

    # Module 1: Place SMP aside at the end of Section 8.1.2
    if os.path.exists(mod1):
        with open(mod1, "r", encoding="utf-8") as f:
            c1 = f.read()
        target = "<!-- GUIDED WALKTHROUGH 4: OS ARCHITECTURES -->"
        if target in c1:
            c1 = c1.replace(target, WIKI_ASIDE_SMP + "\n\n      " + target)
            with open(mod1, "w", encoding="utf-8") as f:
                f.write(c1)
            modified.append(mod1)

    # Module 2: Place Gang aside at the end of Gang Scheduling section
    if os.path.exists(mod2):
        with open(mod2, "r", encoding="utf-8") as f:
            c2 = f.read()
        target = "<!-- GUIDED WALKTHROUGH"
        if target in c2:
            c2 = c2.replace(target, WIKI_ASIDE_GANG + "\n\n      " + target, 1)
            with open(mod2, "w", encoding="utf-8") as f:
                f.write(c2)
            modified.append(mod2)

    # Module 4: Place RPC/DSM aside at the end of RPC/DSM overview
    if os.path.exists(mod4):
        with open(mod4, "r", encoding="utf-8") as f:
            c4 = f.read()
        target = "<!-- GUIDED WALKTHROUGH"
        if target in c4:
            c4 = c4.replace(target, WIKI_ASIDE_RPC_DSM + "\n\n      " + target, 1)
            with open(mod4, "w", encoding="utf-8") as f:
                f.write(c4)
            modified.append(mod4)

    # Also synchronize fix.py to reflect current state
    fix_path = "fix.py"
    if os.path.exists(fix_path):
        modified.append(fix_path)

    if not modified:
        print("--> No files modified.")
        return

    print(f"--> Staging modified files: {modified}")
    subprocess.run(["git", "add"] + modified, check=True)

    commit_msg = (
        "Move asides below relevant sections and add historical summaries\n\n"
        "Relocate Wikipedia research aside boxes to the end of their respective\n"
        "sections across Week 11 modules and enrich them with comprehensive\n"
        "historical summaries."
    )

    print("--> Committing changes...")
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    print("--> Pushing changes to origin main...")
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("--> Aside placement and historical summaries deployed successfully!")

if __name__ == "__main__":
    update_asides()
