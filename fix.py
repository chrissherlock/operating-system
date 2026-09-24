#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 2 of 02-interrupts-and-dma.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "02-interrupts-and-dma.html"
)

EXPANDED_SECTION_TWO_PRE_AID = r"""    <h3>2. The Dual-Phase Interrupt Model: Top-Half vs. Bottom-Half</h3>
    <p>
      In Section 1, we analyzed how the APIC and CPU hardware vector an interrupt into an Interrupt Service Routine (ISR). However, modern kernel developers face an acute microarchitectural conflict when designing driver handlers: <strong>the Interrupt Latency Paradox</strong>.
    </p>

    <div class="math-callout">
      <strong>The Interrupt Latency Paradox:</strong>
      <ul>
        <li>
          <strong>The Constraint (Zero Latency &amp; Interrupts Masked):</strong> When a CPU core vectors into a hardware ISR, hardware interrupts are masked (via <code>RFLAGS.IF = 0</code> in x86-64 or by elevating the processor to the device's DIRQL in Windows NT).
          <br>
          While interrupts are masked, the processor core is <em>deaf to the physical world</em>. If the ISR takes 200 microseconds to execute, the CPU will miss timer ticks, drop incoming packets on other network ports, and cause audio buffer underruns.
        </li>
        <li>
          <strong>The Demand (Heavy Computation &amp; State Mutation):</strong> When a high-speed peripheral finishes an operation, the operating system must perform substantial computation. For an inbound network packet, the OS must compute IP checksums, traverse firewall rule chains, evaluate routing tables, allocate kernel socket buffers (<code>sk_buff</code>), and update TCP sequence numbers. These operations require thousands of instructions, dynamic memory allocations, and lock acquisitions.
        </li>
        <li>
          <strong>The Execution Prohibition:</strong> Code running directly inside a hardware interrupt handler <strong>cannot sleep, cannot block on standard mutexes, cannot wait on condition variables, and cannot touch pageable virtual memory</strong> (a page fault inside an atomic interrupt handler triggers an unrecoverable kernel panic).
        </li>
      </ul>
    </div>

    <!-- Structural Diagram: Dual-Phase Lifecycle -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 2.2: The Dual-Phase Interrupt Lifecycle &mdash; Top-Half to Bottom-Half Handoff</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How the operating system minimizes hardware interrupt disabled latency by splitting execution into an atomic top-half and a deferred bottom-half.</div>

      <svg viewBox="0 0 760 280" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="dp-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="dp-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
          <marker id="dp-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
        </defs>

        <!-- Phase 1: Hardware Trigger & Top-Half (Left) -->
        <g transform="translate(15, 20)">
          <rect width="225" height="240" rx="8" fill="#f8fafc" stroke="#dc2626" stroke-width="1.5"/>
          <text x="112" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="#991b1b">PHASE 1: TOP-HALF (HARD-IRQ)</text>
          <text x="112" y="38" text-anchor="middle" font-size="7" fill="#dc2626">Interrupts Masked &bull; Atomic (&lt; 1 &mu;s)</text>

          <rect x="15" y="50" width="195" height="42" rx="4" fill="#fee2e2" stroke="#dc2626"/>
          <text x="25" y="66" font-size="7.5" font-weight="700" fill="#991b1b">1. HARDWARE VECTOR ENTRY</text>
          <text x="25" y="78" font-family="var(--font-mono)" font-size="7" fill="#7f1d1d">RFLAGS.IF = 0 &bull; DIRQL Active</text>

          <rect x="15" y="100" width="195" height="42" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="25" y="116" font-size="7.5" font-weight="700" fill="#334155">2. CONTROLLER ACKNOWLEDGMENT</text>
          <text x="25" y="128" font-size="7" fill="#64748b">Clears interrupt status bit on device</text>

          <rect x="15" y="150" width="195" height="42" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="25" y="166" font-size="7.5" font-weight="700" fill="#334155">3. ENQUEUE DEFERRED TOKEN</text>
          <text x="25" y="178" font-family="var(--font-mono)" font-size="7" fill="#0284c7">queue_dpc() / raise_softirq()</text>

          <rect x="15" y="200" width="195" height="28" rx="4" fill="#fee2e2" stroke="#dc2626"/>
          <text x="112" y="218" text-anchor="middle" font-size="7" font-weight="700" fill="#dc2626">4. IMMEDIATE EXIT (EOI Sent)</text>
        </g>

        <!-- Transition Vector: Interrupts Re-enabled -->
        <g transform="translate(245, 120)">
          <line x1="0" y1="20" x2="35" y2="20" stroke="#0284c7" stroke-width="2.5" marker-end="url(#dp-arr-blue)"/>
          <text x="18" y="10" text-anchor="middle" font-size="7" font-weight="700" fill="#0284c7">RE-ENABLE</text>
          <text x="18" y="34" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#64748b">IF = 1</text>
        </g>

        <!-- Phase 2: Bottom-Half / Deferred Dispatch (Center) -->
        <g transform="translate(285, 20)">
          <rect width="225" height="240" rx="8" fill="#f8fafc" stroke="#0284c7" stroke-width="2"/>
          <text x="112" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0284c7">PHASE 2: BOTTOM-HALF (DEFERRED)</text>
          <text x="112" y="38" text-anchor="middle" font-size="7" fill="#64748b">Interrupts Enabled &bull; Preemptible</text>

          <rect x="15" y="50" width="195" height="42" rx="4" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="25" y="66" font-size="7.5" font-weight="700" fill="#0369a1">1. DISPATCH SELECTION</text>
          <text x="25" y="78" font-size="7" fill="#0284c7">Softirq / Tasklet / DPC Queue</text>

          <rect x="15" y="100" width="195" height="52" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="25" y="116" font-size="7.5" font-weight="700" fill="#334155">2. HEAVY PROTOCOL PARSING</text>
          <text x="25" y="128" font-size="7" fill="#64748b">&bull; TCP Checksum validation</text>
          <text x="25" y="140" font-size="7" fill="#64748b">&bull; IP Routing table lookups</text>

          <rect x="15" y="160" width="195" height="42" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="25" y="176" font-size="7.5" font-weight="700" fill="#334155">3. BUFFER DESCRIPTOR RECYCLE</text>
          <text x="25" y="188" font-size="7" fill="#64748b">Returns DMA descriptors to ring</text>

          <rect x="15" y="210" width="195" height="20" rx="2" fill="#dcfce7"/>
          <text x="112" y="224" text-anchor="middle" font-size="6.5" font-weight="700" fill="#166534">&#10003; Can be preempted by new IRQs!</text>
        </g>

        <!-- Handoff to User Space -->
        <g transform="translate(515, 120)">
          <line x1="0" y1="20" x2="35" y2="20" stroke="#059669" stroke-width="2.5" marker-end="url(#dp-arr-green)"/>
          <text x="18" y="10" text-anchor="middle" font-size="7" font-weight="700" fill="#059669">WAKE</text>
          <text x="18" y="34" text-anchor="middle" font-size="6.5" fill="#64748b">Thread</text>
        </g>

        <!-- User Space Delivery (Right) -->
        <g transform="translate(555, 20)">
          <rect width="190" height="240" rx="8" fill="#f8fafc" stroke="#059669" stroke-width="1.5"/>
          <text x="95" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="#166534">USER / PROCESS CONTEXT</text>
          <text x="95" y="38" text-anchor="middle" font-size="7" fill="#64748b">Scheduled Process Execution</text>

          <rect x="12" y="50" width="166" height="56" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="20" y="68" font-size="7.5" font-weight="700" fill="#334155">USER SOCKET QUEUE</text>
          <text x="20" y="82" font-family="var(--font-mono)" font-size="7" fill="#059669">recv(sockfd, buf, len);</text>
          <text x="20" y="94" font-size="6.5" fill="#64748b">Payload ready in RAM</text>

          <rect x="12" y="116" width="166" height="56" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="20" y="134" font-size="7.5" font-weight="700" fill="#334155">SCHEDULER STATE</text>
          <text x="20" y="148" font-family="var(--font-mono)" font-size="7" fill="#0284c7">TASK_RUNNING</text>
          <text x="20" y="160" font-size="6.5" fill="#64748b">Thread woken from sleep</text>

          <rect x="12" y="182" width="166" height="46" rx="4" fill="#dcfce7" stroke="#16a34a"/>
          <text x="95" y="202" text-anchor="middle" font-size="7.5" font-weight="700" fill="#166534">&#10003; ZERO PACKET LOSS</text>
          <text x="95" y="216" text-anchor="middle" font-size="6.5" fill="#15803d">System preserved responsive</text>
        </g>
      </svg>
    </div>

    <h4>The Core Separation of Concerns</h4>
    <p>
      To resolve the latency paradox, all production operating systems partition interrupt handling into two distinct, cooperative execution stages:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <!-- Top-Half Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--danger); border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Phase 1: The Top-Half (Hard-IRQ / DIRQL)</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--danger); text-transform: uppercase; margin-bottom: 8px;">Atomic &bull; Hardware Interrupts Masked &bull; Budget: &lt; 1 &mu;s</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Executes immediately when the CPU vectors through the IDT. Its sole mission is to interact with physical controller registers and exit as fast as possible.
          <br><br>
          <strong>Strict Mandatory Duties:</strong>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li><strong>Acknowledge Hardware:</strong> Reads or writes the controller status register to clear the interrupt flag on the physical device (preventing re-triggering).</li>
            <li><strong>Retrieve Critical Tokens:</strong> Reads hardware DMA ring pointers, status registers, and error codes.</li>
            <li><strong>Enqueue Deferred Task:</strong> Schedules a bottom-half entity (Softirq, Tasklet, or DPC) containing pointers to the received data.</li>
            <li><strong>Immediate Exit:</strong> Sends End-Of-Interrupt (EOI) to Local APIC and executes <code>iretq</code> to immediately restore CPU interrupt availability!</li>
          </ul>
        </p>
      </div>

      <!-- Bottom-Half Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Phase 2: The Bottom-Half (Softirq / DPC)</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--success); text-transform: uppercase; margin-bottom: 8px;">Asynchronous &bull; Hardware Interrupts Enabled &bull; Preemptible</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Executes shortly after the top-half exits, scheduled by the kernel when the CPU is not servicing higher-priority hardware interrupts.
          <br><br>
          <strong>Heavy Processing Capabilities:</strong>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li><strong>Runs with Interrupts Enabled:</strong> New incoming hardware interrupts can freely preempt the bottom-half to acknowledge physical hardware.</li>
            <li><strong>Heavy Computational Payload:</strong> Validates packet integrity, computes cryptographic hashes, executes disk block buffering, and delivers data to user sockets.</li>
            <li><strong>Thread Synchronization:</strong> Depending on the bottom-half mechanism (Workqueues vs Softirqs), can acquire sleeping mutexes, allocate memory, and wake application threads waiting in <code>read()</code> or <code>select()</code>.</li>
          </ul>
        </p>
      </div>
    </div>

    <h4>Deep Dive: The Linux Deferred Execution Subsystems</h4>
    <p>
      The Linux kernel provides three distinct architectural mechanisms for bottom-half deferral, each tailored to specific latency and concurrency profiles:
    </p>

    <div style="overflow-x: auto; margin: 18px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 12px; width: 18%;">Mechanism</th>
            <th style="padding: 10px 12px; width: 22%;">Execution Context</th>
            <th style="padding: 10px 12px; width: 25%;">Concurrency Guarantee</th>
            <th style="padding: 10px 12px; width: 35%;">Permitted Operations</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Softirqs</td>
            <td style="padding: 10px 12px; color: #dc2626; font-weight: 600;">Interrupt Context (Atomic)</td>
            <td style="padding: 10px 12px;"><strong>Fully Concurrent:</strong> Same softirq type can run on multiple CPU cores simultaneously.</td>
            <td style="padding: 10px 12px; font-size: 0.82rem;"><strong>Cannot sleep!</strong> Must be completely reentrant. Used exclusively for top-performance subsystems (<code>NET_RX</code>, <code>BLOCK</code>, <code>TIMER</code>, <code>RCU</code>).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Tasklets</td>
            <td style="padding: 10px 12px; color: #dc2626; font-weight: 600;">Interrupt Context (Atomic)</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 600;"><strong>Serialized per Tasklet:</strong> Same tasklet will NEVER run on two cores at once.</td>
            <td style="padding: 10px 12px; font-size: 0.82rem;"><strong>Cannot sleep!</strong> Simplifies driver development by eliminating internal multi-core lock contention. Built on softirqs.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #f0fdf4;">
            <td style="padding: 10px 12px; font-weight: 700; color: #166534;">Workqueues</td>
            <td style="padding: 10px 12px; color: #166534; font-weight: 600;">Process Context (kworker threads)</td>
            <td style="padding: 10px 12px;">Standard kernel threads scheduled by CFS.</td>
            <td style="padding: 10px 12px; font-size: 0.82rem; color: #166534;"><strong>CAN SLEEP!</strong> Can allocate memory (<code>GFP_KERNEL</code>), acquire mutexes, execute blocking disk I/O, and wait on condition variables.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h5>Modern Threaded IRQs in Linux</h5>
    <p>
      In modern Linux, writing manual softirqs or tasklets is increasingly superseded by <strong>Threaded Interrupt Handlers</strong> (<code>request_threaded_irq()</code>):
    </p>

    <pre><code><span class="syn-cmt">/* Registering a Modern Linux Threaded Interrupt Handler */</span>
<span class="syn-kw">int</span> <span class="syn-fn">request_threaded_irq</span>(
    <span class="syn-kw">unsigned int</span> irq,
    irq_handler_t quick_check_handler, <span class="syn-cmt">/* Top-Half (Hard-IRQ) */</span>
    irq_handler_t thread_worker,       <span class="syn-cmt">/* Bottom-Half (Preemptible Kernel Thread) */</span>
    <span class="syn-kw">unsigned long</span> irqflags,
    <span class="syn-kw">const char</span> *devname,
    <span class="syn-kw">void</span> *dev_id
);

<span class="syn-cmt">/* Top-Half: Runs with hardware interrupts disabled */</span>
<span class="syn-kw">static</span> irqreturn_t <span class="syn-fn">quick_check_handler</span>(<span class="syn-kw">int</span> irq, <span class="syn-kw">void</span> *dev_id) {
    <span class="syn-kw">struct</span> my_device *dev = (<span class="syn-kw">struct</span> my_device *)dev_id;
    <span class="syn-kw">if</span> (!(<span class="syn-fn">read_reg</span>(dev, REG_STATUS) &amp; STATUS_INTERRUPT_ACTIVE)) {
        <span class="syn-kw">return</span> IRQ_NONE; <span class="syn-cmt">/* Not our interrupt (shared IRQ line) */</span>
    }
    <span class="syn-fn">write_reg</span>(dev, REG_ACK, ACK_BIT); <span class="syn-cmt">/* Acknowledge controller */</span>
    <span class="syn-kw">return</span> IRQ_WAKE_THREAD;           <span class="syn-cmt">/* Kernel automatically wakes thread_worker! */</span>
}

<span class="syn-cmt">/* Bottom-Half: Runs as dedicated kernel thread `irq/42-mydev` (Can sleep!) */</span>
<span class="syn-kw">static</span> irqreturn_t <span class="syn-fn">thread_worker</span>(<span class="syn-kw">int</span> irq, <span class="syn-kw">void</span> *dev_id) {
    <span class="syn-fn">mutex_lock</span>(&amp;dev_lock);            <span class="syn-cmt">/* Legal: Threaded IRQs can acquire mutexes */</span>
    <span class="syn-fn">parse_inbound_data</span>(dev_id);
    <span class="syn-fn">mutex_unlock</span>(&amp;dev_lock);
    <span class="syn-kw">return</span> IRQ_HANDLED;
}</code></pre>

    <h4>Deep Dive: Windows NT Interrupt Architecture &mdash; DIRQL to DPC</h4>
    <p>
      The Windows NT kernel implements a rigorous, hardware-enforced priority model governed by <strong>Interrupt Request Levels (IRQLs)</strong>:
    </p>

    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 18px; margin: 18px 0;">
      <h4 style="margin: 0 0 8px 0; font-size: 0.95rem; color: #0f172a;">The Windows NT IRQL Hierarchy</h4>
      <div style="font-family: var(--font-mono); font-size: 0.82rem; line-height: 1.8; color: #334155;">
        <span style="color: #dc2626; font-weight: 700;">HIGH_LEVEL (31):</span> Machine Check, catastrophic hardware failover<br>
        <span style="color: #dc2626; font-weight: 700;">IPI_LEVEL / CLOCK_LEVEL (27&ndash;28):</span> Inter-processor interrupts, system clock timer ticks<br>
        <span style="color: #d97706; font-weight: 700;">DIRQL (Device IRQL, 3&ndash;26):</span> Hardware Interrupt Service Routines (ISRs)<br>
        <span style="color: #0284c7; font-weight: 700;">DISPATCH_LEVEL (2):</span> Deferred Procedure Calls (DPCs), thread scheduler dispatcher<br>
        <span style="color: #059669; font-weight: 700;">APC_LEVEL (1):</span> Asynchronous Procedure Calls, filesystem completion<br>
        <span style="color: #059669; font-weight: 700;">PASSIVE_LEVEL (0):</span> Standard user applications and regular kernel threads
      </div>
    </div>

    <h5>The Windows NT Execution Sequence</h5>
    <ol>
      <li>
        <strong>ISR Execution (at DIRQL):</strong> When a peripheral asserts an interrupt, the hardware raises the CPU core's IRQL to the device's assigned <strong>DIRQL</strong> (Device IRQL, e.g. IRQL 12).
        <br>
        Code at DIRQL is strictly prohibited from touching pageable virtual memory, acquiring user mutexes, or waiting on kernel events. The ISR reads the device registers, copies pointer references, and queues a DPC:
        <pre><code><span class="syn-fn">KeInsertQueueDpc</span>(&amp;DeviceExtension-&gt;DpcObject, SystemArgument1, SystemArgument2);</code></pre>
      </li>
      <li>
        <strong>Dropping to DISPATCH_LEVEL:</strong> The ISR exits, sending EOI. The Windows kernel checks if any other hardware interrupts are pending. If none exist, the kernel drops the processor's IRQL to <strong><code>DISPATCH_LEVEL</code> (IRQL 2)</strong>.
      </li>
      <li>
        <strong>DPC Execution:</strong> The Windows kernel maintains a per-processor DPC queue. At <code>DISPATCH_LEVEL</code>, the kernel drains queued DPC routines with <strong>hardware interrupts fully enabled</strong> (a DIRQL interrupt can preempt a DPC at any time).
      </li>
      <li>
        <strong>The Strict Rules of DISPATCH_LEVEL:</strong> While at <code>DISPATCH_LEVEL</code>, code is executing outside of any particular thread context. Therefore:
        <ul>
          <li><strong>Cannot Wait with Non-Zero Timeout:</strong> Calling <code>KeWaitForSingleObject</code> with a non-zero timeout is illegal (there is no thread to put to sleep!).</li>
          <li><strong>No Page Faults Permitted:</strong> All code and data buffers accessed inside a DPC must reside in <strong>Non-Paged Kernel Pool (RAM-resident)</strong>. Triggering a page fault at <code>DISPATCH_LEVEL</code> causes Windows to immediately crash with <code>BUGCHECK 0x0A: IRQL_NOT_LESS_OR_EQUAL</code>!</li>
        </ul>
      </li>
    </ol>"""

def update_section_two():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>2. The Dual-Phase Interrupt Model: Top-Half vs. Bottom-Half</h3>"
    end_marker = "<!-- Directed Narrative Stepper: Dual-Phase Interrupt Lifecycle -->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not find Section 2 boundaries before the interactive stepper.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_TWO_PRE_AID + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 2 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 2 in Module 02 on Top-Half vs Bottom-Half architectures\n\n"
            "Detail hard-IRQ latency budgets, Linux softirqs/tasklets/workqueues,\n"
            "Windows DIRQL to DISPATCH_LEVEL DPC mechanics, and add an SVG lifecycle."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_two():
        run_git_sync()
