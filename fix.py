#!/usr/bin/env python3
# =====================================================================
# fix_aside_injection.py: Robustly Inject Wikipedia Aside Boxes
# =====================================================================
import os
import subprocess
import sys

WIKI_ASIDE_SMP = r"""
        <!-- WIKIPEDIA ASIDE BOX -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 20px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Context &amp; Further Reading</h4>
          <p style="margin-bottom: 6px; color: #334155; font-size: 0.9rem;">
            Explore the evolution of shared-memory architectures on Wikipedia:
          </p>
          <ul style="margin-left: 20px; display: flex; flex-direction: column; gap: 4px;">
            <li><a href="https://en.wikipedia.org/wiki/Symmetric_multiprocessing" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Symmetric Multiprocessing (SMP)</a> &mdash; Historical development from early mainframes (Burroughs D825) to commercial Open Systems (Sequent).</li>
          </ul>
        </aside>"""

WIKI_ASIDE_GANG = r"""
        <!-- WIKIPEDIA ASIDE BOX -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 20px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Context &amp; Further Reading</h4>
          <p style="margin-bottom: 6px; color: #334155; font-size: 0.9rem;">
            Explore parallel scheduling research on Wikipedia:
          </p>
          <ul style="margin-left: 20px; display: flex; flex-direction: column; gap: 4px;">
            <li><a href="https://en.wikipedia.org/wiki/Gang_scheduling" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Gang Scheduling</a> &mdash; Coordinated multi-core thread scheduling pioneered by John Ousterhout (1982).</li>
          </ul>
        </aside>"""

WIKI_ASIDE_RPC_DSM = r"""
        <!-- WIKIPEDIA ASIDE BOX -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 20px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Context &amp; Further Reading</h4>
          <p style="margin-bottom: 6px; color: #334155; font-size: 0.9rem;">
            Explore distributed programming paradigms on Wikipedia:
          </p>
          <ul style="margin-left: 20px; display: flex; flex-direction: column; gap: 4px;">
            <li><a href="https://en.wikipedia.org/wiki/Remote_procedure_call" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Remote Procedure Call (RPC)</a> &mdash; Transparent network subroutines pioneered by Birrell and Nelson (1984).</li>
            <li><a href="https://en.wikipedia.org/wiki/Distributed_shared_memory" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Distributed Shared Memory (DSM)</a> &mdash; Page-based memory emulation pioneered by Kai Li (Ivy system, 1986).</li>
          </ul>
        </aside>"""

def force_inject():
    mod1 = os.path.join("week11-multiprocessors", "01-multiprocessor-hardware.html")
    mod2 = os.path.join("week11-multiprocessors", "02-multiprocessor-scheduling.html")
    mod4 = os.path.join("week11-multiprocessors", "04-rpc-dsm-load-balancing.html")

    modified = []

    # Module 1
    if os.path.exists(mod1):
        with open(mod1, "r", encoding="utf-8") as f:
            c1 = f.read()
        # Remove old aside if present to avoid duplication
        c1 = c1.split("<!-- WIKIPEDIA ASIDE BOX -->")[0] + c1.split("</aside>")[-1] if "WIKIPEDIA ASIDE BOX" in c1 else c1

        target = "</header>"
        if target in c1:
            c1 = c1.replace(target, target + "\n" + WIKI_ASIDE_SMP)
            with open(mod1, "w", encoding="utf-8") as f:
                f.write(c1)
            modified.append(mod1)

    # Module 2
    if os.path.exists(mod2):
        with open(mod2, "r", encoding="utf-8") as f:
            c2 = f.read()
        c2 = c2.split("<!-- WIKIPEDIA ASIDE BOX -->")[0] + c2.split("</aside>")[-1] if "WIKIPEDIA ASIDE BOX" in c2 else c2

        target = "</header>"
        if target in c2:
            c2 = c2.replace(target, target + "\n" + WIKI_ASIDE_GANG)
            with open(mod2, "w", encoding="utf-8") as f:
                f.write(c2)
            modified.append(mod2)

    # Module 4
    if os.path.exists(mod4):
        with open(mod4, "r", encoding="utf-8") as f:
            c4 = f.read()
        c4 = c4.split("<!-- WIKIPEDIA ASIDE BOX -->")[0] + c4.split("</aside>")[-1] if "WIKIPEDIA ASIDE BOX" in c4 else c4

        target = "</header>"
        if target in c4:
            c4 = c4.replace(target, target + "\n" + WIKI_ASIDE_RPC_DSM)
            with open(mod4, "w", encoding="utf-8") as f:
                f.write(c4)
            modified.append(mod4)

    if not modified:
        print("--> No target files found.")
        return

    print(f"--> Staging modified files: {modified}")
    subprocess.run(["git", "add"] + modified, check=True)

    commit_msg = (
        "Fix aside box injection across Week 11 modules\n\n"
        "Target reliable header boundaries in HTML modules to ensure Wikipedia\n"
        "research aside boxes render correctly on the page."
    )

    print("--> Committing changes...")
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    print("--> Pushing changes to origin main...")
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("--> Aside boxes successfully fixed and deployed!")

if __name__ == "__main__":
    force_inject()
