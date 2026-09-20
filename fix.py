#!/usr/bin/env python3
# =====================================================================
# fix.py: Inject CPU cycle and pipeline SVG diagrams into Module 2
# =====================================================================
import os
import re
import subprocess

SVG_CPU_CYCLE = """
      <div class="diagram-container" id="svg-cpu-cycle">
        <svg viewBox="0 0 840 320" width="100%" height="auto" style="max-width: 840px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="arrowCycle" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#0284c7" />
            </marker>
            <marker id="arrowData" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#475569" />
            </marker>
          </defs>

          <!-- Main Memory / Bus Box -->
          <rect x="30" y="40" width="170" height="230" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
          <text x="115" y="70" fill="#0f172a" font-size="13" font-weight="700" text-anchor="middle">Main Memory</text>
          <text x="115" y="88" fill="#64748b" font-size="10" text-anchor="middle">(Instructions &amp; Data)</text>

          <rect x="50" y="115" width="130" height="36" rx="4" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.5" />
          <text x="115" y="138" fill="#0284c7" font-size="11" font-weight="600" text-anchor="middle">Code Segment</text>

          <rect x="50" y="165" width="130" height="36" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
          <text x="115" y="188" fill="#475569" font-size="11" font-weight="600" text-anchor="middle">Data Segment</text>

          <rect x="50" y="215" width="130" height="36" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
          <text x="115" y="238" fill="#475569" font-size="11" font-weight="600" text-anchor="middle">Stack Segment</text>

          <!-- CPU Core Boundary -->
          <rect x="250" y="25" width="560" height="265" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2" />
          <text x="270" y="52" fill="#0284c7" font-size="13" font-weight="700">CPU Core Architecture</text>

          <!-- Registers & PC Block -->
          <rect x="280" y="80" width="130" height="70" rx="6" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" />
          <text x="345" y="105" fill="#0369a1" font-size="12" font-weight="700" text-anchor="middle">1. FETCH</text>
          <text x="345" y="123" fill="#0f172a" font-size="11" font-weight="600" text-anchor="middle">Program Counter</text>
          <text x="345" y="139" fill="#64748b" font-size="10" text-anchor="middle">Points to PC Address</text>

          <!-- Instruction Register & Decoder -->
          <rect x="460" y="80" width="140" height="70" rx="6" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" />
          <text x="530" y="105" fill="#0369a1" font-size="12" font-weight="700" text-anchor="middle">2. DECODE</text>
          <text x="530" y="123" fill="#0f172a" font-size="11" font-weight="600" text-anchor="middle">Instruction Decoder</text>
          <text x="530" y="139" fill="#64748b" font-size="10" text-anchor="middle">Extract Opcode / Regs</text>

          <!-- Execution ALU -->
          <rect x="650" y="80" width="130" height="70" rx="6" fill="#0284c7" stroke="#0369a1" stroke-width="1.5" />
          <text x="715" y="105" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">3. EXECUTE</text>
          <text x="715" y="123" fill="#ffffff" font-size="11" font-weight="600" text-anchor="middle">ALU &amp; Shifter</text>
          <text x="715" y="139" fill="#e0f2fe" font-size="10" text-anchor="middle">Math / Logic / Branch</text>

          <!-- Register File & Writeback -->
          <rect x="420" y="195" width="220" height="65" rx="6" fill="#f8fafc" stroke="#64748b" stroke-width="1.5" />
          <text x="530" y="218" fill="#0f172a" font-size="12" font-weight="700" text-anchor="middle">General Purpose Registers &amp; PSW</text>
          <text x="530" y="235" fill="#475569" font-size="11" text-anchor="middle">4. WRITEBACK (R0..Rn, Flags)</text>
          <text x="530" y="250" fill="#0284c7" font-size="10" font-weight="600" text-anchor="middle">PC &larr; PC + Instruction Length</text>

          <!-- Bus Lines & Arrows -->
          <!-- Memory to Fetch -->
          <path d="M 180,133 L 270,115" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowCycle)" />
          <text x="210" y="115" fill="#0284c7" font-size="10" font-weight="700">Instr Bus</text>

          <!-- Fetch to Decode -->
          <line x1="410" y1="115" x2="450" y2="115" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowCycle)" />

          <!-- Decode to ALU -->
          <line x1="600" y1="115" x2="640" y2="115" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowCycle)" />

          <!-- ALU to Writeback -->
          <path d="M 715,150 L 715,225 L 645,225" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowCycle)" />

          <!-- Writeback / Register to Decode operands -->
          <path d="M 470,195 L 470,155" fill="none" stroke="#475569" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrowData)" />

          <!-- Loop back from Writeback to PC (Next cycle) -->
          <path d="M 420,230 L 345,230 L 345,155" fill="none" stroke="#0284c7" stroke-width="2" stroke-dasharray="5,3" marker-end="url(#arrowCycle)" />
          <text x="355" y="215" fill="#0284c7" font-size="10" font-weight="700">Next Cycle</text>
        </svg>
      </div>
"""

