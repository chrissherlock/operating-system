#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 2 in 01-io-hardware-device-controllers.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "01-io-hardware-device-controllers.html"
)

EXPANDED_SECTION_TWO = r"""    <h3>2. Device Controllers: The Electronic Bridge</h3>
    <p>
      Computer systems do not connect central processing units directly to physical mechanical motors, laser diodes, or flash silicon cells. Doing so would paralyze the processor: CPU registers cannot interpret the millivolt-level analog variations of an optical sensor, nor can instruction decoders accommodate the physical delay of a spinning magnetic platter.
    </p>
    <p>
      Instead, modern I/O systems enforce a strict architectural partition between two components:
    </p>
    <ol>
      <li><strong>The Physical / Mechanical Unit:</strong> The transducer or peripheral medium itself (e.g. glass platter surfaces, read/write heads, voice-coil actuators, silicon NAND flash floating gates, optical fiber transceivers, or keyboard matrix contact switches).</li>
      <li><strong>The Electronic Controller (Host Adapter):</strong> A specialized silicon chip, PCIe add-in card, or motherboard chipset module that presents a standardized digital register interface to the system bus while generating raw, timing-critical electrical signals to drive the physical peripheral.</li>
    </ol>

    <!-- Structural Diagram: Deep Controller Microarchitecture -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 1.1: Internal Microarchitecture of an Enterprise Device Controller</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How the controller decouples high-speed host bus protocol logic from physical-layer bitstream deserialization and error correction.</div>

      <svg viewBox="0 0 760 280" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="dc2-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="dc2-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
          <marker id="dc2-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
        </defs>

        <!-- System Bus Domain (Left) -->
        <g transform="translate(15, 20)">
          <rect width="130" height="240" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="65" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0f172a">SYSTEM BUS</text>
          <text x="65" y="38" text-anchor="middle" font-size="7" fill="#64748b">(PCIe 5.0 / AXI / CXL)</text>

          <rect x="10" y="52" width="110" height="30" rx="3" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="65" y="71" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">Address Bus</text>

          <rect x="10" y="90" width="110" height="30" rx="3" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="65" y="109" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">Data Bus (64-bit)</text>

          <rect x="10" y="128" width="110" height="30" rx="3" fill="#f1f5f9" stroke="#cbd5e1"/>
          <text x="65" y="147" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#475569">Control Lines</text>

          <rect x="10" y="166" width="110" height="30" rx="3" fill="#fee2e2" stroke="#dc2626"/>
          <text x="65" y="185" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#991b1b">MSI-X / IRQ Line</text>

          <rect x="10" y="204" width="110" height="24" rx="3" fill="#dcfce7" stroke="#16a34a"/>
          <text x="65" y="220" text-anchor="middle" font-family="var(--font-mono)" font-size="7" fill="#166534">DMA Master Lines</text>
        </g>

        <!-- Interconnect Arrow -->
        <line x1="145" y1="140" x2="175" y2="140" stroke="#0284c7" stroke-width="2" marker-end="url(#dc2-arr-blue)"/>

        <!-- The Device Controller Box (Center) -->
        <g transform="translate(180, 20)">
          <rect width="380" height="240" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <text x="20" y="24" font-size="10.5" font-weight="700" fill="#0284c7">DEVICE CONTROLLER (HOST ADAPTER ASIC)</text>

          <!-- Register Block -->
          <g transform="translate(15, 38)">
            <rect width="165" height="185" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
            <text x="82" y="18" text-anchor="middle" font-size="8" font-weight="700" fill="#334155">HOST-ACCESSIBLE REGISTERS</text>

            <rect x="10" y="26" width="145" height="24" rx="2" fill="#ffffff" stroke="#94a3b8"/>
            <text x="18" y="42" font-family="var(--font-mono)" font-size="7.5" fill="#0f172a">STATUS (RO):</text>
            <text x="145" y="42" text-anchor="end" font-family="var(--font-mono)" font-size="7" font-weight="700" fill="#dc2626">BUSY|DRQ|ERR</text>

            <rect x="10" y="56" width="145" height="24" rx="2" fill="#ffffff" stroke="#94a3b8"/>
            <text x="18" y="72" font-family="var(--font-mono)" font-size="7.5" fill="#0f172a">CONTROL (WO):</text>
            <text x="145" y="72" text-anchor="end" font-family="var(--font-mono)" font-size="7" font-weight="700" fill="#0284c7">READ|WRITE|RST</text>

            <rect x="10" y="86" width="145" height="24" rx="2" fill="#ffffff" stroke="#94a3b8"/>
            <text x="18" y="102" font-family="var(--font-mono)" font-size="7.5" fill="#0f172a">DATA FIFO PORT:</text>
            <text x="145" y="102" text-anchor="end" font-family="var(--font-mono)" font-size="7" fill="#64748b">In/Out Window</text>

            <rect x="10" y="116" width="145" height="24" rx="2" fill="#ffffff" stroke="#94a3b8"/>
            <text x="18" y="132" font-family="var(--font-mono)" font-size="7.5" fill="#0f172a">DMA TARGET ADDR:</text>
            <text x="145" y="132" text-anchor="end" font-family="var(--font-mono)" font-size="7" fill="#059669">0x7FFF0000</text>

            <rect x="10" y="146" width="145" height="28" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
            <text x="18" y="160" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">TRANSFER COUNT:</text>
            <text x="145" y="160" text-anchor="end" font-family="var(--font-mono)" font-size="7" font-weight="700" fill="#0284c7">4096 Bytes</text>
            <text x="82" y="172" text-anchor="middle" font-size="6.5" fill="#64748b">(Mapped via PMIO / MMIO BAR)</text>
          </g>

          <!-- Controller Internal Processing Engines -->
          <g transform="translate(195, 38)">
            <!-- Embedded CPU / Firmware -->
            <rect width="170" height="52" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
            <text x="85" y="18" text-anchor="middle" font-size="8" font-weight="700" fill="#334155">EMBEDDED PROCESSOR</text>
            <text x="85" y="32" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0284c7">ARM Cortex-R / RISC-V Core</text>
            <text x="85" y="44" text-anchor="middle" font-size="7" fill="#64748b">Runs controller firmware / FTL</text>

            <!-- On-Board SRAM/DRAM Buffer -->
            <rect y="60" width="170" height="56" rx="4" fill="#f0fdf4" stroke="#16a34a"/>
            <text x="85" y="78" text-anchor="middle" font-size="8" font-weight="700" fill="#166534">ON-BOARD RAM BUFFER (FIFO)</text>
            <text x="85" y="92" text-anchor="middle" font-size="7" fill="#15803d">&bull; Absorbs mechanical jitter &amp; bursts</text>
            <text x="85" y="104" text-anchor="middle" font-size="7" fill="#15803d">&bull; Speed matching: Bus &harr; Device</text>

            <!-- SerDes & Hardware ECC/LDPC -->
            <rect y="124" width="170" height="56" rx="4" fill="#fef2f2" stroke="#dc2626"/>
            <text x="85" y="142" text-anchor="middle" font-size="8" font-weight="700" fill="#991b1b">ECC &amp; SERDES PHY ENGINE</text>
            <text x="85" y="156" text-anchor="middle" font-size="7" fill="#7f1d1d">&bull; LDPC error correction engine</text>
            <text x="85" y="168" text-anchor="middle" font-size="7" fill="#7f1d1d">&bull; Serial-to-parallel bit converter</text>
          </g>
        </g>

        <!-- PHY to Device Arrow -->
        <line x1="560" y1="140" x2="590" y2="140" stroke="#059669" stroke-width="2" marker-end="url(#dc2-arr-green)"/>

        <!-- Physical Peripheral Device Domain (Right) -->
        <g transform="translate(595, 20)">
          <rect width="150" height="240" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="75" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0f172a">RAW PERIPHERAL</text>
          <text x="75" y="38" text-anchor="middle" font-size="7" fill="#64748b">(Mechanical / Physical)</text>

          <rect x="10" y="52" width="130" height="52" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="75" y="70" text-anchor="middle" font-size="7.5" font-weight="700" fill="#334155">TRANSDUCERS</text>
          <text x="75" y="84" text-anchor="middle" font-size="7" fill="#64748b">Platter read heads</text>
          <text x="75" y="96" text-anchor="middle" font-size="7" fill="#64748b">Optocouplers, photodetectors</text>

          <rect x="10" y="112" width="130" height="52" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="75" y="130" text-anchor="middle" font-size="7.5" font-weight="700" fill="#334155">RAW SERIAL MEDIA</text>
          <text x="75" y="144" text-anchor="middle" font-size="7" fill="#64748b">Analog voltage flux lines</text>
          <text x="75" y="156" text-anchor="middle" font-size="7" fill="#64748b">Unframed serial bitstream</text>

          <rect x="10" y="172" width="130" height="56" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="75" y="190" text-anchor="middle" font-size="7.5" font-weight="700" fill="#dc2626">ELECTROMECHANICAL</text>
          <text x="75" y="204" text-anchor="middle" font-size="7" fill="#7f1d1d">Voice-coil arm motors</text>
          <text x="75" y="216" text-anchor="middle" font-size="7" fill="#7f1d1d">Spindle motor tachometers</text>
        </g>
      </svg>
    </div>

    <h4>Internal Architecture of the Device Controller</h4>
    <p>
      An enterprise device controller is essentially a self-contained embedded computer dedicated to managing peripheral physics. Its internal layout incorporates four key subsystems:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <!-- Embedded Microcontroller Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--accent); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">1. Embedded Processor &amp; Firmware</h4>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Controllers contain multi-core embedded processors (typically ARM Cortex-R real-time cores or RISC-V cores) running dedicated proprietary firmware.
          <br><br>
          <em>Key Responsibilities:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li><strong>Solid-State Drives (SSDs):</strong> Executes the <strong>Flash Translation Layer (FTL)</strong>, translating logical block addresses (LBAs) to physical NAND flash dies, managing wear-leveling algorithms, and running garbage collection.</li>
            <li><strong>Mechanical Drives (HDDs):</strong> Computes servo acceleration curves for the voice-coil actuator arm and tracks thermal expansion head calibration.</li>
            <li><strong>Network Controllers (NICs):</strong> Parses packet headers, computes TCP/UDP checksum offloads, and classifies flows across receive-side scaling (RSS) hardware queues.</li>
          </ul>
        </p>
      </div>

      <!-- Elastic RAM Buffers Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">2. On-Board Elastic RAM Buffers (FIFO)</h4>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Peripherals operate under strict physical timing constraints: once a rotating disk platter passes underneath a read head, data bits must be captured instantaneously or they are lost until the next revolution.
          <br><br>
          <em>Why Elastic Buffering is Mandatory:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li><strong>Speed Matching:</strong> Bridges the mismatch between high-speed burst bus transfers (PCIe at 32 GB/s) and slower, fluctuating peripheral media rates.</li>
            <li><strong>Preventing Overrun/Underrun Errors:</strong> If the host PCIe bus is momentarily congested with graphics traffic, incoming network packets or disk sectors are buffered safely in on-controller SRAM/DRAM without data loss.</li>
            <li><strong>Transactional Integrity:</strong> Data is not presented to the OS until an entire block or packet is buffered and verified.</li>
          </ul>
        </p>
      </div>

      <!-- SerDes and PHY Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--warning); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">3. The SerDes &amp; PHY Layer</h4>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Internal computer buses are wide, parallel channels (64-bit or 128-bit data buses). In contrast, high-speed physical cables (SATA, SAS, PCIe lanes, Ethernet) are serial differential links to prevent electromagnetic interference and clock skew.
          <br><br>
          <em>Role of the Serializer/Deserializer (SerDes):</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>Deserializes raw high-frequency serial pulses into parallel 32-bit or 64-bit words for the controller bus.</li>
            <li>Uses <strong>Phase-Locked Loops (PLLs)</strong> to extract and synchronize clock signals directly from the incoming data transitions (clock recovery).</li>
            <li>Performs physical line code decoding (e.g. 8b/10b, 64b/66b, or 128b/130b encoding) to maintain DC balance on copper traces.</li>
          </ul>
        </p>
      </div>

      <!-- Hardware ECC & LDPC Engine -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--danger); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">4. Error Detection &amp; Correction (ECC)</h4>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Physical transmission media are inherently noisy and imperfect. Platter magnetic domains degrade over time, and NAND flash memory gates leak charge.
          <br><br>
          <em>Autonomous Hardware Error Correction:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>Controllers append <strong>Error-Correcting Code (ECC)</strong> symbols (such as Reed-Solomon or <strong>Low-Density Parity-Check / LDPC</strong> matrices) to every block written.</li>
            <li>Upon read, the controller's dedicated hardware math engine evaluates parity syndrome equations.</li>
            <li>If bit errors occur, the hardware <strong>corrects the flipped bits in real-time</strong> inside the FIFO buffer. The operating system is completely shielded from hardware noise unless the error exceeds the unrecoverable ECC threshold.</li>
          </ul>
        </p>
      </div>
    </div>

    <h4>The Four Canonical Hardware Register Types</h4>
    <p>
      Software device drivers communicate with controllers by reading and writing four primary functional classes of hardware registers:
    </p>
    <div style="overflow-x: auto; margin: 18px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 12px; width: 22%;">Register Type</th>
            <th style="padding: 10px 12px; width: 18%;">Access Mode</th>
            <th style="padding: 10px 12px; width: 60%;">Operational Functionality</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Status Register</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); color: #0284c7;">Read-Only</td>
            <td style="padding: 10px 12px;">Reflects the controller's real-time state flags. Contains bits such as <code>BUSY</code> (controller is executing command), <code>DRQ</code> (Data Request: FIFO ready to transfer), <code>READY</code> (device is spun up and idle), and <code>ERROR</code>.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Control / Command Register</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); color: #dc2626;">Write-Only (or R/W)</td>
            <td style="padding: 10px 12px;">Accepts operational opcodes from the device driver. Writing an opcode (such as <code>CMD_SEEK</code>, <code>CMD_READ_SECTORS</code>, <code>CMD_FLUSH_CACHE</code>, or <code>ENABLE_INTERRUPTS</code>) immediately transitions the controller out of idle and kicks off physical operations.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Data In / Data Out Register</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); color: #059669;">Read / Write</td>
            <td style="padding: 10px 12px;">A memory window or I/O port providing direct access to the controller's internal FIFO buffer. In Programmed I/O (PIO), the driver reads or writes this register in a tight loop to move words between the controller buffer and host RAM.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #f0fdf4;">
            <td style="padding: 10px 12px; font-weight: 700; color: #166534;">DMA Parameter Registers</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); color: #166534;">Read / Write</td>
            <td style="padding: 10px 12px;">Configures autonomous bus mastering. Includes the <strong>Base Memory Address Register</strong> (physical 64-bit DRAM address) and the <strong>Transfer Length Register</strong> (byte count). Modern controllers accept pointers to circular submission/completion queues in host memory.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h4>The Device Driver &amp; Controller Handshake Protocol</h4>
    <p>
      When an operating system driver initiates a hardware operation, the driver and controller engage in a synchronized, hardware-level <strong>handshake sequence</strong>:
    </p>

    <pre><code><span class="syn-cmt">/* Example: Standard Driver-to-Controller Command Handshake */</span>

<span class="syn-cmt">/* 1. Driver waits until controller is not busy */</span>
<span class="syn-kw">while</span> (*reg_status &amp; STATUS_BUSY) {
    <span class="syn-cmt">/* Wait for controller to clear BUSY flag */</span>
}

<span class="syn-cmt">/* 2. Driver loads command parameters into device registers */</span>
*reg_dma_addr = target_physical_ram_address;
*reg_sector   = target_lba_sector;
*reg_count    = <span class="syn-num">8</span>; <span class="syn-cmt">/* Request 8 sectors (4096 bytes) */</span>

<span class="syn-cmt">/* 3. Driver writes operational opcode to command register (KICKS OFF HARDWARE) */</span>
*reg_command = CMD_READ_WITH_DMA;

<span class="syn-cmt">/* 4. Controller autonomously executes:
      - Sets STATUS_BUSY = 1
      - Commands mechanical heads to seek
      - Reads bits into on-board FIFO, runs ECC checks
      - Bus-masters DMA payload across PCIe directly to target_physical_ram_address
      - Clears STATUS_BUSY = 0
      - Asserts electrical interrupt line (or fires MSI-X message to APIC)
*/</span>

<span class="syn-cmt">/* 5. CPU receives interrupt, invokes Driver ISR to verify completion */</span>
<span class="syn-kw">if</span> (*reg_status &amp; STATUS_ERROR) {
    <span class="syn-cmt">/* Read controller error details */</span>
    <span class="syn-kw">uint32_t</span> err = *reg_error;
    <span class="syn-fn">log_device_fault</span>(err);
} <span class="syn-kw">else</span> {
    <span class="syn-fn">notify_io_completion</span>(request_token); <span class="syn-cmt">/* Wake sleeping user thread */</span>
}</code></pre>"""

def update_section_two():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>2. Device Controllers: The Electronic Bridge</h3>"
    end_marker = "<h3>3. Communicating with Controllers: PMIO vs. MMIO</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not find Section 2 boundaries in Module 01.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_TWO + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 2 in {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 2 in Module 01 on Device Controllers and PHY interfaces\n\n"
            "Detail SerDes, FTL firmware microcontrollers, FIFO elastic buffers,\n"
            "ECC/LDPC hardware engines, and register handshaking with an SVG diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_two():
        run_git_sync()
