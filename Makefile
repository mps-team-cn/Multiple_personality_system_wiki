SHELL := /bin/sh

UV ?= uv
PYTHON ?= python3
ENTRIES_DIR ?= docs/entries
MARKDOWNLINT ?= markdownlint
MARKDOWN_FILES ?= docs/**/*.md
PDF_ENGINE ?= tectonic
CJK_FONT ?= Microsoft YaHei
PDF_OUTPUT ?= releases/Multiple_Personality_System_wiki.pdf
PDF_EXTRA_ARGS ?=

.PHONY: help links tags frontmatter build serve pdf fix lint check all

help:
	@printf '%s\n' \
		'可用命令:' \
		'  make help         查看帮助' \
		'  make links        检查词条链接规范' \
		'  make tags         检查词条标签规范' \
		'  make frontmatter  检查词条 Frontmatter' \
		'  make build        严格构建 MkDocs 站点' \
		'  make serve        启动本地预览服务' \
		'  make pdf          导出 PDF' \
		'  make fix          修复 docs/entries/ 下的 Markdown 格式' \
		'  make lint         运行 markdownlint' \
		'  make check        依次执行 links/tags/frontmatter/build' \
		'  make all          执行 check 和 pdf' \
		'' \
		'常用变量:' \
		'  ENTRIES_DIR=docs/entries' \
		'  PDF_ENGINE=tectonic' \
		'  CJK_FONT=Microsoft YaHei' \
		'  PDF_OUTPUT=releases/Multiple_Personality_System_wiki.pdf' \
		'  PDF_EXTRA_ARGS=...' \
		'' \
		'示例:' \
		'  make check' \
		'  make pdf PDF_ENGINE=xelatex CJK_FONT="Noto Serif CJK SC"' \
		'  make pdf PDF_OUTPUT=dist/wiki.pdf PDF_EXTRA_ARGS='\''--include-tags "guide:入门指南"'\'''

links:
	$(UV) run $(PYTHON) tools/check_links.py $(ENTRIES_DIR)/

tags:
	$(UV) run $(PYTHON) tools/check_tags.py $(ENTRIES_DIR)/

frontmatter:
	$(UV) run $(PYTHON) tools/check_frontmatter.py --path $(ENTRIES_DIR)

build:
	$(UV) run mkdocs build --strict

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
