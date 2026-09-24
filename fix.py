#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 4 of 04-raid-architectures.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "04-raid-architectures.html"
)

EXPANDED_SECTION_FOUR = r"""    <h3>4. Software RAID vs. Hardware RAID &amp; Modern Filesystems</h3>
    <p>
      Implementing multi-disk redundancy requires deciding where the RAID logic executes in the computer hierarchy. Historically, this divided storage engineering into two camps: dedicated <strong>Hardware RAID Controllers</strong> versus operating system <strong>Software RAID</strong>.
    </p>
    <p>
      However, modern multi-core processors, PCIe NVMe storage, and advanced <strong>Copy-on-Write (CoW) filesystems</strong> have rendered traditional block-level RAID architectures obsolete, replacing rigid array logic with integrated, self-healing volume managers.
    </p>

    <!-- Structural Diagram: Hardware RAID vs Modern CoW Filesystems -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 4.3: The Architectural Shift &mdash; Traditional Block RAID vs. Self-Healing Copy-on-Write (ZFS / Btrfs)</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">Contrasting the uncoordinated block-level Write Hole with atomic tree updates and parent-pointer checksum validation.</div>

      <svg viewBox="0 0 760 280" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="cow-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="cow-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
          <marker id="cow-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
        </defs>

        <!-- Left: Traditional Block-Level RAID Architecture & Write Hole -->
        <g transform="translate(15, 20)">
          <rect width="345" height="240" rx="8" fill="#f8fafc" stroke="#dc2626" stroke-width="1.5"/>
          <text x="172" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="#991b1b">TRADITIONAL BLOCK-LEVEL RAID</text>
          <text x="172" y="38" text-anchor="middle" font-size="7.5" fill="#dc2626">Rigid In-Place Overwrites &bull; The Write Hole Vulnerability</text>

          <!-- Layer 1: Filesystem (Blind) -->
          <rect x="20" y="50" width="305" height="34" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="30" y="66" font-size="8" font-weight="700" fill="#334155">FILESYSTEM (ext4 / NTFS / XFS)</text>
          <text x="30" y="78" font-size="7" fill="#64748b">Completely blind to underlying multi-disk topology</text>

          <line x1="172" y1="84" x2="172" y2="100" stroke="#dc2626" stroke-width="1.5" marker-end="url(#cow-arr-red)"/>

          <!-- Layer 2: Hardware Controller / md Driver -->
          <rect x="20" y="102" width="305" height="42" rx="4" fill="#fee2e2" stroke="#dc2626"/>
          <text x="30" y="118" font-size="8" font-weight="700" fill="#991b1b">RAID ENGINE (Block Virtualization)</text>
          <text x="30" y="132" font-size="7" fill="#7f1d1d">Maps logical LBAs &rarr; Striped member physical disks</text>

          <!-- Layer 3: The Write Hole Incident -->
          <g transform="translate(20, 154)">
            <rect width="305" height="66" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="10" y="16" font-size="7.5" font-weight="700" fill="#dc2626">POWER FAILURE MID-UPDATE:</text>
            <text x="10" y="30" font-family="var(--font-mono)" font-size="7" fill="#334155">1. Data Block D0 written to Disk 0 &bull; <tspan font-weight="700" fill="#059669">COMMITTED</tspan></text>
            <text x="10" y="44" font-family="var(--font-mono)" font-size="7" fill="#dc2626">2. Power Dies! Parity P0 never reaches Disk 3 &bull; <tspan font-weight="700" fill="#dc2626">LOST</tspan></text>
            <text x="10" y="58" font-size="7" font-weight="700" fill="#991b1b">&times; SILENT PARITY CORRUPTION &bull; Rebuild destroys data!</text>
          </g>
        </g>

        <!-- Right: Modern Integrated CoW Architecture (ZFS / Btrfs) -->
        <g transform="translate(390, 20)">
          <rect width="355" height="240" rx="8" fill="#f8fafc" stroke="#059669" stroke-width="2"/>
          <text x="177" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="#166534">MODERN COPY-ON-WRITE (ZFS / Btrfs)</text>
          <text x="177" y="38" text-anchor="middle" font-size="7.5" fill="#166534">Integrated Volume + End-to-End Checksums</text>

          <!-- Merged File + Volume Layer -->
          <rect x="20" y="50" width="315" height="42" rx="4" fill="#dcfce7" stroke="#16a34a"/>
          <text x="30" y="66" font-size="8" font-weight="700" fill="#166534">INTEGRATED POOL (ZFS SPA / DMU)</text>
          <text x="30" y="80" font-size="7" fill="#15803d">Filesystem aware of allocation &bull; Rebuilds only active data</text>

          <line x1="177" y1="92" x2="177" y2="108" stroke="#059669" stroke-width="2" marker-end="url(#cow-arr-green)"/>

          <!-- Atomic Out-of-Place Write Tree -->
          <g transform="translate(20, 110)">
            <rect width="315" height="110" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="10" y="16" font-size="7.5" font-weight="700" fill="#0284c7">ATOMIC OUT-OF-PLACE TRANSACTION:</text>
            <text x="10" y="32" font-size="7" fill="#334155">&bull; Data and Parity written to <tspan font-weight="700" fill="#059669">NEW, unallocated blocks</tspan>.</text>
            <text x="10" y="46" font-size="7" fill="#334155">&bull; Old blocks remain untouched until transaction commits.</text>
            <text x="10" y="60" font-size="7" fill="#334155">&bull; <tspan font-weight="700" fill="#166534">Root Uberblock</tspan> swapped atomically via flush barrier.</text>

            <!-- Self-Healing Box -->
            <rect x="10" y="70" width="295" height="30" rx="3" fill="#f0fdf4" stroke="#86efac"/>
            <text x="15" y="84" font-size="7" font-weight="700" fill="#166534">&#10003; SELF-HEALING BIT ROT DETECTION:</text>
            <text x="15" y="94" font-size="6.5" fill="#15803d">Parent pointers hold SHA-256 hashes &rarr; Auto-repairs bad sectors!</text>
          </g>
        </g>
      </svg>
    </div>

    <h4>1. Hardware RAID vs. Software RAID</h4>
    <p>
      For decades, enterprise deployments strictly favored Hardware RAID. However, rapid microarchitectural advancements in CPU vector instruction sets (x86 AVX-512, ARM NEON) and PCIe NVMe interconnects fundamentally transformed the trade-off space:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <!-- Hardware RAID Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--accent); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Hardware RAID (Dedicated HBA Controller)</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--accent); text-transform: uppercase; margin-bottom: 8px;">Hardware ASIC &bull; Dedicated Battery Cache</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          A specialized PCI Express add-in card incorporating an embedded processor, hardware XOR/Galois engines, and onboard DRAM cache.
          <br><br>
          <em>Architectural Strengths:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li><strong>Zero Host CPU Overhead:</strong> Parity calculations and rebuild streams execute on the controller's internal processor.</li>
            <li><strong>OS Agnostic:</strong> Exposes a single, standard synthetic disk (e.g. <code>/dev/sda</code>). No special OS drivers required to boot.</li>
            <li><strong>BBU / Flash Cache:</strong> Incorporates a <strong>Battery-Backed Unit (BBU)</strong> or <strong>Flash-Backed Write Cache (FBWC)</strong> with supercapacitors to flush dirty cache to NAND flash during power loss.</li>
          </ul>
          <em style="color: #991b1b;">Severe Operational Weaknesses:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li><strong>Proprietary Metadata Lock-in:</strong> If the physical RAID card catches fire, member disks cannot be read by another computer unless an <em>identical model and firmware revision controller</em> is installed.</li>
            <li><strong>NVMe Saturation Bottleneck:</strong> Hardware RAID controllers top out at PCIe interface limits, forming a catastrophic bottleneck for arrays of ultra-fast PCIe Gen 5 NVMe SSDs.</li>
          </ul>
        </p>
      </div>

      <!-- Software RAID Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Software RAID (Kernel Block Driver)</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--success); text-transform: uppercase; margin-bottom: 8px;">Linux mdadm &bull; Windows Storage Spaces</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Executes directly inside the operating system kernel block layer (Linux <code>md</code> subsystem or Windows Storage Spaces), managing commodity drives attached to standard SATA/SAS/NVMe ports.
          <br><br>
          <em>Architectural Strengths:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li><strong>Extreme AVX Throughput:</strong> Host CPU SIMD units (AVX-512) execute XOR and Galois field multiplication at <strong>30 to 50 GB/s</strong>, dwarfing dedicated ASIC chips.</li>
            <li><strong>Open, Portable Metadata:</strong> Disks use open standards (Linux <code>md</code> metadata format 1.2). If a motherboard dies, drives can be plugged into any Linux machine on Earth and mounted instantly.</li>
            <li><strong>Direct NVMe Scaling:</strong> Bypasses single-controller PCIe bottlenecks, streaming directly across CPU Root Complex lanes.</li>
          </ul>
          <em style="color: #991b1b;">Operational Considerations:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>Consumes a fraction of host CPU cycles during rebuilds.</li>
            <li>Requires a dedicated write-intent bitmap or journal log to defend against the Write Hole.</li>
          </ul>
        </p>
      </div>
    </div>

    <h4>2. The RAID Write Hole Phenomenon</h4>
    <p>
      In traditional block-level RAID (RAID 4, 5, and 6), updating a single data block requires two separate, non-atomic physical write operations:
    </p>
    <ol>
      <li>Writing the updated user data block to Data Disk <i>K</i>.</li>
      <li>Writing the updated parity block to Parity Disk <i>P</i>.</li>
    </ol>
    <div class="math-callout" style="background: #fef2f2; border-left-color: #dc2626;">
      <strong style="color: #991b1b;">The Write Hole Anatomy:</strong>
      <br>
      A standard PC hardware bus cannot update two physically separate disk drives atomically in a single electrical cycle.
      <br><br>
      Suppose the server suffers a sudden power blackout, kernel panic, or hardware crash between step 1 and step 2:
      <ul>
        <li>Data Disk <i>K</i> successfully committed the new data block.</li>
        <li>Parity Disk <i>P</i> never received the new parity block before power died.</li>
      </ul>
      <strong>The Silent Corruption Disaster:</strong>
      Upon reboot, the operating system has no mechanism to detect that Parity Disk <i>P</i> is desynchronized from Data Disk <i>K</i>. The array appears healthy.
      <br>
      Months later, when a completely unrelated drive dies, the controller attempts to rebuild the lost drive by XORing all surviving drives. <strong>Because Parity <i>P</i> is desynchronized, the reconstructed data is pure garbage</strong>! The Write Hole silently corrupts user data without raising any hardware alert.
    </div>

    <h5>Classical Hardware &amp; Software Mitigations</h5>
    <ul>
      <li>
        <strong>Battery-Backed Write Caches (BBUs) / Non-Volatile RAM:</strong>
        Hardware RAID cards buffer writes in non-volatile DRAM. During a sudden power cut, an onboard lithium battery (or supercapacitor driving flash memory) keeps the cache alive. Upon reboot, the controller replays the uncommitted parity updates before presenting the logical volume to the OS.
      </li>
      <li>
        <strong>Write-Intent Bitmaps (Linux md):</strong>
        Software RAID allocates a coarse-grained bitmap where each bit represents a chunk of the array. Before initiating a write, the kernel sets the corresponding bit to <code>1</code> on disk. After data and parity commit, the bit is cleared to <code>0</code>. Upon reboot after a crash, the kernel scans the bitmap and resynchronizes only the few dirty chunks rather than scanning the entire multi-terabyte disk.
      </li>
    </ul>

    <h4>3. The Modern Paradigm: Copy-on-Write Filesystems (ZFS &amp; Btrfs)</h4>
    <p>
      The fundamental flaw of both hardware and software RAID is <strong>architectural layering isolation</strong>: the RAID controller operates at the block layer and has zero knowledge of the filesystem, while the filesystem operates above and has zero knowledge of disk parity.
    </p>
    <p>
      Modern storage architectures (championed by Sun Microsystems' <strong>ZFS</strong> and Linux <strong>Btrfs</strong>) eliminate this partition entirely by <strong>merging the volume manager and the filesystem into a single, unified engine</strong>:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <!-- Elimination of Write Hole -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--accent); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Permanent Elimination of the Write Hole</h4>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          CoW filesystems <strong>never overwrite data in-place</strong>.
          <br><br>
          When an existing file block is modified:
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>The new data block and its new parity block are written to completely <strong>new, previously unallocated physical sectors</strong>.</li>
            <li>The original data and original parity remain completely untouched on disk.</li>
            <li>Once the new blocks are fully flushed to media, the filesystem executes a single atomic pointer update (updating the <em>uberblock</em> root).</li>
            <li>If power fails at any millisecond during the write, the filesystem reboots into the previous valid tree state. <strong>The Write Hole is mathematically impossible!</strong></li>
          </ul>
        </p>
      </div>

      <!-- End to End Checksumming -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">Self-Healing Bit Rot Defense</h4>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Traditional RAID cannot detect <strong>Silent Data Corruption (Bit Rot)</strong>: if a magnetic domain flips silently, the drive returns bad data with a valid status. RAID assumes the data is good.
          <br><br>
          <em>How ZFS Solves Bit Rot:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>Every block contains a 256-bit cryptographic checksum (e.g. SHA-256 or Fletcher4) stored in its <strong>parent pointer block</strong>.</li>
            <li>When data is read, the checksum is verified against the payload.</li>
            <li>If the checksum fails, ZFS knows <em>with mathematical certainty</em> which disk is corrupt, reconstructs the valid block from parity, delivers clean data to the application, and <strong>transparently overwrites the corrupt sector on disk (Self-Healing)</strong>!</li>
          </ul>
        </p>
      </div>
    </div>

    <h4>ZFS RAID-Z vs. Traditional RAID</h4>
    <p>
      ZFS replaces traditional fixed-stripe RAID with <strong>RAID-Z</strong> (supporting RAID-Z1, RAID-Z2, and RAID-Z3 for single, double, and triple parity):
    </p>
    <ul>
      <li>
        <strong>Dynamic Stripe Width:</strong> Unlike traditional RAID 5 (which uses rigid, fixed-size 64 KB chunks), RAID-Z allocates <strong>dynamic variable-length stripes</strong> for every individual write. A small 4 KB file is written as a single data block plus a single parity block, eliminating the Read-Modify-Write cycle entirely!
      </li>
      <li>
        <strong>Intelligent Resilvering (Rebuilding Active Data Only):</strong>
        Suppose an 8-disk RAID array contains 16 TB drives, but only 2 TB of actual user data is stored on the volume:
        <ul>
          <li><strong>Traditional RAID Controller:</strong> Ignorant of filesystems, the hardware controller must blindly copy and recalculate <strong>all 16 terabytes of empty, unallocated sectors</strong>, forcing a brutal 48-hour mechanical rebuild!</li>
          <li><strong>ZFS Resilver Engine:</strong> Aware of the filesystem tree, ZFS rebuilds <strong>only the 2 TB of active, allocated user blocks</strong>, completing the replacement in a fraction of the time and drastically shrinking the window of vulnerability.</li>
        </ul>
      </li>
    </ul>"""

def update_section_four():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>4. Software RAID vs. Hardware RAID &amp; Modern Filesystems</h3>"
    end_marker = '<nav class="nav-bar" style="margin-top: 36px;'

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 4 boundaries in Module 04.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_FOUR + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 4 in {TARGET_FILE}")
    return True

def run_git_sync():
    status = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
    if not status:
        print("--> Working tree is clean. Nothing to commit.")
        return

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 4 in Module 04 on Hardware vs Software RAID and CoW\n\n"
            "Detail HBA controllers, NVRAM write holes, BBU/FBWC, Linux mdadm,\n"
            "and ZFS/Btrfs Copy-on-Write RAID-Z self-healing checksum architectures."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_four():
        run_git_sync()
