#!/usr/bin/env python3
# =====================================================================
# fix.py: Generalize PCB explanation across Linux, Windows, and microkernels
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "03-os-concepts.html"
)

NEW_PCB_SECTION = r"""    <h4>The Process Control Block (PCB): Cross-Platform Realities</h4>
    <p>
      Because CPU cores can execute only one sequence of instructions at any given instant, the operating system kernel maintains a centralized control structure—the <strong>Process Control Block (PCB)</strong>—to manage identity, ownership, security bounds, and hardware state for every active execution entity.
    </p>
    <p>
      However, the internal implementation of a PCB varies substantially between operating system families:
    </p>

    <div style="overflow-x: auto; margin: 16px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; background: #ffffff;">
        <thead>
          <tr style="background: #f1f5f9; color: #1e293b;">
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Design Dimension</th>
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Linux / Unix (<code>struct task_struct</code>)</th>
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Windows NT (<code>EPROCESS</code> / <code>KPROCESS</code>)</th>
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Microkernels (e.g., seL4 / QNX)</th>
          </tr>
        </thead>
        <tbody style="color: #334155;">
          <tr>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">Entity Philosophy</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Unified scheduler entity. Processes and threads are both represented by <code>task_struct</code>, sharing resources via <code>clone()</code> flags.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Strict container abstraction. An <code>EPROCESS</code> represents address space and resources; execution is delegated entirely to threads (<code>ETHREAD</code>).</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Minimalist capability model. The kernel tracks Thread Control Blocks (TCBs) and capability nodes (Cnodes); process concepts live in user space.</td>
          </tr>
          <tr style="background: #f8fafc;">
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">Identification</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Process ID (PID) and Thread Group ID (TGID).</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Unique Process ID (<code>UniqueProcessId</code>) and Client ID.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Kernel capability references or badge tokens.</td>
          </tr>
          <tr>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">Hardware Register Context</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Stored within kernel stack and <code>thread_struct</code> embedded directly in <code>task_struct</code>.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Absent from <code>EPROCESS</code>; saved exclusively inside individual <code>KTHREAD</code> context frames.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Stored directly in the hardware-mapped register block of the TCB.</td>
          </tr>
          <tr style="background: #f8fafc;">
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">I/O &amp; Object Tracking</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Zero-indexed file descriptor table (<code>struct files_struct</code>) mapping integers to open file descriptions.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Kernel Object Handle Table (<code>ObjectTable</code>) mapping opaque <code>HANDLE</code> pointers with explicit security ACLs.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">IPC endpoint capabilities and notification slots; no internal device or file tables.</td>
          </tr>
          <tr>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">Memory Context Pointer</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;"><code>mm_struct</code> pointer referencing the PML4 root and Virtual Memory Areas (VMAs).</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;"><code>DirectoryTableBase</code> in <code>KPROCESS</code> storing CR3, alongside a Virtual Address Descriptor (VAD) tree.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Page directory capability (VSpace root).</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h4>Key Elements Universal to All PCBs</h4>
    <p>
      Despite naming differences across kernel architectures, any production operating system maintains the following core invariants inside or associated with its process control tracking:
    </p>
    <ul>
      <li><strong>Architectural Root Anchor:</strong> A hardware-mandated pointer to the top-level page table (e.g., <code>CR3</code> on x86-64, <code>TTBR0</code> on ARM64) enabling the MMU to swap address spaces during context switches.</li>
      <li><strong>Execution State Tracking:</strong> Flags denoting whether the entity is active, ready to run, sleeping on a synchronization primitive, or in a zombie/terminated state awaiting cleanup.</li>
      <li><strong>Security Token &amp; Credentials:</strong> User/group identifiers (POSIX UID/GID) or Windows Access Tokens specifying privileges, security identifiers (SIDs), and audit policies.</li>
      <li><strong>Resource Descriptors &amp; Limits:</strong> Quotas and references to system resources, including CPU affinity masks, memory working-set limits, and tables mapping private application references to underlying kernel objects.</li>
    </ul>"""

def update_pcb_content():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Define old PCB section markers
    start_marker = "<h4>The Process Control Block (PCB)</h4>"
    end_marker = "<h4>Process State Transitions: The Three-State Model</h4>"

    if start_marker not in content or end_marker not in content:
        print("--> Error: Could not locate PCB section boundaries.")
        return

    prefix = content.split(start_marker)[0]
    suffix = content.split(end_marker)[1]

    updated_html = f"{prefix}{NEW_PCB_SECTION}\n\n    {end_marker}{suffix}"

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_html)

    print(f"--> Generalized PCB section in {TARGET_FILE} across Linux, Windows NT, and microkernels.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Generalize PCB section to cover Windows EPROCESS and cross-platform designs\n\n"
            "Expand Section 1 of 03-os-concepts.html beyond Unix/Linux to detail how\n"
            "Windows NT (EPROCESS/KPROCESS) and microkernels structure process control\n"
            "blocks and separate thread execution from process resource containers."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for cross-platform PCB update!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_pcb_content()
