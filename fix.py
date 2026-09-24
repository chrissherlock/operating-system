#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 1 of 04-raid-architectures.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "04-raid-architectures.html"
)

EXPANDED_SECTION_ONE = r"""    <h3>1. The Three Orthogonal Design Axes &amp; Striping</h3>
    <p>
      In 1988, David Patterson, Garth Gibson, and Randy Katz published their foundational paper at the University of California, Berkeley: <em>"A Case for Redundant Arrays of Inexpensive Disks (RAID)"</em>. The paper identified a widening architectural crisis: <strong>while microprocessors were doubling in computational throughput every 18 months in accordance with Moore's Law, physical disk access times were improving by only 7% to 10% per year due to mechanical inertia</strong>.
    </p>
    <p>
      Enterprise mainframes had historically addressed this latency gap by building <strong>SLEDs (Single Large Expensive Disks)</strong>&mdash;massive, custom-engineered platters with high spindle speeds and extreme manufacturing costs. Patterson, Gibson, and Katz proposed a radical counter-strategy: replace a single expensive disk with an array of multiple, commodity, low-cost disks developed for the personal computer market.
    </p>
    <p>
      Organizing multiple independent physical drives into a single logical block storage volume requires balancing three competing, orthogonal architectural dimensions:
    </p>

    <!-- Structural Diagram: Design Axes and Striping Geometry -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 4.0: The Three Orthogonal Design Axes &amp; Striping Chunk Distribution</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">The trade-off space between Capacity, Performance, and Reliability, alongside the mathematical mapping of linear file offsets to physical disk chunks.</div>

      <svg viewBox="0 0 760 300" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="ax-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="ax-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
          <marker id="ax-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
        </defs>

        <!-- Left: The Three Orthogonal Axes Radar/Triad -->
        <g transform="translate(15, 20)">
          <rect width="260" height="260" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="130" y="24" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0f172a">THE THREE ORTHOGONAL AXES</text>

          <!-- Triangular Coordinate Framework -->
          <g transform="translate(130, 140)">
            <!-- Axis 1: Capacity (Top) -->
            <line x1="0" y1="0" x2="0" y2="-90" stroke="#0284c7" stroke-width="2" marker-end="url(#ax-arr-blue)"/>
            <text x="0" y="-98" text-anchor="middle" font-size="8" font-weight="700" fill="#0284c7">1. CAPACITY EFFICIENCY (&eta;)</text>
            <text x="0" y="-108" text-anchor="middle" font-size="6.5" fill="#64748b">Usable Space / Raw Space</text>

            <!-- Axis 2: Performance (Bottom Right) -->
            <line x1="0" y1="0" x2="78" y2="45" stroke="#059669" stroke-width="2" marker-end="url(#ax-arr-green)"/>
            <text x="90" y="55" font-size="8" font-weight="700" fill="#166534">2. PERFORMANCE</text>
            <text x="90" y="66" font-size="6.5" fill="#64748b">IOPS &bull; Throughput</text>

            <!-- Axis 3: Reliability (Bottom Left) -->
            <line x1="0" y1="0" x2="-78" y2="45" stroke="#dc2626" stroke-width="2" marker-end="url(#ax-arr-red)"/>
            <text x="-90" y="55" text-anchor="end" font-size="8" font-weight="700" fill="#991b1b">3. RELIABILITY</text>
            <text x="-90" y="66" text-anchor="end" font-size="6.5" fill="#64748b">MTTDL &bull; Fault Tolerance</text>

            <!-- Center Polygon: RAID 5 Profile -->
            <polygon points="0,-60 52,30 -52,30" fill="#bae6fd" stroke="#0284c7" stroke-width="1.5" opacity="0.6"/>
            <circle cx="0" cy="-60" r="3" fill="#0284c7"/>
            <circle cx="52" cy="30" r="3" fill="#059669"/>
            <circle cx="-52" cy="30" r="3" fill="#dc2626"/>
            <text x="0" y="5" text-anchor="middle" font-size="7.5" font-weight="700" fill="#0369a1">RAID 5 Sweet Spot</text>
          </g>

          <text x="130" y="248" text-anchor="middle" font-size="6.5" fill="#475569">No architecture maximizes all three simultaneously!</text>
        </g>

        <!-- Right: Striping Block Allocation & Chunk Geometry -->
        <g transform="translate(290, 20)">
          <rect width="455" height="260" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <text x="20" y="24" font-size="10" font-weight="700" fill="#0284c7">DATA STRIPING: LINEAR STREAM TO DISK CHUNKS</text>
          <text x="20" y="38" font-size="7.5" fill="#64748b">Chunk Size (S) = 64 KB &bull; Stripe Width = 4 Disks &bull; Full Stripe = 256 KB</text>

          <!-- Input Linear File Stream (Top) -->
          <g transform="translate(20, 52)">
            <rect width="415" height="26" rx="3" fill="#f1f5f9" stroke="#94a3b8"/>
            <text x="10" y="17" font-size="7" font-weight="700" fill="#334155">LOGICAL FILE OFFSET:</text>
            <rect x="110" y="3" width="70" height="20" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
            <text x="145" y="16" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">Chunk 0 (0&ndash;64K)</text>
            <rect x="185" y="3" width="70" height="20" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
            <text x="220" y="16" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">Chunk 1 (64&ndash;128K)</text>
            <rect x="260" y="3" width="70" height="20" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
            <text x="295" y="16" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">Chunk 2 (128&ndash;192K)</text>
            <rect x="335" y="3" width="70" height="20" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
            <text x="370" y="16" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">Chunk 3 (192&ndash;256K)</text>
          </g>

          <!-- Parallel Striped Disks (Bottom) -->
          <g transform="translate(20, 95)">
            <!-- Disk 0 -->
            <g transform="translate(0, 0)">
              <rect width="95" height="145" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
              <text x="47" y="16" text-anchor="middle" font-size="7.5" font-weight="700" fill="#0f172a">DISK 0</text>
              <rect x="8" y="24" width="79" height="22" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
              <text x="47" y="38" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">Chunk 0</text>
              <rect x="8" y="50" width="79" height="22" rx="2" fill="#f1f5f9" stroke="#94a3b8"/>
              <text x="47" y="64" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#475569">Chunk 4</text>
              <rect x="8" y="76" width="79" height="22" rx="2" fill="#f1f5f9" stroke="#94a3b8"/>
              <text x="47" y="90" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#475569">Chunk 8</text>
              <rect x="8" y="102" width="79" height="22" rx="2" fill="#f1f5f9" stroke="#94a3b8"/>
              <text x="47" y="116" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#475569">Chunk 12</text>
            </g>

            <!-- Disk 1 -->
            <g transform="translate(107, 0)">
              <rect width="95" height="145" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
              <text x="47" y="16" text-anchor="middle" font-size="7.5" font-weight="700" fill="#0f172a">DISK 1</text>
              <rect x="8" y="24" width="79" height="22" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
              <text x="47" y="38" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">Chunk 1</text>
              <rect x="8" y="50" width="79" height="22" rx="2" fill="#f1f5f9" stroke="#94a3b8"/>
              <text x="47" y="64" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#475569">Chunk 5</text>
              <rect x="8" y="76" width="79" height="22" rx="2" fill="#f1f5f9" stroke="#94a3b8"/>
              <text x="47" y="90" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#475569">Chunk 9</text>
              <rect x="8" y="102" width="79" height="22" rx="2" fill="#f1f5f9" stroke="#94a3b8"/>
              <text x="47" y="116" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#475569">Chunk 13</text>
            </g>

            <!-- Disk 2 -->
            <g transform="translate(214, 0)">
              <rect width="95" height="145" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
              <text x="47" y="16" text-anchor="middle" font-size="7.5" font-weight="700" fill="#0f172a">DISK 2</text>
              <rect x="8" y="24" width="79" height="22" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
              <text x="47" y="38" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">Chunk 2</text>
              <rect x="8" y="50" width="79" height="22" rx="2" fill="#f1f5f9" stroke="#94a3b8"/>
              <text x="47" y="64" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#475569">Chunk 6</text>
              <rect x="8" y="76" width="79" height="22" rx="2" fill="#f1f5f9" stroke="#94a3b8"/>
              <text x="47" y="90" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#475569">Chunk 10</text>
              <rect x="8" y="102" width="79" height="22" rx="2" fill="#f1f5f9" stroke="#94a3b8"/>
              <text x="47" y="116" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#475569">Chunk 14</text>
            </g>

            <!-- Disk 3 -->
            <g transform="translate(320, 0)">
              <rect width="95" height="145" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
              <text x="47" y="16" text-anchor="middle" font-size="7.5" font-weight="700" fill="#0f172a">DISK 3</text>
              <rect x="8" y="24" width="79" height="22" rx="2" fill="#e0f2fe" stroke="#0284c7"/>
              <text x="47" y="38" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">Chunk 3</text>
              <rect x="8" y="50" width="79" height="22" rx="2" fill="#f1f5f9" stroke="#94a3b8"/>
              <text x="47" y="64" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#475569">Chunk 7</text>
              <rect x="8" y="76" width="79" height="22" rx="2" fill="#f1f5f9" stroke="#94a3b8"/>
              <text x="47" y="90" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#475569">Chunk 11</text>
              <rect x="8" y="102" width="79" height="22" rx="2" fill="#f1f5f9" stroke="#94a3b8"/>
              <text x="47" y="116" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#475569">Chunk 15</text>
            </g>
          </g>
        </g>
      </svg>
    </div>

    <h4>The Three Orthogonal Design Axes</h4>
    <p>
      Every multi-disk storage topology represents a deliberate engineering compromise across three interdependent design criteria:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; margin: 20px 0;">
      <!-- Capacity Efficiency Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--accent); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.92rem;">1. Capacity Efficiency (&eta;)</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--accent); text-transform: uppercase; margin-bottom: 8px;">Storage Overhead Ratio</div>
        <p style="margin: 0; font-size: 0.8rem; color: #475569; line-height: 1.5;">
          The fraction of raw installed storage available for user files:
          <div style="margin: 8px 0; font-family: var(--font-mono); font-size: 0.75rem; color: #0369a1;">
            &eta; = Usable / (<i>N</i> &times; <i>C</i>)
          </div>
          &bull; <strong>RAID 0:</strong> 100% (&eta; = 1.0)<br>
          &bull; <strong>RAID 1:</strong> 50% (&eta; = 0.5)<br>
          &bull; <strong>RAID 5:</strong> (<i>N</i>-1)/<i>N</i> (e.g. 87.5% on 8 disks)<br>
          &bull; <strong>RAID 6:</strong> (<i>N</i>-2)/<i>N</i> (e.g. 75.0% on 8 disks)
        </p>
      </div>

      <!-- Performance Multiplier Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.92rem;">2. Performance Multiplier</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--success); text-transform: uppercase; margin-bottom: 8px;">IOPS &amp; Bandwidth Scaling</div>
        <p style="margin: 0; font-size: 0.8rem; color: #475569; line-height: 1.5;">
          The degree of concurrency:
          <br><br>
          &bull; <strong>Throughput (MB/s):</strong> Aggregates up to <i>N</i> &times; single-disk bandwidth for large sequential transfers.<br>
          &bull; <strong>Random IOPS:</strong> Scales with independent spindle count for reads, but is constrained by parity read-modify-write updates on writes.
        </p>
      </div>

      <!-- Reliability & MTTDL Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--danger); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.92rem;">3. Reliability (MTTDL)</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--danger); text-transform: uppercase; margin-bottom: 8px;">Mean Time to Data Loss</div>
        <p style="margin: 0; font-size: 0.8rem; color: #475569; line-height: 1.5;">
          Tolerance against physical drive failures:
          <br><br>
          &bull; <strong>RAID 0:</strong> 0 drive failures tolerated.<br>
          &bull; <strong>RAID 1 / 5:</strong> Exactly 1 drive failure.<br>
          &bull; <strong>RAID 6:</strong> Exactly 2 concurrent drive failures.<br>
          Accounts for rebuild windows and unrecoverable read errors (UREs).
        </p>
      </div>
    </div>

    <h4>The Reliability Multiplication Trap</h4>
    <p>
      Why did the 1988 Berkeley paper mandate redundancy? Why could computer architects not simply stripe data across 50 inexpensive disks to achieve 50 times the performance?
    </p>
    <p>
      The answer lies in Poisson reliability probability. Suppose a single commodity drive has a Mean Time To Failure (MTTF) of <strong>1,000,000 hours</strong> (approximately 114 years):
    </p>
    <ul>
      <li>If an array contains <i>N</i> = 100 identical independent disks, the failure rate of the array (&lambda;<sub>array</sub>) is the sum of the individual failure rates:
        <div class="math-callout" style="text-align: center;">
          &lambda;<sub>array</sub> = <i>N</i> &times; &lambda;<sub>single</sub> = <sup><i>N</i></sup>&frasl;<sub>MTTF<sub>single</sub></sub>
        </div>
      </li>
      <li>The Mean Time To Failure of the unstriped array collapses linearly:
        <div class="math-callout" style="text-align: center;">
          MTTF<sub>array</sub> = <sup>MTTF<sub>single</sub></sup>&frasl;<sub><i>N</i></sub> = <sup>1,000,000 hours</sup>&frasl;<sub>100</sub> = <strong>10,000 hours &asymp; 1.14 years</strong>
        </div>
      </li>
      <li>In a datacenter operating 1,000 unstriped disks, a catastrophic array failure destroying all user data would occur <strong>every 41 days</strong>!</li>
    </ul>
    <p>
      Therefore, <strong>striping without redundancy (RAID 0) is a reliability disaster</strong>. To harvest the throughput and capacity benefits of multiple spindles, storage architectures must introduce mathematical redundancy (mirroring or parity codes) to survive drive deaths.
    </p>

    <h4>Data Striping Mechanics: Chunk Mapping Formulas</h4>
    <p>
      <strong>Data Striping</strong> segments a contiguous linear logical address space into fixed-size chunks and interleaves those chunks across <i>N</i> physical disks in a round-robin cycle:
    </p>
    <ul>
      <li><strong>Stripe Unit / Chunk Size (<i>S</i>):</strong> The amount of contiguous data written to a single drive before stepping to the next drive (typically 64 KB, 128 KB, or 256 KB in production filesystems).</li>
      <li><strong>Stripe Width:</strong> The number of physical data disks participating in the stripe.</li>
      <li><strong>Full Stripe Size:</strong> The total capacity of data written across all data disks in one complete round-robin cycle:
        <div style="margin: 6px 0; font-family: var(--font-mono); font-size: 0.85rem; color: #0284c7;">
          Full Stripe Size = Stripe Width &times; <i>S</i>
        </div>
      </li>
    </ul>

    <div class="math-callout">
      <strong>Mathematical Coordinate Transformation:</strong>
      <br>
      Given an incoming logical byte offset <i>B</i> from an application write, the RAID controller determines the physical disk and on-disk offset using integer division and modulo arithmetic:
      <div style="margin: 10px 0; font-family: var(--font-mono); font-size: 0.85rem; color: #0f172a; line-height: 1.8;">
        Chunk Index = &lfloor; <i>B</i> / <i>S</i> &rfloor;<br>
        Target Disk Index = Chunk Index mod <i>N</i><br>
        Physical Offset on Target Disk = ( &lfloor; Chunk Index / <i>N</i> &rfloor; &times; <i>S</i> ) + ( <i>B</i> mod <i>S</i> )
      </div>
      <em>Worked Example:</em> On a 4-disk array (<i>N</i> = 4) with chunk size <i>S</i> = 64 KB (65,536 bytes), where does logical byte offset <strong><i>B</i> = 300,000</strong> reside?
      <ol style="margin: 6px 0 0 16px; padding: 0; font-size: 0.82rem;">
        <li>Chunk Index = &lfloor; 300,000 / 65,536 &rfloor; = <strong>4</strong> (the 5th chunk in the stream).</li>
        <li>Target Disk Index = 4 mod 4 = <strong>Disk 0</strong>.</li>
        <li>Physical Offset = ( &lfloor; 4 / 4 &rfloor; &times; 65,536 ) + ( 300,000 mod 65,536 ) = 65,536 + 37,856 = <strong>Byte 103,392 on Disk 0</strong>.</li>
      </ol>
    </div>

    <h4>Chunk Size Trade-off: Fine-Grained vs. Coarse-Grained Striping</h4>
    <p>
      The selection of chunk size <i>S</i> represents a critical performance tuning parameter that dictates how the storage array behaves under concurrent workloads:
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
      <!-- Fine-Grained Striping Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--warning); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.92rem;">Fine-Grained Striping (Byte / Word Level)</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--warning); text-transform: uppercase; margin-bottom: 8px;">RAID 2 &amp; RAID 3 &bull; Lockstep Spindles</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Data is interleaved at the byte or 32-bit word level. Every single file read or write spans across all <i>N</i> disks concurrently.
          <br><br>
          <em>The Fundamental Limitation:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>All drive spindle motors must be synchronized in lockstep rotation.</li>
            <li>All read/write heads seek to identical cylinder locations simultaneously.</li>
            <li><strong>Zero Concurrency:</strong> The entire array acts as a single monolithic drive. The array can service only <strong>one I/O request at a time</strong> (Random IOPS &asymp; 1&times;). Ideal only for single-user sequential workloads like uncompressed video playback.</li>
          </ul>
        </p>
      </div>

      <!-- Coarse-Grained Striping Card -->
      <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--success); border-radius: 6px; padding: 14px;">
        <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 0.92rem;">Coarse-Grained Striping (Block Level)</h4>
        <div style="font-size: 0.72rem; font-weight: 700; color: var(--success); text-transform: uppercase; margin-bottom: 8px;">RAID 0, 4, 5, 6, 10 &bull; Independent Spindles</div>
        <p style="margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.5;">
          Chunk size <i>S</i> is large (e.g. 64 KB &ndash; 256 KB), matching or exceeding typical operating system filesystem block allocations (4 KB &ndash; 16 KB).
          <br><br>
          <em>The Multi-Spindle Throughput Advantage:</em>
          <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.8rem;">
            <li>Small individual reads (e.g. an 8 KB database record) fit entirely inside a single chunk on a single disk.</li>
            <li><strong>Maximum Multi-User Concurrency:</strong> Different disks can service completely unrelated read requests from different application threads simultaneously, scaling aggregate random performance to <strong><i>N</i> &times; IOPS</strong>!</li>
            <li>Large sequential streaming requests automatically span across all <i>N</i> disks, harvesting <strong><i>N</i> &times; Transfer Bandwidth</strong>.</li>
          </ul>
        </p>
      </div>
    </div>

    <div class="math-callout">
      <strong>The Production Sizing Dilemma for Chunk Size (S):</strong>
      <br>
      Selecting <i>S</i> requires careful workload profiling:
      <ul>
        <li><strong>If <i>S</i> is too small (e.g. 4 KB):</strong> A modest 64 KB request fragments across all drives, forcing every spindle to seek and thrash, destroying independent concurrency.</li>
        <li><strong>If <i>S</i> is too large (e.g. 4 MB):</strong> Small files concentrate onto a single physical drive, causing severe <strong>hotspotting</strong> (one disk hits 100% utilization while adjacent disks sit idle).</li>
        <li><strong>Industrial Default:</strong> Most enterprise storage arrays standardize on <strong>64 KB or 128 KB chunk sizes</strong>, balancing single-request parallelism with multi-threaded independent IOPS.</li>
      </ul>
    </div>"""

def update_section_one():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>1. The Three Orthogonal Design Axes &amp; Striping</h3>"
    end_marker = "<h3>2. Taxonomy of Standard RAID Levels</h3>"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 1 boundaries in Module 04.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_ONE + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 1 in {TARGET_FILE}")
    return True

def run_git_sync():
    status = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
    if not status:
        print("--> Working tree is clean. Nothing to commit.")
        return

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 1 of Module 04 on RAID Design Axes and Striping Math\n\n"
            "Detail capacity efficiency, IOPS vs throughput scaling, MTTDL modeling,\n"
            "LBA-to-disk chunk mapping formulas, fine vs coarse striping, and add SVG."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_one():
        run_git_sync()