SVG_PIPELINE_ARCHITECTURE = """
      <div class="diagram-container" id="svg-pipeline-architecture">
        <svg viewBox="0 0 840 370" width="100%" height="auto" style="max-width: 840px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <!-- Non-Pipelined vs Pipelined Comparison -->
          <text x="20" y="30" fill="#0f172a" font-size="13" font-weight="700">1. Sequential (Non-Pipelined) Execution: 1 Instruction Every 4 Cycles</text>

          <!-- Sequential row 1 -->
          <g transform="translate(30, 45)">
            <rect x="0" y="0" width="55" height="28" fill="#e0f2fe" stroke="#0284c7" />
            <text x="27" y="18" font-size="11" font-weight="700" fill="#0369a1" text-anchor="middle">Fetch</text>

            <rect x="60" y="0" width="55" height="28" fill="#f0f9ff" stroke="#0284c7" />
            <text x="87" y="18" font-size="11" font-weight="700" fill="#0369a1" text-anchor="middle">Dec</text>

            <rect x="120" y="0" width="55" height="28" fill="#0284c7" stroke="#0369a1" />
            <text x="147" y="18" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">Exec</text>

            <rect x="180" y="0" width="55" height="28" fill="#f8fafc" stroke="#64748b" />
            <text x="207" y="18" font-size="11" font-weight="700" fill="#475569" text-anchor="middle">WB</text>

            <!-- Second instruction starts only at T5 -->
            <rect x="250" y="0" width="55" height="28" fill="#e0f2fe" stroke="#0284c7" />
            <text x="277" y="18" font-size="11" font-weight="700" fill="#0369a1" text-anchor="middle">Fetch</text>

            <rect x="310" y="0" width="55" height="28" fill="#f0f9ff" stroke="#0284c7" />
            <text x="337" y="18" font-size="11" font-weight="700" fill="#0369a1" text-anchor="middle">Dec</text>

            <rect x="370" y="0" width="55" height="28" fill="#0284c7" stroke="#0369a1" />
            <text x="397" y="18" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">Exec</text>

            <rect x="430" y="0" width="55" height="28" fill="#f8fafc" stroke="#64748b" />
            <text x="457" y="18" font-size="11" font-weight="700" fill="#475569" text-anchor="middle">WB</text>
          </g>

          <!-- Divider -->
          <line x1="20" y1="100" x2="820" y2="100" stroke="#e2e8f0" stroke-width="1.5" />

          <!-- Pipelined -->
          <text x="20" y="125" fill="#0f172a" font-size="13" font-weight="700">2. Pipelined Execution: Overlapping Stages Complete 1 Instruction Every Cycle</text>

          <g transform="translate(30, 140)">
            <!-- Header T1..T7 -->
            <text x="35" y="14" font-size="10" font-weight="700" fill="#64748b" text-anchor="middle">Cycle 1</text>
            <text x="110" y="14" font-size="10" font-weight="700" fill="#64748b" text-anchor="middle">Cycle 2</text>
            <text x="185" y="14" font-size="10" font-weight="700" fill="#64748b" text-anchor="middle">Cycle 3</text>
            <text x="260" y="14" font-size="10" font-weight="700" fill="#64748b" text-anchor="middle">Cycle 4</text>
            <text x="335" y="14" font-size="10" font-weight="700" fill="#64748b" text-anchor="middle">Cycle 5</text>
            <text x="410" y="14" font-size="10" font-weight="700" fill="#64748b" text-anchor="middle">Cycle 6</text>

            <!-- Instr 1 -->
            <text x="-15" y="42" font-size="11" font-weight="700" fill="#0284c7">I1</text>
            <rect x="10" y="26" width="55" height="24" rx="3" fill="#e0f2fe" stroke="#0284c7" />
            <text x="37" y="42" font-size="10" font-weight="700" fill="#0369a1" text-anchor="middle">Fetch</text>
            <rect x="85" y="26" width="55" height="24" rx="3" fill="#f0f9ff" stroke="#0284c7" />
            <text x="112" y="42" font-size="10" font-weight="700" fill="#0369a1" text-anchor="middle">Decode</text>
            <rect x="160" y="26" width="55" height="24" rx="3" fill="#0284c7" stroke="#0369a1" />
            <text x="187" y="42" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">Execute</text>
            <rect x="235" y="26" width="55" height="24" rx="3" fill="#f8fafc" stroke="#64748b" />
            <text x="262" y="42" font-size="10" font-weight="700" fill="#475569" text-anchor="middle">WB</text>

            <!-- Instr 2 -->
            <text x="-15" y="72" font-size="11" font-weight="700" fill="#0284c7">I2</text>
            <rect x="85" y="56" width="55" height="24" rx="3" fill="#e0f2fe" stroke="#0284c7" />
            <text x="112" y="72" font-size="10" font-weight="700" fill="#0369a1" text-anchor="middle">Fetch</text>
            <rect x="160" y="56" width="55" height="24" rx="3" fill="#f0f9ff" stroke="#0284c7" />
            <text x="187" y="72" font-size="10" font-weight="700" fill="#0369a1" text-anchor="middle">Decode</text>
            <rect x="235" y="56" width="55" height="24" rx="3" fill="#0284c7" stroke="#0369a1" />
            <text x="262" y="72" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">Execute</text>
            <rect x="310" y="56" width="55" height="24" rx="3" fill="#f8fafc" stroke="#64748b" />
            <text x="337" y="72" font-size="10" font-weight="700" fill="#475569" text-anchor="middle">WB</text>

            <!-- Instr 3 -->
            <text x="-15" y="102" font-size="11" font-weight="700" fill="#0284c7">I3</text>
            <rect x="160" y="86" width="55" height="24" rx="3" fill="#e0f2fe" stroke="#0284c7" />
            <text x="187" y="102" font-size="10" font-weight="700" fill="#0369a1" text-anchor="middle">Fetch</text>
            <rect x="235" y="86" width="55" height="24" rx="3" fill="#f0f9ff" stroke="#0284c7" />
            <text x="262" y="102" font-size="10" font-weight="700" fill="#0369a1" text-anchor="middle">Decode</text>
            <rect x="310" y="86" width="55" height="24" rx="3" fill="#0284c7" stroke="#0369a1" />
            <text x="337" y="102" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">Execute</text>
            <rect x="385" y="86" width="55" height="24" rx="3" fill="#f8fafc" stroke="#64748b" />
            <text x="412" y="102" font-size="10" font-weight="700" fill="#475569" text-anchor="middle">WB</text>
          </g>

          <!-- Divider -->
          <line x1="20" y1="280" x2="820" y2="280" stroke="#e2e8f0" stroke-width="1.5" />

          <!-- Superscalar Note -->
          <g transform="translate(20, 295)">
            <text x="0" y="20" fill="#0f172a" font-size="13" font-weight="700">3. Superscalar Execution: Multiple Pipelines (e.g., Dual-Issue)</text>
            <rect x="0" y="32" width="790" height="30" rx="4" fill="#f0f9ff" stroke="#bae6fd" />
            <text x="15" y="52" fill="#0369a1" font-size="11" font-weight="600">Dual Fetch &amp; Decode &rarr; Parallel ALUs (ALU 1 &amp; ALU 2) &rarr; Retired Concurrently (&gt; 1 IPC Throughput)</text>
          </g>
        </svg>
      </div>
"""

