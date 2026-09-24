#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 4 in 01-io-hardware-device-controllers.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "01-io-hardware-device-controllers.html"
)

EXPANDED_SECTION_FOUR_PRE_AID = r"""    <h3>4. The Three I/O Execution Models: PIO, Interrupts, and DMA</h3>
    <p>
      Once peripheral device registers are mapped into the processor's address space, the operating system must orchestrate the actual movement of data payloads (such as a 4 KB disk page, a 1500-byte Ethernet frame, or an audio buffer) between device controller FIFOs and host physical RAM.
    </p>
    <p>
      Over the history of operating system design, three fundamental execution paradigms have emerged to govern this data flow, each striking a radically different trade-off between CPU cycle consumption, transfer latency, hardware complexity, and bus saturation.
    </p>

    <!-- Structural Diagram: The Three Data Flow Pathways -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 1.3: Data Pathways &amp; CPU Intervention across the Three I/O Models</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">Contrasting the double-hop CPU bottleneck of PIO with the direct memory path of Bus-Master DMA.</div>

      <svg viewBox="0 0 760 270" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="flow-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="flow-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
          <marker id="flow-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
        </defs>

        <!-- Column 1: PIO (Double Hop) -->
        <g transform="translate(15, 20)">
          <rect width="225" height="230" rx="8" fill="#f8fafc" stroke="#dc2626" stroke-width="1.5"/>
          <text x="112" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="#991b1b">1. PROGRAMMED I/O (PIO)</text>
          <text x="112" y="38" text-anchor="middle" font-size="7" fill="#dc2626">CPU Middleman &bull; 100% Pinned</text>

          <rect x="25" y="52" width="175" height="34" rx="4" fill="#fee2e2" stroke="#dc2626"/>
          <text x="112" y="73" text-anchor="middle" font-size="8" font-weight="700" fill="#991b1b">DEVICE CONTROLLER</text>

          <!-- Up Arrow to CPU -->
          <line x1="112" y1="86" x2="112" y2="108" stroke="#dc2626" stroke-width="2" marker-end="url(#flow-arr-red)"/>
          <text x="120" y="100" font-size="6.5" font-family="var(--font-mono)" fill="#dc2626">Hop 1: Bus Read</text>

          <rect x="25" y="110" width="175" height="42" rx="4" fill="#fee2e2" stroke="#dc2626"/>
          <text x="112" y="126" text-anchor="middle" font-size="8" font-weight="700" fill="#991b1b">CPU CORE REGISTERS</text>
          <text x="112" y="140" text-anchor="middle" font-family="var(--font-mono)" font-size="7" fill="#7f1d1d">while(busy); in al, dx;</text>

          <!-- Down Arrow to RAM -->
          <line x1="112" y1="152" x2="112" y2="174" stroke="#dc2626" stroke-width="2" marker-end="url(#flow-arr-red)"/>
          <text x="120" y="166" font-size="6.5" font-family="var(--font-mono)" fill="#dc2626">Hop 2: RAM Write</text>

          <rect x="25" y="176" width="175" height="34" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="112" y="197" text-anchor="middle" font-size="8" font-weight="700" fill="#0f172a">PHYSICAL HOST RAM</text>
          <text x="112" y="222" text-anchor="middle" font-size="6.5" font-weight="700" fill="#dc2626">2 Bus Transfers per Word!</text>
        </g>

        <!-- Column 2: Interrupt-Driven I/O -->
        <g transform="translate(260, 20)">
          <rect width="235" height="230" rx="8" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5"/>
          <text x="117" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0284c7">2. INTERRUPT-DRIVEN I/O</text>
          <text x="117" y="38" text-anchor="middle" font-size="7" fill="#64748b">Asynchronous Yield &bull; Context Switch Tax</text>

          <rect x="25" y="52" width="185" height="34" rx="4" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="117" y="68" text-anchor="middle" font-size="8" font-weight="700" fill="#0369a1">DEVICE CONTROLLER</text>
          <text x="117" y="79" text-anchor="middle" font-size="6.5" fill="#0284c7">Raises IRQ when sector ready</text>

          <!-- Interrupt Arrow to APIC/CPU -->
          <line x1="117" y1="86" x2="117" y2="108" stroke="#0284c7" stroke-width="2" marker-end="url(#flow-arr-blue)"/>
          <text x="125" y="100" font-size="6.5" font-family="var(--font-mono)" fill="#0284c7">IRQ Vector Trigger</text>

          <rect x="25" y="110" width="185" height="42" rx="4" fill="#ffffff" stroke="#0284c7"/>
          <text x="117" y="126" text-anchor="middle" font-size="8" font-weight="700" fill="#0f172a">CPU / INTERRUPT DISPATCH</text>
          <text x="117" y="140" text-anchor="middle" font-size="6.5" fill="#64748b">IDT Vector &rarr; ISR &rarr; Context Switch</text>

          <line x1="117" y1="152" x2="117" y2="174" stroke="#0284c7" stroke-width="2" marker-end="url(#flow-arr-blue)"/>
          <text x="125" y="166" font-size="6.5" font-family="var(--font-mono)" fill="#0284c7">ISR Moves Block</text>

          <rect x="25" y="176" width="185" height="34" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="117" y="197" text-anchor="middle" font-size="8" font-weight="700" fill="#0f172a">PHYSICAL HOST RAM</text>
          <text x="117" y="222" text-anchor="middle" font-size="6.5" fill="#475569">Frees CPU during mechanical wait</text>
        </g>

        <!-- Column 3: Bus-Master DMA -->
        <g transform="translate(515, 20)">
          <rect width="230" height="230" rx="8" fill="#f8fafc" stroke="#059669" stroke-width="2"/>
          <text x="115" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="#059669">3. BUS-MASTER DMA</text>
          <text x="115" y="38" text-anchor="middle" font-size="7" fill="#166534">Direct Memory Path &bull; Zero CPU Middleman</text>

          <rect x="25" y="52" width="180" height="40" rx="4" fill="#dcfce7" stroke="#16a34a"/>
          <text x="115" y="68" text-anchor="middle" font-size="8" font-weight="700" fill="#166534">DEVICE CONTROLLER (DMA ENGINE)</text>
          <text x="115" y="82" text-anchor="middle" font-size="6.5" fill="#15803d">Holds PCIe Bus Master Grant</text>

          <!-- Direct Bypass Arrow to RAM -->
          <line x1="115" y1="92" x2="115" y2="174" stroke="#059669" stroke-width="3" stroke-dasharray="4 2" marker-end="url(#flow-arr-green)"/>
          <text x="125" y="136" font-size="7.5" font-family="var(--font-mono)" font-weight="700" fill="#059669">DIRECT BUS STREAM</text>

          <!-- Side Annotation: CPU Uninvolved -->
          <rect x="15" y="108" width="85" height="42" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="57" y="124" text-anchor="middle" font-size="6.5" font-weight="700" fill="#0284c7">CPU CORE 0</text>
          <text x="57" y="138" text-anchor="middle" font-size="6" fill="#64748b">Runs user apps</text>

          <rect x="25" y="176" width="180" height="34" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="115" y="197" text-anchor="middle" font-size="8" font-weight="700" fill="#0f172a">PHYSICAL HOST RAM</text>
          <text x="115" y="222" text-anchor="middle" font-size="6.5" font-weight="700" fill="#166534">Single Completion IRQ at End!</text>
        </g>
      </svg>
    </div>

    <h4>1. Programmed I/O (PIO) &amp; Polling</h4>
    <p>
      In Programmed I/O, the central processor is directly responsible for every single phase of data movement. The device driver executes a tight polling loop on the CPU, querying the controller's status register until the device indicates that data is ready, and then reading or writing data one word at a time:
    </p>

    <pre><code><span class="syn-cmt">/* Programmed I/O (PIO) Block Read Routine */</span>
<span class="syn-kw">void</span> pio_read_block(<span class="syn-kw">uint16_t</span> data_port, <span class="syn-kw">uint16_t</span> status_port, <span class="syn-kw">uint32_t</span> *buffer, <span class="syn-kw">int</span> words) {
    <span class="syn-kw">for</span> (<span class="syn-kw">int</span> i = <span class="syn-num">0</span>; i &lt; words; i++) {
        <span class="syn-cmt">/* 1. Poll status register until controller clears BUSY and sets DRQ (Data Request) */</span>
        <span class="syn-kw">while</span> ((<span class="syn-fn">in_byte</span>(status_port) &amp; (STATUS_BUSY | STATUS_DRQ)) != STATUS_DRQ) {
            <span class="syn-cmt">/* CPU spins at 100% utilization doing zero productive computation */</span>
            <span class="syn-fn">cpu_pause</span>();
        }

        <span class="syn-cmt">/* 2. Hop 1: Load 32-bit word from device register into CPU register (EAX) */</span>
        <span class="syn-kw">uint32_t</span> word = <span class="syn-fn">in_dword</span>(data_port);

        <span class="syn-cmt">/* 3. Hop 2: Store 32-bit word from CPU register into DRAM buffer */</span>
        buffer[i] = word;
    }
}</code></pre>

    <div class="math-callout">
      <strong>The Fundamental Inefficiencies of PIO:</strong>
      <ol>
        <li>
          <strong>The Double-Hop Bus Penalty:</strong> Moving a 32-bit word from the controller to RAM requires <strong>two distinct bus transactions</strong>:
          <br>
          $$\text{Controller} \xrightarrow[\text{PCIe Bus}]{\text{Hop 1}} \text{CPU General-Purpose Register} \xrightarrow[\text{System Memory Interconnect}]{\text{Hop 2}} \text{DRAM}$$
          This doubles the bandwidth consumed on internal processor interconnects.
        </li>
        <li>
          <strong>Total CPU Starvation:</strong> The processor is pinned in a tight loop executing <code>in/out</code> instructions. If reading a 4 KB block from a magnetic disk takes 10 milliseconds, a 4 GHz CPU wastes <strong>40,000,000 clock cycles</strong> simply waiting for platter rotation!
        </li>
      </ol>
      <strong>When Polling is Actually Optimal (Modern Kernel Polling):</strong>
      <br>
      While PIO is catastrophic for slow bulk transfers, <strong>pure polling is the fastest possible mechanism for ultra-low-latency devices</strong> (e.g. PCIe Gen 5 NVMe SSDs operating at &lt; 5 &mu;s latency, and High-Frequency Trading 100 GbE NICs).
      <br>
      Because taking an interrupt and executing a full kernel context switch consumes <strong>1 to 3 microseconds</strong>, yielding to an interrupt on sub-5 &mu;s hardware costs up to 50% of total transfer time. Modern Linux high-performance frameworks (such as <code>io_uring</code> with <code>IORING_SETUP_IOPOLL</code>, SPDK, and DPDK) deliberately dedicate an isolated CPU core to poll hardware completion queues directly, trading raw CPU cycles for sub-microsecond latency.
    </div>

    <h4>2. Interrupt-Driven I/O</h4>
    <p>
      To eliminate the CPU polling tax, Interrupt-Driven I/O decouples the initiation of a command from its completion:
    </p>
    <ol>
      <li><strong>Command Initiation:</strong> The driver writes target parameters to the controller's command registers (e.g. <code>SEEK cylinder 42, READ sector 7</code>).</li>
      <li><strong>Asynchronous Sleep:</strong> Rather than polling, the driver sets the calling process state to <code>TASK_UNINTERRUPTIBLE</code> (or <code>Waiting</code> in Windows), enqueues the process PCB onto the device wait queue, and calls <code>schedule()</code>. The CPU immediately switches to executing other productive user-space processes.</li>
      <li><strong>Asynchronous Completion:</strong> The mechanical unit spins and reads the sector into its on-board FIFO. When data is verified, the controller asserts an electrical <strong>Interrupt Request (IRQ)</strong> or fires an MSI-X packet to the CPU Local APIC.</li>
      <li><strong>State Restoration:</strong> The CPU suspends the background application, saves registers to the kernel interrupt stack, executes the driver's Interrupt Service Routine (ISR), transfers the data from the controller FIFO into RAM, and transitions the sleeping process back to <code>TASK_RUNNING</code>.</li>
    </ol>

    <div class="math-callout">
      <strong>The Interrupt Storm / Livelock Phenomenon:</strong>
      <br>
      While interrupt-driven I/O is ideal for low-to-medium throughput devices (keyboards, serial ports, legacy disks), it encounters a fatal failure mode under modern multi-gigabit workloads: <strong>Interrupt Livelock</strong>.
      <br><br>
      Consider a 100 GbE network interface receiving a deluge of minimum-sized 64-byte packets:
      $$\text{Packet Rate} = \frac{100 \times 10^9\text{ bits/sec}}{(64 + 20\text{ bytes preamble/gap}) \times 8\text{ bits/byte}} \approx \mathbf{148{,}800{,}000\text{ packets/second}}$$
      If the NIC fired a hardware interrupt for every packet:
      <ul>
        <li>Each interrupt cycle incurs register saving, pipeline flushes, IDT dispatch, and kernel stack switching (&asymp; 1,000 to 2,000 CPU cycles per interrupt).</li>
        <li>The processor spends <strong>100% of its execution time processing interrupt entry and exit code</strong>, leaving zero CPU cycles to actually execute the network stack or deliver packets to user sockets!</li>
        <li>Eventually, kernel buffers overflow, and the system collapses into livelock&mdash;burning maximum CPU power while achieving zero useful throughput.</li>
      </ul>
      <strong>The Industrial Remedy &mdash; Adaptive Hybrid Polling (Linux NAPI):</strong>
      <br>
      Modern OS network drivers use an adaptive hybrid model (such as the Linux <strong>New API / NAPI</strong>):
      <ol>
        <li>When packet traffic is low, the driver operates in <strong>Interrupt Mode</strong> to maintain instant responsiveness.</li>
        <li>Upon the arrival of the first packet interrupt, the driver executes its top-half, <strong>disables device interrupts on the NIC entirely</strong>, and schedules a bottom-half polling loop (via <code>ksoftirqd</code>).</li>
        <li>The kernel polls and drains packets directly from the NIC's ring buffer in batches (e.g. 64 packets per poll budget).</li>
        <li>Only when the RX ring buffer is completely empty does the kernel re-enable hardware interrupts on the NIC.</li>
      </ol>
    </div>

    <h4>3. Direct Memory Access (DMA) &amp; Bus Mastering</h4>
    <p>
      While interrupt-driven I/O frees the CPU during long mechanical delays, the CPU must still act as the middleman to move data words between the controller FIFO and host RAM during the ISR. For multi-megabyte transfers, this still wastes vast quantities of CPU instructions.
    </p>
    <p>
      <strong>Direct Memory Access (DMA)</strong> eliminates the CPU from the data transfer path entirely. The hardware architecture incorporates a specialized <strong>DMA Engine</strong> directly onto the system interconnect:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 18px 0;">
      <!-- Cycle Stealing Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--accent); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Cycle Stealing (Interleaved Mode)</h4>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          The DMA controller requests ownership of the system bus for exactly <strong>one memory bus cycle</strong>, transfers a single word, and immediately relinquishes the bus back to the CPU.
          <br><br>
          <em>Trade-off:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>The CPU is never locked out of memory for extended periods; CPU instruction execution continues with minimal interruption.</li>
            <li>Transfer throughput is lower due to the repeated bus arbitration overhead (Bus Request &rarr; Bus Grant &rarr; Release) for every word.</li>
          </ul>
        </p>
      </div>

      <!-- Burst Mode Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Burst Mode (Block Transfer Mode)</h4>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          The DMA controller seizes ownership of the system bus and <strong>retains control continuously</strong> until the entire multi-kilobyte or multi-megabyte buffer is transferred.
          <br><br>
          <em>Trade-off:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>Achieves maximum theoretical bus bandwidth by streaming back-to-back data words without re-arbitration.</li>
            <li>If the CPU experiences a cache miss, it must stall until the DMA burst concludes or until a bus arbitration timeout preempts the DMA burst.</li>
          </ul>
        </p>
      </div>
    </div>

    <h4>Modern Bus Mastering: Scatter-Gather Descriptor Rings</h4>
    <p>
      Legacy PC architectures utilized a centralized, motherboard-based DMA controller (the Intel 8237). In modern architectures, every high-speed PCIe peripheral acts as an independent <strong>Bus Master</strong> containing its own internal DMA engine.
    </p>
    <p>
      Furthermore, because modern operating systems execute within <strong>Paging Virtual Memory</strong>, a 1 MB file buffer allocated contiguously in user space is almost always fragmented across hundreds of non-contiguous 4 KB physical page frames scattered throughout physical RAM:
    </p>

    <pre><code><span class="syn-cmt">/* Scatter-Gather DMA Physical Region Descriptor (PRD) Table */</span>
<span class="syn-kw">typedef struct</span> {
    <span class="syn-kw">uint64_t</span> physical_base_address; <span class="syn-cmt">/* Physical address of 4 KB page frame */</span>
    <span class="syn-kw">uint32_t</span> byte_length;           <span class="syn-cmt">/* Length of chunk (e.g. 4096 bytes) */</span>
    <span class="syn-kw">uint32_t</span> flags;                 <span class="syn-cmt">/* Bit 31: End of Table (EOT) marker */</span>
} prd_entry_t;

<span class="syn-cmt">/* The driver builds a linked array of descriptors representing scattered pages */</span>
prd_entry_t sg_list[<span class="syn-num">3</span>] = {
    { <span class="syn-num">0x10004000</span>, <span class="syn-num">4096</span>, <span class="syn-num">0</span> },         <span class="syn-cmt">/* Page 1 in physical RAM */</span>
    { <span class="syn-num">0x20500000</span>, <span class="syn-num">4096</span>, <span class="syn-num">0</span> },         <span class="syn-cmt">/* Page 2 (disjoint physical location) */</span>
    { <span class="syn-num">0x08102000</span>, <span class="syn-num">4096</span>, PRD_EOT }   <span class="syn-cmt">/* Page 3 (final chunk with EOT set) */</span>
};</code></pre>
    <p>
      The driver passes the 64-bit physical address of the <code>sg_list</code> descriptor array to the peripheral's DMA controller. The controller's hardware engine automatically reads the list, streams data into each physical page frame, seamlessly jumps to the next descriptor, and fires <strong>exactly one completion interrupt when the entire multi-page transfer finishes</strong>.
    </p>"""

def update_section_four():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>4. The Three I/O Execution Models: PIO, Interrupts, and DMA</h3>"
    end_marker = "<!-- Directed Narrative Stepper: PIO vs DMA Data Transfer -->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 4 boundaries before the interactive aid.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_FOUR_PRE_AID + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 4 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 4 of Module 01 on PIO, Interrupt-Driven, and DMA I/O\n\n"
            "Detail 2x bus penalties, interrupt storms, NAPI polling, cycle stealing\n"
            "vs burst mode, scatter-gather descriptor rings, and add an SVG diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_four():
        run_git_sync()
