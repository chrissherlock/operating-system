#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 3 in 01-io-hardware-device-controllers.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "01-io-hardware-device-controllers.html"
)

EXPANDED_SECTION_THREE = r"""    <h3>3. Communicating with Controllers: PMIO vs. MMIO</h3>
    <p>
      For an operating system driver to command a peripheral, the processor must be capable of reading from and writing to the controller's internal registers. Over the evolution of computer architecture, two competing hardware paradigms emerged for routing CPU instructions to device controllers: <strong>Port-Mapped I/O (PMIO)</strong> and <strong>Memory-Mapped I/O (MMIO)</strong>.
    </p>

    <!-- Structural Diagram: PMIO vs MMIO Hardware Topology -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 1.2: Hardware Interconnect Architectures &mdash; PMIO vs. MMIO</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How the processor routes bus cycles through isolated control lines vs. unified memory address decoders.</div>

      <svg viewBox="0 0 760 270" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="pio-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="pio-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
        </defs>

        <!-- Left: Port-Mapped I/O Topology -->
        <g transform="translate(15, 20)">
          <rect width="345" height="230" rx="8" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5"/>
          <text x="172" y="24" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0284c7">PORT-MAPPED I/O (ISOLATED I/O SPACE)</text>
          <text x="172" y="38" text-anchor="middle" font-size="7.5" fill="#64748b">Dual Address Spaces &bull; Special Machine Instructions</text>

          <!-- CPU Core -->
          <rect x="20" y="52" width="130" height="50" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="85" y="72" text-anchor="middle" font-size="8.5" font-weight="700" fill="#0f172a">CPU CORE (x86)</text>
          <text x="85" y="86" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0284c7">in / out instructions</text>

          <!-- Address / Bus Selector -->
          <g transform="translate(170, 52)">
            <rect width="155" height="50" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="77" y="68" text-anchor="middle" font-size="7.5" font-weight="700" fill="#334155">BUS CONTROL LINES</text>
            <text x="77" y="84" text-anchor="middle" font-family="var(--font-mono)" font-size="7" fill="#dc2626">/IOR, /IOW vs /MEMR, /MEMW</text>
          </g>

          <!-- Dual Target Blocks -->
          <g transform="translate(20, 120)">
            <!-- Physical RAM -->
            <rect x="0" y="0" width="145" height="85" rx="4" fill="#f0f9ff" stroke="#bae6fd"/>
            <text x="72" y="20" text-anchor="middle" font-size="8" font-weight="700" fill="#0369a1">SYSTEM RAM SPACE</text>
            <text x="72" y="36" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0284c7">0x00000000 &hellip; Max</text>
            <text x="72" y="52" text-anchor="middle" font-size="7" fill="#64748b">Accessed via: mov, push</text>
            <text x="72" y="66" text-anchor="middle" font-size="7" fill="#166534">Asserts: /MEMR, /MEMW</text>

            <!-- Isolated I/O Space -->
            <rect x="160" y="0" width="145" height="85" rx="4" fill="#fef2f2" stroke="#dc2626"/>
            <text x="232" y="20" text-anchor="middle" font-size="8" font-weight="700" fill="#991b1b">I/O PORT SPACE (64 KB)</text>
            <text x="232" y="36" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#dc2626">0x0000 &hellip; 0xFFFF</text>
            <text x="232" y="52" text-anchor="middle" font-size="7" fill="#64748b">Accessed via: in, out</text>
            <text x="232" y="66" text-anchor="middle" font-size="7" fill="#991b1b">Asserts: /IOR, /IOW</text>
          </g>
        </g>

        <!-- Right: Memory-Mapped I/O Topology -->
        <g transform="translate(390, 20)">
          <rect width="355" height="230" rx="8" fill="#f8fafc" stroke="#059669" stroke-width="1.5"/>
          <text x="177" y="24" text-anchor="middle" font-size="10.5" font-weight="700" fill="#059669">MEMORY-MAPPED I/O (MMIO)</text>
          <text x="177" y="38" text-anchor="middle" font-size="7.5" fill="#64748b">Unified Physical Address Space &bull; Universal Standard</text>

          <!-- CPU Core -->
          <rect x="20" y="52" width="130" height="50" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="85" y="72" text-anchor="middle" font-size="8.5" font-weight="700" fill="#0f172a">CPU CORE (Any ISA)</text>
          <text x="85" y="86" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#059669">mov, ldr, str (Standard)</text>

          <!-- System Memory Controller / PCIe Root -->
          <g transform="translate(170, 52)">
            <rect width="165" height="50" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="82" y="68" text-anchor="middle" font-size="7.5" font-weight="700" fill="#334155">MEMORY CONTROLLER</text>
            <text x="82" y="84" text-anchor="middle" font-size="7" fill="#64748b">Address Range Decoders</text>
          </g>

          <!-- Unified Address Space Column -->
          <g transform="translate(20, 120)">
            <rect width="315" height="85" rx="4" fill="#ffffff" stroke="#94a3b8"/>
            <text x="157" y="16" text-anchor="middle" font-size="7.5" font-weight="700" fill="#334155">UNIFIED 64-BIT PHYSICAL ADDRESS MAP</text>

            <!-- DRAM slice -->
            <rect x="10" y="24" width="140" height="48" rx="2" fill="#f0f9ff" stroke="#bae6fd"/>
            <text x="80" y="42" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">0x00000000 &hellip; RAM</text>
            <text x="80" y="58" text-anchor="middle" font-size="6.5" fill="#64748b">Physical DRAM Chips</text>

            <!-- MMIO BAR slice -->
            <rect x="165" y="24" width="140" height="48" rx="2" fill="#dcfce7" stroke="#16a34a"/>
            <text x="235" y="42" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#166534">0xFEC00000 &hellip; MMIO</text>
            <text x="235" y="58" text-anchor="middle" font-size="6.5" fill="#15803d">PCIe BARs &bull; Device Regs</text>
          </g>
        </g>
      </svg>
    </div>

    <h4>1. Port-Mapped I/O (PMIO / Isolated I/O)</h4>
    <p>
      Port-Mapped I/O is an architectural design historically championed by Intel x86 microprocessors. The processor implements a completely separate, dedicated <strong>16-bit I/O address space</strong> ($0\text{x}0000 \dots 0\text{xFFFF}$), providing exactly 65,536 distinct 8-bit I/O ports.
    </p>
    <ul>
      <li>
        <strong>Dedicated Bus Control Lines:</strong> The processor does not use memory control lines when executing port instructions. When asserting an address on the bus, the CPU asserts the <strong><code>/IOR</code> (I/O Read)</strong> or <strong><code>/IOW</code> (I/O Write)</strong> control lines rather than <code>/MEMR</code> or <code>/MEMW</code>. Physical memory chips remain deaf to these cycles; only peripheral device controllers respond.
      </li>
      <li>
        <strong>Specialized Machine Instructions:</strong> Reading or writing to an I/O port cannot be done via regular memory load/store instructions. The programmer must use explicit x86 assembly instructions:
        <pre><code><span class="syn-cmt">; Reading a byte from I/O port 0x3F8 (COM1 Serial Port Status)</span>
<span class="syn-kw">mov</span> dx, <span class="syn-num">0x3FD</span>   <span class="syn-cmt">; Load port address into 16-bit DX register</span>
<span class="syn-kw">in</span>  al, dx      <span class="syn-cmt">; Read 8-bit value from port into AL register</span>

<span class="syn-cmt">; Writing a byte to I/O port 0x3F8 (Transmit Data)</span>
<span class="syn-kw">mov</span> dx, <span class="syn-num">0x3F8</span>   <span class="syn-cmt">; Data port address</span>
<span class="syn-kw">mov</span> al, <span class="syn-str">'A'</span>     <span class="syn-cmt">; Payload byte</span>
<span class="syn-kw">out</span> dx, al      <span class="syn-cmt">; Transmit byte to device</span></code></pre>
      </li>
      <li>
        <strong>Security &amp; Privilege Protection (IOPL and the TSS IOPB):</strong> Because I/O ports can directly reprogram system timers, initiate DMA transfers, or reset hardware, user-space processes must never be allowed unvetted port access.
        <br>
        The x86 architecture enforces port security via two mechanisms:
        <ol>
          <li><strong>I/O Privilege Level (IOPL):</strong> A 2-bit field in the <code>EFLAGS</code> register. If the current privilege level (CPL, Ring 0&ndash;3) is numerically greater than the IOPL, executing <code>in</code> or <code>out</code> immediately triggers a <strong>General Protection Fault (#GP)</strong>.</li>
          <li><strong>I/O Permission Bit Map (IOPB):</strong> Located inside the Task State Segment (TSS). An operating system kernel can configure an 8 KB bitmap where each bit corresponds to one of the 65,536 I/O ports. Setting a bit to <code>0</code> grants a specific unprivileged Ring 3 application direct access to that individual port without granting broad system privileges.</li>
        </ol>
      </li>
    </ul>

    <h4>2. Memory-Mapped I/O (MMIO)</h4>
    <p>
      In Memory-Mapped I/O, there is no isolated I/O address space and no special machine instructions. Instead, ranges of the system's standard physical memory address space are reserved for peripheral hardware.
    </p>
    <ul>
      <li>
        <strong>Universal Address Decoding:</strong> The CPU executes ordinary memory load and store instructions (<code>mov</code> on x86, <code>ldr</code>/<code>str</code> on ARM and RISC-V). When the processor places an address on the system interconnect, the address decoder in the memory controller or PCIe Root Complex recognizes that the target address falls within a peripheral aperture, routing the transaction across the PCIe link rather than to DRAM.
      </li>
      <li>
        <strong>PCI Express Base Address Registers (BARs):</strong> When a modern PCIe peripheral (e.g. an NVMe solid-state drive or GPU) boots, the operating system kernel or UEFI firmware interrogates the card's configuration header:
        <ul>
          <li>The card declares how much physical memory space its registers require using <strong>Base Address Registers (BARs)</strong>.</li>
          <li>The OS kernel assigns a contiguous range of available physical memory addresses to each BAR (e.g. assigning BAR0 to physical address <code>0xDF000000 &ndash; 0xDF003FFF</code>).</li>
          <li>The kernel then maps this physical range into its virtual address space using page tables, allowing device drivers to interact with hardware registers through standard C pointers:</li>
        </ul>
        <pre><code><span class="syn-cmt">/* Interacting with an NVMe Controller via Memory-Mapped Registers */</span>
<span class="syn-kw">typedef struct</span> {
    <span class="syn-kw">volatile uint32_t</span> cap_low;    <span class="syn-cmt">/* Controller Capabilities */</span>
    <span class="syn-kw">volatile uint32_t</span> cap_high;
    <span class="syn-kw">volatile uint32_t</span> version;     <span class="syn-cmt">/* NVMe Specification Version */</span>
    <span class="syn-kw">volatile uint32_t</span> intms;       <span class="syn-cmt">/* Interrupt Mask Set */</span>
    <span class="syn-kw">volatile uint32_t</span> intmc;       <span class="syn-cmt">/* Interrupt Mask Clear */</span>
    <span class="syn-kw">volatile uint32_t</span> cc;          <span class="syn-cmt">/* Controller Configuration (Enable/Shutdown) */</span>
    <span class="syn-kw">volatile uint32_t</span> csts;        <span class="syn-cmt">/* Controller Status (Ready flag) */</span>
} nvme_regs_t;

<span class="syn-kw">void</span> init_nvme_hardware(<span class="syn-kw">void</span> *mmio_base) {
    nvme_regs_t *regs = (nvme_regs_t *)mmio_base;

    <span class="syn-cmt">/* Read controller version directly through pointer dereference */</span>
    <span class="syn-kw">uint32_t</span> ver = regs-&gt;version;

    <span class="syn-cmt">/* Enable controller by setting bit 0 in Controller Configuration register */</span>
    regs-&gt;cc |= <span class="syn-num">0x00000001</span>;

    <span class="syn-cmt">/* Wait for hardware to assert the Ready (RDY) bit in status register */</span>
    <span class="syn-kw">while</span> ((regs-&gt;csts &amp; <span class="syn-num">0x00000001</span>) == <span class="syn-num">0</span>) {
        <span class="syn-cmt">/* Poll or pause until hardware stabilizes */</span>
    }
}</code></pre>
      </li>
      <li>
        <strong>Memory Protection Integration:</strong> Unlike PMIO, which requires specialized TSS bitmaps, MMIO integrates cleanly with the processor's standard <strong>Memory Management Unit (MMU)</strong>. The operating system kernel maps MMIO physical pages with precise page-table flags: read-only for status registers, supervisor-only to prevent user tampering, and Execute-Disable (NX) to prevent code execution exploits.
      </li>
    </ul>

    <h4>The Three Fatal Traps of MMIO in Production Systems</h4>
    <p>
      While MMIO provides clean, unified C pointer access to hardware, it introduces three severe microarchitectural hazards that do not exist in ordinary RAM programming:
    </p>

    <h5>1. The Caching Hazard &amp; Uncacheable Memory Types</h5>
    <p>
      Modern processors achieve high throughput by routing memory accesses through multi-level L1/L2/L3 write-back caches. If an MMIO register range is inadvertently mapped with standard cacheable memory attributes:
    </p>
    <ul>
      <li><strong>Stale Reads:</strong> When the driver reads <code>regs-&gt;csts</code> to check if hardware is ready, the CPU loads the value into L1 cache. On subsequent loop iterations, the CPU satisfies the load <em>directly from L1 cache</em>! The CPU never places an electrical read cycle onto the PCIe bus, looping infinitely even after the physical device has transitioned to ready.</li>
      <li><strong>Lost Writes:</strong> In a write-back cache, writing to a memory address updates the cache line and marks it dirty; data is not flushed to the physical bus until the cache line is evicted. A driver write intended to command hardware will sit dormant in the CPU cache, never reaching the device controller!</li>
    </ul>
    <div class="math-callout">
      <strong>The Solution &mdash; Hardware Memory Types:</strong>
      <br>
      The operating system must explicitly configure the Page Table Entries (PTEs) for all MMIO ranges to disable CPU caching:
      <ul>
        <li><strong>x86 PAT (Page Attribute Table) / MTRR:</strong> Marked as <strong>Uncacheable (UC)</strong>. Every single load and store instruction bypasses all internal caches and forces an immediate physical bus transaction. For video framebuffers, pages are mapped as <strong>Write-Combining (WC)</strong>, which aggregates sequential pixel writes into a 64-byte burst buffer without caching reads.</li>
        <li><strong>ARM Memory Model:</strong> Configured as <strong>Device-nGnRnE</strong> (<em>non-Gathering, non-Reordering, no Early Write Acknowledgment</em>), guaranteeing that every access reaches the peripheral with exact program order and size.</li>
      </ul>
    </div>

    <h5>2. The Compiler Optimization Trap &amp; The volatile Qualifier</h5>
    <p>
      Modern optimizing compilers (such as GCC and Clang) assume the <em>as-if</em> rule: memory contents do not change unless the program itself explicitly writes to that memory.
    </p>
    <p>
      Consider what happens without the <code>volatile</code> keyword:
    </p>
    <pre><code><span class="syn-cmt">/* FATAL BUG: Missing volatile keyword */</span>
<span class="syn-kw">uint32_t</span> *status_reg = (<span class="syn-kw">uint32_t</span> *)<span class="syn-num">0xDF00001C</span>;

<span class="syn-kw">while</span> ((*status_reg &amp; <span class="syn-num">0x01</span>) == <span class="syn-num">0</span>) {
    <span class="syn-cmt">/* Wait for hardware ready */</span>
}</code></pre>
    <p>
      The compiler analyzes this loop and reasons: <em>"The loop body contains no writes to <code>*status_reg</code>. Therefore, the memory value cannot change. I will hoist the read outside the loop into a register to save bus cycles!"</em>
    </p>
    <p>
      The compiler emits the following broken assembly:
    </p>
    <pre><code><span class="syn-kw">mov</span> eax, [<span class="syn-num">0xDF00001C</span>]  <span class="syn-cmt">; Read status register ONCE into EAX</span>
.loop:
<span class="syn-kw">test</span> eax, <span class="syn-num">1</span>             <span class="syn-cmt">; Test register EAX</span>
<span class="syn-kw">jz</span>   .loop              <span class="syn-cmt">; Infinite loop! Hardware is never re-queried!</span></code></pre>
    <p>
      Declaring pointers with the <strong><code>volatile</code></strong> qualifier informs the compiler that the underlying memory can be modified by hardware external to the program at any instant. The compiler is legally forbidden from caching the value in a register, omitting writes (dead store elimination), or reordering accesses with respect to other volatile accesses.
    </p>

    <h5>3. Out-of-Order Execution &amp; Memory Barrier Fences</h5>
    <p>
      Even with <code>volatile</code> preventing compiler reordering, modern out-of-order superscalar CPUs (x86-64, ARM Cortex, Apple Silicon) aggressively reorder instructions dynamically at runtime to maximize pipeline utilization:
    </p>
    <ul>
      <li>Suppose a driver writes payload data to a DMA descriptor in RAM, and immediately writes a <code>START</code> flag to the controller's MMIO doorbell register:
        <pre><code>desc-&gt;buffer_addr = target_ram; <span class="syn-cmt">/* Step 1: Write RAM descriptor */</span>
desc-&gt;length      = <span class="syn-num">4096</span>;
*doorbell_reg     = <span class="syn-num">1</span>;          <span class="syn-cmt">/* Step 2: Ring hardware doorbell */</span></code></pre>
      </li>
      <li>If the CPU memory subsystem reorders these transactions, the MMIO store to <code>doorbell_reg</code> may arrive at the controller <em>before</em> the stores to <code>desc</code> have settled in DRAM!</li>
      <li>The controller begins DMA immediately, reading uninitialized, garbage memory, corrupting disk or network storage!</li>
    </ul>
    <div class="math-callout">
      <strong>Memory Barriers / Fences:</strong>
      <br>
      To enforce strict sequential ordering between normal memory and MMIO registers, drivers must emit architectural <strong>Memory Barriers</strong>:
      <ul>
        <li><strong>x86 Architecture:</strong> <code>sfence</code> (Store Fence), <code>lfence</code> (Load Fence), or <code>mfence</code> (Full Memory Barrier).</li>
        <li><strong>ARM Architecture:</strong> <code>dmb osh</code> (Data Memory Barrier, Outer Shareable) or <code>dsb</code> (Data Synchronization Barrier).</li>
        <li><strong>Linux Kernel I/O Accessors:</strong> Driver code should never use raw pointer dereferencing directly. Linux provides specialized architecture-aware macros that automatically bundle the necessary volatile dereferences and memory barriers:
          <pre><code><span class="syn-kw">uint32_t</span> val = <span class="syn-fn">readl</span>(io_addr);   <span class="syn-cmt">/* Read 32-bit MMIO with barrier */</span>
<span class="syn-fn">writel</span>(val, io_addr);            <span class="syn-cmt">/* Write 32-bit MMIO with barrier */</span></code></pre>
        </li>
      </ul>
    </div>

    <h4>Comprehensive Comparison: PMIO vs. MMIO</h4>
    <div style="overflow-x: auto; margin: 18px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 12px; width: 22%;">Feature / Metric</th>
            <th style="padding: 10px 12px; width: 39%;">Port-Mapped I/O (PMIO)</th>
            <th style="padding: 10px 12px; width: 39%;">Memory-Mapped I/O (MMIO)</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Address Space</td>
            <td style="padding: 10px 12px;">Separate, isolated 16-bit address space ($0\text{x}0000 \dots 0\text{xFFFF}$).</td>
            <td style="padding: 10px 12px;">Unified physical address space shared with DRAM.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">CPU Instructions</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">in, out (insb, outsb)</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">mov, ldr, str (Any standard memory instruction)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Bus Control Lines</td>
            <td style="padding: 10px 12px;">Dedicated lines: <code>/IOR</code>, <code>/IOW</code>.</td>
            <td style="padding: 10px 12px;">Standard memory read/write control lines (decoded by PCIe / chipset).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Address Space Capacity</td>
            <td style="padding: 10px 12px; color: #dc2626;">Severely constrained: maximum 64 KB ports.</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 600;">Gigabytes to Terabytes (bounded only by 64-bit physical addressing).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Protection Mechanism</td>
            <td style="padding: 10px 12px;">x86 <code>IOPL</code> in <code>EFLAGS</code> and TSS I/O Permission Bit Map (IOPB).</td>
            <td style="padding: 10px 12px;">Standard MMU page tables (User/Supervisor, Read/Write, NX).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #f0fdf4;">
            <td style="padding: 10px 12px; font-weight: 700; color: #166534;">Industry Adoption</td>
            <td style="padding: 10px 12px;">Legacy x86 PC architecture (legacy PIC, PIT, PS/2 keyboard, COM ports).</td>
            <td style="padding: 10px 12px; font-weight: 700; color: #166534;">Universal standard: PCI Express (NVMe, GPUs, NICs), ARM, RISC-V, SoC peripherals.</td>
          </tr>
        </tbody>
      </table>
    </div>"""

def update_section_three():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>3. Communicating with Controllers: PMIO vs. MMIO</h3>"
    end_marker = "<h3>4. The Three I/O Execution Models: PIO, Interrupts, and DMA</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not find Section 3 boundaries in Module 01.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_THREE + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 3 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 3 of Module 01 on PMIO vs MMIO hardware interfacing\n\n"
            "Detail x86 IN/OUT, IOPB security, PCIe BARs, uncacheable memory types,\n"
            "volatile compiler hazards, memory ordering fences, and add an SVG diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_three():
        run_git_sync()
