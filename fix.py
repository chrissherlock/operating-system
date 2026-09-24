#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 2 of 03-disk-hardware-scheduling.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "03-disk-hardware-scheduling.html"
)

EXPANDED_SECTION_TWO = r"""    <h3>2. Modeling I/O Access Latency (<i>T</i><sub>I/O</sub>)</h3>
    <p>
      To an operating system kernel, secondary storage operations are enormously expensive compared to register and cache access. Reading a block of data from main DRAM requires tens of nanoseconds, whereas reading a block from a mechanical hard disk requires <strong>millions of nanoseconds</strong>.
    </p>
    <p>
      To design effective disk scheduling algorithms and filesystem page caches, we must construct a rigorous mathematical latency model decomposed into its physical and electronic sub-components:
    </p>

    <div class="math-callout" style="text-align: center; font-size: 1.05rem;">
      <i>T</i><sub>I/O</sub> = <i>T</i><sub>seek</sub> + <i>T</i><sub>rotational</sub> + <i>T</i><sub>transfer</sub> + <i>T</i><sub>controller</sub>
    </div>

    <!-- Structural Diagram: Time-Domain Latency Timeline -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 2.2: Time-Domain Decomposition of a Random 4 KB Disk Read Operation (~10.2 ms)</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">Visualizing how mechanical arm movement and platter rotation dwarf electronic transfer time by over 500 to 1.</div>

      <svg viewBox="0 0 760 220" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <!-- Timeline Bar Base -->
        <g transform="translate(20, 40)">
          <!-- Total Timeline Bar (720px width = 10.2 ms total) -->
          <!-- Seek Phase: 6.0 ms = ~423px -->
          <rect x="0" y="20" width="423" height="42" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
          <text x="211" y="38" text-anchor="middle" font-size="8.5" font-weight="700" fill="#991b1b">SEEK TIME (T<sub>seek</sub>): 6.0 ms (58.8%)</text>
          <text x="211" y="52" text-anchor="middle" font-size="7" fill="#7f1d1d">Arm acceleration, coasting, deceleration, head settling</text>

          <!-- Rotational Phase: 4.17 ms = ~294px -->
          <rect x="423" y="20" width="294" height="42" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
          <text x="570" y="38" text-anchor="middle" font-size="8.5" font-weight="700" fill="#92400e">ROTATIONAL DELAY (T<sub>rot</sub>): 4.17 ms (40.9%)</text>
          <text x="570" y="52" text-anchor="middle" font-size="7" fill="#b45309">Waiting for sector to spin under head at 7200 RPM</text>

          <!-- Transfer Phase: 0.02 ms = ~3px (exaggerated to 3px for visibility) -->
          <rect x="717" y="20" width="3" height="42" fill="#16a34a"/>
        </g>

        <!-- Callout Annotations -->
        <g transform="translate(20, 115)">
          <rect width="720" height="85" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>

          <text x="15" y="22" font-size="8.5" font-weight="700" fill="#0f172a">THE MECHANICAL LATENCY REALITY:</text>
          <text x="15" y="40" font-size="8" fill="#334155">&bull; <strong>Mechanical Latency (Seek + Rotation):</strong> Consumes <tspan font-weight="700" fill="#dc2626">10.17 ms (99.8% of total I/O time)</tspan>.</text>
          <text x="15" y="56" font-size="8" fill="#334155">&bull; <strong>Electronic Media Transfer Time (4 KB):</strong> Consumes <tspan font-weight="700" fill="#16a34a">0.02 ms (less than 0.2% of total I/O time)</tspan>.</text>
          <text x="15" y="72" font-size="8" fill="#334155">&bull; <strong>Conclusion:</strong> Random I/O is completely bound by the physical laws of mechanical inertia and electric motor torque!</text>
        </g>
      </svg>
    </div>

    <h4>1. Seek Time (<i>T</i><sub>seek</sub>): The Voice-Coil Mechanics</h4>
    <p>
      <strong>Seek time</strong> is the physical delay required for the voice-coil actuator arm to position the read/write heads radially across the platters and align precisely over the target cylinder.
    </p>
    <p>
      An actuator movement is not an instantaneous, uniform velocity slide. The voice-coil motor must obey classical Newtonian mechanics across four distinct physical phases:
    </p>
    <ol>
      <li><strong>Acceleration Phase:</strong> Maximum electrical current is driven through the coil, creating an intense magnetic field against the permanent rare-earth magnets to accelerate the mass of the arm.</li>
      <li><strong>Coasting Phase:</strong> For long seeks across hundreds of cylinders, the arm reaches its maximum terminal velocity and coasts across the platter radius.</li>
      <li><strong>Deceleration Phase:</strong> Reverse current is applied through the voice coil, exerting braking force to bring the high-speed arm to a controlled stop over the target cylinder.</li>
      <li><strong>Head Settling Time:</strong> The heads vibrate slightly upon arrival. The closed-loop servo mechanism reads embedded magnetic servo bursts to dampen oscillations and settle the head within the target track boundary (a mechanical settling budget of <strong>0.5 to 1.5 milliseconds</strong>).</li>
    </ol>

    <div style="overflow-x: auto; margin: 18px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 12px; width: 25%;">Seek Classification</th>
            <th style="padding: 10px 12px; width: 25%;">Typical Duration</th>
            <th style="padding: 10px 12px; width: 50%;">Physical Description</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Track-to-Track Seek</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem; color: #0284c7;">0.5 &ndash; 1.5 ms</td>
            <td style="padding: 10px 12px;">Stepping between immediately adjacent cylinders (dominated entirely by settling time).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Full-Stroke Seek</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem; color: #dc2626;">15.0 &ndash; 20.0 ms</td>
            <td style="padding: 10px 12px;">Traveling across the entire radius of the disk (from innermost cylinder to outermost cylinder).</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #f0fdf4;">
            <td style="padding: 10px 12px; font-weight: 700; color: #166534;">Average Seek Time</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem; color: #166534; font-weight: 700;">4.0 &ndash; 9.0 ms</td>
            <td style="padding: 10px 12px; color: #166534;">The expected seek time between two uniformly distributed random cylinders across the disk.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="math-callout">
      <strong>Mathematical Derivation: The <sup>1</sup>&frasl;<sub>3</sub> Disk Stroke Law</strong>
      <br>
      Suppose a disk has <i>N</i> cylinders numbered continuously from 0 to <i>N</i>. If target requests are uniformly and independently distributed across all cylinders, what is the average physical seek distance traveled between two consecutive random requests located at positions <i>x</i> and <i>y</i>?
      <br><br>
      The expected distance is given by the continuous double integral over the disk radius:
      <div style="margin: 10px 0; text-align: center; font-size: 0.95rem;">
        Expected Seek Distance = <sup>1</sup>&frasl;<sub><i>N</i><sup>2</sup></sub> &int;<sub>0</sub><sup><i>N</i></sup> &int;<sub>0</sub><sup><i>N</i></sup> |<i>x</i> - <i>y</i>| <i>dx</i> <i>dy</i> = <strong><sup><i>N</i></sup>&frasl;<sub>3</sub></strong>
      </div>
      On average, a completely random seek travels <strong>one-third of the entire disk surface stroke</strong>! This statistical law allows operating system simulators to accurately estimate average random seek times as approximately one-third of the full-stroke seek duration.
    </div>

    <h4>2. Rotational Latency (<i>T</i><sub>rotational</sub>): Platter RPM Physics</h4>
    <p>
      Once the voice-coil arm settles precisely over the target cylinder, the read head cannot immediately begin reading data. The target sector may currently be on the opposite side of the rotating platter. The time required for the target sector to rotate underneath the read head is the <strong>Rotational Latency</strong>.
    </p>
    <p>
      Because disk platters rotate at a strict <strong>Constant Angular Velocity (CAV)</strong> measured in Revolutions Per Minute (RPM), the period of one complete physical revolution (<i>T</i><sub>rev</sub>) is constant:
    </p>

    <div class="math-callout" style="text-align: center; font-size: 0.95rem;">
      <i>T</i><sub>rev</sub> = ( <sup>60</sup>&frasl;<sub>RPM</sub> ) &times; 1000 ms
    </div>

    <p>
      Assuming random access, the target sector may arrive immediately beneath the head (best case: 0 ms), or it may have just passed the head by a fraction of a millimeter (worst case: one full physical revolution, <i>T</i><sub>rev</sub>).
      <br>
      Under a uniform distribution, the <strong>Average Rotational Latency (<i>T</i><sub>rot (avg)</sub>)</strong> is exactly half a revolution:
    </p>

    <div class="math-callout" style="text-align: center; font-size: 0.95rem;">
      <i>T</i><sub>rot (avg)</sub> = <sup>1</sup>&frasl;<sub>2</sub> &times; <i>T</i><sub>rev</sub> = ( <sup>30</sup>&frasl;<sub>RPM</sub> ) &times; 1000 ms
    </div>

    <div style="overflow-x: auto; margin: 18px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 12px; width: 25%;">Spindle Speed (RPM)</th>
            <th style="padding: 10px 12px; width: 25%;">Full Revolution Period</th>
            <th style="padding: 10px 12px; width: 25%;">Average Rotational Latency</th>
            <th style="padding: 10px 12px; width: 25%;">Target Market Segment</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">5,400 RPM</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">11.11 ms</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem; color: #dc2626;">5.56 ms</td>
            <td style="padding: 10px 12px;">Consumer laptops, low-power NAS archives</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">7,200 RPM</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">8.33 ms</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem; color: #d97706;">4.17 ms</td>
            <td style="padding: 10px 12px;">Standard desktop storage, datacenter bulk arrays</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">10,000 RPM</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">6.00 ms</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem; color: #0284c7;">3.00 ms</td>
            <td style="padding: 10px 12px;">Enterprise mission-critical database storage</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #f0fdf4;">
            <td style="padding: 10px 12px; font-weight: 700; color: #166534;">15,000 RPM</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">4.00 ms</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem; color: #166534; font-weight: 700;">2.00 ms</td>
            <td style="padding: 10px 12px; color: #166534;">High-performance SAS enterprise drives</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h4>3. Transfer Time (<i>T</i><sub>transfer</sub>) &amp; Controller Overhead</h4>
    <p>
      Once the head settles over the cylinder and the target sector rotates underneath, the drive enters the <strong>Transfer Phase</strong>.
    </p>
    <ul>
      <li>
        <strong>Media Transfer Time:</strong> The time required for the sector's magnetic bits to sweep past the TMR sensor:
        <div class="math-callout" style="text-align: center;">
          <i>T</i><sub>transfer</sub> = <sup>Transfer Size (Bytes)</sup>&frasl;<sub>Internal Track Media Transfer Rate (Bytes/sec)</sub>
        </div>
        For a standard 4 KB (4,096 bytes) block read on an outer track streaming at 200 MB/s:
        <div style="margin: 6px 0; text-align: center; font-family: var(--font-mono); font-size: 0.85rem; color: #059669;">
          <i>T</i><sub>transfer</sub> = <sup>4,096 Bytes</sup>&frasl;<sub>200,000,000 Bytes/sec</sub> &asymp; <strong>0.0000205 seconds = 0.02 ms</strong>
        </div>
      </li>
      <li>
        <strong>Controller Overhead (<i>T</i><sub>controller</sub>):</strong> The electronic setup time required for the controller's ASIC to decode commands, program DMA registers, verify ECC checksums, and trigger host interrupts (typically <strong>&lt; 0.02 milliseconds</strong>).
      </li>
    </ul>

    <h4>The 500&times; Asymmetry: Random vs. Sequential Performance</h4>
    <p>
      We can now calculate the catastrophic performance penalty of random I/O versus sequential streaming on a modern 7,200 RPM mechanical drive:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <!-- Random I/O Math -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--danger); border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Case 1: Random Access (4 KB Block)</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--danger); text-transform: uppercase; margin-bottom: 8px;">Physical Seek &amp; Rotation Paid on Every Block</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Every 4 KB read accesses an arbitrary, disjoint cylinder:
          <br><br>
          <i>T</i><sub>seek</sub> &asymp; 6.00 ms<br>
          <i>T</i><sub>rot</sub> &asymp; 4.17 ms<br>
          <i>T</i><sub>transfer</sub> &asymp; 0.02 ms<br>
          <strong>Total Time (<i>T</i><sub>I/O</sub>): &asymp; 10.19 ms</strong>
          <br><br>
          <span style="font-family: var(--font-mono); font-weight: 700; color: #dc2626; font-size: 0.88rem;">
            IOPS = 1 / 0.01019 s &asymp; 98 IOPS<br>
            Throughput = 98 &times; 4 KB &asymp; 0.39 MB/s!
          </span>
        </p>
      </div>

      <!-- Sequential I/O Math -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Case 2: Sequential Access (Streaming)</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--success); text-transform: uppercase; margin-bottom: 8px;">Seek &amp; Rotation Amortized to Zero</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Blocks reside contiguously along the same track:
          <br><br>
          Initial Seek + Rotation paid ONCE for the entire stream.<br>
          Subsequent blocks stream continuously as the track rotates.<br>
          Track skewing prevents rotational misses between tracks.
          <br><br>
          <span style="font-family: var(--font-mono); font-weight: 700; color: #166534; font-size: 0.88rem;">
            IOPS = Not seek-bound<br>
            Throughput = Wire Media Rate &asymp; 200.00 MB/s!
          </span>
        </p>
      </div>
    </div>

    <div class="math-callout" style="background: #fef2f2; border-left-color: #dc2626;">
      <strong style="color: #991b1b;">The Core Architectural Lesson:</strong>
      <br>
      Sequential I/O is more than <strong>500 times faster</strong> than random I/O on mechanical storage ($200\text{ MB/s}$ vs. $0.39\text{ MB/s}$).
      <br><br>
      This vast performance disparity explains why operating system kernels incorporate:
      <ul>
        <li><strong>Read-Ahead (Prefetching):</strong> Detecting sequential reads and proactively loading dozens of subsequent sectors into the page cache ahead of user requests.</li>
        <li><strong>Write Buffering &amp; Elevator Schedulers:</strong> Queueing writes in RAM to merge adjacent blocks and sort requests into sequential cylinder order before dispatching to physical hardware.</li>
      </ul>
    </div>"""

def update_section_two():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>2. Modeling I/O Access Latency"
    end_marker = "<h3>3. Disk Arm Scheduling Algorithms</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 2 boundaries in Module 03.")
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
            "Expand Section 2 in Module 03 on Modeling I/O Access Latency (T_I/O)\n\n"
            "Detail seek time derivation, rotational latency math across RPM tiers,\n"
            "transfer time formulas, the 500x random vs sequential gap, and add SVG."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_two():
        run_git_sync()
