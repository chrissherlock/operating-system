#!/usr/bin/env python3
import base64
import os
import subprocess
import sys

def read_and_encode_audio(audio_path):
    print(f"--> Reading audio file from {audio_path}...")
    if not os.path.exists(audio_path):
        print(f"Error: Could not find audio file at {audio_path}", file=sys.stderr)
        sys.exit(1)
    with open(audio_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

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

def execute_deployment():
    audio_file = os.path.join("images", "defrag2.mp3")
    html_file = os.path.join("week10-file-management", "03-filesystem-implementation.html")

    base64_str = read_and_encode_audio(audio_file)
    data_uri = f"data:audio/mp3;base64,{base64_str}"

    print(f"--> Updating HTML file at {html_file}...")
    if not os.path.exists(html_file):
        print(f"Error: Could not find HTML file at {html_file}", file=sys.stderr)
        sys.exit(1)

    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure audio tag has correct base64 data URI
    import re
    new_audio_tag = f'<audio id="defragAudio" src="{data_uri}" preload="auto" loop></audio>'
    pattern = r'<audio\s+id="defragAudio"[^>]*>.*?</audio>|<audio\s+id="defragAudio"[^>]*/>'

    if re.search(pattern, content):
        content = re.sub(pattern, new_audio_tag, content)
    else:
        content = content.replace("</body>", f"  {new_audio_tag}\n</body>")

    # Fix image source paths to use relative ../images/ instead of absolute /images/
    content = content.replace('src="/images/ousterhout.png"', 'src="../images/ousterhout.png"')
    content = content.replace('src="/images/rosenblum.jpg"', 'src="../images/rosenblum.jpg"')

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("--> HTML file updated with correct relative image paths!")

    commit_msg = (
        "Fix relative image paths for pioneers portraits in LFS section\n\n"
        "Update week10-file-management/03-filesystem-implementation.html to use "
        "relative paths (../images/...) for John Ousterhout and Mendel Rosenblum's "
        "headshots so they load properly on GitHub Pages."
    )

    execute_git_command(["git", "add", html_file], "Staging HTML file")
    execute_git_command(["git", "commit", "-am", commit_msg], "Committing changes")
    execute_git_command(["git", "push", "origin", "main"], "Pushing changes to origin")
    print("--> Deployment complete!")

if __name__ == "__main__":
    execute_deployment()
