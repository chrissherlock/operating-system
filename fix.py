#!/usr/bin/env python3
# =====================================================================
# fix.py: Create Module 01 on The File Abstraction in Week 10
# =====================================================================
import os
import subprocess

TARGET_DIR = "week10-file-management"
TARGET_FILE = os.path.join(TARGET_DIR, "01-files-abstraction.html")

MODULE_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Module 01: The File Abstraction - COSC240</title>
  <style>
    :root {
      --primary: #0f172a;
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --border: #e2e8f0;
      --card-bg: #ffffff;
      --text: #334155;
      --text-muted: #64748b;
      --bg: #f8fafc;
      --danger: #dc2626;
      --success: #16a34a;
      --warning: #d97706;
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: var(--font-sans);
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 24px;
    }
    .container { max-width: 1040px; margin: 0 auto; }
    .nav-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #ffffff;
      border: 1px solid var(--border);
      padding: 12px 20px;
      border-radius: 8px;
      margin-bottom: 24px;
    }
    .nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--accent);
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 6px;
      transition: background 0.15s ease;
    }
    .nav-btn:hover { background: #f0f9ff; }
    .content-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 36px;
      margin-bottom: 28px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    h1 { margin: 0 0 12px 0; font-size: 1.85rem; color: var(--primary); letter-spacing: -0.02em; }
    h3 { font-size: 1.25rem; color: var(--primary); margin-top: 28px; border-bottom: 2px solid var(--border); padding-bottom: 8px; }
    h4 { font-size: 1.05rem; color: var(--primary); margin-top: 20px; }
    p, li { font-size: 0.95rem; color: var(--text); }
    .math-callout {
      background: #f8fafc;
      border-left: 4px solid var(--accent);
      padding: 16px;
      border-radius: 0 6px 6px 0;
      margin: 18px 0;
      font-size: 0.92rem;
    }
    pre {
      background: #0f172a;
      color: #e2e8f0;
      padding: 16px;
      border-radius: 6px;
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      margin: 16px 0;
    }
    code { font-family: var(--font-mono); font-size: 0.88rem; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; color: #0f172a; }
    pre code { background: none; padding: 0; color: inherit; }

    /* Interactive Pedagogical Aid Styles */
    .aid-wrapper {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 24px;
      margin: 28px 0;
      box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .aid-header { font-weight: 700; font-size: 1.05rem; color: var(--primary); margin-bottom: 4px; }
    .aid-subtitle { font-size: 0.82rem; color: var(--text-muted); margin-bottom: 16px; }
    .aid-grid { display: grid; grid-template-columns: 280px 1fr; gap: 20px; align-items: start; }
    .controls-panel { background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 16px; }
    .preview-box { background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 14px; font-size: 0.86rem; color: var(--text); margin-bottom: 14px; line-height: 1.5; height: 150px; max-height: 150px; display: flex; flex-direction: column; justify-content: center; overflow-y: auto; }
    .stepper-btns { display: flex; gap: 8px; margin-bottom: 14px; }
    .step-btn {
      flex: 1;
      background: var(--primary);
      color: #ffffff;
      border: none;
      padding: 8px 12px;
      font-size: 0.8rem;
      font-weight: 600;
      border-radius: 4px;
      cursor: pointer;
      transition: background 0.15s;
    }
    .step-btn:hover { background: var(--accent); }
    .step-btn:disabled { background: #cbd5e1; cursor: not-allowed; }
    .telemetry-bar { background: #0f172a; color: #e2e8f0; font-family: var(--font-mono); font-size: 0.75rem; padding: 10px 12px; border-radius: 6px; margin-bottom: 14px; display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px 12px; }
    .visual-canvas { background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between; height: 100%; min-height: 240px; }
    .panes-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 16px; }
    .pane-box { background: #f8fafc; border: 1px solid var(--border); border-radius: 6px; padding: 12px 14px; font-size: 0.82rem; }
    .pane-title { font-weight: 700; font-size: 0.82rem; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.04em; }
    .toggle-bar { display: flex; gap: 8px; margin-top: 12px; padding-top: 10px; border-top: 1px solid var(--border); }
    .toggle-btn { background: #f1f5f9; border: 1px solid var(--border); padding: 4px 8px; font-size: 0.72rem; border-radius: 4px; cursor: pointer; font-weight: 600; color: var(--text-muted); }
    .toggle-btn.active { background: #e0f2fe; color: var(--accent); border-color: #bae6fd; }
    @media (max-width: 768px) {
      .aid-grid, .panes-grid { grid-template-columns: 1fr; }
      body { padding: 16px; }
    }
  </style>
  <!-- KaTeX CSS & JS CDN -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css" crossorigin="anonymous">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js" crossorigin="anonymous"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" crossorigin="anonymous" onload="renderMathInElement(document.body, { delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}] });"></script>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a href="index.html" class="nav-btn">&larr; Week 10 Hub</a>
      <a href="../index.html" class="nav-btn">&#127968; Course Index</a>
      <a href="02-directories.html" class="nav-btn">Module 02: Directories &rarr;</a>
    </nav>

    <div class="content-card">
      <span style="font-size: 0.75rem; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.05em;">Module 01 &bull; COSC240</span>
      <h1>The File Abstraction</h1>
      <p style="font-size: 1.05rem; color: var(--text-muted); margin-bottom: 24px;">
        Investigate how operating systems transform raw, physical non-volatile storage sectors into persistent, named, and structured byte streams. Examine file structures, metadata attributes, POSIX operational primitives, and the kernel's three-tier file table architecture.
      </p>

      <h3>1. Motivation: Persistence &amp; Device Virtualization</h3>
      <p>
        Process memory (the virtual address space covered in Week 07) is fundamentally <strong>ephemeral</strong>. When a process terminates, crashes, or when power drops, all state held in RAM volatile registers and dynamic page frames vanishes instantly. Furthermore, a single process's address space is strictly private; sharing vast datasets across distinct user accounts and lifetimes requires an external medium.
      </p>
      <p>
        Physical non-volatile storage hardware (such as magnetic hard disks, NVMe SSDs, and flash arrays) presents an unforgiving interface:
      </p>
      <ul>
        <li>Storage is partitioned into fixed-size physical sectors or Logical Block Addresses (LBAs, typically 512 bytes or 4 KB).</li>
        <li>Devices accept only low-level commands: read block $k$, write block $k$, erase block $k$.</li>
        <li>Storage media lack human-readable names, ownership protections, concurrency arbitration, and dynamic resizing.</li>
      </ul>
      <p>
        The <strong>File Abstraction</strong> is the fundamental operating system construct that bridges this gap. A <strong>file</strong> is a named, logical collection of persistent information recorded on secondary storage, presented to user processes as a continuous, linear address space of bytes ($0 \dots N-1$).
      </p>

      <h3>2. File Structure Models</h3>
      <p>
        Historically, operating systems have differed significantly in how much internal structure the kernel imposes upon file contents. Three canonical models define this evolution:
      </p>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin: 20px 0;">
        <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 18px;">
          <strong style="color: var(--primary); font-size: 0.98rem;">1. Byte Sequence (UNIX / Windows)</strong>
          <p style="font-size: 0.86rem; color: var(--text); margin-top: 8px; line-height: 1.5;">
            The file is an unformatted sequence of 8-bit bytes. The kernel imposes zero schema, record boundaries, or syntax:
          </p>
          <div style="font-size: 0.8rem; font-family: var(--font-mono); background: #ffffff; border: 1px solid var(--border); border-radius: 4px; padding: 6px 10px; margin-top: 8px;">
            File = [ B0, B1, B2, ..., B(N-1) ]
          </div>
          <p style="font-size: 0.82rem; color: var(--text-muted); margin-top: 8px;">
            <strong>Philosophy:</strong> The OS provides raw byte storage; application software (compilers, database engines, media players) parses semantic meaning. This approach provides maximum architectural flexibility.
          </p>
        </div>

        <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 18px;">
          <strong style="color: var(--primary); font-size: 0.98rem;">2. Record Sequence (CP/M, VMS)</strong>
          <p style="font-size: 0.86rem; color: var(--text); margin-top: 8px; line-height: 1.5;">
            The file is modeled as a sequence of fixed-length or variable-length records, reflecting 80-column punched-card heritage:
          </p>
          <div style="font-size: 0.8rem; font-family: var(--font-mono); background: #ffffff; border: 1px solid var(--border); border-radius: 4px; padding: 6px 10px; margin-top: 8px;">
            read_record() &rarr; returns Record[i]
          </div>
          <p style="font-size: 0.82rem; color: var(--text-muted); margin-top: 8px;">
            <strong>Philosophy:</strong> The kernel's file subsystem understands record delimiters. Reading returns an exact record boundary rather than an arbitrary count of bytes.
          </p>
        </div>

        <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 18px;">
          <strong style="color: var(--primary); font-size: 0.98rem;">3. Keyed Tree / ISAM (Mainframes)</strong>
          <p style="font-size: 0.86rem; color: var(--text); margin-top: 8px; line-height: 1.5;">
            The file is structured internally as a B-tree or sorted index of keyed records (e.g., IBM VSAM):
          </p>
          <div style="font-size: 0.8rem; font-family: var(--font-mono); background: #ffffff; border: 1px solid var(--border); border-radius: 4px; padding: 6px 10px; margin-top: 8px;">
            get_record("Smith") &rarr; O(log N)
          </div>
          <p style="font-size: 0.82rem; color: var(--text-muted); margin-top: 8px;">
            <strong>Philosophy:</strong> Fast key-based querying embedded into the operating system filesystem routines, common in banking mainframes before relational DBMS ubiquity.
          </p>
        </div>
      </div>

      <h3>3. Access Methods: Sequential vs. Random Access</h3>
      <p>
        Processes access files through two primary paradigms:
      </p>
      <ul>
        <li>
          <strong>Sequential Access:</strong> Bytes are read or written in strict chronological order from beginning to end ($B_0, B_1, B_2, \dots$). The kernel tracks an implicit <em>file offset pointer</em> that automatically advances with every read or write. This mirrors magnetic tape media and remains the standard for audio streams, loggers, and video playback.
        </li>
        <li>
          <strong>Random / Direct Access:</strong> The application can read or write bytes at arbitrary offsets ($B_{4096}, B_{1024}, B_{0}$) in any sequence. Essential for relational databases, virtual machine disk images, and index structures. Implemented via system calls such as <code>lseek(fd, offset, whence)</code> or positional I/O (<code>pread</code> / <code>pwrite</code>).
        </li>
      </ul>

      <h3>4. File Attributes &amp; Inode Metadata</h3>
      <p>
        In addition to raw data bytes, every file possesses associated <strong>metadata</strong> (attributes) describing its administrative and physical storage properties. In UNIX/POSIX environments, metadata is encapsulated within the <code>struct stat</code> record retrieved via the <code>stat()</code> system call:
      </p>

      <!-- Syntax-Highlighted C Struct Box -->
      <div style="background: #0f172a; color: #f8fafc; border-radius: 8px; padding: 20px; font-family: var(--font-mono); font-size: 0.84rem; overflow-x: auto; margin: 16px 0; border: 1px solid var(--border);">
        <div style="color: #64748b; margin-bottom: 10px; font-size: 0.78rem; border-bottom: 1px solid #334155; padding-bottom: 6px;">
          c &bull; posix_stat.h
        </div>
        <pre style="margin: 0; line-height: 1.5;"><span style="color: #c084fc;">struct</span> <span style="color: #6ee7b7;">stat</span> {
    <span style="color: #6ee7b7;">dev_t</span>     st_dev;         <span style="color: #94a3b8;">// ID of device containing file</span>
    <span style="color: #6ee7b7;">ino_t</span>     st_ino;         <span style="color: #94a3b8;">// File serial number (Inode Number)</span>
    <span style="color: #6ee7b7;">mode_t</span>    st_mode;        <span style="color: #94a3b8;">// File mode (type and permissions: rwxr-xr-x)</span>
    <span style="color: #6ee7b7;">nlink_t</span>   st_nlink;       <span style="color: #94a3b8;">// Number of hard links</span>
    <span style="color: #6ee7b7;">uid_t</span>     st_uid;         <span style="color: #94a3b8;">// User ID of owner</span>
    <span style="color: #6ee7b7;">gid_t</span>     st_gid;         <span style="color: #94a3b8;">// Group ID of owner</span>
    <span style="color: #6ee7b7;">off_t</span>     st_size;        <span style="color: #94a3b8;">// Total size in bytes</span>
    <span style="color: #6ee7b7;">struct timespec</span> st_atim;  <span style="color: #94a3b8;">// Time of last access (atime)</span>
    <span style="color: #6ee7b7;">struct timespec</span> st_mtim;  <span style="color: #94a3b8;">// Time of last data modification (mtime)</span>
    <span style="color: #6ee7b7;">struct timespec</span> st_ctim;  <span style="color: #94a3b8;">// Time of last status/metadata change (ctime)</span>
};</pre>
      </div>

      <div class="math-callout" style="background: #f8fafc; border-left-color: var(--accent);">
        <strong style="color: var(--primary);">Critical POSIX Distinctions:</strong>
        <br><br>
        <strong>1. <code>mtime</code> vs. <code>ctime</code>:</strong> Modification time (<code>mtime</code>) updates when file <em>data bytes</em> are written. Change time (<code>ctime</code>) updates when file <em>metadata</em> (such as permissions via <code>chmod</code> or ownership via <code>chown</code>) changes. <em>POSIX does not track creation time by default.</em>
        <br><br>
        <strong>2. The Inode Disconnect:</strong> The human-readable name of a file is <strong>not</strong> stored inside the file's inode or metadata! File names live strictly inside directory entry tables mapping strings to inode numbers ($\text{"thesis.pdf"} \to \text{Inode } 41209$).
      </div>

      <h3>5. The 3-Tier Kernel Architecture for Open Files</h3>
      <p>
        When an application executes <code>int fd = open("log.txt", O_RDWR);</code>, the operating system does not simply bind the integer file descriptor directly to a disk block. Instead, POSIX kernels coordinate <strong>three distinct layers of kernel tables</strong>:
      </p>

      <ol style="font-size: 0.92rem; line-height: 1.7;">
        <li>
          <strong>Per-Process File Descriptor Table:</strong> Each process control block (PCB) contains an array of descriptors indexed by small integers ($0, 1, 2, \dots$). Standard descriptors: $0$ (stdin), $1$ (stdout), $2$ (stderr). Each valid entry contains a pointer to an entry in the System-Wide Open File Table.
        </li>
        <li>
          <strong>System-Wide Open File Description Table:</strong> Shared across the entire operating system. Contains an entry for every active `open()` handle. Stores the <strong>current byte offset</strong>, access mode flags (read-only, write-only, append), and an active reference count.
        </li>
        <li>
          <strong>VFS Inode Table (Active Inode Cache):</strong> Contains in-memory vnodes/inodes representing actual physical files on disk. Stores file size, device identifiers, disk block pointers, and lock state.
        </li>
      </ol>

      <!-- ================================================================= -->
      <!-- INTERACTIVE PEDAGOGICAL AID: 3-TIER FILE TABLE STEPPER           -->
      <!-- ================================================================= -->
      <div class="aid-wrapper">
        <div class="aid-header">Interactive Walkthrough: 3-Tier Kernel Table Resolution &amp; I/O Operations</div>
        <div class="aid-subtitle">Trace step-by-step how a user-space read() or lseek() navigates the Per-Process FD Table, the System-Wide Open File Table, and the VFS Inode Table.</div>

        <div class="aid-grid">
          <div class="controls-panel">
            <div class="preview-box" id="vfs-preview-text">
              <strong>Step 1: File Opened.</strong> Process calls <code>open("data.bin")</code>. Kernel assigns descriptor <code>fd = 3</code> pointing to Open File Description #1 with offset = 0.
            </div>

            <div class="stepper-btns">
              <button class="step-btn" id="vfs-prev-btn" onclick="changeVfsStep(-1)" disabled>&larr; Prev</button>
              <button class="step-btn" id="vfs-next-btn" onclick="changeVfsStep(1)">Next &rarr;</button>
              <button class="step-btn" onclick="resetVfsStepper()" style="background:#64748b;">Reset</button>
            </div>

            <div class="telemetry-bar" id="vfs-telemetry-bar">
              <div><strong>Phase:</strong> <span id="vfs-tel-phase" style="color: #38bdf8;">1/4</span></div>
              <div><strong>Descriptor:</strong> <span id="vfs-tel-fd">fd = 3</span></div>
              <div><strong>Offset:</strong> <span id="vfs-tel-offset">0 bytes</span></div>
              <div><strong>Status:</strong> <span id="vfs-tel-status" style="color: #4ade80; font-weight: 700;">Open (Ready)</span></div>
            </div>

            <div class="toggle-bar">
              <span style="font-size: 0.72rem; font-weight: 700; align-self: center; color: var(--text-muted);">OPERATION:</span>
              <button class="toggle-btn active" id="vfs-btn-seq" onclick="setVfsMode('seq')">Sequential Read</button>
              <button class="toggle-btn" id="vfs-btn-seek" onclick="setVfsMode('seek')">lseek() Seek</button>
            </div>
          </div>

          <div class="visual-canvas">
            <div style="font-weight: 700; font-size: 0.82rem; margin-bottom: 6px; color: var(--primary);">Synchronized Visual Canvas &mdash; Kernel 3-Tier Indirection Pipeline</div>

            <!-- 3-Tier Architecture SVG Canvas -->
            <svg viewBox="0 0 320 200" style="width: 100%; height: 100%; min-height: 200px; background: #f8fafc; border: 1px solid var(--border); border-radius: 6px; padding: 6px;">
              <!-- Tier 1: Per-Process FD Table -->
              <rect x="10" y="25" width="70" height="150" rx="3" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" />
              <text x="45" y="18" fill="#0284c7" font-size="7" font-weight="bold" text-anchor="middle">PROCESS FD TABLE</text>
              <rect x="12" y="30" width="66" height="18" fill="#f1f5f9" stroke="#cbd5e1" />
              <text x="45" y="42" fill="#64748b" font-size="7.5" font-family="monospace" text-anchor="middle">fd 0: stdin</text>
              <rect x="12" y="52" width="66" height="18" fill="#f1f5f9" stroke="#cbd5e1" />
              <text x="45" y="64" fill="#64748b" font-size="7.5" font-family="monospace" text-anchor="middle">fd 1: stdout</text>
              <rect x="12" y="74" width="66" height="18" fill="#f1f5f9" stroke="#cbd5e1" />
              <text x="45" y="86" fill="#64748b" font-size="7.5" font-family="monospace" text-anchor="middle">fd 2: stderr</text>
              <!-- Target FD 3 -->
              <rect id="vfs-row-fd" x="12" y="96" width="66" height="22" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" />
              <text x="45" y="110" fill="#0369a1" font-size="8" font-family="monospace" font-weight="bold" text-anchor="middle">fd 3 &rarr; OFT</text>

              <!-- Arrow: FD to Open File Table -->
              <path id="vfs-arrow-1" d="M 78 107 L 115 107" fill="none" stroke="#0284c7" stroke-width="2" />

              <!-- Tier 2: System-Wide Open File Table -->
              <rect x="115" y="45" width="95" height="110" rx="3" fill="#ffffff" stroke="#d97706" stroke-width="1.5" />
              <text x="162" y="38" fill="#d97706" font-size="7" font-weight="bold" text-anchor="middle">OPEN FILE TABLE</text>
              <rect id="vfs-row-oft" x="118" y="75" width="89" height="50" rx="3" fill="#fffbeb" stroke="#d97706" stroke-width="1.5" />
              <text x="162" y="90" fill="#b45309" font-size="7.5" font-family="monospace" font-weight="bold" text-anchor="middle">Entry #1</text>
              <text id="vfs-txt-offset" x="162" y="104" fill="#0f172a" font-size="8" font-family="monospace" font-weight="bold" text-anchor="middle">Offset: 0</text>
              <text x="162" y="117" fill="#64748b" font-size="7" font-family="monospace" text-anchor="middle">Mode: O_RDONLY</text>

              <!-- Arrow: OFT to Inode Table -->
              <path id="vfs-arrow-2" d="M 210 100 L 235 100" fill="none" stroke="#d97706" stroke-width="2" />

              <!-- Tier 3: Inode Table -->
              <rect x="235" y="30" width="75" height="140" rx="3" fill="#ffffff" stroke="#16a34a" stroke-width="1.5" />
              <text x="272" y="22" fill="#16a34a" font-size="7" font-weight="bold" text-anchor="middle">VFS INODE TABLE</text>
              <rect id="vfs-row-inode" x="238" y="55" width="69" height="90" rx="3" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5" />
              <text x="272" y="70" fill="#15803d" font-size="7.5" font-family="monospace" font-weight="bold" text-anchor="middle">Inode 4120</text>
              <text x="272" y="85" fill="#64748b" font-size="7" font-family="monospace" text-anchor="middle">Size: 4096B</text>
              <text x="272" y="98" fill="#64748b" font-size="7" font-family="monospace" text-anchor="middle">Ref: 1</text>
              <rect x="242" y="106" width="61" height="14" fill="#dcfce7" stroke="#86efac" />
              <text x="272" y="116" fill="#166534" font-size="6.5" font-family="monospace" text-anchor="middle">Block #8902</text>
              <rect x="242" y="124" width="61" height="14" fill="#dcfce7" stroke="#86efac" />
              <text x="272" y="134" fill="#166534" font-size="6.5" font-family="monospace" text-anchor="middle">Block #9104</text>
            </svg>

            <div style="font-size: 0.8rem; color: var(--text-muted); text-align: center; margin-top: 8px;" id="vfs-canvas-banner">
              VFS Pipeline: <strong>Ready to step</strong>
            </div>
          </div>
        </div>

        <div class="panes-grid">
          <div class="pane-box" style="border-left: 3px solid var(--success);">
            <div class="pane-title" style="color: var(--success);">&#128269; What Is Happening</div>
            <div id="vfs-pane-what" style="color: var(--text);">Process executes open(). Descriptor 3 is allocated in the PCB table, referencing a new Open File Table entry initialized at offset 0.</div>
          </div>
          <div class="pane-box" style="border-left: 3px solid var(--accent);">
            <div class="pane-title" style="color: var(--accent);">&#9881; Why The System Does This</div>
            <div id="vfs-pane-why" style="color: var(--text);">Separating file descriptors from open file objects allows child processes across fork() to share file offsets cooperatively.</div>
          </div>
        </div>
      </div>

      <h4>Why Three Tables? The <code>fork()</code> vs. <code>open()</code> Semantics</h4>
      <p>
        The separation between Per-Process Descriptors, Open File Descriptions, and Inodes is one of the most elegant architectural designs in UNIX:
      </p>
      <ul>
        <li>
          <strong>Sharing Offset across <code>fork()</code>:</strong> When a parent process calls <code>fork()</code>, the child inherits an exact duplicate of the parent's file descriptor table. Both descriptors point to the <em>same</em> Open File Description. If the parent reads 100 bytes, the offset advances to 100; when the child subsequently reads, it reads from byte 100! This enables shell pipelines and shared logging.
        </li>
        <li>
          <strong>Independent Offsets across separate <code>open()</code> calls:</strong> If two unrelated processes independently call <code>open("data.bin")</code>, they each receive their own independent Open File Description entry with its own offset pointer, pointing to the <em>same</em> underlying VFS Inode. Both processes can read the file at their own pace without interfering with each other's offsets.
        </li>
      </ul>
    </div>

    <nav class="nav-bar">
      <a href="index.html" class="nav-btn">&larr; Week 10 Hub</a>
      <a href="../index.html" class="nav-btn">&#127968; Course Index</a>
      <a href="02-directories.html" class="nav-btn">Module 02: Directories &rarr;</a>
    </nav>
  </div>

  <script>
    let vfsStep = 1;
    const vfsTotalSteps = 4;
    let vfsMode = 'seq';

    const vfsSeqData = [
      {
        preview: "<strong>Step 1: File Opened.</strong> Process calls <code>open(\"data.bin\")</code>. Kernel allocates descriptor <code>fd = 3</code> pointing to Open File Table Entry #1 (offset = 0).",
        phase: "1/4", fd: "fd = 3", offset: "0 bytes", status: "Open (Offset 0)", statusColor: "#38bdf8",
        what: "Process requests handle for 'data.bin'. OS allocates descriptor 3. Inode 4120 referenced.",
        why: "Initializing offset to 0 prepares the file stream for sequential reading from the beginning.",
        banner: "Handle Active: <strong>Descriptor fd=3 mapped to Inode 4120 (Offset 0)</strong>",
        offsetVal: "Offset: 0"
      },
      {
        preview: "<strong>Step 2: First Read (512 Bytes).</strong> Process executes <code>read(3, buf, 512)</code>. Kernel reads bytes 0&ndash;511 from Block #8902 and advances offset to 512.",
        phase: "2/4", fd: "fd = 3", offset: "512 bytes", status: "Read 512B", statusColor: "#38bdf8",
        what: "Kernel reads 512 bytes from physical storage. Updates Open File Table offset to 512.",
        why: "Automatic offset progression frees applications from manually tracking read pointers.",
        banner: "I/O Active: <strong>Read 512 bytes &mdash; Offset auto-advanced to 512</strong>",
        offsetVal: "Offset: 512"
      },
      {
        preview: "<strong>Step 3: Second Read (1024 Bytes).</strong> Process executes <code>read(3, buf, 1024)</code>. Kernel reads bytes 512&ndash;1535 and advances offset to 1536.",
        phase: "3/4", fd: "fd = 3", offset: "1536 bytes", status: "Read 1024B", statusColor: "#4ade80",
        what: "Subsequent read begins exactly where the previous read left off. Offset advances to 1536.",
        why: "Sequential access guarantees continuous streaming without repetitive seek commands.",
        banner: "I/O Stream: <strong>Read 1024 bytes &mdash; Offset auto-advanced to 1536</strong>",
        offsetVal: "Offset: 1536"
      },
      {
        preview: "<strong>Step 4: File Closed.</strong> Process calls <code>close(3)</code>. Descriptors and Open File Table reference counts decrement; buffer caches flush.",
        phase: "4/4", fd: "Closed", offset: "1536 bytes", status: "Released", statusColor: "#16a34a",
        what: "Descriptor 3 freed in process table. Reference count in Inode decrements to 0.",
        why: "Releasing descriptors prevents kernel table exhaustion leaks.",
        banner: "Complete: <strong>File closed &mdash; Kernel structures released cleanly</strong>",
        offsetVal: "Offset: Closed"
      }
    ];

    const vfsSeekData = [
      {
        preview: "<strong>Step 1: File Opened.</strong> Process calls <code>open(\"data.bin\")</code>. Descriptor <code>fd = 3</code> allocated with initial offset = 0.",
        phase: "1/4", fd: "fd = 3", offset: "0 bytes", status: "Open (Offset 0)", statusColor: "#38bdf8",
        what: "File handle opened at offset 0.",
        why: "Default access pointer begins at position 0.",
        banner: "Handle Active: <strong>fd=3 opened at offset 0</strong>",
        offsetVal: "Offset: 0"
      },
      {
        preview: "<strong>Step 2: Arbitrary Repositioning via lseek().</strong> Process calls <code>lseek(3, 2048, SEEK_SET)</code>. Kernel sets offset directly to 2048 <em>without reading any disk blocks</em>.",
        phase: "2/4", fd: "fd = 3", offset: "2048 bytes", status: "Offset Repositioned", statusColor: "#d97706",
        what: "lseek modifies the integer offset in the Open File Table entry from 0 to 2048. Zero physical I/O occurs.",
        why: "Direct access enables instant pointer relocation without transferring unneeded intermediate data across the bus.",
        banner: "Seek Executed: <strong>Offset changed to 2048 (Zero disk I/O overhead)</strong>",
        offsetVal: "Offset: 2048"
      },
      {
        preview: "<strong>Step 3: Direct Read from Offset 2048.</strong> Process calls <code>read(3, buf, 256)</code>. Kernel accesses byte offset 2048 (Block #8902) directly.",
        phase: "3/4", fd: "fd = 3", offset: "2304 bytes", status: "Direct Read", statusColor: "#4ade80",
        what: "Kernel reads bytes 2048&ndash;2303 directly. Offset updates to 2304.",
        why: "Random access allows database engines to inspect B-tree records scattered across gigabyte files.",
        banner: "I/O Active: <strong>Direct read executed at offset 2048 &rarr; advances to 2304</strong>",
        offsetVal: "Offset: 2304"
      },
      {
        preview: "<strong>Step 4: Seek to EOF.</strong> Process calls <code>lseek(3, 0, SEEK_END)</code>. Offset moves to byte 4096 (end of file) ready for append mode.",
        phase: "4/4", fd: "fd = 3", offset: "4096 (EOF)", status: "At End of File", statusColor: "#16a34a",
        what: "Kernel inspects Inode size (4096) and updates offset to match file length.",
        why: "SEEK_END enables fast atomic appending without scanning file contents.",
        banner: "Complete: <strong>Offset positioned at EOF (4096)</strong>",
        offsetVal: "Offset: 4096"
      }
    ];

    function changeVfsStep(dir) {
      vfsStep += dir;
      if (vfsStep < 1) vfsStep = 1;
      if (vfsStep > vfsTotalSteps) vfsStep = vfsTotalSteps;
      updateVfsUI();
    }

    function resetVfsStepper() {
      vfsStep = 1;
      updateVfsUI();
    }

    function setVfsMode(mode) {
      vfsMode = mode;
      document.getElementById('vfs-btn-seq').className = (mode === 'seq') ? 'toggle-btn active' : 'toggle-btn';
      document.getElementById('vfs-btn-seek').className = (mode === 'seek') ? 'toggle-btn active' : 'toggle-btn';
      document.getElementById('vfs-btn-seq').style.background = (mode === 'seq') ? '#e0f2fe' : '#f1f5f9';
      document.getElementById('vfs-btn-seek').style.background = (mode === 'seek') ? '#e0f2fe' : '#f1f5f9';
      vfsStep = 1;
      updateVfsUI();
    }

    function updateVfsUI() {
      const dataset = (vfsMode === 'seq') ? vfsSeqData : vfsSeekData;
      const data = dataset[vfsStep - 1];

      document.getElementById('vfs-preview-text').innerHTML = data.preview;
      document.getElementById('vfs-tel-phase').innerText = data.phase;
      document.getElementById('vfs-tel-fd').innerText = data.fd;
      document.getElementById('vfs-tel-offset').innerText = data.offset;

      const statusEl = document.getElementById('vfs-tel-status');
      statusEl.innerText = data.status;
      statusEl.style.color = data.statusColor;

      document.getElementById('vfs-pane-what').innerHTML = data.what;
      document.getElementById('vfs-pane-why').innerHTML = data.why;
      document.getElementById('vfs-canvas-banner').innerHTML = data.banner;

      // Update SVG dynamic offset
      document.getElementById('vfs-txt-offset').textContent = data.offsetVal;

      document.getElementById('vfs-prev-btn').disabled = (vfsStep === 1);
      document.getElementById('vfs-next-btn').disabled = (vfsStep === vfsTotalSteps);
    }
  </script>
</body>
</html>
"""

def create_module_file_abstraction():
    os.makedirs(TARGET_DIR, exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(MODULE_CONTENT.strip() + "\n")
    print(f"--> Successfully created {TARGET_FILE}")
    return True

if __name__ == "__main__":
    if create_module_file_abstraction():
        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Create Module 01 on The File Abstraction in Week 10\n\n"
                "Implement byte sequences, record models, file attributes, 3-tier kernel\n"
                "table architecture, and an interactive POSIX VFS descriptor stepper."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully!")
        except Exception as e:
            print(f"Git note: {e}")
