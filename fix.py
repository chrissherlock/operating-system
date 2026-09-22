#!/usr/bin/env python3
# =====================================================================
# fix.py: Rebuild cross-architecture I/O stepper canvas in Module 4
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "04-os-structure.html"
)

REBUILT_STEPPER_HTML = r"""    <!-- INTERACTIVE PEDAGOGICAL AID: DIRECTED NARRATIVE STEPPER -->
    <div id="interactive-os-stepper" style="margin: 36px 0; border: 1px solid #cbd5e1; border-radius: 8px; background: #ffffff; padding: 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 16px;">
        <div>
          <h3 style="margin: 0; color: #0284c7; font-size: 1.25rem;">Interactive Simulator: Cross-Architecture I/O Request Stepper</h3>
          <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Scenario: Application issues read() to fetch 4 KiB from an NVMe SSD across OS architectures.</p>
        </div>

        <!-- Comparative Dimension Toggles -->
        <div style="display: flex; gap: 6px;">
          <button type="button" class="arch-toggle active" data-arch="monolithic" style="padding: 6px 12px; font-size: 0.8rem; font-weight: 700; border-radius: 4px; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; cursor: pointer;">Monolithic</button>
          <button type="button" class="arch-toggle" data-arch="microkernel" style="padding: 6px 12px; font-size: 0.8rem; font-weight: 700; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">Microkernel</button>
          <button type="button" class="arch-toggle" data-arch="hybrid" style="padding: 6px 12px; font-size: 0.8rem; font-weight: 700; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">Hybrid (NT)</button>
          <button type="button" class="arch-toggle" data-arch="exokernel" style="padding: 6px 12px; font-size: 0.8rem; font-weight: 700; border-radius: 4px; border: 1px solid #cbd5e1; background: #ffffff; color: #475569; cursor: pointer;">Exokernel</button>
        </div>
      </div>

      <!-- Live State Telemetry Status Bar -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 14px; margin-bottom: 18px; font-family: var(--font-mono); font-size: 0.8rem;">
        <div><span style="color: #64748b;">EXECUTION MODE:</span> <strong id="telemetry-mode" style="color: #0284c7;">USER MODE (RING 3)</strong></div>
        <div><span style="color: #64748b;">ACTIVE COMPONENT:</span> <strong id="telemetry-component" style="color: #059669;">APPLICATION RUNTIME</strong></div>
        <div><span style="color: #64748b;">CONTEXT SWITCHES:</span> <strong id="telemetry-switches" style="color: #475569;">0</strong></div>
        <div><span style="color: #64748b;">COMMUNICATION:</span> <strong id="telemetry-comm" style="color: #475569;">LOCAL CALL</strong></div>
      </div>

      <!-- Synchronized Visual Canvas -->
      <div style="display: flex; justify-content: center; background: #ffffff; border: 1px solid #f1f5f9; border-radius: 6px; padding: 12px; margin-bottom: 18px;">
        <svg id="arch-stepper-svg" viewBox="0 0 820 370" width="100%" height="100%" style="max-width: 820px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="arch-arrow-default" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
              <polygon points="0 1, 6 3.5, 0 6" fill="#94a3b8" />
            </marker>
            <marker id="arch-arrow-active" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
              <polygon points="0 1, 6 3.5, 0 6" fill="#0284c7" />
            </marker>
            <filter id="arch-active-glow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#0284c7" flood-opacity="0.6" />
            </filter>
          </defs>

          <!-- Ring 3 Boundary Zone (Top) -->
          <rect x="10" y="15" width="800" height="150" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-dasharray="4,4" />
          <text x="25" y="34" fill="#64748b" font-size="8.5" font-weight="700">USER MODE (RING 3 - UNPRIVILEGED)</text>

          <!-- Ring 0 Boundary Zone (Bottom) -->
          <rect x="10" y="180" width="800" height="175" rx="6" fill="#f0fdf4" stroke="#86efac" stroke-dasharray="4,4" />
          <text x="25" y="198" fill="#15803d" font-size="8.5" font-weight="700">KERNEL / SUPERVISOR MODE (RING 0 - PRIVILEGED)</text>

          <!-- Node 1: User Application (Ring 3) -->
          <g id="box-app" transform="translate(30, 50)">
            <rect width="130" height="85" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.8" />
            <text x="65" y="32" fill="#0f172a" font-size="10.5" font-weight="700" text-anchor="middle">User App</text>
            <text id="label-app-sub" x="65" y="50" fill="#64748b" font-size="8" text-anchor="middle">read(fd, buf)</text>
            <text x="65" y="68" fill="#0284c7" font-size="7.5" font-weight="600" text-anchor="middle">PID 4092</text>
          </g>

          <!-- Node 2: User-Space OS Service / LibOS (Ring 3) -->
          <g id="box-userservice" transform="translate(200, 50)">
            <rect width="165" height="85" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.8" />
            <text id="label-userservice-title" x="82" y="30" fill="#0f172a" font-size="10" font-weight="700" text-anchor="middle">User Service</text>
            <text id="label-userservice-sub" x="82" y="48" fill="#64748b" font-size="8" text-anchor="middle">Inactive in Monolithic</text>
            <rect id="badge-userservice" x="25" y="58" width="115" height="18" rx="3" fill="#f1f5f9" stroke="#cbd5e1" />
            <text id="label-userservice-badge" x="82" y="70" fill="#475569" font-size="7.5" text-anchor="middle">POSIX Library</text>
          </g>

          <!-- Node 3: User-Space Driver (Used in Microkernel) -->
          <g id="box-userdriver" transform="translate(410, 50)">
            <rect width="165" height="85" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.8" />
            <text id="label-userdriver-title" x="82" y="30" fill="#0f172a" font-size="10" font-weight="700" text-anchor="middle">User Driver</text>
            <text id="label-userdriver-sub" x="82" y="48" fill="#64748b" font-size="8" text-anchor="middle">Ring 3 Server</text>
            <rect id="badge-userdriver" x="25" y="58" width="115" height="18" rx="3" fill="#f1f5f9" stroke="#cbd5e1" />
            <text id="label-userdriver-badge" x="82" y="70" fill="#475569" font-size="7.5" text-anchor="middle">Capability MMIO</text>
          </g>

          <!-- Node 4: Kernel Core / Executive (Ring 0) -->
          <g id="box-kernel" transform="translate(200, 220)">
            <rect width="165" height="95" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.8" />
            <text id="label-kernel-title" x="82" y="30" fill="#0f172a" font-size="10" font-weight="700" text-anchor="middle">Kernel Core</text>
            <text id="label-kernel-sub" x="82" y="48" fill="#64748b" font-size="8" text-anchor="middle">VFS &amp; Subsystems</text>
            <rect id="badge-kernel" x="20" y="62" width="125" height="20" rx="3" fill="#ecfdf5" stroke="#a7f3d0" />
            <text id="label-kernel-badge" x="82" y="75" fill="#065f46" font-size="7.5" font-weight="600" text-anchor="middle">Ring 0 Supervisor</text>
          </g>

          <!-- Node 5: Kernel Device Driver (Ring 0 - Monolithic / Hybrid) -->
          <g id="box-kerneldriver" transform="translate(410, 220)">
            <rect width="165" height="95" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.8" />
            <text id="label-kerneldriver-title" x="82" y="30" fill="#0f172a" font-size="10" font-weight="700" text-anchor="middle">NVMe Driver</text>
            <text id="label-kerneldriver-sub" x="82" y="48" fill="#64748b" font-size="8" text-anchor="middle">Ring 0 Driver Module</text>
            <rect id="badge-kerneldriver" x="20" y="62" width="125" height="20" rx="3" fill="#ecfdf5" stroke="#a7f3d0" />
            <text id="label-kerneldriver-badge" x="82" y="75" fill="#065f46" font-size="7.5" font-weight="600" text-anchor="middle">Direct Bus Master</text>
          </g>

          <!-- Node 6: Physical NVMe Storage Hardware -->
          <g id="box-hardware" transform="translate(640, 130)">
            <rect width="145" height="110" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" />
            <rect width="145" height="24" rx="6" fill="#f8fafc" />
            <text x="72" y="16" fill="#475569" font-size="8.5" font-weight="700" text-anchor="middle">PHYSICAL DEVICE</text>
            <text x="72" y="50" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">NVMe SSD</text>
            <text x="72" y="68" fill="#64748b" font-size="8" text-anchor="middle">PCIe Gen4 x4 Bus</text>
            <rect x="15" y="80" width="115" height="20" rx="3" fill="#fef3c7" stroke="#fde68a" />
            <text x="72" y="93" fill="#92400e" font-size="7.5" font-weight="600" text-anchor="middle">Flash NAND Blocks</text>
          </g>

          <!-- Connecting Paths -->
          <!-- P1: App -> Kernel Syscall Trap -->
          <path id="path-app-kernel-trap" d="M 95,135 L 95,265 L 195,265" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arch-arrow-default)" />

          <!-- P2: App -> User Service (IPC / LibOS) -->
          <path id="path-app-userservice" d="M 160,92 L 195,92" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arch-arrow-default)" />

          <!-- P3: User Service -> Kernel (IPC / Cap Trap) -->
          <path id="path-userservice-kernel" d="M 282,135 L 282,215" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arch-arrow-default)" />

          <!-- P4: Kernel -> User Driver (Microkernel Driver IPC) -->
          <path id="path-kernel-userdriver" d="M 365,245 C 440,245 440,165 440,140" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arch-arrow-default)" />

          <!-- P5: Kernel -> Kernel Driver (Monolithic / Hybrid Direct Call) -->
          <path id="path-kernel-driver" d="M 365,265 L 405,265" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arch-arrow-default)" />

          <!-- P6: Kernel Driver -> Hardware (MMIO Doorbell) -->
          <path id="path-driver-hw" d="M 575,265 L 600,265 L 600,195 L 635,195" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arch-arrow-default)" />

          <!-- P7: User Driver -> Hardware (Direct via Cap) -->
          <path id="path-userdriver-hw" d="M 575,92 L 600,92 L 600,170 L 635,170" fill="none" stroke="#cbd5e1" stroke-width="2" marker-end="url(#arch-arrow-default)" />
        </svg>
      </div>

      <!-- Foreshadowed Navigation & Controls -->
      <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 20px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 16px;">
        <div style="display: flex; gap: 8px;">
          <button type="button" id="btn-arch-prev" style="padding: 6px 14px; font-weight: 600; font-size: 0.85rem; border: 1px solid #cbd5e1; background: #ffffff; color: #334155; border-radius: 5px; cursor: pointer;">&larr; Prev</button>
          <button type="button" id="btn-arch-next" style="padding: 6px 14px; font-weight: 600; font-size: 0.85rem; border: 1px solid #0284c7; background: #0284c7; color: #ffffff; border-radius: 5px; cursor: pointer;">Next Step &rarr;</button>
          <button type="button" id="btn-arch-reset" style="padding: 6px 12px; font-size: 0.85rem; border: 1px solid #cbd5e1; background: #ffffff; color: #64748b; border-radius: 5px; cursor: pointer;">Reset</button>
        </div>

        <!-- Inline Preview of Next Action -->
        <div style="font-size: 0.85rem; color: #334155;">
          <span style="color: #64748b; font-weight: 600;">UPCOMING TRANSITION:</span> <span id="arch-preview-text" style="font-weight: 700; color: #0284c7;">Application executes syscall trap into kernel mode</span>
        </div>
      </div>

      <!-- Paired Analytical Panes (Strict Mechanics vs. Rationale) -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
        <!-- Pane 1: Mechanics -->
        <div style="border: 1px solid #bae6fd; background: #f0f9ff; border-radius: 6px; padding: 16px;">
          <div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.85rem; color: #0369a1; text-transform: uppercase; margin-bottom: 6px;">1. What Is Happening (Low-Level Mechanics)</div>
          <div id="arch-pane-mechanics" style="font-size: 0.9rem; color: #1e293b; line-height: 1.5;"></div>
        </div>

        <!-- Pane 2: Rationale -->
        <div style="border: 1px solid #fde68a; background: #fffbeb; border-radius: 6px; padding: 16px;">
          <div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.85rem; color: #92400e; text-transform: uppercase; margin-bottom: 6px;">2. Why The System Does This (Design Rationale)</div>
          <div id="arch-pane-rationale" style="font-size: 0.9rem; color: #78350f; line-height: 1.5;"></div>
        </div>
      </div>

      <!-- Dedicated Contextual Definitions Section (Underneath on its own) -->
      <div style="border: 1px solid #e2e8f0; background: #f8fafc; border-radius: 6px; padding: 16px;">
        <div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.85rem; color: #475569; text-transform: uppercase; margin-bottom: 8px;">Contextual Definitions &amp; Architectural Concepts</div>
        <div id="arch-pane-definitions" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 12px;"></div>
      </div>
    </div>

    <!-- Stepper Logic Script -->
    <script>
      (function() {
        const archWorkflows = {
          "monolithic": [
            {
              mode: "USER MODE (RING 3)",
              component: "USER APPLICATION",
              switches: "0",
              comm: "LOCAL CALL",
              activeBox: "box-app",
              activePath: "path-app-kernel-trap",
              preview: "App traps into kernel via syscall instruction",
              mechanics: "The application passes parameters in registers (RAX=0 for sys_read, RDI=fd, RSI=buf) and executes the syscall instruction, switching CPU execution to Ring 0.",
              rationale: "Limited Direct Execution allows native CPU performance for computation while interposing hardware gates for privileged storage operations.",
              definitions: [
                { term: "Limited Direct Execution (LDE)", desc: "Running user code directly on raw CPU hardware while trapping into supervisor mode for privileged operations." },
                { term: "Syscall Gate", desc: "A hardware-enforced CPU transition mechanism that switches execution privilege levels from Ring 3 to Ring 0." }
              ]
            },
            {
              mode: "KERNEL MODE (RING 0)",
              component: "VFS & EXT4 FILE SYSTEM",
              switches: "0 (SAME ADDRESS SPACE)",
              comm: "DIRECT C FUNCTION CALL",
              activeBox: "box-kernel",
              activePath: "path-kernel-driver",
              preview: "VFS resolves inode and passes request directly to NVMe block driver",
              mechanics: "The Virtual File System validates file descriptors, calculates logical block addresses (LBAs) via extent trees, and invokes the NVMe driver via a standard C function pointer.",
              rationale: "Zero address-space switches. All subsystems share a single contiguous supervisor address space, eliminating translation buffer invalidations.",
              definitions: [
                { term: "Virtual File System (VFS)", desc: "The kernel abstraction layer providing standardized POSIX file operations atop diverse underlying filesystem drivers." },
                { term: "Function Pointer Dispatch", desc: "Executing module routines directly via in-memory pointers without inter-process message passing." }
              ]
            },
            {
              mode: "KERNEL MODE (RING 0)",
              component: "NVMe DRIVER & CONTROLLER",
              switches: "0 (SAME CONTEXT)",
              comm: "MMIO DOORBELL WRITE",
              activeBox: "box-kerneldriver",
              activePath: "path-driver-hw",
              preview: "Driver writes submission descriptor to NVMe hardware doorbell",
              mechanics: "The driver constructs a 64-byte command descriptor in DMA host memory and writes the new tail pointer to the controller's memory-mapped I/O (MMIO) register.",
              rationale: "Direct memory-mapped hardware access maximizes storage I/O operations per second (IOPS) with absolute minimum latency.",
              definitions: [
                { term: "Memory-Mapped I/O (MMIO)", desc: "Mapping device controller registers directly into the CPU physical address space for register access via standard store instructions." },
                { term: "Direct Memory Access (DMA)", desc: "Hardware capability allowing storage controllers to stream data directly into host DRAM without CPU cycle consumption." }
              ]
            }
          ],
          "microkernel": [
            {
              mode: "USER MODE (RING 3)",
              component: "USER APPLICATION",
              switches: "0",
              comm: "LOCAL STUB",
              activeBox: "box-app",
              activePath: "path-app-userservice",
              preview: "App formats message and issues IPC call to File System Server",
              mechanics: "The application encodes the read request into a standardized IPC message buffer and transfers execution to the isolated File System Server process.",
              rationale: "Microkernels strip file system logic out of the supervisor core; user applications communicate with independent service daemons.",
              definitions: [
                { term: "User-Space Server", desc: "A system service (e.g. file system or network stack) executing as an isolated unprivileged user process in Ring 3." },
                { term: "Message Marshalling", desc: "Serializing parameters into a standardized buffer for inter-process communication across isolated address spaces." }
              ]
            },
            {
              mode: "USER MODE (RING 3)",
              component: "FILE SYSTEM SERVER",
              switches: "2 (APP -> KERN -> FS)",
              comm: "SYNCHRONOUS IPC VIA MICROKERNEL",
              activeBox: "box-userservice",
              activePath: "path-userservice-kernel",
              preview: "FS server translates request and invokes kernel to route IPC to driver",
              mechanics: "The microkernel switches page tables (CR3 swap) to run the File System Server. The server translates the path to block offsets and calls microkernel IPC to signal the driver.",
              rationale: "Fault isolation: if the file system server crashes, the core kernel and hardware device drivers remain fully operational and unaffected.",
              definitions: [
                { term: "Address Space Switch", desc: "Reloading CPU page directory registers (CR3/TTBR0), invalidating cached TLB address translations." },
                { term: "Fault Domain Isolation", desc: "Confining software failures to an unprivileged container so bugs cannot crash the operating system." }
              ]
            },
            {
              mode: "USER MODE (RING 3)",
              component: "USER-SPACE NVMe DRIVER",
              switches: "4 (FS -> KERN -> DRV)",
              comm: "CAPABILITY-PROTECTED MMIO",
              activeBox: "box-userdriver",
              activePath: "path-userdriver-hw",
              preview: "Driver accesses controller MMIO registers via kernel capability",
              mechanics: "The user-space driver receives the IPC packet. Using physical memory pages explicitly mapped by the microkernel via capability tokens, it writes the NVMe doorbell.",
              rationale: "Running device drivers in user space protects against hardware driver bugs, which account for the vast majority of operating system crashes.",
              definitions: [
                { term: "User-Space Device Driver", desc: "A device driver running in Ring 3 that interacts with hardware strictly through capability-authorized MMIO regions." },
                { term: "Capability Token", desc: "An unforgeable cryptographic or kernel-held authority token granting access to a specific system or hardware resource." }
              ]
            }
          ],
          "hybrid": [
            {
              mode: "USER MODE (RING 3)",
              component: "USER APPLICATION",
              switches: "0",
              comm: "WIN32 SUBSYSTEM CALL",
              activeBox: "box-app",
              activePath: "path-app-kernel-trap",
              preview: "App calls ReadFile() and traps into NT Executive via ntdll.dll",
              mechanics: "The application calls Win32 ReadFile(). System DLLs construct arguments and invoke NtReadFile() in ntdll.dll, executing a syscall trap into Ring 0.",
              rationale: "Separates OS environment personalities (Win32, POSIX) from core kernel primitives while maintaining high-speed entry.",
              definitions: [
                { term: "Environment Subsystem", desc: "User-mode processes (such as csrss.exe) that present specific operating system personalities to applications." },
                { term: "Native API (ntdll.dll)", desc: "The foundational user-mode interface bridging subsystem DLLs directly to the Windows NT Executive." }
              ]
            },
            {
              mode: "KERNEL MODE (RING 0)",
              component: "NT EXECUTIVE & I/O MANAGER",
              switches: "0 (NO ADDRESS SWITCH)",
              comm: "I/O REQUEST PACKET (IRP)",
              activeBox: "box-kernel",
              activePath: "path-kernel-driver",
              preview: "I/O Manager creates IRP and routes it down the layered driver stack",
              mechanics: "The I/O Manager allocates an I/O Request Packet (IRP) representing the read operation and passes it down a chain of filter and filesystem drivers.",
              rationale: "Layered IRP dispatching allows volume management, disk encryption (BitLocker), and antivirus filters to intercept data transparently.",
              definitions: [
                { term: "I/O Request Packet (IRP)", desc: "The core data structure in Windows NT representing an asynchronous I/O transaction through driver stacks." },
                { term: "Layered Driver Model", desc: "Organizing drivers in vertical stacks where each layer performs processing before delegating downward." }
              ]
            },
            {
              mode: "KERNEL MODE (RING 0)",
              component: "STORPORT & NVMe MINI-PORT",
              switches: "0 (SAME CONTEXT)",
              comm: "DIRECT CONTROLLER ACCESS",
              activeBox: "box-kerneldriver",
              activePath: "path-driver-hw",
              preview: "Miniport driver submits command directly to NVMe hardware queue",
              mechanics: "The Storport driver routes the IRP to the NVMe miniport driver, which builds submission queue entries in DMA space and rings the controller doorbell.",
              rationale: "Executes performance-critical hardware drivers in Ring 0 to match monolithic throughput while retaining structured layered abstractions.",
              definitions: [
                { term: "Miniport Driver", desc: "A specialized hardware driver handling device silicon while an OS class driver handles generic OS protocols." },
                { term: "Doorbell Register", desc: "A memory-mapped register used by the host CPU to notify an NVMe controller of new pending commands." }
              ]
            }
          ],
          "exokernel": [
            {
              mode: "USER MODE (RING 3)",
              component: "APPLICATION + LIBOS",
              switches: "0",
              comm: "IN-PROCESS LIBRARY CALL",
              activeBox: "box-userservice",
              activePath: "path-userservice-kernel",
              preview: "LibOS calculates exact physical block and formats capability request",
              mechanics: "The application calls its statically linked Library OS (LibOS). The LibOS calculates the raw physical disk sector and formats a capability token.",
              rationale: "Eliminates centralized kernel abstractions. The application customizes disk layout, cache management, and data indexing directly.",
              definitions: [
                { term: "Library OS (LibOS)", desc: "Operating system services (such as file systems or network stacks) compiled directly into an application binary." },
                { term: "End-to-End Argument", desc: "The systems principle stating that application-specific functions are best implemented in application space rather than in the kernel." }
              ]
            },
            {
              mode: "KERNEL MODE (RING 0)",
              component: "EXOKERNEL CORE",
              switches: "0",
              comm: "CAPABILITY VALIDATION",
              activeBox: "box-kernel",
              activePath: "path-driver-hw",
              preview: "Exokernel verifies capability and gives hardware direct access",
              mechanics: "The tiny exokernel verifies that the calling LibOS possesses the capability key for the target physical block. Once validated, it triggers the transfer.",
              rationale: "Separates protection from management: the exokernel enforces isolation and hardware multiplexing, while the LibOS manages all policies.",
              definitions: [
                { term: "Protection vs. Management", desc: "The exokernel doctrine: the kernel only enforces resource bounds; applications manage all policies." },
                { term: "Secure Binding", desc: "Hardware or software mechanism that locks a resource to an application without runtime kernel intervention." }
              ]
            }
          ]
        };

        let currentArch = "monolithic";
        let currentStep = 0;

        function refreshArchView() {
          const archData = archWorkflows[currentArch];
          if (currentStep >= archData.length) currentStep = 0;
          const stepData = archData[currentStep];

          // 1. Update Telemetry
          document.getElementById("telemetry-mode").textContent = stepData.mode;
          document.getElementById("telemetry-component").textContent = stepData.component;
          document.getElementById("telemetry-switches").textContent = stepData.switches;
          document.getElementById("telemetry-comm").textContent = stepData.comm;

          // 2. Update Narrative Panes
          document.getElementById("arch-preview-text").textContent = stepData.preview;
          document.getElementById("arch-pane-mechanics").textContent = stepData.mechanics;
          document.getElementById("arch-pane-rationale").textContent = stepData.rationale;

          // 3. Render Dedicated Definitions Container
          const defsContainer = document.getElementById("arch-pane-definitions");
          defsContainer.innerHTML = "";
          stepData.definitions.forEach(item => {
            const card = document.createElement("div");
            card.style.background = "#ffffff";
            card.style.border = "1px solid #cbd5e1";
            card.style.borderRadius = "4px";
            card.style.padding = "10px 12px";
            card.innerHTML = `<div style="font-family: var(--font-mono); font-weight: 700; font-size: 0.85rem; color: #0284c7; margin-bottom: 4px;">${item.term}</div><div style="font-size: 0.85rem; color: #475569; line-height: 1.4;">${item.desc}</div>`;
            defsContainer.appendChild(card);
          });

          // 4. Update Node Labels and Visibility by Architecture
          const userServ = document.getElementById("box-userservice");
          const userDrv = document.getElementById("box-userdriver");
          const kernDrv = document.getElementById("box-kerneldriver");
          const kernCore = document.getElementById("box-kernel");

          if (currentArch === "monolithic") {
            userServ.style.opacity = "0.35";
            document.getElementById("label-userservice-title").textContent = "User Service (N/A)";
            document.getElementById("label-userservice-sub").textContent = "In Kernel";
            userDrv.style.opacity = "0.35";
            document.getElementById("label-userdriver-title").textContent = "User Driver (N/A)";
            document.getElementById("label-userdriver-sub").textContent = "In Kernel";
            kernDrv.style.opacity = "1.0";
            document.getElementById("label-kernel-title").textContent = "VFS & Ext4";
            document.getElementById("label-kernel-sub").textContent = "Monolithic Ring 0";
          } else if (currentArch === "microkernel") {
            userServ.style.opacity = "1.0";
            document.getElementById("label-userservice-title").textContent = "File Server";
            document.getElementById("label-userservice-sub").textContent = "User Process (Ring 3)";
            userDrv.style.opacity = "1.0";
            document.getElementById("label-userdriver-title").textContent = "NVMe Driver";
            document.getElementById("label-userdriver-sub").textContent = "User Process (Ring 3)";
            kernDrv.style.opacity = "0.35";
            document.getElementById("label-kernel-title").textContent = "Minimal Microkernel";
            document.getElementById("label-kernel-sub").textContent = "IPC & Scheduling";
          } else if (currentArch === "hybrid") {
            userServ.style.opacity = "0.35";
            document.getElementById("label-userservice-title").textContent = "Subsystem (csrss)";
            document.getElementById("label-userservice-sub").textContent = "User Mode Personality";
            userDrv.style.opacity = "0.35";
            document.getElementById("label-userdriver-title").textContent = "User Driver (UMDF)";
            document.getElementById("label-userdriver-sub").textContent = "Not Used for Disk";
            kernDrv.style.opacity = "1.0";
            document.getElementById("label-kernel-title").textContent = "NT Executive & VFS";
            document.getElementById("label-kernel-sub").textContent = "Ring 0 Subsystems";
          } else if (currentArch === "exokernel") {
            userServ.style.opacity = "1.0";
            document.getElementById("label-userservice-title").textContent = "App Library OS";
            document.getElementById("label-userservice-sub").textContent = "In-Process LibOS";
            userDrv.style.opacity = "0.35";
            document.getElementById("label-userdriver-title").textContent = "User Driver (N/A)";
            document.getElementById("label-userdriver-sub").textContent = "Direct Cap Access";
            kernDrv.style.opacity = "0.35";
            document.getElementById("label-kernel-title").textContent = "Exokernel Core";
            document.getElementById("label-kernel-sub").textContent = "Capability Gate";
          }

          // 5. Highlight Active Box
          const allBoxes = ["box-app", "box-userservice", "box-userdriver", "box-kernel", "box-kerneldriver", "box-hardware"];
          allBoxes.forEach(bid => {
            const el = document.getElementById(bid);
            if (el) {
              const rect = el.querySelector("rect");
              if (rect) {
                rect.removeAttribute("filter");
                rect.style.strokeWidth = "1.8px";
                rect.style.stroke = "#cbd5e1";
              }
            }
          });

          const activeEl = document.getElementById(stepData.activeBox);
          if (activeEl) {
            const rect = activeEl.querySelector("rect");
            if (rect) {
              rect.setAttribute("filter", "url(#arch-active-glow)");
              rect.style.strokeWidth = "3px";
              rect.style.stroke = "#0284c7";
            }
          }

          // 6. Highlight Active Path & Marker
          const allPaths = [
            "path-app-kernel-trap", "path-app-userservice", "path-userservice-kernel",
            "path-kernel-userdriver", "path-kernel-driver", "path-driver-hw", "path-userdriver-hw"
          ];
          allPaths.forEach(pid => {
            const pel = document.getElementById(pid);
            if (pel) {
              pel.style.stroke = "#cbd5e1";
              pel.style.strokeWidth = "2px";
              pel.setAttribute("marker-end", "url(#arch-arrow-default)");
            }
          });

          if (stepData.activePath) {
            const activePel = document.getElementById(stepData.activePath);
            if (activePel) {
              activePel.style.stroke = "#0284c7";
              activePel.style.strokeWidth = "3.2px";
              activePel.setAttribute("marker-end", "url(#arch-arrow-active)");
            }
          }
        }

        // Toggle Buttons
        document.querySelectorAll(".arch-toggle").forEach(btn => {
          btn.addEventListener("click", function() {
            document.querySelectorAll(".arch-toggle").forEach(b => {
              b.style.background = "#ffffff";
              b.style.color = "#475569";
              b.style.borderColor = "#cbd5e1";
            });
            this.style.background = "#0284c7";
            this.style.color = "#ffffff";
            this.style.borderColor = "#0284c7";
            currentArch = this.getAttribute("data-arch");
            currentStep = 0;
            refreshArchView();
          });
        });

        // Stepper Navigation
        document.getElementById("btn-arch-next").addEventListener("click", function() {
          currentStep = (currentStep + 1) % archWorkflows[currentArch].length;
          refreshArchView();
        });

        document.getElementById("btn-arch-prev").addEventListener("click", function() {
          currentStep = (currentStep - 1 + archWorkflows[currentArch].length) % archWorkflows[currentArch].length;
          refreshArchView();
        });

        document.getElementById("btn-arch-reset").addEventListener("click", function() {
          currentStep = 0;
          refreshArchView();
        });

        // Initial Paint
        refreshArchView();
      })();
    </script>
"""

def update_module_four():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- INTERACTIVE PEDAGOGICAL AID: DIRECTED NARRATIVE STEPPER -->"
    end_tag = "<!-- Navigation Bar Bottom -->"

    if start_tag not in content or end_tag not in content:
        print("--> Error: Could not locate stepper container boundaries in Module 4.")
        return

    part_before = content.split(start_tag)[0]
    part_after = content.split(end_tag)[1]

    updated_content = f"{part_before}{REBUILT_STEPPER_HTML}\n\n    {end_tag}{part_after}"

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"--> Successfully replaced interactive stepper in {TARGET_FILE}.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Fix missing nodes and misaligned paths in Module 4 I/O stepper\n\n"
            "Rebuild the SVG layout in 04-os-structure.html with dedicated Ring 0\n"
            "and Ring 3 lanes, correct driver placement across architectures, and\n"
            "properly anchored vector paths for all stepper stages."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_module_four()
