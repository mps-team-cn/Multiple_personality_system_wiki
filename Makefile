SHELL := /bin/sh

UV ?= uv
PYTHON ?= python3
DOCS_DIR ?= docs
STATUS_DIRS ?= docs/entries docs/guides
ENTRIES_DIR ?= docs/entries
MARKDOWNLINT ?= markdownlint
MARKDOWN_FILES ?= docs/**/*.md
PDF_ENGINE ?= tectonic
CJK_FONT ?= Microsoft YaHei
PDF_OUTPUT ?= releases/Multiple_Personality_System_wiki.pdf
PDF_EXTRA_ARGS ?=
STATUS_TOP ?= 10

.PHONY: help status links tags frontmatter build serve pdf fix lint check all

help:
	@printf '%s\n' \
		'可用命令:' \
		'  make help         查看帮助' \
		'  make status       统计 entries/guides Markdown 文件概况' \
		'  make links        检查 docs/ 下的 Markdown 链接规范' \
		'  make tags         检查词条标签规范' \
		'  make frontmatter  检查词条 Frontmatter' \
		'  make build        构建 MkDocs 站点' \
		'  make serve        启动本地预览服务' \
		'  make pdf          导出 PDF' \
		'  make fix          修复 docs/entries/ 下的 Markdown 格式' \
		'  make lint         运行 markdownlint' \
		'  make check        依次执行 links/tags/frontmatter/build' \
		'  make all          执行 check 和 pdf' \
		'' \
		'常用变量:' \
		'  DOCS_DIR=docs' \
		'  STATUS_DIRS="docs/entries docs/guides"' \
		'  ENTRIES_DIR=docs/entries' \
		'  STATUS_TOP=10' \
		'  PDF_ENGINE=tectonic' \
		'  CJK_FONT=Microsoft YaHei' \
		'  PDF_OUTPUT=releases/Multiple_Personality_System_wiki.pdf' \
		'  PDF_EXTRA_ARGS=...' \
		'' \
		'示例:' \
		'  make status' \
		'  make status STATUS_DIRS="docs/entries"' \
		'  make status STATUS_TOP=20' \
		'  make check' \
		'  make pdf PDF_ENGINE=xelatex CJK_FONT="Noto Serif CJK SC"' \
		'  make pdf PDF_OUTPUT=dist/wiki.pdf PDF_EXTRA_ARGS='\''--include-tags "guide:入门指南"'\'''

status:
	@printf '%s\n' 'Markdown 状态统计'
	@printf '%s\n' '=================='
	@printf '目录: %s\n' "$(STATUS_DIRS)"
	@printf 'Markdown 文件数: %s\n' "$$(find $(STATUS_DIRS) -type f -name '*.md' | wc -l | awk '{print $$1}')"
	@printf '总行数: %s\n' "$$(find $(STATUS_DIRS) -type f -name '*.md' -exec wc -l {} + | awk 'END {print $$1}')"
	@printf '非空白字符数: %s\n' "$$(find $(STATUS_DIRS) -type f -name '*.md' -exec cat {} + | tr -d '[:space:]' | wc -m | awk '{print $$1}')"
	@if [ -f mkdocs.yml ]; then \
		printf '%s\n' 'MkDocs 配置: 已检测到 mkdocs.yml'; \
	else \
		printf '%s\n' 'MkDocs 配置: 未检测到 mkdocs.yml'; \
	fi
	@printf '\n%s\n' "最长文件 Top $(STATUS_TOP)（按行数排序）:"
	@find $(STATUS_DIRS) -type f -name '*.md' -exec wc -l {} + | sort -nr | awk -v top="$(STATUS_TOP)" '$$2 != "total" && count < top { count++; path = $$2; for (i = 3; i <= NF; i++) path = path " " $$i; printf "%2d. %6d 行  %s\n", count, $$1, path }'

links:
	$(UV) run $(PYTHON) tools/check_links.py $(DOCS_DIR)/

tags:
	$(UV) run $(PYTHON) tools/check_tags.py $(ENTRIES_DIR)/

frontmatter:
	$(UV) run $(PYTHON) tools/check_frontmatter.py --path $(ENTRIES_DIR)

build:
	$(UV) run mkdocs build

serve:
	$(UV) run mkdocs serve

pdf:
	@set -- $(UV) run $(PYTHON) tools/pdf_export/export_to_pdf.py --pdf-engine "$(PDF_ENGINE)" --cjk-font "$(CJK_FONT)"; \
	if [ -n "$(strip $(PDF_OUTPUT))" ]; then \
		set -- "$$@" --output "$(PDF_OUTPUT)"; \
	fi; \
	if [ -n "$(strip $(PDF_EXTRA_ARGS))" ]; then \
		set -- "$$@" $(PDF_EXTRA_ARGS); \
	fi; \
	"$$@"

fix:
	$(UV) run $(PYTHON) tools/fix_markdown.py $(ENTRIES_DIR)/

lint:
	$(MARKDOWNLINT) "$(MARKDOWN_FILES)" --ignore "node_modules" --ignore "tools/pdf_export/vendor"

check: links tags frontmatter build

all: check pdf
