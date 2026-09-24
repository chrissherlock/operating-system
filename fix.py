#!/usr/bin/env python3
# =====================================================================
# check_and_sync.py: Verify Figure 2.2 SVG cleanliness and sync cleanly
# =====================================================================
import os
import subprocess

TARGET_FILE = os.path.join(
    "week05-io-and-disk-scheduling", "03-disk-hardware-scheduling.html"
)

CORRECTED_FIGURE = r"""    <!-- Structural Diagram: Time-Domain Latency Timeline -->
    <div style="background: #ffffff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin: 24px 0;">
      <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 4px;">Figure 2.2: Time-Domain Decomposition of a Random 4 KB Disk Read Operation (~10.2 ms)</div>
      <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 14px;">Visualizing how mechanical arm movement and platter rotation dwarf electronic transfer time by over 500 to 1.</div>

      <svg viewBox="0 0 760 250" style="width: 100%; height: auto; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <defs>
          <marker id="fig22-arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#0284c7" />
          </marker>
          <marker id="fig22-arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#059669" />
          </marker>
        </defs>

        <!-- Timeline Scale Bar -->
        <g transform="translate(30, 30)">
          <!-- Total Container Width: 700px representing 10.2 ms -->

          <!-- 1. Seek Phase (6.0 ms -> ~412px) -->
          <rect x="0" y="20" width="412" height="46" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
          <text x="206" y="40" text-anchor="middle" font-size="8.5" font-weight="700" fill="#991b1b">SEEK TIME (T_seek): 6.00 ms (58.8%)</text>
          <text x="206" y="54" text-anchor="middle" font-size="7" fill="#7f1d1d">Arm acceleration, coasting, deceleration, head settling</text>

          <!-- 2. Rotational Phase (4.17 ms -> ~286px) -->
          <rect x="412" y="20" width="286" height="46" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
          <text x="555" y="40" text-anchor="middle" font-size="8.5" font-weight="700" fill="#92400e">ROTATIONAL DELAY (T_rot): 4.17 ms (40.9%)</text>
          <text x="555" y="54" text-anchor="middle" font-size="7" fill="#b45309">Waiting for target sector to spin under head (7200 RPM)</text>

          <!-- 3. Electronic Transfer & Controller Phase (0.02 ms + 0.01 ms) -> magnified inset -->
          <rect x="696" y="20" width="4" height="46" fill="#16a34a"/>

          <!-- Axis Ticks -->
          <line x1="0" y1="66" x2="0" y2="76" stroke="#475569" stroke-width="1.5"/>
          <text x="0" y="88" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#475569">0.0 ms</text>

          <line x1="412" y1="66" x2="412" y2="76" stroke="#475569" stroke-width="1.5"/>
          <text x="412" y="88" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#475569">6.00 ms</text>

          <line x1="698" y1="66" x2="698" y2="76" stroke="#475569" stroke-width="1.5"/>
          <text x="698" y="88" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" fill="#475569">10.17 ms</text>

          <!-- Magnified Inset Pointer for Transfer & Controller Phase -->
          <line x1="698" y1="20" x2="650" y2="-8" stroke="#059669" stroke-width="1" stroke-dasharray="3 2"/>
          <rect x="520" y="-22" width="176" height="22" rx="3" fill="#dcfce7" stroke="#16a34a" stroke-width="1"/>
          <text x="608" y="-8" text-anchor="middle" font-family="var(--font-mono)" font-size="7.5" font-weight="700" fill="#166534">T_transfer + T_ctrl: ~0.03 ms (0.3%)</text>
        </g>

        <!-- Explanatory Diagnostic Card -->
        <g transform="translate(30, 140)">
          <rect width="700" height="90" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>

          <text x="20" y="24" font-size="8.5" font-weight="700" fill="#0f172a">THE MECHANICAL LATENCY REALITY (Random 4 KB Read = ~10.20 ms):</text>
          <text x="20" y="44" font-size="8" fill="#334155">&bull; <tspan font-weight="700" fill="#dc2626">Mechanical Latency (Seek + Rotation):</tspan> Consumes <tspan font-weight="700" fill="#dc2626">10.17 ms (99.7% of total I/O time)</tspan>.</text>
          <text x="20" y="60" font-size="8" fill="#334155">&bull; <tspan font-weight="700" fill="#059669">Electronic Transfer Time (4 KB @ 200 MB/s):</tspan> Consumes <tspan font-weight="700" fill="#059669">0.02 ms (less than 0.2% of total time)</tspan>.</text>
          <text x="20" y="76" font-size="8" fill="#334155">&bull; <tspan font-weight="700" fill="#0284c7">Controller &amp; Bus Handshake Overhead:</tspan> Consumes <tspan font-weight="700" fill="#0284c7">0.01 ms (0.1% of total time)</tspan>.</text>
        </g>
      </svg>
    </div>"""


def check_and_update():
  if not os.path.exists(TARGET_FILE):
    print(f"File {TARGET_FILE} not found.")
    return

  with open(TARGET_FILE, "r", encoding="utf-8") as f:
    content = f.read()

  # Check if Figure 2.2 needs replacing
  start_marker = "<!-- Structural Diagram: Time-Domain Latency Timeline -->"
  end_marker = (
      "<h4>1. Seek Time (<i>T</i><sub>seek</sub>): The Voice-Coil Mechanics</h4>"
  )

  start_idx = content.find(start_marker)
  end_idx = content.find(end_marker)

  if start_idx != -1 and end_idx != -1:
    current_block = content[start_idx:end_idx].strip()
    if current_block != CORRECTED_FIGURE.strip():
      updated = (
          content[:start_idx]
          + CORRECTED_FIGURE.strip()
          + "\n\n    "
          + content[end_idx:]
      )
      with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated)
      print(f"--> Replaced Figure 2.2 with clean markup in {TARGET_FILE}")
    else:
      print("--> Figure 2.2 is already up-to-date and clean.")
  else:
    print("--> Notice: Boundary markers not matched as expected.")

  # Check git status
  status = (
      subprocess.check_output(["git", "status", "--porcelain"])
      .decode("utf-8")
      .strip()
  )
  if not status:
    print("--> Working tree is already clean. Nothing to commit or push.")
    return

  print(f"--> Changes detected:\n{status}")
  subprocess.run(["git", "add", "."], check=True)
  commit_msg = (
      "Fix SVG markup corruption in Figure 2.2 of Module 03\n\n"
      "Remove invalid HTML <sub> tags inside SVG text elements, repair\n"
      "timeline bar layout, and add a transfer inset callout."
  )
  subprocess.run(["git", "commit", "-m", commit_msg], check=True)
  subprocess.run(["git", "push", "origin", "main"], check=True)
  print("--> Successfully synced with origin main!")


if __name__ == "__main__":
  check_and_update()
