# 项目改进建议

> **生成时间**: 2025-10-12
> **最后更新**: 2025-10-12
> **项目版本**: v3.10.0
> **状态**: 持续更新

本文档汇总了 Multiple Personality System Wiki 项目的改进建议,帮助团队规划未来的开发方向。

## 📌 实施进度概览

- ✅ **已完成**: 统一 CLI 工具、词条验证器基础框架
- 🚧 **进行中**: 依赖版本锁定、工具完善
- ⏳ **待开始**: GitHub Actions、pre-commit hooks、Makefile

---

## 📊 项目现状评估

### ✅ 项目优势

1. **文档组织出色**
    - 184+ 词条内容丰富
    - 9 个主题导览结构清晰
    - 完善的贡献指南体系

2. **工具链完善**
    - 模块化 Python 工具(`tools/core/`, `tools/processors/`)
    - Markdown 自动格式化
    - PDF 导出功能
    - 链接检查工具

3. **开发体验良好**
    - MkDocs Material 主题配置完善
    - Sveltia CMS 后台管理
    - 详细的项目文档

4. **技术栈现代化**
    - Cloudflare Pages 部署
    - 响应式设计
    - 搜索功能优化(jieba + 自定义词典)

---

## 🎯 改进建议

### 一、CI/CD 自动化 🔴 高优先级

**问题**: `.github/workflows/` 目录为空,缺少自动化流程

#### 建议实施

1. **Lint & Quality Check 工作流**

创建 `.github/workflows/lint.yml`:

```yaml
name: Lint & Quality Check

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  markdown-lint:
    name: Markdown 格式检查
    runs-on: ubuntu-latest
    steps:

      - name: Checkout 代码

        uses: actions/checkout@v4

      - name: 设置 Python 环境

        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 安装依赖

        run: |
          pip install -r requirements.txt

      - name: 运行 Markdown 格式检查

        run: |
          python3 tools/fix_markdown.py docs/ --dry-run --verbose

      - name: 检查链接有效性

        run: |
          python3 tools/check_links.py --root . --verbose

  build-test:
    name: 构建测试
    runs-on: ubuntu-latest
    steps:

      - name: Checkout 代码

        uses: actions/checkout@v4

      - name: 设置 Python 环境

        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 安装依赖

        run: |
          pip install -r requirements.txt

      - name: 构建站点

        run: |
          mkdocs build --strict

      - name: 上传构建产物

        uses: actions/upload-artifact@v4
        with:
          name: site
          path: site/
          retention-days: 7
```

2. **自动部署工作流** (可选,Cloudflare Pages 已处理)

如需额外的部署前检查,可创建 `.github/workflows/deploy-check.yml`:

```yaml
name: Deploy Readiness Check

on:
  push:
    branches: [main]

jobs:
  pre-deploy-check:
    name: 部署前检查
    runs-on: ubuntu-latest
    steps:

      - name: Checkout 代码

        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # 获取完整历史用于 changelog

      - name: 设置 Python 环境

        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 安装依赖

        run: pip install -r requirements.txt

      - name: 验证词条结构

        run: python3 tools/gen-validation-report.py

      - name: 检查 changelog 完整性

        run: |
          if ! grep -q "$(git describe --tags --abbrev=0)" docs/changelog.md; then
            echo "⚠️ 警告: changelog.md 可能未更新最新版本"
            exit 1
          fi
```

#### 预期收益

- ✅ 自动发现格式问题
- ✅ PR 提交前自动检查
- ✅ 减少人工审查负担
- ✅ 保证代码质量一致性

---

### 二、文档质量保证 🔴 高优先级

**问题**: 缺少自动化的文档质量检查机制

**当前状态**: ✅ 词条验证器基础框架已实现 (`tools/validators/`)

#### 建议实施

1. **创建 pre-commit hooks** - ⏳ 待实施

创建 `.pre-commit-config.yaml`:

```yaml

# Multiple Personality System Wiki - Pre-commit Hooks

# 安装: pip install pre-commit && pre-commit install

repos:

  - repo: local

    hooks:
      # Markdown 格式自动修复

      - id: markdown-fix

        name: 修复 Markdown 格式
        entry: python3 tools/fix_markdown.py
        language: system
        types: [markdown]
        pass_filenames: true
        args: [--verbose]

      # 链接有效性检查

      - id: check-links

        name: 检查链接有效性
        entry: python3 tools/check_links.py
        language: system
        pass_filenames: false
        args: [--root, .]

      # 词条 Frontmatter 验证

      - id: validate-frontmatter

        name: 验证词条 Frontmatter
        entry: python3 tools/validators/frontmatter_validator.py
        language: system
        files: ^docs/entries/.*\.md$
        pass_filenames: true

  # 通用检查

  - repo: https://github.com/pre-commit/pre-commit-hooks

    rev: v4.5.0
    hooks:

      - id: trailing-whitespace  # 移除行尾空格

        exclude: ^(legacy/|releases/)

      - id: end-of-file-fixer    # 确保文件以换行符结尾

        exclude: ^(legacy/|releases/)

      - id: check-yaml            # YAML 语法检查

        exclude: ^(legacy/|releases/)

      - id: check-json            # JSON 语法检查
      - id: mixed-line-ending     # 统一行尾符

        args: [--fix=lf]
```

