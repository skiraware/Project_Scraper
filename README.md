# Project Scraper

A universal Python script that exports your entire project structure and the contents of every text based file into a single flat file. It smartly skips binaries, images, dependencies, build artifacts, and temporary files.

## Purpose

Quickly ingest your whole codebase into a single document for sharing, analysis, or feeding into large language models.

## Usage

Place the script anywhere, then run:

`python project_scraper.py`

To scan a specific directory instead of the current folder:

`python project_scraper.py /path/to/your/project`

## Output

The script generates `project_structure_and_contents.txt` inside the scanned root folder. This file contains:

* a hierarchical tree view of all folders and files
* the full UTF‑8 text content of every code, config, and markup file, appended sequentially

## What gets skipped automatically

The scraper ignores the following types of items to keep the output clean and manageable:

* dependency folders like `node_modules`, `.venv`, and `Pods`
* version control directories such as `.git`
* build outputs including `dist`, `build`, `.nuxt`, and `.expo`
* binary and media files: images, fonts, audio, video, archives, and executables
* lock files, log files, environment files, and package manager lockfiles (package‑lock.json, yarn.lock, etc.)
* common binary detection via null bytes and magic headers

## Customization

Open the script and adjust the sets at the top:

* `SKIP_TREE_ALWAYS` for folders excluded from both tree and content
* `SKIP_CONTENT_EXTENSIONS` for file extensions to omit from the text dump
* `SKIP_CONTENT_FILENAMES` for exact file names to exclude
* `SKIP_CONTENT_FOLDERS` for additional folders to hide

Modify these lists to tailor the scraper to your specific project needs.

## License

MIT. Use freely, but no warranties or guarantees are provided.