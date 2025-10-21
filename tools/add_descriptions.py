#!/usr/bin/env python3
"""
为词条批量添加 description 字段的工具
"""
import os
import re
from pathlib import Path

# 优先处理的核心词条及其 description
PRIORITY_DESCRIPTIONS = {
    "DID.md": "深入解析解离性身份障碍（DID）的诊断标准、临床表现与治疗方法。了解多重人格障碍的本质、创伤根源及康复路径，包含 ICD-11 与 DSM-5-TR 权威诊断标准",
    "OSDD.md": "详解其他特定解离性障碍（OSDD）的诊断标准与临床特征。探讨部分 DID、非典型解离障碍的表现形式，理解不完全符合 DID 标准的解离性障碍",
    "Tulpa.md": "全面了解 Tulpa（图帕）的创造原理、培育方法与实践指南。探索意识同伴的形成机制、与 DID 的区别及社群文化，包含系统化训练技巧",
    "Dissociation.md": "解离现象的全面解析：功能性分离、防御性解离与解离障碍的区别。理解从正常解离到病理性解离的连续谱，掌握解离体验的本质",
    "CPTSD.md": "复杂性创伤后应激障碍（CPTSD）完整指南：诊断标准、自我组织障碍（DSO）与治疗方法。了解长期创伤的影响、与 PTSD 的区别及康复路径",
    "Multiple_Personality_System.md": "多意识体系统（MPS）概念详解：定义、类型、运作机制与日常管理。了解多重人格系统的本质、成员关系及协作方式的专业指南",
    "PTSD.md": "创伤后应激障碍（PTSD）权威指南：症状识别、诊断标准与治疗方法。掌握闪回、回避、过度警觉等核心症状及有效应对策略",
    "System.md": "多意识体系统的完整定义与运作原理。了解系统成员、内部沟通、前台切换等核心概念，探索多意识体的协作与管理机制",
    "Alter.md": "系统成员（Alter）的定义、分类与角色功能。深入理解多意识体系统中不同成员的特征、形成原因及其在系统中的作用",
    "Front-Fronting.md": "前台（Fronting）机制详解：成员切换、意识控制与日常管理。了解谁在控制身体、如何切换及切换过程中的体验与挑战",
    "Switch.md": "深入解析系统成员切换（Switch）的类型、触发因素与管理方法。了解切换的生理心理机制、如何识别切换及应对策略",
    "Co-Consciousness.md": "意识共存（Co-consciousness）现象详解：多个成员同时在线的体验与管理。理解共同觉察、信息共享及协作运作的机制",
    "Headspace-Inner-World.md": "内部空间（Headspace）构建指南：创建、维护与功能。探索系统成员的内在世界、可视化技术及内部环境对系统稳定性的作用",
    "Internal-Communication.md": "系统内部沟通技巧与方法：建立有效对话、解决冲突、增进合作。掌握日记、内部会议等实用工具，提升系统协作效率",
    "Grounding.md": "接地（Grounding）技术完整指南：应对解离、焦虑与创伤触发的有效方法。学习感官觉察、身体定向等实用技巧，重建当下连接",
    "Trauma.md": "创伤（Trauma）的本质、类型与影响机制。理解急性创伤、复杂创伤及发展性创伤对身心的深远影响，掌握创伤知情视角",
    "Trigger.md": "创伤触发（Trigger）的识别、管理与应对策略。了解触发机制、如何建立触发清单及有效的预防与缓解方法",
    "Flashback.md": "闪回（Flashback）现象详解：类型、触发因素与应对技巧。理解创伤记忆再现的机制，掌握接地与安全策略减轻闪回影响",
    "Integration.md": "系统整合（Integration）的含义、方法与争议。探讨成员融合、合作整合等不同路径，理解整合在创伤康复中的作用与个人选择",
    "Fusion.md": "成员融合（Fusion）过程详解：自愿融合、融合体验与后续适应。了解融合的条件、过程及融合后的身份重建与情感调适",
    "Host.md": "宿主（Host）的定义、角色与挑战。理解主要控制身体的成员特征、宿主与其他成员的关系及宿主身份的动态性",
    "Protector.md": "保护者（Protector）成员的类型、功能与工作方式。了解保护性成员如何维护系统安全、应对威胁及其可能的过度保护模式",
    "Persecutor.md": "迫害者（Persecutor）成员的本质、形成原因与转化。理解看似敌对的成员实际上的保护意图，探索化解内部冲突的方法",
    "Child-Alter.md": "儿童人格（Little / Child Alter）的特征、需求与照护。了解儿童成员的脆弱性、创伤持有及如何提供安全支持与内部照顾",
    "Caregiver.md": "照顾者（Caregiver）成员的角色与功能。理解内部照护系统、照顾者如何支持其他成员及避免过度照顾导致的耗竭",
    "Gatekeeper.md": "守门人（Gatekeeper）的职能与重要性。了解控制成员切换、保护记忆、维护系统秩序的关键成员及其运作机制",
    "Memory-Holder.md": "记忆持有者（Memory Holder）的角色与创伤记忆管理。理解特定成员持有特定记忆的机制、记忆分隔的保护作用及整合挑战",
    "Depersonalization.md": "人格解体（Depersonalization）体验详解：与自我脱节的感受、诊断标准与应对方法。理解非我感、观察者视角等解离现象",
    "Derealization.md": "现实解体（Derealization）现象解析：世界失真感、诊断标准与管理策略。了解现实感丧失、环境陌生化等体验的本质",
    "Depersonalization-Derealization-Disorder-DPDR.md": "人格解体/现实解体障碍（DPDR）权威指南：诊断标准、临床表现与治疗方法。掌握持续性解离体验的识别与康复策略",
    "Dissociative-Amnesia-DA.md": "解离性遗忘（DA）详解：记忆缺失类型、诊断标准与恢复方法。理解创伤相关记忆断片、遗忘性漫游等现象的本质",
    "Dissociative-Disorders.md": "解离障碍（Dissociative Disorders）完整分类：DID、OSDD、DPDR、DA 等诊断概览。理解解离障碍谱系的临床特征与鉴别诊断",
}

