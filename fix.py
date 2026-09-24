#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 1 of 02-interrupts-and-dma.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "02-interrupts-and-dma.html"
)

EXPANDED_SECTION_ONE = r"""    <h3>1. Hardware Interrupt Mechanics &amp; The APIC</h3>
    <p>
      A hardware interrupt is an asynchronous electrical event initiated by a peripheral device controller that forces the microprocessor to temporarily suspend its current instruction pipeline, execute an involuntary privilege boundary transition, and jump to a pre-registered kernel routine.
    </p>
    <p>
      Interrupts form the bedrock of interactive and real-time operating systems. Without hardware interrupts, a central processor would have no mechanism to detect external physical events&mdash;such as an inbound network packet, a keystroke, a disk block DMA completion, or a timer tick&mdash;without dedicating 100% of its computational cycles to wasteful polling loops.
    </p>

    <!-- Structural Diagram: Modern APIC and MSI-X Routing Hierarchy -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 2.0: Multi-Core Interrupt Architecture &mdash; From PCIe MSI-X to Local APIC Vectoring</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How physical peripherals bypass legacy electrical pins to route MSI-X memory transactions directly to per-core Local APICs.</div>

      <svg viewBox="0 0 760 280" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="apic-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="apic-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
          <marker id="apic-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
        </defs>

        <!-- Peripheral Layer: PCIe Endpoints (Left) -->
        <g transform="translate(15, 20)">
          <rect width="180" height="240" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="90" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0f172a">PERIPHERAL DOMAIN</text>
          <text x="90" y="38" text-anchor="middle" font-size="7" fill="#64748b">(PCIe Gen 5 Endpoints)</text>

          <!-- Device 1: NVMe SSD -->
          <rect x="12" y="50" width="156" height="52" rx="4" fill="#ffffff" stroke="#0284c7"/>
          <text x="20" y="68" font-size="8" font-weight="700" fill="#0284c7">NVMe SSD (Multi-Queue)</text>
          <text x="20" y="82" font-family="var(--font-mono)" font-size="7" fill="#475569">MSI-X Vector 0x42 &rarr; Core 0</text>
          <text x="20" y="94" font-family="var(--font-mono)" font-size="7" fill="#475569">MSI-X Vector 0x43 &rarr; Core 1</text>

          <!-- Device 2: 100 GbE NIC -->
          <rect x="12" y="112" width="156" height="52" rx="4" fill="#ffffff" stroke="#059669"/>
          <text x="20" y="130" font-size="8" font-weight="700" fill="#166534">100 GbE NIC (RSS Queues)</text>
          <text x="20" y="144" font-family="var(--font-mono)" font-size="7" fill="#475569">MSI-X Vector 0x60 &rarr; Core 0</text>
          <text x="20" y="156" font-family="var(--font-mono)" font-size="7" fill="#475569">MSI-X Vector 0x61 &rarr; Core 1</text>

          <!-- Legacy Device: UART/Timer -->
          <rect x="12" y="174" width="156" height="48" rx="4" fill="#fef2f2" stroke="#dc2626"/>
          <text x="20" y="192" font-size="8" font-weight="700" fill="#991b1b">Legacy UART / Platform</text>
          <text x="20" y="206" font-size="7" fill="#7f1d1d">Physical IRQ Line &rarr; I/O APIC</text>
        </g>

        <!-- Interconnect Fabric (Middle) -->
        <g transform="translate(210, 20)">
          <rect width="180" height="240" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <text x="90" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="#0284c7">SYSTEM INTERCONNECT</text>
          <text x="90" y="38" text-anchor="middle" font-size="7" fill="#64748b">(Root Complex &amp; I/O APIC)</text>

          <!-- PCIe MSI-X Address Decoder -->
          <rect x="12" y="52" width="156" height="80" rx="4" fill="#f0f9ff" stroke="#bae6fd"/>
          <text x="20" y="70" font-size="8" font-weight="700" fill="#0369a1">MSI-X MEMORY WRITES</text>
          <text x="20" y="86" font-family="var(--font-mono)" font-size="7.5" fill="#0284c7">Addr: 0xFEE00000</text>
          <text x="20" y="100" font-size="7" fill="#334155">&bull; Decoded directly by</text>
          <text x="20" y="112" font-size="7" fill="#334155">  Memory Controller Hub</text>
          <text x="20" y="124" font-size="7" fill="#334155">&bull; Zero electrical IRQ pins!</text>

          <!-- Chipset I/O APIC -->
          <rect x="12" y="142" width="156" height="80" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="20" y="160" font-size="8" font-weight="700" fill="#334155">CHIPSET I/O APIC</text>
          <text x="20" y="174" font-size="7" fill="#64748b">24 Redirection Table Entries</text>
          <text x="20" y="188" font-size="7" fill="#475569">&bull; Maps legacy physical pins</text>
          <text x="20" y="200" font-size="7" fill="#475569">&bull; Arbitrates level-triggered</text>
          <text x="20" y="212" font-size="7" fill="#475569">  shared PCI lines (INTA#)</text>
        </g>

        <!-- Multi-Core Processor Domain (Right) -->
        <g transform="translate(405, 20)">
          <rect width="340" height="240" rx="8" fill="#f8fafc" stroke="#059669" stroke-width="2"/>
          <text x="170" y="24" text-anchor="middle" font-size="10.5" font-weight="700" fill="#166534">SMP MULTI-CORE CPU DIE</text>

          <!-- Core 0 Slice -->
          <g transform="translate(15, 38)">
            <rect width="145" height="185" rx="4" fill="#ffffff" stroke="#059669"/>
            <text x="72" y="18" text-anchor="middle" font-size="8" font-weight="700" fill="#166534">CPU CORE 0</text>

            <rect x="8" y="26" width="129" height="42" rx="2" fill="#dcfce7" stroke="#16a34a"/>
            <text x="14" y="42" font-size="7" font-weight="700" fill="#166534">LOCAL APIC (LAPIC 0)</text>
            <text x="14" y="54" font-family="var(--font-mono)" font-size="6.5" fill="#15803d">TPR: Task Priority Reg</text>
            <text x="14" y="64" font-family="var(--font-mono)" font-size="6.5" fill="#15803d">ISR: In-Service Reg</text>

            <rect x="8" y="74" width="129" height="44" rx="2" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="14" y="90" font-size="7" font-weight="700" fill="#334155">IDT DISPATCH [0x42]</text>
            <text x="14" y="102" font-family="var(--font-mono)" font-size="6.5" fill="#0284c7">Gate &rarr; nvme_isr_c0()</text>
            <text x="14" y="112" font-size="6.5" fill="#64748b">Clears RFLAGS.IF</text>

            <rect x="8" y="124" width="129" height="50" rx="2" fill="#f8fafc" stroke="#cbd5e1"/>
            <text x="14" y="140" font-size="7" font-weight="700" fill="#334155">STACK FRAME PUSH</text>
            <text x="14" y="152" font-family="var(--font-mono)" font-size="6.5" fill="#475569">SS:RSP &bull; RFLAGS &bull; CS:RIP</text>
            <text x="14" y="164" font-size="6.5" font-weight="700" fill="#059669">Executes in Ring 0</text>
          </g>

          <!-- Core 1 Slice -->
          <g transform="translate(175, 38)">
            <rect width="150" height="185" rx="4" fill="#ffffff" stroke="#0284c7"/>
            <text x="75" y="18" text-anchor="middle" font-size="8" font-weight="700" fill="#0284c7">CPU CORE 1</text>

            <rect x="8" y="26" width="134" height="42" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
            <text x="14" y="42" font-size="7" font-weight="700" fill="#0369a1">LOCAL APIC (LAPIC 1)</text>
            <text x="14" y="54" font-family="var(--font-mono)" font-size="6.5" fill="#0284c7">TPR: Task Priority Reg</text>
            <text x="14" y="64" font-family="var(--font-mono)" font-size="6.5" fill="#0284c7">ISR: In-Service Reg</text>

            <rect x="8" y="74" width="134" height="44" rx="2" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="14" y="90" font-size="7" font-weight="700" fill="#334155">IDT DISPATCH [0x43]</text>
            <text x="14" y="102" font-family="var(--font-mono)" font-size="6.5" fill="#0284c7">Gate &rarr; nvme_isr_c1()</text>
            <text x="14" y="112" font-size="6.5" fill="#64748b">Parallel execution!</text>

            <rect x="8" y="124" width="134" height="50" rx="2" fill="#f8fafc" stroke="#cbd5e1"/>
            <text x="14" y="140" font-size="7" font-weight="700" fill="#334155">INTER-PROCESSOR (IPI)</text>
            <text x="14" y="152" font-size="6.5" fill="#475569">ICR: Cross-Core Shootdown</text>
            <text x="14" y="164" font-size="6.5" font-weight="700" fill="#0284c7">Preemption / Reschedule</text>
          </g>
        </g>
      </svg>
    </div>

    <h4>1. Physical Electrical Signaling: Edge vs. Level Triggering</h4>
    <p>
      At the hardware layer, an interrupt begins as a change in electrical voltage across a physical trace connecting the peripheral controller to the interrupt controller. Two distinct electrical conventions govern this signaling:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <!-- Edge-Triggered -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--accent); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Edge-Triggered Interrupts</h4>
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--accent); text-transform: uppercase; margin-bottom: 8px;">Voltage Transition Sensitive</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          The interrupt controller latches an event exclusively when it detects a <strong>dynamic transition between voltage states</strong> (e.g. a rising edge from $0\text{V}$ to $+3.3\text{V}$, or a falling edge).
          <br><br>
          <em>Key Characteristics &amp; Hazards:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li><strong>Zero Lingering Line Assertion:</strong> The peripheral pulses the line briefly. The controller does not require the line to remain held.</li>
            <li><strong>The Dropped Interrupt Hazard:</strong> If two devices share an edge-triggered line, and Device B pulses the line while Device A is already holding it high, <strong>no voltage edge occurs</strong>! The second interrupt is silently dropped, freezing the operating system driver forever. Consequently, edge-triggered lines cannot be shared safely across multiple physical devices.</li>
          </ul>
        </p>
      </div>

      <!-- Level-Triggered -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Level-Triggered Interrupts</h4>
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--success); text-transform: uppercase; margin-bottom: 8px;">Voltage State Sensitive (Wire-OR Shared)</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          The interrupt controller recognizes an active interrupt as long as the electrical line is <strong>continuously maintained at an asserted voltage level</strong> (typically active-low, held at ground).
          <br><br>
          <em>Key Characteristics &amp; Mechanics:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li><strong>Mandatory for Shared PCI Lines:</strong> Legacy PCI uses open-collector, pull-up lines (<code>INTA#</code> through <code>INTD#</code>). Multiple peripherals can pull the identical physical line low simultaneously without electrical short-circuits.</li>
            <li><strong>The Handshake Requirement:</strong> The CPU cannot simply return from the ISR. The driver <em>must</em> read or write the device's status register to command the hardware to release the electrical line. If the driver forgets to acknowledge the device, the line remains held low, causing the CPU to re-enter the ISR infinitely upon exit!</li>
          </ul>
        </p>
      </div>
    </div>

    <h4>2. Evolution of the Interrupt Controller: 8259A PIC to Modern APIC</h4>
    <p>
      To understand why modern operating systems demand specialized hardware routing, we must contrast the historical PC interrupt controller with the modern symmetric multiprocessing (SMP) APIC architecture:
    </p>

    <h5>The Legacy 8259A PIC (Programmable Interrupt Controller)</h5>
    <p>
      The original 1981 IBM PC incorporated an Intel 8259A PIC supporting 8 hardware interrupt lines (IRQ0&ndash;IRQ7). The IBM PC/AT cascaded a second slave 8259A controller through Master IRQ2, yielding 15 usable lines:
    </p>
    <ul>
      <li><strong>Master PIC:</strong> IRQ0 (Timer), IRQ1 (Keyboard), IRQ2 (Cascade to Slave), IRQ3 (COM2), IRQ4 (COM1), IRQ5 (LPT2), IRQ6 (Floppy Disk), IRQ7 (Spurious / LPT1).</li>
      <li><strong>Slave PIC:</strong> IRQ8 (Real-Time Clock), IRQ9 (Redirected IRQ2), IRQ10&ndash;IRQ11 (Unassigned / PCI), IRQ12 (PS/2 Mouse), IRQ13 (FPU Coprocessor), IRQ14 (Primary IDE Hard Disk), IRQ15 (Secondary IDE).</li>
    </ul>
    <p>
      <em>Why the 8259A Failed Modern Computing:</em>
      The 8259A is electrically unscalable. It is hardwired to uniprocessor execution&mdash;it can route interrupts to only a single CPU core. Furthermore, 15 interrupt lines proved completely inadequate as modern PCs added multiple sound cards, SCSI host adapters, USB controllers, and network interfaces, leading to severe resource conflicts and shared-line interrupt latency.
    </p>

    <h5>The Advanced Programmable Interrupt Controller (APIC Architecture)</h5>
    <p>
      To support multi-core symmetric multiprocessing (SMP), Intel and industry partners introduced the <strong>APIC Architecture</strong>, partitioning interrupt management into two discrete silicon entities:
    </p>
    <ol>
      <li>
        <strong>The I/O APIC (Chipset / Platform Controller Hub):</strong>
        Located on the motherboard chipset or root complex. The standard I/O APIC provides 24 (or more) programmable <strong>Redirection Table Entries (RTEs)</strong>.
        <br>
        Each 64-bit RTE allows the operating system kernel to configure:
        <ul>
          <li><strong>Interrupt Vector Number:</strong> The exact byte index (from <code>0x20</code> to <code>0xFE</code>) to trigger in the processor's IDT.</li>
          <li><strong>Delivery Mode:</strong> Fixed, Lowest Priority (directing the interrupt to the least busy core), System Management Interrupt (SMI), or Non-Maskable Interrupt (NMI).</li>
          <li><strong>Destination Mode &amp; Target Core:</strong> Specifies physical or logical APIC IDs, enabling the OS kernel to bind specific device interrupts to dedicated CPU cores (<strong>IRQ Affinity</strong>).</li>
        </ul>
      </li>
      <li>
        <strong>The Local APIC (LAPIC &mdash; On-Die Per Core):</strong>
        Every physical CPU core integrates its own dedicated Local APIC. The Local APIC contains specialized hardware registers:
        <ul>
          <li><strong>Task Priority Register (TPR):</strong> Allows the operating system kernel to dynamically set a priority threshold. The LAPIC will automatically suppress all incoming device interrupts whose priority is lower than or equal to the value in the TPR, without requiring software masking of individual devices.</li>
          <li><strong>In-Service Register (ISR):</strong> A 256-bit register tracking which interrupt vectors are currently being serviced by the CPU core.</li>
          <li><strong>End of Interrupt Register (EOI):</strong> When an Interrupt Service Routine completes, the kernel <strong>must write a value of <code>0</code> to the Local APIC EOI register</strong> (located at physical MMIO address <code>0xFEE000B0</code> or via MSR <code>0x80B</code> in x2APIC mode). Writing to the EOI register clears the highest-priority bit in the In-Service Register, notifying the APIC that the core is ready to accept subsequent interrupts of equal or lower priority.</li>
          <li><strong>Interrupt Command Register (ICR):</strong> Enables the CPU core to issue <strong>Inter-Processor Interrupts (IPIs)</strong> across the system bus to other cores, driving cross-core scheduling wakeups, thread preemption, and TLB invalidation shootdowns.</li>
        </ul>
      </li>
    </ol>

    <h4>3. Message Signaled Interrupts (MSI &amp; MSI-X)</h4>
    <p>
      In high-throughput PCIe systems, physical interrupt pins are obsolete. Routing physical copper traces across motherboards introduces signal integrity degradation, latency, and pin-count bottlenecks.
    </p>
    <p>
      To solve this, PCI 2.2 introduced <strong>Message Signaled Interrupts (MSI)</strong>, and PCI Express expanded it into <strong>MSI-X</strong>:
    </p>
    <div class="math-callout">
      <strong>How MSI-X Operates &mdash; Interrupts as In-Band Memory Writes:</strong>
      <br>
      An MSI-X interrupt is <strong>not an electrical pin assertion</strong>. It is an ordinary <strong>in-band PCIe DMA 32-bit Memory Write Transaction</strong> issued by the peripheral controller directly across the PCIe fabric!
      <br><br>
      Every PCIe peripheral declares an <strong>MSI-X Table</strong> in its MMIO BAR space, composed of up to <strong>2,048 independent entries</strong>. Each entry defines:
      <ul>
        <li><strong>Message Address (64-bit):</strong> Formatted with a base address of <code>0xFEE00000</code> and an encoded Destination APIC ID. When the controller issues a write to this address, the PCIe Root Complex decodes it directly into the target CPU core's Local APIC.</li>
        <li><strong>Message Data (32-bit):</strong> Specifies the exact 8-bit interrupt vector (e.g. <code>0x42</code>) to invoke in the CPU's IDT, along with trigger attributes.</li>
        <li><strong>Vector Control (32-bit):</strong> Provides a hardware <code>Mask</code> bit, allowing the OS to mask individual queues independently.</li>
      </ul>
    </div>

    <h4>The Power of MSI-X Multi-Queue Affinity</h4>
    <p>
      MSI-X enables true linear scaling on multi-core servers:
    </p>
    <ul>
      <li>An enterprise 100 GbE NIC allocates 64 separate hardware receive (RX) descriptor queues.</li>
      <li>Through MSI-X, the operating system kernel assigns Queue 0 to fire Vector <code>0x50</code> targeting <strong>Core 0</strong>, Queue 1 to fire Vector <code>0x51</code> targeting <strong>Core 1</strong>, and so forth.</li>
      <li>Each CPU core services its own independent network stream from its own hardware queue, executing locklessly with <strong>100% CPU cache locality</strong> and zero inter-core synchronization contention!</li>
    </ul>

    <h4>4. Silicon Execution Sequence: IDT &amp; Hardware Stack Switching</h4>
    <p>
      When an interrupt vector arrives at a CPU core (either from an MSI-X memory write or the I/O APIC), the processor hardware executes an atomic sequence before software receives control:
    </p>

    <pre><code><span class="syn-cmt">/* The x86-64 Interrupt Descriptor Table (IDT) Gate Descriptor (16 Bytes) */</span>
<span class="syn-kw">typedef struct</span> {
    <span class="syn-kw">uint16_t</span> offset_low;      <span class="syn-cmt">/* Target ISR Handler Address [Bits 0..15] */</span>
    <span class="syn-kw">uint16_t</span> segment_selector;<span class="syn-cmt">/* Kernel Code Segment Selector (e.g. 0x08) */</span>
    <span class="syn-kw">uint8_t</span>  ist;             <span class="syn-cmt">/* Interrupt Stack Table (Bits 0..2) */</span>
    <span class="syn-kw">uint8_t</span>  type_attributes; <span class="syn-cmt">/* DPL (Privilege), Present Flag, Gate Type (0xE) */</span>
    <span class="syn-kw">uint16_t</span> offset_mid;      <span class="syn-cmt">/* Target ISR Handler Address [Bits 16..31] */</span>
    <span class="syn-kw">uint32_t</span> offset_high;     <span class="syn-cmt">/* Target ISR Handler Address [Bits 32..63] */</span>
    <span class="syn-kw">uint32_t</span> reserved;
} __attribute__((packed)) idt_entry_t;</code></pre>

    <div class="math-callout">
      <strong>The 64-Bit Hardware Interrupt Transition Sequence:</strong>
      <ol>
        <li><strong>Interrupt Evaluation:</strong> The core evaluates the interrupt vector against its Local APIC Task Priority Register (TPR). If vector priority &gt; TPR, and <code>RFLAGS.IF == 1</code>, the interrupt is accepted.</li>
        <li><strong>Privilege Escalation &amp; Stack Switch:</strong> The CPU transitions from Ring 3 (User) to Ring 0 (Kernel).
          <br>
          If the gate's <code>IST</code> (Interrupt Stack Table) field is non-zero, the CPU automatically loads the stack pointer from the specified TSS IST entry. This guarantees that critical interrupts (such as Double Faults or Machine Checks) execute on a dedicated, known-good kernel stack even if the user or kernel stack has overflowed!
        </li>
        <li><strong>State Preservation on Stack:</strong> The hardware pushes five architectural registers onto the kernel interrupt stack in strict sequence:
          <pre><code>[RSP + 32] &rarr; SS      (User Stack Segment)
[RSP + 24] &rarr; RSP     (User Stack Pointer)
[RSP + 16] &rarr; RFLAGS  (Processor Status &amp; Arithmetic Flags)
[RSP + 8]  &rarr; CS      (User Code Segment)
[RSP + 0]  &rarr; RIP     (Return Program Counter)</code></pre>
        </li>
        <li><strong>Masking Interrupts:</strong> For a standard 64-bit Interrupt Gate (type <code>0xE</code>), the CPU <strong>automatically clears <code>RFLAGS.IF = 0</code></strong>, disabling maskable interrupts to prevent nested execution.</li>
        <li><strong>Vector Dispatch:</strong> The CPU indexes the <strong>Interrupt Descriptor Table (IDT)</strong> using the 8-bit vector number, loads the 64-bit ISR handler address, and begins executing the driver's assembly entry point.</li>
        <li><strong>Atomic Return:</strong> At the conclusion of interrupt servicing, the driver executes the <strong><code>iretq</code> (Interrupt Return)</strong> instruction, which atomically pops <code>RIP</code>, <code>CS</code>, <code>RFLAGS</code>, <code>RSP</code>, and <code>SS</code>, restoring the interrupted user application in Ring 3 seamlessly.</li>
      </ol>
    </div>"""

def update_section_one():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>1. Hardware Interrupt Mechanics &amp; The APIC</h3>"
    end_marker = "<h3>2. The Dual-Phase Interrupt Model: Top-Half vs. Bottom-Half</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 1 boundaries in Module 02.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_ONE + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 1 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 1 of Module 02 on Interrupt Hardware and APIC/MSI-X\n\n"
            "Detail edge vs level triggering, 8259A to APIC routing, MSI-X PCIe\n"
            "packets, LAPIC TPR/ISR registers, IST stack switches, and add an SVG."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_one():
        run_git_sync()
