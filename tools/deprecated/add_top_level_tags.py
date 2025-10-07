#!/usr/bin/env python3
"""批量为词条添加顶级标签，基于 legacy/index.md 的分类。"""

from pathlib import Path
import re
import yaml

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
ENTRIES_DIR = PROJECT_ROOT / "docs" / "entries"

# legacy/index.md 中的分类到顶级标签的映射
CATEGORY_TO_TOP_TAG = {
    "诊断与临床": "诊断与临床",
    "系统角色与类型": "角色与身份",
    "系统体验与机制": "系统运作",
    "心理学与理论基础": "理论与分类",
    "实践与支持": "创伤与疗愈",
    "虚拟角色与文学影视作品": "文化与表现",
}

# 从 legacy/index.md 解析出分类和词条文件名的映射
def parse_legacy_index():
    """解析 legacy/index.md，返回 {文件名: 顶级标签} 的映射。"""
    index_path = PROJECT_ROOT / "legacy" / "index.md"

    if not index_path.exists():
        raise FileNotFoundError(f"找不到 {index_path}")

    content = index_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    file_to_tag = {}
    current_category = None

    for line in lines:
        # 检测分类标题 (## 开头)
        category_match = re.match(r'^##\s+(.+)$', line.strip())
        if category_match:
            category_name = category_match.group(1).strip()
            current_category = CATEGORY_TO_TOP_TAG.get(category_name)
            continue

        # 检测词条链接 (- [标题](entries/文件名.md))
        if current_category:
            entry_match = re.search(r'\(entries/([^)]+\.md)\)', line)
            if entry_match:
                filename = entry_match.group(1)
                file_to_tag[filename] = current_category

    return file_to_tag


def update_entry_tags(entry_path: Path, top_tag: str):
    """为单个词条文件添加顶级标签（如果还没有的话）。"""

    content = entry_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    # 检查是否有 frontmatter
    if not lines or lines[0].strip() != "---":
        print(f"⚠️  {entry_path.name}: 没有 frontmatter，跳过")
        return False

    # 找到 frontmatter 的结束位置
    frontmatter_end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            frontmatter_end = i
            break

    if frontmatter_end is None:
        print(f"⚠️  {entry_path.name}: frontmatter 格式错误，跳过")
        return False

    # 解析 frontmatter
    frontmatter_text = "\n".join(lines[1:frontmatter_end])
    try:
        metadata = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as e:
        print(f"❌ {entry_path.name}: YAML 解析失败: {e}")
        return False

    # 获取现有标签
    current_tags = metadata.get("tags", [])
    if isinstance(current_tags, str):
        current_tags = [t.strip() for t in current_tags.split(",") if t.strip()]
    elif not isinstance(current_tags, list):
        current_tags = []

    # 检查是否已有顶级标签
    if top_tag in current_tags:
        print(f"✓  {entry_path.name}: 已有标签 '{top_tag}'")
        return False

    # 添加顶级标签到列表开头
    new_tags = [top_tag] + current_tags
    metadata["tags"] = new_tags

    # 重新构建 frontmatter
    new_frontmatter = yaml.dump(
        metadata,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False
    ).strip()

    # 重新组合文件内容
    body = "\n".join(lines[frontmatter_end + 1:])
    new_content = f"---\n{new_frontmatter}\n---\n{body}"

    # 写回文件
    entry_path.write_text(new_content, encoding="utf-8")
    print(f"✅ {entry_path.name}: 已添加标签 '{top_tag}'")
    return True


def main():
    """主函数：批量更新所有词条。"""

    print("📖 解析 legacy/index.md...")
    file_to_tag = parse_legacy_index()
    print(f"   找到 {len(file_to_tag)} 个词条分类")

    print("\n🔄 开始更新词条标签...\n")

    updated_count = 0
    skipped_count = 0
    not_found_count = 0

    for filename, top_tag in sorted(file_to_tag.items()):
        entry_path = ENTRIES_DIR / filename

        if not entry_path.exists():
            print(f"⚠️  {filename}: 文件不存在")
            not_found_count += 1
            continue

        if update_entry_tags(entry_path, top_tag):
            updated_count += 1
        else:
            skipped_count += 1

    print(f"\n📊 更新完成:")
    print(f"   ✅ 已更新: {updated_count} 个")
    print(f"   ⏭️  跳过: {skipped_count} 个")
    print(f"   ⚠️  未找到: {not_found_count} 个")


if __name__ == "__main__":
    main()
