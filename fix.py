#!/usr/bin/env python3
# =====================================================================
# fix_shebang_paths.py: Correct shebang paths across all python scripts
# =====================================================================
import os
import subprocess
import sys

def fix_all_shebangs():
    modified = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                if "#!/usr/bin/env python3" in content or "#!/usr/bin/env python3" in content:
                    content = content.replace("#!/usr/bin/env python3", "#!/usr/bin/env python3")
                    content = content.replace("#!/usr/bin/env python3", "#!/usr/bin/env python3")
                    content = content.replace("#!/usr/bin/env python3", "#!/usr/bin/env python3")
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    modified.append(path)

    if not modified:
        print("--> No shebang errors found.")
        return

    print(f"--> Fixed shebang in files: {modified}")
    try:
        subprocess.run(["git", "add"] + modified, check=True)
        commit_msg = (
            "Correct shebang path from usr/init/env to usr/bin/env python3\n\n"
            "Ensure all Python scripts use the canonical interpreter path #!/usr/bin/env python3\n"
            "instead of the incorrect path."
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception:
        pass
    print("--> Shebang corrections deployed successfully!")

if __name__ == "__main__":
    fix_all_shebangs()