def extract_frontmatter_and_content(content):
    """提取 Frontmatter 和正文内容"""
    match = re.match(r'^(---\s*\n.*?\n---\s*\n)(.*)', content, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return None, content

def parse_frontmatter(frontmatter_text):
    """解析 Frontmatter 为字典"""
    lines = frontmatter_text.strip().split('\n')
    data = {}
    current_key = None
    current_list = []

    for line in lines:
        if line.strip() in ['---', '']:
            continue

        # 检查是否是键值对行
        if ':' in line and not line.startswith('  ') and not line.startswith('-'):
            if current_key and current_list:
                data[current_key] = current_list
                current_list = []

            key, value = line.split(':', 1)
            current_key = key.strip()
            value = value.strip()

            if value:
                data[current_key] = value
            else:
                current_list = []
        elif line.strip().startswith('-') and current_key:
            # 列表项
            current_list.append(line.strip()[1:].strip())
        elif current_key and not data.get(current_key):
            # 继续上一个键的值
            if current_list:
                current_list.append(line.strip())
            else:
                data[current_key] = line.strip()

    # 处理最后一个键
    if current_key and current_list:
        data[current_key] = current_list

    return data

def has_description(frontmatter_dict):
    """检查是否已有 description"""
    return 'description' in frontmatter_dict

def add_description_to_frontmatter(frontmatter_text, description):
    """在 Frontmatter 中添加 description 字段"""
    lines = frontmatter_text.strip().split('\n')

    # 找到第一个 --- 后插入
    result_lines = []
    inserted = False

    for i, line in enumerate(lines):
        result_lines.append(line)

        # 在第一个 --- 之后、title 之前插入 description
        if not inserted and line.strip() == '---' and i == 0:
            # 继续到找到合适的位置
            continue
        elif not inserted and 'title:' in line:
            # 在 title 之前插入 description
            result_lines.insert(-1, f"description: {description}")
            inserted = True

    if not inserted:
        # 如果没找到 title，在最后一个 --- 之前插入
        for i in range(len(result_lines) - 1, -1, -1):
            if result_lines[i].strip() == '---':
                result_lines.insert(i, f"description: {description}")
                inserted = True
                break

    return '\n'.join(result_lines)

def main():
    entries_dir = Path('docs/entries')

    if not entries_dir.exists():
        print(f"错误: {entries_dir} 目录不存在")
        return

    updated_count = 0
    skipped_count = 0
    error_count = 0

    print("=" * 70)
    print("开始为优先词条添加 description 字段")
    print("=" * 70)

    for filename, description in PRIORITY_DESCRIPTIONS.items():
        entry_file = entries_dir / filename

        if not entry_file.exists():
            print(f"⚠️  跳过: {filename} (文件不存在)")
            error_count += 1
            continue

        try:
            content = entry_file.read_text(encoding='utf-8')
            frontmatter_text, body = extract_frontmatter_and_content(content)

            if not frontmatter_text:
                print(f"⚠️  跳过: {filename} (无 Frontmatter)")
                skipped_count += 1
                continue

            frontmatter_dict = parse_frontmatter(frontmatter_text)

            if has_description(frontmatter_dict):
                print(f"✓  跳过: {filename} (已有 description)")
                skipped_count += 1
                continue

            # 添加 description
            new_frontmatter = add_description_to_frontmatter(frontmatter_text, description)
            new_content = new_frontmatter + '\n' + body

            # 写入文件
            entry_file.write_text(new_content, encoding='utf-8')
            print(f"✓  已更新: {filename}")
            updated_count += 1

        except Exception as e:
            print(f"❌ 错误: {filename} - {e}")
            error_count += 1

    print("\n" + "=" * 70)
    print(f"处理完成:")
    print(f"  已更新: {updated_count} 个文件")
    print(f"  已跳过: {skipped_count} 个文件")
    print(f"  发生错误: {error_count} 个文件")
    print("=" * 70)

if __name__ == '__main__':
    main()
