#!/usr/bin/env python3
# =====================================================================
# fix.py: Deeply expand Section 3 of 04-raid-architectures.html
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "04-raid-architectures.html"
)

EXPANDED_SECTION_THREE_PRE_AID = r"""    <h3>3. Mathematical Foundations: XOR Parity &amp; The URE Rebuild Crisis</h3>
    <p>
      At the core of redundant storage arrays lies discrete linear algebra. Rather than paying the 100% capacity overhead of full physical mirroring, parity-based architectures (RAID 4, 5, and 6) exploit algebraic invariants to reconstruct missing information from surviving physical channels.
    </p>
    <p>
      However, the mathematical assumptions established in the 1988 Berkeley paper assumed small mechanical drives (20 MB to 100 MB). In modern architectures with 16 TB to 24 TB physical disks, the physical interaction between long rebuild times and magnetic recording noise introduces a catastrophic failure phenomenon known as the <strong>Unrecoverable Read Error (URE) Rebuild Crisis</strong>.
    </p>

    <!-- Structural Diagram: URE Rebuild Collision vs RAID 6 Rescue -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 4.2: The URE Rebuild Collision &mdash; Single Parity Collapse vs. Galois Field Q Rescue</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">Why a secondary bad sector during a RAID 5 rebuild permanently destroys data, and how RAID 6 solves the dual-unknown equation.</div>

      <svg viewBox="0 0 760 270" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="ure-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="ure-arr-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#dc2626" />
          </marker>
          <marker id="ure-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
        </defs>

        <!-- Column 1: RAID 5 URE Rebuild Trap (Left) -->
        <g transform="translate(15, 20)">
          <rect width="345" height="230" rx="8" fill="#f8fafc" stroke="#dc2626" stroke-width="1.5"/>
          <text x="172" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="#991b1b">RAID 5: REBUILD COLLISION (TOTAL LOSS)</text>
          <text x="172" y="38" text-anchor="middle" font-size="7.5" fill="#dc2626">1 Dead Drive + 1 URE = 2 Unknowns (Unsolvable)</text>

          <!-- Drive Bay Strip -->
          <g transform="translate(15, 52)">
            <!-- Disk 0 (Online) -->
            <rect x="0" y="0" width="70" height="60" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="35" y="16" text-anchor="middle" font-size="7" font-weight="700" fill="#334155">DISK 0</text>
            <rect x="5" y="22" width="60" height="18" rx="2" fill="#e0f2fe"/>
            <text x="35" y="34" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#0369a1">A0 = 1011</text>
            <text x="35" y="52" text-anchor="middle" font-size="6.5" fill="#059669">&#10003; Read OK</text>

            <!-- Disk 1 (Dead) -->
            <rect x="80" y="0" width="70" height="60" rx="3" fill="#fee2e2" stroke="#dc2626"/>
            <text x="115" y="16" text-anchor="middle" font-size="7" font-weight="700" fill="#dc2626">DISK 1</text>
            <rect x="85" y="22" width="60" height="18" rx="2" fill="#f1f5f9" stroke="#cbd5e1" stroke-dasharray="2 2"/>
            <text x="115" y="34" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" fill="#94a3b8">A1 = ?</text>
            <text x="115" y="52" text-anchor="middle" font-size="6.5" font-weight="700" fill="#dc2626">&times; DEAD</text>

            <!-- Disk 2 (URE Bad Sector!) -->
            <rect x="160" y="0" width="75" height="60" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
            <text x="197" y="16" text-anchor="middle" font-size="7" font-weight="700" fill="#dc2626">DISK 2</text>
            <rect x="165" y="22" width="65" height="18" rx="2" fill="#dc2626"/>
            <text x="197" y="34" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" font-weight="700" fill="#ffffff">URE SECTOR!</text>
            <text x="197" y="52" text-anchor="middle" font-size="6.5" font-weight="700" fill="#dc2626">&times; A2 = ?</text>

            <!-- Disk 3 (Parity) -->
            <rect x="245" y="0" width="70" height="60" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="280" y="16" text-anchor="middle" font-size="7" font-weight="700" fill="#334155">DISK 3</text>
            <rect x="250" y="22" width="60" height="18" rx="2" fill="#fee2e2" stroke="#dc2626"/>
            <text x="280" y="34" text-anchor="middle" font-family="var(--font-mono)" font-size="6.5" font-weight="700" fill="#991b1b">Ap = 1101</text>
            <text x="280" y="52" text-anchor="middle" font-size="6.5" fill="#059669">&#10003; Read OK</text>
          </g>

          <!-- Algebraic Failure Box -->
          <rect x="15" y="125" width="315" height="90" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="25" y="142" font-size="7.5" font-weight="700" fill="#dc2626">ALGEBRAIC IMPOSSIBILITY IN GF(2):</text>
          <text x="25" y="158" font-family="var(--font-mono)" font-size="7.5" fill="#334155">Equation: A0 &oplus; <tspan fill="#dc2626" font-weight="700">A1</tspan> &oplus; <tspan fill="#dc2626" font-weight="700">A2</tspan> = Ap</text>
          <text x="25" y="174" font-family="var(--font-mono)" font-size="7.5" fill="#334155">&rarr; 1011 &oplus; <tspan fill="#dc2626" font-weight="700">A1</tspan> &oplus; <tspan fill="#dc2626" font-weight="700">A2</tspan> = 1101 &implies; <tspan fill="#dc2626" font-weight="700">A1 &oplus; A2 = 0110</tspan></text>
          <text x="25" y="190" font-size="7" fill="#dc2626">1 Equation, 2 Unknowns &rarr; Infinite solutions!</text>
          <text x="25" y="204" font-size="7" font-weight="700" fill="#991b1b">&times; ARRAY ABORTS &bull; REBUILD FAILS &bull; DATA DESTROYED</text>
        </g>

        <!-- Column 2: RAID 6 Dual-Parity Rescue (Right) -->
        <g transform="translate(385, 20)">
          <rect width="360" height="230" rx="8" fill="#f8fafc" stroke="#059669" stroke-width="2"/>
          <text x="180" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="#166534">RAID 6: GALOIS FIELD RESCUE (DATA SAVED)</text>
          <text x="180" y="38" text-anchor="middle" font-size="7.5" fill="#166534">Dual Parity (P + Q) Solves 2 Independent Equations</text>

          <!-- Drive Bay Strip -->
          <g transform="translate(15, 52)">
            <!-- Disk 0 -->
            <rect x="0" y="0" width="58" height="60" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="29" y="16" text-anchor="middle" font-size="6.5" font-weight="700" fill="#334155">D0</text>
            <text x="29" y="34" text-anchor="middle" font-family="var(--font-mono)" font-size="6" fill="#0369a1">A0: OK</text>

            <!-- Disk 1 (Dead) -->
            <rect x="66" y="0" width="58" height="60" rx="3" fill="#fee2e2" stroke="#dc2626"/>
            <text x="95" y="16" text-anchor="middle" font-size="6.5" font-weight="700" fill="#dc2626">D1 [Dead]</text>
            <text x="95" y="34" text-anchor="middle" font-family="var(--font-mono)" font-size="6" fill="#dc2626">A1 = ?</text>

            <!-- Disk 2 (URE) -->
            <rect x="132" y="0" width="58" height="60" rx="3" fill="#fee2e2" stroke="#dc2626"/>
            <text x="161" y="16" text-anchor="middle" font-size="6.5" font-weight="700" fill="#dc2626">D2 [URE]</text>
            <text x="161" y="34" text-anchor="middle" font-family="var(--font-mono)" font-size="6" fill="#dc2626">A2 = ?</text>

            <!-- Disk 3 (P) -->
            <rect x="198" y="0" width="62" height="60" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="229" y="16" text-anchor="middle" font-size="6.5" font-weight="700" fill="#334155">D3 [P-Par]</text>
            <text x="229" y="34" text-anchor="middle" font-family="var(--font-mono)" font-size="6" fill="#991b1b">P: Valid</text>

            <!-- Disk 4 (Q) -->
            <rect x="268" y="0" width="62" height="60" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="299" y="16" text-anchor="middle" font-size="6.5" font-weight="700" fill="#334155">D4 [Q-Par]</text>
            <text x="299" y="34" text-anchor="middle" font-family="var(--font-mono)" font-size="6" fill="#b45309">Q: Valid</text>
          </g>

          <!-- Algebraic Rescue Box -->
          <rect x="15" y="125" width="330" height="90" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="25" y="142" font-size="7.5" font-weight="700" fill="#166534">LINEAR SYSTEM SOLVED IN GF(2^8):</text>
          <text x="25" y="158" font-family="var(--font-mono)" font-size="7.5" fill="#334155">Eq 1: A1 &oplus; A2 = P &oplus; A0</text>
          <text x="25" y="174" font-family="var(--font-mono)" font-size="7.5" fill="#334155">Eq 2: (g^1 &otimes; A1) &oplus; (g^2 &otimes; A2) = Q &oplus; (g^0 &otimes; A0)</text>
          <text x="25" y="190" font-size="7" fill="#166534">2 Linearly Independent Equations &rarr; Unique Solution!</text>
          <text x="25" y="204" font-size="7" font-weight="700" fill="#15803d">&#10003; BOTH MISSING BLOCKS RESTORED &bull; ARRAY SURVIVES</text>
        </g>
      </svg>
    </div>

    <h4>1. Boolean XOR Algebraic Mechanics</h4>
    <p>
      The exclusive-OR operator (denoted by &oplus; in Boolean algebra and <code>^</code> in C/C++) forms an <strong>Abelian (commutative) group</strong> over binary fields. Parity encoding and decoding rely on four elementary algebraic properties:
    </p>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 14px 0;">
      <div style="background: #ffffff; border: 1px solid var(--border); border-left: 4px solid var(--accent); padding: 10px 14px; border-radius: 4px;">
        <span style="font-size: 0.8rem; font-weight: 700; color: #0284c7;">1. Commutativity &amp; Associativity:</span>
        <div style="font-family: var(--font-mono); font-size: 0.82rem; color: #1e293b; margin-top: 4px;">
          <i>A</i> &oplus; <i>B</i> = <i>B</i> &oplus; <i>A</i><br>
          (<i>A</i> &oplus; <i>B</i>) &oplus; <i>C</i> = <i>A</i> &oplus; (<i>B</i> &oplus; <i>C</i>)
        </div>
      </div>
      <div style="background: #ffffff; border: 1px solid var(--border); border-left: 4px solid var(--success); padding: 10px 14px; border-radius: 4px;">
        <span style="font-size: 0.8rem; font-weight: 700; color: #166534;">2. Identity &amp; Self-Inversion:</span>
        <div style="font-family: var(--font-mono); font-size: 0.82rem; color: #1e293b; margin-top: 4px;">
          <i>A</i> &oplus; 0 = <i>A</i><br>
          <i>A</i> &oplus; <i>A</i> = 0 &nbsp; (Self-Inverting Inverse)
        </div>
      </div>
    </div>

    <h5>The Parity Invariant and Recovery Derivation</h5>
    <p>
      In a RAID 5 stripe composed of <i>N</i> - 1 data blocks (<i>D</i><sub>0</sub>, <i>D</i><sub>1</sub>, &hellip;, <i>D</i><sub><i>N</i>-2</sub>) and one parity block <i>P</i>, the parity is defined as:
    </p>
    <div class="math-callout" style="text-align: center; font-size: 0.95rem;">
      <i>P</i> = <i>D</i><sub>0</sub> &oplus; <i>D</i><sub>1</sub> &oplus; &hellip; &oplus; <i>D</i><sub><i>N</i>-2</sub>
    </div>
    <p>
      XORing both sides of this equation with <i>P</i> yields the fundamental <strong>Stripe Invariant</strong>:
    </p>
    <div class="math-callout" style="text-align: center; font-size: 0.95rem;">
      <i>D</i><sub>0</sub> &oplus; <i>D</i><sub>1</sub> &oplus; &hellip; &oplus; <i>D</i><sub><i>N</i>-2</sub> &oplus; <i>P</i> = 0
    </div>
    <p>
      Suppose physical drive <i>k</i> suffers a hardware head crash, losing block <i>D</i><sub><i>k</i></sub>. To reconstruct the missing data, the RAID controller reads all surviving data blocks and the parity block, and XORs them together:
    </p>
    <div class="math-callout" style="text-align: center; font-size: 0.95rem;">
      <i>D</i><sub><i>k</i></sub> = <i>P</i> &oplus; &sum;<sub><i>i</i> &ne; <i>k</i></sub><sup>&oplus;</sup> <i>D</i><sub><i>i</i></sub>
    </div>
    <p>
      Because XOR is self-inverting (<i>D</i><sub><i>i</i></sub> &oplus; <i>D</i><sub><i>i</i></sub> = 0 for all surviving blocks), every surviving block cancels itself out, leaving the exact bit pattern of the lost block <i>D</i><sub><i>k</i></sub>.
    </p>

    <h5>Two Parity Update Strategies: RMW vs. Reconstruct-Write</h5>
    <p>
      When an application modifies disk data, the RAID controller dynamically selects one of two algorithms to update parity:
    </p>
    <ul>
      <li>
        <strong>Read-Modify-Write (RMW / Sub-Stripe Update):</strong>
        If an application updates a single block (<i>D</i><sub><i>k</i> (new)</sub>), reading the entire remaining stripe is wasteful. The controller computes the differential parity change:
        <div style="margin: 6px 0; font-family: var(--font-mono); font-size: 0.85rem; color: #0284c7; text-align: center;">
          <i>P</i><sub>new</sub> = ( <i>D</i><sub><i>k</i> (old)</sub> &oplus; <i>D</i><sub><i>k</i> (new)</sub> ) &oplus; <i>P</i><sub>old</sub>
        </div>
        <em>Cost:</em> 2 physical reads (<i>D</i><sub>old</sub>, <i>P</i><sub>old</sub>) + 2 physical writes (<i>D</i><sub>new</sub>, <i>P</i><sub>new</sub>) = <strong>4 physical I/Os</strong>.
      </li>
      <li>
        <strong>Reconstruct-Write (RCW / Full-Stripe Write):</strong>
        If an application issues a large sequential write that modifies more than half of the data blocks in a stripe (or the entire stripe), RMW becomes inefficient. The controller does not read old parity; instead, it reads the few <em>unmodified</em> data blocks, computes the new parity directly in RAM from the new data, and writes the new data and new parity concurrently.
      </li>
    </ul>

    <h4>2. Galois Field GF(2<sup>8</sup>) Dual-Parity Mechanics (RAID 6)</h4>
    <p>
      Why can RAID 5 not survive two drive failures?
      If two drives fail in the same stripe (e.g. <i>D</i><sub>1</sub> and <i>D</i><sub>2</sub>), the parity equation becomes:
    </p>
    <div style="margin: 8px 0; font-family: var(--font-mono); font-size: 0.85rem; color: #dc2626; text-align: center;">
      <i>D</i><sub>1</sub> &oplus; <i>D</i><sub>2</sub> = <i>P</i> &oplus; &sum;<sub><i>i</i> &ne; 1,2</sub><sup>&oplus;</sup> <i>D</i><sub><i>i</i></sub>
    </div>
    <p>
      This represents <strong>one linear equation with two unknowns</strong>. In binary arithmetic, there are $2^{32}$ valid pairs of (<i>D</i><sub>1</sub>, <i>D</i><sub>2</sub>) that satisfy this sum. The data is mathematically unrecoverable.
    </p>

    <h5>The Reed-Solomon P+Q Formulation</h5>
    <p>
      To resolve two unknowns, linear algebra mandates <strong>two linearly independent equations</strong>. In RAID 6, the storage controller evaluates operations over the <strong>Galois Field GF(2<sup>8</sup>)</strong> (a finite field of 256 elements where each byte is treated as an 8-bit polynomial modulo an irreducible primitive polynomial <i>p</i>(<i>x</i>) = <i>x</i><sup>8</sup> + <i>x</i><sup>4</sup> + <i>x</i><sup>3</sup> + <i>x</i><sup>2</sup> + 1):
    </p>
    <ul>
      <li><strong>Parity P (Linear XOR Code):</strong>
        <div style="margin: 4px 0; font-family: var(--font-mono); font-size: 0.82rem; color: #0284c7; text-align: center;">
          <i>P</i> = <i>D</i><sub>0</sub> &oplus; <i>D</i><sub>1</sub> &oplus; <i>D</i><sub>2</sub> &hellip; &oplus; <i>D</i><sub><i>N</i>-3</sub>
        </div>
      </li>
      <li><strong>Parity Q (Galois Field Polynomial Code):</strong>
        <div style="margin: 4px 0; font-family: var(--font-mono); font-size: 0.82rem; color: #d97706; text-align: center;">
          <i>Q</i> = ( <i>g</i><sup>0</sup> &otimes; <i>D</i><sub>0</sub> ) &oplus; ( <i>g</i><sup>1</sup> &otimes; <i>D</i><sub>1</sub> ) &oplus; ( <i>g</i><sup>2</sup> &otimes; <i>D</i><sub>2</sub> ) &hellip; &oplus; ( <i>g</i><sup><i>N</i>-3</sup> &otimes; <i>D</i><sub><i>N</i>-3</sub> )
        </div>
        where <i>g</i> is the primitive generator of GF(2<sup>8</sup>) (typically <i>g</i> = 0x02) and &otimes; represents polynomial Galois multiplication.
      </li>
    </ul>

    <h5>Dual-Drive Recovery in RAID 6</h5>
    <p>
      If both Drive <i>x</i> and Drive <i>y</i> fail simultaneously, the controller measures the residual syndromic differences:
    </p>
    <div class="math-callout" style="font-family: var(--font-mono); font-size: 0.85rem; line-height: 1.8;">
      <i>D</i><sub><i>x</i></sub> &oplus; <i>D</i><sub><i>y</i></sub> = <i>P</i> &oplus; &sum;<sub><i>i</i> &ne; <i>x</i>,<i>y</i></sub> <i>D</i><sub><i>i</i></sub> = <i>P</i>'<br>
      ( <i>g</i><sup><i>x</i></sup> &otimes; <i>D</i><sub><i>x</i></sub> ) &oplus; ( <i>g</i><sup><i>y</i></sup> &otimes; <i>D</i><sub><i>y</i></sub> ) = <i>Q</i> &oplus; &sum;<sub><i>i</i> &ne; <i>x</i>,<i>y</i></sub> ( <i>g</i><sup><i>i</i></sup> &otimes; <i>D</i><sub><i>i</i></sub> ) = <i>Q</i>'
    </div>
    <p>
      This represents a $2 \times 2$ <strong>Vandermonde linear system</strong> over GF(2<sup>8</sup>). Because the generator powers $g^x$ and $g^y$ are distinct, the system matrix determinant is strictly non-zero. By multiplying through by $(g^x \oplus g^y)^{-1}$, the controller solves uniquely for both <i>D</i><sub><i>x</i></sub> and <i>D</i><sub><i>y</i></sub>, restoring all data without loss.
    </p>

    <h4>3. Mean Time to Data Loss (MTTDL) Reliability Modeling</h4>
    <p>
      To quantitatively evaluate array resilience, storage engineers model disk failures using continuous-time <strong>Markov Chains</strong>:
    </p>
    <div style="overflow-x: auto; margin: 16px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 12px; width: 25%;">System State</th>
            <th style="padding: 10px 12px; width: 35%;">Transition Out</th>
            <th style="padding: 10px 12px; width: 40%;">Physical Reality</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700; color: #166534;">State 0: Optimal</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">Rate = <i>N</i> &times; &lambda;</td>
            <td style="padding: 10px 12px;">All <i>N</i> drives healthy. Any drive can fail with Poisson arrival rate &lambda; = 1 / MTTF.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #fffbeb;">
            <td style="padding: 10px 12px; font-weight: 700; color: #b45309;">State 1: Degraded</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">Repair Rate = &mu; = 1 / MTTR<br>Failure Rate = (<i>N</i> - 1) &times; &lambda;</td>
            <td style="padding: 10px 12px;">One drive dead. Rebuild underway to hot spare. Array is vulnerable to secondary failures.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #fef2f2;">
            <td style="padding: 10px 12px; font-weight: 700; color: #dc2626;">State 2: Data Loss</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem; color: #dc2626;">Absorbing State</td>
            <td style="padding: 10px 12px; color: #dc2626;">A second drive dies before the rebuild completes. Array collapses; data lost permanently.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="math-callout">
      <strong>The Analytical MTTDL Formulation (Single-Fault Tolerant Arrays):</strong>
      <br>
      Solving the Markov differential equations yields the classical MTTDL formula for RAID 1 and RAID 5 arrays:
      <div style="margin: 8px 0; font-size: 1.05rem; text-align: center;">
        MTTDL = <sup>MTTF<sub>disk</sub><sup>2</sup></sup>&frasl;<sub><i>N</i>(<i>N</i> - 1) &times; MTTR</sub>
      </div>
      where:
      <ul style="margin: 6px 0 0 16px; padding: 0; font-size: 0.82rem;">
        <li><strong>MTTF<sub>disk</sub>:</strong> Mean Time To Failure of an individual drive (typically 1,000,000 to 1,500,000 hours &asymp; 114 to 170 years).</li>
        <li><strong><i>N</i>:</strong> Total number of drives in the array.</li>
        <li><strong>MTTR:</strong> Mean Time To Repair (the time required to detect failure, insert a hot spare, and rebuild all parity data).</li>
      </ul>
      <strong>The Critical Vulnerability:</strong> Notice that MTTR resides in the denominator. As hard drive capacity ballooned from 500 GB to 18 TB, <strong>rebuild times stretched from 2 hours to 48&ndash;72 hours</strong>. Increasing MTTR directly degrades MTTDL by orders of magnitude!
    </div>

    <h4>4. The Modern URE Crisis: Why RAID 5 is Dead for Large Disks</h4>
    <p>
      While mechanical motor seizures and head crashes are visible, hard drives suffer from an insidious, microscopic physical flaw: <strong>Unrecoverable Read Errors (UREs)</strong> (also known as Non-Recoverable Read Errors).
    </p>
    <ul>
      <li>
        <strong>The Physics of a URE:</strong> Platter magnetic domains experience thermal decay, micro-shock head contact, or electromagnetic crosstalk. When a sector degrades beyond the internal ECC engine's capability to correct, the drive's firmware attempts multiple internal retries, fails, and returns an uncorrectable I/O read error (e.g. <code>EIO</code> or <code>UNC</code> in Linux).
      </li>
      <li>
        <strong>Manufacturer Specifications:</strong>
        Hard drive manufacturers specify the statistical frequency of UREs in drive technical datasheets:
        <ul>
          <li><strong>Consumer SATA Drives:</strong> Rated at <strong>1 sector error in every 10<sup>14</sup> bits read</strong> (roughly 1 error per 12.5 TB read).</li>
          <li><strong>Enterprise SAS / NVMe Drives:</strong> Rated at <strong>1 sector error in every 10<sup>15</sup> bits read</strong> (roughly 1 error per 125 TB read).</li>
        </ul>
      </li>
    </ul>

    <h5>The Statistical Impossibility of RAID 5 Rebuilds</h5>
    <p>
      During normal operation, a single URE on a healthy RAID 5 array is harmless: the controller simply reconstructs the bad sector on the fly from the surviving data and parity disks.
    </p>
    <p>
      <strong>However, during an active RAID 5 rebuild, a URE is catastrophic.</strong>
      When Drive 1 fails, the controller must read <em>every single sector from start to finish</em> across all remaining <i>N</i> - 1 surviving drives to reconstruct Drive 1 onto the replacement drive.
    </p>
    <p>
      The probability of reading <i>B</i> bits without encountering an unrecoverable read error obeys the Bernoulli trial distribution:
    </p>

    <div class="math-callout" style="text-align: center; font-size: 1.05rem;">
      <i>P</i>(Successful Rebuild) = ( 1 - <i>p</i><sub>error</sub> )<sup><i>B</i><sub>rebuild</sub></sup> &asymp; <i>e</i><sup>- <i>B</i><sub>rebuild</sub> &times; <i>p</i><sub>error</sub></sup>
    </div>

    <div style="background: #ffffff; border: 1px solid var(--border); border-top: 4px solid var(--danger); border-radius: 6px; padding: 16px; margin: 18px 0;">
      <h4 style="margin: 0 0 8px 0; color: #0f172a; font-size: 0.95rem;">Concrete Numerical Proof: 8-Disk Array with 16 TB Drives</h4>
      <p style="margin: 0; font-size: 0.84rem; color: #475569; line-height: 1.6;">
        Consider an 8-disk RAID 5 array populated with 16 TB consumer SATA drives (<i>p</i><sub>error</sub> = 10<sup>-14</sup>):
        <ol style="margin: 8px 0 0 16px; padding: 0; font-size: 0.82rem;">
          <li>One drive dies. To rebuild the spare, the controller must read all 7 surviving 16 TB drives:
            <div style="font-family: var(--font-mono); margin: 4px 0; color: #1e293b;">
              Total Data to Read = 7 &times; 16 TB = 112 TB = 112 &times; 10<sup>12</sup> Bytes &times; 8 = <strong>8.96 &times; 10<sup>14</sup> bits</strong>
            </div>
          </li>
          <li>Calculate the probability of reading 8.96 &times; 10<sup>14</sup> bits without a single URE:
            <div style="font-family: var(--font-mono); margin: 4px 0; color: #dc2626; font-weight: 700;">
              <i>P</i>(Survival) = ( 1 - 10<sup>-14</sup> )<sup>8.96 &times; 10<sup>14</sup></sup> &asymp; <i>e</i><sup>-8.96</sup> &asymp; <strong>0.000128 &asymp; 0.01%</strong>
            </div>
          </li>
          <li><strong>The Catastrophic Reality:</strong>
            The probability of successfully rebuilding this array is <strong>less than 0.02%</strong>! The probability of encountering a fatal URE that destroys the entire volume is <strong>99.98%</strong>!
          </li>
        </ol>
      </p>
    </div>

    <blockquote style="border-left: 4px solid var(--danger); padding: 10px 18px; margin: 18px 0; background: #fef2f2; color: #991b1b; font-size: 0.88rem;">
      <strong>The Modern Storage Law:</strong>
      Because consumer and enterprise mechanical drive capacities now routinely exceed 12 TB, <strong>RAID 5 is considered architecturally obsolete and hazardous for spinning disks</strong>. All modern enterprise storage engineering mandates <strong>RAID 6 (dual parity)</strong> or <strong>RAID 10 (mirrored striping)</strong> to ensure that secondary UREs encountered during multi-terabyte rebuilds do not destroy customer data.
    </blockquote>"""

def update_section_three():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<h3>3. Mathematical Foundations: XOR Parity &amp; The URE Rebuild Crisis</h3>"
    end_marker = "<!-- Directed Narrative Stepper: RAID Rebuild & Parity Engine -->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate Section 3 boundaries before the interactive aid.")
        return False

    updated_content = content[:start_idx] + EXPANDED_SECTION_THREE_PRE_AID + "\n\n    " + content[end_idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully expanded Section 3 in {TARGET_FILE}")
    return True

def run_git_sync():
    status = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
    if not status:
        print("--> Working tree is clean. Nothing to commit.")
        return

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 3 in Module 04 on XOR Parity Math and the URE Crisis\n\n"
            "Detail Boolean XOR invariants, Galois Field GF(2^8) Reed-Solomon math,\n"
            "Markov MTTDL modeling, and the Bernoulli probability of rebuild UREs."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if update_section_three():
        run_git_sync()
