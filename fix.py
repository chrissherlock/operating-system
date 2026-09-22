#!/usr/bin/env python3
# =====================================================================
# fix.py: Add 7-state process model and SVG diagram to 03-os-concepts.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "03-os-concepts.html"
)

SEVEN_STATE_SECTION = r"""    <h4>Virtual Memory Realities: The Seven-State Process Model</h4>
    <p>
      While the 5-state model accounts for lifecycle boundaries, it implicitly assumes that all active processes reside permanently in physical RAM. In reality, modern systems frequently face memory overcommitment—where the aggregate virtual address spaces of all runnable and blocked processes exceed physical DRAM capacity.
    </p>
    <p>
      To prevent the system from crashing under memory exhaustion, the operating system introduces a <strong>Medium-Term Scheduler (The Swapper)</strong>. The swapper moves dormant or blocked processes from physical RAM to secondary backing stores (a swap partition, swapfile, or pagefile), introducing two distinct <strong>suspended states</strong> and giving rise to the classical <strong>Seven-State Model</strong>:
    </p>

    <ul>
      <li><strong>Ready (In-Memory):</strong> The process resides in physical DRAM and is ready for the dispatcher to schedule onto an available CPU core.</li>
      <li><strong>Blocked (In-Memory):</strong> The process resides in physical DRAM, but is waiting for an external event (I/O completion, timer, mutex).</li>
      <li><strong>Blocked / Suspended (On Disk):</strong> The process was waiting for an event and, to relieve severe memory pressure, the OS swapped its address space out to disk. It cannot run even if a CPU is idle.</li>
      <li><strong>Ready / Suspended (On Disk):</strong> The event the process was waiting for has completed, or a runnable process was swapped to disk. The process is ready to execute instructions immediately once the OS swaps its working set back into physical DRAM.</li>
    </ul>

    <!-- Diagram 2c: Seven-State Process Lifecycle -->
    <div style="display: flex; justify-content: center; margin: 28px 0;">
      <svg viewBox="0 0 860 480" width="100%" height="100%" style="max-width: 860px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="trans7-arrow-blue" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#0284c7" />
          </marker>
          <marker id="trans7-arrow-slate" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#64748b" />
          </marker>
          <marker id="trans7-arrow-red" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#ef4444" />
          </marker>
          <marker id="trans7-arrow-green" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#059669" />
          </marker>
          <marker id="trans7-arrow-amber" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#d97706" />
          </marker>
          <marker id="trans7-arrow-purple" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#9333ea" />
          </marker>
          <filter id="node7-shadow" x="-8%" y="-8%" width="116%" height="116%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.08" />
          </filter>
        </defs>

        <!-- Canvas Background Zones -->
        <!-- In-Memory Zone -->
        <rect x="15" y="40" width="830" height="230" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-dasharray="4,4" />
        <text x="30" y="60" fill="#475569" font-size="9" font-weight="700">PRIMARY MEMORY (PHYSICAL RAM - ACTIVE)</text>

        <!-- Swapped Backing Store Zone -->
        <rect x="15" y="290" width="830" height="170" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-dasharray="4,4" />
        <text x="30" y="310" fill="#475569" font-size="9" font-weight="700">SECONDARY STORAGE (SWAPFILE / BACKING STORE - SUSPENDED)</text>

        <!-- 1. NEW STATE -->
        <g transform="translate(75, 135)" filter="url(#node7-shadow)">
          <circle cx="0" cy="0" r="38" fill="#ffffff" stroke="#94a3b8" stroke-width="2" />
          <text x="0" y="-4" fill="#334155" font-size="11" font-weight="700" text-anchor="middle">NEW</text>
          <text x="0" y="10" fill="#64748b" font-size="7.5" text-anchor="middle">Created</text>
        </g>

        <!-- Transition: New -> Ready -->
        <path d="M 113,135 L 182,135" fill="none" stroke="#0284c7" stroke-width="1.8" marker-end="url(#trans7-arrow-blue)" />
        <text x="147" y="127" fill="#0369a1" font-size="7.5" font-weight="700" text-anchor="middle">Admit</text>

        <!-- Transition: New -> Ready/Suspended (Direct Admit to Swap) -->
        <path d="M 95,168 C 115,225 150,335 202,370" fill="none" stroke="#9333ea" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#trans7-arrow-purple)" />
        <text x="125" y="270" fill="#7e22ce" font-size="7" font-weight="600">Admit (Overcommit)</text>

        <!-- 2. READY STATE (In-Memory) -->
        <g transform="translate(225, 135)" filter="url(#node7-shadow)">
          <circle cx="0" cy="0" r="42" fill="#eff6ff" stroke="#0284c7" stroke-width="2" />
          <text x="0" y="-4" fill="#0369a1" font-size="11" font-weight="700" text-anchor="middle">READY</text>
          <text x="0" y="10" fill="#64748b" font-size="7.5" text-anchor="middle">In Memory</text>
        </g>

        <!-- 3. RUNNING STATE -->
        <g transform="translate(500, 135)" filter="url(#node7-shadow)">
          <circle cx="0" cy="0" r="42" fill="#ecfdf5" stroke="#059669" stroke-width="2" />
          <text x="0" y="-4" fill="#065f46" font-size="11" font-weight="700" text-anchor="middle">RUNNING</text>
          <text x="0" y="10" fill="#047857" font-size="7.5" text-anchor="middle">On CPU Core</text>
        </g>

        <!-- Transition: Ready -> Running (Dispatch) -->
        <path d="M 264,120 C 330,95 395,95 461,120" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#trans7-arrow-blue)" />
        <text x="362" y="96" fill="#0369a1" font-size="8" font-weight="700" text-anchor="middle">Dispatch</text>

        <!-- Transition: Running -> Ready (Preempt) -->
        <path d="M 461,150 C 395,175 330,175 264,150" fill="none" stroke="#64748b" stroke-width="1.8" stroke-dasharray="4,4" marker-end="url(#trans7-arrow-slate)" />
        <text x="362" y="180" fill="#475569" font-size="8" font-weight="600" text-anchor="middle">Timeout / Preempt</text>

        <!-- 4. BLOCKED STATE (In-Memory) -->
        <g transform="translate(670, 135)" filter="url(#node7-shadow)">
          <circle cx="0" cy="0" r="42" fill="#fef2f2" stroke="#ef4444" stroke-width="2" />
          <text x="0" y="-4" fill="#991b1b" font-size="11" font-weight="700" text-anchor="middle">BLOCKED</text>
          <text x="0" y="10" fill="#b91c1c" font-size="7.5" text-anchor="middle">In Memory</text>
        </g>

        <!-- Transition: Running -> Blocked -->
        <path d="M 542,135 L 626,135" fill="none" stroke="#ef4444" stroke-width="1.8" marker-end="url(#trans7-arrow-red)" />
        <text x="584" y="127" fill="#b91c1c" font-size="7.5" font-weight="700" text-anchor="middle">Event Wait</text>

        <!-- Transition: Blocked -> Ready -->
        <path d="M 660,95 C 630,60 310,40 240,96" fill="none" stroke="#059669" stroke-width="1.8" marker-end="url(#trans7-arrow-green)" />
        <text x="450" y="58" fill="#065f46" font-size="7.5" font-weight="700" text-anchor="middle">Event Occurred</text>

        <!-- Transition: Running -> Terminated -->
        <path d="M 500,93 L 500,45 C 500,30 750,30 775,88" fill="none" stroke="#d97706" stroke-width="1.8" marker-end="url(#trans7-arrow-amber)" />
        <text x="740" y="44" fill="#92400e" font-size="7.5" font-weight="700" text-anchor="middle">Exit / Release</text>

        <!-- 5. TERMINATED STATE -->
        <g transform="translate(780, 135)" filter="url(#node7-shadow)">
          <circle cx="0" cy="0" r="38" fill="#fffbeb" stroke="#d97706" stroke-width="2" />
          <text x="0" y="-4" fill="#92400e" font-size="10.5" font-weight="700" text-anchor="middle">TERMINATED</text>
          <text x="0" y="10" fill="#78350f" font-size="7" text-anchor="middle">Zombie</text>
        </g>

        <!-- ==================== SWAPPED STATES (LOWER TIER) ==================== -->

        <!-- 6. READY / SUSPENDED -->
        <g transform="translate(245, 385)" filter="url(#node7-shadow)">
          <circle cx="0" cy="0" r="44" fill="#faf5ff" stroke="#9333ea" stroke-width="2" />
          <text x="0" y="-10" fill="#7e22ce" font-size="9.5" font-weight="700" text-anchor="middle">READY /</text>
          <text x="0" y="4" fill="#7e22ce" font-size="9.5" font-weight="700" text-anchor="middle">SUSPENDED</text>
          <text x="0" y="18" fill="#6b21a8" font-size="7" text-anchor="middle">(On Disk)</text>
        </g>

        <!-- 7. BLOCKED / SUSPENDED -->
        <g transform="translate(670, 385)" filter="url(#node7-shadow)">
          <circle cx="0" cy="0" r="44" fill="#fff1f2" stroke="#e11d48" stroke-width="2" />
          <text x="0" y="-10" fill="#be123c" font-size="9.5" font-weight="700" text-anchor="middle">BLOCKED /</text>
          <text x="0" y="4" fill="#be123c" font-size="9.5" font-weight="700" text-anchor="middle">SUSPENDED</text>
          <text x="0" y="18" fill="#9f1239" font-size="7" text-anchor="middle">(On Disk)</text>
        </g>

        <!-- Vertical Swap Transitions: Ready <-> Ready/Suspended -->
        <path d="M 215,177 L 215,340" fill="none" stroke="#9333ea" stroke-width="1.8" marker-end="url(#trans7-arrow-purple)" />
        <text x="180" y="255" fill="#7e22ce" font-size="7.5" font-weight="700" text-anchor="middle">Suspend (Swap Out)</text>

        <path d="M 245,340 L 245,178" fill="none" stroke="#0284c7" stroke-width="1.8" marker-end="url(#trans7-arrow-blue)" />
        <text x="282" y="255" fill="#0369a1" font-size="7.5" font-weight="700" text-anchor="middle">Activate (Swap In)</text>

        <!-- Vertical Swap Transitions: Blocked <-> Blocked/Suspended -->
        <path d="M 660,177 L 660,340" fill="none" stroke="#e11d48" stroke-width="1.8" marker-end="url(#trans7-arrow-red)" />
        <text x="625" y="255" fill="#be123c" font-size="7.5" font-weight="700" text-anchor="middle">Suspend (Swap Out)</text>

        <path d="M 685,340 L 685,178" fill="none" stroke="#059669" stroke-width="1.8" marker-end="url(#trans7-arrow-green)" />
        <text x="722" y="255" fill="#065f46" font-size="7.5" font-weight="700" text-anchor="middle">Activate (Swap In)</text>

        <!-- Horizontal Transition on Disk: Blocked/Suspended -> Ready/Suspended -->
        <path d="M 625,385 L 291,385" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#trans7-arrow-green)" />
        <rect x="405" y="375" width="115" height="18" rx="3" fill="#ffffff" stroke="#86efac" />
        <text x="462" y="388" fill="#065f46" font-size="7.5" font-weight="700" text-anchor="middle">Event Occurs (While Swapped)</text>
      </svg>
    </div>

    <h4>Key Swapping Dynamics in the Seven-State Model</h4>
    <ul>
      <li><strong>Autonomous Event Completion in Storage:</strong> Notice the horizontal transition from <code>Blocked/Suspended</code> to <code>Ready/Suspended</code>. When a hardware I/O request finishes for a swapped-out process, the interrupt service routine updates the PCB in kernel memory immediately—moving it to the Ready/Suspended queue without requiring an expensive page-in until memory pressure subsides.</li>
      <li><strong>Swapping Policy Trade-offs:</strong> The OS prioritizes swapping out <em>Blocked</em> processes over <em>Ready</em> ones, as blocked jobs cannot utilize CPU cycles anyway. However, if severe memory starvation persists, even Ready processes are suspended to allow remaining tasks to finish without destructive page thrashing.</li>
    </ul>"""