安装方法:

```bash
pip install pre-commit
pre-commit install
```

2. **增强链接检查工具**

修改 `tools/check_links.py` 支持目录递归:

```python

# tools/check_links.py 改进建议

def main():
    parser = argparse.ArgumentParser(
        description='检查 Markdown 文件中的链接有效性'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='要检查的文件或目录路径'
    )
    parser.add_argument('--root', default='.', help='项目根目录')
    parser.add_argument('--recursive', '-r', action='store_true',
                       help='递归检查目录')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='显示详细输出')
    # ... 其余代码
```

3. **创建词条完整性验证器** - 🚧 基础框架已有,待完善

参考现有的 `tools/validators/` 目录,建议扩展功能:

新建 `tools/validators/entry_completeness.py`:

```python
"""词条完整性检查工具

检查项目:

1. Frontmatter 完整性 (title, tags, updated)
2. 必需章节存在性
3. 引用格式规范
4. 医疗词条触发警告

"""

import frontmatter
from pathlib import Path
from typing import List, Dict, Any

REQUIRED_FRONTMATTER = ['title', 'tags', 'updated']
MEDICAL_TAGS = ['诊断', '临床', '医疗', '病理']

def check_entry_completeness(file_path: Path) -> Dict[str, Any]:
    """检查单个词条的完整性"""
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    issues = []

    # 检查 Frontmatter
    for field in REQUIRED_FRONTMATTER:
        if field not in post.metadata:
            issues.append(f"缺少必需字段: {field}")

    # 检查医疗词条的触发警告
    if any(tag in post.metadata.get('tags', []) for tag in MEDICAL_TAGS):
        if '!!! warning' not in post.content:
            issues.append("医疗相关词条缺少触发警告")

    # 检查引用格式
    if '[^' in post.content:
        # 简单检查是否有参考文献章节
        if '## 参考文献' not in post.content and '## 参考资料' not in post.content:
            issues.append("使用了脚注但缺少参考文献章节")

    return {
        'file': file_path.name,
        'issues': issues,
        'passed': len(issues) == 0
    }
```

#### 预期收益

- ✅ 提交前自动检查
- ✅ 词条质量标准化
- ✅ 减少 PR 往返次数

---

### 三、依赖管理优化 🟡 中优先级

**问题**: `requirements.txt` 缺少版本锁定,可能导致构建不稳定

**当前状态**: 🚧 部分依赖已锁定版本 (使用 `>=` 语法),建议全部精确锁定

#### 建议实施

1. **锁定依赖版本** - 🚧 进行中

当前 `requirements.txt` 状态:

- ✅ 已有版本约束 (使用 `>=`)
- ⚠️ 建议精确锁定 (使用 `==`)

建议修改为:

```txt

# 基础工具

pyyaml==6.0.1
python-frontmatter==1.1.0
jieba==0.42.1
unidecode==1.3.8
pypinyin==0.51.0

# MkDocs Material 及相关依赖

mkdocs==1.6.0
mkdocs-material==9.5.42
mkdocs-material-extensions==1.3.1

# 插件

mkdocs-git-revision-date-localized-plugin==1.2.9
mkdocs-minify-plugin==0.8.0
mkdocs-glightbox==0.4.0
mkdocs-exclude==1.0.2
mkdocs-exclude-search==0.6.6

# Markdown 扩展

pymdown-extensions==10.11

# 开发工具(可选)

# pre-commit==3.8.0

# pytest==8.3.3

```

2. **创建开发依赖文件**

新建 `requirements-dev.txt`:

```txt

# 开发依赖

-r requirements.txt

# 代码质量

pre-commit==3.8.0
markdownlint-cli2==0.13.0

# 测试

pytest==8.3.3
pytest-cov==5.0.0

# 工具

click==8.1.7
rich==13.8.0
```

3. **考虑迁移到 pyproject.toml**

创建 `pyproject.toml`:

```toml
[project]
name = "mps-wiki"
version = "3.10.0"
description = "Multiple Personality System Wiki"
requires-python = ">=3.10"
dependencies = [
    "mkdocs>=1.6.0",
    "mkdocs-material>=9.5.0",
    "pymdown-extensions>=10.7",
    # ... 其他依赖
]

[project.optional-dependencies]
dev = [
    "pre-commit>=3.5.0",
    "pytest>=8.0.0",
]

[tool.setuptools]
packages = ["tools"]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"
```

