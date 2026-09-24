#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 1 of 03-disk-hardware-scheduling.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "03-disk-hardware-scheduling.html"
)

EXPANDED_SECTION_ONE = r"""    <h3>1. Physical Disk Geometry: Platters, Cylinders, and Sectors</h3>
    <p>
      For over half a century, the <strong>magnetic hard disk drive (HDD)</strong> served as the primary secondary storage substrate in computing. Although solid-state flash drives (SSDs) have surpassed magnetic disks in random transaction performance, mechanical disk drives remain the dominant medium for massive, exabyte-scale datacenter storage due to their favorable cost-per-terabyte profile.
    </p>
    <p>
      From an operating system engineering perspective, magnetic disks provide a textbook case study in <strong>mechanical latency modeling, asymmetric access costs, and physical resource scheduling</strong>. To write efficient filesystem and buffer cache algorithms, kernel developers must understand the microscopic electro-mechanical physics governing disk hardware.
    </p>

    <!-- Structural Diagram: Comprehensive Physical Disk Anatomy -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 2.1: Electro-Mechanical Organization of a Modern Magnetic Hard Drive</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">Platter stacking, aerodynamic slider flying height, embedded servo sectors, and Zoned Bit Recording (ZBR).</div>

      <svg viewBox="0 0 760 300" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="dg-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="dg-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
        </defs>

        <!-- Left: Platter Stack (Isometric 3D Projection) -->
        <g transform="translate(145, 140)">
          <!-- Central Spindle -->
          <line x1="0" y1="-105" x2="0" y2="105" stroke="#334155" stroke-width="8"/>
          <text x="0" y="125" text-anchor="middle" font-size="8.5" font-weight="700" fill="#0f172a">FLUID BEARING SPINDLE</text>
          <text x="0" y="137" text-anchor="middle" font-size="7.5" fill="#64748b">Constant Angular Velocity (7200 RPM)</text>

          <!-- Platter 3 (Top Surface) -->
          <g transform="translate(0, -65)">
            <ellipse cx="0" cy="0" rx="115" ry="36" fill="#f8fafc" stroke="#0284c7" stroke-width="2"/>
            <!-- Outer Track (ZBR High Density) -->
            <ellipse cx="0" cy="0" rx="100" ry="31" fill="none" stroke="#0284c7" stroke-width="1.5"/>
            <!-- Mid Track -->
            <ellipse cx="0" cy="0" rx="70" ry="22" fill="none" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4 3"/>
            <!-- Inner Track (ZBR Low Density) -->
            <ellipse cx="0" cy="0" rx="40" ry="12" fill="none" stroke="#dc2626" stroke-width="1.5"/>
            <!-- Spindle Center Hole -->
            <ellipse cx="0" cy="0" rx="14" ry="4" fill="#475569"/>

            <!-- Sector Arc Slice -->
            <path d="M 0 0 L 95 18 A 100 31 0 0 0 100 0 Z" fill="#bae6fd" opacity="0.6"/>
            <text x="75" y="16" font-family="var(--font-mono)" font-size="6.5" font-weight="700" fill="#0369a1">Sector</text>
          </g>

          <!-- Platter 2 (Middle) -->
          <g transform="translate(0, 0)">
            <ellipse cx="0" cy="0" rx="115" ry="36" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5" opacity="0.9"/>
            <ellipse cx="0" cy="0" rx="70" ry="22" fill="none" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4 3"/>
            <ellipse cx="0" cy="0" rx="14" ry="4" fill="#475569"/>
          </g>

          <!-- Platter 1 (Bottom) -->
          <g transform="translate(0, 65)">
            <ellipse cx="0" cy="0" rx="115" ry="36" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5" opacity="0.8"/>
            <ellipse cx="0" cy="0" rx="70" ry="22" fill="none" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4 3"/>
            <ellipse cx="0" cy="0" rx="14" ry="4" fill="#475569"/>
          </g>

          <!-- Cylinder Visual Alignment (Vertical Dashed Lines) -->
          <line x1="70" y1="-65" x2="70" y2="65" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="4 3"/>
          <line x1="-70" y1="-65" x2="-70" y2="65" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="4 3"/>
          <rect x="74" y="-12" width="68" height="24" rx="3" fill="#ffffff" stroke="#dc2626"/>
          <text x="108" y="3" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#dc2626">CYLINDER</text>
        </g>

        <!-- Center-Right: Rotary Voice-Coil Actuator Arm -->
        <g transform="translate(365, 140)">
          <!-- Actuator Pivot Base -->
          <circle cx="0" cy="0" r="22" fill="#e2e8f0" stroke="#334155" stroke-width="2"/>
          <circle cx="0" cy="0" r="8" fill="#0f172a"/>
          <text x="0" y="-30" text-anchor="middle" font-size="8" font-weight="700" fill="#334155">VOICE-COIL PIVOT</text>
          <text x="0" y="-18" text-anchor="middle" font-size="7" fill="#64748b">(Permanent Magnet + Coil)</text>

          <!-- Arm Extensions to Platters -->
          <polygon points="0,-12 0,12 -150,-67 -150,-63" fill="#64748b" opacity="0.95"/>
          <polygon points="0,-12 0,12 -150,-2 -150,2" fill="#64748b" opacity="0.95"/>
          <polygon points="0,-12 0,12 -150,63 -150,67" fill="#64748b" opacity="0.95"/>

          <!-- Magnetic Head Sliders -->
          <rect x="-156" y="-68" width="10" height="6" rx="1" fill="#dc2626"/>
          <rect x="-156" y="-3" width="10" height="6" rx="1" fill="#dc2626"/>
          <rect x="-156" y="62" width="10" height="6" rx="1" fill="#dc2626"/>

          <text x="-162" y="-76" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#dc2626">R/W HEADS</text>
          <text x="-162" y="-86" font-size="6.5" fill="#64748b">GMR / TMR Sensors</text>
        </g>

        <!-- Right Panel: Micro-Scale Physics & ZBR Breakdown -->
        <g transform="translate(500, 20)">
          <rect width="245" height="260" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
          <text x="16" y="24" font-size="9.5" font-weight="700" fill="#0f172a">AERODYNAMICS &amp; HEAD FLYING HEIGHT</text>

          <!-- Flying Height Comparison Graphic -->
          <g transform="translate(12, 36)">
            <rect width="220" height="96" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="10" y="16" font-size="7.5" font-weight="700" fill="#dc2626">THE NANOMETER CATASTROPHE:</text>

            <rect x="10" y="26" width="200" height="12" rx="2" fill="#e2e8f0"/>
            <text x="15" y="35" font-size="7" fill="#334155">Human Hair Diameter: &sim;75,000 nm</text>

            <rect x="10" y="42" width="140" height="12" rx="2" fill="#fef3c7"/>
            <text x="15" y="51" font-size="7" fill="#92400e">Dust / Smoke Particle: &sim;1,500 nm</text>

            <rect x="10" y="58" width="80" height="12" rx="2" fill="#fee2e2"/>
            <text x="15" y="67" font-size="7" fill="#991b1b">Fingerprint Smear: &sim;600 nm</text>

            <rect x="10" y="74" width="25" height="14" rx="2" fill="#dcfce7" stroke="#16a34a"/>
            <text x="40" y="84" font-family="var(--font-mono)" font-size="7" font-weight="700" fill="#166534">Head Fly Height: 5 &ndash; 10 nm!</text>
          </g>

          <!-- Zoned Bit Recording (ZBR) Metric -->
          <g transform="translate(12, 142)">
            <rect width="220" height="106" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="10" y="18" font-size="7.5" font-weight="700" fill="#0284c7">ZONED BIT RECORDING (ZBR)</text>
            <text x="10" y="34" font-size="7" fill="#475569">&bull; Outer tracks have larger circumference</text>
            <text x="10" y="46" font-size="7" fill="#475569">  (<i>C</i> = 2&pi;<i>r</i>) than inner tracks.</text>
            <text x="10" y="58" font-size="7" fill="#475569">&bull; Outer tracks hold up to <strong>2&times; more sectors</strong>.</text>
            <text x="10" y="72" font-size="7" font-weight="700" fill="#059669">Throughput Asymmetry:</text>
            <text x="10" y="86" font-family="var(--font-mono)" font-size="7" fill="#059669">Outer Zone: &sim;260 MB/s (High Speed)</text>
            <text x="10" y="98" font-family="var(--font-mono)" font-size="7" fill="#dc2626">Inner Zone: &sim;120 MB/s (Slow Speed)</text>
          </g>
        </g>
      </svg>
    </div>

    <h4>Anatomy of the Mechanical Hard Disk</h4>
    <p>
      A modern hard disk drive is an ultra-precise, hermetically sealed unit containing several key mechanical and magnetic subsystems:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <!-- Platters and Spindle -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--accent); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">1. Platters &amp; The Spindle Motor</h4>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          The storage medium consists of one or more stacked, rigid circular disks called <strong>platters</strong>, fabricated from high-strength aluminum-magnesium alloys or specialized glass-ceramic substrates.
          <br><br>
          <em>Key Structural Details:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>Both the top and bottom surfaces of each platter are coated with a sub-micron sputtered magnetic thin film (cobalt-chromium-platinum alloys) protected by an atomic-layer diamond-like carbon (DLC) wear barrier.</li>
            <li>The platters rotate together on a central <strong>spindle motor</strong> operating at a strict <strong>Constant Angular Velocity (CAV)</strong>. Enterprise servers use drives spinning at 10,000 or 15,000 RPM, while consumer storage rotates at 5,400 or 7,200 RPM.</li>
            <li>Enterprise drives replace internal air with <strong>Helium gas</strong> (which has one-seventh the density of air), dramatically reducing turbulent air drag, motor power consumption, and mechanical vibration across stacks of up to 10 platters.</li>
          </ul>
        </p>
      </div>

      <!-- Heads and Actuator -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">2. Read/Write Heads &amp; Voice-Coil Actuator</h4>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Data is sensed and recorded by microscopic electromagnetic read/write heads mounted on a shared rotary <strong>actuator arm</strong> driven by a high-speed Voice-Coil Motor (VCM).
          <br><br>
          <em>The Physics of Head Flying Height:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>The heads <strong>never physically touch the platter surface</strong> during operation. The rapid rotation of the platter generates an aerodynamic air cushion (an <em>air bearing</em>) that lifts the head slider, causing it to "fly" merely <strong>5 to 10 nanometers</strong> above the spinning media.</li>
            <li>For perspective, a single human hair is &sim;75,000 nm in diameter, a smoke particle is &sim;1,500 nm, and a fingerprint ridge is &sim;600 nm. If a dust particle enters the chamber, it hits the head at 120 km/h, causing a catastrophic <strong>Head Crash</strong> that scrapes off the magnetic recording layer and permanently destroys data!</li>
            <li>Modern heads use separate technologies: <strong>Tunneling Magnetoresistive (TMR)</strong> sensors for reading minute magnetic fluctuations, and inductive coils for writing.</li>
          </ul>
        </p>
      </div>
    </div>

    <h4>The Geometry Hierarchy: Tracks, Cylinders, and Sectors</h4>
    <p>
      Data recorded on platters is organized along three geometric dimensions:
    </p>
    <ul>
      <li>
        <strong>Tracks:</strong> Data is recorded along concentric circular rings called <strong>tracks</strong>. Unlike a vinyl phonograph record or an optical compact disc (which use a single continuous spiral), magnetic disk tracks are closed, discrete circles.
        <br>
        Track density is extraordinarily high, often exceeding <strong>300,000 to 500,000 Tracks Per Inch (TPI)</strong>. The width of an individual magnetic track is less than 50 nanometers!
      </li>
      <li>
        <strong>Cylinders:</strong> The actuator arm moves all read/write heads simultaneously across all platter surfaces. The collection of all tracks across every platter surface situated at the identical radial arm distance forms an imaginary geometric vertical tube called a <strong>Cylinder</strong>:
        <div class="math-callout" style="margin: 10px 0;">
          <strong>The Cylinder Optimization Principle:</strong>
          <br>
          If a file spans multiple blocks, placing those blocks on the <strong>same cylinder across different platter surfaces</strong> allows the drive to switch from reading Head 0 to Head 1, 2, or 3 via purely electronic head-selection logic (consuming less than 0.5 milliseconds) <strong>without executing any physical, mechanical voice-coil movement</strong>!
        </div>
      </li>
      <li>
        <strong>Sectors:</strong> A track is partitioned into discrete arc segments called <strong>sectors</strong>. The sector is the smallest unit of physical storage and transfer that the disk controller can read or write atomically:
        <ul>
          <li><strong>Legacy Standard (512-Byte Sectors):</strong> Historically, sectors stored exactly 512 bytes of user data.</li>
          <li><strong>Advanced Format (4Kn / 4096-Byte Sectors):</strong> Modern drives use 4 KB physical sectors. A 4096-byte sector reduces the overhead of inter-sector gaps and preambles, and significantly increases error-correction efficiency by providing larger data blocks for modern <strong>Low-Density Parity-Check (LDPC)</strong> error-correction codes.</li>
        </ul>
      </li>
    </ul>

    <h4>The Evolution of Addressing: From CHS to Logical Block Addressing (LBA)</h4>

    <h5>1. Cylinder-Head-Sector (CHS) Addressing &amp; Historical Barriers</h5>
    <p>
      In early operating systems (such as MS-DOS and early Unix on IBM PCs), the kernel had to explicitly calculate and provide the 3-dimensional physical coordinates for every disk operation:
    </p>
    <pre><code><span class="syn-cmt">/* Historical CHS Access: Read Cylinder 20, Head 2, Sector 5 */</span>
<span class="syn-kw">struct</span> chs_address {
    <span class="syn-kw">uint16_t</span> cylinder; <span class="syn-cmt">/* 0 .. 1023 (10 bits) */</span>
    <span class="syn-kw">uint8_t</span>  head;     <span class="syn-cmt">/* 0 .. 15 (4 bits)   */</span>
    <span class="syn-kw">uint8_t</span>  sector;   <span class="syn-cmt">/* 1 .. 63 (6 bits - 1-indexed!) */</span>
};</code></pre>
    <p>
      CHS addressing contained a fatal flaw: the combination of BIOS register limitations (10 bits for cylinders, 4 bits for heads, 6 bits for sectors) created the notorious <strong>504 MiB Barrier</strong>:
    </p>
    <div class="math-callout">
      $$\text{Max CHS Capacity} = 1024\text{ Cylinders} \times 16\text{ Heads} \times 63\text{ Sectors} \times 512\text{ Bytes} = \mathbf{528{,}482{,}304\text{ Bytes (504 MiB)}}$$
    </div>

    <h5>2. Zoned Bit Recording (ZBR / Zone CAV)</h5>
    <p>
      Beyond the BIOS architectural limits, CHS was destroyed by basic physics: <strong>rigid geometry is geometrically inefficient</strong>.
    </p>
    <p>
      Because a disk platter is circular, the circumference of an outer track is more than twice the circumference of an inner track:
    </p>
    <div class="math-callout">
      $$\text{Track Circumference} = 2\pi r$$
    </div>
    <p>
      Under historical CHS, every track was forced to contain the exact same number of sectors (e.g. 63 sectors per track). This meant magnetic bit transitions on outer tracks were spaced far apart, wasting massive amounts of surface area.
    </p>
    <p>
      Modern drives implement <strong>Zoned Bit Recording (ZBR)</strong>:
    </p>
    <ul>
      <li>The disk surface is grouped into 16 to 30 concentric <strong>zones</strong>.</li>
      <li>Outer zones (with larger radii) pack significantly more sectors per track (e.g. 1,200 sectors per track) than inner zones (e.g. 600 sectors per track), maintaining a uniform magnetic recording density across the entire platter.</li>
      <li><strong>Operating System Performance Consequence:</strong> Because the spindle motor rotates at a constant angular speed, <strong>outer tracks pass beneath the read/write heads faster, streaming data at more than double the throughput of inner tracks</strong> (e.g. 260 MB/s on outer tracks vs. 120 MB/s on inner tracks)! Operating system partition formatters deliberately place root filesystems and high-performance swap partitions on the outer edge of the disk.</li>
    </ul>

    <h5>3. Logical Block Addressing (LBA) &amp; Controller Virtualization</h5>
    <p>
      Because Zoned Bit Recording destroyed uniform CHS dimensions, the storage industry transitioned universally to <strong>Logical Block Addressing (LBA)</strong>:
    </p>
    <ul>
      <li>The operating system completely abandons tracking cylinders, heads, and tracks.</li>
      <li>The disk controller exposes the disk as a flat, linear array of 64-bit integer blocks:
        <pre><code>LBA 0, LBA 1, LBA 2, LBA 3, &hellip;, LBA (TotalSectors - 1)</code></pre>
      </li>
      <li>The on-board disk controller firmware maintains an internal mathematical mapping table, translating logical LBA numbers to physical zones, cylinders, heads, and physical sectors.</li>
    </ul>

    <h4>Physical Latency Mitigations: Track and Cylinder Skewing</h4>
    <p>
      To prevent catastrophic rotational latency penalties during sequential reads, disk controllers implement microscopic angular offsets known as <strong>skewing</strong>:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <!-- Track Skewing -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--accent); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Track Skewing</h4>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Suppose a sequential file spans Track 0 and Track 1. If Sector 0 on Track 1 is placed at the exact same angular position as Sector 0 on Track 0:
          <br><br>
          When the head finishes reading Track 0, it takes approximately <strong>0.8 milliseconds</strong> for the actuator arm to mechanically step to Track 1.
          <br><br>
          During those 0.8 ms, the platter spins past Sector 0! The head lands over Sector 4, forcing the disk to wait <strong>almost an entire physical revolution (8.3 ms at 7200 RPM)</strong> just to read Sector 0!
          <br><br>
          <strong>The Solution:</strong> The controller offsets (skews) Sector 0 on Track 1 by several angular positions, ensuring that exactly as the head settles onto Track 1, Sector 0 spins directly underneath it.
        </p>
      </div>

      <!-- Defect Reallocation -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--danger); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Defect Management (G-List &amp; P-List)</h4>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          No physical platter is manufactured without microscopic silicon imperfections. Controllers maintain two defect lists:
          <br><br>
          <strong>1. Primary Defect List (P-List):</strong> Populated at the factory during low-level surface scanning. Defective sectors are skipped during initial track mapping (sector slipping).
          <br><br>
          <strong>2. Grown Defect List (G-List):</strong> When a sector fails in the field due to magnetic wear, the controller marks the sector bad and transparently remaps that LBA to an unallocated <strong>spare sector</strong> reserved on an inner or outer track.
          <br><br>
          <em>OS Performance Impact:</em> While remapping preserves data integrity, reading a remapped sector requires the actuator arm to seek to the spare track and back, causing sudden anomalous latency spikes during sequential reads.
        </p>
      </div>
    </div>"""

def update_section_one():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>1. Physical Disk Geometry: Platters, Cylinders, and Sectors</h3>"
    end_marker = "<h3>2. Modeling I/O Access Latency"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 1 boundaries in Module 03.")
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
            "Expand Section 1 of Module 03 on Physical Disk Geometry & CHS/LBA\n\n"
            "Detail fluid bearings, aerodynamic slider flying heights, ZBR zoning,\n"
            "track/cylinder skewing, G-list defect reallocation, and add an SVG."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_one():
        run_git_sync()
