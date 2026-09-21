#!/usr/bin/env python3
# =====================================================================
# fix.py: Replace &amp; leaks with literal & in 02-hardware-review.html
# =====================================================================
import os
import re
import subprocess

TARGET_FILE = os.path.join("week01-operating-system-concepts", "02-hardware-review.html")

def sanitize_ampersands():
    if not os.path.exists(TARGET_FILE):
        print(f"Error: {TARGET_FILE} not found.")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Clean JS script strings where &amp; was passed to textContent or innerHTML
    # Target script blocks specifically
    def clean_script_block(match):
        script_body = match.group(0)
        # Replace &amp; inside script strings with literal &
        cleaned = script_body.replace("&amp;", "&")
        return cleaned

    new_content = re.sub(r'<script\b[^>]*>.*?</script>', clean_script_block, content, flags=re.DOTALL)

    # 2. Clean SVG text nodes where &amp; was used inside text content
    def clean_svg_text(match):
        svg_body = match.group(0)
        # In SVG <text> elements, replace &amp; with literal &
        cleaned = re.sub(r'(<text\b[^>]*>)(.*?)(</text>)', lambda m: m.group(1) + m.group(2).replace("&amp;", "&") + m.group(3), svg_body, flags=re.DOTALL)
        return cleaned

    new_content = re.sub(r'<svg\b[^>]*>.*?</svg>', clean_svg_text, new_content, flags=re.DOTALL)

    # 3. Clean specific node titles that leak into UI cards
    node_replacements = [
        ('node2Title: "kernel32 &amp; ntdll"', 'node2Title: "kernel32 & ntdll"'),
        ('node4Title: "VFS &amp; NVMe Driver"', 'node4Title: "VFS & NVMe Driver"'),
        ('node5Title: "VFS &amp; NVMe Driver"', 'node5Title: "VFS & NVMe Driver"'),
        ('node5Title: "I/O Manager &amp; Drivers"', 'node5Title: "I/O Manager & Drivers"'),
        ('node5Title: "ntfs.sys &amp; stornvme.sys"', 'node5Title: "ntfs.sys & stornvme.sys"'),
        ('node3Title: "vmlinuz &amp; initramfs"', 'node3Title: "vmlinuz & initramfs"'),
        ('node4Title: "vmlinuz &amp; initramfs"', 'node4Title: "vmlinuz & initramfs"'),
        ('node4Title: "winload &amp; ntoskrnl"', 'node4Title: "winload & ntoskrnl"'),
        ('node5Title: "smss &amp; csrss"', 'node5Title: "smss & csrss"'),
        ('&amp;rarr;', '→'),
        ('&amp;larr;', '←'),
        ('&amp;bull;', '•'),
    ]

    for old, new in node_replacements:
        new_content = new_content.replace(old, new)

    if new_content != content:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("--> Replaced leaking &amp; instances with clean characters.")

        try:
            subprocess.run(["git", "add", "fix.py", TARGET_FILE], check=True)
            commit_msg = (
                "Replace leaking &amp; entities with literal ampersands in Module 2\n\n"
                "Clean up JavaScript data objects and SVG text labels in\n"
                "02-hardware-review.html so ampersands render properly as plain text."
            )
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("--> Git sync completed successfully for 02-hardware-review.html!")
        except Exception as e:
            print(f"Git execution note: {e}")
    else:
        print("--> No leaking &amp; found in targeted sections.")

if __name__ == "__main__":
    sanitize_ampersands()
