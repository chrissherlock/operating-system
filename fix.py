#!/usr/bin/env python3
# =====================================================================
# fix.py: Cleanly reformat CPU registers and PSW bitfield layout
# =====================================================================
import os
import re
import subprocess

REFINED_REGISTERS_DIAGRAM = """
      <div class="diagram-container" id="svg-key-registers">
        <svg viewBox="0 0 860 410" width="100%" height="auto" style="max-width: 860px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <!-- Outer Boundary -->
          <rect x="15" y="15" width="830" height="380" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" />
          <text x="35" y="42" fill="#0369a1" font-size="13" font-weight="700">CPU INTERNAL REGISTERS &amp; EXECUTION STATE</text>

          <!-- Top Section: 3 Dedicated Columns -->
          <!-- 1. General-Purpose Registers -->
          <g transform="translate(35, 60)">
            <rect x="0" y="0" width="250" height="175" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" />
            <text x="125" y="24" fill="#0f172a" font-size="12" font-weight="700" text-anchor="middle">General-Purpose Registers (GPRs)</text>
            <text x="125" y="40" fill="#64748b" font-size="10" text-anchor="middle">User-Visible Data &amp; Operand Scratchpad</text>

            <rect x="15" y="52" width="220" height="26" rx="3" fill="#ffffff" stroke="#cbd5e1" />
            <text x="25" y="69" fill="#0284c7" font-size="11" font-weight="700">R0 / RAX</text>
            <text x="100" y="69" fill="#475569" font-size="10">Accumulator / Return Val</text>

            <rect x="15" y="82" width="220" height="26" rx="3" fill="#ffffff" stroke="#cbd5e1" />
            <text x="25" y="99" fill="#0284c7" font-size="11" font-weight="700">R1 / RBX</text>
            <text x="100" y="99" fill="#475569" font-size="10">Base / Pointer Data</text>

            <rect x="15" y="112" width="220" height="26" rx="3" fill="#ffffff" stroke="#cbd5e1" />
            <text x="25" y="129" fill="#0284c7" font-size="11" font-weight="700">R2 / RCX</text>
            <text x="100" y="129" fill="#475569" font-size="10">Counter / Loop Index</text>

            <rect x="15" y="142" width="220" height="24" rx="3" fill="#f1f5f9" stroke="#cbd5e1" />
            <text x="125" y="158" fill="#64748b" font-size="10" font-weight="600" text-anchor="middle">R3..Rn-1 (x86-64 / ARM / RISC-V)</text>
          </g>

          <!-- 2. Program Counter -->
          <g transform="translate(305, 60)">
            <rect x="0" y="0" width="250" height="175" rx="6" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" />
            <text x="125" y="24" fill="#0369a1" font-size="12" font-weight="700" text-anchor="middle">Program Counter (PC / IP)</text>
            <text x="125" y="40" fill="#64748b" font-size="10" text-anchor="middle">Instruction Sequencing</text>

            <rect x="15" y="55" width="220" height="105" rx="4" fill="#ffffff" stroke="#0284c7" stroke-width="1" />
            <text x="25" y="80" fill="#0f172a" font-size="11" font-weight="700">Holds Next Instruction Addr</text>
            <text x="25" y="100" fill="#64748b" font-size="10">• Incremented during Fetch</text>
            <text x="25" y="120" fill="#64748b" font-size="10">• Branched via JMP / CALL / RET</text>
            <text x="25" y="140" fill="#64748b" font-size="10">• Traps vector PC to kernel handler</text>
          </g>

          <!-- 3. Stack Pointer -->
          <g transform="translate(575, 60)">
            <rect x="0" y="0" width="250" height="175" rx="6" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" />
            <text x="125" y="24" fill="#0369a1" font-size="12" font-weight="700" text-anchor="middle">Stack Pointer (SP)</text>
            <text x="125" y="40" fill="#64748b" font-size="10" text-anchor="middle">Call Stack Boundary</text>

            <rect x="15" y="55" width="220" height="105" rx="4" fill="#ffffff" stroke="#0284c7" stroke-width="1" />
            <text x="25" y="80" fill="#0f172a" font-size="11" font-weight="700">Points to Top of Active Stack</text>
            <text x="25" y="100" fill="#64748b" font-size="10">• Adjusted on PUSH and POP</text>
            <text x="25" y="120" fill="#64748b" font-size="10">• Tracks Activation Records &amp; Frames</text>
            <text x="25" y="140" fill="#64748b" font-size="10">• Holds Subroutine Return Addrs</text>
          </g>

          <!-- Bottom Section: Full Width Program Status Word (PSW) Bitfield Ribbon -->
          <g transform="translate(35, 250)">
            <rect x="0" y="0" width="790" height="130" rx="6" fill="#f8fafc" stroke="#475569" stroke-width="1.5" />
            <text x="20" y="24" fill="#0f172a" font-size="12" font-weight="700">Program Status Word (PSW / Flags Register)</text>
            <text x="440" y="24" fill="#64748b" font-size="10">Hardware Execution Flags &amp; Protection Level</text>

            <!-- Bitfield Grid Container -->
            <!-- Arithmetic Status Flags (Bits 0-3) -->
            <g transform="translate(20, 36)">
              <rect x="0" y="0" width="750" height="34" fill="#ffffff" stroke="#cbd5e1" />

              <!-- Mode Bit -->
              <rect x="0" y="0" width="130" height="34" fill="#f0fdf4" stroke="#86efac" />
              <text x="65" y="22" fill="#166534" font-size="11" font-weight="700" text-anchor="middle">Mode Bit (0=K, 1=U)</text>

              <!-- Interrupt Enable Bit -->
              <rect x="130" y="0" width="130" height="34" fill="#f0fdf4" stroke="#86efac" />
              <text x="195" y="22" fill="#166534" font-size="11" font-weight="700" text-anchor="middle">Interrupt Bit (IE)</text>

              <!-- IOPL Privilege -->
              <rect x="260" y="0" width="130" height="34" fill="#f0fdf4" stroke="#86efac" />
              <text x="325" y="22" fill="#166534" font-size="11" font-weight="700" text-anchor="middle">IOPL (Rings 0..3)</text>

              <!-- ZF -->
              <rect x="390" y="0" width="90" height="34" fill="#f0f9ff" stroke="#bae6fd" />
              <text x="435" y="22" fill="#0369a1" font-size="11" font-weight="700" text-anchor="middle">ZF (Zero)</text>

              <!-- SF -->
              <rect x="480" y="0" width="90" height="34" fill="#f0f9ff" stroke="#bae6fd" />
              <text x="525" y="22" fill="#0369a1" font-size="11" font-weight="700" text-anchor="middle">SF (Sign)</text>

              <!-- CF -->
              <rect x="570" y="0" width="90" height="34" fill="#f0f9ff" stroke="#bae6fd" />
              <text x="615" y="22" fill="#0369a1" font-size="11" font-weight="700" text-anchor="middle">CF (Carry)</text>

              <!-- OF -->
              <rect x="660" y="0" width="90" height="34" fill="#f0f9ff" stroke="#bae6fd" />
              <text x="705" y="22" fill="#0369a1" font-size="11" font-weight="700" text-anchor="middle">OF (Overflow)</text>
            </g>

            <!-- Bottom Descriptive Labels -->
            <g transform="translate(20, 82)">
              <rect x="0" y="0" width="390" height="36" rx="4" fill="#f0fdf4" stroke="#86efac" />
              <text x="195" y="16" fill="#166534" font-size="10" font-weight="700" text-anchor="middle">Control &amp; Privilege State</text>
              <text x="195" y="29" fill="#15803d" font-size="9" text-anchor="middle">Enforces hardware isolation between OS kernel and user space</text>

              <rect x="390" y="0" width="360" height="36" rx="4" fill="#f0f9ff" stroke="#bae6fd" />
              <text x="570" y="16" fill="#0369a1" font-size="10" font-weight="700" text-anchor="middle">ALU Condition Codes</text>
              <text x="570" y="29" fill="#0284c7" font-size="9" text-anchor="middle">Inspected by conditional branch instructions (JE, JNE, JL, JG)</text>
            </g>
          </g>
        </svg>
      </div>
"""

def reformat_registers_diagram():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'<div class="diagram-container" id="svg-key-registers">.*?</div>\s*</div>'
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, REFINED_REGISTERS_DIAGRAM.strip(), content, flags=re.DOTALL)
        print("--> Replaced #svg-key-registers with clean full-width bitfield layout.")
    else:
        # Fallback search by container id
        pattern_fallback = r'<div class="diagram-container" id="svg-key-registers">.*?</svg>\s*</div>'
        content = re.sub(pattern_fallback, REFINED_REGISTERS_DIAGRAM.strip(), content, flags=re.DOTALL)
        print("--> Replaced #svg-key-registers via fallback pattern.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Redesign PSW bitfield layout in Module 2 register architecture SVG\n\n"
            "Replace cramped vertical column with full-width horizontal bitfield ribbon\n"
            "in week01-operating-system-concepts/02-hardware-review.html to fix overlap."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    reformat_registers_diagram()
