import os
import re
import datetime

# CONFIG 

root_dir = r"C:\Users\taman\Desktop\PythonTut\13-Flask\Flask-ToDo_App"
output_file = r"C:\Users\taman\Desktop\Projects\Project_txt_files\flask_todo_project.txt"


# root_dir = r"C:\Users\taman\Desktop\Projects\shopify-ai-analytics"
# output_file = r"C:\Users\taman\Desktop\Projects\Project_txt_files\shopify_project.txt"


excluded_files = {
    ".", "..",
    "25.3",
    "LICENSE.txt",
    "db.sqlite3",
    "package-lock.json",
    "react.svg",
}

excluded_dirs = {
    ".", "..",
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "node_modules",
}

ALLOWED_EXTENSIONS = (
    ".py", ".js", ".ts", ".json", ".md",
    ".txt", ".html", ".css", ".yml", ".yaml", ".rb", ".sh"
)

# ================= UTILITIES =================

def generate_tree(root, prefix=""):
    lines = []
    try:
        entries = sorted(
            e for e in os.listdir(root)
            if e not in excluded_dirs and e not in excluded_files
        )
    except PermissionError:
        return lines

    for index, entry in enumerate(entries):
        path = os.path.join(root, entry)
        connector = "└── " if index == len(entries) - 1 else "├── "
        lines.append(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "    " if index == len(entries) - 1 else "│   "
            lines.extend(generate_tree(path, prefix + extension))

    return lines

# ================= VERSIONING =================

major, minor, patch = 0, 0, 0

if os.path.exists(output_file):
    try:
        with open(output_file, "r", encoding="utf-8") as existing:
            first_line = existing.readline().strip()
            match = re.match(r"^Version:\s*(\d+)\.(\d+)\.(\d+)", first_line)
            if match:
                major, minor, patch = map(int, match.groups())
    except Exception:
        pass  # silent reset is intentional

patch += 1
if patch >= 10:
    patch = 0
    minor += 1
    if minor >= 10:
        minor = 0
        major += 1

version_str = f"{major}.{minor}.{patch}"

now = datetime.datetime.now()
date_str = now.strftime("%d-%m-%Y")
time_str = now.strftime("%H:%M")

# ================= WRITE OUTPUT =================

os.makedirs(os.path.dirname(output_file), exist_ok=True)

try:
    with open(output_file, "w", encoding="utf-8") as out:
        out.write(f"Version: {version_str} | Updated: {date_str} | {time_str}\n")
        out.write("=" * 50 + "\n\n")

        # ---- TREE ----
        out.write("# Project Structure:\n")
        out.write("\n".join(generate_tree(root_dir)))
        out.write("\n\n")

        # ---- FILE CONTENTS ----
        for foldername, subfolders, filenames in os.walk(root_dir):
            subfolders[:] = [d for d in subfolders if d not in excluded_dirs]

            for filename in filenames:
                if filename in excluded_files:
                    continue
                if not filename.endswith(ALLOWED_EXTENSIONS):
                    continue

                filepath = os.path.join(foldername, filename)
                relpath = os.path.relpath(filepath, root_dir)

                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception:
                    continue

                out.write(f"\n\n# Path: {relpath}\n\n")
                out.write(content)
                out.write("\n")

    print(f"✅ Project exported successfully (Version {version_str})")

except Exception as e:
    print(f"❌ Failed to write project file: {e}")
