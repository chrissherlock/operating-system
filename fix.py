#!/usr/bin/env python3
# =====================================================================
# fix.py: Align 04-os-structure.html layout into single container card
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week01-operating-system-concepts",
    "04-os-structure.html"
)

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>04. Operating System Structure -- COSC240</title>
  <style>
    :root {
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #cbd5e1;
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --text: #0f172a;
      --text-muted: #475569;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; overflow-wrap: break-word; word-break: break-word; }
    body {
      font-family: var(--font-sans);
      color: var(--text);
      background-color: var(--bg);
      margin: 0;
      padding: 32px 16px;
      line-height: 1.6;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .module-nav-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
    }
    .module-nav-bar.bottom {
      margin-top: 36px;
      margin-bottom: 0;
      padding-top: 16px;
      padding-bottom: 0;
      border-bottom: none;
      border-top: 1px solid var(--border);
    }
    .module-nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #334155;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.85rem;
      font-family: var(--font-sans);
      transition: all 0.15s ease;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }
    .module-nav-btn:hover {
      background-color: #f8fafc;
      color: var(--accent);
      border-color: var(--accent);
    }
    .module-nav-placeholder {
      visibility: hidden;
      padding: 6px 12px;
      font-size: 0.85rem;
    }
    header {
      margin-bottom: 24px;
    }
    h1 {
      font-size: 1.8rem;
      color: var(--accent);
      margin-bottom: 8px;
    }
    p.subtitle {
      color: var(--text-muted);
      font-size: 0.95rem;
    }
    article.module-body {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    h2 {
      font-size: 1.3rem;
      color: #0369a1;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 8px;
      margin-top: 36px;
    }
    h3 {
      font-size: 1.15rem;
      color: #1e293b;
      margin-top: 24px;
      margin-bottom: 8px;
    }
    p {
      color: var(--text-muted);
      line-height: 1.6;
      font-size: 0.95rem;
      margin-bottom: 12px;
    }
    ul, ol {
      margin-left: 20px;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 12px;
    }
    li {
      margin-bottom: 6px;
    }
    code {
      font-family: var(--font-mono);
      font-size: 0.88rem;
      background-color: #f1f5f9;
      padding: 2px 6px;
      border-radius: 4px;
      color: #0369a1;
    }
    .aside-box {
      background: #f8fafc;
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent);
      padding: 16px;
      border-radius: 0 6px 6px 0;
      margin: 16px 0;
    }
  </style>
</head>
<body>
  <div class="container">

    <nav class="module-nav-bar">
      <div>
        <a href="03-os-concepts.html" class="module-nav-btn">&larr; Previous: 03. OS Concepts</a>
      </div>
      <div>
        <a href="index.html" class="module-nav-btn">&#127968; Week 1: Operating System Concepts</a>
      </div>
      <div class="module-nav-placeholder">&rarr; Placeholder</div>
    </nav>

    <header>
      <h1>04. Operating System Structure</h1>
      <p class="subtitle">Tanenbaum Chapter 1.7: Monolithic, Layered, Microkernel, Client-Server, and Virtual Machine Architectures.</p>
    </header>

    <article class="module-body">
      <h2>Architectural Archetypes</h2>
      <p>
        How an operating system is structured internally dictates its reliability, performance, maintainability, and extensibility. Modern designs balance raw kernel performance against isolation barriers that prevent subsystem faults from causing catastrophic system panics.
      </p>

      <h3>1. Monolithic Systems</h3>
      <p>
        In a monolithic architecture, the entire operating system executes as a single unified program in supervisor mode (Ring 0). All kernel components—including the CPU scheduler, virtual memory management, virtual file system, networking stacks, and peripheral device drivers—share the same address space.
      </p>
      <ul>
        <li><strong>Strengths:</strong> Maximum runtime performance with minimal call overhead; kernel subsystems communicate via direct, fast function calls.</li>
        <li><strong>Weaknesses:</strong> Poor fault isolation. A bug, memory leak, or invalid pointer dereference in a third-party device driver can compromise or crash the entire machine.</li>
      </ul>

      <h3>2. Layered Systems</h3>
      <p>
        Layered systems organize the operating system into a strict hierarchy of abstraction tiers, where each layer depends solely on the interfaces provided by the layer immediately below it. The hardware resides at Layer 0, while the user interface sits at the highest layer (such as Dijkstra's THE multiprogramming system).
      </p>

      <h3>3. Microkernels</h3>
      <p>
        Microkernel architectures adopt a philosophy of minimal kernel privilege. Only the absolute essentials required to support an operating system remain in supervisor mode: primitive low-level memory mapping, fundamental thread scheduling, and inter-process communication (IPC).
      </p>
      <p>
        All other traditional operating system services—including file systems, network protocol stacks, and device drivers—are moved into unprivileged user mode (Ring 3) as discrete server daemons.
      </p>
      <ul>
        <li><strong>Strengths:</strong> Exceptional fault tolerance and security. If a file system or network driver crashes, the microkernel restarts the server process without bringing down the machine.</li>
        <li><strong>Weaknesses:</strong> IPC overhead. Transitioning requests between user-space servers requires repeated context switches and memory boundary crossings.</li>
      </ul>

      <div class="aside-box">
        <strong>Case Study: MINIX 3 &amp; QNX Neutrino</strong>
        <p style="margin-top: 6px; font-size: 0.88rem;">
          Both MINIX 3 and BlackBerry QNX showcase microkernel designs where device drivers run as isolated user processes. In mission-critical embedded environments like automotive dashboards and medical equipment, an isolated driver crash can self-heal without interrupting core system operation.
        </p>
      </div>

      <h3>4. Client-Server Architectures</h3>
      <p>
        A generalization of the microkernel concept where the operating system splits into clients (applications requesting services) and servers (subsystems servicing those requests). Because communication occurs through standardized message-passing protocols, clients and servers can reside on the same physical machine or communicate across network fabrics seamlessly.
      </p>

      <h3>5. Virtual Machines &amp; Hypervisors</h3>
      <p>
        Virtualization abstracts physical machine hardware into multiple isolated execution environments. <strong>Type-1 (bare-metal) hypervisors</strong> execute directly on raw server silicon, managing CPU scheduling and memory partitions for multiple concurrent guest kernels. <strong>Type-2 (hosted) hypervisors</strong> run as applications inside a conventional host operating system.
      </p>
    </article>

    <nav class="module-nav-bar bottom">
      <div>
        <a href="03-os-concepts.html" class="module-nav-btn">&larr; Previous: 03. OS Concepts</a>
      </div>
      <div>
        <a href="index.html" class="module-nav-btn">&#127968; Week 1: Operating System Concepts</a>
      </div>
      <div class="module-nav-placeholder">&rarr; Placeholder</div>
    </nav>

  </div>
</body>
</html>
"""

def generate_module_four():
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"--> Overwrote {TARGET_FILE} with unified single-card container structure.")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Unify Module 4 OS structure layout into single container card\n\n"
            "Align 04-os-structure.html with the course layout standard: wrap all\n"
            "elements in a single bounded .container card, remove nested content-section\n"
            "boxes, and standardize navigation buttons and typography."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for Module 4!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    generate_module_four()
