# Mine slide assets

You are organizing a repository of talks and reusable presentation assets.

Before changing anything, ask me:

1. Where are my slides stored?
2. Which presentation software and file formats do I use, such as Keynote, PowerPoint, Google Slides, PDF, LibreOffice Impress, or another tool?
3. Is this a first import or an update, and which talks have already been contributed?

Do not assume these answers. Adapt the directory names and extraction process to the formats I name. If files are in cloud storage, identify placeholders and ensure each file is fully downloaded before copying it. Do not force downloads by repeatedly reading entire files; request native cloud-provider downloads and report anything still pending.

Then:

1. Inspect the repository and preserve its existing conventions.
2. Inventory existing presentations and assets by filename and SHA-256 before importing anything. For an update, skip presentations whose name and content hash already match. Treat a new name as a new talk and a matching name with a different hash as an update. Replace the repository copy only when I confirm it should represent the latest version; otherwise preserve both with a meaningful version suffix.
3. Create one format-specific directory under `slides/` for each kind of presentation I use. Keep those directories at the same level. If I use hosted presentations, create a text file under `slides/` for their URLs. Create `assets/` with useful type-specific subdirectories such as `images/`, `plots/`, `animations/`, `diagrams/`, `equations/`, `logos/`, `screenshots/`, `video/`, `audio/`, `pdfs/`, and `other/`.
4. Copy only new or confirmed-updated presentations from the location I provide, leaving every source file in place. Ignore filesystem metadata such as `.DS_Store`.
5. Preserve every presentation in its native format. For package-based formats, create a temporary validated ZIP archive only when needed for extraction; Keynote files are usually ZIP containers, while Keynote package directories must be archived first. Remove temporary archives after successful extraction. Never delete or move a source.
6. Extract new or updated talks into a temporary directory. Use the native file, format package structure, or standard export tools rather than lossy screenshots. Exclude application-generated thumbnails, poster frames, blank placeholders, and other package internals. For Keynote, common junk includes `*-small-*`, `mt-*`, `st-*`, `posterImage-*`, and `blankMoviePosterImage-*`. Classify retained files under the appropriate asset-type directory and strip meaningless package-generated numeric suffixes from filenames.
7. Deduplicate new assets against the entire existing asset collection by content hash, not filename. Add only unseen content. If cleaned filenames collide but content differs, retain both using a short content hash in the second filename. Never overwrite silently. During updates, do not delete existing assets as "stale" unless I explicitly request cleanup; another talk may still use them.
8. Before adding binaries, run `git lfs version` and `git lfs install --local`. If Git LFS is unavailable, stop and ask me to install it. Reuse existing `.gitattributes` rules and add only missing binary formats. Stage `.gitattributes` with or before binary files. After staging, confirm every tracked binary appears in `git lfs ls-files`.
9. Run `python3 tools/verify_assets.py` and `python3 tools/verify_lfs.py`. Inspect the mined output before finishing. Report talks skipped as unchanged, talks added or updated, raw extracted count, generated junk removed, exact duplicates removed, and final unique count. Report anything that could not be downloaded, validated, classified, copied, or extracted.

Prefer standard operating-system tools and the smallest reliable implementation. Do not commit or push unless I ask.
