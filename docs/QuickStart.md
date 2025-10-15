---
title: 快速开始
summary: 快速了解多重意识体核心概念、阅读顺序与自护工具的导航指南。
updated: 2025-10-15
---

# 快速开始（Quick Start）

!!! info "欢迎"
    欢迎来到 Multiple Personality System Wiki。这里汇集了 **多意识体系统（MPS）**、**解离障碍（DID/OSDD）** 与 **创伤疗愈** 的结构化内容。本页提供快速入口、推荐路线与常见操作，帮助你更快找到所需信息。

!!! warning "紧急提醒"
    若你或伙伴正处于紧急或临床风险情境，请优先联系当地紧急服务、心理危机干预中心或持证专业人员。Multiple Personality System Wiki 旨在整理知识与经验分享，无法替代医疗或法律建议。

---

## 🎯 快速入口

<div class="grid cards" markdown>

-   :material-compass: **核心概念导览**  
    从零建立框架，理解「多意识体」「解离」与系统类型。
    [:octicons-arrow-right-24: 进入](entries/Core-Concepts-Guide.md)

-   :material-heart-pulse: **心理健康导览**  
    关注创伤与疗愈，了解 PTSD/CPTSD、DID/OSDD 与循证治疗。
    [:octicons-arrow-right-24: 进入](entries/Mental-Health-Guide.md)

-   :material-cog: **系统运作导览**  
    前台与切换、共同意识、内部沟通与记忆管理的实践路径。
    [:octicons-arrow-right-24: 进入](entries/System-Operations.md)

-   :material-hammer-wrench: **实践指南**  
    Tulpa、冥想、可视化与接地等可直接上手的练习。
    [:octicons-arrow-right-24: 进入](entries/Practice-Guide.md)

</div>

???+ tip "需要更深入？5 个专题导览"
    <div class="grid cards" markdown>

    -   :material-hospital-building: **临床诊断**  
        DID/OSDD、PTSD/CPTSD 标准与鉴别要点。
        [:octicons-arrow-right-24: 进入](entries/Clinical-Diagnosis-Guide.md)

    -   :material-bandage: **创伤与疗愈**  
        稳定 → 处理 → 整合的三阶段模型与工具。
        [:octicons-arrow-right-24: 进入](entries/Trauma-Healing-Guide.md)

    -   :material-account-group: **角色与身份**  
        宿主/守门人/保护者等角色与系统治理。
        [:octicons-arrow-right-24: 进入](entries/Roles-Identity-Guide.md)

    -   :material-thought-bubble: **理论与分类**  
        结构性解离、依恋与自我决定等核心理论。
        [:octicons-arrow-right-24: 进入](entries/Theory-Classification-Guide.md)

    -   :material-movie-open: **文化与媒体**  
        影视/文学/动画/游戏中的多意识体呈现。
        [:octicons-arrow-right-24: 进入](entries/Cultural-Media-Guide.md)

    </div>

---

## 🚀 立即开始

=== "阅读学习"

    - 首先浏览「快速入口」中的一个导览页，建立主线。
    - 遇到陌生术语，使用 [术语表](Glossary.md) 或页面内搜索。
    - 通过页面底部的「相关条目」继续横向扩展。

=== "本地运行"

    !!! success "本地预览（MkDocs Material）"
        ```bash
        # 1) 安装依赖（推荐虚拟环境）
        python3 -m venv venv && source venv/bin/activate
        pip install -r requirements.txt

        # 2) 启动本地服务（支持热重载）
        mkdocs serve
        # 访问 http://127.0.0.1:8000
        ```

    !!! tip "常用命令"
        ```bash
        # 构建静态站点
        mkdocs build --strict

        # 链接规范检查
        python3 tools/check_links.py

        # Markdown 自动修复
        python3 tools/fix_markdown.py .
        ```

=== "参与贡献"

    1. 新词条放在 `docs/entries/`，不得创建子目录，使用模板 `docs/TEMPLATE_ENTRY.md`。
    2. 必填 Frontmatter 字段：`title`, `topic`, `tags`, `updated`（Y-M-D）。
    3. 同步更新对应 Guide 索引（见[映射规则](contributing/technical-conventions.md#13-索引与链接规范)）。
    4. 提交前运行：`fix_markdown.py`、`check_links.py` 与 `markdownlint`。
    5. 使用 Conventional Commits（如 `feat: 新增 Grounding 词条`）。

---

## 🗺️ 推荐学习路线

=== "新手（0–4 周）"

    1. 阅读 [核心概念导览](entries/Core-Concepts-Guide.md) 建立框架。
    2. 选择 [心理健康](entries/Mental-Health-Guide.md) 或 [系统运作](entries/System-Operations.md)。
    3. 浏览 [术语表](Glossary.md) 熟悉常用术语。
    4. 开始练习 [接地](entries/Grounding.md) 等基础技巧。

=== "进阶（1–3 个月）"

    1. 深入 1–2 个专题导览（临床/创伤/角色）。
    2. 参考 [实践指南](entries/Practice-Guide.md) 制定练习计划。
    3. 通过 [标签索引](tags.md) 扩展相关主题。
    4. 结合实际问题查阅具体词条。

=== "精通（3 个月以上）"

    1. 系统学习 [理论与分类](entries/Theory-Classification-Guide.md)。
    2. 探索 [文化与媒体](entries/Cultural-Media-Guide.md) 的跨学科视角。
    3. 参与讨论与贡献，迭代自己的知识框架。

---

## 🔎 快速工具

<div class="grid cards" markdown>

-   :material-book-education: **术语表**  
    遇到陌生术语时的第一站。
    [:octicons-search-24: 打开](Glossary.md)

-   :material-tag: **标签索引**  
    按主题浏览全部词条。
    [:octicons-list-unordered-24: 打开](tags.md)

-   :material-magnify: **站内搜索**  
    顶部搜索栏支持短语与符号搜索。
    [:octicons-arrow-right-24: 使用](index.md)

</div>

---

## 📌 常见问题（FAQ）

??? question "我不确定自己是什么类型的系统？"
    建议先阅读 [核心概念导览](entries/Core-Concepts-Guide.md) 了解类型差异。
    记住：分类不是目的，理解自己与保障安全更重要。

??? question "我需要诊断吗？"
    取决于你的需求：

    - 症状影响生活功能时，建议就医评估（如 [DID](entries/DID.md)、[OSDD](entries/OSDD.md)、[PTSD](entries/PTSD.md)）。
    - 若仅为自我理解，未必需要正式诊断。

    可参考 [心理健康导览](entries/Mental-Health-Guide.md) 与 [临床诊断导览](entries/Clinical-Diagnosis-Guide.md)。

??? question "内容可靠吗？"
    - 医疗/诊断内容遵循 ICD‑11、DSM‑5‑TR 等权威来源。
    - 断言均附来源与访问日期；经验内容会标注「经验分享」。
    - 详见 [贡献指南·学术引用](contributing/academic-citation.md)。

---

祝你在探索过程中保持好奇、尊重与自护 💙
