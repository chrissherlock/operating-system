#!/usr/bin/env python3
# =====================================================================
# fix.py: Add cross-architecture privilege levels deep dive box
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

PRIVILEGE_DEEP_DIVE_HTML = """      <div class="aside-box" style="border-left-color: #7c3aed; background: #fef6ff; margin: 20px 0;">
        <strong style="color: #6d28d9; font-size: 1rem;">Deep Dive: Privilege Hierarchies Across Architectures (Rings, ELs, and Modes)</strong>
        <p style="margin-top: 8px; color: #334155;">
          While the term <strong>\\"Rings\\"</strong> (Ring 0 through Ring 3) is famously associated with x86 architecture (originating from Multics and Intel), the underlying concept of hierarchical hardware privilege is universal. Every modern processor implements multiple execution tiers to isolate untrusted user code from the supervisor kernel and hardware firmware:
        </p>
        <div style="overflow-x: auto; margin: 12px 0;">
          <table style="width: 100%; border-collapse: collapse; font-size: 0.84rem; background: #ffffff; text-align: left;">
            <thead>
              <tr style="background: #f3e8ff; color: #581c87; font-family: var(--font-mono); font-size: 0.75rem; text-transform: uppercase;">
                <th style="padding: 8px 12px; border: 1px solid #d8b4fe;">Processor Architecture</th>
                <th style="padding: 8px 12px; border: 1px solid #d8b4fe;">User / Application Tier</th>
                <th style="padding: 8px 12px; border: 1px solid #d8b4fe;">Kernel / Supervisor Tier</th>
                <th style="padding: 8px 12px; border: 1px solid #d8b4fe;">Virtualization / Firmware Tier</th>
              </tr>
            </thead>
            <tbody style="color: #334155;">
              <tr>
                <td style="padding: 8px 12px; border: 1px solid #e2e8f0; font-weight: 700; color: #7c3aed;">x86-64 (Intel / AMD)</td>
                <td style="padding: 8px 12px; border: 1px solid #e2e8f0;"><strong>Ring 3</strong> (User applications)</td>
                <td style="padding: 8px 12px; border: 1px solid #e2e8f0;"><strong>Ring 0</strong> (OS Kernel)</td>
                <td style="padding: 8px 12px; border: 1px solid #e2e8f0;"><strong>Ring -1 / VMX Root</strong> (Hypervisors)</td>
              </tr>
              <tr style="background: #faf5ff;">
                <td style="padding: 8px 12px; border: 1px solid #e2e8f0; font-weight: 700; color: #7c3aed;">ARM64 (AArch64)</td>
                <td style="padding: 8px 12px; border: 1px solid #e2e8f0;"><strong>EL0</strong> (Apps &amp; OS Daemons)</td>
                <td style="padding: 8px 12px; border: 1px solid #e2e8f0;"><strong>EL1</strong> (OS Kernel / Supervisor)</td>
                <td style="padding: 8px 12px; border: 1px solid #e2e8f0;"><strong>EL2 / EL3</strong> (Hypervisor / Secure Monitor)</td>
              </tr>
              <tr>
                <td style="padding: 8px 12px; border: 1px solid #e2e8f0; font-weight: 700; color: #7c3aed;">RISC-V</td>
                <td style="padding: 8px 12px; border: 1px solid #e2e8f0;"><strong>U-mode</strong> (User Mode)</td>
                <td style="padding: 8px 12px; border: 1px solid #e2e8f0;"><strong>S-mode</strong> (Supervisor Mode)</td>
                <td style="padding: 8px 12px; border: 1px solid #e2e8f0;"><strong>M-mode</strong> (Machine Mode / Firmware)</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p style="margin-top: 8px; color: #334155; font-size: 0.88rem;">
          Regardless of nomenclature, the hardware state machine enforces identical safety guarantees: unprivileged instructions cannot manipulate page tables, modify control registers, or execute raw I/O without trapping through a controlled supervisor gateway.
        </p>
      </div>"""

def add_privilege_hierarchy_deep_dive():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if already added
    if "Deep Dive: Privilege Hierarchies Across Architectures" in content:
        print("--> Privilege hierarchy deep dive box already present.")
        return

    # Find the end of Section 2 narrative or right before Section 3
    section3_marker = '<h2>3. Virtual Memory &amp; The Memory Management Unit (MMU)</h2>'
    if section3_marker in content:
        content = content.replace(section3_marker, PRIVILEGE_DEEP_DIVE_HTML + "\n\n      " + section3_marker)
        print("--> Added cross-architecture privilege deep dive before Section 3.")
    else:
        print("--> Error: Could not locate Section 3 marker in target file.")
        return

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add privilege hierarchies cross-architecture deep dive to Module 2\n\n"
            "Insert a structured Deep Dive callout box comparing x86 rings, ARM exception\n"
            "levels, and RISC-V modes within 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for privilege hierarchies deep dive!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    add_privilege_hierarchy_deep_dive()
