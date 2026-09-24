#!/usr/bin/env python3
# =====================================================================
# fix.py: Embed structural & state diagrams into Section 2 of Module 04
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join("week02-processes", "04-thread-implementation.html")

def inject_section_two_diagrams():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Diagram 1: Windows NT Thread Structure Layering (TEB -> ETHREAD -> KTHREAD)
    structure_diagram = r"""
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 2.1: Windows NT Thread Data Structure Layering &amp; Privilege Boundaries</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 16px;">Visualizing how the User-Mode TEB links across the Ring 3/Ring 0 boundary to the Executive ETHREAD and embedded Microkernel KTHREAD.</div>

      <svg viewBox="0 0 820 400" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="nt-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
          </marker>
          <marker id="nt-pointer" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669" />
          </marker>
        </defs>

        <!-- USER SPACE CONTAINER (Ring 3) -->
        <rect x="20" y="15" width="350" height="370" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5 5" />
        <text x="35" y="40" font-size="12" font-weight="700" fill="#475569">USER SPACE (Ring 3) &mdash; Mapped in Process Memory</text>

        <!-- TEB Card -->
        <rect x="35" y="55" width="320" height="315" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2" />
        <text x="50" y="80" font-size="13" font-weight="700" fill="#0284c7">TEB / TIB (Thread Environment Block)</text>
        <text x="50" y="96" font-size="10" fill="#64748b">Accessed without syscalls via segment register (%gs on x64, %fs on x86)</text>

        <rect x="48" y="108" width="294" height="32" rx="4" fill="#f0f9ff" stroke="#bae6fd" />
        <text x="58" y="128" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#0369a1">StackBase &amp; StackLimit</text>
        <text x="215" y="128" font-size="9" fill="#64748b">User Stack Bounds</text>

        <rect x="48" y="146" width="294" height="32" rx="4" fill="#f0f9ff" stroke="#bae6fd" />
        <text x="58" y="166" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#0369a1">ExceptionList (fs:[0])</text>
        <text x="205" y="166" font-size="9" fill="#64748b">SEH Exception Frame Head</text>

        <rect x="48" y="184" width="294" height="32" rx="4" fill="#f0f9ff" stroke="#bae6fd" />
        <text x="58" y="204" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#0369a1">TlsSlots[64] &amp; Expansion</text>
        <text x="210" y="204" font-size="9" fill="#64748b">Static &amp; Dynamic TLS</text>

        <rect x="48" y="222" width="294" height="32" rx="4" fill="#f0f9ff" stroke="#bae6fd" />
        <text x="58" y="242" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#0369a1">LastErrorValue</text>
        <text x="200" y="242" font-size="9" fill="#64748b">GetLastError() Source</text>

        <rect x="48" y="260" width="294" height="32" rx="4" fill="#f0f9ff" stroke="#bae6fd" />
        <text x="58" y="280" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#0369a1">ClientId (PID / TID)</text>
        <text x="200" y="280" font-size="9" fill="#64748b">gs:[0x48] Thread ID</text>

        <rect x="48" y="298" width="294" height="32" rx="4" fill="#f0f9ff" stroke="#bae6fd" />
        <text x="58" y="318" font-family="var(--font-mono)" font-size="10" font-weight="600" fill="#0369a1">ProcessEnvironmentBlock</text>
        <text x="215" y="318" font-size="9" fill="#64748b">Pointer to PEB</text>

        <!-- KERNEL SPACE CONTAINER (Ring 0) -->
        <rect x="410" y="15" width="390" height="370" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
        <text x="425" y="40" font-size="12" font-weight="700" fill="#0f172a">KERNEL SPACE (Ring 0) &mdash; Executive &amp; Microkernel</text>

        <!-- ETHREAD Outer Block -->
        <rect x="425" y="55" width="360" height="315" rx="6" fill="#ffffff" stroke="#334155" stroke-width="2" />
        <text x="440" y="78" font-size="13" font-weight="700" fill="#0f172a">ETHREAD (Executive Thread Block)</text>
        <text x="440" y="93" font-size="10" fill="#64748b">Higher-Level Subsystem State &amp; Object Manager Integration</text>

        <rect x="438" y="103" width="334" height="22" rx="3" fill="#f1f5f9" stroke="#cbd5e1" />
        <text x="446" y="118" font-family="var(--font-mono)" font-size="10" fill="#334155">EPROCESS *Process &amp; CID (UniqueProcess / UniqueThread)</text>

        <rect x="438" y="130" width="334" height="22" rx="3" fill="#f1f5f9" stroke="#cbd5e1" />
        <text x="446" y="145" font-family="var(--font-mono)" font-size="10" fill="#334155">Security Token (Impersonation) &amp; IrpList (Pending I/O)</text>

        <!-- KTHREAD Embedded Inner Block -->
        <rect x="438" y="160" width="334" height="198" rx="5" fill="#f0fdf4" stroke="#059669" stroke-width="1.5" />
        <text x="450" y="180" font-size="11" font-weight="700" fill="#166534">KTHREAD: Embedded Microkernel Schedulable Unit</text>
        <text x="450" y="194" font-size="9" fill="#15803d">Directly manipulated by interrupt handlers, timers, and the dispatcher</text>

        <rect x="448" y="202" width="314" height="26" rx="3" fill="#ffffff" stroke="#86efac" />
        <text x="456" y="219" font-family="var(--font-mono)" font-size="9" font-weight="600" fill="#166534">DISPATCHER_HEADER (Signal State / Wait Block List)</text>

        <rect x="448" y="233" width="314" height="26" rx="3" fill="#ffffff" stroke="#86efac" />
        <text x="456" y="250" font-family="var(--font-mono)" font-size="9" font-weight="600" fill="#166534">KernelStack (24KB) &amp; TrapFrame (KTRAP_FRAME)</text>

        <rect x="448" y="264" width="314" height="26" rx="3" fill="#ffffff" stroke="#86efac" />
        <text x="456" y="281" font-family="var(--font-mono)" font-size="9" font-weight="600" fill="#166534">BasePriority (0-31), Priority, Quantum, Affinity</text>

        <rect x="448" y="295" width="314" height="26" rx="3" fill="#ffffff" stroke="#86efac" />
        <text x="456" y="312" font-family="var(--font-mono)" font-size="9" font-weight="600" fill="#166534">ApcState (Kernel/User APC Queues) &amp; WaitListEntry</text>

        <rect x="448" y="326" width="314" height="24" rx="3" fill="#ffffff" stroke="#86efac" />
        <text x="456" y="342" font-family="var(--font-mono)" font-size="9" font-weight="600" fill="#166534">Teb Pointer &rarr; Links back to User Mode TEB</text>

        <!-- Cross-Boundary Pointer Linkage -->
        <path d="M 448 338 C 390 338, 380 320, 355 318" stroke="#059669" stroke-width="2" marker-end="url(#nt-pointer)" />
        <text x="375" y="352" font-family="var(--font-mono)" font-size="9" fill="#059669" font-weight="600">Teb Ref</text>
      </svg>
    </div>
"""

    # Diagram 2: Windows NT Dispatcher State Machine
    state_machine_diagram = r"""
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 2.2: Windows NT Microkernel Dispatcher State Transitions</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 16px;">The complete state lifecycle of an NT thread managed by the priority-driven preemptive scheduler.</div>

      <svg viewBox="0 0 820 280" style="width: 100%; height: auto; font-family: system-ui, -apple-system, sans-serif;">
        <defs>
          <marker id="sm-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
          </marker>
          <marker id="sm-arr-alert" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626" />
          </marker>
        </defs>

        <!-- State 1: Initialized -->
        <g transform="translate(30, 110)">
          <rect width="105" height="55" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" />
          <text x="52" y="26" text-anchor="middle" font-size="11" font-weight="700" fill="#334155">Initialized</text>
          <text x="52" y="42" text-anchor="middle" font-size="9" fill="#64748b">Structure Built</text>
        </g>

        <!-- State 2: Ready -->
        <g transform="translate(185, 110)">
          <rect width="105" height="55" rx="6" fill="#f0f9ff" stroke="#0284c7" stroke-width="2" />
          <text x="52" y="26" text-anchor="middle" font-size="11" font-weight="700" fill="#0284c7">Ready</text>
          <text x="52" y="42" text-anchor="middle" font-size="9" fill="#64748b">In Ready Queue</text>
        </g>

        <!-- State 3: Standby -->
        <g transform="translate(340, 110)">
          <rect width="105" height="55" rx="6" fill="#fef3c7" stroke="#d97706" stroke-width="2" />
          <text x="52" y="26" text-anchor="middle" font-size="11" font-weight="700" fill="#b45309">Standby</text>
          <text x="52" y="42" text-anchor="middle" font-size="9" fill="#64748b">Pre-assigned Core</text>
        </g>

        <!-- State 4: Running -->
        <g transform="translate(495, 110)">
          <rect width="105" height="55" rx="6" fill="#f0fdf4" stroke="#059669" stroke-width="2" />
          <text x="52" y="26" text-anchor="middle" font-size="11" font-weight="700" fill="#15803d">Running</text>
          <text x="52" y="42" text-anchor="middle" font-size="9" fill="#64748b">Active in CPU</text>
        </g>

        <!-- State 5: Terminated -->
        <g transform="translate(670, 110)">
          <rect width="115" height="55" rx="6" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3 3" />
          <text x="57" y="26" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">Terminated</text>
          <text x="57" y="42" text-anchor="middle" font-size="9" fill="#64748b">Signaled / Freed</text>
        </g>

        <!-- State 6: Waiting (Below) -->
        <g transform="translate(340, 205)">
          <rect width="105" height="55" rx="6" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5" />
          <text x="52" y="26" text-anchor="middle" font-size="11" font-weight="700" fill="#b91c1c">Waiting</text>
          <text x="52" y="42" text-anchor="middle" font-size="9" fill="#64748b">Blocked on Object</text>
        </g>

        <!-- State 7: Transition (Top) -->
        <g transform="translate(185, 15)">
          <rect width="105" height="50" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" />
          <text x="52" y="24" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">Transition</text>
          <text x="52" y="38" text-anchor="middle" font-size="9" fill="#64748b">Stack Paged Out</text>
        </g>

        <!-- Forward Transitions -->
        <path d="M 135 137 L 185 137" stroke="#0284c7" stroke-width="1.8" marker-end="url(#sm-arr)" />
        <path d="M 290 137 L 340 137" stroke="#0284c7" stroke-width="1.8" marker-end="url(#sm-arr)" />
        <path d="M 445 137 L 495 137" stroke="#0284c7" stroke-width="1.8" marker-end="url(#sm-arr)" />
        <path d="M 600 137 L 670 137" stroke="#0284c7" stroke-width="1.8" marker-end="url(#sm-arr)" />

        <!-- Running -> Waiting -> Ready -->
        <path d="M 525 165 C 510 230, 480 232, 445 232" stroke="#dc2626" stroke-width="1.8" marker-end="url(#sm-arr-alert)" />
        <text x="530" y="210" font-size="9" fill="#dc2626" font-weight="600">WaitForSingleObject()</text>

        <path d="M 340 232 C 240 232, 230 200, 237 165" stroke="#0284c7" stroke-width="1.8" marker-end="url(#sm-arr)" />
        <text x="210" y="222" font-size="9" fill="#0284c7" font-weight="600">Object Signaled / IRQ</text>

        <!-- Running -> Preempted (Back to Ready) -->
        <path d="M 547 110 C 547 65, 260 65, 245 105" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="3 3" marker-end="url(#sm-arr)" />
        <text x="370" y="60" text-anchor="middle" font-size="9" fill="#0284c7" font-weight="600">Quantum Expired / Preempted</text>
      </svg>
    </div>
"""

    # Inject Figure 2.1 after Section 2.1
    anchor_21 = "<h4>1. Two-Tiered Kernel Representation: ETHREAD and KTHREAD</h4>"
    if "Figure 2.1: Windows NT Thread Data Structure Layering" not in content:
        content = content.replace(anchor_21, anchor_21 + "\n" + structure_diagram)

    # Inject Figure 2.2 after Section 2.3
    anchor_23 = "<h5>Thread Dispatcher States</h5>"
    if "Figure 2.2: Windows NT Microkernel Dispatcher State Transitions" not in content:
        content = content.replace(anchor_23, anchor_23 + "\n" + state_machine_diagram)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Successfully injected Windows NT diagrams into Section 2 of {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add dedicated structural and state diagrams to Section 2 of Module 04\n\n"
            "Embed SVG diagrams illustrating the Windows NT ETHREAD/KTHREAD/TEB\n"
            "privilege hierarchy and the eight-state Microkernel dispatcher machine."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    inject_section_two_diagrams()
