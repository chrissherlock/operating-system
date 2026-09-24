#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 3 of 02-interrupts-and-dma.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "02-interrupts-and-dma.html"
)

EXPANDED_SECTION_THREE = r"""    <h3>3. Direct Memory Access (DMA) &amp; Cache Coherency</h3>
    <p>
      Direct Memory Access (DMA) is the cornerstone of high-throughput operating system I/O. By delegating data movement to dedicated bus-mastering engines on peripheral controllers, the CPU is completely liberated from the cycle-wasting overhead of byte-by-byte Programmed I/O.
    </p>
    <p>
      However, routing high-speed peripheral data directly into physical DRAM introduces a profound architectural conflict with modern CPU memory hierarchies: <strong>The Cache Coherency Dilemma</strong>.
    </p>

    <!-- Structural Diagram: DMA Cache Coherency and IOMMU Mapping -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 2.3: DMA Cache Coherency Snooping &amp; IOMMU Translation Pipeline</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How hardware snooping resolves stale cache lines, and how the IOMMU translates device IOVA addresses to physical host page frames.</div>

      <svg viewBox="0 0 760 290" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="dma-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="dma-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
          <marker id="dma-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
        </defs>

        <!-- Left: CPU Core & Cache Hierarchy -->
        <g transform="translate(15, 20)">
          <rect width="215" height="250" rx="8" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5"/>
          <text x="107" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0284c7">CPU EXECUTION CORE</text>

          <!-- L1 / L2 Local Caches -->
          <rect x="15" y="42" width="185" height="52" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="25" y="58" font-size="7.5" font-weight="700" fill="#334155">L1 / L2 CACHES (Write-Back)</text>
          <text x="25" y="72" font-family="var(--font-mono)" font-size="7" fill="#dc2626">Cacheline [0x7000]: DIRTY (M)</text>
          <text x="25" y="84" font-size="6.5" fill="#64748b">Holds modified CPU variables</text>

          <!-- Coherency Snoop Logic -->
          <rect x="15" y="104" width="185" height="60" rx="4" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="25" y="122" font-size="7.5" font-weight="700" fill="#0369a1">BUS SNOOP CONTROLLER</text>
          <text x="25" y="136" font-size="7" fill="#0284c7">&bull; Monitors PCIe interconnect</text>
          <text x="25" y="148" font-size="7" fill="#0284c7">&bull; Broadcasts Invalidate / Write-Back</text>

          <!-- MMU Page Tables -->
          <rect x="15" y="174" width="185" height="56" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="25" y="192" font-size="7.5" font-weight="700" fill="#334155">CPU MMU (Paging Engine)</text>
          <text x="25" y="206" font-size="7" fill="#475569">Translates Virtual &rarr; Physical</text>
          <text x="25" y="218" font-size="6.5" fill="#64748b">Controls PAT / Memory Types (UC vs WB)</text>
        </g>

        <!-- Middle: System Interconnect & IOMMU -->
        <g transform="translate(245, 20)">
          <rect width="265" height="250" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
          <text x="132" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="#059669">SYSTEM INTERCONNECT &amp; IOMMU</text>
          <text x="132" y="38" text-anchor="middle" font-size="7" fill="#64748b">(PCIe Root Complex / VT-d / SMMU)</text>

          <!-- IOMMU Engine Box -->
          <rect x="15" y="50" width="235" height="85" rx="5" fill="#f0fdf4" stroke="#16a34a"/>
          <text x="25" y="68" font-size="8" font-weight="700" fill="#166534">IOMMU (IOVA &rarr; PHYSICAL TRANSLATOR)</text>

          <rect x="25" y="76" width="215" height="22" rx="3" fill="#ffffff" stroke="#86efac"/>
          <text x="35" y="90" font-family="var(--font-mono)" font-size="7" fill="#166534">IOVA: 0x1000 &rarr; Physical DRAM: 0x8F400000</text>

          <text x="25" y="112" font-size="6.5" fill="#15803d">&bull; Hardware DMA isolation &amp; bounds checking</text>
          <text x="25" y="124" font-size="6.5" fill="#15803d">&bull; Assembles scattered 4 KB pages into one IOVA</text>

          <!-- Coherency Snoop Vector -->
          <line x1="15" y1="145" x2="-10" y2="145" stroke="#0284c7" stroke-width="2" marker-end="url(#dma-arr-blue)"/>
          <text x="65" y="152" font-size="6.5" font-family="var(--font-mono)" fill="#0284c7">Snoop Broadcast &rarr;</text>

          <!-- Physical Host DRAM -->
          <rect x="15" y="165" width="235" height="65" rx="5" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="25" y="182" font-size="8" font-weight="700" fill="#0f172a">HOST PHYSICAL RAM (DRAM)</text>
          <rect x="25" y="190" width="100" height="28" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="75" y="208" text-anchor="middle" font-family="var(--font-mono)" font-size="7" fill="#0369a1">Page Frame A</text>
          <rect x="135" y="190" width="100" height="28" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="185" y="208" text-anchor="middle" font-family="var(--font-mono)" font-size="7" fill="#0369a1">Page Frame B</text>
        </g>

        <!-- Right: Bus Master Peripheral Device -->
        <g transform="translate(525, 20)">
          <rect width="220" height="250" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="110" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0f172a">BUS-MASTER PERIPHERAL</text>
          <text x="110" y="38" text-anchor="middle" font-size="7" fill="#64748b">(NVMe Controller / 100 GbE NIC)</text>

          <!-- Device DMA Engine -->
          <rect x="15" y="50" width="190" height="75" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="25" y="68" font-size="8" font-weight="700" fill="#334155">INTERNAL DMA CONTROLLER</text>
          <text x="25" y="84" font-family="var(--font-mono)" font-size="7" fill="#059669">Target: IOVA 0x1000</text>
          <text x="25" y="98" font-family="var(--font-mono)" font-size="7" fill="#059669">Count:  65,536 Bytes</text>
          <text x="25" y="112" font-size="6.5" fill="#64748b">Issues PCIe Memory Writes</text>

          <!-- Outbound Vector to IOMMU -->
          <line x1="15" y1="88" x2="-10" y2="88" stroke="#059669" stroke-width="2.5" marker-end="url(#dma-arr-green)"/>

          <!-- Ring Descriptors -->
          <rect x="15" y="135" width="190" height="95" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="25" y="152" font-size="7.5" font-weight="700" fill="#334155">SCATTER-GATHER LIST (SGL)</text>
          <text x="25" y="168" font-size="7" fill="#475569">&bull; Entry 0: Base 0x8F400000</text>
          <text x="25" y="180" font-size="7" fill="#475569">&bull; Entry 1: Base 0x90200000</text>
          <text x="25" y="194" font-size="6.5" fill="#64748b">Allows non-contiguous</text>
          <text x="25" y="206" font-size="6.5" fill="#64748b">physical memory chaining</text>
          <text x="25" y="218" font-size="6.5" font-weight="700" fill="#166534">&#10003; 1 Interrupt on Complete</text>
        </g>
      </svg>
    </div>

    <h4>The Fundamental Problem: The CPU-DRAM Semantic Gap</h4>
    <p>
      Central processing units read and write memory through high-speed, on-die write-back L1, L2, and L3 caches. A write instruction executed by the CPU does not immediately touch physical DRAM; instead, it updates the CPU's local cache line and marks the line as <strong>Dirty (Modified)</strong>.
    </p>
    <p>
      In contrast, a Direct Memory Access engine is an independent bus master that reads and writes <strong>directly to physical DRAM across the system interconnect</strong>, bypassing CPU caches entirely. This creates two distinct data corruption hazards:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <!-- Hazard 1: Stale Reads -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--danger); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Hazard 1: Stale Reads (Device &rarr; RAM)</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--danger); text-transform: uppercase; margin-bottom: 8px;">Inbound DMA Data Corruption</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Occurs when the peripheral writes new data into physical DRAM while the CPU holds that same memory range in its local L1/L2 cache.
          <br><br>
          <em>The Sequence of Failure:</em>
          <ol style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>CPU previously read buffer at address <code>0x1000</code>; data sits cached in L1.</li>
            <li>NIC DMA writes a new incoming network packet directly into physical DRAM at <code>0x1000</code>.</li>
            <li>CPU executes a read from <code>0x1000</code>. The CPU satisfies the load <strong>directly from its L1 cache</strong>!</li>
            <li><strong>Outcome:</strong> The CPU processes stale, obsolete data, completely blind to the freshly arrived packet in DRAM.</li>
          </ol>
        </p>
      </div>

      <!-- Hazard 2: Dirty Overwrites -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--warning); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Hazard 2: Dirty Overwrites (Cache Eviction)</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--warning); text-transform: uppercase; margin-bottom: 8px;">Silent Data Destruction</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Occurs due to cacheline granularity (typically 64 bytes) and write-back caching policies.
          <br><br>
          <em>The Sequence of Failure:</em>
          <ol style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>CPU modifies a variable located in the same 64-byte cache line as the DMA receive buffer; the line becomes <code>Dirty</code> in L1 cache.</li>
            <li>Device DMAs fresh data into DRAM at that address.</li>
            <li>Moments later, the CPU cache controller suffers a conflict miss and <strong>evicts the dirty cache line back to DRAM</strong>.</li>
            <li><strong>Outcome:</strong> The obsolete CPU cache line overwrites the freshly arrived DMA payload in DRAM, silently destroying the received data!</li>
          </ol>
        </p>
      </div>
    </div>

    <h4>Architectural Solutions: Hardware Snooping vs. Software Maintenance</h4>
    <p>
      Operating systems interface with two fundamentally different hardware caching topologies:
    </p>

    <h5>1. Hardware-Coherent Architectures (x86-64 &amp; Enterprise ARM)</h5>
    <p>
      On standard x86 and enterprise server architectures, cache coherency is enforced completely in silicon via <strong>Bus Snooping</strong> and directory protocols (such as MESI/MOESI):
    </p>
    <ul>
      <li>When a PCIe device writes to physical DRAM, the PCIe Root Complex and Memory Controller broadcast a <strong>snoop transaction</strong> to all CPU cores across the internal coherent interconnect.</li>
      <li>If a CPU core detects that the DMA write address is present in its L1/L2/L3 cache, the hardware cache controller automatically <strong>invalidates</strong> the local cache line.</li>
      <li>If the device reads from DRAM while a CPU core holds dirty uncommitted data in its cache, the snoop controller forces the CPU core to flush its dirty line to the bus first, satisfying the device read with valid data.</li>
      <li><strong>Operating System Impact:</strong> Device driver developers on x86 do not need to execute manual cache flushes. Hardware guarantees transparent memory coherency.</li>
    </ul>

    <h5>2. Non-Coherent Architectures (Embedded ARM, Mobile SoCs, DSPs)</h5>
    <p>
      To conserve silicon die area, reduce design complexity, and minimize battery power consumption, mobile and embedded System-on-Chip (SoC) architectures frequently omit bus snooping logic.
    </p>
    <p>
      On non-coherent systems, <strong>the operating system kernel is legally responsible for executing manual cache maintenance operations before and after every DMA transfer</strong>:
    </p>

    <div style="overflow-x: auto; margin: 18px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 12px; width: 25%;">DMA Operation</th>
            <th style="padding: 10px 12px; width: 35%;">Required Software Cache Action</th>
            <th style="padding: 10px 12px; width: 40%;">Underlying Silicon Purpose</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">DMA Transmit (Outbound)<br><span style="font-size: 0.75rem; color: #64748b;">Host RAM &rarr; Device</span></td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); color: #0284c7;"><strong>Cache Clean (Flush)</strong><br><span style="font-size: 0.75rem; color: #475569;">dma_sync_single_for_device()</span></td>
            <td style="padding: 10px 12px;">Forces the CPU to push any dirty, modified cache lines out to physical DRAM so the peripheral reads fresh, updated data.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #f0fdf4;">
            <td style="padding: 10px 12px; font-weight: 700; color: #166534;">DMA Receive (Inbound)<br><span style="font-size: 0.75rem; color: #166534;">Device &rarr; Host RAM</span></td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); color: #166534;"><strong>Cache Invalidate</strong><br><span style="font-size: 0.75rem; color: #166534;">dma_sync_single_for_cpu()</span></td>
            <td style="padding: 10px 12px; color: #166534;">Discards all CPU cache lines over the destination buffer without writing them back. When the CPU subsequently reads the buffer, it misses L1/L2 and fetches the fresh data from physical DRAM.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h4>The Linux DMA Mapping API</h4>
    <p>
      To write portable device drivers that run identically on hardware-coherent x86 systems and non-coherent ARM platforms, Linux provides the unified <strong>DMA Mapping Framework</strong>:
    </p>

    <pre><code><span class="syn-cmt">/* 1. Consistent (Coherent) DMA Allocation:
      Allocates physically contiguous memory that is mapped as Uncacheable (UC).
      Ideal for circular ring descriptors and command mailboxes accessed continuously. */</span>
<span class="syn-kw">dma_addr_t</span> dma_handle;
<span class="syn-kw">void</span> *ring_buffer = <span class="syn-fn">dma_alloc_coherent</span>(
    dev,
    <span class="syn-num">4096</span>,
    &amp;dma_handle,      <span class="syn-cmt">/* Physical address given to device */</span>
    GFP_KERNEL
);

<span class="syn-cmt">/* 2. Streaming DMA Mapping:
      Used for high-throughput packet and disk buffers allocated via standard kmalloc/page-alloc.
      Automatically executes cache clean/invalidate instructions on non-coherent hardware! */</span>
<span class="syn-kw">dma_addr_t</span> phys_addr = <span class="syn-fn">dma_map_single</span>(
    dev,
    packet_data,
    packet_len,
    DMA_FROM_DEVICE    <span class="syn-cmt">/* Direction: Inbound receive */</span>
);

<span class="syn-cmt">/* Give phys_addr to hardware controller... wait for completion interrupt */</span>

<span class="syn-cmt">/* After interrupt arrives: unmap to invalidate CPU caches before CPU reads packet */</span>
<span class="syn-fn">dma_unmap_single</span>(dev, phys_addr, packet_len, DMA_FROM_DEVICE);</code></pre>

    <h4>The IOMMU: Translation, Isolation, and Virtualization</h4>
    <p>
      In early computer architectures, peripherals placed raw host physical addresses directly onto the system memory bus. In modern enterprise systems, all DMA transactions pass through a dedicated hardware memory management unit: the <strong>I/O Memory Management Unit (IOMMU)</strong> (known as Intel VT-d, AMD-Vi, or ARM SMMU).
    </p>
    <p>
      The IOMMU solves three critical operating system challenges:
    </p>

    <h5>1. IOVA to Physical Address Translation (De-fragmenting Paged Memory)</h5>
    <p>
      User applications allocate large memory buffers that appear contiguous in virtual memory, but are fragmented across hundreds of arbitrary 4 KB page frames in physical DRAM.
    </p>
    <ul>
      <li>Without an IOMMU, the driver must build complex Scatter-Gather Lists, and devices without scatter-gather hardware must copy data through intermediate <strong>Bounce Buffers</strong> (costing massive CPU memory-copy overhead).</li>
      <li>With an IOMMU, the kernel programs <strong>I/O Page Tables</strong>. The IOMMU maps a single, contiguous range of <strong>I/O Virtual Addresses (IOVA)</strong> to the scattered physical page frames in DRAM. The peripheral executes a single, continuous DMA burst without knowing that physical memory is fragmented!</li>
      <li>Furthermore, the IOMMU allows legacy 32-bit DMA devices (limited to 4 GB addressing) to access physical memory located above the 4 GB boundary in 64-bit systems without bounce buffers.</li>
    </ul>

    <h5>2. Memory Protection &amp; DMA Fault Isolation</h5>
    <p>
      Direct Memory Access is inherently hazardous: a compromised PCIe network card or a device with buggy firmware could issue rogue DMA memory writes over the top of the operating system kernel code, page tables, or security tokens.
    </p>
    <ul>
      <li>The IOMMU implements strict <strong>Device Context Tables</strong> indexed by the peripheral's PCIe <strong>Bus/Device/Function (BDF)</strong> identifier.</li>
      <li>Each device is restricted to its own private address translation space. If a peripheral attempts a DMA read or write to an address that has not been explicitly mapped by the OS kernel, the IOMMU blocks the transaction at the hardware layer, halts the transfer, and triggers an uncorrectable PCIe <strong>DMA Remapping Fault</strong> interrupt to the kernel.</li>
    </ul>

    <h5>3. Direct Hardware Passthrough in Virtualization (SR-IOV)</h5>
    <p>
      In cloud and hypervisor environments, operating systems virtualize I/O:
    </p>
    <ul>
      <li>Normally, hypervisors emulate hardware devices in software, introducing significant latency.</li>
      <li>With IOMMU support, the hypervisor can assign a physical PCIe network interface or GPU directly to a guest Virtual Machine (VM).</li>
      <li>The IOMMU translates <strong>Guest Physical Addresses (GPA) directly into Host Physical Addresses (HPA)</strong> at wire speed. The guest VM controls the hardware directly with zero hypervisor intervention and bare-metal performance, while the IOMMU guarantees that the guest VM cannot access host memory outside its assigned slice.</li>
    </ul>"""

def update_section_three():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>3. Direct Memory Access (DMA) &amp; Cache Coherency</h3>"
    end_marker = '<nav class="nav-bar" style="margin-top: 36px;'

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 3 boundaries in Module 02.")
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
            "Expand Section 3 in Module 02 on DMA Coherency, Snooping, and IOMMUs\n\n"
            "Detail stale reads, dirty evictions, non-coherent cache sync APIs,\n"
            "IOMMU IOVA translation, bounce buffers, and add an SVG architecture."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_three():
        run_git_sync()
