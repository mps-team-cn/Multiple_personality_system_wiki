#!/usr/bin/env python3
"""根据 legacy/index.md 的分类为词条添加主题标签"""

from pathlib import Path
import sys
import re

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# 根据 legacy/index.md 的分类定义主题标签映射
TOPIC_MAPPING = {
    "诊断与临床": [
        "Trauma", "PTSD", "CPTSD", "Flashback", "Anxiety",
        "Autism-Spectrum-Disorder", "Attention-Deficit-Hyperactivity-Disorder-ADHD",
        "Depressive-Disorders", "Learned-Helplessness", "Affective-Disorders",
        "Bipolar-Disorders", "Mania", "Hypomania", "OCD", "Schizophrenia-SC",
        "DID", "Dissociative-Amnesia-DA", "Pathological-Dissociation",
        "Depersonalization-Derealization-Disorder-DPDR", "OSDD",
        "Somatic-Symptom-Disorder-SSD", "Borderline-Personality-Disorder-BPD",
        "Narcissistic-Personality-Disorder-NPD", "Partial-Dissociative-Identity-Disorder-PDID",
        "Alexithymia", "Delirium", "Disorientation"
    ],
    "系统角色与类型": [
        "System-Roles", "Main", "Servitor", "Internal-Self-Helper-ISH", "Core",
        "Alterhuman", "Admin", "Gatekeeper", "Persona", "Fauxmain",
        "Imaginary-Companion", "Blending", "Fragment", "Polyfragmented",
        "Soulbond", "Tulpa", "Host", "Alter", "Emmengard-Classification",
        "Adaptive", "Spontaneous", "Original", "Memory-Holder", "Persecutor",
        "Little", "Teen", "Protector", "Caregiver", "Performer-Executive"
    ],
    "系统体验与机制": [
        "Apparently-Normal-Part-Emotional-Part-Model", "Co-Fronting",
        "Plurality-Basics", "Plurality", "Bias", "Front-Fronting",
        "Back-Being-Back", "Sense-Of-Presence", "Projection",
        "Visualization-Imagination", "External-Projection", "Sequestration",
        "Head-Pressure", "Stress-Response", "Intrusive-Thoughts",
        "Consciousness-Modification", "Co-Consciousness", "Permissions",
        "Exomemory", "Independence", "Headspace-Inner-World", "Tulpish",
        "Fusion", "Memory-Shielding", "Iteration", "Dissociation",
        "Functional-Dissociation", "Structural-Dissociation-Theory",
        "Neurodiversity", "Integration", "Reconstruction", "Body-Ownership",
        "Depersonalization", "Derealization", "Switch", "System", "Subsystem",
        "Xianyu-Theory-Niche-Classification", "Single-Class-Systems-Xianyu",
        "Mixed-Systems-Xianyu", "Family-Systems-Xianyu", "Soul-Linked-Systems-Xianyu",
        "Autopilot", "Trigger", "Regression-In-Psychology", "Alcohol-Induced-Dissociation"
    ],
    "心理学与理论": [
        "Defense-Mechanisms", "Cognitive-Dissonance", "Attachment-Theory",
        "Self-Concept", "Projection-Psychology", "Transference-Countertransference",
        "Personality-Structure-Theory", "Defensive-Dissociation", "Emotion-Regulation",
        "Psychic-Energy-Attention", "Psychological-Resilience", "Self-Efficacy",
        "Humanistic-Psychology", "Social-Cognitive-Theory", "Motivation-Theories",
        "Self-Determination-Theory", "Attention-Awareness", "Learning-Conditioning",
        "Highly-Sensitive-Person", "Mood-Disorders"
    ],
    "实践与支持": [
        "Sensory-Regulation-Strategies", "Meditation", "Grounding",
        "Internal-Communication"
    ],
    "文化与影视": [
        "Nonexistent-You-And-Me-Tulpa-Lilith", "Split-2016-DID-Representation",
        "Bu-Ke-Raoshu-De-Ta-Multiplicity-Narrative", "Sybil-1976-Cultural-Prototype",
        "Three-Faces-Of-Eve-1957-Dissociation", "United-States-Of-Tara-System-Daily-Life",
        "Fight-Club-1999-Identity-Metaphor", "Mr-Robot-DID-Narrative",
        "Paranoia-Agent-Collective-Consciousness", "Dostoevsky-The-Double-Self-Division",
        "Kafka-Metamorphosis-Identity-Dissolution", "Lovecraft-Tulpa-Motifs",
        "Another-Me-DID-Depictions", "Madoka-Magica-Kyubey-Otherness",
        "Touhou-Tulpa-Fandom", "Hatsune-Miku-Virtual-Idol-Tulpa-Boundary"
    ]
}

def get_topic_tag(file_stem: str) -> str:
    """根据文件名获取主题标签"""
    for topic, files in TOPIC_MAPPING.items():
        if file_stem in files:
            return topic
    return None

def add_topic_tag_to_file(file_path: Path) -> bool:
    """为文件添加主题标签"""
    content = file_path.read_text(encoding='utf-8')

    # 匹配 frontmatter
    pattern = r'^---\n(.*?)\n---'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print(f'警告: {file_path.name} 没有找到 frontmatter')
        return False

    frontmatter = match.group(1)

    # 检查是否已有 topic 字段
    if re.search(r'^topic:', frontmatter, re.MULTILINE):
        return False  # 已有 topic，跳过

    # 获取主题标签
    topic = get_topic_tag(file_path.stem)
    if not topic:
        print(f'提示: {file_path.name} 未找到对应主题分类')
        return False

    # 在 tags 之后添加 topic
    tags_pattern = r'(tags:\n(?:- .+\n)+)'

    def add_topic(match):
        tags_section = match.group(1)
        return f"{tags_section}topic: {topic}\n"

    new_frontmatter = re.sub(tags_pattern, add_topic, frontmatter)

    if new_frontmatter == frontmatter:
        # 没有找到 tags，在 title 前添加
        title_pattern = r'(title:)'
        new_frontmatter = re.sub(title_pattern, f'topic: {topic}\n\\1', frontmatter)

    # 替换整个 frontmatter
    new_content = content.replace(f'---\n{frontmatter}\n---', f'---\n{new_frontmatter}\n---')

    if new_content != content:
        file_path.write_text(new_content, encoding='utf-8')
        return True

    return False

def main():
    entries_dirs = [
        REPO_ROOT / 'entries',
        REPO_ROOT / 'docs' / 'entries'
    ]

    for entries_dir in entries_dirs:
        if not entries_dir.exists():
            print(f'跳过不存在的目录: {entries_dir}')
            continue

        print(f'开始处理: {entries_dir}')
        print('=' * 80)

        updated_count = 0
        skipped_count = 0

        for path in sorted(entries_dir.glob('*.md')):
            try:
                if add_topic_tag_to_file(path):
                    topic = get_topic_tag(path.stem)
                    print(f'[OK] {path.name} -> {topic}')
                    updated_count += 1
                else:
                    skipped_count += 1
            except Exception as e:
                print(f'[ERROR] {path.name}: {e}')

        print('=' * 80)
        print(f'{entries_dir.name} 目录完成! 更新 {updated_count} 个文件，跳过 {skipped_count} 个')
        print()

if __name__ == '__main__':
    main()
