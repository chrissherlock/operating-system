#!/usr/bin/env python3
# =====================================================================
# fix.py: Correct SVG marker orientations in Figure 1.2
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week03-process-scheduling", "01-scheduling-introduction.html")

def correct_arrow_markers():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Isolate Figure 1.2 block
    start_tag = '<!-- Structural SVG Diagram: The Dispatcher Cycle -->'
    end_tag = '<h4>2. Deconstructing Dispatch Latency: Direct vs. Indirect Costs</h4>'

    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Figure 1.2 in target file.")
        return

    clean_figure_svg = r"""<!-- Structural SVG Diagram: The Dispatcher Cycle -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 1.2: Anatomical Breakdown of the Scheduler &amp; Dispatcher Execution Cycle</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 16px;">Tracing the privilege transitions, policy evaluation, and silicon-level context swap between Outgoing Task A and Incoming Task B.</div>

      <svg viewBox="0 0 820 420" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <!-- Standard horizontal right-pointing markers (orient="auto" handles 0°, 90°, 270° rotations accurately) -->
          <marker id="dc-arrow-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
          <marker id="dc-arrow-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="dc-arrow-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
        </defs>

        <!-- USER SPACE BAND (Top) -->
        <rect x="20" y="15" width="780" height="95" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4 4" />
        <text x="35" y="38" font-size="11" font-weight="700" fill="#475569">USER MODE (Ring 3) &mdash; Applications &amp; Threads</text>

        <!-- Task A Box (Left) -->
        <g transform="translate(45, 48)">
          <rect width="210" height="50" rx="6" fill="#ffffff" stroke="#dc2626" stroke-width="2" />
          <text x="14" y="22" font-size="11" font-weight="700" fill="#0f172a">Task A (Outgoing Process)</text>
          <text x="14" y="38" font-family="var(--font-mono)" font-size="9" fill="#dc2626">RIP: 0x4010a2 | Ring 3 Running</text>
        </g>

        <!-- Task B Box (Right) -->
        <g transform="translate(565, 48)">
          <rect width="210" height="50" rx="6" fill="#ffffff" stroke="#059669" stroke-width="2" />
          <text x="14" y="22" font-size="11" font-weight="700" fill="#0f172a">Task B (Incoming Process)</text>
          <text x="14" y="38" font-family="var(--font-mono)" font-size="9" fill="#059669">RIP: 0x4087fe | Ring 3 Resumed</text>
        </g>

        <!-- KERNEL SPACE BAND (Bottom) -->
        <rect x="20" y="130" width="780" height="270" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
        <text x="35" y="153" font-size="11" font-weight="700" fill="#0f172a">KERNEL MODE (Ring 0) &mdash; Supervisor Execution</text>

        <!-- 1. Trap & State Save -->
        <g transform="translate(45, 175)">
          <rect width="210" height="95" rx="6" fill="#ffffff" stroke="#dc2626" stroke-width="1.5" />
          <text x="12" y="20" font-size="11" font-weight="700" fill="#dc2626">1. Trap &amp; Context Save</text>
          <rect x="10" y="28" width="190" height="22" rx="3" fill="#fef2f2" stroke="#fca5a5" />
          <text x="16" y="43" font-family="var(--font-mono)" font-size="9" fill="#b91c1c">APIC Timer / Syscall</text>
          <text x="12" y="68" font-size="9" fill="#475569">&bull; Save RSP, RIP, RFLAGS</text>
          <text x="12" y="83" font-size="9" fill="#475569">&bull; Push regs (struct pt_regs)</text>
        </g>

        <!-- 2. Scheduler Policy -->
        <g transform="translate(305, 175)">
          <rect width="210" height="95" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2" />
          <text x="12" y="20" font-size="11" font-weight="700" fill="#0284c7">2. CPU Scheduler (Policy)</text>
          <rect x="10" y="28" width="190" height="22" rx="3" fill="#f0f9ff" stroke="#bae6fd" />
          <text x="16" y="43" font-family="var(--font-mono)" font-size="9" fill="#0369a1">pick_next_task()</text>
          <text x="12" y="68" font-size="9" fill="#475569">&bull; Decrement quantum / charge CPU</text>
          <text x="12" y="83" font-size="9" fill="#475569">&bull; Selects Task B from Ready queue</text>
        </g>

        <!-- 3. Dispatcher Mechanism -->
        <g transform="translate(45, 290)">
          <rect width="730" height="95" rx="6" fill="#ffffff" stroke="#059669" stroke-width="2" />
          <text x="16" y="20" font-size="11" font-weight="700" fill="#059669">3. The Dispatcher (Low-Level Hardware Mechanism: switch_to)</text>

          <g transform="translate(15, 32)">
            <rect width="220" height="50" rx="4" fill="#f0fdf4" stroke="#86efac" />
            <text x="10" y="18" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#166534">A. MMU Context Switch</text>
            <text x="10" y="32" font-size="8.5" fill="#334155">Reload CR3 with Task B Page Table</text>
            <text x="10" y="43" font-size="8.5" fill="#64748b">(Bypassed if threads share same mm)</text>
          </g>

          <g transform="translate(250, 32)">
            <rect width="225" height="50" rx="4" fill="#f0fdf4" stroke="#86efac" />
            <text x="10" y="18" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#166534">B. Kernel Stack &amp; TSS</text>
            <text x="10" y="32" font-size="8.5" fill="#334155">Switch RSP to Task B kernel stack</text>
            <text x="10" y="43" font-size="8.5" fill="#64748b">Update TSS.sp0 for next interrupt</text>
          </g>

          <g transform="translate(490, 32)">
            <rect width="225" height="50" rx="4" fill="#f0fdf4" stroke="#86efac" />
            <text x="10" y="18" font-family="var(--font-mono)" font-size="9" font-weight="700" fill="#166534">C. Hardware Registers &amp; TLS</text>
            <text x="10" y="32" font-size="8.5" fill="#334155">Set %fs/%gs MSR to Task B TCB</text>
            <text x="10" y="43" font-size="8.5" fill="#64748b">Pop general registers from stack</text>
          </g>
        </g>

        <!-- Downward Trap Path: Task A into Step 1 (M 150 98 to 150 173) -->
        <path d="M 150 98 L 150 173" fill="none" stroke="#dc2626" stroke-width="2" marker-end="url(#dc-arrow-red)" />
        <text x="158" y="125" font-size="9" font-weight="700" fill="#dc2626">Trap / IRQ</text>
        <text x="158" y="137" font-size="8" fill="#64748b">(Ring 3 &rarr; Ring 0)</text>

        <!-- Step 1 to Step 2 Horizontal Connector (M 255 222 to 303 222) -->
        <path d="M 255 222 L 303 222" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#dc-arrow-blue)" />

        <!-- Step 2 to Step 3 Clean Vertical Drop (M 410 270 to 410 288) -->
        <path d="M 410 270 L 410 288" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#dc-arrow-blue)" />
        <text x="418" y="282" font-size="8.5" font-weight="700" fill="#0284c7">switch_to()</text>

        <!-- Upward Return Path: Step 3 to Task B (M 670 290 to 670 100) -->
        <path d="M 670 290 L 670 100" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#dc-arrow-green)" />
        <text x="678" y="125" font-size="9" font-weight="700" fill="#059669">IRETQ / SYSRETQ</text>
        <text x="678" y="137" font-size="8" fill="#64748b">(Ring 0 &rarr; Ring 3)</text>
      </svg>
    </div>"""

    content = content[:start_idx] + clean_figure_svg + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully corrected SVG arrow markers in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix SVG marker orientations in Figure 1.2 of Module 01\n\n"
            "Standardize marker definitions to horizontal base vectors with\n"
            "orient=\"auto\" so downward and upward paths render correct arrowheads."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    correct_arrow_markers()
