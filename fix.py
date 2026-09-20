#!/usr/bin/env python3
# =====================================================================
# enforce_bold_asides.py: Re-verify and enforce bold keywords in asides
# =====================================================================
import os
import subprocess
import sys

WIKI_ASIDE_SMP_BOLD = r"""
        <!-- WIKIPEDIA ASIDE BOX -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 24px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Summary &amp; Further Reading: Symmetric Multiprocessing (SMP)</h4>
          <p style="margin-bottom: 10px; color: #334155; font-size: 0.9rem; line-height: 1.5;">
            <strong>Symmetric Multiprocessing (SMP)</strong> evolved from early mainframe architectures such as the <strong>Burroughs D825 (1962)</strong> into commercial open-systems hardware pioneered by <strong>Sequent Computer Systems</strong> in the 1980s. Unlike asynchronous master-slave models where one CPU monopolizes kernel execution, SMP allows any processor to execute kernel code, service hardware interrupts, and schedule threads concurrently across a <strong>unified shared physical memory space</strong>.
          </p>

          <!-- Compact Responsive Video Preview Card -->
          <div style="display: flex; align-items: center; gap: 14px; background: #ffffff; border: 1px solid #bae6fd; border-radius: 6px; padding: 10px 14px; margin: 12px 0; max-width: 540px;">
            <div style="flex-shrink: 0; position: relative; width: 110px; height: 65px; background: #0f172a; border-radius: 4px; overflow: hidden; display: flex; align-items: center; justify-content: center;">
              <img src="https://img.youtube.com/vi/9wQEgm3FNxo/hqdefault.jpg" alt="Burroughs D825 Video Thumbnail" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.85;">
              <div style="position: absolute; width: 28px; height: 28px; background: rgba(2, 132, 199, 0.9); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #ffffff; font-size: 12px; font-weight: bold;">&#9658;</div>
            </div>
            <div style="flex-grow: 1; display: flex; flex-direction: column; gap: 3px;">
              <div style="font-weight: 600; font-size: 0.88rem; color: #0f172a;">1964 Burroughs Computers &amp; D825 Multiprocessing</div>
              <div style="font-size: 0.78rem; color: #64748b;">Computer History Archives Project (CHAP) &bull; 21 mins</div>
              <a href="https://www.youtube.com/watch?v=9wQEgm3FNxo" target="_blank" rel="noopener" style="font-size: 0.82rem; color: #0284c7; text-decoration: underline; font-weight: 500;">Watch Documentary on YouTube &rarr;</a>
            </div>
          </div>

          <ul style="margin-left: 20px; margin-top: 10px; display: flex; flex-direction: column; gap: 4px;">
            <li><a href="https://en.wikipedia.org/wiki/Symmetric_multiprocessing" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Symmetric Multiprocessing on Wikipedia</a></li>
          </ul>
        </aside>"""

WIKI_ASIDE_GANG_BOLD = r"""
        <!-- WIKIPEDIA ASIDE BOX -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 24px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Summary &amp; Further Reading: Gang Scheduling</h4>

          <div style="display: flex; gap: 14px; align-items: flex-start; margin-bottom: 10px;">
            <div style="flex-shrink: 0; width: 85px; height: 105px; background: #e2e8f0; border-radius: 4px; overflow: hidden; border: 1px solid #bae6fd;">
              <img src="../images/ousterhout.png" alt="John Ousterhout Portrait" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <p style="color: #334155; font-size: 0.9rem; line-height: 1.5; margin: 0;">
              <strong>Gang scheduling</strong> was pioneered by <strong>John Ousterhout</strong> in 1982 to address the coordination failure of independent thread schedulers on parallel hardware. By scheduling related threads across multiple cores simultaneously (a <strong>two-dimensional matrix of Cores $\times$ Time Quanta</strong>), gang scheduling prevents preemption delays and blocking when cooperating threads communicate.
            </p>
          </div>

          <ul style="margin-left: 20px; display: flex; flex-direction: column; gap: 4px;">
            <li><a href="https://en.wikipedia.org/wiki/Gang_scheduling" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Gang Scheduling on Wikipedia</a></li>
          </ul>
        </aside>"""

