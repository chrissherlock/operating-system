#!/usr/bin/env python3
# =====================================================================
# fix.py: Explain and update MSR_LSTAR context in 02-hardware-review.html
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def update_msr_lstar_context():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Enhanced explanation for Unix Chapter 3
    old_unix_ch3 = (
        'what: "The CPU microcode has taken control and crossed the silicon wall. '
        'It has cleared the Mode Bit from <code>1</code> to <code>0</code>, saved the user '
        'Program Counter and Stack Pointer onto the process\'s private kernel stack, and '
        'branched to the kernel entry point stored in the CPU\'s Model-Specific Register '
        '(<code>MSR_LSTAR</code>)."'
    )

    new_unix_ch3 = (
        'what: "The CPU microcode has taken control and crossed the silicon wall. '
        'It clears the Mode Bit from <code>1</code> to <code>0</code>, saves the return '
        'Program Counter into <code>RCX</code> and flags into <code>R11</code>, swaps to '
        'the private kernel stack, and directly sets the instruction pointer to the address '
        'stored in <code>MSR_LSTAR</code> (Model-Specific Register 0xC0000082, the Long System '
        'Target Address Register pointing to <code>entry_SYSCALL_64</code>)."'
    )

    old_unix_ch3_why = (
        'why: "The CPU switches to a private kernel stack because user-space memory is untrusted. '
        'If the kernel used the user\'s stack, a malicious concurrent thread could rewrite return '
        'addresses while the kernel was running in Ring 0, hijacking the supervisor."'
    )

    new_unix_ch3_why = (
        'why: "Early x86 processors used software interrupts (<code>INT 0x80</code>) that required '
        'expensive memory reads through the Interrupt Descriptor Table (IDT). With 64-bit <code>syscall</code>, '
        'the CPU reads the target kernel function pointer directly from high-speed on-die silicon '
        '(<code>MSR_LSTAR</code>), eliminating IDT lookups. The kernel stack swap ensures unprivileged '
        'threads cannot tamper with supervisor call frames."'
    )

    # Enhanced explanation for Windows Chapter 3
    old_win_ch3 = (
        'what: "The CPU hardware has caught the trap. It has set Mode Bit = 0, loaded the '
        'privileged kernel stack pointer from the active thread\'s <code>KTHREAD</code> structure, '
        'and branched directly to the entry point stored in <code>MSR_LSTAR</code>: '
        '<code>KiSystemCall64</code> inside <code>ntoskrnl.exe</code>."'
    )

    new_win_ch3 = (
        'what: "The CPU hardware catches the trap. It sets Mode Bit = 0, loads the privileged '
        'kernel stack pointer from <code>KTHREAD.InitialStack</code>, and loads <code>RIP</code> '
        'directly from <code>MSR_LSTAR</code> (Long System Target Address Register), jumping straight '
        'into <code>ntoskrnl.exe!KiSystemCall64</code> with zero IDT memory lookup latency."'
    )

    old_win_ch3_why = (
        'why: "Switching to an isolated kernel stack in silicon ensures that user-mode code cannot '
        'tamper with execution context while running in supervisor mode. The processor hardware '
        'enforces this boundary before executing any kernel instructions."'
    )

    new_win_ch3_why = (
        'why: "By caching the kernel entry vector in the dedicated <code>MSR_LSTAR</code> register '
        'during Windows initialization, 64-bit systems bypass legacy software interrupt dispatching. '
        'The processor atomically switches to a secure kernel stack and begins executing <code>KiSystemCall64</code> '
        'before user-mode threads can observe or modify CPU state."'
    )

    content = content.replace(old_unix_ch3, new_unix_ch3)
    content = content.replace(old_unix_ch3_why, new_unix_ch3_why)
    content = content.replace(old_win_ch3, new_win_ch3)
    content = content.replace(old_win_ch3_why, new_win_ch3_why)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"--> Updated MSR_LSTAR narrative panels in {TARGET_FILE}")

    try:
        subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
        commit_msg = (
            "Clarify MSR_LSTAR hardware dispatch in Syscall Story simulator\n\n"
            "Expand Chapter 3 explanatory panes in 02-hardware-review.html to\n"
            "demystify MSR_LSTAR (Model-Specific Register) and fast syscall entry."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully for MSR_LSTAR clarification!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    update_msr_lstar_context()
