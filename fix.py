#!/usr/bin/env python3
import os
import subprocess
import sys

def execute_git_command(cmd, desc):
    print(f"--> {desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout.strip():
        print(res.stdout.strip())
    if res.stderr.strip():
        print(f"[{desc} stderr]\n{res.stderr.strip()}")
    if res.returncode != 0 and "nothing to commit" not in res.stdout and "nothing to commit" not in res.stderr:
        print(f"Error during {desc} (code {res.returncode})", file=sys.stderr)
        sys.exit(res.returncode)

def execute_restoration_and_patch():
    html_file = os.path.join("week10-file-management", "03-filesystem-implementation.html")

    # Step 1: Revert the file to the fully fleshed-out commit prior to the overwrite
    execute_git_command(["git", "checkout", "HEAD~1", "--", html_file], "Restoring full file from git history")

    print(f"--> Reading restored content from {html_file}...")
    if not os.path.exists(html_file):
        print(f"Error: Could not find {html_file} after git checkout", file=sys.stderr)
        sys.exit(1)

    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Step 2: Define the Database Pioneers Infobox HTML block
    pioneers_html = r"""
      <!-- DATABASE PIONEERS INFOBOX (Jim Gray & C. Mohan) -->
      <div class="pioneers-infobox">
        <h4>Database Pioneers: Jim Gray &amp; C. Mohan (Transaction Processing &amp; WAL Theory)</h4>
        <div class="pioneers-portraits">
          <div class="pioneer-card">
            <div class="pioneer-top">
              <img src="https://upload.wikimedia.org/wikipedia/commons/7/76/Jim_Gray_Computing_in_the_21st_Century_2006.jpg" alt="Jim Gray">
              <div class="pioneer-info">
                <strong><a href="https://en.wikipedia.org/wiki/Jim_Gray_(computer_scientist)" target="_blank" style="color: var(--accent); text-decoration: none;">Jim Gray (James N. Gray)</a></strong>
                <span>IBM, Tandem &amp; Microsoft Research &bull; <a href="https://en.wikipedia.org/wiki/Jim_Gray_(computer_scientist)" target="_blank" style="color: var(--accent); text-decoration: underline;">Wikipedia Entry</a></span>
                <span>Turing Award Laureate (1998)</span>
              </div>
            </div>
            <div class="pioneer-bio">
              Pioneered transaction processing, database atomicity, locking, and crash-recovery protocols. His foundational work on System R and distributed transactions laid the blueprint for Write-Ahead Logging and reliable data-intensive computing.
            </div>
          </div>
          <div class="pioneer-card">
            <div class="pioneer-top">
              <img src="https://duk.ac.in/seemohan/Mohan%20Portrait%20Interconnect%20Las%20Vegas%20Heidi%20Jeanne%20Angle%20Joanne%20Weaver%203-2017%20mohan_c_mohan_m18_2%20lg%20e.jpg" alt="C. Mohan">
              <div class="pioneer-info">
                <strong><a href="https://en.wikipedia.org/wiki/C._Mohan" target="_blank" style="color: var(--accent); text-decoration: none;">C. Mohan (Chandrasekaran Mohan)</a></strong>
                <span>IBM Fellow &bull; <a href="https://en.wikipedia.org/wiki/C._Mohan" target="_blank" style="color: var(--accent); text-decoration: underline;">Wikipedia Entry</a></span>
                <span><a href="https://duk.ac.in/seemohan/" target="_blank" style="color: var(--text-muted); text-decoration: underline;">Photo Credit: Digital University Kerala</a></span>
              </div>
            </div>
            <div class="pioneer-bio">
              Master innovator in database systems best known for co-authoring the <strong>ARIES</strong> recovery and concurrency control system. His rigorous protocols solved the theoretical challenges of Write-Ahead Logging and crash recovery used across modern databases and filesystems.
            </div>
          </div>
        </div>
        <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">
          Historical Source Reference: Tony Hey, Stewart Tansley, Kristin Tolle (Eds.): <em>The Fourth Paradigm: Data-Intensive Scientific Discovery</em>. Microsoft Research, 2009.
        </div>
      </div>
"""

    # Step 3: Insert the infobox cleanly into Section 4.3.6
    target_string = "<h2>4.3.6 Journaling File Systems</h2>"
    if target_string not in content:
        # Fallback target if header wording differs slightly
        target_string = "<h2>4.3.6 Journaling File Systems"

    if target_string in content:
        # Insert right after the section header paragraph / opening
        parts = content.split(target_string)
        # Find closing tag of the intro paragraph or insert right after header
        insertion_point = parts[1].find("</p>") + 4
        new_content = parts[0] + target_string + parts[1][:insertion_point] + pioneers_html + parts[1][insertion_point:]
    else:
        print("Error: Could not locate Section 4.3.6 header in restored file.", file=sys.stderr)
        sys.exit(1)

    print(f"--> Writing patched full content back to {html_file}...")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("--> File restored and successfully patched!")

    # Step 4: Commit and push changes
    commit_msg = (
        "Restore full file content and add database pioneers to section 4.3.6\n\n"
        "Restore week10-file-management/03-filesystem-implementation.html from git "
        "history and cleanly insert the Jim Gray and C. Mohan pioneers infobox "
        "into section 4.3.6 without losing any material."
    )

    execute_git_command(["git", "add", html_file], "Staging restored and patched HTML file")
    execute_git_command(["git", "commit", "-am", commit_msg], "Committing restoration")
    execute_git_command(["git", "push", "origin", "main"], "Pushing changes to origin")
    print("--> Deployment and restoration complete!")

if __name__ == "__main__":
    execute_restoration_and_patch()
