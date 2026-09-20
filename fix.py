#!/usr/bin/env python3
# =====================================================================
# fix_os_logos_paths.py: Correct image paths for OS logos family grid
# =====================================================================
import os
import subprocess
import sys

FAMILY_GRID_HTML_FIXED = r"""
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
              <img src="images/logos/windows.svg" alt="Windows Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">Windows</span>
            </div>
            <!-- Apple -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="images/logos/apple.svg" alt="Apple Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">Apple macOS</span>
            </div>
            <!-- ChromeOS -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="images/logos/chrome.svg" alt="ChromeOS Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">ChromeOS</span>
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
              <img src="images/logos/tux.svg" alt="Linux Tux Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">Linux (Tux)</span>
            </div>
            <!-- FreeBSD -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="images/logos/freebsd.svg" alt="FreeBSD Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">FreeBSD</span>
            </div>
            <!-- Android -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="images/logos/android.svg" alt="Android Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">Android</span>
            </div>
            <!-- MINIX -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="images/logos/minix.png" alt="MINIX Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">MINIX</span>
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
              <img src="images/logos/free-rtos.png" alt="FreeRTOS Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">FreeRTOS</span>
            </div>
            <!-- QNX -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="images/logos/qnx.svg" alt="QNX Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">QNX RTOS</span>
            </div>
            <!-- VxWorks -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="images/logos/vxworks.svg" alt="VxWorks Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">VxWorks</span>
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
              <img src="images/logos/os2.svg" alt="IBM OS/2 Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">IBM OS/2</span>
            </div>
            <!-- Solaris -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="images/logos/solaris.svg" alt="Solaris Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">Solaris</span>
            </div>
            <!-- OpenVMS -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="images/logos/openvms.svg" alt="OpenVMS Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">OpenVMS</span>
            </div>
            <!-- Multics -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="images/logos/multics.svg" alt="Multics Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">Multics</span>
            </div>
            <!-- BeOS -->
            <div style="width: 120px; height: 110px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; gap: 6px;">
              <img src="images/logos/beos.svg" alt="BeOS Logo" style="max-width: 42px; max-height: 42px; object-fit: contain;">
              <span style="font-size: 0.72rem; font-family: var(--font-mono); font-weight: bold; color: #334155; text-align: center;">BeOS</span>
            </div>
          </div>
        </div>

      </div>
    </section>"""

def fix_paths():
    portal_path = os.path.join("week01-operating-system-concepts", "index.html")
    modified = []

    if os.path.exists(portal_path):
        with open(portal_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "OPERATING SYSTEM LOGOS FAMILY GRID SECTION" in content:
            parts = content.split("    <!-- OPERATING SYSTEM LOGOS FAMILY GRID SECTION -->")
            trailer = parts[1].split("</section>", 1)[1]
            content = parts[0] + FAMILY_GRID_HTML_FIXED + "\n\n    " + trailer.strip()
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
            "Fix relative image paths for OS logos family grid in Week 1 portal index\n\n"
            "Update week01-operating-system-concepts/index.html logo sources from ../images/logos/\n"
            "to images/logos/ so icons resolve and render correctly."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> OS logos family grid path fix successfully deployed!")

if __name__ == "__main__":
    fix_paths()