def inject_cpu_diagrams():
    file_path = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Insert CPU Cycle Diagram after the fetch-decode-execute list
    if 'id="svg-cpu-cycle"' not in content:
        cycle_marker = "<li><strong>Execute:</strong> Carry out the operation within the Arithmetic Logic Unit (ALU), manipulate data registers, and adjust processor state flags.</li>\n      </ul>"
        if cycle_marker in content:
            content = content.replace(cycle_marker, f"{cycle_marker}\n{SVG_CPU_CYCLE}")
            print("--> Injected CPU Instruction Cycle SVG diagram.")
        else:
            # Fallback regex search
            pattern = r"(<li><strong>Execute:</strong>.*?</li>\s*</ul>)"
            content = re.sub(pattern, f"\\1\n{SVG_CPU_CYCLE}", content, count=1, flags=re.DOTALL)
            print("--> Injected CPU Instruction Cycle SVG diagram via fallback pattern.")

    # 2. Insert Pipeline Diagram after Pipelining, Superscalar, & Multicore section
    if 'id="svg-pipeline-architecture"' not in content:
        pipeline_marker = "<li><strong>Multicore Processors:</strong> Embed multiple complete, independent CPU cores onto a single silicon die, each with dedicated L1/L2 caches and shared L3 caches.</li>\n      </ul>"
        if pipeline_marker in content:
            content = content.replace(pipeline_marker, f"{pipeline_marker}\n{SVG_PIPELINE_ARCHITECTURE}")
            print("--> Injected Pipelining vs Superscalar SVG diagram.")
        else:
            # Fallback pattern
            pattern = r"(<li><strong>Multicore Processors:</strong>.*?</li>\s*</ul>)"
            content = re.sub(pattern, f"\\1\n{SVG_PIPELINE_ARCHITECTURE}", content, count=1, flags=re.DOTALL)
            print("--> Injected Pipelining vs Superscalar SVG diagram via fallback pattern.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", file_path], check=True)
        commit_msg = (
            "Add CPU cycle and pipelining architecture SVG diagrams to Module 2\n\n"
            "Insert vector diagrams for the fetch-decode-execute instruction cycle\n"
            "and comparative pipelined vs superscalar execution into Module 2."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully via fix.py!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    inject_cpu_diagrams()
