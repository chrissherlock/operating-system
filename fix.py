#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 2 of 04-raid-architectures.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "04-raid-architectures.html"
)

EXPANDED_SECTION_TWO = r"""    <h3>2. Taxonomy of Standard RAID Levels</h3>
    <p>
      The 1988 Berkeley paper established five canonical RAID levels (RAID 1 through RAID 5). In the decades since, the storage industry codified non-redundant striping as RAID 0, introduced dual-parity RAID 6 to survive multi-terabyte rebuild failures, and developed nested topologies such as RAID 10.
    </p>
    <p>
      Each RAID level embodies a fundamentally different mathematical strategy for laying out data blocks and error-correcting codes across physical disk spindles:
    </p>

    <!-- Structural Diagram: Comprehensive RAID Topology Matrix -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 4.1: Block Allocation Mapping Across Standard RAID Architectures</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">Comparing non-redundant striping, mirroring, dedicated parity bottlenecks, rotating distributed parity, and dual P+Q fault tolerance.</div>

      <svg viewBox="0 0 760 260" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <!-- RAID 0 -->
        <g transform="translate(10, 15)">
          <rect width="135" height="230" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="67" y="22" text-anchor="middle" font-size="9" font-weight="700" fill="#0284c7">RAID 0: STRIPING</text>
          <text x="67" y="34" text-anchor="middle" font-size="7" fill="#dc2626">0 Redundancy &bull; 0 Faults</text>

          <rect x="12" y="44" width="50" height="26" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="37" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">A0</text>
          <rect x="72" y="44" width="50" height="26" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="97" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">A1</text>

          <rect x="12" y="74" width="50" height="26" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="37" y="90" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">B0</text>
          <rect x="72" y="74" width="50" height="26" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="97" y="90" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">B1</text>

          <text x="37" y="118" text-anchor="middle" font-size="7" font-weight="700" fill="#475569">Disk 0</text>
          <text x="97" y="118" text-anchor="middle" font-size="7" font-weight="700" fill="#475569">Disk 1</text>

          <rect x="10" y="132" width="115" height="42" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="67" y="148" text-anchor="middle" font-size="7" fill="#475569">Cap: N &times; C (100%)</text>
          <text x="67" y="162" text-anchor="middle" font-size="7" fill="#059669">Throughput: N &times;</text>
        </g>

        <!-- RAID 1 -->
        <g transform="translate(155, 15)">
          <rect width="135" height="230" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="67" y="22" text-anchor="middle" font-size="9" font-weight="700" fill="#059669">RAID 1: MIRROR</text>
          <text x="67" y="34" text-anchor="middle" font-size="7" fill="#166534">Tolerates 1 Fault</text>

          <rect x="12" y="44" width="50" height="26" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="37" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">A0</text>
          <rect x="72" y="44" width="50" height="26" rx="2" fill="#fef3c7" stroke="#d97706"/>
          <text x="97" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#b45309">A0 (Mir)</text>

          <rect x="12" y="74" width="50" height="26" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="37" y="90" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">B0</text>
          <rect x="72" y="74" width="50" height="26" rx="2" fill="#fef3c7" stroke="#d97706"/>
          <text x="97" y="90" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#b45309">B0 (Mir)</text>

          <text x="37" y="118" text-anchor="middle" font-size="7" font-weight="700" fill="#475569">Disk 0 (Pri)</text>
          <text x="97" y="118" text-anchor="middle" font-size="7" font-weight="700" fill="#475569">Disk 1 (Mir)</text>

          <rect x="10" y="132" width="115" height="42" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="67" y="148" text-anchor="middle" font-size="7" fill="#dc2626">Cap: 50% (High Cost)</text>
          <text x="67" y="162" text-anchor="middle" font-size="7" fill="#059669">Read: 2 &times; IOPS</text>
        </g>

        <!-- RAID 4 -->
        <g transform="translate(300, 15)">
          <rect width="145" height="230" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="72" y="22" text-anchor="middle" font-size="9" font-weight="700" fill="#d97706">RAID 4: FIXED PARITY</text>
          <text x="72" y="34" text-anchor="middle" font-size="7" fill="#dc2626">Parity Disk Bottleneck</text>

          <rect x="8" y="44" width="38" height="26" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="27" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="7" fill="#0369a1">A0</text>
          <rect x="52" y="44" width="38" height="26" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="71" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">A1</text>
          <rect x="96" y="44" width="40" height="26" rx="2" fill="#fee2e2" stroke="#dc2626"/>
          <text x="116" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="7" font-weight="700" fill="#991b1b">Ap</text>

          <rect x="8" y="74" width="38" height="26" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="27" y="90" text-anchor="middle" font-family="var(--font-mono)" font-size="7" fill="#0369a1">B0</text>
          <rect x="52" y="74" width="38" height="26" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="71" y="90" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">B1</text>
          <rect x="96" y="74" width="40" height="26" rx="2" fill="#fee2e2" stroke="#dc2626"/>
          <text x="116" y="90" text-anchor="middle" font-family="var(--font-mono)" font-size="7" font-weight="700" fill="#991b1b">Bp</text>

          <text x="27" y="118" text-anchor="middle" font-size="6.5" font-weight="700" fill="#475569">D0</text>
          <text x="71" y="118" text-anchor="middle" font-size="6.5" font-weight="700" fill="#475569">D1</text>
          <text x="116" y="118" text-anchor="middle" font-size="6.5" font-weight="700" fill="#dc2626">Parity</text>

          <rect x="8" y="132" width="129" height="42" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="72" y="148" text-anchor="middle" font-size="7" fill="#475569">Cap: (N - 1) &times; C</text>
          <text x="72" y="162" text-anchor="middle" font-size="7" fill="#dc2626">Small writes serialize!</text>
        </g>

        <!-- RAID 5 -->
        <g transform="translate(455, 15)">
          <rect width="145" height="230" rx="6" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5"/>
          <text x="72" y="22" text-anchor="middle" font-size="9" font-weight="700" fill="#0284c7">RAID 5: ROTATING</text>
          <text x="72" y="34" text-anchor="middle" font-size="7" fill="#166534">Distributed Parity &bull; Optimal</text>

          <rect x="8" y="44" width="38" height="24" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="27" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="7" fill="#0369a1">A0</text>
          <rect x="52" y="44" width="38" height="24" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="71" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">A1</text>
          <rect x="96" y="44" width="40" height="24" rx="2" fill="#fee2e2" stroke="#dc2626"/>
          <text x="116" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="7" font-weight="700" fill="#991b1b">Ap</text>

          <rect x="8" y="72" width="38" height="24" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="27" y="88" text-anchor="middle" font-family="var(--font-mono)" font-size="7" fill="#0369a1">B0</text>
          <rect x="52" y="72" width="38" height="24" rx="2" fill="#fee2e2" stroke="#dc2626"/>
          <text x="71" y="88" text-anchor="middle" font-family="var(--font-mono)" font-size="7" font-weight="700" fill="#991b1b">Bp</text>
          <rect x="96" y="72" width="40" height="24" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="116" y="88" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">B1</text>

          <rect x="8" y="100" width="38" height="24" rx="2" fill="#fee2e2" stroke="#dc2626"/>
          <text x="27" y="116" text-anchor="middle" font-family="var(--font-mono)" font-size="7" font-weight="700" fill="#991b1b">Cp</text>
          <rect x="52" y="100" width="38" height="24" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="71" y="116" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">C0</text>
          <rect x="96" y="100" width="40" height="24" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="116" y="116" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#0369a1">C1</text>

          <rect x="8" y="132" width="129" height="42" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="72" y="148" text-anchor="middle" font-size="7" fill="#475569">Cap: (N - 1) &times; C</text>
          <text x="72" y="162" text-anchor="middle" font-size="7" fill="#059669">No Parity Bottleneck!</text>
        </g>

        <!-- RAID 6 -->
        <g transform="translate(610, 15)">
          <rect width="140" height="230" rx="6" fill="#f8fafc" stroke="#059669" stroke-width="1.5"/>
          <text x="70" y="22" text-anchor="middle" font-size="9" font-weight="700" fill="#059669">RAID 6: DUAL PAR</text>
          <text x="70" y="34" text-anchor="middle" font-size="7" fill="#166534">Tolerates 2 Faults</text>

          <rect x="8" y="44" width="28" height="24" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="22" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">A0</text>
          <rect x="40" y="44" width="28" height="24" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="54" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">A1</text>
          <rect x="72" y="44" width="28" height="24" rx="2" fill="#fee2e2" stroke="#dc2626"/>
          <text x="86" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" font-weight="700" fill="#991b1b">Ap</text>
          <rect x="104" y="44" width="28" height="24" rx="2" fill="#fef3c7" stroke="#d97706"/>
          <text x="118" y="60" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" font-weight="700" fill="#b45309">Aq</text>

          <rect x="8" y="72" width="28" height="24" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="22" y="88" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">B0</text>
          <rect x="40" y="72" width="28" height="24" rx="2" fill="#fee2e2" stroke="#dc2626"/>
          <text x="54" y="88" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" font-weight="700" fill="#991b1b">Bp</text>
          <rect x="72" y="72" width="28" height="24" rx="2" fill="#fef3c7" stroke="#d97706"/>
          <text x="86" y="88" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" font-weight="700" fill="#b45309">Bq</text>
          <rect x="104" y="72" width="28" height="24" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="118" y="88" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">B1</text>

          <rect x="8" y="100" width="28" height="24" rx="2" fill="#fee2e2" stroke="#dc2626"/>
          <text x="22" y="116" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" font-weight="700" fill="#991b1b">Cp</text>
          <rect x="40" y="100" width="28" height="24" rx="2" fill="#fef3c7" stroke="#d97706"/>
          <text x="54" y="116" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" font-weight="700" fill="#b45309">Cq</text>
          <rect x="72" y="100" width="28" height="24" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="86" y="116" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">C0</text>
          <rect x="104" y="100" width="28" height="24" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="118" y="116" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">C1</text>

          <rect x="8" y="132" width="124" height="42" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="70" y="148" text-anchor="middle" font-size="7" fill="#475569">Cap: (N - 2) &times; C</text>
          <text x="70" y="162" text-anchor="middle" font-size="7" fill="#166534">Survives URE during rebuild</text>
        </g>
      </svg>
    </div>

    <h4>1. RAID 0: Non-Redundant Block-Level Striping</h4>
    <p>
      RAID 0 partitions user data into discrete chunks (e.g. 64 KB) and stripes them across <i>N</i> physical disks in pure round-robin sequence without calculating parity or storing redundant copies:
    </p>
    <ul>
      <li><strong>Usable Capacity:</strong> <i>N</i> &times; <i>C</i> (100% capacity efficiency). Zero storage is wasted on redundancy.</li>
      <li><strong>Sequential Throughput:</strong> Scales linearly to <strong><i>N</i> &times; Single Disk Bandwidth</strong> for reads and writes.</li>
      <li><strong>Random I/O Operations (IOPS):</strong> Scales to <strong><i>N</i> &times; IOPS</strong> because independent heads seek independently.</li>
      <li>
        <strong>The Fault Tolerance Disaster:</strong> RAID 0 has <strong>zero fault tolerance</strong>. If any single drive suffers hardware failure, unrecoverable media read error, or controller seizure, <strong>all data across the entire logical volume is permanently destroyed</strong>.
        <br>
        Because drive failures are statistically independent Poisson events, the array failure rate is additive, causing array Mean Time To Failure to drop precipitously:
        <div class="math-callout" style="text-align: center;">
          MTTF<sub>RAID 0</sub> = <sup>MTTF<sub>single</sub></sup>&frasl;<sub><i>N</i></sub>
        </div>
        An array of 8 drives with an individual MTTF of 1,200,000 hours has an array MTTF of merely 150,000 hours (&asymp; 17 years). In a datacenter with 1,000 such arrays, one crashes every week!
      </li>
      <li><strong>Industrial Role:</strong> Ephemeral scratch disks, compiler build directories, GPU training caches, and video rendering swap spaces where raw speed dominates and data can be reconstructed from source.</li>
    </ul>

    <h4>2. RAID 1: Mirroring / Shadowing</h4>
    <p>
      RAID 1 guarantees reliability through pure duplication: every logical block is written simultaneously to two (or more) completely independent physical disks:
    </p>
    <ul>
      <li><strong>Usable Capacity:</strong> <i>C</i> (50% capacity efficiency for 2-way mirroring). Storage cost per usable gigabyte is doubled.</li>
      <li><strong>Write Throughput &amp; IOPS:</strong> Every write operation must be dispatched to both physical disks. Write throughput is bounded by the slowest disk in the mirror pair (1&times; speed).</li>
      <li>
        <strong>Read Optimization (Split-Head Scheduling):</strong> Because both disks hold identical data, the storage controller can schedule independent reads across both spindles in parallel:
        <div class="math-callout" style="margin: 8px 0;">
          <strong>Split-Head Seek Optimization:</strong> When an application issues a read for Sector <i>K</i>, the controller inspects the physical arm positions of both drives and dispatches the read to the head <strong>closest to the target cylinder</strong>, cutting average seek latency almost in half and achieving up to <strong>2 &times; Read IOPS</strong>!
        </div>
      </li>
      <li><strong>Fault Tolerance:</strong> Survives the total death of any one disk. If Disk 0 fails, the controller immediately switches all I/O to Disk 1 with zero downtime and zero rebuild delay.</li>
      <li><strong>Industrial Role:</strong> Operating system boot drives (EFI system partitions), database transaction log journals (WAL), and mission-critical financial ledgers.</li>
    </ul>

    <h4>3. RAID 2: Bit-Level Striping with Hamming Code ECC</h4>
    <p>
      Historically developed at UC Berkeley, RAID 2 stripes data at the <strong>individual bit level</strong> across data drives, computing error-correcting <strong>Hamming Codes</strong> recorded onto multiple dedicated parity drives:
    </p>
    <ul>
      <li>For example, in a 4-data-drive setup, 3 additional parity drives were required to implement a (7, 4) Hamming Code capable of single-bit error correction and double-bit error detection.</li>
      <li>All spindle motors had to be synchronized in lockstep rotation; all heads sought in unison.</li>
      <li>
        <strong>Why RAID 2 is Completely Obsolete:</strong>
        RAID 2 was designed under the assumption that physical disks did not provide internal error detection. Modern Integrated Drive Electronics (IDE/ATA/SCSI/SATA/SAS) controllers embed sophisticated Reed-Solomon and Low-Density Parity-Check (LDPC) error correction directly onto every sector on the platter. The drive controller itself reports whether a read sector is valid or unrecoverable. Adding external Hamming parity in software or RAID hardware is completely redundant.
      </li>
    </ul>

    <h4>4. RAID 3: Byte-Level Striping with Dedicated Parity</h4>
    <p>
      RAID 3 stripes data at the <strong>byte level</strong> across <i>N</i> - 1 data drives, storing Boolean XOR parity on a <strong>single dedicated parity disk</strong>:
    </p>
    <ul>
      <li>Like RAID 2, RAID 3 requires synchronized spindles rotating in strict lockstep.</li>
      <li>Every read or write access touches every single drive in the array simultaneously.</li>
      <li><strong>The Bottleneck:</strong> While RAID 3 achieves massive transfer rates for a single sequential stream (e.g. historical uncompressed satellite imagery or video editing), it cannot service multiple I/O requests concurrently. The entire array delivers the random IOPS of <strong>exactly one single drive</strong> (Random IOPS &asymp; 1&times;).</li>
      <li>Obsoleted by block-level striping architectures (RAID 5).</li>
    </ul>

    <h4>5. RAID 4: Block-Level Striping with Dedicated Parity Disk</h4>
    <p>
      RAID 4 advances beyond RAID 3 by striping data in coarse <strong>blocks</strong> (e.g. 64 KB) across <i>N</i> - 1 data disks, allowing independent reads to execute concurrently. Redundancy is provided by writing computed XOR parity to a <strong>single dedicated parity disk</strong>.
    </p>
    <p>
      While independent reads scale to (<i>N</i> - 1) &times; IOPS, RAID 4 introduces an infamous architectural bottleneck during write operations:
    </p>

    <div class="math-callout" style="background: #fef2f2; border-left-color: #dc2626;">
      <strong style="color: #991b1b;">The Small-Write Parity Disk Bottleneck (The 4&times; Read-Modify-Write Penalty)</strong>
      <br>
      Suppose an application updates a single 4 KB block on Disk 1 (transforming <i>D</i><sub>1 (old)</sub> into <i>D</i><sub>1 (new)</sub>).
      <br>
      The controller could recalculate parity by reading all other data disks (<i>D</i><sub>0</sub>, <i>D</i><sub>2</sub>, <i>D</i><sub>3</sub>) and computing the full stripe XOR sum. However, reading every disk in the array for a single block write is disastrously slow.
      <br><br>
      Instead, the controller calculates the new parity using the <strong>algebraic XOR difference</strong>:
      <div style="margin: 8px 0; font-family: var(--font-mono); font-size: 0.88rem; color: #0f172a; text-align: center;">
        <i>P</i><sub>new</sub> = ( <i>D</i><sub>1 (old)</sub> &oplus; <i>D</i><sub>1 (new)</sub> ) &oplus; <i>P</i><sub>old</sub>
      </div>
      To execute this single-block write, the RAID controller must perform <strong>four distinct physical I/O operations (the Read-Modify-Write cycle)</strong>:
      <ol style="margin: 6px 0 0 16px; padding: 0; font-size: 0.82rem;">
        <li><strong>Read</strong> old data block <i>D</i><sub>1 (old)</sub> from Disk 1.</li>
        <li><strong>Read</strong> old parity block <i>P</i><sub>old</sub> from the Dedicated Parity Disk.</li>
        <li><strong>Calculate</strong> new parity in memory: <i>P</i><sub>new</sub> = (<i>D</i><sub>1 (old)</sub> &oplus; <i>D</i><sub>1 (new)</sub>) &oplus; <i>P</i><sub>old</sub>.</li>
        <li><strong>Write</strong> new data block <i>D</i><sub>1 (new)</sub> to Disk 1.</li>
        <li><strong>Write</strong> new parity block <i>P</i><sub>new</sub> to the Dedicated Parity Disk.</li>
      </ol>
      <strong>The Fatal Consequence:</strong>
      Every single write in the entire storage subsystem&mdash;regardless of which data disk is updated&mdash;<strong>must read and write the single dedicated parity disk</strong>. The parity disk arm thrashes continuously, capping the entire array's write throughput at <sup>1</sup>&frasl;<sub>2</sub> the write speed of a single physical disk!
    </div>

    <h4>6. RAID 5: Block-Level Striping with Distributed Rotating Parity</h4>
    <p>
      RAID 5 eliminates the dedicated parity bottleneck by <strong>distributing and rotating parity blocks uniformly across all physical disks</strong> in a round-robin cycle:
    </p>
    <ul>
      <li>In Stripe 0, Parity resides on Disk 3 (<i>A</i><sub>p</sub> = <i>A</i><sub>0</sub> &oplus; <i>A</i><sub>1</sub> &oplus; <i>A</i><sub>2</sub>).</li>
      <li>In Stripe 1, Parity rotates to Disk 2 (<i>B</i><sub>p</sub> = <i>B</i><sub>0</sub> &oplus; <i>B</i><sub>1</sub> &oplus; <i>B</i><sub>2</sub>).</li>
      <li>In Stripe 2, Parity rotates to Disk 1 (<i>C</i><sub>p</sub> = <i>C</i><sub>0</sub> &oplus; <i>C</i><sub>1</sub> &oplus; <i>C</i><sub>2</sub>).</li>
      <li>In Stripe 3, Parity rotates to Disk 0 (<i>D</i><sub>p</sub> = <i>D</i><sub>0</sub> &oplus; <i>D</i><sub>1</sub> &oplus; <i>D</i><sub>2</sub>).</li>
    </ul>

    <h5>The Performance Breakthrough of Distributed Parity</h5>
    <p>
      Because parity blocks are distributed across all spindles, <strong>multiple independent small writes can execute simultaneously in parallel</strong>, provided they access different stripes. The single-disk parity bottleneck is permanently broken!
    </p>
    <ul>
      <li><strong>Usable Capacity:</strong> (<i>N</i> - 1) &times; <i>C</i>. Parity consumes exactly one disk's worth of total capacity across the array (e.g. 87.5% usable on an 8-disk array).</li>
      <li><strong>Read Performance:</strong> Scales to <strong><i>N</i> &times; IOPS</strong> and (<i>N</i> - 1) &times; sequential bandwidth.</li>
      <li>
        <strong>Write Performance Profiles:</strong>
        <ul>
          <li><strong>Large Full-Stripe Writes (Optimal):</strong> If an application writes a full stripe (e.g. updating <i>A</i><sub>0</sub>, <i>A</i><sub>1</sub>, and <i>A</i><sub>2</sub> simultaneously), the controller does not execute the Read-Modify-Write cycle! It computes <i>A</i><sub>p</sub> = <i>A</i><sub>0</sub> &oplus; <i>A</i><sub>1</sub> &oplus; <i>A</i><sub>2</sub> directly in memory and writes all blocks to all disks in a single parallel burst.</li>
          <li><strong>Small Random Writes (RMW Penalty):</strong> Single-block updates still incur the 4&times; Read-Modify-Write penalty (2 reads + 2 writes), but the operations are balanced evenly across all spindles.</li>
        </ul>
      </li>
      <li><strong>Fault Tolerance:</strong> Survives the physical loss of <strong>exactly one drive</strong>.</li>
    </ul>

    <h4>7. RAID 6: Dual Distributed Parity (P + Q Parity)</h4>
    <p>
      As physical hard drive capacities expanded from gigabytes to multi-terabytes (10 TB &ndash; 24 TB), RAID 5 became highly dangerous due to the <strong>Unrecoverable Read Error (URE) crisis</strong> during multi-day rebuilds.
    </p>
    <p>
      To provide enterprise reliability, <strong>RAID 6 computes two completely independent parity blocks per stripe</strong> (labeled <i>P</i> and <i>Q</i>) and distributes both across all disks:
    </p>
    <ul>
      <li>
        <strong>Parity P (Linear XOR Code):</strong>
        Standard Boolean parity across data blocks:
        <div style="margin: 6px 0; font-family: var(--font-mono); font-size: 0.85rem; color: #0284c7; text-align: center;">
          <i>P</i> = <i>D</i><sub>0</sub> &oplus; <i>D</i><sub>1</sub> &oplus; <i>D</i><sub>2</sub> &hellip; &oplus; <i>D</i><sub><i>N</i>-3</sub>
        </div>
      </li>
      <li>
        <strong>Parity Q (Reed-Solomon Galois Field Code):</strong>
        A non-linear polynomial code computed using <strong>Galois Field arithmetic over GF(2<sup>8</sup>)</strong>:
        <div style="margin: 6px 0; font-family: var(--font-mono); font-size: 0.85rem; color: #d97706; text-align: center;">
          <i>Q</i> = ( <i>g</i><sup>0</sup> &otimes; <i>D</i><sub>0</sub> ) &oplus; ( <i>g</i><sup>1</sup> &otimes; <i>D</i><sub>1</sub> ) &oplus; &hellip; &oplus; ( <i>g</i><sup><i>N</i>-3</sup> &otimes; <i>D</i><sub><i>N</i>-3</sub> )
        </div>
        where <i>g</i> is a generator element of GF(2<sup>8</sup>) and &otimes; denotes Galois field multiplication.
      </li>
      <li><strong>Usable Capacity:</strong> (<i>N</i> - 2) &times; <i>C</i>. Two disks' worth of total capacity are dedicated to dual parity.</li>
      <li><strong>The Small-Write Penalty (6&times; I/O Penalty):</strong> A single random block write requires updating <i>D</i>, <i>P</i>, and <i>Q</i>, forcing <strong>3 physical reads and 3 physical writes (6 total I/O operations)</strong>! Modern hardware RAID cards incorporate dedicated hardware Galois Field polynomial coprocessors to offload this math.</li>
      <li>
        <strong>Fault Tolerance:</strong> Survives <strong>two simultaneous, concurrent physical drive failures</strong> without data loss. If one drive physically dies and a second drive encounters an unrecoverable bad sector during the rebuild, RAID 6 uses the <i>Q</i> polynomial equations to solve for both missing blocks simultaneously!
      </li>
    </ul>

    <h4>8. Nested RAID: RAID 10 (1+0) vs. RAID 01 (0+1)</h4>
    <p>
      Enterprise databases (such as Oracle, Microsoft SQL Server, and PostgreSQL) demand high random IOPS and zero Read-Modify-Write penalties. They deploy <strong>Nested / Hybrid RAID</strong>, combining the speed of striping (RAID 0) with the simplicity of mirroring (RAID 1):
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <!-- RAID 10 Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">RAID 10 (Stripe of Mirrors) &mdash; INDUSTRIAL STANDARD</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--success); text-transform: uppercase; margin-bottom: 8px;">RAID 1 First, Then RAID 0 on Top</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Disks are paired into mirrored sets (Sub-array 0: Disk 0/1; Sub-array 1: Disk 2/3), and user data is striped across the mirrored pairs.
          <br><br>
          <em>Rebuild Reliability Mathematics:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>Suppose Disk 0 dies. The array continues operating from Disk 1.</li>
            <li>If a second drive dies during the rebuild, the array <strong>survives as long as the second failed drive is NOT Disk 1</strong>!</li>
            <li>In an 8-disk RAID 10 array, the mathematical probability of surviving a second independent drive failure is:
              <div style="margin: 4px 0; font-family: var(--font-mono); font-weight: 700; color: #166534;">
                P(Survival) = (<i>N</i> - 2) / (<i>N</i> - 1) = 6 / 7 &asymp; 85.7%!
              </div>
            </li>
          </ul>
        </p>
      </div>

      <!-- RAID 01 Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--danger); border-radius: 6px; padding: 16px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.95rem;">RAID 01 (Mirror of Stripes) &mdash; HAZARDOUS ARCHITECTURE</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--danger); text-transform: uppercase; margin-bottom: 8px;">RAID 0 First, Then RAID 1 on Top</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Disks are grouped into two large striped sets (Stripe A: Disks 0, 1; Stripe B: Disks 2, 3), and the two stripes are mirrored.
          <br><br>
          <em>The Rebuild Vulnerability Trap:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>If Disk 0 dies, the <strong>entire Stripe A sub-array collapses</strong> and becomes inoperative.</li>
            <li>The entire logical volume is now surviving on a single striped array (Stripe B).</li>
            <li><strong>Any secondary drive failure on ANY disk in Stripe B destroys the entire storage volume</strong>!</li>
            <li>Probability of surviving a second failure:
              <div style="margin: 4px 0; font-family: var(--font-mono); font-weight: 700; color: #dc2626;">
                P(Survival) = 0%! (Guaranteed Collapse)
              </div>
            </li>
          </ul>
        </p>
      </div>
    </div>

    <h4>Comprehensive RAID Level Synthesis Matrix</h4>
    <div style="overflow-x: auto; margin: 18px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.86rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 10px; width: 12%;">RAID Level</th>
            <th style="padding: 10px 10px; width: 15%;">Usable Capacity</th>
            <th style="padding: 10px 10px; width: 11%;">Min Disks</th>
            <th style="padding: 10px 10px; width: 15%;">Fault Tolerance</th>
            <th style="padding: 10px 10px; width: 15%;">Small-Write Penalty</th>
            <th style="padding: 10px 10px; width: 32%;">Primary Industrial Use Case</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 10px; font-weight: 700;">RAID 0</td>
            <td style="padding: 10px 10px; font-family: var(--font-mono); color: #0284c7;"><i>N</i> &times; <i>C</i> (100%)</td>
            <td style="padding: 10px 10px; font-family: var(--font-mono);">2</td>
            <td style="padding: 10px 10px; color: #dc2626; font-weight: 700;">0 Disks</td>
            <td style="padding: 10px 10px; font-family: var(--font-mono); color: #059669;">1&times; (0 Penalty)</td>
            <td style="padding: 10px 10px;">Ephemeral high-speed scratchpad, swap space, GPU caches.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 10px; font-weight: 700;">RAID 1</td>
            <td style="padding: 10px 10px; font-family: var(--font-mono); color: #dc2626;"><i>C</i> (50%)</td>
            <td style="padding: 10px 10px; font-family: var(--font-mono);">2</td>
            <td style="padding: 10px 10px; color: #166534; font-weight: 700;">1 Disk</td>
            <td style="padding: 10px 10px; font-family: var(--font-mono);">2&times; Writes</td>
            <td style="padding: 10px 10px;">OS boot volumes, transaction logs, mission-critical systems.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 10px; font-weight: 700;">RAID 4</td>
            <td style="padding: 10px 10px; font-family: var(--font-mono); color: #059669;">(<i>N</i> - 1) &times; <i>C</i></td>
            <td style="padding: 10px 10px; font-family: var(--font-mono);">3</td>
            <td style="padding: 10px 10px; color: #166534;">1 Disk</td>
            <td style="padding: 10px 10px; color: #dc2626; font-weight: 700;">4&times; (Parity Bottleneck)</td>
            <td style="padding: 10px 10px;">Historical interest; NetApp WAFL NVRAM write-gathering filesystems.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #f0fdf4;">
            <td style="padding: 10px 10px; font-weight: 700; color: #166534;">RAID 5</td>
            <td style="padding: 10px 10px; font-family: var(--font-mono); color: #166534; font-weight: 700;">(<i>N</i> - 1) &times; <i>C</i></td>
            <td style="padding: 10px 10px; font-family: var(--font-mono);">3</td>
            <td style="padding: 10px 10px; color: #166534;">1 Disk</td>
            <td style="padding: 10px 10px; font-family: var(--font-mono); color: #d97706;">4&times; (RMW Cycle)</td>
            <td style="padding: 10px 10px;">General file servers, web tiers, arrays with small (&le; 2 TB) disks.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #f0fdf4;">
            <td style="padding: 10px 10px; font-weight: 700; color: #166534;">RAID 6</td>
            <td style="padding: 10px 10px; font-family: var(--font-mono); color: #166534; font-weight: 700;">(<i>N</i> - 2) &times; <i>C</i></td>
            <td style="padding: 10px 10px; font-family: var(--font-mono);">4</td>
            <td style="padding: 10px 10px; color: #166534; font-weight: 700;">2 Disks (Dual Parity)</td>
            <td style="padding: 10px 10px; font-family: var(--font-mono); color: #dc2626;">6&times; (P+Q Cycle)</td>
            <td style="padding: 10px 10px;">Enterprise storage arrays with multi-terabyte SATA/SAS drives.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 10px; font-weight: 700;">RAID 10</td>
            <td style="padding: 10px 10px; font-family: var(--font-mono); color: #dc2626;">(<i>N</i> / 2) &times; <i>C</i> (50%)</td>
            <td style="padding: 10px 10px; font-family: var(--font-mono);">4</td>
            <td style="padding: 10px 10px; color: #166534; font-weight: 700;">1 to <i>N</i>/2 Disks</td>
            <td style="padding: 10px 10px; font-family: var(--font-mono); color: #059669;">2&times; (Zero Parity RMW)</td>
            <td style="padding: 10px 10px;">High-concurrency relational databases (Oracle, PostgreSQL, SQL Server).</td>
          </tr>
        </tbody>
      </table>
    </div>"""

def update_section_two():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>2. Taxonomy of Standard RAID Levels</h3>"
    end_marker = "<h3>3. Mathematical Foundations: XOR Parity &amp; The URE Rebuild Crisis</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 2 boundaries in Module 04.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_TWO + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 2 in {TARGET_FILE}")
    return True

def run_git_sync():
    status = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
    if not status:
        print("--> Working tree is clean. Nothing to commit.")
        return

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 2 in Module 04 on Standard and Nested RAID Taxonomy\n\n"
            "Detail RAID 0-6 and RAID 10 vs 01, RMW penalty math, Galois field P+Q\n"
            "parity, rebuild survival probabilities, and update the layout matrix."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_two():
        run_git_sync()
