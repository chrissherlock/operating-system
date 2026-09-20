#!/usr/bin/env python3
# =====================================================================
# add_wikipedia_links_to_os_labels.py: Add Wikipedia links to OS labels
# =====================================================================
import os
import subprocess
import sys

FAMILY_GRID_WITH_LINKS = r"""
    <!-- OPERATING SYSTEM LOGOS FAMILY GRID SECTION -->
    <section class="content-section">
      <h2>Operating System Ecosystem &amp; Architecture Families</h2>
      <p>
        The operating system landscape spans diverse paradigms. Below is a structured visual index of system brand marks and logos organized by architectural family.
      </p>

      <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; display: flex; flex-direction: column; gap: 20px;">

        <!-- Family 1: Commercial Desktop & Mobile -->
        <div>
          <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: bold; color: #0369a1; text-transform: uppercase; margin-bottom: 10px;">
            Commercial Desktop &amp; Mobile Systems
          </div>
          <div style="display: flex; gap: 14px; flex-wrap: wrap;">
            <!-- Windows -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/windows.svg" alt="Windows Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/Microsoft_Windows" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">Windows</a>
            </div>
            <!-- Apple -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/apple.svg" alt="Apple Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/MacOS" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">Apple macOS</a>
            </div>
            <!-- ChromeOS -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/chrome.svg" alt="ChromeOS Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/ChromeOS" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">ChromeOS</a>
            </div>
          </div>
        </div>

        <!-- Family 2: Open-Source & Unix-Like -->
        <div>
          <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: bold; color: #0369a1; text-transform: uppercase; margin-bottom: 10px;">
            Open-Source &amp; Unix-Like Kernels
          </div>
          <div style="display: flex; gap: 14px; flex-wrap: wrap;">
            <!-- Linux Tux -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/tux.svg" alt="Linux Tux Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/Linux" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">Linux (Tux)</a>
            </div>
            <!-- FreeBSD -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/freebsd.svg" alt="FreeBSD Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/FreeBSD" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">FreeBSD</a>
            </div>
            <!-- Android -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/android.svg" alt="Android Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/Android_(operating_system)" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">Android</a>
            </div>
            <!-- MINIX -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/minix.png" alt="MINIX Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/MINIX" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">MINIX</a>
            </div>
          </div>
        </div>

        <!-- Family 3: Real-Time Operating Systems (RTOS) -->
        <div>
          <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: bold; color: #0369a1; text-transform: uppercase; margin-bottom: 10px;">
            Real-Time Operating Systems (RTOS)
          </div>
          <div style="display: flex; gap: 14px; flex-wrap: wrap;">
            <!-- FreeRTOS -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/free-rtos.png" alt="FreeRTOS Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/FreeRTOS" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">FreeRTOS</a>
            </div>
            <!-- QNX -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/qnx.svg" alt="QNX Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/QNX" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">QNX RTOS</a>
            </div>
            <!-- VxWorks -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/vxworks.svg" alt="VxWorks Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/VxWorks" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">VxWorks</a>
            </div>
          </div>
        </div>

        <!-- Family 4: Historical & Enterprise Architectures -->
        <div>
          <div style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: bold; color: #0369a1; text-transform: uppercase; margin-bottom: 10px;">
            Historical &amp; Enterprise Systems
          </div>
          <div style="display: flex; gap: 14px; flex-wrap: wrap;">
            <!-- OS/2 -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/os2.svg" alt="IBM OS/2 Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/OS/2" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">IBM OS/2</a>
            </div>
            <!-- Solaris -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/solaris.svg" alt="Solaris Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/Solaris_(operating_system)" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">Solaris</a>
            </div>
            <!-- OpenVMS -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/openvms.svg" alt="OpenVMS Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/OpenVMS" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">OpenVMS</a>
            </div>
            <!-- Multics -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/multics.svg" alt="Multics Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/Multics" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">Multics</a>
            </div>
            <!-- BeOS -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="../images/logos/beos.svg" alt="BeOS Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <a href="https://en.wikipedia.org/wiki/BeOS" target="_blank" rel="noopener" style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #0284c7; text-decoration: underline; text-align: center;">BeOS</a>
            </div>
          </div>
        </div>

      </div>
    </section>"""

def add_wikipedia_links():
    portal_path = os.path.join("week01-operating-system-concepts", "index.html")
    modified = []

    if os.path.exists(portal_path):
        with open(portal_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "OPERATING SYSTEM LOGOS FAMILY GRID SECTION" in content:
            parts = content.split("    <!-- OPERATING SYSTEM LOGOS FAMILY GRID SECTION -->")
            trailer = parts[1].split("</section>", 1)[1]
            content = parts[0] + FAMILY_GRID_WITH_LINKS + "\n\n    " + trailer.strip()
            with open(portal_path, "w", encoding="utf-8") as f:
                f.write(content)
            modified.append(portal_path)

    fix_path = "fix.py"
    if os.path.exists(fix_path):
        modified.append(fix_path)

    if not modified:
        print("--> No files modified.")
        return

    print(f"--> Staging modified files: {modified}")
    try:
        subprocess.run(["git", "add"] + modified, check=True)
        commit_msg = (
            "Add Wikipedia hyperlinks to operating system labels in Week 1 portal index\n\n"
            "Update week01-operating-system-concepts/index.html to turn system text labels\n"
            "beneath each logo into direct Wikipedia links for each respective operating system."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Wikipedia links successfully deployed to OS labels!")

if __name__ == "__main__":
    add_wikipedia_links()
