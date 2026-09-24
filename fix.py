#!/usr/bin/env python3
# =====================================================================
# fix.py: Restore week06-synchronisation-and-deadlock/index.html stub
# =====================================================================
import os
import subprocess

LEGACY_DIR = "week06-synchronisation-and-deadlock"
CANONICAL_URL = "../week06-synchronization-and-deadlock/index.html"

STUB_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url={CANONICAL_URL}">
  <title>Redirecting to Week 6 Synchronization &amp; Deadlock</title>
</head>
<body>
  <p>Redirecting to <a href="{CANONICAL_URL}">Week 6 Synchronization &amp; Deadlock Hub</a>...</p>
</body>
</html>
"""

def restore_legacy_stub():
    os.makedirs(LEGACY_DIR, exist_ok=True)
    stub_path = os.path.join(LEGACY_DIR, "index.html")
    with open(stub_path, "w", encoding="utf-8") as f:
        f.write(STUB_HTML.strip() + "\n")
    print(f"--> Restored compatibility redirect stub at {stub_path}")

def run_git_sync():
    try:
        subprocess.run(["git", "add", "fix.py", LEGACY_DIR], check=True)
        commit_msg = (
            "Restore week06-synchronisation-and-deadlock/index.html as redirect stub\n\n"
            "Provide a compatibility redirect stub for the British spelling directory\n"
            "to prevent 404 errors on legacy links pointing to week06-synchronisation."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("--> Git sync completed successfully!")
    except Exception as e:
        print(f"Git execution note: {e}")

if __name__ == "__main__":
    restore_legacy_stub()
    run_git_sync()
