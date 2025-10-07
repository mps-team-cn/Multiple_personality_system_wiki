#!/usr/bin/env python3
"""分析所有词条的标签使用情况"""

from pathlib import Path
from collections import defaultdict
import sys

# 添加路径
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.pdf_export.pdf_export.frontmatter import load_entry_document

def main():
    entries_dir = REPO_ROOT / 'entries'
    tag_count = defaultdict(int)
    tag_entries = defaultdict(list)

    for path in sorted(entries_dir.glob('*.md')):
        try:
            doc = load_entry_document(path)
            for tag in doc.tags:
                tag_count[tag] += 1
                tag_entries[tag].append(path.stem)
        except Exception as e:
            print(f'Error: {path.name}: {e}', file=sys.stderr)

    # 输出到文件避免编码问题
    output = REPO_ROOT / 'tag_analysis.txt'
    with open(output, 'w', encoding='utf-8') as f:
        f.write('标签使用统计（按出现次数排序）:\n')
        f.write('=' * 80 + '\n\n')

        for tag, count in sorted(tag_count.items(), key=lambda x: (-x[1], x[0])):
            f.write(f'{tag}: {count}次\n')
            # 只显示前5个使用该标签的词条
            sample_entries = tag_entries[tag][:5]
            for entry in sample_entries:
                f.write(f'  - {entry}\n')
            if len(tag_entries[tag]) > 5:
                f.write(f'  - ... 还有 {len(tag_entries[tag]) - 5} 个\n')
            f.write('\n')

    print(f'分析完成，结果已保存到: {output}')

if __name__ == '__main__':
    main()
