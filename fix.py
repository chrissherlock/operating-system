#!/usr/bin/env python3
# =====================================================================
# fix.py: Inject CPU Register Architecture & PSW diagram into Module 2
# =====================================================================
import os
import re
import subprocess

SVG_REGISTERS_DIAGRAM = """
      <div class="diagram-container" id="svg-key-registers">
        <svg viewBox="0 0 860 380" width="100%" height="auto" style="max-width: 860px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <!-- Outer Box -->
          <rect x="20" y="20" width="820" height="340" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" />
          <text x="40" y="48" fill="#0369a1" font-size="13" font-weight="700">CPU INTERNAL REGISTERS &amp; EXECUTION STATE</text>

          <!-- Left Column: General Purpose Registers -->
          <g transform="translate(40, 70)">
            <rect x="0" y="0" width="240" height="265" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" />
            <text x="120" y="25" fill="#0f172a" font-size="12" font-weight="700" text-anchor="middle">General-Purpose (GPRs)</text>
            <text x="120" y="42" fill="#64748b" font-size="10" text-anchor="middle">User-Visible Scratchpad Storage</text>

            <!-- GPR list items -->
            <rect x="15" y="55" width="210" height="30" rx="4" fill="#ffffff" stroke="#cbd5e1" />
            <text x="25" y="75" fill="#0284c7" font-size="11" font-weight="700">R0 / RAX</text>
            <text x="120" y="75" fill="#475569" font-size="10">Accumulator / Return</text>

            <rect x="15" y="92" width="210" height="30" rx="4" fill="#ffffff" stroke="#cbd5e1" />
            <text x="25" y="112" fill="#0284c7" font-size="11" font-weight="700">R1 / RBX</text>
            <text x="120" y="112" fill="#475569" font-size="10">Base / General Data</text>

            <rect x="15" y="129" width="210" height="30" rx="4" fill="#ffffff" stroke="#cbd5e1" />
            <text x="25" y="149" fill="#0284c7" font-size="11" font-weight="700">R2 / RCX</text>
            <text x="120" y="149" fill="#475569" font-size="10">Counter / Loop Variable</text>

            <rect x="15" y="166" width="210" height="30" rx="4" fill="#ffffff" stroke="#cbd5e1" />
            <text x="25" y="186" fill="#0284c7" font-size="11" font-weight="700">R3 / RDX</text>
            <text x="120" y="186" fill="#475569" font-size="10">Data / I/O Destination</text>

            <rect x="15" y="203" width="210" height="42" rx="4" fill="#f1f5f9" stroke="#cbd5e1" />
            <text x="120" y="222" fill="#64748b" font-size="10" font-weight="600" text-anchor="middle">R4 ... Rn-1 (x86-64 / ARM)</text>
            <text x="120" y="236" fill="#94a3b8" font-size="9" text-anchor="middle">Passed Parameters &amp; Temps</text>
          </g>

          <!-- Middle Column: Special Pointer Registers -->
          <g transform="translate(305, 70)">
            <rect x="0" y="0" width="240" height="265" rx="6" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" />
            <text x="120" y="25" fill="#0369a1" font-size="12" font-weight="700" text-anchor="middle">Control &amp; Pointers</text>
            <text x="120" y="42" fill="#64748b" font-size="10" text-anchor="middle">Special CPU Execution Vectors</text>

            <!-- PC -->
            <rect x="15" y="55" width="210" height="85" rx="4" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" />
            <text x="25" y="78" fill="#0284c7" font-size="12" font-weight="700">Program Counter (PC)</text>
            <text x="25" y="96" fill="#0f172a" font-size="10" font-weight="600">Holds Next Instruction Addr</text>
            <text x="25" y="112" fill="#64748b" font-size="9">Auto-incremented on Fetch</text>
            <text x="25" y="126" fill="#64748b" font-size="9">Modified by JMP, CALL, RET</text>

            <!-- SP -->
            <rect x="15" y="152" width="210" height="95" rx="4" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" />
            <text x="25" y="175" fill="#0284c7" font-size="12" font-weight="700">Stack Pointer (SP)</text>
            <text x="25" y="193" fill="#0f172a" font-size="10" font-weight="600">Points to Call Stack Top</text>
            <text x="25" y="209" fill="#64748b" font-size="9">Tracks Local Stack Frames</text>
            <text x="25" y="223" fill="#64748b" font-size="9">Updated via PUSH / POP</text>
            <text x="25" y="237" fill="#64748b" font-size="9">Subroutines &amp; Return Addrs</text>
          </g>

          <!-- Right Column: Program Status Word (PSW) -->
          <g transform="translate(570, 70)">
            <rect x="0" y="0" width="250" height="265" rx="6" fill="#f8fafc" stroke="#475569" stroke-width="1.5" />
            <text x="125" y="25" fill="#0f172a" font-size="12" font-weight="700" text-anchor="middle">Program Status Word (PSW)</text>
            <text x="125" y="42" fill="#64748b" font-size="10" text-anchor="middle">Hardware State &amp; Privilege Flags</text>

            <!-- Arithmetic Status Flags -->
            <rect x="15" y="55" width="220" height="90" rx="4" fill="#ffffff" stroke="#cbd5e1" />
            <text x="25" y="75" fill="#1e293b" font-size="11" font-weight="700">Condition Codes (ALU Flags)</text>
            <text x="25" y="93" fill="#475569" font-size="10"><strong>ZF:</strong> Zero Result</text>
            <text x="130" y="93" fill="#475569" font-size="10"><strong>SF:</strong> Negative / Sign</text>
            <text x="25" y="111" fill="#475569" font-size="10"><strong>CF:</strong> Unsigned Carry</text>
            <text x="130" y="111" fill="#475569" font-size="10"><strong>OF:</strong> Signed Overflow</text>
            <text x="25" y="130" fill="#64748b" font-size="9">Evaluated by conditional branches (JE, JNE)</text>

            <!-- Control & Privilege Flags -->
            <rect x="15" y="155" width="220" height="92" rx="4" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5" />
            <text x="25" y="176" fill="#166534" font-size="11" font-weight="700">Control &amp; OS Privilege Bits</text>

            <rect x="25" y="185" width="100" height="24" rx="3" fill="#ffffff" stroke="#86efac" />
            <text x="75" y="201" fill="#166534" font-size="10" font-weight="700" text-anchor="middle">Mode Bit</text>
            <text x="135" y="201" fill="#166534" font-size="9">0 = Kernel, 1 = User</text>

            <rect x="25" y="214" width="100" height="24" rx="3" fill="#ffffff" stroke="#86efac" />
            <text x="75" y="230" fill="#166534" font-size="10" font-weight="700" text-anchor="middle">Interrupt Bit</text>
            <text x="135" y="230" fill="#166534" font-size="9">1 = Enabled, 0 = Masked</text>
          </g>
        </svg>
      </div>
"""

def inject_registers_diagram():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Insert Register Diagram after the Key Processor Registers list
    if 'id="svg-key-registers"' not in content:
        target_marker = "<li><strong>Program Status Word (PSW):</strong> Contains condition code bits (carry, overflow, zero, sign), CPU priority level, mode bits (user vs. kernel mode), and interrupt enablement flags.</li>\n      </ul>"
        if target_marker in content:
            content = content.replace(target_marker, f"{target_marker}\n{SVG_REGISTERS_DIAGRAM}")
            print("--> Injected Key Processor Registers SVG diagram.")
        else:
            # Fallback regex pattern matching the PSW list item
            pattern = r"(<li><strong>Program Status Word \(PSW\):</strong>.*?</li>\s*</ul>)"
            content = re.sub(pattern, f"\\1\n{SVG_REGISTERS_DIAGRAM}", content, count=1, flags=re.DOTALL)
            print("--> Injected Key Processor Registers SVG diagram via fallback pattern.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Add CPU register architecture and PSW layout SVG diagram to Module 2\n\n"
            "Update week01-operating-system-concepts/02-hardware-review.html with a\n"
            "vector diagram detailing GPRs, PC, SP, and the Program Status Word (PSW)."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    inject_registers_diagram()
