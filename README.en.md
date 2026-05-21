[简体中文](./README.md) | English

# Multiple Personality System Wiki

> A Chinese-language knowledge base and open-source collaborative project on plural systems and related mental health topics.
> This wiki is committed to providing neutral, objective information. All updates are user-oriented and are not influenced by community disputes, political events, or ideological factors.
> Live site: <https://wiki.mpsteam.cn/>

[![Cloudflare Pages](https://img.shields.io/badge/Cloudflare%20Pages-deployed-brightgreen?logo=cloudflare)](https://wiki.mpsteam.cn/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/mps-team-cn/Multiple_personality_system_wiki?style=social)](https://github.com/mps-team-cn/Multiple_personality_system_wiki/stargazers)

---

📖 Note: General readers should visit the live site at [wiki.mpsteam.cn](https://wiki.mpsteam.cn/). This document is intended for developers and contributors.

---

## ✨ Project Goals

- Collect and organize high-quality Chinese-language resources on plural systems (Multiple Personality System) and related mental health topics;
- Maintain consistent entry standards and contribution workflows to ensure maintainability, citability, and extensibility;
- Serve both general readers and professionals, balancing readability with rigor (informed by E-E-A-T principles).

---

## 🛠️ Tech Stack

### Frontend & Runtime

- MkDocs Material (static site generator)
- Python ≥ 3.10 (build and toolchain)

### Core Plugins & Features

- `mkdocs-material` · `pymdown-extensions` · Rich Markdown syntax and components
- `mkdocs-git-revision-date-localized-plugin` · Git-based last-updated display
- `mkdocs-minify-plugin` · HTML/CSS/JS minification
- `mkdocs-glightbox` · Image lightbox
- `mkdocs-exclude` · Build-time exclusion
- `mkdocs-exclude-search` · Search index exclusion
- `search + jieba` · Chinese word segmentation + custom dictionary (`data/user_dict.txt`)

### Content Management & Deployment

- Sveltia CMS (frontend CMS) → path: `/admin` ([live admin panel](https://wiki.mpsteam.cn/admin/))
- Cloudflare Functions (`functions/api/auth.ts`) for GitHub OAuth proxy
- Cloudflare Pages: automated build and deployment (build script: `.cfpages-build.sh`)

---

## 📦 Repository Structure (abridged)

```text
Multiple_personality_system_wiki/
├─ README.md                     # This file (for developers/contributors)
├─ AGENTS.md                     # Development conventions (mandatory)
├─ CONTRIBUTING.md               # Contribution guide (overview)
├─ mkdocs.yml                    # Site config (theme/plugins/navigation)
├─ requirements.txt              # Python dependencies
├─ .cfpages-build.sh             # Cloudflare Pages build script
│
├─ docs/
│  ├─ index.md                  # Homepage
│  ├─ Preface.md                # Preface
│  ├─ Glossary.md               # Glossary
│  ├─ tags.md                   # Tag index
│  ├─ changelog.md              # Changelog
│  ├─ TEMPLATE_ENTRY.md         # Entry template (must-read)
│  ├─ ADMIN_GUIDE.md            # Admin guide
│  ├─ GITHUB_WORKFLOW.md        # GitHub workflow guide
│  ├─ dev/                      # Developer docs
│  ├─ admin/                    # Sveltia CMS (index.html / config.yml / admin.css)
│  ├─ assets/                   # Static assets: CSS/JS/icons (incl. mid60 component)
│  ├─ entries/                  # Entry directory (no subdirectories)
│  ├─ guides/                   # Index and navigation files (no subdirectories)
│  └─ includes/                 # Reusable snippets (e.g. abbreviation tables)
│
├─ tools/                       # Maintenance scripts and utilities
│  ├─ fix_markdown.py           # Markdown auto-fix
│  ├─ check_links.py            # Link convention checker
│  ├─ update_git_timestamps.py  # Update timestamps from Git history
│  └─ pdf_export/               # PDF export tools
│
├─ functions/api/auth.ts        # GitHub OAuth proxy (Sveltia CMS login)
├─ .github/workflows/           # CI (PR quality checks / post-merge auto-fix)
└─ releases/                    # Historical release artifacts (e.g. PDFs)
```

---

## 🚀 Quick Start

We recommend using [uv](https://docs.astral.sh/uv/) for dependency and virtual environment management.

```bash

# Install dependencies (auto-creates an isolated .venv)

uv sync

# Local preview with hot reload

uv run mkdocs serve

# Visit: http://127.0.0.1:8000

```

### Build Static Site

```bash

# Standard build (output to site/)

uv run mkdocs build

# Strict mode (fail on warnings)

uv run mkdocs build --strict
```

---

## 🤖 Automation & Tooling

The `tools/` directory contains content maintenance utilities. See `docs/dev/Tools-Index.md` for full documentation.

- `uv run python3 tools/fix_markdown.py [path]` — Auto-fix Markdown formatting (supports `--dry-run`)
- `uv run python3 tools/check_links.py [path]` — Link convention checker (context-aware)
- `uv run python3 tools/update_git_timestamps.py` — Update timestamps from Git history
- PDF export: `uv run python3 tools/pdf_export/export_to_pdf.py`

Two-tier CI (see `.github/workflows/`):

- PR stage: `pr-check.yml` checks link conventions, Frontmatter, and tag conventions
- Post-merge: `auto-fix-entries.yml` auto-updates timestamps, fixes formatting, and re-validates

---

## 🧭 Contributing

Contributions are welcome! First-time contributors should read:

- Contribution guide: `docs/contributing/index.md`
- Entry template: `docs/TEMPLATE_ENTRY.md`
- Development conventions: `AGENTS.md`

Pre-submit checklist:

- Entries are placed in `docs/entries/` (no subdirectories)
- Frontmatter includes `title / topic / tags` (timestamps are maintained by CI)
- Run: `uv run python3 tools/fix_markdown.py docs/entries/`
- Run: `uv run python3 tools/check_links.py docs/entries/`
- Run: `uv run python3 tools/check_tags.py docs/entries/`
- Build passes: `uv run mkdocs build --strict`

When adding or modifying entries, update the corresponding topic Guide (see the mapping table in `AGENTS.md`).

---

## 📦 Deployment

Automated build and deployment via Cloudflare Pages:

```yaml
Build command: bash .cfpages-build.sh
Build output directory: site
```

Live site: <https://wiki.mpsteam.cn/>

---

## 📄 License

- **Code and tooling** (such as `tools/`, `functions/`, config files, and scripts) are licensed under the [MIT License](LICENSE)
- **Content materials** (unless otherwise noted, including text content under `docs/`, release artifacts under `releases/`, and PDF exports distributed in this repository) are licensed under [CC BY-SA 4.0](LICENSE-CONTENT)

If a specific file or page contains its own source, copyright, or license
notice, that notice takes precedence.

---

## 📮 Feedback & Contact

- Content feedback: support@mpsteam.cn (errors, suggestions, usage issues)
- Official contact: contact@mpsteam.cn (partnerships, media inquiries, other matters)
- GitHub Issues: <https://github.com/mps-team-cn/Multiple_personality_system_wiki/issues>

---

## ⭐ Star History

If you find this project useful, please give it a star ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=mps-team-cn/Multiple_personality_system_wiki&type=Date)](https://star-history.com/#mps-team-cn/Multiple_personality_system_wiki&Date)
