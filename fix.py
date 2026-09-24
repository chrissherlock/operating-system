#!/usr/bin/env python3
# =====================================================================
# fix.py: Add Windows I/O model and IRP architecture to Module 01
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling",
    "01-io-hardware-device-controllers.html"
)

WINDOWS_IO_SECTION = r"""    <h4>The Windows Contrast: Object Namespace, DeviceIoControl, and IRPs</h4>
    <p>
      While Unix and POSIX adhere to the design tenet <em>"everything is a file"</em>, Windows NT implements a fundamentally different abstraction: <strong>"everything is an executive object"</strong>.
    </p>
    <p>
      In Windows, peripheral devices do not exist as special filesystem inode nodes within a root mount directory (like <code>/dev/sda</code> or <code>/dev/ttyS0</code>). Instead, the <strong>Windows Object Manager</strong> maintains an internal, kernel-level hierarchical object directory namespace:
    </p>
    <ul>
      <li>Kernel hardware devices reside under the internal <code>\Device\</code> directory (e.g. <code>\Device\Harddisk0\DR0</code> or <code>\Device\Serial0</code>).</li>
      <li>Because user-space Win32 applications cannot access the <code>\Device\</code> namespace directly, device drivers create <strong>Symbolic Links</strong> inside the <code>\DosDevices\</code> (or <code>\??\</code>) directory, exposing devices through the Win32 device namespace using the <strong><code>\\.\</code> prefix</strong>.</li>
    </ul>

    <!-- Structural Diagram: POSIX vs Windows I/O Subsystem Architecture -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 1.0b: POSIX Direct File Descriptor Path vs. Windows Layered IRP Pipeline</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">How Unix dispatches directly through driver function pointers while Windows routes I/O Request Packets through layered driver stacks.</div>

      <svg viewBox="0 0 760 270" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="win-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="win-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
          <marker id="win-arr-purple" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#7c3aed" />
          </marker>
        </defs>

        <!-- Left: POSIX Model -->
        <g transform="translate(20, 20)">
          <rect width="330" height="230" rx="8" fill="#f8fafc" stroke="#0284c7" stroke-width="1.5"/>
          <text x="165" y="24" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0284c7">POSIX / LINUX I/O MODEL</text>
          <text x="165" y="38" text-anchor="middle" font-size="7.5" fill="#64748b">Direct Call &bull; Synchronous In-Thread Dispatch</text>

          <rect x="20" y="50" width="290" height="34" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="30" y="66" font-size="8" font-weight="700" fill="#334155">USER SPACE: int fd = open("/dev/nvme0n1", ...);</text>
          <text x="30" y="77" font-family="var(--font-mono)" font-size="7.5" fill="#0284c7">read(fd, buf, len); ioctl(fd, NVME_CMD, ...);</text>

          <line x1="165" y1="84" x2="165" y2="102" stroke="#0284c7" stroke-width="2" marker-end="url(#win-arr-blue)"/>

          <rect x="20" y="104" width="290" height="42" rx="4" fill="#e0f2fe" stroke="#0284c7"/>
          <text x="30" y="120" font-size="8" font-weight="700" fill="#0369a1">VFS &amp; BLOCK LAYER (VFS Inode Indexing)</text>
          <text x="30" y="134" font-size="7.5" fill="#0284c7">Resolves file struct &rarr; file_operations table</text>

          <line x1="165" y1="146" x2="165" y2="164" stroke="#0284c7" stroke-width="2" marker-end="url(#win-arr-blue)"/>

          <rect x="20" y="166" width="290" height="45" rx="4" fill="#ffffff" stroke="#94a3b8"/>
          <text x="30" y="182" font-size="8" font-weight="700" fill="#0f172a">DEVICE DRIVER: struct file_operations</text>
          <text x="30" y="196" font-family="var(--font-mono)" font-size="7.5" fill="#475569">.read = nvme_read, .unlocked_ioctl = nvme_ioctl</text>
        </g>

        <!-- Right: Windows NT Model -->
        <g transform="translate(390, 20)">
          <rect width="350" height="230" rx="8" fill="#f8fafc" stroke="#059669" stroke-width="1.5"/>
          <text x="175" y="24" text-anchor="middle" font-size="10.5" font-weight="700" fill="#059669">WINDOWS NT I/O SUBSYSTEM</text>
          <text x="175" y="38" text-anchor="middle" font-size="7.5" fill="#64748b">Packet-Driven &bull; Layered Driver Stack</text>

          <rect x="20" y="50" width="310" height="34" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="30" y="66" font-size="8" font-weight="700" fill="#334155">USER SPACE: CreateFileW(L"\\\\.\\PhysicalDrive0", ...);</text>
          <text x="30" y="77" font-family="var(--font-mono)" font-size="7.5" fill="#059669">ReadFile(...); DeviceIoControl(hDev, FSCTL_..., ...);</text>

          <line x1="175" y1="84" x2="175" y2="102" stroke="#059669" stroke-width="2" marker-end="url(#win-arr-green)"/>

          <rect x="20" y="104" width="310" height="42" rx="4" fill="#dcfce7" stroke="#16a34a"/>
          <text x="30" y="120" font-size="8" font-weight="700" fill="#166534">I/O MANAGER: Allocates IRP Object</text>
          <text x="30" y="134" font-size="7.5" fill="#15803d">Creates I/O Request Packet with per-driver stack locations</text>

          <line x1="175" y1="146" x2="175" y2="164" stroke="#059669" stroke-width="2" marker-end="url(#win-arr-green)"/>

          <!-- Layered Driver Stack -->
          <rect x="20" y="166" width="310" height="45" rx="4" fill="#ffffff" stroke="#94a3b8"/>
          <text x="30" y="182" font-size="8" font-weight="700" fill="#0f172a">LAYERED DRIVER STACK (Class &rarr; Port &rarr; Miniport)</text>
          <text x="30" y="196" font-size="7.5" fill="#475569">Volume Manager &rarr; Disk.sys &rarr; Storport.sys &rarr; NVMe Driver</text>
        </g>
      </svg>
    </div>

    <h4>Interfacing with Hardware in Win32: CreateFile and Device Namespaces</h4>
    <p>
      To communicate with block drives, serial ports, or volume controllers in Windows, user applications call <strong><code>CreateFileW</code></strong> using specialized device namespace syntax:
    </p>
    <ul>
      <li><strong>Physical Block Storage:</strong> <code>L"\\\\.\\PhysicalDrive0"</code> opens the raw physical disk directly (analogous to <code>/dev/sda</code> in Linux).</li>
      <li><strong>Volume Partitions:</strong> <code>L"\\\\.\\C:"</code> opens the volume partition container directly (analogous to <code>/dev/sda1</code>).</li>
      <li><strong>Character Ports:</strong> <code>L"\\\\.\\COM1"</code> opens physical serial UART port 1 (analogous to <code>/dev/ttyS0</code>).</li>
      <li><strong>Console Streams:</strong> <code>L"CONIN$"</code> and <code>L"CONOUT$"</code> access the raw keyboard input and display output buffers (analogous to <code>/dev/stdin</code> and <code>/dev/stdout</code>).</li>
    </ul>

    <pre><code><span class="syn-cmt">/* Interfacing with Raw Hardware in Windows via Win32 */</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;windows.h&gt;</span>
<span class="syn-kw">#include</span> <span class="syn-str">&lt;winioctl.h&gt;</span>

<span class="syn-cmt">/* 1. Open raw physical disk block device */</span>
HANDLE hDisk = <span class="syn-fn">CreateFileW</span>(
    <span class="syn-str">L"\\\\.\\PhysicalDrive0"</span>,
    GENERIC_READ | GENERIC_WRITE,
    FILE_SHARE_READ | FILE_SHARE_WRITE,
    NULL,
    OPEN_EXISTING,
    FILE_FLAG_NO_BUFFERING | FILE_FLAG_WRITE_THROUGH, <span class="syn-cmt">/* O_DIRECT equivalent */</span>
    NULL
);

<span class="syn-cmt">/* 2. Read physical block into aligned memory */</span>
BYTE buffer[<span class="syn-num">4096</span>];
DWORD bytesRead;
<span class="syn-fn">ReadFile</span>(hDisk, buffer, <span class="syn-kw">sizeof</span>(buffer), &amp;bytesRead, NULL);</code></pre>

    <h4>The Out-of-Band Escape Hatch: ioctl() vs. DeviceIoControl()</h4>
    <p>
      In Section 1, we examined how Unix systems use <code>ioctl()</code> to send device-specific control commands. The Windows direct architectural equivalent is <strong><code>DeviceIoControl()</code></strong>:
    </p>

    <pre><code><span class="syn-kw">BOOL</span> DeviceIoControl(
    HANDLE          hDevice,              <span class="syn-cmt">/* Handle returned by CreateFile */</span>
    <span class="syn-kw">DWORD</span>           dwIoControlCode,      <span class="syn-cmt">/* Structured 32-bit IOCTL code */</span>
    <span class="syn-kw">LPVOID</span>          lpInBuffer,           <span class="syn-cmt">/* Input parameter buffer */</span>
    <span class="syn-kw">DWORD</span>           nInBufferSize,        <span class="syn-cmt">/* Size of input buffer */</span>
    <span class="syn-kw">LPVOID</span>          lpOutBuffer,          <span class="syn-cmt">/* Output data buffer */</span>
    <span class="syn-kw">DWORD</span>           nOutBufferSize,       <span class="syn-cmt">/* Size of output buffer */</span>
    <span class="syn-kw">LPDWORD</span>         lpBytesReturned,      <span class="syn-cmt">/* Bytes populated by driver */</span>
    LPOVERLAPPED    lpOverlapped          <span class="syn-cmt">/* Asynchronous I/O structure */</span>
);</code></pre>

    <div class="math-callout">
      <strong>Engineering Contrast: Why DeviceIoControl is Structurally Safer than Unix ioctl()</strong>
      <br>
      Unix <code>ioctl()</code> accepts a single untyped variadic pointer (<code>...</code>), which is notoriously vulnerable to buffer overflow vulnerabilities, pointer confusion, and architecture mismatch bugs (e.g. 32-bit user space calling 64-bit kernel).
      <br><br>
      In contrast, Windows <strong><code>DeviceIoControl</code> enforces a strict typed contract</strong>:
      <ol>
        <li><strong>Structured 32-bit Control Code:</strong> Every <code>dwIoControlCode</code> (built with the <code>CTL_CODE</code> macro) encodes:
          <ul>
            <li><em>Device Type</em> (16 bits, e.g. <code>FILE_DEVICE_DISK</code>, <code>FILE_DEVICE_NETWORK</code>).</li>
            <li><em>Required Access</em> (2 bits: Read, Write, or Any). The I/O Manager rejects calls before reaching the driver if the caller lacks permission.</li>
            <li><em>Transfer Method</em> (2 bits: <code>METHOD_BUFFERED</code>, <code>METHOD_IN_DIRECT</code>, <code>METHOD_OUT_DIRECT</code>, or <code>METHOD_NEITHER</code>), instructing the kernel how to lock and validate memory buffers automatically.</li>
          </ul>
        </li>
        <li><strong>Separate Input and Output Buffers:</strong> Input parameters (command arguments) and output payloads (sensor readings, disk geometry metadata) use independent, bounds-checked buffers with explicit size parameters verified by the I/O Manager.</li>
      </ol>
    </div>

    <h4>The Core Architectural Difference: The I/O Request Packet (IRP)</h4>
    <p>
      The deepest divergence between POSIX and Windows NT lies in how requests travel through the operating system:
    </p>
    <ul>
      <li>
        <strong>POSIX (Call-Based):</strong> In Unix, a system call typically executes synchronously down through the Virtual File System (VFS) and directly invokes driver callbacks in the calling thread's context. The thread descends into kernel space, reaches the driver, and blocks or returns.
      </li>
      <li>
        <strong>Windows NT (Packet-Driven):</strong> In Windows, <strong>all I/O operations are packet-based and natively asynchronous</strong>.
        <br>
        When an application issues <code>ReadFile</code> or <code>DeviceIoControl</code>, the Windows <strong>I/O Manager</strong> allocates an <strong>I/O Request Packet (IRP)</strong> from a non-paged kernel pool:
        <ul>
          <li>An IRP is an independent, dynamic data structure containing operational metadata, caller credentials, buffer pointers, and an array of <strong>I/O Stack Locations</strong> (<code>IO_STACK_LOCATION</code>).</li>
          <li>Each layer in a driver stack (e.g., File System Filter Driver &rarr; File System Driver &rarr; Volume Manager &rarr; Disk Class Driver &rarr; Storage Port Driver) receives its own dedicated stack location in the IRP.</li>
          <li>A driver inspects its parameters, performs its work, and either passes the IRP down to the next lower driver via <code>IoCallDriver()</code> or completes it via <code>IoCompleteRequest()</code>.</li>
          <li>Because the request is self-contained in a discrete packet, <strong>the calling thread never needs to block inside the driver</strong>. The driver can enqueue the IRP onto an asynchronous hardware queue and return immediately!</li>
        </ul>
      </li>
    </ul>

    <h4>Asynchronous Completion: POSIX epoll/io_uring vs. Windows IOCP</h4>
    <p>
      Because Windows was designed from inception around packet-driven asynchronous I/O, its multi-threaded scalability model differs markedly from Unix:
    </p>

    <div style="overflow-x: auto; margin: 18px 0;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid var(--border);">
            <th style="padding: 10px 12px; width: 22%;">Dimension</th>
            <th style="padding: 10px 12px; width: 39%;">POSIX / Linux</th>
            <th style="padding: 10px 12px; width: 39%;">Windows NT</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Device Addressing</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">Filesystem path: /dev/sda, /dev/ttyS0</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">Device namespace: \\.\PhysicalDrive0, \\.\COM1</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Device Control Hook</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">ioctl(fd, request, ...)</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">DeviceIoControl(h, code, in, in_len, out, out_len, ...)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Driver Request Model</td>
            <td style="padding: 10px 12px;">Direct function pointers (file_operations)</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 600;">Packet-driven: I/O Request Packets (IRPs)</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 10px 12px; font-weight: 700;">Asynchronous Paradigm</td>
            <td style="padding: 10px 12px;"><strong>Readiness-based:</strong> epoll notifies when fd is ready to read without blocking (io_uring modernizes to submission/completion rings).</td>
            <td style="padding: 10px 12px; color: #059669; font-weight: 600;"><strong>Completion-based:</strong> Overlapped I/O executes in background; notifies only after data is transferred into RAM.</td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border); background: #f0fdf4;">
            <td style="padding: 10px 12px; font-weight: 700; color: #166534;">High-Concurrency Engine</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">epoll_wait() / io_uring_enter()</td>
            <td style="padding: 10px 12px; font-family: var(--font-mono); font-size: 0.82rem;">I/O Completion Ports (IOCP) via GetQueuedCompletionStatus()</td>
          </tr>
        </tbody>
      </table>
    </div>"""

def integrate_windows_io():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    target_marker = "<h3>2. Device Controllers: The Electronic Bridge</h3>"
    if target_marker not in content:
        print("Error: Could not locate Section 2 marker in Module 01.")
        return False

    if "The Windows Contrast: Object Namespace, DeviceIoControl, and IRPs" in content:
        print("Notice: Windows section already exists in Module 01. Skipping.")
        return True

    idx = content.find(target_marker)
    updated_content = content[:idx] + WINDOWS_IO_SECTION + "\n\n    " + content[idx:]

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully integrated Windows I/O and IRP architecture into {TARGET_FILE}")
    return True

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add Windows I/O model and IRP architecture comparison to Module 01\n\n"
            "Contrast POSIX /dev and ioctl with Win32 CreateFile, DeviceIoControl,\n"
            "layered Driver Objects, I/O Request Packets (IRPs), and IOCP completion."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    if integrate_windows_io():
        run_git_sync()