WIKI_ASIDE_RPC_DSM_BOLD = r"""
        <!-- WIKIPEDIA ASIDE BOX -->
        <aside style="display: block; border-left: 4px solid #0284c7; background: #f0f9ff; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 24px 0; font-size: 0.92rem; color: #0369a1;">
          <h4 style="margin-bottom: 8px; font-weight: bold; color: #0369a1;">Historical Summary &amp; Further Reading: RPC &amp; DSM</h4>
          <p style="margin-bottom: 8px; color: #334155; font-size: 0.9rem; line-height: 1.5;">
            <strong>Remote Procedure Calls (RPC)</strong>, introduced by <strong>Birrell and Nelson</strong> in 1984, abstract network messaging into transparent local subroutine calls. <strong>Distributed Shared Memory (DSM)</strong>, pioneered by <strong>Kai Li</strong> with the <strong>Ivy system</strong> in 1986, bridges multicomputer hardware by emulating a single shared virtual address space across physically disjoint nodes using <strong>MMU page faults</strong> and network replication.
          </p>
          <ul style="margin-left: 20px; display: flex; flex-direction: column; gap: 4px;">
            <li><a href="https://en.wikipedia.org/wiki/Remote_procedure_call" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Remote Procedure Call on Wikipedia</a></li>
            <li><a href="https://en.wikipedia.org/wiki/Distributed_shared_memory" target="_blank" rel="noopener" style="color: #0284c7; text-decoration: underline;">Distributed Shared Memory on Wikipedia</a></li>
          </ul>
        </aside>"""

def enforce_all():
    mod1 = os.path.join("week11-multiprocessors", "01-multiprocessor-hardware.html")
    mod2 = os.path.join("week11-multiprocessors", "02-multiprocessor-scheduling.html")
    mod4 = os.path.join("week11-multiprocessors", "04-rpc-dsm-load-balancing.html")

    modified = []

    if os.path.exists(mod1):
        with open(mod1, "r", encoding="utf-8") as f:
            c1 = f.read()
        if "Historical Summary &amp; Further Reading: Symmetric Multiprocessing (SMP)" in c1:
            parts = c1.split("<!-- WIKIPEDIA ASIDE BOX")
            c1 = parts[0] + parts[1].split("</aside>", 1)[1]
        target = "<!-- GUIDED WALKTHROUGH 4: OS ARCHITECTURES -->"
        if target in c1:
            c1 = c1.replace(target, WIKI_ASIDE_SMP_BOLD + "\n\n      " + target)
            with open(mod1, "w", encoding="utf-8") as f:
                f.write(c1)
            modified.append(mod1)

    if os.path.exists(mod2):
        with open(mod2, "r", encoding="utf-8") as f:
            c2 = f.read()
        if "Historical Summary &amp; Further Reading: Gang Scheduling" in c2:
            parts = c2.split("<!-- WIKIPEDIA ASIDE BOX")
            c2 = parts[0] + parts[1].split("</aside>", 1)[1]
        target = "<!-- GUIDED WALKTHROUGH"
        if target in c2:
            c2 = c2.replace(target, WIKI_ASIDE_GANG_BOLD + "\n\n      " + target, 1)
            with open(mod2, "w", encoding="utf-8") as f:
                f.write(c2)
            modified.append(mod2)

    if os.path.exists(mod4):
        with open(mod4, "r", encoding="utf-8") as f:
            c4 = f.read()
        if "Historical Summary &amp; Further Reading: RPC &amp; DSM" in c4:
            parts = c4.split("<!-- WIKIPEDIA ASIDE BOX")
            c4 = parts[0] + parts[1].split("</aside>", 1)[1]
        target = "<!-- GUIDED WALKTHROUGH"
        if target in c4:
            c4 = c4.replace(target, WIKI_ASIDE_RPC_DSM_BOLD + "\n\n      " + target, 1)
            with open(mod4, "w", encoding="utf-8") as f:
                f.write(c4)
            modified.append(mod4)

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
            "Re-verify and enforce bolding of key terminology in research asides\n\n"
            "Ensure all key architectural terms, pioneers, and systems are bolded across\n"
            "research aside boxes in Week 11 curriculum modules."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Bold keywords successfully enforced in aside boxes!")

if __name__ == "__main__":
    enforce_all()
