#!/usr/bin/env python3
"""PDF 导出新增开关的单测（无第三方依赖）。

运行:
    uv run python3 tools/pdf_export/test_pdf_export.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pdf_export.cli import main
from pdf_export.exporter import build_pandoc_command, normalize_paper
from pdf_export.ignore_loader import load_ignore_rules
from pdf_export.markdown import build_cover_page, strip_html_markup
from pdf_export.paths import IGNORE_FILE_PATH
from pdf_export.structure import collect_markdown_structure


def _cmd(**overrides) -> list[str]:
    kwargs = dict(
        markdown_path=Path("/tmp/x.md"),
        output_path=Path("/tmp/x.pdf"),
        pandoc_cmd="pandoc",
        pdf_engine="xelatex",
        cjk_font=None,
        main_font=None,
        sans_font=None,
        mono_font=None,
    )
    kwargs.update(overrides)
    return build_pandoc_command(**kwargs)


def _cover(**overrides) -> str:
    kwargs = dict(
        title="T",
        subtitle=None,
        date_text=None,
        footer_text=None,
        online_link_label=None,
        online_link_url=None,
    )
    kwargs.update(overrides)
    return build_cover_page(**kwargs)


def test_paper_and_margin():
    command = " ".join(_cmd(paper="A4paper", margin="2.5cm"))
    assert "geometry=a4paper,margin=2.5cm,footskip=1.95cm" in command
    assert _cmd().count("--variable") == 0


def test_footskip_follows_bottom_margin():
    # 默认 footskip=30pt，底边距 1.3cm 时页码会跑到纸边 2mm 处
    assert "geometry=margin=1.3cm,footskip=0.75cm" in " ".join(_cmd(margin="1.3cm"))
    assert "footskip=1.45cm" in " ".join(_cmd(margin="top=2cm,bottom=2cm"))
    assert "footskip=0.40cm" in " ".join(_cmd(margin="bottom=0.6cm"))
    assert not any("footskip" in item for item in _cmd())


def test_margin_geometry_syntax():
    command = " ".join(_cmd(margin="top=2cm,bottom=2cm"))
    assert "geometry=top=2cm,bottom=2cm" in command


def test_binding_offset():
    command = " ".join(_cmd(paper="a5", margin="2cm", binding_offset="1cm"))
    assert "geometry=a5paper,margin=2cm,footskip=1.45cm,bindingoffset=1cm" in command
    assert "classoption=twoside" in command
    # 不传就不该带 twoside（不改默认版式）
    assert "classoption=twoside" not in " ".join(_cmd(margin="2cm"))


def test_paper_normalize():
    assert normalize_paper("A4") == "a4"
    assert normalize_paper("a4paper") == "a4"
    assert normalize_paper("letter") == "letter"


def test_cover_image():
    tex = _cover(cover_image="/abs/cover.png")
    assert "\\includegraphics" in tex
    assert "\\detokenize{/abs/cover.png}" in tex
    assert "\\includegraphics" not in _cover()


def test_exclude_topics():
    rules = load_ignore_rules(IGNORE_FILE_PATH)
    _, kept = collect_markdown_structure(rules)
    assert any(title == "文化与表现" for title, _ in kept)

    _, filtered = collect_markdown_structure(rules, exclude_topics={"文化与表现"})
    assert filtered
    assert all(title != "文化与表现" for title, _ in filtered)


def test_emit_markdown_is_pandoc_free():
    """--emit-markdown 不装 pandoc / LaTeX 也能跑，且章节过滤生效。"""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "preview.md"
        main(["--emit-markdown", str(out), "--exclude-topics", "文化与表现"])
        text = out.read_text(encoding="utf-8")

    assert "\\begin{titlepage}" in text
    assert "\n# 文化与表现\n" not in text
    assert "\n# 诊断与临床\n" in text


def test_cover_file_overrides_builtin():
    """cover.md 存在时整页原样替换，不拼接内置 LaTeX。"""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        cover = Path(tmp) / "cover.md"
        cover.write_text("\\begin{titlepage}\\Huge 自定义\\end{titlepage}", encoding="utf-8")
        out = Path(tmp) / "preview.md"
        main(["--emit-markdown", str(out), "--cover-file", str(cover)])
        text = out.read_text(encoding="utf-8")

    assert text.startswith("\\begin{titlepage}\\Huge 自定义\\end{titlepage}")
    assert "多意识体系统知识库" not in text.split("\n# 目录")[0]
    assert "\\newpage" in text


def test_html_markup_stripped():
    """量表词条里的 HTML 控件不能当正文排出去（也是长串顶出右边界的根源）。"""
    source = (
        '<div class="brief-scale-hint" aria-valuemax="&quot;10&quot;">若焦虑持续，请尽快联系</div>\n'
        "<!-- 注释 -->\n"
        "```html\n<div>代码里的标签保留</div>\n```\n"
    )
    out = strip_html_markup(source)

    assert "class=" not in out
    assert "&quot;" not in out
    assert "注释" not in out
    assert "若焦虑持续" in out
    assert "<div>代码里的标签保留</div>" in out


if __name__ == "__main__":
    failures = 0
    for name, func in sorted(globals().items()):
        if name.startswith("test_") and callable(func):
            try:
                func()
                print(f"PASS {name}")
            except AssertionError as error:
                failures += 1
                print(f"FAIL {name}: {error}")
    sys.exit(1 if failures else 0)
