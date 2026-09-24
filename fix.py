#!/usr/bin/env python3
# =====================================================================
# fix.py: Reconcile Week 5 module numbering and link topology
# =====================================================================
import os
import subprocess

WEEK5_DIR = "week05-io-and-disk-scheduling"
OLD_DISK_FILE = os.path.join(WEEK5_DIR, "02-disk-hardware-scheduling.html")
NEW_DISK_FILE = os.path.join(WEEK5_DIR, "03-disk-hardware-scheduling.html")
MOD01_FILE = os.path.join(WEEK5_DIR, "01-io-hardware-device-controllers.html")
MOD02_FILE = os.path.join(WEEK5_DIR, "02-interrupts-and-dma.html")
INDEX_FILE = os.path.join(WEEK5_DIR, "index.html")

def reconcile_files():
    # 1. Rename 02-disk-hardware-scheduling.html -> 03-disk-hardware-scheduling.html
    if os.path.exists(OLD_DISK_FILE):
        os.rename(OLD_DISK_FILE, NEW_DISK_FILE)
        print(f"--> Renamed {OLD_DISK_FILE} -> {NEW_DISK_FILE}")

    # 2. Update Module 01 navigation: Next -> 02-interrupts-and-dma.html
    if os.path.exists(MOD01_FILE):
        with open(MOD01_FILE, "r", encoding="utf-8") as f:
            m1 = f.read()

        m1 = m1.replace(
            '<a href="02-disk-hardware-scheduling.html">Next: 02. Disk Hardware &amp; Scheduling &rarr;</a>',
            '<a href="02-interrupts-and-dma.html">Next: 02. Interrupts &amp; DMA &rarr;</a>'
        )
        with open(MOD01_FILE, "w", encoding="utf-8") as f:
            f.write(m1)
        print(f"--> Updated navigation in {MOD01_FILE}")

    # 3. Update Module 02 navigation: Next -> 03-disk-hardware-scheduling.html
    if os.path.exists(MOD02_FILE):
        with open(MOD02_FILE, "r", encoding="utf-8") as f:
            m2 = f.read()

        m2 = m2.replace(
            '<a href="03-io-software-layers-buffering.html">Next: 03. I/O Software Layers &rarr;</a>',
            '<a href="03-disk-hardware-scheduling.html">Next: 03. Disk Geometry &amp; Arm Scheduling &rarr;</a>'
        )
        with open(MOD02_FILE, "w", encoding="utf-8") as f:
            f.write(m2)
        print(f"--> Updated navigation in {MOD02_FILE}")

    # 4. Update Module 03 navigation & header title
    if os.path.exists(NEW_DISK_FILE):
        with open(NEW_DISK_FILE, "r", encoding="utf-8") as f:
            m3 = f.read()

        # Update title and heading number
        m3 = m3.replace(
            "<title>02. Disk Geometry &amp; Arm Scheduling | Week 5: I/O &amp; Disk Scheduling</title>",
            "<title>03. Disk Geometry &amp; Arm Scheduling | Week 5: I/O &amp; Disk Scheduling</title>"
        )
        m3 = m3.replace(
            "<h2>02. Disk Geometry &amp; Arm Scheduling</h2>",
            "<h2>03. Disk Geometry &amp; Arm Scheduling</h2>"
        )

        # Update nav-bar links
        m3 = m3.replace(
            '<a href="01-io-hardware-device-controllers.html">&larr; 01. I/O Hardware &amp; Controllers</a>',
            '<a href="02-interrupts-and-dma.html">&larr; 02. Interrupts &amp; DMA</a>'
        )
        m3 = m3.replace(
            '<a href="03-io-software-layers-buffering.html">Next: 03. I/O Software Layers &rarr;</a>',
            '<a href="04-raid-architectures.html">Next: 04. RAID Architectures &rarr;</a>'
        )

        with open(NEW_DISK_FILE, "w", encoding="utf-8") as f:
            f.write(m3)
        print(f"--> Updated numbering and navigation in {NEW_DISK_FILE}")

    # 5. Synchronize Week 5 Hub (index.html)
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            idx = f.read()

        # Ensure Module 01, 02, 03 are correctly linked in the card list
        if "01-io-hardware-device-controllers.html" not in idx or "02-interrupts-and-dma.html" not in idx:
            # Replace placeholder or stale links with active module cards
            stale_block_start = idx.find('<div class="modules-grid">')
            stale_block_end = idx.find('</div>\n  </div>\n</body>')
            if stale_block_start != -1 and stale_block_end != -1:
                replacement_grid = """<div class="modules-grid">
      <a class="module-card" href="01-io-hardware-device-controllers.html">
        <span class="module-num">Module 01</span>
        <h3>I/O Hardware &amp; Device Controllers</h3>
        <p>Device classes, PMIO vs. MMIO, hardware status/command registers, and PIO vs. DMA data transfers.</p>
      </a>

      <a class="module-card" href="02-interrupts-and-dma.html">
        <span class="module-num">Module 02</span>
        <h3>Interrupts &amp; Direct Memory Access (DMA)</h3>
        <p>APIC/MSI-X vectoring, top-half vs. bottom-half deferral, Windows DPCs, and cache coherency snooping.</p>
      </a>

      <a class="module-card" href="03-disk-hardware-scheduling.html">
        <span class="module-num">Module 03</span>
        <h3>Disk Geometry &amp; Arm Scheduling</h3>
        <p>Platters, cylinders, CHS to LBA translation, seek/rotational latency math, and SSTF/SCAN/C-LOOK algorithms.</p>
      </a>

      <a class="module-card" href="04-raid-architectures.html">
        <span class="module-num">Module 04</span>
        <h3>RAID Architectures &amp; Reliability</h3>
        <p>Striping, mirroring, parity math, RAID 0 through RAID 6, MTTF reliability modeling, and rebuild rebuild delays.</p>
      </a>"""
                idx = idx[:stale_block_start] + replacement_grid + idx[stale_block_end:]
                with open(INDEX_FILE, "w", encoding="utf-8") as f:
                    f.write(idx)
                print(f"--> Synchronized Week 5 Hub cards in {INDEX_FILE}")

def run_git_sync():
    try:
        # Check if old file was in git and remove it
        subprocess.run(["git", "rm", "-f", OLD_DISK_FILE], stderr=subprocess.DEVNULL)
        subprocess.run(["git", "add", "fix.py", WEEK5_DIR], check=True)
        commit_msg = (
            "Reconcile Week 5 module numbering and link topology\n\n"
            "Rename 02-disk-hardware-scheduling to 03-disk-hardware-scheduling,\n"
            "correct sequential navigation links, and synchronize Week 5 hub index."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    reconcile_files()
    run_git_sync()
