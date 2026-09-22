#!/usr/bin/env python3
# =====================================================================
# fix.py: Generalize Section 3 in 03-os-concepts.html with correct markers
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "03-os-concepts.html"
)

NEW_FILES_SECTION = r"""    <h3>3. Files &amp; Hierarchical Directories: Diverse Paradigms</h3>
    <p>
      The <strong>file</strong> abstraction provides a persistent, named container for information that survives process termination and power outages. While contemporary developers frequently assume the Unix model—a linear, untyped byte stream anchored in a single unified directory tree—operating system history reflects fundamentally different approaches to structuring persistent storage.
    </p>

    <h4>File Structuring Models: Byte Streams vs. Record Datasets</h4>
    <p>
      Operating systems categorize the internal structure of files into three primary models:
    </p>
    <ul>
      <li><strong>Unstructured Byte Sequences (POSIX / Windows):</strong> The OS treats the file as an arbitrary sequence of 8-bit bytes. The kernel imposes no internal boundaries, record structures, or record keys; interpreting the contents is left entirely to user applications.</li>
      <li><strong>Multi-Stream &amp; Forked Files (macOS HFS / Windows NTFS):</strong> Files can house multiple discrete data streams attached to a single directory entry. Apple's classic HFS utilized a <em>Data Fork</em> (raw content) and a <em>Resource Fork</em> (compiled icons, menus, and localization strings). Similarly, NTFS supports <strong>Alternate Data Streams (ADS)</strong>, allowing metadata (such as web origin tags like <code>Zone.Identifier</code>) to adhere silently to a file.</li>
      <li><strong>Record-Oriented Datasets (IBM z/OS / MVS / VMS):</strong> The operating system defines and enforces internal record structures. Files are sequences of fixed-length (Fixed Blocked) or variable-length records. In Indexed Sequential Access Method (ISAM) or VSAM datasets, the OS kernel itself manages indexed key searches to fetch specific customer or account records without requiring database middleware.</li>
    </ul>

    <h4>Namespace Topologies: Unified Trees vs. Per-Volume Roots</h4>
    <p>
      How an operating system organizes and accesses multiple physical disk volumes varies dramatically:
    </p>
    <ul>
      <li><strong>Unified Virtual File System (POSIX / Unix):</strong> Every physical disk, network share, and pseudo-filesystem is spliced into a single root tree starting at <code>/</code> using the <code>mount</code> operation. Physical boundaries are completely transparent to userspace paths (e.g., <code>/home/user/docs</code> might reside across three distinct NVMe and NFS storage devices).</li>
      <li><strong>Drive Letters &amp; The NT Object Manager (Windows):</strong> Exposed to users as segmented per-drive root directories (<code>C:\</code>, <code>D:\</code>). Internally, the Windows NT Object Manager maintains a unified root namespace (<code>\GLOBAL??\C:</code> symlinked to <code>\Device\HarddiskVolume1</code>), with Win32 path prefixes providing compatibility.</li>
      <li><strong>Flat Cataloged Namespaces (IBM Mainframes):</strong> Traditional z/OS does not use hierarchical directory trees for datasets. Instead, datasets use dotted qualifiers (e.g., <code>USER1.COBOL.SOURCE(MAIN)</code>) tracked via a centralized system catalog (Master and User Catalogs) mapping names to volume serial identifiers (VOLSERs).</li>
    </ul>

    <!-- Diagram 3: Namespace Topologies Comparison -->
    <div style="display: flex; justify-content: center; margin: 24px 0;">
      <svg viewBox="0 0 760 260" width="100%" height="100%" style="max-width: 760px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="tree-arrow" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <polygon points="0 1, 6 3.5, 0 6" fill="#0284c7" />
          </marker>
          <filter id="box-shadow" x="-5%" y="-5%" width="110%" height="110%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.06" />
          </filter>
        </defs>

        <!-- Left: POSIX Unified Hierarchy -->
        <g transform="translate(40, 20)" filter="url(#box-shadow)">
          <rect width="320" height="220" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" />
          <rect width="320" height="28" rx="6" fill="#f0f9ff" />
          <line x1="0" y1="28" x2="320" y2="28" stroke="#bae6fd" />
          <text x="160" y="19" fill="#0369a1" font-size="10.5" font-weight="700" text-anchor="middle">POSIX Unified Namespace</text>

          <!-- Tree Nodes -->
          <circle cx="160" cy="55" r="14" fill="#0284c7" />
          <text x="160" y="60" fill="#ffffff" font-size="11" font-weight="700" text-anchor="middle">/</text>

          <line x1="148" y1="67" x2="80" y2="105" stroke="#94a3b8" stroke-width="1.5" />
          <line x1="160" y1="69" x2="160" y2="105" stroke="#94a3b8" stroke-width="1.5" />
          <line x1="172" y1="67" x2="240" y2="105" stroke="#94a3b8" stroke-width="1.5" />

          <rect x="50" y="105" width="60" height="22" rx="3" fill="#f8fafc" stroke="#cbd5e1" />
          <text x="80" y="120" fill="#334155" font-size="9" text-anchor="middle">/bin</text>

          <rect x="130" y="105" width="60" height="22" rx="3" fill="#f8fafc" stroke="#cbd5e1" />
          <text x="160" y="120" fill="#334155" font-size="9" text-anchor="middle">/etc</text>

          <rect x="210" y="105" width="60" height="22" rx="3" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" />
          <text x="240" y="120" fill="#0369a1" font-size="9" font-weight="700" text-anchor="middle">/mnt/usb</text>

          <!-- Mount boundary label -->
          <path d="M 240, 130 L 240, 160" stroke="#0284c7" stroke-dasharray="3,3" stroke-width="1.5" marker-end="url(#tree-arrow)" />
          <rect x="180" y="165" width="120" height="34" rx="4" fill="#eff6ff" stroke="#93c5fd" />
          <text x="240" y="180" fill="#1e40af" font-size="8" font-weight="700" text-anchor="middle">Volume Mounted In-Tree</text>
          <text x="240" y="192" fill="#64748b" font-size="7.5" text-anchor="middle">Seamless /dev/sdb1 splice</text>
        </g>

        <!-- Right: Windows Drive Letters / NT Namespace -->
        <g transform="translate(400, 20)" filter="url(#box-shadow)">
          <rect width="320" height="220" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
          <rect width="320" height="28" rx="6" fill="#f8fafc" />
          <line x1="0" y1="28" x2="320" y2="28" stroke="#e2e8f0" />
          <text x="160" y="19" fill="#334155" font-size="10.5" font-weight="700" text-anchor="middle">Windows NT Namespace</text>

          <!-- Independent Roots -->
          <rect x="50" y="45" width="90" height="32" rx="4" fill="#ecfdf5" stroke="#059669" stroke-width="1.2" />
          <text x="95" y="65" fill="#065f46" font-size="11" font-weight="700" text-anchor="middle">C:\ (NVMe)</text>

          <rect x="180" y="45" width="90" height="32" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.2" />
          <text x="225" y="65" fill="#92400e" font-size="11" font-weight="700" text-anchor="middle">D:\ (USB)</text>

          <line x1="95" y1="77" x2="95" y2="105" stroke="#94a3b8" stroke-width="1.5" />
          <line x1="225" y1="77" x2="225" y2="105" stroke="#94a3b8" stroke-width="1.5" />

          <rect x="40" y="105" width="110" height="22" rx="3" fill="#f8fafc" stroke="#cbd5e1" />
          <text x="95" y="120" fill="#334155" font-size="8.5" text-anchor="middle">\Windows\System32</text>

          <rect x="180" y="105" width="90" height="22" rx="3" fill="#f8fafc" stroke="#cbd5e1" />
          <text x="225" y="120" fill="#334155" font-size="8.5" text-anchor="middle">\Backups</text>

          <!-- NT Object Manager callout -->
          <rect x="30" y="150" width="260" height="50" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-dasharray="3,3" />
          <text x="160" y="168" fill="#475569" font-size="8.5" font-weight="700" text-anchor="middle">Underlying NT Object Manager:</text>
          <text x="160" y="184" fill="#0369a1" font-size="8" text-anchor="middle">\GLOBAL??\C: &rarr; \Device\HarddiskVolume1</text>
        </g>
      </svg>
    </div>

    <h4>Architectural Comparison of File System Implementations</h4>
    <div style="overflow-x: auto; margin: 16px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; background: #ffffff;">
        <thead>
          <tr style="background: #f1f5f9; color: #1e293b;">
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Design Attribute</th>
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">POSIX / Linux (ext4, XFS)</th>
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">Windows NT (NTFS, ReFS)</th>
            <th style="padding: 10px 14px; border: 1px solid #cbd5e1;">IBM Mainframes (z/OS VSAM)</th>
          </tr>
        </thead>
        <tbody style="color: #334155;">
          <tr>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">Data Model</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Unstructured byte array.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Unstructured byte array + Alternate Data Streams (ADS).</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Structured records (Fixed, Variable, or Key-Sequenced).</td>
          </tr>
          <tr style="background: #f8fafc;">
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">Metadata Container</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Index Node (<strong>inode</strong>) storing pointers to extent/block maps, size, ownership, and mode flags.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Master File Table (<strong>MFT</strong>) row storing attributes (small files fit directly inside the MFT record).</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Volume Table of Contents (<strong>VTOC</strong>) containing Data Set Control Blocks (DSCBs).</td>
          </tr>
          <tr>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">Access Security</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Classic User/Group/Other <code>rwx</code> bits + POSIX 1e ACLs.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Granular Security Descriptors (DACLs/SACLs) with inheritance.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">System Authorization Facility (SAF) / RACF profiles.</td>
          </tr>
          <tr style="background: #f8fafc;">
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">Case Sensitivity</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Strictly case-sensitive (<code>file.txt</code> &ne; <code>File.txt</code>).</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Case-preserving but case-insensitive by default in Win32.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Strictly uppercase alphanumeric characters only.</td>
          </tr>
          <tr>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0; font-weight: 600;">File Locking Semantics</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Advisory locking by default (<code>fcntl</code> / <code>flock</code>).</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Mandatory sharing/locking modes enforced on <code>CreateFile</code>.</td>
            <td style="padding: 10px 14px; border: 1px solid #e2e8f0;">Exclusive system-enforced enqueue (ENQ) locks per dataset.</td>
          </tr>
        </tbody>
      </table>
    </div>"""

def update_section_three():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Exact boundary markers matching your file content
    start_marker = "<h3>3. Files &amp; Hierarchical Directories</h3>"
    end_marker = "<h3>4. Input/Output (I/O) Subsystems</h3>"

    if start_marker not in content:
        print(f"Error: Start marker '{start_marker}' not found in {TARGET_FILE}.")
        return

    if end_marker not in content:
        print(f"Error: End marker '{end_marker}' not found in {TARGET_FILE}.")
        return

    prefix = content.split(start_marker)[0]
    suffix = content.split(end_marker)[1]

    updated_content = f"{prefix}{NEW_FILES_SECTION}\n\n    {end_marker}{suffix}"

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully replaced Section 3 in {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Expand Section 3 in Module 3 with cross-platform file system concepts\n\n"
            "Generalize Section 3 of 03-os-concepts.html across POSIX byte streams,\n"
            "Windows NTFS streams/drive letters, and IBM z/OS record datasets,\n"
            "adding a comparative table and namespace topology diagram."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for Section 3 update!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_section_three()
