#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 1 of 01-io-hardware-device-controllers.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "01-io-hardware-device-controllers.html"
)

EXPANDED_SECTION_ONE = r"""    <h3>1. The Physical Spectrum &amp; Device Categorization</h3>
    <p>
      An operating system is fundamentally an orchestrator of asynchronous, heterogeneous hardware. While modern CPU cores execute instructions deterministically within uniform sub-nanosecond clock cycles (3&ndash;5 GHz), <strong>input/output peripherals exhibit performance and latency characteristics spanning more than ten orders of magnitude</strong>.
    </p>
    <p>
      Managing this hardware divergence presents a profound architectural challenge: the operating system must provide uniform, clean abstractions to application software (such as the POSIX file system and socket interfaces) without degrading the throughput of multi-gigabyte silicon buses or starving under slow, human-operated peripherals.
    </p>

    <!-- Structural Diagram: Physical Spectrum & Data Rate Hierarchy -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 1.0: The Ten Orders of Magnitude I/O Data Rate Hierarchy</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">Logarithmic comparison of peripheral data transfer rates alongside CPU cycle wait penalties.</div>

      <svg viewBox="0 0 760 260" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <!-- Logarithmic Scale Bar (Top) -->
        <g transform="translate(30, 30)">
          <line x1="0" y1="20" x2="700" y2="20" stroke="#94a3b8" stroke-width="2"/>

          <!-- Log Ticks: 10 B/s, 1 KB/s, 100 KB/s, 10 MB/s, 1 GB/s, 100 GB/s -->
          <line x1="0" y1="15" x2="0" y2="25" stroke="#475569" stroke-width="2"/>
          <text x="0" y="10" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#475569">10 B/s</text>

          <line x1="140" y1="15" x2="140" y2="25" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="140" y="10" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#64748b">1 KB/s</text>

          <line x1="280" y1="15" x2="280" y2="25" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="280" y="10" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#64748b">100 KB/s</text>

          <line x1="420" y1="15" x2="420" y2="25" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="420" y="10" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#64748b">10 MB/s</text>

          <line x1="560" y1="15" x2="560" y2="25" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="560" y="10" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#64748b">1 GB/s</text>

          <line x1="700" y1="15" x2="700" y2="25" stroke="#475569" stroke-width="2"/>
          <text x="700" y="10" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0284c7">100+ GB/s</text>
        </g>

        <!-- Peripheral Categories Placed on Log Scale -->
        <g transform="translate(30, 70)">
          <!-- Keyboard / Mouse -->
          <g transform="translate(10, 0)">
            <rect width="105" height="60" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="52" y="18" text-anchor="middle" font-size="8" font-weight="700" fill="#991b1b">KEYBOARD / MOUSE</text>
            <text x="52" y="32" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#dc2626">10 &ndash; 100 B/s</text>
            <text x="52" y="48" text-anchor="middle" font-size="7" fill="#7f1d1d">Human response time</text>
          </g>

          <!-- Audio / UART -->
          <g transform="translate(160, 0)">
            <rect width="115" height="60" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
            <text x="57" y="18" text-anchor="middle" font-size="8" font-weight="700" fill="#92400e">SERIAL UART / AUDIO</text>
            <text x="57" y="32" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#b45309">115 Kb/s &ndash; 2 MB/s</text>
            <text x="57" y="48" text-anchor="middle" font-size="7" fill="#b45309">Isochronous byte flow</text>
          </g>

          <!-- Magnetic Hard Drives -->
          <g transform="translate(330, 0)">
            <rect width="125" height="60" rx="4" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
            <text x="62" y="18" text-anchor="middle" font-size="8" font-weight="700" fill="#0369a1">MECHANICAL DISK (HDD)</text>
            <text x="62" y="32" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0284c7">100 &ndash; 250 MB/s</text>
            <text x="62" y="48" text-anchor="middle" font-size="7" fill="#0369a1">Millisecond mechanical seeks</text>
          </g>

          <!-- NVMe SSDs & High-Speed NICs -->
          <g transform="translate(510, 0)">
            <rect width="180" height="60" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
            <text x="90" y="18" text-anchor="middle" font-size="8.5" font-weight="700" fill="#166534">PCIe 5.0 NVMe / 400 GbE</text>
            <text x="90" y="32" text-anchor="middle" font-family="var(--font-mono)" font-size="8" font-weight="700" fill="#15803d">16 &ndash; 64 GB/s (Bus Master DMA)</text>
            <text x="90" y="48" text-anchor="middle" font-size="7" fill="#166534">Saturates memory controllers</text>
          </g>
        </g>

        <!-- Cycle Inefficiency Annotation -->
        <g transform="translate(30, 160)">
          <rect width="700" height="75" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
          <text x="20" y="24" font-size="8.5" font-weight="700" fill="#0f172a">THE CPU CYCLE WASTAGE DILEMMA (Scale of 1 CPU Clock Cycle &asymp; 0.25 ns at 4 GHz):</text>
          <text x="20" y="42" font-size="8" fill="#334155">&bull; Reading an L1 Cache hit: <tspan font-family="var(--font-mono)" font-weight="700" fill="#16a34a">~4 cycles</tspan> (1 nanosecond). Equivalent to glancing at a wrist watch.</text>
          <text x="20" y="56" font-size="8" fill="#334155">&bull; Reading from PCIe NVMe Flash: <tspan font-family="var(--font-mono)" font-weight="700" fill="#0284c7">~40,000 cycles</tspan> (10 microseconds). Equivalent to walking to the local grocery store.</text>
          <text x="20" y="70" font-size="8" fill="#334155">&bull; Seeking a block on a Mechanical HDD: <tspan font-family="var(--font-mono)" font-weight="700" fill="#dc2626">~20,000,000 to 40,000,000 cycles</tspan> (5 to 10 milliseconds). Equivalent to a six-month sabbatical!</text>
        </g>
      </svg>
    </div>

    <h4>Taxonomy of I/O Peripherals</h4>
    <p>
      Operating system kernels classify physical devices according to their operational semantics, access mechanisms, and structural boundaries:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <!-- Block Devices Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--accent); border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a;">1. Block Devices</h4>
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--accent); text-transform: uppercase; margin-bottom: 8px;">Random-Access Persistent Storage</div>
        <p style="margin: 0; font-size: 0.84rem; color: #475569; line-height: 1.5;">
          Data is organized into fixed-size, independently addressable storage units called <strong>blocks</strong> (traditionally 512 bytes, modernized to <strong>4096 bytes / 4Kn</strong>).
          <br><br>
          <strong>Defining Characteristics:</strong>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.82rem;">
            <li><strong>Independent Addressability:</strong> The operating system can read or write any arbitrary block <i>N</i> without reading or modifying blocks <i>0 &hellip; N-1</i>.</li>
            <li><strong>Random Access (Seekable):</strong> Supports <code>lseek()</code>; pointers can jump backwards and forwards across the logical volume.</li>
            <li><strong>OS Subsystem:</strong> Interfaced through the OS <strong>Page Cache / Unified Buffer Cache</strong>. Requests are queued, sorted, and merged by the Block I/O Layer and disk schedulers before reaching device drivers.</li>
            <li><strong>Examples:</strong> NVMe SSDs, SATA hard drives, SAN LUNs, USB mass storage drives.</li>
          </ul>
        </p>
      </div>

      <!-- Character Devices Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--warning); border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a;">2. Character (Stream) Devices</h4>
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--warning); text-transform: uppercase; margin-bottom: 8px;">Sequential Non-Seekable Byte Streams</div>
        <p style="margin: 0; font-size: 0.84rem; color: #475569; line-height: 1.5;">
          Data is produced or consumed as an unorganized, sequential <strong>stream of individual bytes</strong> without block boundaries.
          <br><br>
          <strong>Defining Characteristics:</strong>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.82rem;">
            <li><strong>Non-Addressable:</strong> Bytes cannot be addressed individually by physical location; once a byte is consumed from the queue, it cannot be re-read.</li>
            <li><strong>Non-Seekable:</strong> Seeking is illegal. Invoking <code>lseek()</code> on a character device returns <code>-1</code> with <code>errno = ESPIPE</code> (Illegal seek).</li>
            <li><strong>OS Subsystem:</strong> Streams pass directly through device driver queues and line disciplines (e.g. <code>termios</code>) without page cache buffering.</li>
            <li><strong>Examples:</strong> Keyboards, computer mice, serial UARTs, MIDI synthesizers, pseudoterminals (PTYs), and hardware random number generators (<code>/dev/urandom</code>).</li>
          </ul>
        </p>
      </div>

      <!-- Network Devices Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a;">3. Network Devices</h4>
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--success); text-transform: uppercase; margin-bottom: 8px;">Packet-Switched Frame Endpoints</div>
        <p style="margin: 0; font-size: 0.84rem; color: #475569; line-height: 1.5;">
          Peripherals that transmit and receive structured data frames across transmission media.
          <br><br>
          <strong>Defining Characteristics:</strong>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.82rem;">
            <li><strong>Discrete Packet Framing:</strong> Neither purely stream-like nor block-like; data arrives as discrete packets with variable headers and payloads (Ethernet frames, IP datagrams).</li>
            <li><strong>Specialized Socket Abstraction:</strong> Network cards do not map to ordinary file nodes in <code>/dev</code>; user applications interface via the <strong>BSD Socket API</strong> (<code>socket()</code>, <code>bind()</code>, <code>sendmsg()</code>, <code>recvmsg()</code>).</li>
            <li><strong>Ring-Buffer Queuing:</strong> Driven by asynchronous transmit (TX) and receive (RX) DMA descriptor rings, serviced by polling engines (Linux NAPI).</li>
            <li><strong>Examples:</strong> 10/400 GbE NICs, Wi-Fi 7 adapters, Cellular modems, InfiniBand host channel adapters.</li>
          </ul>
        </p>
      </div>

      <!-- Specialized / Clock Devices Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid #7c3aed; border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a;">4. Timers, Clocks &amp; Memory-Mapped Devices</h4>
        <div style="font-size: 0.75rem; font-weight: 700; color: #7c3aed; text-transform: uppercase; margin-bottom: 8px;">Non-Data &amp; Direct Access Endpoints</div>
        <p style="margin: 0; font-size: 0.84rem; color: #475569; line-height: 1.5;">
          Specialized hardware units that do not fit classical byte-pump models:
          <br><br>
          <strong>Subcategories:</strong>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.82rem;">
            <li><strong>Clocks &amp; Timers:</strong> Generate periodic electrical ticks or one-shot deadlines without payload data (HPET, Local APIC timer, TSC). Drive operating system preemption, process scheduling, and wall-clock timekeeping.</li>
            <li><strong>Direct Access (DAX) Memory:</strong> Non-Volatile Dual in-line Memory Modules (NVDIMMs) and Compute Express Link (CXL) storage. Mapped directly into virtual address space via page tables, bypassing all OS block and buffer layers.</li>
            <li><strong>Framebuffers / GPUs:</strong> Memory-mapped display surfaces where pixels are written directly into video RAM via MMIO apertures.</li>
          </ul>
        </p>
      </div>
    </div>

    <h4>Dimensions of Functional Differentiation</h4>
    <p>
      When designing an I/O architecture, kernel architects classify each device along five orthogonal operational dimensions:
    </p>
    <div style="overflow-x: auto; margin: 18px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 12px; width: 22%;">Dimension</th>
            <th style="padding: 10px 12px; width: 38%;">Option A</th>
            <th style="padding: 10px 12px; width: 40%;">Option B</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Data Transfer Granularity</td>
            <td style="padding: 10px 12px;"><strong>Byte-at-a-time:</strong> Data flows as individual characters (serial ports, keyboards).</td>
            <td style="padding: 10px 12px;"><strong>Block / Packet:</strong> Data is transferred in discrete multi-kilobyte bursts (disks, NICs).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Access Sequence</td>
            <td style="padding: 10px 12px;"><strong>Sequential:</strong> Must access data in strict chronological order; cannot backtrack.</td>
            <td style="padding: 10px 12px;"><strong>Random Access:</strong> Any block or record can be accessed independently in constant time.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Synchronization Mode</td>
            <td style="padding: 10px 12px;"><strong>Synchronous (Blocking):</strong> Calling thread is suspended until hardware execution completes.</td>
            <td style="padding: 10px 12px;"><strong>Asynchronous (Overlapped):</strong> System call returns immediately; kernel signals via epoll/io_uring/completion.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Sharing Capability</td>
            <td style="padding: 10px 12px;"><strong>Sharable:</strong> Multiple concurrent processes access device simultaneously (file system disk).</td>
            <td style="padding: 10px 12px;"><strong>Dedicated:</strong> Exclusively bound to a single thread at a time (audio recording stream, tape drive).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #f0fdf4;">
            <td style="padding: 10px 12px; font-weight: 700; color: #166534;">Speed &amp; Latency Class</td>
            <td style="padding: 10px 12px; color: #166534;"><strong>Latency-Critical (Sub-microsecond):</strong> Ultra-fast PCIe/CXL devices requiring polling or kernel bypass (DPDK, SPDK).</td>
            <td style="padding: 10px 12px; color: #166534;"><strong>Throughput-Critical (Milliseconds):</strong> Mechanical or network endpoints where OS scheduling and batching dominate.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h4>The POSIX Interface Boundary</h4>
    <p>
      The Unix abstraction <em>"everything is a file"</em> maps peripheral devices directly into the file system namespace under the <code>/dev</code> directory, exposing standard file descriptors:
    </p>

    <pre><code><span class="syn-cmt">/* Interfacing with Different Device Classes via POSIX System Calls */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;fcntl.h&gt;</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;unistd.h&gt;</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;sys/ioctl.h&gt;</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;termios.h&gt;</span>

<span class="syn-cmt">/* 1. Block Device Interaction (Raw Partition Access) */</span>
<span class="syn-kw">int</span> block_fd = <span class="syn-fn">open</span>(<span class="syn-str">"/dev/nvme0n1p1"</span>, O_RDWR | O_DIRECT);
<span class="syn-fn">lseek</span>(block_fd, <span class="syn-num">4096</span> * <span class="syn-num">100</span>, SEEK_SET);   <span class="syn-cmt">/* Valid: Seek directly to Sector 100 */</span>
<span class="syn-fn">read</span>(block_fd, buffer, <span class="syn-num">4096</span>);             <span class="syn-cmt">/* Read exact physical sector */</span>

<span class="syn-cmt">/* 2. Character Device Interaction (Serial Port Terminal) */</span>
<span class="syn-kw">int</span> char_fd = <span class="syn-fn">open</span>(<span class="syn-str">"/dev/ttyS0"</span>, O_RDWR | O_NOCTTY);
<span class="syn-kw">off_t</span> err = <span class="syn-fn">lseek</span>(char_fd, <span class="syn-num">0</span>, SEEK_SET); <span class="syn-cmt">/* INVALID: Returns -1, errno = ESPIPE */</span>
<span class="syn-kw">struct</span> termios tty;
<span class="syn-fn">ioctl</span>(char_fd, TCGETS, &amp;tty);             <span class="syn-cmt">/* Out-of-band control via ioctl */</span>
<span class="syn-fn">write</span>(char_fd, <span class="syn-str">"AT\r\n"</span>, <span class="syn-num">4</span>);              <span class="syn-cmt">/* Sequential byte stream */</span></code></pre>

    <div class="math-callout">
      <strong>The Role of the ioctl() Escape Hatch:</strong>
      <br>
      While standard file operations (<code>read()</code>, <code>write()</code>, <code>close()</code>) satisfy generic byte transfers, hardware peripherals possess unique device-specific capabilities (e.g. setting serial baud rates, ejecting optical drives, querying NVMe SMART temperature sensors, or configuring audio sample rates).
      <br>
      To support device-specific commands without cluttering the kernel with hundreds of distinct system calls, Unix provides <strong><code>ioctl()</code> (Input/Output Control)</strong>:
      <pre><code><span class="syn-kw">int</span> ioctl(<span class="syn-kw">int</span> fd, <span class="syn-kw">unsigned long</span> request, ...);</code></pre>
      The <code>request</code> code is decoded by the specific device driver, providing an extensible command escape hatch directly to the hardware controller.
    </div>"""

def update_section_one():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>1. The Physical Spectrum &amp; Device Categorization</h3>"
    end_marker = "<h3>2. Device Controllers: The Electronic Bridge</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not find Section 1 boundaries in Module 01.")
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
            "Expand Section 1 of Module 01 with physical spectrum and taxonomy\n\n"
            "Detail 10 orders of magnitude transfer divergence, block vs. character\n"
            "vs. network semantics, POSIX API boundaries, and add an SVG spectrum chart."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_one():
        run_git_sync()
