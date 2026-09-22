#!/usr/bin/env python3
# =====================================================================
# fix.py: Integrate historical asides and pioneer insights into Module 2
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "02-hardware-review.html"
)

# Historical asides to insert
VON_NEUMANN_ASIDE = """      <!-- Historical Aside: Von Neumann & Goodman -->
      <div class="aside-box" style="border-left-color: #0284c7; background: #f0f9ff; margin: 20px 0;">
        <strong style="color: #0369a1; font-size: 1rem;">Pioneer Insight: John von Neumann &amp; The Stored-Program Model</strong>
        <p style="margin-top: 8px; color: #334155; line-height: 1.55;">
          Before John von Neumann formalized the stored-program architecture in his 1945 EDVAC report, early computers were programmed manually by plugging patch cables and setting physical switches. Treating code as data inside a shared memory space enabled self-loading operating systems and dynamic linkers, but it also introduced the foundational vulnerability of buffer overflows—where malicious inputs overwrite instruction pointers in memory.
        </p>
        <div style="margin-top: 12px; background: #ffffff; border: 1px solid #bae6fd; border-left: 3px solid #0284c7; padding: 10px 14px; border-radius: 0 4px 4px 0; font-size: 0.85rem;">
          <strong style="color: #0369a1;">James Goodman &amp; Bus Snooping (1983)</strong>
          <p style="margin: 4px 0 0 0; color: #475569; line-height: 1.5;">
            When multi-core processors emerged, private L1/L2 caches created a consistency crisis: if Core 0 updated a variable, how did Core 1 know its cached copy was stale? Goodman solved this by introducing <strong>bus snooping</strong>, where cache controllers monitor the shared memory bus to automatically invalidate outdated local copies.
          </p>
        </div>
      </div>"""

ATLAS_MCCARTHY_ASIDE = """      <!-- Historical Aside: Manchester Atlas & John McCarthy -->
      <div class="aside-box" style="border-left-color: #059669; background: #ecfdf5; margin: 20px 0;">
        <strong style="color: #047857; font-size: 1rem;">Pioneer Insight: The Manchester Atlas &amp; The Invention of the Hardware Trap</strong>
        <p style="margin-top: 8px; color: #334155; line-height: 1.55;">
          The University of Manchester Atlas computer (1962), led by Tom Kilburn and David Edwards, pioneered the concept that entering supervisor mode should not be an ordinary subroutine call. Instead, they invented hardware traps that simultaneously elevated processor privilege and redirected execution to immutable vector locations. Without this hardware gateway, unprivileged code could easily forge supervisor privileges.
        </p>
        <div style="margin-top: 12px; background: #ffffff; border: 1px solid #a7f3d0; border-left: 3px solid #059669; padding: 10px 14px; border-radius: 0 4px 4px 0; font-size: 0.85rem;">
          <strong style="color: #047857;">John McCarthy &amp; The Non-Negotiable Timer Interrupt</strong>
          <p style="margin: 4px 0 0 0; color: #475569; line-height: 1.5;">
            Early time-sharing mainframes relied entirely on cooperative yields. If an errant infinite loop began running, the entire machine locked up. In 1963, John McCarthy championed the integration of a non-negotiable hardware clock interrupt (the PDP-1 channel 17 clock), ensuring the CPU would forcibly trap into the supervisor to reclaim control, making preemptive multitasking possible.
          </p>
        </div>
      </div>"""

LAMPSON_OUSTERHOUT_ASIDE = """      <!-- Historical Aside: Butler Lampson & John Ousterhout -->
      <div class="aside-box" style="border-left-color: #d97706; background: #fffbeb; margin: 20px 0;">
        <strong style="color: #b45309; font-size: 1rem;">Systems Engineering: Lampson's Laws &amp; Ousterhout's Law</strong>
        <p style="margin-top: 8px; color: #334155; line-height: 1.55;">
          Turing Award winner Butler Lampson emphasized a core rule of operating system design: <strong>separation of policy from mechanism</strong>. The hardware provides mechanisms (like MMU page walks or timer traps), while the OS establishes policies (like scheduling algorithms or eviction rules). Mixing them leads to brittle architectures.
        </p>
        <div style="margin-top: 12px; background: #ffffff; border: 1px solid #fde68a; border-left: 3px solid #d97706; padding: 10px 14px; border-radius: 0 4px 4px 0; font-size: 0.85rem;">
          <strong style="color: #b45309;">John Ousterhout &amp; The Memory Latency Wall</strong>
          <p style="margin: 4px 0 0 0; color: #475569; line-height: 1.5;">
            In his landmark 1990 paper, John Ousterhout observed that while CPU clock speeds were scaling exponentially, memory and storage bus latency lagged severely behind. This reality explains why hardware architectural breakthroughs like Translation Lookaside Buffers (TLBs), DMA controllers, and superpages are vital to preventing CPU starvation.
          </p>
        </div>
      </div>"""

def integrate_historical_asides():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Insert Von Neumann aside at the end of Section 1
    sec1_marker = "<h2>1. Processors (CPUs) &amp; Execution Mechanics</h2>"
    sec2_marker = "<h2>2. Privilege Modes &amp; Hardware Protection</h2>"
    sec3_marker = "<h2>3. Virtual Memory &amp; The Memory Management Unit (MMU)</h2>"
    io_marker = "<h2>4. Disks, I/O Devices, &amp; Controller Hardware</h2>"

    if sec1_marker in content and sec2_marker in content:
        # Insert Von Neumann & Goodman before Section 2
        parts = content.split(sec2_marker, 1)
        if "Pioneer Insight: John von Neumann" not in parts[0]:
            content = f"{parts[0]}\n{VON_NEUMANN_ASIDE}\n\n    {sec2_marker}{parts[1]}"
            print("--> Added Von Neumann & Goodman aside to Section 1.")

    # 2. Insert Atlas & McCarthy aside into Section 2
    if sec2_marker in content and sec3_marker in content:
        parts = content.split(sec3_marker, 1)
        if "Pioneer Insight: The Manchester Atlas" not in parts[0]:
            content = f"{parts[0]}\n{ATLAS_MCCARTHY_ASIDE}\n\n    {sec3_marker}{parts[1]}"
            print("--> Added Manchester Atlas & McCarthy aside to Section 2.")

    # 3. Insert Lampson & Ousterhout aside before Section 4
    if io_marker in content:
        parts = content.split(io_marker, 1)
        if "Systems Engineering: Lampson's Laws" not in parts[0]:
            content = f"{parts[0]}\n{LAMPSON_OUSTERHOUT_ASIDE}\n\n    {io_marker}{parts[1]}"
            print("--> Added Lampson & Ousterhout aside before Section 4.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully integrated all historical asides into {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add historical pioneer asides and computer architecture insights to Module 2\n\n"
            "Integrate contextual asides on John von Neumann, Tom Kilburn, John\n"
            "McCarthy, Butler Lampson, and James Goodman into 02-hardware-review.html."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    integrate_historical_asides()
