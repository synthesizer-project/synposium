# Synposium

Synposium collects Synthesizer presentations and deduplicated assets for reuse in future talks.

## Layout

- `slides/`: native presentation files, grouped by format; hosted slide links live in `google-docs.txt`.
- `assets/`: reusable plots, images, diagrams, animations, equations, logos, screenshots, and media.
- `MINE_TALKS_PROMPT.md`: prompt for importing and mining collections of talks.
- `tools/`: checks for duplicate or misplaced assets and missing Git LFS coverage.

## Add a talk

1. Install Git LFS with `git lfs install`.
2. Add the native presentation under the matching `slides/` directory; do not add ZIP archives.
3. Add only useful, globally deduplicated assets under the matching `assets/` directory.
4. Run `python3 tools/verify_assets.py` and `python3 tools/verify_lfs.py`.
5. Push a branch and raise a pull request. Talks must be merged through PRs, not added directly to `main`.
