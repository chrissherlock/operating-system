#!/usr/bin/env python3
import os
import subprocess
import sys

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Files &amp; Naming Abstractions — COSC240 Week 10</title>
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
      --border-dark: #94a3b8;
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --text: #0f172a;
      --text-muted: #475569;
      --inspect-color: #d97706;
      --success-color: #059669;
      --danger-color: #dc2626;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 18px;
    }
    header { text-align: center; max-width: 900px; }
    h1 { font-size: 1.8rem; color: var(--accent); margin-bottom: 6px; }
    p.subtitle { color: var(--text-muted); font-size: 0.95rem; }
    .main-container {
      display: flex;
      flex-direction: column;
      gap: 16px;
      width: 100%;
      max-width: 1100px;
    }
    .card {
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .card h2 {
      font-size: 1.25rem;
      color: var(--accent);
      border-bottom: 1px solid var(--border);
      padding-bottom: 6px;
      margin-bottom: 6px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
      margin-top: 8px;
      margin-bottom: 8px;
    }
    th, td {
      border: 1px solid var(--border);
      padding: 8px 12px;
      text-align: left;
    }
    th {
      background-color: #f1f5f9;
      color: var(--text);
      font-weight: 600;
    }
    td {
      color: #334155;
    }
    pre {
      background-color: #0f172a;
      color: #f8fafc;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      padding: 16px;
      border-radius: 6px;
      overflow-x: auto;
      line-height: 1.6;
    }
    .c-kw { color: #f472b6; font-weight: 600; }
    .c-type { color: #38bdf8; font-weight: 600; }
    .c-fn { color: #6ee7b7; font-weight: 600; }
    .c-prep { color: #c084fc; font-weight: 600; }
    .c-num { color: #fbbf24; }
    .c-comm { color: #64748b; font-style: italic; }

    /* Tour Panel Styles */
    .tour-panel {
      border: 1px solid #bae6fd;
      border-left: 5px solid var(--accent);
      background: #f0f9ff;
    }
    .tour-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .tour-title {
      font-size: 1.2rem;
      font-weight: 700;
      color: #0369a1;
    }
    .tour-body {
      font-size: 0.95rem;
      line-height: 1.6;
      color: #0c4a6e;
    }
    .telemetry-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 10px;
      margin-top: 8px;
    }
    .telemetry-box {
      background: #ffffff;
      border: 1px solid #7dd3fc;
      border-radius: 6px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .telemetry-label {
      font-size: 0.75rem;
      font-weight: 700;
      color: #0284c7;
      text-transform: uppercase;
      font-family: var(--font-mono);
    }
    .telemetry-value {
      font-size: 0.9rem;
      font-weight: 600;
      color: #0f172a;
      font-family: var(--font-mono);
    }
    .tour-nav {
      display: flex;
      gap: 10px;
      margin-top: 10px;
      align-items: center;
    }

    /* Kernel Inspector Sandbox Styles (High Contrast White on Dark) */
    .kernel-sandbox {
      background: #0f172a;
      color: #ffffff;
      border-radius: 8px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .inspector-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
    }
    .inspector-panel {
      background: #020617;
      border: 1px solid #334155;
      border-radius: 6px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      font-family: var(--font-mono);
      font-size: 0.82rem;
    }
    .inspector-title {
      font-size: 0.85rem;
      font-weight: 700;
      color: #38bdf8;
      text-transform: uppercase;
      border-bottom: 1px solid #1e293b;
      padding-bottom: 6px;
      display: flex;
      justify-content: space-between;
    }
    .inspector-row {
      display: flex;
      justify-content: space-between;
      color: #ffffff;
      padding: 3px 0;
      border-bottom: 1px dashed #1e293b;
    }
    .inspector-row span.highlight { color: #34d399; font-weight: 700; }
    .inspector-row span.alert { color: #f87171; font-weight: 700; }

    .sandbox-controls {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    button {
      background-color: var(--accent);
      color: #ffffff;
      border: none;
      padding: 8px 16px;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.9rem;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    button:hover { background-color: var(--accent-hover); }
    button.btn-secondary {
      background: #334155;
      border: 1px solid #475569;
      color: #ffffff;
    }
    button.btn-secondary:hover { background: #475569; }
    button.btn-danger { background: var(--danger-color); color: #ffffff; }
    button.btn-danger:hover { background: #b91c1c; }
    button:disabled { opacity: 0.4; cursor: not-allowed; }

    .kernel-console {
      background-color: #020617;
      color: #38bdf8;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      padding: 14px;
      border-radius: 6px;
      min-height: 90px;
      line-height: 1.5;
      white-space: pre-wrap;
      border: 1px solid #1e293b;
    }

    ul, ol {
      padding-left: 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      color: #334155;
      font-size: 0.93rem;
      line-height: 1.5;
    }
    .nav-back {
      width: 100%;
      max-width: 1100px;
      margin: 0 auto 16px auto;
      padding: 0 4px;
      display: flex;
      flex-direction: column;
    }
    .nav-back a {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      font-family: var(--font-mono);
      text-decoration: none;
      color: #0284c7;
      background-color: #f0f9ff;
      border: 1px solid #bae6fd;
      padding: 6px 12px;
      border-radius: 6px;
      transition: background-color 0.15s ease, color 0.15s ease;
      width: fit-content;
    }
    .nav-back a:hover {
      background-color: #0284c7;
      color: #ffffff;
    }

    /* State Machine Diagram Styles */
    .sm-state { transition: all 0.25s ease; }
    .sm-box { fill: #0f172a; stroke: #38bdf8; stroke-width: 2px; rx: 6px; }
    .sm-text { font-size: 10px; font-weight: 700; fill: #38bdf8; text-anchor: middle; font-family: var(--font-mono); }
    .sm-subtext { font-size: 8px; fill: #ffffff; text-anchor: middle; }
    .active-state .sm-box { fill: #0284c7; stroke: #38bdf8; stroke-width: 3px; filter: drop-shadow(0 4px 8px rgba(2,132,199,0.4)); }
    .active-state .sm-text { fill: #ffffff; }
    .active-state .sm-subtext { fill: #e0f2fe; }
  </style>
</head>
<body>
  <div class="nav-back">
    <a href="index.html">&larr; Back to Week 10 Index</a>
  </div>
  <header>
    <h1>01. Files &amp; Naming Abstractions</h1>
    <p class="subtitle">Tanenbaum Chapter 4.1: Comprehensive Reference on File Naming, Structures, Types, Access, Attributes, and POSIX System Calls.</p>
  </header>
  <div class="main-container">

    <!-- Section 4.1.1: File Naming -->
    <div class="card">
      <h2>4.1.1 File Naming</h2>
      <p>
        File naming serves as the fundamental abstraction mechanism for identifying and retrieving stored information across process boundaries. When a process creates a file, it assigns a unique name; when that process terminates, the file persists and remains accessible to other processes using that same name.
      </p>

      <div style="font-weight: 600; color: var(--text); margin-top: 4px;">Character Sets and Length Restrictions</div>
      <ul>
        <li><strong>Character Flexibility:</strong> Modern operating systems permit file names to comprise strings of letters, digits, and various special characters (such as <code>2</code>, <code>urgent!</code>, or <code>Fig.2-14</code>).</li>
        <li><strong>Historical Limits:</strong> Older operating systems, such as the legacy MS-DOS environment, severely restricted file naming conventions to an 8-character base name with a 3-character extension (the 8+3 format).</li>
        <li><strong>Modern Capacity:</strong> Contemporary file systems support extended identifiers, allowing file names of up to 255 characters or more, accommodating descriptive and structured naming schemes.</li>
      </ul>

      <div style="font-weight: 600; color: var(--text); margin-top: 4px;">Case Sensitivity Models</div>
      <ul>
        <li><strong>Case-Sensitive Systems:</strong> UNIX-based environments (including Linux and macOS) distinguish strictly between uppercase and lowercase letters. Consequently, a single directory can simultaneously house three distinct files named <code>maria</code>, <code>Maria</code>, and <code>MARIA</code>.</li>
        <li><strong>Case-Insensitive Systems:</strong> Traditional MS-DOS and legacy Windows architectures treat uppercase and lowercase characters as identical, meaning <code>maria</code> and <code>MARIA</code> reference the exact same file. While modern Windows versions support advanced file management features, they maintain backward compatibility with these legacy rules.</li>
      </ul>
    </div>

    <!-- Section 4.1.2: File Structure -->
    <div class="card">
      <h2>4.1.2 File Structure</h2>
      <p>
        File organization models dictate how the operating system or applications perceive and structure the internal layout of data within a file. Historically and across modern architectures, three primary file structures have been utilized:
      </p>
      <ol>
        <li><strong>Unstructured Sequence of Bytes:</strong> Implemented by modern operating systems including UNIX, Linux, macOS, and Windows. In this model, a file is treated simply as an arbitrary sequence of bytes. The operating system does not interpret, parse, or impose any internal structure on the contents; everything from executable binaries to plain text documents is viewed as raw bytes. Any structuring or parsing of the data (such as lines, records, or headers) is left entirely to the application software reading and writing the file.</li>
        <li><strong>Record Sequences:</strong> Modeled as a sequence of fixed-length records, each possessing its own internal structure. A read operation retrieves a complete record, while a write operation overwrites or appends an entire record. This model was heavily utilized in early mainframe and batch systems based on punch cards (structured around 80-character records) or line printers (structured around 132-character printer lines). While largely absent as a primary OS-level file model today, variations appear in specific legacy applications.</li>
        <li><strong>Key-Indexed Trees:</strong> Consists of records of varying lengths, where each record contains a specific key field. The file is maintained and sorted dynamically based on this key, allowing applications to query and retrieve records using a specific key rather than specifying a relative byte position. New records can be inserted arbitrarily, with the operating system or file management library determining their exact physical placement. This structure differs markedly from unstructured byte streams and is traditionally used in large mainframe environments for commercial data processing.</li>
      </ol>

      <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 16px; display: flex; flex-direction: column; align-items: center; gap: 10px; margin-top: 10px;">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure: Comparison of File Structures (Byte Stream vs Record Sequence vs Key-Indexed)</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 180" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <text x="20" y="25" font-size="11" font-weight="700" fill="#0284c7">1. Unstructured Byte Stream (UNIX / Windows)</text>
          <rect x="20" y="35" width="660" height="30" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" rx="4"/>
          <text x="350" y="54" font-size="11" font-family="monospace" fill="#0369a1" text-anchor="middle">B1 B2 B3 B4 B5 B6 B7 B8 B9 B10 B11 B12 ... (Raw Byte Sequence)</text>

          <text x="20" y="85" font-size="11" font-weight="700" fill="#059669">2. Record Sequence (Fixed-Length Records)</text>
          <rect x="20" y="95" width="200" height="30" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
          <text x="120" y="114" font-size="10" font-weight="600" fill="#059669" text-anchor="middle">Record 1 (e.g., 80 Bytes)</text>

          <rect x="230" y="95" width="200" height="30" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
          <text x="330" y="114" font-size="10" font-weight="600" fill="#059669" text-anchor="middle">Record 2 (e.g., 80 Bytes)</text>

          <rect x="440" y="95" width="200" height="30" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
          <text x="540" y="114" font-size="10" font-weight="600" fill="#059669" text-anchor="middle">Record 3 (e.g., 80 Bytes)</text>

          <text x="20" y="145" font-size="11" font-weight="700" fill="#d97706">3. Key-Indexed Tree (Variable-Length Sorted Records)</text>
          <rect x="20" y="155" width="140" height="20" fill="#fef3c7" stroke="#d97706" stroke-width="1" rx="3"/>
          <text x="90" y="169" font-size="9" font-weight="600" fill="#b45309" text-anchor="middle">Key: "Alpha"</text>

          <rect x="170" y="155" width="160" height="20" fill="#fef3c7" stroke="#d97706" stroke-width="1" rx="3"/>
          <text x="250" y="169" font-size="9" font-weight="600" fill="#b45309" text-anchor="middle">Key: "Beta"</text>

          <rect x="340" y="155" width="180" height="20" fill="#fef3c7" stroke="#d97706" stroke-width="1" rx="3"/>
          <text x="430" y="169" font-size="9" font-weight="600" fill="#b45309" text-anchor="middle">Key: "Gamma"</text>
        </svg>
      </div>
    </div>

    <!-- Section 4.1.3: File Types -->
    <div class="card">
      <h2>4.1.3 File Types</h2>
      <p>
        Operating systems recognize and support several distinct classifications of files. While systems like UNIX, Linux, macOS, and Windows support standard regular files and directories, UNIX architectures also provide specialized device files.
      </p>
      <ul>
        <li><strong>Regular Files:</strong> Containers that store user and system information. Regular files are broadly categorized into:
          <ul>
            <li><em>ASCII Files:</em> Consist of lines of text, where lines are terminated by carriage returns or line feed characters. Their primary advantage is that they can be displayed, printed, edited with any text editor, and easily piped together in shell pipelines.</li>
            <li><em>Binary Files:</em> Files that are not ASCII text. Displaying them directly yields unintelligible output. They possess internal structures understood by specific programs that consume them, such as executable binaries (containing magic numbers, headers, text, data, and symbol tables) or compiled module archives.</li>
          </ul>
        </li>
        <li><strong>Directories:</strong> System-managed files that maintain the hierarchical structure and organization of the file system namespace.</li>
        <li><strong>Character Special Files:</strong> Used to model serial I/O devices, such as terminals, printers, and network connections.</li>
        <li><strong>Block Special Files:</strong> Used to model disk storage drives and block-oriented peripheral devices.</li>
      </ul>

      <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 16px; display: flex; flex-direction: column; align-items: center; gap: 10px; margin-top: 10px;">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure: Operating System File Type Classifications</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 200" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <rect x="270" y="15" width="160" height="36" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" rx="6"/>
          <text x="350" y="38" font-size="11" font-weight="700" fill="#0284c7" text-anchor="middle">Operating System Files</text>

          <path d="M 350 51 L 350 75" stroke="#94a3b8" stroke-width="1.5"/>
          <path d="M 90 75 L 610 75" stroke="#94a3b8" stroke-width="1.5"/>

          <path d="M 90 75 L 90 95" stroke="#94a3b8" stroke-width="1.5"/>
          <path d="M 270 75 L 270 95" stroke="#94a3b8" stroke-width="1.5"/>
          <path d="M 450 75 L 450 95" stroke="#94a3b8" stroke-width="1.5"/>
          <path d="M 610 75 L 610 95" stroke="#94a3b8" stroke-width="1.5"/>

          <rect x="30" y="95" width="120" height="40" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" rx="4"/>
          <text x="90" y="112" font-size="10" font-weight="700" fill="#059669" text-anchor="middle">Regular Files</text>
          <text x="90" y="126" font-size="9" fill="#047857" text-anchor="middle">(ASCII / Binary)</text>

          <rect x="210" y="95" width="120" height="40" fill="#f8fafc" stroke="#334155" stroke-width="1.5" rx="4"/>
          <text x="270" y="112" font-size="10" font-weight="700" fill="#0f172a" text-anchor="middle">Directories</text>
          <text x="270" y="126" font-size="9" fill="#475569" text-anchor="middle">(Namespace Tree)</text>

          <rect x="390" y="95" width="120" height="40" fill="#fffbeb" stroke="#d97706" stroke-width="1.5" rx="4"/>
          <text x="450" y="112" font-size="10" font-weight="700" fill="#d97706" text-anchor="middle">Character Special</text>
          <text x="450" y="126" font-size="9" fill="#b45309" text-anchor="middle">(Terminals, Printers)</text>

          <rect x="550" y="95" width="120" height="40" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5" rx="4"/>
          <text x="610" y="112" font-size="10" font-weight="700" fill="#dc2626" text-anchor="middle">Block Special</text>
          <text x="610" y="126" font-size="9" fill="#b91c1c" text-anchor="middle">(Disks &amp; SSDs)</text>
        </svg>
      </div>
    </div>

    <!-- Section 4.1.4: File Access -->
    <div class="card">
      <h2>4.1.4 File Access</h2>
      <p>
        File access methods dictate how processes interact with stored data elements within a file. Operating systems have historically supported distinct access paradigms based on the underlying storage media and application demands:
      </p>
      <ul>
        <li><strong>Sequential Access:</strong> Early operating systems provided exclusively sequential access. In this model, a process was required to read all bytes or records in strict sequential order, starting from the beginning of the file. While files could be rewound to the start to allow repeated reads, skipping ahead or reading out of order was impossible. This access model was well-suited for magnetic tape storage media where sequential head traversal was mandatory.</li>
        <li><strong>Random-Access Files:</strong> With the transition from magnetic tape to magnetic disks and solid-state drives, random-access files became feasible and essential. Random-access files permit bytes or records to be read or written in any arbitrary order or accessed directly by key. Random-access files are vital for modern database management systems where specific records must be fetched instantly without scanning preceding records.</li>
      </ul>

      <div style="font-weight: 600; color: var(--text); margin-top: 4px;">Positioning Mechanisms</div>
      <p>
        To specify where read or write operations should occur within random-access files, operating systems utilize two primary design approaches:
      </p>
      <ol>
        <li><strong>Explicit Position per Operation:</strong> Every individual read or write system call includes the exact logical file position or offset as an explicit argument.</li>
        <li><strong>Separate Seek Operation:</strong> A dedicated system call (such as <code>lseek</code> in UNIX and Windows) is provided to reposition the file offset pointer. Once positioned via a seek operation, subsequent read or write calls proceed sequentially from that current offset. This latter mechanism is standard across modern UNIX and Windows operating systems.</li>
      </ol>
    </div>

    <!-- Section 4.1.5: File Attributes -->
    <div class="card">
      <h2>4.1.5 File Attributes (Metadata)</h2>
      <p>
        Every operating system associates auxiliary administrative data with each file, commonly referred to as file attributes or metadata. While the exact list of attributes varies across different operating systems, comprehensive file management requires tracking a wide array of metadata elements:
      </p>
      <ul>
        <li><strong>Protection and Ownership:</strong> Attributes controlling who may access the file and with what permissions (read, write, execute). Some systems also require a password to access specific files, while others track the creator and current owner (UID/GID).</li>
        <li><strong>Operational Flags:</strong> Bit flags that control specific file behaviors:
          <ul>
            <li><em>Hidden Flag:</em> Prevents files from appearing in standard directory listings.</li>
            <li><em>System Flag:</em> Identifies critical operating system files.</li>
            <li><em>Read-Only Flag:</em> Restricts files to read-only access.</li>
            <li><em>Archive Flag:</em> Tracks whether a file has been modified since the last backup. The backup program clears this flag, and the operating system sets it whenever the file is changed.</li>
            <li><em>ASCII / Binary Flag:</em> Designates the internal encoding format.</li>
            <li><em>Temporary Flag:</em> Marks a file for automatic deletion when the creating process terminates.</li>
            <li><em>Lock Flag:</em> Prevents concurrent access issues (nonzero when locked, zero when unlocked).</li>
          </ul>
        </li>
        <li><strong>Record and Key Metadata:</strong> For indexed or structured files, attributes include record length, key position within each record, and key length required for key-based lookups.</li>
        <li><strong>Timestamps:</strong> Tracks the exact creation time, the time of the most recent access, and the time of the last modification. These are essential for utilities like the UNIX <code>make</code> program, which inspects modification timestamps to determine the minimum compilations needed to bring software up to date.</li>
        <li><strong>Size Metrics:</strong> Tracks the current byte count of the file as well as the maximum permissible size limit.</li>
      </ul>

      <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 6px; padding: 16px; display: flex; flex-direction: column; align-items: center; gap: 10px; margin-top: 10px;">
        <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Figure: File Control Block (FCB) / I-Node Metadata Layout</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 190" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <rect x="150" y="15" width="400" height="160" fill="#f8fafc" stroke="#0284c7" stroke-width="2" rx="6"/>
          <text x="350" y="38" font-size="12" font-weight="700" fill="#0284c7" text-anchor="middle">File Control Block / I-Node Metadata Structure</text>

          <rect x="170" y="50" width="360" height="24" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1" rx="3"/>
          <text x="180" y="66" font-size="10" font-weight="600" fill="#0369a1">Protection Modes &amp; Owner UID/GID</text>

          <rect x="170" y="79" width="360" height="24" fill="#ecfdf5" stroke="#a7f3d0" stroke-width="1" rx="3"/>
          <text x="180" y="95" font-size="10" font-weight="600" fill="#047857">Flags (Hidden, Read-Only, Archive, Lock)</text>

          <rect x="170" y="108" width="360" height="24" fill="#fffbeb" stroke="#fde68a" stroke-width="1" rx="3"/>
          <text x="180" y="124" font-size="10" font-weight="600" fill="#b45309">Timestamps (Creation, Access, Modification)</text>

          <rect x="170" y="137" width="360" height="24" fill="#fef2f2" stroke="#fecaca" stroke-width="1" rx="3"/>
          <text x="180" y="153" font-size="10" font-weight="600" fill="#b91c1c">File Size &amp; Disk Block Address Pointers</text>
        </svg>
      </div>

      <table>
        <thead>
          <tr>
            <th>Attribute Category</th>
            <th>Examples</th>
            <th>Purpose / Function</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Protection &amp; Security</strong></td>
            <td>Protection modes, Owner UID/GID, Password</td>
            <td>Enforces access control lists and authorization rules.</td>
          </tr>
          <tr>
            <td><strong>Operational Flags</strong></td>
            <td>Hidden, System, Read-Only, Archive, Temporary</td>
            <td>Modifies how system tools and backup routines treat the file.</td>
          </tr>
          <tr>
            <td><strong>Temporal Metadata</strong></td>
            <td>Creation Time, Last Access Time, Last Change Time</td>
            <td>Enables dependency tracking (e.g., software build tools).</td>
          </tr>
          <tr>
            <td><strong>Structural Size</strong></td>
            <td>Current File Size, Maximum Size Limit</td>
            <td>Defines allocated bounds and tracks growth limits.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Section 4.1.6: File Operations & System Calls -->
    <div class="card">
      <h2>4.1.6 File Operations &amp; System Calls</h2>
      <p>
        Files exist to store information persistently and allow its subsequent retrieval. Operating systems provide a robust suite of system calls to facilitate file creation, manipulation, and storage management. Below is an exhaustive breakdown of the ten most common system calls related to files:
      </p>
      <ol>
        <li><strong>Create:</strong> Initializes a new, empty file with no data payload. The primary purpose of the create call is to announce to the operating system that a new file is coming into existence, allocate an initial i-node or directory entry, and establish initial attribute values (such as protection modes).</li>
        <li><strong>Delete:</strong> When a file is no longer required, this system call is invoked to remove the file from its directory structure, deallocate its i-node, and return all associated disk blocks to the free storage pool.</li>
        <li><strong>Open:</strong> Before a process can read or write a file, it must open it. The open call forces the operating system to search the directory path, locate the file's metadata and disk addresses, and load them into a fast main-memory table (such as the open file table or v-node table) for rapid access on subsequent calls. It returns a small integer called a <em>file descriptor</em>.</li>
        <li><strong>Close:</strong> When all file accesses are complete, the file should be closed to free internal table space and release kernel resources. Many operating systems enforce process-level limits on the maximum number of simultaneously open files. Furthermore, closing a file forces the operating system to flush and write out any unwritten buffered blocks residing in memory to the physical disk—even if the final block is not entirely full yet.</li>
        <li><strong>Read:</strong> Retrieves data from a file into a user-provided memory buffer. The caller must specify the file descriptor, a pointer to the destination buffer, and the exact number of bytes requested. Data is normally read starting from the current file offset pointer, which automatically advances by the number of bytes successfully read.</li>
        <li><strong>Write:</strong> Outputs data from a user-provided buffer into the file. Like read, the caller provides the file descriptor, buffer pointer, and byte count. Writing normally occurs at the current offset. If the current offset points to the end of the file, the file's size increases accordingly. If the offset is in the middle of the file, existing data is overwritten and permanently lost.</li>
        <li><strong>Append:</strong> A restricted form of write operations supported by certain operating systems. Append restricts data insertion exclusively to the end of the file, guaranteeing that existing contents cannot be accidentally overwritten regardless of the current offset pointer.</li>
        <li><strong>Seek (lseek):</strong> Essential for random-access files. Because random-access files permit reading and writing out of order, a method is required to specify the exact data offset. The seek system call repositions the file pointer to an arbitrary byte offset within the file, allowing subsequent read and write calls to execute from that specific position.</li>
        <li><strong>Get and Set Attributes:</strong> Processes frequently need to inspect or modify file metadata to perform their work. For instance, software development tools like the UNIX <code>make</code> utility examine modification timestamps across source and object files to determine the minimum compilations required. Systems provide dedicated calls to read or alter these attributes (such as changing permission masks or flags).</li>
        <li><strong>Rename:</strong> Allows a process to change a file's name within the directory hierarchy. While a file can technically be renamed by copying its contents to a new file name and deleting the original, doing so for large files (such as 50 GB archives) is prohibitively slow. A dedicated rename system call updates the directory entry instantly without moving physical data blocks.</li>
      </ol>
    </div>

    <!-- Section 3: Interactive Kernel Table Inspector & Embedded State Machine Sandbox -->
    <div class="card kernel-sandbox">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
        <div style="font-weight: 700; font-size: 1.1rem; color: #ffffff;">3. Interactive Kernel Table Inspector &amp; State Machine</div>
        <div class="sandbox-controls">
          <button onclick="inspectExec('creat')" style="font-size: 0.8rem; padding: 6px 12px;">creat()</button>
          <button onclick="inspectExec('open')" class="btn-secondary" style="font-size: 0.8rem; padding: 6px 12px;">open()</button>
          <button onclick="inspectExec('read')" class="btn-secondary" style="font-size: 0.8rem; padding: 6px 12px;">read()</button>
          <button onclick="inspectExec('write')" class="btn-secondary" style="font-size: 0.8rem; padding: 6px 12px;">write()</button>
          <button onclick="inspectExec('seek')" class="btn-secondary" style="font-size: 0.8rem; padding: 6px 12px;">lseek()</button>
          <button onclick="inspectExec('close')" class="btn-secondary btn-danger" style="font-size: 0.8rem; padding: 6px 12px;">close()</button>
        </div>
      </div>

      <!-- Detailed Instructional Breakdown -->
      <div style="background: #020617; border: 1px solid #334155; border-radius: 6px; padding: 14px; display: flex; flex-direction: column; gap: 8px; font-size: 0.88rem; color: #ffffff; line-height: 1.6;">
        <div style="font-weight: 700; color: #38bdf8; text-transform: uppercase; font-size: 0.8rem; font-family: var(--font-mono);">How to Use This Kernel Inspector &amp; What You Are Seeing:</div>
        <p style="color: #cbd5e1;">
          This interactive sandbox simulates how the operating system kernel maintains state across process boundaries during POSIX file operations. As you click system call buttons above, examine how the interface updates across three synchronized telemetry views:
        </p>
        <ul style="padding-left: 20px; display: flex; flex-direction: column; gap: 4px; color: #cbd5e1;">
          <li><strong style="color: #ffffff;">1. The State Machine Diagram (Above):</strong> Visually tracks the active lifecycle state of your file descriptor (moving from <code>UNALLOCATED</code> to <code>FD_ALLOCATED</code>, <code>OFT_BOUND</code>, and <code>RAM_CACHED</code>) in real time.</li>
          <li><strong style="color: #ffffff;">2. The Three Kernel Tables (Below):</strong>
            <ul style="padding-left: 18px; margin-top: 2px; color: #94a3b8;">
              <li><em style="color: #cbd5e1;">Process FD Table:</em> Shows private per-process file descriptor integer slots (e.g., slot <code>3</code>).</li>
              <li><em style="color: #cbd5e1;">Open File Table:</em> Tracks shared kernel telemetry including access mode flags, active reference counts, and the live byte offset pointer.</li>
              <li><em style="color: #cbd5e1;">Buffer Cache &amp; i-Node:</em> Monitors volatile RAM block residency, dirty cache status, and file size metrics before persistent disk synchronization.</li>
            </ul>
          </li>
          <li><strong style="color: #ffffff;">3. The Kernel Console &amp; Challenges (Bottom):</strong> Reports exact kernel return codes (such as success or <code>EBADF</code> faults) and lets you test real-world debugging challenges.</li>
        </ul>
      </div>

      <!-- Embedded Interactive State Machine Diagram -->
      <div style="background: #020617; border: 1px solid #1e293b; border-radius: 6px; padding: 14px; display: flex; flex-direction: column; align-items: center; gap: 6px;">
        <span style="font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: #38bdf8; text-transform: uppercase;">Live File Descriptor Lifecycle State Machine</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 120" width="100%" height="100%" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
          <g id="sm-state-0" class="sm-state active-state">
            <rect x="20" y="25" width="110" height="55" class="sm-box"/>
            <text x="75" y="48" class="sm-text">UNALLOCATED</text>
            <text x="75" y="64" class="sm-subtext">Process Closed</text>
          </g>
          <path d="M 130 52 L 180 52" stroke="#38bdf8" stroke-width="2" marker-end="url(#smarrow)"/>
          <text x="155" y="42" font-size="8" fill="#38bdf8" font-weight="600" text-anchor="middle">creat/open()</text>

          <g id="sm-state-1" class="sm-state">
            <rect x="180" y="25" width="120" height="55" class="sm-box"/>
            <text x="240" y="48" class="sm-text">FD_ALLOCATED</text>
            <text x="240" y="64" class="sm-subtext">fd slot bound</text>
          </g>
          <path d="M 300 52 L 350 52" stroke="#38bdf8" stroke-width="2" marker-end="url(#smarrow)"/>
          <text x="325" y="42" font-size="8" fill="#38bdf8" font-weight="600" text-anchor="middle">read()</text>

          <g id="sm-state-2" class="sm-state">
            <rect x="350" y="25" width="110" height="55" class="sm-box"/>
            <text x="405" y="48" class="sm-text">OFT_BOUND</text>
            <text x="405" y="64" class="sm-subtext">Offset advancing</text>
          </g>
          <path d="M 460 52 L 510 52" stroke="#38bdf8" stroke-width="2" marker-end="url(#smarrow)"/>
          <text x="485" y="42" font-size="8" fill="#38bdf8" font-weight="600" text-anchor="middle">lseek()</text>

          <g id="sm-state-3" class="sm-state">
            <rect x="510" y="25" width="110" height="55" class="sm-box"/>
            <text x="565" y="48" class="sm-text">RAM_CACHED</text>
            <text x="565" y="64" class="sm-subtext">Random Access</text>
          </g>

          <path d="M 565 80 L 565 102 L 75 102 L 75 80" fill="none" stroke="#d97706" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#smarrow-close)"/>
          <text x="320" y="112" font-size="8" fill="#fbbf24" font-weight="700" text-anchor="middle">close() [Flushes Cache &amp; Deallocates FD]</text>

          <defs>
            <marker id="smarrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8" />
            </marker>
            <marker id="smarrow-close" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#d97706" />
            </marker>
          </defs>
        </svg>
      </div>

      <!-- Side-by-Side Kernel Table Panels -->
      <div class="inspector-grid">
        <div class="inspector-panel">
          <div class="inspector-title"><span>Process FD Table</span><span>(Private)</span></div>
          <div class="inspector-row"><span>fd [0]:</span><span>stdin (keyboard)</span></div>
          <div class="inspector-row"><span>fd [1]:</span><span>stdout (terminal)</span></div>
          <div class="inspector-row"><span>fd [2]:</span><span>stderr (terminal)</span></div>
          <div class="inspector-row"><span>fd [3]:</span><span id="insp-fd3" class="alert">-- UNUSED --</span></div>
        </div>

        <div class="inspector-panel">
          <div class="inspector-title"><span>Open File Table</span><span>(Shared Kernel)</span></div>
          <div class="inspector-row"><span>Target File:</span><span id="insp-filename">None</span></div>
          <div class="inspector-row"><span>Access Flags:</span><span id="insp-flags">--</span></div>
          <div class="inspector-row"><span>Reference Count:</span><span id="insp-ref">0</span></div>
          <div class="inspector-row"><span>Byte Offset Pointer:</span><span id="insp-offset" class="highlight">0 Bytes</span></div>
        </div>

        <div class="inspector-panel">
          <div class="inspector-title"><span>Buffer Cache &amp; i-Node</span><span>(RAM / Disk)</span></div>
          <div class="inspector-row"><span>Active i-Node:</span><span id="insp-inode">None</span></div>
          <div class="inspector-row"><span>Cache Block:</span><span id="insp-block">None</span></div>
          <div class="inspector-row"><span>Buffer Status:</span><span id="insp-dirty" class="highlight">CLEAN</span></div>
          <div class="inspector-row"><span>File Size:</span><span id="insp-size">0 Bytes</span></div>
        </div>
      </div>

      <!-- Guided Debugging Challenge Panel -->
      <div style="background: #020617; border: 1px solid #1e293b; border-radius: 6px; padding: 12px; display: flex; flex-direction: column; gap: 8px;">
        <div style="font-size: 0.78rem; font-weight: 700; color: #fbbf24; text-transform: uppercase; font-family: var(--font-mono);">Guided Debugging Challenge</div>
        <div style="font-size: 0.85rem; color: #cbd5e1;" id="challengeDesc">
          <strong>Challenge 1 (The Missing Open Bug):</strong> Try clicking <code>read()</code> before initializing a file descriptor. Observe how the kernel traps invalid file descriptor references.
        </div>
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
          <button onclick="loadChallenge(1)" style="font-size: 0.72rem; padding: 4px 8px;">1. Missing Open Bug</button>
          <button onclick="loadChallenge(2)" class="btn-secondary" style="font-size: 0.72rem; padding: 4px 8px;">2. Shared Offset Trap</button>
          <button onclick="loadChallenge(3)" class="btn-secondary" style="font-size: 0.72rem; padding: 4px 8px;">3. Unflushed Cache Risk</button>
        </div>
      </div>

      <div id="inspectorConsole" class="kernel-console">$ sandbox telemetry initialized. Ready for system calls...</div>
    </div>

    <!-- Section 4.1.7: Example Program (Syntax Highlighted) -->
    <div class="card">
      <h2>4.1.7 Example: POSIX File-Copy Program</h2>
      <p>
        Below is a standard POSIX C implementation illustrating file descriptor handling, error checking, and block-by-block streaming using <code>open</code>, <code>creat</code>, <code>read</code>, <code>write</code>, and <code>close</code>:
      </p>
      <pre><span class="c-prep">#include &lt;sys/types.h&gt;</span>
<span class="c-prep">#include &lt;fcntl.h&gt;</span>
<span class="c-prep">#include &lt;stdlib.h&gt;</span>
<span class="c-prep">#include &lt;unistd.h&gt;</span>

<span class="c-prep">#define BUF_SIZE 4096</span>
<span class="c-prep">#define OUTPUT_MODE 0700</span>

<span class="c-type">int</span> <span class="c-fn">main</span>(<span class="c-type">int</span> argc, <span class="c-type">char</span> *argv[]) {
    <span class="c-type">int</span> in_fd, out_fd, rd_count, wt_count;
    <span class="c-type">char</span> buffer[BUF_SIZE];

    <span class="c-kw">if</span> (argc != <span class="c-num">3</span>) <span class="c-fn">exit</span>(<span class="c-num">1</span>); <span class="c-comm">// Syntax error</span>

    in_fd = <span class="c-fn">open</span>(argv[<span class="c-num">1</span>], O_RDONLY);
    <span class="c-kw">if</span> (in_fd &lt; <span class="c-num">0</span>) <span class="c-fn">exit</span>(<span class="c-num">2</span>); <span class="c-comm">// Source open failed</span>

    out_fd = <span class="c-fn">creat</span>(argv[<span class="c-num">2</span>], OUTPUT_MODE);
    <span class="c-kw">if</span> (out_fd &lt; <span class="c-num">0</span>) <span class="c-fn">exit</span>(<span class="c-num">3</span>); <span class="c-comm">// Destination creation failed</span>

    <span class="c-kw">while</span> (<span class="c-num">1</span>) {
        rd_count = <span class="c-fn">read</span>(in_fd, buffer, BUF_SIZE);
        <span class="c-kw">if</span> (rd_count &lt; <span class="c-num">0</span>) <span class="c-fn">exit</span>(<span class="c-num">4</span>); <span class="c-comm">// Read error</span>
        <span class="c-kw">if</span> (rd_count == <span class="c-num">0</span>) <span class="c-kw">break</span>; <span class="c-comm">// EOF reached</span>

        wt_count = <span class="c-fn">write</span>(out_fd, buffer, rd_count);
        <span class="c-kw">if</span> (wt_count &lt;= <span class="c-num">0</span>) <span class="c-fn">exit</span>(<span class="c-num">5</span>); <span class="c-comm">// Write error</span>
    }

    <span class="c-fn">close</span>(in_fd);
    <span class="c-fn">close</span>(out_fd);
    <span class="c-fn">exit</span>(<span class="c-num">0</span>);
}</pre>
    </div>

  </div>

  <script>
    let kernelState = {
      isOpen: false,
      fd: "-- UNUSED --",
      filename: "None",
      flags: "--",
      ref: 0,
      offset: 0,
      inode: "None",
      block: "None",
      dirty: "CLEAN",
      size: 0,
      stateIndex: 0
    };

    function updateInspectorUI(consoleMsg) {
      const fdEl = document.getElementById("insp-fd3");
      fdEl.textContent = kernelState.fd;
      fdEl.className = kernelState.isOpen ? "highlight" : "alert";

      document.getElementById("insp-filename").textContent = kernelState.filename;
      document.getElementById("insp-flags").textContent = kernelState.flags;
      document.getElementById("insp-ref").textContent = kernelState.ref;
      document.getElementById("insp-offset").textContent = kernelState.offset + " Bytes";
      document.getElementById("insp-inode").textContent = kernelState.inode;
      document.getElementById("insp-block").textContent = kernelState.block;

      const dirtyEl = document.getElementById("insp-dirty");
      dirtyEl.textContent = kernelState.dirty;
      dirtyEl.className = kernelState.dirty === "DIRTY" ? "alert" : "highlight";

      document.getElementById("insp-size").textContent = kernelState.size + " Bytes";
      document.getElementById("inspectorConsole").textContent = consoleMsg;

      for (let i = 0; i < 4; i++) {
        const node = document.getElementById(`sm-state-${i}`);
        if (i === kernelState.stateIndex) {
          node.classList.add('active-state');
        } else {
          node.classList.remove('active-state');
        }
      }
    }

    function inspectExec(cmd) {
      if (cmd === 'creat' || cmd === 'open') {
        kernelState.isOpen = true;
        kernelState.fd = "fd [3] (Active)";
        kernelState.filename = cmd === 'creat' ? "app.conf (New)" : "access.log";
        kernelState.flags = cmd === 'creat' ? "O_CREAT | O_WRONLY" : "O_RDWR | O_APPEND";
        kernelState.ref = 1;
        kernelState.offset = cmd === 'creat' ? 0 : 4096;
        kernelState.inode = "i-node #512";
        kernelState.block = "Block #104";
        kernelState.dirty = "CLEAN";
        kernelState.size = 256;
        kernelState.stateIndex = 1; // FD_ALLOCATED
        updateInspectorUI(`$ ${cmd}() executed.\n[Kernel] Allocated fd=3 in Process FD Table. Created Open File Table entry & loaded i-node #512 into RAM.`);
      } else if (cmd === 'read') {
        if (!kernelState.isOpen) {
          updateInspectorUI(`$ read(3, buf, 4096);\n[Fault] EBADF: Bad file descriptor! You must call open() or creat() before reading.`);
          return;
        }
        kernelState.offset += 4096;
        kernelState.stateIndex = 2; // OFT_BOUND
        updateInspectorUI(`$ read(3, buf, 4096);\n[Kernel] Buffer cache hit. Copied 4096 bytes into user space. Offset advanced to ${kernelState.offset} Bytes.`);
      } else if (cmd === 'write') {
        if (!kernelState.isOpen) {
          updateInspectorUI(`$ write(3, data, 64);\n[Fault] EBADF: Bad file descriptor! File handle is not open.`);
          return;
        }
        kernelState.offset += 64;
        kernelState.size += 64;
        kernelState.dirty = "DIRTY";
        kernelState.stateIndex = 3; // RAM_CACHED
        updateInspectorUI(`$ write(3, data, 64);\n[Kernel] Wrote 64 bytes into Block #104. Marked buffer as DIRTY. File size updated to ${kernelState.size} Bytes.`);
      } else if (cmd === 'seek') {
        if (!kernelState.isOpen) {
          updateInspectorUI(`$ lseek(3, 0, SEEK_SET);\n[Fault] EBADF: Bad file descriptor!`);
          return;
        }
        kernelState.offset = 0;
        kernelState.stateIndex = 2; // OFT_BOUND
        updateInspectorUI(`$ lseek(3, 0, SEEK_SET);\n[Kernel] Repositioned logical byte offset pointer to 0 Bytes. Zero disk I/O triggered.`);
      } else if (cmd === 'close') {
        if (!kernelState.isOpen) {
          updateInspectorUI(`$ close(3);\n[Fault] EBADF: File descriptor 3 is already closed or inactive.`);
          return;
        }
        const flushed = kernelState.dirty === "DIRTY";
        kernelState.isOpen = false;
        kernelState.fd = "-- UNUSED --";
        kernelState.filename = "None";
        kernelState.flags = "--";
        kernelState.ref = 0;
        kernelState.offset = 0;
        kernelState.inode = "None";
        kernelState.block = "None";
        kernelState.dirty = "CLEAN";
        kernelState.stateIndex = 0; // UNALLOCATED
        updateInspectorUI(`$ close(3);\n[Kernel] ${flushed ? "Flushed DIRTY buffer cache blocks to physical disk." : ""} Released fd=3 and deallocated Open File Table entry.`);
      }
    }

    function loadChallenge(id) {
      const desc = document.getElementById("challengeDesc");
      if (id === 1) {
        desc.innerHTML = "<strong>Challenge 1 (The Missing Open Bug):</strong> Try clicking <code>read()</code> right now without opening a file. Notice how the kernel immediately catches the fault.";
        inspectExec('close');
      } else if (id === 2) {
        desc.innerHTML = "<strong>Challenge 2 (The Shared Offset Trap):</strong> Click <code>open()</code>, then call <code>read()</code> to advance the offset. Notice how the offset pointer ticks upward. In real multi-process systems, shared open file tables cause coupled offsets!";
        inspectExec('open');
      } else if (id === 3) {
        desc.innerHTML = "<strong>Challenge 3 (The Unflushed Cache Risk):</strong> Click <code>write()</code> to make the buffer <strong>DIRTY</strong>. Then notice how calling <code>close()</code> automatically flushes the volatile RAM cache to disk.";
        inspectExec('open');
        setTimeout(() => inspectExec('write'), 200);
      }
    }
  </script>
</body>
</html>
"""

COMMIT_MSG = """Fix contrast and add clear instructional guide to inspector sandbox

Update week10-file-management/01-files-abstraction.html to fix color contrast
issues on dark panels and add comprehensive, step-by-step instructions
explaining the kernel inspector and state machine widgets."""

def run_git_step(cmd, desc):
    print(f"--> {desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout.strip():
        print(res.stdout.strip())
    if res.stderr.strip():
        print(f"[{desc} stderr]\n{res.stderr.strip()}")
    if res.returncode != 0:
        print(f"Error during {desc} (code {res.returncode})", file=sys.stderr)
        sys.exit(res.returncode)

def execute_pipeline():
    target_dir = "week10-file-management"
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, "01-files-abstraction.html")

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Wrote module file with high-contrast guide to {target_file}")

    run_git_step(["git", "add", target_file], "Staging high-contrast guide update 01-files-abstraction.html")
    run_git_step(["git", "commit", "-a", "-m", COMMIT_MSG], "Committing changes")
    run_git_step(["git", "push", "origin", "main"], "Pushing main to origin")
    print("--> High-Contrast Guide Module 01 created, committed, and pushed successfully!")

if __name__ == "__main__":
    execute_pipeline()
