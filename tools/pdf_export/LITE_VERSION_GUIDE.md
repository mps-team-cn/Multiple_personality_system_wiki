# 精简版 PDF 生成指南

本指南说明如何生成只包含部分词条的精简版 PDF。

## 快速开始

### 方式 1: 按标签筛选（最简单）

只需指定要包含或排除的标签即可:

```bash
# 只导出解离障碍相关词条（约 126 个）
python tools/pdf_export/export_to_pdf.py \
  --include-tags "dx:解离障碍" \
  --output MPS_Wiki_Dissociation.pdf

# 只导出系统运作相关词条（约 54 个）
python tools/pdf_export/export_to_pdf.py \
  --include-tags "ops:系统运作" \
  --output MPS_Wiki_Operations.pdf

# 导出除了共病和风险管理之外的所有词条
python tools/pdf_export/export_to_pdf.py \
  --exclude-tags "dx:共病,guide:风险管理" \
  --output MPS_Wiki_Core.pdf
```

### 方式 2: 使用白名单（精确控制）

1. 创建一个文本文件，列出要导出的词条:

```bash
cat > my-lite-entries.txt << 'EOF'
# 我的精选词条
Alter.md
DID.md
OSDD.md
Switch.md
Front-Fronting.md
Trauma.md
Grounding.md
EOF
```

2. 使用白名单导出:

```bash
python tools/pdf_export/export_to_pdf.py \
  --entry-list my-lite-entries.txt \
  --output MPS_Wiki_My_Selection.pdf
```

### 方式 3: 组合使用

可以同时使用白名单和标签过滤:

```bash
python tools/pdf_export/export_to_pdf.py \
  --entry-list my-lite-entries.txt \
  --exclude-tags "guide:风险管理" \
  --output MPS_Wiki_Custom.pdf
```

## 常用标签参考

根据词条数量排序的常用标签（截至 2025-10）:

| 标签 | 词条数 | 说明 |
|------|--------|------|
| `dx:解离障碍` | 129 | 解离障碍相关诊断 |
| `guide:诊断与临床` | 110 | 临床诊断指南 |
| `sx:创伤症状` | 100 | 创伤相关症状 |
| `ops:系统运作` | 54 | 系统日常运作 |
| `role:系统角色` | 37 | 系统成员角色 |
| `tx:创伤治疗` | 18 | 创伤治疗方法 |
| `guide:风险管理` | 16 | 风险管理指南 |
| `dx:共病` | 16 | 共病诊断 |
| `culture:文化表现` | 16 | 文化与媒体表现 |
| `community:Tulpa` | 13 | Tulpa 社区 |
| `guide:实践指南` | 12 | 实践操作指南 |
| `dx:焦虑障碍` | 10 | 焦虑障碍诊断 |
| `tx:心理治疗` | 10 | 心理治疗方法 |
| `guide:创造型系统` | 10 | 创造型系统指南 |

## 推荐配置

### 新手入门版（推荐给初次了解的读者）

```bash
python tools/pdf_export/export_to_pdf.py \
  --include-tags "ops:系统运作,role:系统角色" \
  --output MPS_Wiki_Beginner.pdf
```

预计词条数: 约 70-90 个

### 临床专业版（适合心理健康专业人士）

```bash
python tools/pdf_export/export_to_pdf.py \
  --include-tags "guide:诊断与临床,tx:创伤治疗,dx:解离障碍" \
  --output MPS_Wiki_Clinical.pdf
```

预计词条数: 约 150-200 个

### Tulpa 专题版

```bash
python tools/pdf_export/export_to_pdf.py \
  --include-tags "community:Tulpa,guide:创造型系统" \
  --output MPS_Wiki_Tulpa.pdf
```

预计词条数: 约 20-25 个

## 白名单文件格式

白名单文件是纯文本文件，每行一个词条:

```text
# 注释行以 # 开头
# 可以使用文件名（推荐）
Alter.md
DID.md

# 也可以使用词条标题
成员（Alter）
解离性身份障碍（Dissociative Identity Disorder，DID）

# 空行会被忽略
```

## 查看可用标签

要查看所有可用标签及其词条数，可以运行:

```bash
python3 -c "
import yaml
from pathlib import Path
from collections import Counter

tags_counter = Counter()
for md_file in Path('docs/entries').glob('*.md'):
    content = md_file.read_text(encoding='utf-8')
    if content.startswith('---'):
        lines = content.split('\n')
        end_idx = lines[1:].index('---') + 1
        frontmatter = '\n'.join(lines[1:end_idx])
        try:
            data = yaml.safe_load(frontmatter)
            if 'tags' in data and isinstance(data['tags'], list):
                for tag in data['tags']:
                    tags_counter[tag] += 1
        except: pass

for tag, count in tags_counter.most_common():
    print(f'{tag}: {count}')
"
```

## 提示

1. **组合标签**: 多个标签用逗号分隔，词条只要包含任一标签即会被选中
2. **排除优先**: 如果同时使用 `--include-tags` 和 `--exclude-tags`，排除规则优先级更高
3. **白名单精确**: 使用白名单可以精确控制导出哪些词条
4. **自定义输出**: 使用 `-o` 或 `--output` 指定输出文件名
5. **帮助信息**: 运行 `python tools/pdf_export/export_to_pdf.py --help` 查看所有参数

## 示例文件

项目提供了一个示例白名单文件:

- [example-lite-entries.txt](example-lite-entries.txt) - 精选的核心词条列表

你可以基于此文件修改创建自己的白名单。
