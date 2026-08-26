#!/usr/bin/env python3
import os
from pathlib import Path
import sys

OUTPUT_FILE = "project_structure_and_contents.txt"

# ── always skip these from tree and content ──
SKIP_TREE_ALWAYS = {
    "node_modules", ".git", "__pycache__", "dist", "build", ".nuxt",
    ".output", ".cache", ".expo", ".expo-shared", ".venv", "venv",
    "Pods", "DerivedData", "gradle", "wrapper", "xcshareddata",
    "xcuserdata", "debug", "Release", "main", "debugOptimized",
}

# ── skip these file extensions in content (binary / media) ──
SKIP_CONTENT_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".otf", ".mp3", ".mp4", ".mov",
    ".zip", ".rar", ".7z", ".exe", ".dll", ".bin", ".dat", ".pdf",
    ".lock", ".keystore", ".jks", ".apk", ".ipa", ".xcworkspace",
    ".xcodeproj", ".pbxproj", ".xcconfig", ".plist", ".entitlements",
    ".storyboard", ".xcprivacy", ".json", ".map", ".log",
}

# ── skip these exact filenames ──
SKIP_CONTENT_FILENAMES = {
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "yarn-error.log",
    ".DS_Store", "Thumbs.db", "desktop.ini", "LICENSE", "README.md",
    "Podfile.lock", "Manifest.lock", "gradle-wrapper.jar",
    "settings.gradle", "build.gradle", "proguard-rules.pro",
    "gradlew", "gradlew.bat", ".xcode.env", ".xcode.env.local",
    ".env", ".env.local", ".env.development", ".env.production",
    "theme.ts", "use-color-scheme.ts", "use-theme-color.ts",
    "themed-text.tsx", "themed-view.tsx",
}

# ── folders that are skipped entirely (tree + content) ──
SKIP_CONTENT_FOLDERS = SKIP_TREE_ALWAYS | {
    "assets", "images", "animations", "public", "css", "fonts", "media",
    "Local Podspecs", "Target Support Files", "Headers", "Private", "Public",
}


def is_binary_file(path: Path) -> bool:
    """Quick binary detection by checking for null bytes and common magic bytes."""
    try:
        with path.open("rb") as f:
            chunk = f.read(4096)
            if b"\0" in chunk:
                return True
            if chunk.startswith((b"\x89PNG", b"\xff\xd8\xff", b"%PDF")):
                return True
    except Exception:
        return True
    return False


def should_skip_tree(path: Path) -> bool:
    return any(part in SKIP_TREE_ALWAYS for part in path.parts)


def should_skip_content(path: Path) -> bool:
    if path.name in SKIP_CONTENT_FILENAMES:
        return True
    if path.suffix.lower() in SKIP_CONTENT_EXTENSIONS:
        return True
    if any(part in SKIP_CONTENT_FOLDERS for part in path.parts):
        return True
    if is_binary_file(path):
        return True
    return False


def write_project_tree(root: Path, fp):
    """Write the folder structure (tree) of the root directory."""
    fp.write("=== PROJECT STRUCTURE ===\n")
    all_entries = []

    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        cur = Path(dirpath)
        if should_skip_tree(cur):
            dirnames.clear()
            continue
        # filter subdirectories
        dirnames[:] = [d for d in dirnames if not should_skip_tree(cur / d)]
        dirnames.sort()
        filenames.sort()
        rel_path = cur.relative_to(root)
        all_entries.append((rel_path, dirnames[:], filenames[:]))

    # sort by depth, then by name
    all_entries.sort(key=lambda x: (len(x[0].parts), x[0]))

    printed_dirs = set()
    for rel_path, dirnames, filenames in all_entries:
        if rel_path == Path("."):
            continue
        parts = rel_path.parts
        # print ancestor directories if not printed yet
        for depth in range(1, len(parts) + 1):
            prefix = Path(*parts[:depth])
            if prefix not in printed_dirs:
                indent = "│   " * (depth - 1)
                fp.write(f"{indent}├── {parts[depth-1]}/\n")
                printed_dirs.add(prefix)

        indent = "│   " * (len(parts) - 1) if len(parts) > 1 else ""
        children = dirnames + filenames
        for i, name in enumerate(children):
            is_last = i == len(children) - 1
            branch = "└── " if is_last else "├── "
            suffix = "/" if name in dirnames else ""
            fp.write(f"{indent}{branch}{name}{suffix}\n")


def write_text_contents(root: Path, fp):
    """Write the textual content of all non‑skipped files."""
    fp.write("\n=== TEXT FILE CONTENTS ===\n\n")
    text_files = []

    for dirpath, _, filenames in os.walk(root):
        cur = Path(dirpath)
        if should_skip_tree(cur):
            continue
        for fn in sorted(filenames):
            path = cur / fn
            if should_skip_content(path):
                continue
            text_files.append(path)

    text_files.sort()
    for path in text_files:
        rel = path.relative_to(root)
        fp.write(f"--- {rel} ---\n")
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            fp.write(content.rstrip() + "\n\n")
        except Exception as e:
            fp.write(f"[ERROR reading file: {e}]\n\n")


def main():
    # Use the provided directory or the current working directory
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1]).resolve()
        if not root_dir.is_dir():
            print(f"Error: '{root_dir}' is not a valid directory.", file=sys.stderr)
            return 1
    else:
        root_dir = Path.cwd()

    output_path = root_dir / OUTPUT_FILE
    with open(output_path, "w", encoding="utf-8") as f:
        write_project_tree(root_dir, f)
        write_text_contents(root_dir, f)

    print(f"\n✅ Done. Output written to: {output_path}")
    print(f"Scanned root: {root_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())