#### 预期收益

- ✅ 构建可复现性
- ✅ 依赖冲突提前发现
- ✅ 更快的依赖安装(使用 uv)

---

### 四、搜索功能增强 🟡 中优先级

**当前配置**: 使用 jieba 分词 + `data/user_dict.txt` 自定义词典

#### 建议实施

1. **添加搜索配置说明**

在 `mkdocs.yml` 中添加注释:

```yaml
plugins:

  - search:

      separator: '[\s\u200b\-_,:!=\[\]()"`/]+|\.(?!\d)|&[lg]t;|(?!\b)(?=[A-Z][a-z])'
      lang:

        - zh  # 中文分词(使用 jieba)
        - en  # 英文分词

      jieba_dict_user: data/user_dict.txt  # 自定义词典路径
      # 配置说明:
      # - separator: 自定义分词分隔符
      # - jieba_dict_user: 包含 MPS 领域专业术语
```

2. **词典维护自动化**

创建词典维护工作流 `tools/maintain_search_dict.py`:

```python
"""搜索词典维护工具

功能:

1. 扫描词条提取候选词
2. AI 辅助审核(可选)
3. 合并到 user_dict.txt
4. 分词效果测试

"""

def extract_candidates():
    """提取词典候选词"""
    # 使用现有的 extract_dict_candidates.py

def review_candidates():
    """人工或 AI 审核候选词"""
    # 使用现有的 auto_review_candidates.py

def test_segmentation():
    """测试分词效果"""
    # 使用现有的 test_dict_segmentation.py

def update_dict():
    """更新词典文件"""
    pass

if __name__ == '__main__':
    # 完整维护流程
    extract_candidates()
    review_candidates()
    test_segmentation()
    update_dict()
```

3. **搜索分析工具**

新建 `tools/analyze_search_usage.py`:

```python
"""搜索使用情况分析

功能:

1. 分析搜索日志(如果有)
2. 统计高频搜索词
3. 识别未匹配的搜索
4. 生成优化建议

"""

def analyze_search_logs():
    """分析搜索日志"""
    # 需要集成 Google Analytics API
    pass

def suggest_new_entries():
    """根据搜索建议新词条"""
    pass
```

#### 预期收益

- ✅ 搜索准确度提升
- ✅ 词典维护流程标准化
- ✅ 数据驱动的内容规划

---

### 五、开发体验提升 ✅ 部分完成

#### ✅ 已完成部分

1. **统一工具入口** - 已实现 `tools/cli/main.py`

现有功能:

```bash

# 使用统一 CLI 工具

python -m tools.cli.main fix-md docs/         # 修复 Markdown 格式
python -m tools.cli.main check-links --root . # 检查链接
python -m tools.cli.main validate              # 校验词条
python -m tools.cli.main search-index          # 生成搜索索引
python -m tools.cli.main tags-index            # 生成标签索引
python -m tools.cli.main preview --port 8000   # 启动预览服务器
```

已实现的子命令:

- ✅ `fix-md`: Markdown 格式修复
- ✅ `check-links`: 链接检查
- ✅ `validate`: 词条校验
- ✅ `search-index`: 搜索索引生成
- ✅ `tags-index`: 标签索引生成
- ✅ `preview`: 预览服务器

#### 🚧 待完善部分

1. **简化调用方式**

建议添加快捷脚本 `tools/wiki`:

```bash
#!/usr/bin/env python3
"""快捷入口脚本"""
import sys
from tools.cli.main import main

if __name__ == '__main__':
    sys.exit(main())
```

使用示例:

```bash

# 更简洁的调用方式

./tools/wiki fix-md docs/
./tools/wiki validate
./tools/wiki preview
```

2. **Makefile 快捷命令** - ⏳ 待实现

建议创建 `Makefile`:

```makefile

# Multiple Personality System Wiki - Makefile

.PHONY: help install dev lint fix build clean test

help:  ## 显示帮助信息
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## 安装依赖
	pip install -r requirements.txt
	chmod +x tools/wiki

dev:  ## 启动开发服务器
	mkdocs serve

lint:  ## 运行所有检查
	python -m tools.cli.main fix-md docs/ --dry-run
	python -m tools.cli.main check-links --root .

fix:  ## 自动修复问题
	python -m tools.cli.main fix-md docs/ --verbose

validate:  ## 校验词条
	python -m tools.cli.main validate

build:  ## 构建站点
	mkdocs build

build-strict:  ## 严格模式构建
	mkdocs build --strict

