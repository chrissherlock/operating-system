#!/usr/bin/env python3
# =====================================================================
# fix.py: Insert one-paragraph MSR_LSTAR explanation in Chapter 3
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

MSR_PARAGRAPH = (
    "<p style=\\\"margin-top: 8px; font-size: 0.86rem; color: #0369a1; background: #f0f9ff; "
    "border: 1px solid #bae6fd; border-radius: 4px; padding: 8px 10px;\\\">"
    "<strong>What is MSR_LSTAR?</strong> <code>MSR_LSTAR</code> stands for <em>Model-Specific "
    "Register: Long System Target Address Register</em> (register address <code>0xC0000082</code>). "
    "Unlike 32-bit x86 systems that required slow memory accesses to look up software interrupts in "
    "the Interrupt Descriptor Table (IDT), 64-bit processors store the kernel's system call entry "
    "vector directly on the CPU die. During boot, the OS uses the privileged <code>wrmsr</code> "
    "instruction to write its entry routine (<code>entry_SYSCALL_64</code> on Linux, <code>KiSystemCall64</code> "
    "on Windows) into <code>MSR_LSTAR</code>. When an application issues <code>SYSCALL</code>, the "
    "processor hardware automatically loads <code>RIP</code> directly from this register in a single "
    "clock cycle, instantaneously transferring control to the supervisor."
    "</p>"
)

def update_chapter_3_explanation():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Search for Unix Chapter 3 'what' string
    unix_pattern = r'(stepNum:\s*"Chapter 3 of 6[^"]*",.*?what:\s*")(.*?)(")'
    match_unix = re.search(unix_pattern, content, flags=re.DOTALL)
    if match_unix:
        base_text = match_unix.group(2)
        # Avoid duplicating if already present
        if "What is MSR_LSTAR?" not in base_text:
            updated_text = base_text + MSR_PARAGRAPH
            content = content[:match_unix.start(2)] + updated_text + content[match_unix.end(2):]
            print("--> Added MSR_LSTAR paragraph to Linux/Unix Chapter 3.")

    # Search for Windows Chapter 3 'what' string
    # Re-run regex on modified content to get fresh indices
    win_pattern = r'(stepNum:\s*"Chapter 3 of 6: Crossing the Threshold[^"]*",.*?what:\s*")(.*?)(")'
    match_win = re.search(win_pattern, content, flags=re.DOTALL)
    if match_win:
        base_text_win = match_win.group(2)
        if "What is MSR_LSTAR?" not in base_text_win:
            updated_text_win = base_text_win + MSR_PARAGRAPH
            content = content[:match_win.start(2)] + updated_text_win + content[match_win.end(2):]
            print("--> Added MSR_LSTAR paragraph to Windows Chapter 3.")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Add single-paragraph MSR_LSTAR explanation to Chapter 3 walkthrough\n\n"
            "Explain MSR_LSTAR purpose, register index, and role in fast syscall\n"
            "vectoring directly within the active chapter pane of Module 2."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for Chapter 3 update!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_chapter_3_explanation()
