#!/usr/bin/env python3
# =====================================================================
# fix.py: Embed complete MSR_LSTAR explanation callout in Module 2
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

MSR_EXPLANATION_BOX = """      <div class="aside-box" style="border-left-color: #0284c7; background: #f0f9ff; margin: 20px 0;">
        <strong style="color: #0369a1; font-size: 1rem;">Deep Dive: What is MSR_LSTAR? (Fast System Call Dispatch)</strong>
        <p style="margin-top: 8px; color: #334155;">
          <strong>MSR_LSTAR</strong> stands for <em>Model-Specific Register: Long System Target Address Register</em> (x86 MSR address <code>0xC0000082</code>). It is a dedicated on-die 64-bit CPU register that holds the kernel's direct system call entry vector.
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 12px 0;">
          <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 12px;">
            <strong style="color: #dc2626; font-size: 0.85rem;">The Legacy Way: INT 0x80 (Slow)</strong>
            <p style="font-size: 0.82rem; color: #64748b; margin-top: 4px; line-height: 1.45;">
              In 32-bit x86, traps were software interrupts. The CPU had to pause execution, read the <em>Interrupt Descriptor Table (IDT)</em> in DRAM, perform permission checks, read the Task State Segment, and push flags to the stack—wasting dozens of clock cycles on memory reads before reaching kernel code.
            </p>
          </div>
          <div style="background: #ffffff; border: 1px solid #bae6fd; border-radius: 6px; padding: 12px;">
            <strong style="color: #0284c7; font-size: 0.85rem;">The Modern 64-bit Way: MSR_LSTAR (Fast)</strong>
            <p style="font-size: 0.82rem; color: #0c4a6e; margin-top: 4px; line-height: 1.45;">
              During boot, the OS kernel writes its entry point into <code>MSR_LSTAR</code> via the privileged <code>wrmsr</code> instruction (<code>entry_SYSCALL_64</code> on Linux, <code>KiSystemCall64</code> on Windows). When a program executes <code>syscall</code>, the CPU bypasses the IDT entirely and jumps directly to <code>MSR_LSTAR</code> in silicon.
            </p>
          </div>
        </div>
        <strong style="color: #0369a1; font-size: 0.88rem;">The Atomic Hardware Microcode Sequence:</strong>
        <p style="margin-top: 4px; color: #334155; font-size: 0.88rem;">
          When an application executes the <code>syscall</code> instruction, the CPU executes an atomic microcode routine:
        </p>
        <ol style="font-size: 0.85rem; color: #334155; margin-left: 20px; line-height: 1.5;">
          <li><strong>Saves Program Counter:</strong> Copies current <code>RIP</code> into register <code>RCX</code> (saving where to return).</li>
          <li><strong>Saves CPU Flags:</strong> Copies <code>RFLAGS</code> into register <code>R11</code>.</li>
          <li><strong>Elevates Privilege:</strong> Flips the internal processor Mode Bit from <strong>Ring 3 (User)</strong> to <strong>Ring 0 (Kernel)</strong>.</li>
          <li><strong>Masks Flags:</strong> Clears unsafe flag bits specified in <code>MSR_FMASK</code> (disabling hardware interrupts while entering).</li>
          <li><strong>Instant Vector Jump:</strong> Loads <code>RIP = MSR_LSTAR</code> with zero memory lookups. The kernel starts running immediately.</li>
        </ol>
      </div>"""

def inject_msr_explanation():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if the explanation box is already present
    if "Deep Dive: What is MSR_LSTAR?" in content:
        print("--> MSR_LSTAR explanation is already present.")
        return

    # Target the TRAP instruction callout box and place the MSR_LSTAR deep dive right after it
    target_needle = '<strong>The TRAP Instruction &amp; System Calls</strong>'
    if target_needle not in content:
        target_needle = '<strong>The TRAP Instruction & System Calls</strong>'

    if target_needle in content:
        # Find the closing tag of this aside-box
        idx = content.find(target_needle)
        end_aside = content.find('</div>', idx) + 6
        content = content[:end_aside] + "\n\n" + MSR_EXPLANATION_BOX.strip() + content[end_aside:]
        print("--> Injected comprehensive MSR_LSTAR callout box.")
    else:
        # Fallback: insert right before the interactive trap simulator
        sim_needle = '<div id="interactive-trap-simulator"'
        idx = content.find(sim_needle)
        if idx != -1:
            content = content[:idx] + MSR_EXPLANATION_BOX.strip() + "\n\n      " + content[idx:]
            print("--> Injected MSR_LSTAR callout box before simulator.")
        else:
            print("--> Error: could not find insertion location.")
            return

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add dedicated MSR_LSTAR technical breakdown callout in Module 2\n\n"
            "Document MSR_LSTAR register mechanics, atomic hardware syscall sequence,\n"
            "and comparison with legacy INT 0x80 IDT lookups in 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for MSR_LSTAR explanation!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    inject_msr_explanation()