def update_process_lifecycle_section():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Search for the old seven-state placeholder/section
    # In earlier scripts, it started with <h4>Virtual Memory Realities: The Seven-State Model</h4>
    # and ended right before <h3>2. Address Spaces
    old_start = "<h4>Virtual Memory Realities: The Seven-State Model</h4>"
    sec2_start = "<h3>2. Address Spaces &amp; Virtual Memory"

    if old_start in content and sec2_start in content:
        part_before = content.split(old_start)[0]
        part_after = content.split(sec2_start)[1]
        content = f"{part_before}{SEVEN_STATE_SECTION}\n\n    {sec2_start}{part_after}"
        print("--> Replaced older seven-state placeholder with full 7-state model and diagram.")
    else:
        # Fallback: look for </svg>\n    </div> before Section 2
        sec2_pos = content.find(sec2_start)
        if sec2_pos != -1:
            # Find the closing </div> of Diagram 2b
            prev_div = content.rfind("</div>", 0, sec2_pos)
            if prev_div != -1:
                content = content[:prev_div + 6] + "\n\n" + SEVEN_STATE_SECTION + "\n\n    " + content[sec2_pos:]
                print("--> Appended 7-state section using relative diagram anchor.")
            else:
                print("--> Error: Could not locate insertion point before Section 2.")
                return
        else:
            print(f"--> Error: Could not locate Section 2 in {TARGET_FILE}.")
            return

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Saved complete 7-state process model to {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add comprehensive seven-state process model and diagram to Module 3\n\n"
            "Expand Section 1 of 03-os-concepts.html to detail the seven-state model\n"
            "governing medium-term scheduling, swapping, and suspended states under\n"
            "memory pressure, complete with a dedicated two-tier SVG diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for Seven-State model!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_process_lifecycle_section()