clean:  ## 清理构建文件
	rm -rf site/ .mkdocs_cache/

.DEFAULT_GOAL := help
```

#### 预期收益

- ✅ 降低新贡献者门槛
- ✅ 统一工具使用方式
- ✅ 提高开发效率
- 🚧 CLI 工具已部分实现,仍需改进易用性

---

### 六、性能优化 🟢 低优先级

#### 建议实施

1. **图片优化**

创建 `tools/optimize_images.py`:

```python
"""图片优化工具

功能:

1. 压缩 PNG/JPG
2. 转换为 WebP
3. 生成响应式图片

"""

from PIL import Image
from pathlib import Path

def optimize_image(image_path: Path, quality=85):
    """优化单张图片"""
    img = Image.open(image_path)

    # 转换为 WebP
    webp_path = image_path.with_suffix('.webp')
    img.save(webp_path, 'webp', quality=quality, optimize=True)

    # 压缩原始格式
    img.save(image_path, optimize=True, quality=quality)
```

2. **构建缓存**

修改 `mkdocs.yml`:

```yaml
plugins:

  - search:

      prebuild_index: true  # 预构建搜索索引

  - minify:

      minify_html: true
      minify_js: true
      minify_css: true
      htmlmin_opts:
        remove_comments: true
      cache_safe: true  # 启用缓存
```

3. **CDN 配置**

在 `docs/assets/extra-material.css` 中使用系统字体(已实现):

```css
/* 已优化: 使用系统字体 */
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
```

---

## 📋 实施优先级与时间规划

### ✅ 已完成项目

| 任务 | 完成时间 | 状态 |
|------|---------|------|
| 统一工具 CLI 入口 (tools/cli/main.py) | 2025-10 | ✅ 已完成 |
| 词条验证器基础框架 (tools/validators/) | 2025-10 | ✅ 已完成 |
| 项目改进建议文档 | 2025-10-12 | ✅ 已完成 |

### 🔴 立即实施 (1-2周)

| 任务 | 预计时间 | 状态 | 优先级 |
|------|---------|------|--------|
| 添加 GitHub Actions 工作流 | 2-3 小时 | ⏳ 待开始 | 🔴 高 |
| 创建 pre-commit hooks | 1-2 小时 | ⏳ 待开始 | 🔴 高 |
| 锁定依赖版本到 requirements.txt | 30 分钟 | 🚧 进行中 | 🔴 高 |
| 创建 Makefile 快捷命令 | 1 小时 | ⏳ 待开始 | 🟡 中 |
| 添加快捷脚本 tools/wiki | 15 分钟 | ⏳ 待开始 | 🟡 中 |

### 🟡 短期计划 (1个月内)

| 任务 | 预计时间 | 状态 | 优先级 |
|------|---------|------|--------|
| 改进链接检查工具 | 2-3 小时 | ⏳ 待开始 | 🟡 中 |
| 完善词条完整性验证器 | 3-4 小时 | ⏳ 待开始 | 🟡 中 |
| 创建 requirements-dev.txt | 30 分钟 | ⏳ 待开始 | 🟡 中 |
| 搜索词典维护自动化 | 2-3 小时 | ⏳ 待开始 | 🟡 中 |

### 🟢 长期计划 (3个月+)

| 任务 | 预计时间 | 状态 | 优先级 |
|------|---------|------|--------|
| 迁移到 pyproject.toml | 1-2 小时 | ⏳ 待开始 | 🟢 低 |
| 搜索功能深度优化 | 1-2 周 | ⏳ 待开始 | 🟢 低 |
| 图片优化工具 | 3-4 小时 | ⏳ 待开始 | 🟢 低 |
| API 文档生成 | 1 周 | ⏳ 待开始 | 🟢 低 |

---

## 💡 其他建议

### 1. 社区建设

- 创建贡献者墙 (`docs/contributing/contributors.md`)
- 定期发布项目进展报告
- 建立词条认领机制

### 2. 文档补充

- 录制新手教程视频
- 创建架构决策记录(ADR)
- 补充常见问题解答(FAQ)

### 3. 数据分析

- 分析 Google Analytics 数据
- 优化高频访问词条
- 识别内容缺口

---

## 📝 更新日志

| 日期 | 内容 | 作者 |
|------|------|------|
| 2025-10-12 | 初始版本创建 | Claude |
| 2025-10-12 | 更新实施进度,标记已完成项目 | Claude |

---

## 📞 反馈与建议

如有任何改进建议或问题,请:

1. 在 [GitHub Issues](https://github.com/mps-team-cn/Multiple_personality_system_wiki/issues) 提出
2. 联系维护团队
3. 提交 Pull Request 完善本文档

---

**最后更新**: 2025-10-12
