#!/usr/bin/env python3
"""批量更新词条的 topic 和 tags 字段，统一为6大主标签分类体系。"""

import re
from pathlib import Path
from typing import Dict, List, Optional

# 新的6大主标签
MAIN_TAGS = [
    "诊断与临床",
    "系统运作",
    "创伤与疗愈",
    "角色与身份",
    "理论与分类",
    "文化与表现",
]

# 旧分类到新分类的映射
TOPIC_MAPPING = {
    "系统体验与机制": "系统运作",
    "系统角色与类型": "角色与身份",
    "诊断与临床": "诊断与临床",
    "心理学与理论": "理论与分类",
    "文化与影视": "文化与表现",
    "实践与支持": None,  # 需要根据内容判断
    "心理健康": "诊断与临床",  # 已存在的
    "理论与分类": "理论与分类",  # 已存在的
    "创伤与疗愈": "创伤与疗愈",  # 已存在的
}

# 需要手动检查的词条（原分类为"实践与支持"）
MANUAL_CHECK_ENTRIES = []


def extract_frontmatter(content: str) -> tuple[Optional[str], str]:
    """提取 frontmatter 和正文内容。"""
    if not content.startswith("---"):
        return None, content

    match = re.match(r"^---\n(.*?\n)---\n(.*)$", content, re.DOTALL)
    if not match:
        return None, content

    return match.group(1), match.group(2)


def parse_frontmatter(fm_text: str) -> Dict[str, any]:
    """解析 frontmatter 文本为字典。"""
    data = {}
    current_key = None
    current_list = []

    for line in fm_text.split("\n"):
        # 检查是否是键值对
        if ":" in line and not line.startswith("-"):
            if current_key and current_list:
                data[current_key] = current_list
                current_list = []

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if value:
                data[key] = value
                current_key = None
            else:
                current_key = key
        # 检查是否是列表项
        elif line.startswith("-") and current_key:
            item = line.strip("- ").strip()
            if item:
                current_list.append(item)

    # 处理最后一个列表
    if current_key and current_list:
        data[current_key] = current_list

    return data


def build_frontmatter(data: Dict[str, any]) -> str:
    """从字典构建 frontmatter 文本。"""
    lines = ["---"]

    # 按固定顺序输出字段
    field_order = ["tags", "topic", "title", "updated"]

    for key in field_order:
        if key in data:
            value = data[key]
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"- {item}")
            else:
                lines.append(f"{key}: {value}")

    # 添加其他未列出的字段
    for key, value in data.items():
        if key not in field_order:
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"- {item}")
            else:
                lines.append(f"{key}: {value}")

    lines.append("---")
    return "\n".join(lines)


def update_entry_classification(
    fm_data: Dict[str, any],
    filename: str
) -> tuple[Dict[str, any], bool]:
    """更新词条的 topic 和 tags 字段。"""
    modified = False

    # 获取当前 topic
    old_topic = fm_data.get("topic", "")

    # 映射到新 topic
    new_topic = TOPIC_MAPPING.get(old_topic)

    # 如果是"实践与支持"，需要手动检查
    if old_topic == "实践与支持":
        MANUAL_CHECK_ENTRIES.append(filename)
        # 暂时默认为"创伤与疗愈"
        new_topic = "创伤与疗愈"

    # 更新 topic
    if new_topic and new_topic != old_topic:
        fm_data["topic"] = new_topic
        modified = True

    # 获取当前 tags
    tags = fm_data.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]

    # 确保主标签在 tags 列表开头
    main_tag = new_topic or old_topic
    if main_tag in MAIN_TAGS and main_tag not in tags:
        tags.insert(0, main_tag)
        fm_data["tags"] = tags
        modified = True
    elif main_tag in MAIN_TAGS and tags[0] != main_tag:
        # 移除旧位置的主标签，添加到开头
        if main_tag in tags:
            tags.remove(main_tag)
        tags.insert(0, main_tag)
        fm_data["tags"] = tags
        modified = True

    return fm_data, modified


def process_entry_file(file_path: Path) -> bool:
    """处理单个词条文件。"""
    content = file_path.read_text(encoding="utf-8")

    # 提取 frontmatter
    fm_text, body = extract_frontmatter(content)
    if not fm_text:
        print(f"[SKIP] {file_path.name}: 无 frontmatter")
        return False

    # 解析 frontmatter
    fm_data = parse_frontmatter(fm_text)

    # 更新分类
    fm_data, modified = update_entry_classification(fm_data, file_path.name)

    if not modified:
        return False

    # 重新构建内容
    new_fm_text = build_frontmatter(fm_data)
    new_content = f"{new_fm_text}\n\n{body}"

    # 写回文件
    file_path.write_text(new_content, encoding="utf-8")

    return True


def main():
    """主函数：批量处理所有词条。"""
    import sys
    import io

    # 设置 stdout 为 UTF-8 编码
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    entries_dir = Path(__file__).parent.parent / "docs" / "entries"

    if not entries_dir.exists():
        print(f"错误: 词条目录不存在: {entries_dir}")
        return

    entry_files = sorted(entries_dir.glob("*.md"))
    total = len(entry_files)
    modified_count = 0

    print(f"开始处理 {total} 个词条文件...")
    print()

    for file_path in entry_files:
        try:
            if process_entry_file(file_path):
                modified_count += 1
                print(f"[OK] {file_path.name}: 已更新")
        except Exception as e:
            print(f"[ERR] {file_path.name}: 处理失败 - {e}")

    print()
    print(f"{'='*60}")
    print(f"处理完成:")
    print(f"   总计: {total} 个文件")
    print(f"   已修改: {modified_count} 个文件")
    print(f"   未修改: {total - modified_count} 个文件")

    if MANUAL_CHECK_ENTRIES:
        print()
        print(f"需要手动检查的词条 (原分类为'实践与支持'):")
        for filename in MANUAL_CHECK_ENTRIES:
            print(f"   - {filename}")

    print(f"{'='*60}")


if __name__ == "__main__":
    main()
