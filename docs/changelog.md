---
title: 更新日志
description: MPS Wiki 项目版本更新历史与功能变更记录。追踪词条新增、内容完善、工具优化、架构升级等变化,了解多意识体系统知识库的持续演进
search:
  exclude: true
---

# 更新日志

## [v3.18.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.18.0) - 临床词条体系化重构与交互功能增强 (2025-10-22)

### ✨ 新增功能

- **交互式评估工具** (PR #370)
    - 新增 [躯体形式解离问卷 (SDQ-20)](entries/SDQ-20.md) 交互式评估工具
    - 增强量表使用体验

- **PDF 导出系统优化** (PR #369, #373)
    - 修复前言文档处理
    - 新增 admonitions 提示块转换支持
    - 优化 HTML 标签转换和多级列表渲染

### 📚 词条完善

- **注意力与发展性障碍**
    - **全面重构 [ADHD (注意缺陷多动障碍)](entries/ADHD.md)** (PR #380)
        - 按照 DID 标杆风格对齐结构
        - 补充临床诊断标准与评估量表
        - 增强治疗与管理章节
    - **新增 [过度专注 (Hyperfocus)](entries/Hyperfocus.md) 与 [心流 (Flow)](entries/Flow.md)** (PR #379)
        - 完善 ADHD 相关概念体系
    - **重构 [孤独症谱系障碍 (ASD)](entries/ASD.md)** (PR #382)
        - 更新诊断标准与临床表现
        - 优化内容结构

- **创伤与应激相关障碍**
    - **优化 [CPTSD/PTSD](entries/CPTSD.md) 词条** (PR #375)
        - 按照 DID 风格对齐格式
        - 补充诊断标准与治疗方法
    - **重构 [躯体症状障碍 (SSD)](entries/SSD.md)** (PR #374)
        - 结构对齐 DID 标杆
        - 修正标签与链接,补充评估与治疗段落
    - **新增 [侵入性记忆 (Intrusive-Memory)](entries/Intrusive-Memory.md)** (PR #376)
        - 重写 [侵入性思维 (Intrusive-Thoughts)](entries/Intrusive-Thoughts.md) 并补充链接
        - 优化侵入性思维词条并同步导览映射 (PR #377)
    - **增强 ["非我感" (Not-Me-Feeling)](entries/Not-Me-Feeling.md)** (PR #372)
        - 强化鉴别诊断章节并优化文档结构

- **心境障碍**
    - **翻修 [心境障碍/抑郁障碍](entries/Mood-Disorders.md)** (PR #378)
        - 对齐 DID 标杆风格
        - 更新诊断分类与治疗建议

- **破坏性、冲动控制及品行障碍**
    - **完成破坏性冲动控制障碍核心词条** (PR #383)
        - 新增多个相关诊断词条
    - **修正 [ODD (对立违抗性障碍)](entries/ODD.md) 诊断阈值描述** (PR #385)

- **角色与系统运作**
    - **补充 [迫害者 (Persecutor)](entries/Persecutor.md) 角色概述** (PR #371)

### 🏗️ 架构与标准化

- **文档架构重组** (PR #386)
    - 将导览和索引文件迁移到独立的 `guides/` 目录
    - 优化项目文档结构

- **Markdown 书写规范** (PR #381)
    - 在贡献指南中新增 Markdown 书写规范章节
    - 强制使用连字符 (`-`) 作为无序列表符号
    - 补充标题与排版要求
    - 统一全项目列表符号格式

- **标签体系优化**
    - 修复 PTSD 标签 (PR #384)
    - 优化 tag 标签显示

- **链接修复**
    - 修复两个 index 文件的链接问题 (PR #384)
    - 修正主页链接 (PR #188efe5)

### 🎨 样式改进

- **首页优化**
    - 调整 Hero 区域字体大小以符合 MkDocs Material 标准
    - 优化首页 Hero 区域的字体大小和间距

### 🔧 工具与基础设施

- **CI 流程**
    - 自动更新词条、分区索引与格式
    - 移除未使用的 `.dates_cache.jsonl` 缓存文件

### 📊 影响范围

- 重构/优化 10+ 个核心临床词条
- 新增 5+ 个词条
- 完成 Markdown 书写规范标准化
- 优化文档架构和导览体系
- 增强交互式评估功能

## [v3.17.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.17.0) - SEO 集成与内容标准化升级 (2025-10-21)

### ✨ 新增功能

- **SEO 自动化系统 (PR #366, #368)**
    - 集成 IndexNow 自动推送系统，支持 Bing/Yandex 快速收录
    - 新增 IndexNow 密钥文件预检验证步骤
    - 修正 `--recent` 参数逻辑，确保提交数而非文件数控制
    - 在相关文档中添加 SEO 自动化指南链接

### 📚 词条完善

- **精神障碍与解离专题**
    - **全面重构 [闪回 (Flashback)](entries/Flashback.md)** (PR #367)
        - 补充闪回与解离的核心区别对照表
        - 增强创伤记忆再体验的临床描述
    - **完善 [谵妄 (Delirium)](entries/Delirium.md)** (PR #362, #364, #365, #366)
        - 按照 DID 词条标准重新排版
        - 补充流行病学数据与延伸阅读
        - 修复标签格式和急救提醒语法
    - **新增四个精神病性障碍词条** (PR #362)
        - 涵盖精神分裂症谱系与其他精神病性障碍

- **理论与分类体系**
    - **优化 [ANP-EP 模型](entries/ANP-EP-Model.md)** (PR #355)
        - 全面增强临床严谨性与实用性
    - **澄清 [Emmengard 分类法](entries/Emmengard.md)** (PR #352)
        - 增加 Clinician's Summary 与使用范围说明
        - 自发型 (Spontaneous) 边界与对照表、风险评估
    - **新增 [心理学三大势力](entries/Psychoanalysis.md)** (PR #359)
        - 完善理论框架词条体系

- **角色与系统运作**
    - **增强 [Blending](entries/Blending.md)** (PR #361)
        - 优化内容与标签规范
    - **新增 [主导 (Dominant/Lead)](entries/Dominant.md)** (PR #347)
    - **修订 [记忆屏蔽 (Memory-Shielding)](entries/Memory-Shielding.md)** (PR #348)
        - 标注为社群/经验性术语，新增 Clinician's Summary
        - 补充法证与记忆可靠性警示

- **创伤与疗愈**
    - **新增 [内在批评者 (Inner-Critic)](entries/Inner-Critic.md)** (PR #343)
    - **优化 [迫害者 (Persecutor)](entries/Persecutor.md)** (PR #342)
        - 新增 Clinician's Summary、结构性解离定义与对照表
    - **创伤与疗愈主题更新** (PR #344)
        - 新增创伤后成长 (PTG) 词条
        - 更新三阶段治疗模型与导览

- **其他词条**
    - **新增 [选择性缄默症 (Selective-Mutism)](entries/Selective-Mutism.md)** - 增加 Clinician's Summary
    - **新增 [异装癖 (Transvestism，已过时)](entries/Transvestism.md)** (PR #349)

### 🏗️ 架构与标准化

- **术语统一工程** (PR #353, #354)
    - 全面统一使用"多意识体 (Multiple Personality)"替代其他术语
    - 确保项目术语一致性

- **标签体系重构** (PR #360)
    - 引入分面标签规范 (Frontmatter 标签体系)
    - 优化解离与焦虑障碍词条标签 (PR #358)
    - 降低文化表现类词条检索权重，突出核心临床内容

- **格式标准化** (PR #351)
    - 统一 Clinician's Summary 为提示块 (admonition) 格式
    - 统一提示块类型为 Material 支持的类型
    - 将非标准提示块类型替换为标准类型

- **链接与导览优化**
    - 统一"整合/融合"术语并链接至 Fusion/Integration (PR #345)
    - 将导览章节中文引号改为标准 Markdown 链接
    - 修正 Tulpa-Guide 文件命名保持系列一致性 (PR #356)
    - 删除"投影"词条，统一使用"外投射" (PR #357)

### 🔧 工具与基础设施

- **CI 流程优化**
    - IndexNow 密钥文件路径修正以确保部署可访问
    - 自动更新词条、分区索引与格式

- **搜索与配置**
    - 优化标签与搜索配置，提升检索精准度
    - 优化 `agents.md` 文档

### 📊 影响范围

- 新增 10+ 个词条，完善 20+ 个现有词条
- 完成术语统一与标签体系标准化
- 集成 SEO 自动推送提升搜索引擎可见度
- 多处导览、索引与 Glossary 同步更新

---

## [v3.16.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.16.0) - 危机资源上线与量表体验升级 (2025-10-19)

### ✨ 新增词条

- **危机与支援资源（Crisis & Support）(PR #341)**
    - [危机与支援资源](entries/Crisis-And-Support-Resources.md)：24 小时求助热线、城市支援资源、在线自助平台
    - 提供可复制的「自助安全计划」模板与使用指引
    - 导航与导览入口已接入首页、QuickStart、实践与创伤导览

### 📚 词条完善

- **临床与导览**
    - 翻修 [定向障碍（Disorientation）](entries/Disorientation.md)，对齐 DID 相关临床标准（PR #340）
    - 扩充 OSDD 词条并优化搜索配置（PR #330）
    - 调整 Tulpa 等相关条目内部链接与一致性

### 🧪 量表与前端体验

- **DES‑II 在线量表与交互优化**
    - 新增 [DES‑II 在线量表](entries/Dissociative-Experiences-Scale-DES-II.md)，支持实时计分与三子量表进度条
    - 统一中文题干与阈值，对齐 NovoPsych（PR #335）
    - 限制 DES‑II/MID‑60 滑块为仅拖拽，禁用滚轮/键盘并屏蔽轨道点击跳值，避免误操作

- **MID‑60 可访问性与导出**
    - 新增移动端导出图片（含水印）（PR #336）
    - 改进结果导出与可访问性（PR #339）

- **界面细节**
    - 开启“编辑此页”图标，提升文档协作体验

### 🔧 工具与基础设施

- 新增基于 Frontmatter 的用户词典生成工具，增强中文搜索（PR #329）
- 清理无用的报表 PDF 导出项与若干格式修复

### 📊 影响范围

- 新增 1 个核心资源词条；大幅改善量表与交互体验
- 涉及首页与导览入口同步接入；多处文档结构与链接规范优化

---

## [v3.15.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.15.0) - 角色体系扩充与内容格式标准化 (2025-10-18)

### ✨ 新增词条

- **新增 4 个睡眠障碍词条 (PR #318)**
    - [呼吸相关睡眠障碍 （Breathing-Related-Sleep-Disorders）](entries/Breathing-Related-Sleep-Disorders.md)
    - [阻塞性睡眠呼吸暂停低通气 （Obstructive-Sleep-Apnea-Hypopnea）](entries/Obstructive-Sleep-Apnea-Hypopnea.md)
    - [昼夜节律睡眠-觉醒障碍 （Circadian-Rhythm-Sleep-Wake-Disorders）](entries/Circadian-Rhythm-Sleep-Wake-Disorders.md)
    - [不宁腿综合征 （Restless-Legs-Syndrome）](entries/Restless-Legs-Syndrome.md)

- **新增系统运作与理论词条 (PR #320)**
    - [角色面具 （Masking）](entries/Masking.md) - 多意识体系统的社会适应策略
    - [偏重倾向 （Median-Bias）](entries/Median-Bias.md) - 咸鱼理论中的核心概念

- **新增创伤疗愈核心词条 (PR #314)**
    - [深层记忆 （Deep-Memory）](entries/Deep-Memory.md) - 与核心创伤高度相关的隐性记忆（⚠️ 仅限专业支持下探索）

### 📚 词条完善

- **临床诊断词条大幅扩充 (PR #317)**
    - 全面完善 [解离性身份障碍 （DID）](entries/DID.md) 词条
        - 新增 ICD-11 与 DSM-5-TR 详细诊断标准对比
        - 补充诊断评估工具表格（SCID-D、MID、DDIS、DES、SDQ-20）
        - 增加治疗伦理与边界、长期照护、争议与特殊议题等章节
    - 全面完善 [精神分裂症 （Schizophrenia）](entries/Schizophrenia.md) 词条
        - 扩充阳性/阴性/认知症状详细说明
        - 新增鉴别诊断、共病管理、风险管理重点
        - 详细阐述药物治疗与心理社会干预方案

- **核心角色与理论词条大规模扩充 (PR #319)**
    - [管理者 （Admin）](entries/Admin.md) - 从 75 行扩充至 251 行
    - [宿主 （Host）](entries/Host.md) - 补充身份认知、角色转换、临床视角
    - [身体所有权 （Body-Ownership）](entries/Body-Ownership.md) - 完善神经科学基础与解离视角
    - [意识修改 （Consciousness-Modification）](entries/Consciousness-Modification.md) - 从 88 行扩充至 275 行
    - [习得性无助 （Learned-Helplessness）](entries/Learned-Helplessness.md) - 从 120 行扩充至 316 行
    - [外部投射 （External-Projection）](entries/External-Projection.md)、[迭代 （Iteration）](entries/Iteration.md)、[隔离 （Sequestration）](entries/Sequestration.md)

- **系统运作相关词条优化 (PR #320)**
    - 完善 [Tulpa](entries/Tulpa.md) 与 [Tulpish](entries/Tulpish.md) 的社群实践与术语演变历史
    - 优化 [System](entries/System.md)、[System-Roles](entries/System-Roles.md)、[OCD](entries/OCD.md)、[Trigger](entries/Trigger.md) 等词条

- **解离与创伤词条强化**
    - 全面升级 [解离 （Dissociation）](entries/Dissociation.md) 词条的临床专业性
    - 全面改进 [创伤 （Trauma）](entries/Trauma.md) 词条的临床专业性与可操作性
    - 新增 [嗜睡障碍 （Hypersomnolence-Disorder）](entries/Hypersomnolence-Disorder.md) 词条

### 🔧 工具与基础设施

- **PDF 导出功能优化 (PR #321)**
    - 添加索引文件（`*index.md`、`*-index.md`）和导览文件（`*Guide.md`、`*-Guide.md`）排除规则
    - 优化 PDF 封面信息：添加"全体贡献者"字样，优化在线链接显示

- **Google Indexing API 集成 (PR #311)**
    - 新增自动提交工具，支持批量提交和定时更新
    - 完善快速开始指南、实施总结、测试检查清单

### 📝 格式规范与文档更新

- **全面格式标准化 (PR #319)**
    - 统一全部 65 个文档的括号格式（英文括号 → 中文全角括号）
    - 规范 Frontmatter 的 `tags`、`synonyms` 等字段缩进
    - 为核心词条添加 `search.boost` SEO 配置

- **开发文档完善 (PR #319)**
    - 新增或更新 7 个开发指南（Tools-Manual.md、Performance-Optimization.md 等）
    - 在 CLAUDE.md 中明确 PR 阶段与合并后的双重检查流程

- **DSM-5-TR 清单更新 (PR #318)**
    - 修正 8 处词条完成状态标记
    - 更新进度统计：已完成 80/199 (40.2%)

### 🎨 其他改进

- **导航与索引**
    - 更新所有分区索引（Clinical-Diagnosis、System-Operations、Roles-Identity 等）
    - 优化 QuickStart.md 与贡献指南的结构

- **Favicon 与社交分享**
    - 添加 favicon 和社交媒体分享图片

### 📊 影响范围

- **100+ 个文件变更**
- **新增词条**: 7 个
- **大幅扩充词条**: 10+ 个（内容翻倍）
- **格式标准化**: 覆盖全部词条与文档
- **工具增强**: PDF 导出、Google Indexing API

---

## [v3.14.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.14.0) - Tulpa 实践体系完善与主题索引优化 (2025-10-17)

### ✨ 新增词条

- **新增 7 个物质相关障碍核心词条**
    - [酒精相关障碍 （Alcohol-Related Disorders）](entries/Alcohol-Related-Disorders.md)
    - [咖啡因相关障碍 （Caffeine-Related Disorders）](entries/Caffeine-Related-Disorders.md)
    - [大麻相关障碍 （Cannabis-Related Disorders）](entries/Cannabis-Related-Disorders.md)
    - [阿片类相关障碍 （Opioid-Related Disorders）](entries/Opioid-Related-Disorders.md)
    - [镇静催眠抗焦虑药相关障碍 （Sedative-Hypnotic-Anxiolytic-Related Disorders）](entries/Sedative-Hypnotic-Anxiolytic-Related-Disorders.md)
    - [兴奋剂相关障碍 （Stimulant-Related Disorders）](entries/Stimulant-Related-Disorders.md)
    - [烟草相关障碍 （Tobacco-Related-Disorders）](entries/Tobacco-Related-Disorders.md)

- **新增 3 个精神障碍诊断词条**
    - [遗忘症 （Amnesia）](entries/Amnesia.md) - 记忆功能受损的神经认知障碍
    - [沟通障碍 （Communication Disorders）](entries/Communication-Disorders.md) - 语言表达与理解障碍
    - [特定学习障碍 （Specific Learning Disorder）](entries/Specific-Learning-Disorder.md) - 学业技能获取困难
    - [分裂样精神病性障碍 （Schizophreniform Disorder）](entries/Schizophreniform-Disorder.md) - 短期精神分裂症样症状

- **新增 Tulpa 实践核心词条 (PR #301)**
    - [Forcing](entries/Forcing.md) - Tulpa 创建的核心训练方法
    - [Parroting/Puppeting](entries/Parroting-Puppeting.md) - 识别鹦鹉学舌与傀儡操控现象
    - [Deviation](entries/Deviation.md) - Tulpa 自主偏离预期设定的发展过程

- **新增 8 个角色与身份相关词条 (PR #298)**
    - [创造者 （Creative）](entries/Creative.md) - 系统内负责艺术与创意产出的成员
    - [社交者 （Social）](entries/Social.md) - 负责外部社交互动的成员
    - [内射人格 （Introject）](entries/Introject.md) - 基于外部人物或角色形成的人格
    - [非人类人格 （Nonhuman Alter）](entries/Nonhuman-Alter.md) - 非人类身份认同的系统成员
    - [成年人格 （Adult Alter）](entries/Adult-Alter.md) - 呈现成年心智状态的人格
    - [青少年人格 （Teen Alter）](entries/Teen-Alter.md) - 呈现青少年心智状态的人格
    - [创伤持有者 （Trauma Holder）](entries/Trauma-Holder.md) - 承载特定创伤记忆的成员
    - [非创伤持有者 （Non-Trauma Holder）](entries/Non-Trauma-Holder.md) - 不直接持有创伤记忆的成员

- **新增非我感核心概念 (PR #302)**
    - [非我感 （Not-me Feeling）](entries/Not-Me-Feeling.md) - 识别系统成员边界的核心体验机制

### 📚 词条完善

- **人格障碍词条优化 (PR #299, #300)**
    - 重写边缘型人格障碍 (BPD) 词条,新增 DSM-5-TR 诊断标准与鉴别诊断
    - 重写自恋型人格障碍 (NPD) 词条,统一诊断标题格式
    - 补充内部空间 (Inner World) 词条的理论基础与实践方法
    - 统一人格障碍词条结构:概述→诊断要点(ICD/DSM/差异)→临床表现→流行病学→鉴别→治疗→社群→相关条目→参考

- **系统运作词条重构 (PR #296)**
    - 重构前台 (Fronting)、后台 (Background)、共前台 (Co-fronting) 词条
    - 完善自动驾驶 (Autopilot) 与切换 (Switching) 机制说明
    - 统一运作机制词条格式与内部链接

- **融合与整合安全提示强化 (PR #295)**
    - 重写融合 (Fusion) 词条,新增触发警告与安全边界说明
    - 重写整合 (Integration) 词条,补充阶段路径与自愿前提
    - 在系统运作导览中强调融合/整合的安全与自愿原则

- **DPDR 词条重构 (PR #302)**
    - 完善人格解体/现实解体障碍 (DPDR) 诊断标准
    - 新增与 DID/OSDD 的鉴别要点
    - 补充治疗方法与临床实践指引

- **实践指南整合 (PR #301)**
    - 更新实践指南导览,整合 Tulpa 三阶段训练体系
    - 优化 Tulpa 实践路径与相关词条链接
    - 完善冥想、可视化等意识训练方法说明

### 🎨 界面与体验优化

- **主题索引页面新增 (PR #292)**
    - 创建 8 个主题索引页面:Clinical-Diagnosis-index、System-Operations-index、Practice-index、Trauma-Healing-index、Roles-Identity-index、Theory-Classification-index、Cultural-Media-index
    - 优化导览结构,提升主题浏览体验
    - 统一索引页面 Frontmatter 格式

- **主题跟随系统选项**
    - 添加主题跟随系统选项支持,自动适配浅色/深色模式

### 🔧 基础设施改进

- **CI/CD 优化**
    - 集成 build_partitions_cn 到 auto-fix-entries 工作流,自动生成索引与 SUMMARY
    - 改进 PR Frontmatter 检查机制,确保索引页面合规
    - 修复主题索引页面缺少必需 Frontmatter 字段的问题

- **工具文档重构 (PR #303)**
    - 重构工具文档结构,创建独立的 Tools-Index.md
    - 清理废弃文件,优化文档组织
    - 修复技术规范文档中的工具文档引用路径

- **代码质量**
    - 运行 fix_markdown 与 check_links 验证所有新增词条
    - 统一词条 tags、updated、description 字段格式
    - 完善词条间的内部链接网络

### 📊 统计信息

- 新增词条:30+ 个
- 完善词条:15+ 个
- 新增索引页:8 个
- 修复链接错误:10+ 处

---

## [v3.13.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.13.0) - DSM-5-TR 诊断体系完善与 Favicon 支持 (2025-10-16)

### ✨ 新增词条

- **新增 12 个 DSM-5-TR 核心诊断词条**
    - [焦虑障碍 （Anxiety Disorders）](entries/Anxiety-Disorders.md) - 焦虑障碍总览词条
    - [退行 （Regression）](entries/Regression.md) - 心理防御机制与解离现象的重要概念
    - [妄想障碍 （Delusional Disorder）](entries/Delusional-Disorder.md) - 持续性妄想但无精神分裂症谱系其他症状
    - [短暂性精神病性障碍 （Brief Psychotic Disorder）](entries/Brief-Psychotic-Disorder.md) - 短期精神病性症状发作
    - [分裂情感性障碍 （Schizoaffective Disorder）](entries/Schizoaffective-Disorder.md) - 精神分裂症与情感障碍的复合诊断
    - [疾病焦虑障碍 （Illness Anxiety Disorder）](entries/Illness-Anxiety-Disorder.md) - 对患严重疾病的过度担忧
    - [影响其他躯体疾病的心理因素 （Psychological Factors Affecting Other Medical Conditions）](entries/Psychological-Factors-Affecting-Other-Medical-Conditions.md)
    - [储物障碍 （Hoarding Disorder）](entries/Hoarding-Disorder.md) - 强迫性储物行为
    - [拔毛障碍 （Trichotillomania）](entries/Trichotillomania-Hair-Pulling-Disorder.md) - 反复拔除自己的毛发
    - [抓挖障碍 （Excoriation Disorder）](entries/Excoriation-Skin-Picking-Disorder.md) - 反复抓挖皮肤导致损伤
    - [经前焦虑障碍 （Premenstrual Dysphoric Disorder, PMDD）](entries/Premenstrual-Dysphoric-Disorder.md) - 月经前期的严重情绪症状
    - [其他特定的和未特定的性别焦虑 （Other Specified/Unspecified Gender Dysphoria）](entries/Other-Specified-Unspecified-Gender-Dysphoria.md)

### 📚 词条完善

- **重构核心障碍词条**
    - 重写双相障碍词条，对齐抑郁障碍和焦虑障碍格式标准
    - 重命名 Anxiety.md 为 Anxiety-Disorders.md 并统一术语
    - 完善重性抑郁障碍 (MDD) 词条，新增子类型说明与关联词条
    - 强化解离性时间定向障碍指引内容

- **词条关联优化**
    - 完善 DID、OSDD、创伤相关词条的内部链接
    - 增强 IAD 与 PFAOMC 的交叉互引
    - 重命名儿童人格词条并更新退行相关链接
    - 补充退行词条文献引用，重构核心特征与鉴别诊断

- **导览体系改进**
    - 增强临床诊断导览，新增神经系统疾病章节
    - 更新 DSM5tr.md 完成状态标记
    - 修正 DSM-5-TR 分类结构为官方 22 章标准

### 🎨 界面与体验优化

- **Favicon 多尺寸支持**
    - 添加 7 种尺寸的 favicon 文件（16x16, 32x32, 48x48, 180x180, 192x192, 512x512）
    - 配置 MkDocs Material 主题 favicon 支持
    - 优化不同设备和浏览器的图标显示效果

- **文档改进**
    - 重构快速开始与贡献指南，采用 MkDocs Material 现代化组件
    - 优化标题和导览结构

### 🔧 基础设施改进

- **CI/CD 优化**
    - 优化 PR 检查工作流，完整执行所有检查后再报错
    - 修复链接检查工具在单文件检查时排除列表不生效的问题
    - 优化代码结构，减少 check_links.py 重复代码

- **代码质量**
    - 修复多个词条的链接错误
    - 统一 UDD 文件命名为 SDD.md
    - 修复 Premenstrual-Dysphoric-Disorder.md 链接错误

### 🌐 其他改进

- 添加 Logo 设计师到贡献者列表
- 修复格式问题和提交优化

---

## [v3.12.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.12.0) - 进食障碍词条扩充与 SEO 优化 (2025-10-14)

### ✨ 新增词条

- **新增 3 个进食障碍核心词条**
    - [神经性厌食症 （Anorexia Nervosa, AN）](entries/Anorexia-Nervosa-AN.md) - 限制性饮食和体重显著偏低的进食障碍
    - [神经性贪食症 （Bulimia Nervosa, BN）](entries/Bulimia-Nervosa-BN.md) - 反复暴食与补偿行为的进食障碍
    - [暴食障碍 （Binge Eating Disorder, BED）](entries/Binge-Eating-Disorder-BED.md) - 无补偿行为的反复暴食障碍

### 📚 词条完善

- **SEO 优化**
    - 为 32 个核心词条添加 description 字段，提升搜索引擎可见度
    - 修正搜索路由和关键词策略，优化 sitemap 配置
    - 为偏重词条添加 synonyms 字段，支持同义词搜索

- **词条内容完善**
    - 补全 ASPD 词条中 PCL-R 量表缺失的 3 个项目
    - 补充歇斯底里与精神病态词条的现代诊断与测验内容
    - 完善慢性疼痛等词条的 DSM-5-TR 标准
    - 新增 [DSM-5-TR 量表概览](entries/DSM-5-TR-Scales.md) 词条

- **导览优化**
    - 为心理治疗词条添加内部链接并完善导览
    - 在创伤与疗愈导览中补充 ACT 疗法
    - 优化创伤与疗愈导览词条总览结构
    - 修正 ACT 词条中 Switch 的链接错误

### 🔧 基础设施改进

- **CI/CD 优化**
    - 添加 PR 阶段 CI 检查，验证链接规范和 Frontmatter
    - 在 PR 检查中添加 topic 字段验证
    - 增强链接检查工具并集成到 CI 流程

- **搜索功能增强**
    - 修复搜索同义词索引不支持字符串格式的问题
    - 增强搜索功能，支持索引 Frontmatter 中的 synonyms 字段

- **性能优化**
    - 禁用 navigation.instant 以优化页面交互性能
    - 移除 mkdocs-recently-updated-docs 依赖，实现自定义最近更新功能
    - 修复本地测试时 /updates 页面为空的问题

### 📖 文档优化

- **首页改进**
    - 改进首页导���结构
    - 更新首页主题卡片文案
    - 优化首页显示和布局

- **贡献文档**
    - 完善贡献指南和技术约定文档
    - 更新术语表索引和使用建议
    - 增强条目状态说明

- **工具文档**
    - 更新 check_links.py 排除列表和文档说明
    - 更新开发日志

### 🌐 其他改进

- 添加 Cloudflare Web Analytics 追踪代码
- 禁用 GitHub Pages Jekyll 构建
- 移除过时的 PYTHON_VERSION 环境变量配置
- 优化主页布局并清理 QQ 群相关功能

---

## [v3.11.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.11.0) - 精神障碍词条扩充与贡献体系完善 (2025-10-13)

### ✨ 新增词条

- **新增 11 个精神障碍诊断词条**
    - [急性应激障碍 （ASD）](entries/Acute-Stress-Disorder-ASD.md) - 创伤后 3 天至 1 个月的急性应激反应
    - [适应障碍 （Adjustment Disorders）](entries/Adjustment-Disorders.md) - 对可识别应激源的不成比例情绪/行为反应
    - [长期哀伤障碍 （PGD）](entries/Prolonged-Grief-Disorder.md) - 亲密关系人死亡后的持续强烈哀伤反应
    - [失眠障碍](entries/Insomnia-Disorder.md) - 睡眠数量/质量不满，包含 CBT-I 治疗策略
    - [重性抑郁障碍 （MDD）](entries/Major-Depressive-Disorder-MDD.md) - 持续 ≥2 周的抑郁心境
    - [持续性抑郁障碍 （PDD）](entries/Persistent-Depressive-Disorder-PDD.md) - 慢性抑郁 ≥2 年
    - [选择性缄默症 （SM）](entries/Selective-Mutism-SM.md) - 特定社交情境无法说话
    - [社交焦虑障碍 （SAD）](entries/Social-Anxiety-Disorder-SAD.md) - 对社交/表现情境的强烈恐惧
    - [惊恐障碍 （Panic Disorder）](entries/Panic-Disorder.md) - 反复意外惊恐发作
    - [躯体变形障碍 （BDD）](entries/Body-Dysmorphic-Disorder-BDD.md) - 对外貌缺陷的强迫性关注

- **新增 4 个历史术语词条**
    - [癔症 （Hysteria，已过时）](entries/Hysteria.md) - 追溯从古希腊"游走子宫"到现代诊断的演变
    - [分离转换障碍 （ICD-10 F44，已过时）](entries/Dissociative-Conversion-Disorder-Obsolete.md) - ICD-10 混合分类的历史问题
    - [多人格障碍 （MPD，已过时）](entries/Multiple-Personality-Disorder-Obsolete.md) - DSM-III-R 术语到 DID 的演变
    - [易性症 （Transsexualism，已过时）](entries/Transsexualism-Obsolete.md) - 从 ICD-9 到 ICD-11 的性别诊断演变

### 📚 词条完善

- **扩展惊恐障碍词条**
    - 添加惊恐发作完整 DSM-5-TR 症状清单（13 项症状）
    - 补充与广场恐惧症、解离障碍的共病关系

- **优化并行 (Parallelism) 词条**
    - 完善词条结构与内容
    - 增强与切换 (Switch) 词条的相互关联性

### 🔧 贡献体系完善

- **贡献者墙上线**
    - 新增 [贡献者墙页面](contributing/contributors.md)
    - 使用 MkDocs Material Grid Cards 展示核心维护者
    - 添加 GitHub 头像（核心维护者 80px，贡献者表格 40px）
    - 响应式卡片布局，自适应屏幕尺寸

- **贡献指南文件重命名**
    - 所有中文文件名改为英文，提升兼容性
    - PR流程.md → pr-workflow.md
    - 学术引用.md → academic-citation.md
    - 诊断临床规范.md → clinical-guidelines.md
    - 技术约定.md → technical-conventions.md
    - 编写规范.md → writing-guidelines.md

- **贡献者团队更新**
    - 核心维护者 4 人：[@kuliantnt](https://github.com/kuliantnt)、[@shishuiliunian5](https://github.com/shishuiliunian5)、[@fengqingyu430-collab](https://github.com/fengqingyu430-collab)、[@GrainRR](https://github.com/GrainRR)
    - 新增词条贡献者：[@raven027192](https://github.com/raven027192)
    - 其他贡献者：[@XingY-YuXi](https://github.com/XingY-YuXi)、[@Jellyfish-eng](https://github.com/Jellyfish-eng)

### 📖 导览优化

- **临床诊断导览重构**
    - 更新 27 个条目的状态标记从"草稿"到"已完成"
    - 新增 DSM5tr.md 清单，为 60 个已存在词条打勾
    - 优化章节结构，添加快速导航卡片
    - 合并"非正式诊断"和"已过时诊断"为"非正式与历史术语"章节
    - 细分为"非正式术语"和"历史诊断（已过时）"子章节

- **首页导航优化**
    - 合并重复的"快速导航"与"快速入口"区块
    - 在"快速导航"区新增"快速入口"子区块
    - 提升页面结构清晰度，改善用户体验

### ⚙️ 配置优化

- **搜索功能增强**
    - 优化搜索配置和依赖项，提升部署性能
    - 配置搜索排除规则，避免索引模板和导览文件

- **导航菜单增强**
    - 在导航菜单底部添加"回到主站"链接
    - 添加 MPS Team 主站导航链接

### 📝 开发文档

- 维护开发文档
- 重构管理员操作指南
- 添加项目改进建议文档
- 更新 CONTRIBUTING.md 所有链接指向新文件名
- 更新 README.md 项目结构说明

---

## [v3.10.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.10.0) - 搜索优化与基础设施迁移 (2025-10-12)

### ✨ 新功能

- **AI 辅助搜索词典生成工具链**
    - 新增基于 GPT-5 的搜索词典清洗工具
    - 自动提取和审核词条候选项
    - 支持分词测试和词典质量评估
    - 优化中文搜索匹配准确度

- **搜索体验全面优化**
    - 使用 GPT-5 清洗后的高质量搜索词典
    - 系统性补充自定义词典基础词
    - 支持自定义词典和短语搜索
    - 优化搜索插件最小匹配长度

### 🚀 基础设施升级

- **迁移至 Cloudflare Pages**
    - 优化中国用户访问速度
    - 清理旧的 CI 配置
    - 更新 Wiki 地址为新域名 `wiki.mpsteam.cn`

- **性能优化**
    - 优化 Sveltia CMS 后台加载性能
    - 改用系统字体解决字体加载失败问题
    - 优化移动端字体支持(iOS/Android)

### 🐛 Bug 修复

- 修复 Sveltia CMS 白屏问题并添加使用说明
- 移除重复的评论系统访问提示
- 移除重复依赖配置
- 统一术语"记忆持有者"并添加相关链接

### 📝 文档优化

- 更新主页内容
- 添加 Star History 图表
- 移除冗余评论说明
- 更新 Head-Pressure.md 词条内容

### 📦 工具改进

- 添加 AI 词典生成工具的临时文件到 `.gitignore`
- 优化词典生成工具链的完整性

### 📊 统计数据

- **文件变更**: 26 个文件修改
- **搜索词典**: 使用 GPT-5 清洗后的高质量词典
- **性能提升**: Cloudflare Pages 加速中国访问

---

## [v3.9.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.9.0) - Giscus 评论系统集成与开发文档优化 (2025-10-11)

### ✨ 新功能

- **集成 Giscus 评论系统**
    - 为所有词条页面添加评论功能
    - 支持 GitHub Discussions 作为评论后端
    - 提供评论回退机制,优化用户体验
    - 添加完整的错误处理和用户指导

### 🐛 Bug 修复

- **修复 Giscus 评论系统问题**
    - 修复 "Unable to create discussion" 错误
    - 改进评论未找到时的回退处理
    - 优化评论区加载和显示逻辑

### 📝 文档优化

- **新增开发文档**
    - 新增 [Sveltia CMS 本地开发指南](dev/LOCAL_DEV_SERVER.md)(推荐阅读)
    - 新增 [Giscus 评论系统集成指南](dev/GISCUS_INTEGRATION.md)
    - 新增 [Giscus 常见问题排查指南](dev/GISCUS_TROUBLESHOOTING.md)

- **整理开发文档结构**
    - 将 Sveltia CMS 本地开发指南移动到 `docs/dev/` 目录
    - 更新 `docs/dev/README.md` 添加新文档索引
    - 清理重复的 PDF 导出文档(`docs/pdf_export/`)

- **修复文档链接**
    - 更新 `docs/ADMIN_GUIDE.md` 中的文档引用链接
    - 修复 `docs/dev/Tools-Index.md` 中的失效链接

### 📊 统计数据

- **文件变更**: 5 个文件修改, 1 个目录删除
- **新增文档**: 3 个开发指南文档
- **删除重复**: 1 个重复的 PDF 文档目录

---

## [v3.8.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.8.0) - 导航优化与新手体验提升 (2025-10-10)

### 📚 内容优化

- **全面优化快速开始指南**
    - 新增"专题深入"章节，整合 5 个专题导览（临床诊断、创伤疗愈、角色身份、理论分类、文化媒体）
    - 重新组织学习路径：基础入门（4个导览）+ 专题深入（5个导览）
    - 新增推荐学习路线：新手路线（0-4周）、进阶路线（1-3个月）、精通路线（3个月以上）
    - 新增常见问题："9个导览页面该如何使用？"
    - 优化阅读技巧，添加"从导览开始"提示

### ♻️ 术语统一

- **统一"接地（Grounding）"术语表述**
    - `docs/index-simple.md`: "立足当下" → "接地"
    - `docs/README.md`: "立足当下" → "接地"
    - `tools/deprecated/retag_and_related.py`: "地面化" → "接地"
    - 确保全站术语一致性

### 🎨 导航优化

- **新增专题导览导航栏**
    - 在 `mkdocs.yml` 添加"专题导览"一级导航
    - 收录 5 个专题导览页面，提供进阶学习入口

- **优化导航结构，移除重复条目**
    - 从"系统运作"移除内部空间、沟通、权限（保留在"实践指南 > 内部协作"）
    - 从"心理健康"移除解离（保留在"核心概念"）和接地（保留在"实践指南"）
    - 确保每个词条在导航中仅出现一次，提高清晰度

### ✨ 新增功能

- **新增 404 错误页面** (`docs/404.md`)
    - 提供友好的导航引导
    - 包含快速链接：首页、标签索引、术语表、快速开始
    - 说明常见原因和使用提示

### 🐛 Bug 修复

- **修复 MkDocs 构建警告**
    - 修正导航中贡献指南路径：`CONTRIBUTING.md` → `contributing/index.md`
    - 修复术语表中缺失的链接：`Pathological-Dissociation.md` → `Dissociative-Disorders.md`

- **修正贡献指南链接路径**
    - `docs/QuickStart.md`: `CONTRIBUTING/index.md` → `contributing/index.md`
    - `docs/README.md`: `CONTRIBUTING/index.md` → `contributing/index.md`
    - `docs/index-simple.md`: `CONTRIBUTING/index.md` → `contributing/index.md`
    - 解决所有页面中贡献指南链接 404 的问题

### 📊 统计数据

- **文件变更**: 7 个文件修改
- **导览整合**: 9 个导览页面（4个基础 + 5个专题）
- **导航条目**: 从 51 个减少到 46 个唯一条目
- **新增页面**: 1 个（404.md）

---

## [v3.7.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.7.0) - MPS 术语体系重构与内容扩充 (2025-10-09)

### ♻️ 术语体系重构（破坏性变更）

- **全面迁移至 MPS（Multiple Personality System，多意识体系统）术语体系**
    - 重命名核心文件：`Plurality.md` → `Multiple_Personality_System.md`
    - 重命名基础文件：`Plurality-Basics.md` → `Mps-Basics.md`
    - 全站替换 "Plurality" 为 "MPS（多意识体系统）"
    - 重写主页，全面引入 MPS 术语体系
    - 更新仓库名称：`plurality_wiki` → `Multiple_personality_system_wiki`
    - 统一主页和各导览页面的术语表述

### 📖 新增内容

- **新增诊断词条**
    - **智力发育障碍（Intellectual Developmental Disorder）** - 参照 DID 标杆结构编写
    - **人格障碍与广泛性焦虑障碍完整词条体系** - 按 DSM-5-TR 体系新增多个诊断条目

- **新增系统类型词条**
    - **系魂型系统（Soulbond System）** - 包含定义、特征及相关讨论

- **补充共病内容**
    - 补充 DID 共病相关内容
    - 新增相关诊断条目的互链

### 🔧 条目优化

- **refactor**: 大幅优化 ADHD 条目，参照 DID 标杆结构
- **refactor**: 优化 ASD 条目，参照 DID 标杆结构
- **docs**: 优化共病与诊断词条结构
- **docs**: 按 DSM-5-TR 完整体系重构诊断导览
- **docs**: 更新临床诊断指南，添加智力发育障碍链接

### 🎨 样式与格式优化

- **style**: 优化心理健康导览问答格式
- **style**: 优化首页术语说明和样式
- **docs**: 添加提示块语法示例以增强文档可读性
- **fix**: 标准化链接格式和改进 markdown 一致性

### 🐛 Bug 修复

- **fix**: 修正转换障碍条目 topic 字段顺序（"临床与诊断" → "诊断与临床"）
- **fix**: 更新系魂文档，修正标签格式和更新时间，优化部分段落表述
- **fix**: 更新文档中的链接和名称，确保一致性
- **fix**: 更新工作流状态链接和 GitHub Pages 地址
- **fix**: 修改域名地址为 mpswiki.page.dev
- **fix**: 正确配置 mkdocs 设置说明

### 🔍 搜索优化

- **fix(search)**: 优化中文搜索分词，解决"系魂"被拆分问题
- **fix**: 移除搜索用户词典配置，改用默认分词

### 🔐 认证与配置

- **fix(auth)**: 支持配置 GitHub OAuth 回调域名

### 📝 文档完善

- **docs**: 添加 Python 环境配置说明文档
- **feat(docs)**: 更新条目维护规范，增加主题总览页面同步要求
- **feat(docs)**: 添加"系魂型系统"条目及相关定义，更新内容以增强文档结构

### 📦 杂务

- **chore**: 用户本地配置与文档格式更新
- **chore**: 更新站点配置和清理文件
- **chore**: 同步仓库改动
- **chore**: 同步本地修改

### 🔨 技术改进

- 优化 Admin.md 中的 Frontmatter 格式，确保标签和同义词的统一性
- 删除过时的心理健康主题词条（Depressive Disorders, Disorientation, Flashback, OCD, PTSD, Trauma）
- 更新 .gitignore：添加 pdf、logs、.obsidian、Codex 规则及特定 pyc 忽略

### ⚠️ 破坏性变更

- 核心术语从 "Plurality" 全面迁移至 "MPS（多意识体系统）"
- 多个核心文件重命名，旧链接可能失效
- 仓库名称变更：`plurality_wiki` → `Multiple_personality_system_wiki`

---

## [v3.6.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.6.0) - 主题导览重构与 CMS 体验优化 (2025-10-08)

### ✨ 内容重构

- **feat(entries)**: 全面重构 7 个主题导览页面
    - [理论与分类导览](guides/Theory-Classification-Guide.md) - 从心理学流派到解离视角的知识地图
    - [诊断与临床导览](guides/Clinical-Diagnosis-Guide.md) - 掌握精神医学诊断语言与临床知识
    - [系统运作导览](guides/System-Operations-Guide.md) - 多意识体系统的日常运作机制
    - [角色与身份导览](guides/Roles-Identity-Guide.md) - 系统中的不同角色与职能分工
    - [文化与表现导览](guides/Cultural-Media-Guide.md) - 影视文学中的多意识体主题
    - [创伤与疗愈导览](guides/Trauma-Healing-Guide.md) - 创伤知情的自助策略与临床框架
    - [实践指南导览](guides/Practice-Guide.md) - 操作性训练方法与实践技巧
- **refactor**: 从层级结构简化为扁平化的主题分类结构
- **refactor**: 更新内部链接为相对路径 + .md 扩展名格式
- **docs**: 统一更新所有导览页面日期为 2025-10-08

### 🔧 Decap CMS 优化

- **feat(admin)**: 新增自动提交消息（遵循 Conventional Commits 规范）
    - `create`: `docs({{collection}}): 新增词条 "{{slug}}"`
    - `update`: `docs({{collection}}): 更新词条 "{{slug}}"`
    - `delete`: `docs({{collection}}): 删除词条 "{{slug}}"`
    - `uploadMedia`: `docs(media): 上传 "{{path}}"`
    - `deleteMedia`: `docs(media): 删除 "{{path}}"`
- **feat(admin)**: 增强视图过滤器
    - 保留原有 7 个主题分类过滤器
    - 新增 "📝 未分类词条" 过滤器（`pattern: '^$'`）
    - 新增 "🆕 最近更新" 过滤器（`pattern: '2025'`）
- **feat(admin)**: 改进视图分组
    - 从标签分组改为"主题分类"和"更新年份"分组
    - 使用正则表达式 `\d{4}` 自动提取年份
- **feat(admin)**: 优化字段配置
    - 明确文件扩展名 `.md` 和 frontmatter 格式
    - 添加 `topic` 字段默认值为空字符串
    - 添加 `updated` 字段提示文本和禁用 UTC
    - 优化标题字段提示文本，强调中英文分离

### 🎨 界面改进

- **style**: 优化首页导航布局
- **style**: 完善管理员入口样式

### 📊 技术细节

- **文件变更**: 8 个文件修改，297 行新增，540 行删除
- **配置增强**: config.yml 新增 6 个配置项
- **用户体验**: 编辑器提示更清晰，分类筛选更智能

---

## [v3.5.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.5.0) - Sveltia CMS 迁移与增强 (2025-10-07)

### ✨ 新功能

- **feat(admin)**: 迁移到 Sveltia CMS，提供更好的搜索和用户体验
- **feat**: 优化 Decap CMS 配置，增强词条过滤和分组功能
- **feat**: 添加 topic 主题分类字段
- **feat**: 添加 Decap CMS 本地开发配置

### 🐛 修复

- **fix(admin)**: 移除多余的 en 字段，title 已包含英文/缩写
- **fix(admin)**: 更新 topic 字段下拉选项以匹配实际值
- **fix(admin)**: 修正 topic 筛选器以匹配实际词条值
- **fix(entries)**: 统一 topic 字段值为"诊断与临床"
- **fix(auth)**: 修复 OAuth 回调使用 postMessage 与 Decap CMS 通信
- **fix**: 修复 Decap CMS 布局问题并优化样式
- **fix**: 修复登录页面 Logo 和双重加载动画问题
- **fix(cms)**: 创建缺失的媒体上传目录修复 Decap CMS 加载问题

### 📝 文档

- **docs**: 完成 Sveltia CMS 迁移相关文档更新
- **docs**: 更新 README 工具说明

### 🎨 样式优化

- **style**: 全面升级 Decap CMS 界面设计
- **style**: 大幅简化 admin.css，移除冲突样式

### 🔧 重构

- **refactor**: 删除重复的病理性解离词条，统一使用解离障碍
- **refactor(admin)**: 移除自定义加载动画，使用 Decap CMS 自带加载器
- **refactor**: 优化 Decap CMS OAuth 认证流程

### 其他改进

- 优化词条列表布局和添加排序分页功能
- 切换回生产环境配置
- 在主页和诊断导览中添加完整解离障碍词条链接

---

## [v3.4.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.4.0) - 工具重构与链接检查增强 (2025-10-07)

### 🔧 工具重构与整合

- **Markdown 处理工具整合**
    - 整合 `fix_md.py`、`fix_bold_format.py`、`fix_list_bold_colon.py` 到统一的 `tools/processors/markdown.py`
    - 新增 `MarkdownProcessor` 类提供统一接口
    - 支持 13 条 Markdownlint 规则（MD009, MD012, MD022, MD028, MD031, MD032, MD034, MD037, MD040, MD047）
    - 支持 5 条自定义中文排版规则（列表标记空格、加粗空格、列表加粗冒号、链接括号、链接前冒号）
    - 旧工具移至 `tools/deprecated/`，新增详细迁移指南
    - 全局更新所有引用：`fix_md.py` → `fix_markdown.py`（涉及 15 个文件）

- **链接检查脚本重构**
    - 支持上下文感知验证（entries、docs_root、docs_subdir、root、other）
    - 修复 docs 根目录判断问题（区分 `docs/Glossary.md` 和 `docs/contributing/index.md`）
    - 支持尖括号包裹的 Markdown 链接格式 `[text](<url>)`
    - 新增文件排除列表，跳过文档示例和模板文件

- **清理 Docsify 时代的过时工具**
    - 移除 `docs_preview.py` → 使用 `mkdocs serve` 替代
    - 移除 `generate_tags_index.py` → 使用 MkDocs Material tags 插件替代
    - 移除标签管理工具组（7个）：`add_top_level_tags.py`, `add_topic_tags.py`, `analyze_current_tags.py`, `analyze_tags.py`, `optimize_tags.py`, `update_entry_tags.py`, `retag_and_related.py`
    - 所有过时工具移至 `tools/deprecated/` 目录保留历史
    - 新增 `docs/dev/CLEANUP_RECOMMENDATIONS.md` 详细分析报告

### 📝 文档改进

- **管理员指南集成**
    - 将 ADMIN_GUIDE.md 添加到贡献指南导航和参考资源
    - 修复 ADMIN_GUIDE.md 中的链接路径问题

- **更新维护文档**
    - 更新核心配置文件：`.claude/CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`
    - 更新贡献文档：`docs/contributing/` 目录下所有文件
    - 更新开发文档：`docs/dev/`, `docs/tools/`
    - 更新批处理脚本：`tools/run_local_updates.{bat,sh}`
    - 补充 MkDocs Material 替代功能说明

### 🎨 设计优化

- **新增 SVG 可视化图表**
    - `healthy-pathological-boundary.svg` - 健康与病理性多意识体的界限
    - 使用渐变色和双向箭头展示解离程度谱系
    - 更新 Core-Concepts-Guide.md 使用 SVG 替代文本图表

- **品牌设计更新**
    - 更新 favicon 为 Multiple Personality System Wiki 专属网络连接图案
    - 清理根目录遗留的 assets 文件夹
    - 清理 Docsify 遗留的数据文件和 legacy 目录

### 📖 新增内容

- 新增功能性神经症状障碍（FND）词条
- 优化文档格式和链接

---

## [v3.3.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.3.0) - 贡献指南重构与文档优化 (2025-10-07)

### 📚 贡献指南重构

- 将 CONTRIBUTING/index.md 拆分为 6 个专题文档到 `docs/contributing/`
    - **index.md** - 贡献指南总览
    - **编写规范.md** - 语言、格式规范
    - **学术引用.md** - 引用格式、证据分级
    - **诊断临床规范.md** - 病理学内容要求
    - **技术约定.md** - 文件结构、链接管理
    - **PR流程.md** - 提交流程、检查清单
- 根目录 CONTRIBUTING/index.md 改为简化版，指向详细文档

### 📖 新增内容

- 新增 **Tulpa 完全创造指南系列**（基础篇、实践篇、提高篇）
- 新增 **实践指南导览**
- 新增 **核心概念导航结构**

### 🔧 文档优化

- 重组静态资源目录结构（`figures/images/icons`）
- 移动导览文件到 `docs/entries/`
- 移动 `FRONTEND_ARCHITECTURE.md` 到 `docs/dev/`
- 优化首页布局与核心主题展示
- 更新所有相关链接和文件引用

### 🐛 问题修复

- 修复文档链接错误
- 修复列表粗体冒号格式
- 修复图片路径规范
- 修复 PDF 导出目录跳转

### 🎨 格式优化

- 统一中英文排版格式
- 增强 `fix_md.py` 支持更多 markdownlint 规则
- 优化加粗文本空格规范

### 📋 其他改进

- 同步更新 `AGENTS.md` 和 `CLAUDE.md`
- 优化 `.gitignore` 配置
- 删除重复文件和过时说明

---

## v3.2.0 (2025-10-06)

### ✨ 新功能

- **新增六大主题导览页面完善导航体系**

    - Cultural-Media-Guide.md - 文化与表现导览
    - Trauma-Healing-Guide.md - 创伤与疗愈导览
    - Theory-Classification-Guide.md - 理论与分类导览
    - Roles-Identity-Guide.md - 角色与身份导览
    - Clinical-Diagnosis-Guide.md - 诊断与临床导览
    - DSM-ICD-Diagnosis-Index.md - DSM-5 & ICD-11 官方诊断索引

- **新增三阶段创伤治疗模型词条**

    - entries/Three-Phase-Trauma-Treatment.md
    - 阶段 1：安全与稳定
    - 阶段 2：创伤记忆加工
    - 阶段 3：整合与重建
    - 包含多意识体系统的特殊考量

### ♻️ 重构

- **精简所有导览页面内容，统一采用简洁描述风格**

    - 参考 System-Operations-Guide.md 的格式
    - 移除罗嗦的多级子点说明
    - 每个词条改为一句核心描述
    - 保持清晰的章节结构

- **重构诊断与临床导览**

    - 包含所有 27 个 topic 为"诊断与临床"的词条
    - 按类别组织：解离性障碍、创伤相关、情绪与焦虑、人格障碍等
    - 每个词条包含 DSM-5-TR/ICD-11 编码

- **简化创伤与疗愈导览为纯目录格式**

    - 移除详细的阶段说明（转移至独立词条）
    - 保留关键分类和简洁描述

### 📝 文档

- **更新主页和标签索引的主题导览链接**

    - tags.md 更新所有主题导览链接和描述
    - index.md 更新核心主题部分的导览链接
    - 所有主题导览现在指向独立的导览/索引页面

### 🐛 修复

- **PDF 导出支持导览页面和索引页面**

    - 修复 PDF 导出脚本未包含导览页面的问题
    - 新增支持：*-Guide.md,*-Operations.md, DSM-ICD-*.md, Glossary.md
    - 导览页面无 frontmatter 时使用简化处理
    - 现在 PDF 导出包含所有 8 个导览/索引页面

## v3.1.0 (2025-10-06)

### ✨ 新功能

- **全站启用 TOC 在左侧显示，隐藏导航树** ([ed12ffc](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/ed12ffc))

    - 使用 CSS 隐藏左侧导航树
    - 将页面目录（TOC）移到左侧显示
    - 所有页面（包括搜索结果）都有一致的 TOC 显示
    - 内容区域更宽敞，阅读体验更好

### 🐛 修复

- **禁用 toc.integrate 确保所有页面都显示左侧导航** ([6612b21](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/6612b21))

    - 修复通过搜索访问的词条页面没有左侧导航的问题
    - 移除 toc.integrate 配置项，避免导航不一致

- **修复 Markdown 加粗格式在 MkDocs Material 中的渲染问题**

    - 修复 ` [**text**](url) ` 格式不正确渲染([批量修复 14 个文件，67 处问题](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/[commit_hash]))
    - 修复列表中加粗文本缺少空格的问题
    - 统一使用全角括号和冒号
    - 创建自动修复工具 `tools/fix_bold_format.py`
    - 更新 CONTRIBUTING/index.md 和 TEMPLATE_ENTRY.md 添加格式规范

### 📝 文档

- **更新贡献指南添加 MkDocs Material 兼容性格式规范**

    - 详细说明加粗链接、列表格式、括号和冒号的正确用法
    - 提供错误和正确示例对比
    - 添加自动修复工具使用说明

### 🔧 工具

- **新增 Markdown 格式自动修复工具** （`tools/fix_bold_format.py`）

    - 自动修复加粗链接格式
    - 自动修复列表加粗间距
    - 自动转换半角括号为全角
    - 自动修正冒号格式
    - 支持批量处理并生成详细报告

---

## [v3.0.0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/releases/tag/v3.0.0) - 医疗内容规范化与前端优化 (2025-10-05)

### ✨ 医疗内容规范化

- **为所有 40 个医疗相关词条添加统一的警告框**
    - ⚠️ **触发警告**: 提醒读者内容涉及敏感议题
    - ℹ️ **免责声明**: 明确资料仅供参考，不构成医疗建议
    - **覆盖词条类型**：
    - 诊断类 (20个): DID, OSDD, PTSD, CPTSD, 精神分裂症等
    - 症状/现象类 (12个): 解离, 人格解体, 闪回等
    - 治疗/干预类 (8个): 创伤, 接地, 情绪调节等
    - 理论模型类 (2个): 结构性解离理论, ANP/EP模型

### 🔧 前端优化

- 将核心主题改为扁平列表布局
- 优化主页核心主题展示
- 改善移动端和桌面端的阅读体验

### 🐛 Bug 修复

- 修复标签索引生成脚本的链接路径问题
- 修正导览页面内部链接路径
- 修正 Cloudflare Pages 构建脚本依赖文件路径

### 📝 文档与内容

- 重构系统运作导览与导航
- 为所有词条添加主题分类标签
- 优化标签索引排序算法

### 🗂️ 重构

- 删除根目录 entries/ 文件夹
- 统一所有词条位置到 docs/entries/

### ⚠️ 破坏性变更

- 根目录 entries/ 文件夹已删除，所有词条现位于 docs/entries/
- 部分内部链接路径已更新，旧书签可能失效

---

## v2.2.0 (2025-10-05)

### 🔧 重构（重大更新）

- **完成 tools 目录重构第二阶段**

    - 新增三大核心处理器模块([9e19aec](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/9e19aec))
    - `processors/markdown.py` - 基于 fix_md.py 重构,支持 7 种 Markdown lint 规则
    - `processors/links.py` - 基于 check_links.py 重构,完整的链接完整性检查
    - `processors/tags.py` - 基于 retag_and_related.py 重构,智能标签提取与规范化
    - 完整的 Python 类型提示和数据类支持
    - 统一的配置管理和日志系统
    - 详细的 API 文档和使用示例

- **完成 tools 目录重构第一阶段** - 基础设施建设([6e39282](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/6e39282))

    - 新增 `core/` 核心模块
    - `config.py` - 统一配置管理系统
    - `frontmatter.py` - YAML frontmatter 解析器
    - `logger.py` - 分级日志系统
    - `utils.py` - 通用工具函数库
    - 新增 `cli/` 命令行接口模块
    - `main.py` - 统一的 CLI 入口和参数解析
    - 创建模块化目录结构
    - `generators/` - 生成器模块目录
    - `processors/` - 处理器模块目录
    - `validators/` - 校验器模块目录
    - 完整的重构计划文档 `REFACTORING_PLAN.md`

### 🐛 修复（关键问题）

- **修复标签重建脚本导致的无意义排序变更** ([9e19aec](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/9e19aec))

    - 问题：浮点数精度导致每次执行 `retag_and_related.py` 时相关词条顺序发生微小变化
    - 解决：在 `retag_and_related.py:664-670` 实现多级排序键
    - 将分数四舍五入到 6 位小数避免浮点数微小差异
    - 添加英文标题和路径作为次要排序键确保完全稳定
    - 影响：消除了大量词条的无意义 Git diff,保持仓库整洁
    - 详细文档：新增 `docs/RETAG_STABILITY_FIX.md` 记录问题分析和解决方案

### ✨ 新增

- **增强本地维护脚本功能** ([9e19aec](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/9e19aec))

    - `run_local_updates.bat` 完全重写（168 行）
    - 支持 8 个维护步骤的独立跳过选项（`--skip-*`）
    - 添加完整的帮助信息（`--help`）
    - 实现进度显示（[1/8] 到 [8/8]）
    - UTF-8 编码支持（`chcp 65001`）
    - 错误检测和警告提示
    - `run_local_updates.sh` 同步增强
    - 添加搜索索引生成步骤
    - 修复输出格式问题
    - 保持与 .bat 版本功能一致

- **优化 .gitignore 配置** ([9e19aec](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/9e19aec))

    - 添加完整的 Python 缓存规则（` __pycache__ /`、`*.py[cod]` 等）
    - 清理已跟踪的 Python 缓存文件
    - 移除冗余的特定路径配置

### 📝 文档

- **更新工具文档** `docs/dev/Tools-Index.md`([9e19aec](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/9e19aec))

    - 新增"核心处理器模块(重构后)"章节
    - 详细的 API 文档和使用示例
    - `MarkdownProcessor` 类完整说明
    - `LinkProcessor` 类完整说明
    - `TagProcessor` 类完整说明
    - 更新 `run_local_updates` 脚本文档
    - 完整的 8 个执行步骤说明
    - 所有 `--skip-*` 选项文档
    - Windows 和 Linux/macOS 使用示例

- **新增技术文档** `docs/RETAG_STABILITY_FIX.md`([9e19aec](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/9e19aec))

    - 问题描述：排序不稳定的技术原因
    - 解决方案：浮点数精度处理和多级排序
    - 代码对比：修改前后的详细对比
    - 验证结果：测试脚本和稳定性验证

- **更新重构计划** `tools/REFACTORING_PLAN.md`([6e39282](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/6e39282))

    - 标记 Phase 1（基础设施）为已完成
    - 标记 Phase 2（处理器模块）为已完成
    - 详细的实现进度和下一步计划

### 📦 杂务（自动更新）

- 更新搜索索引（新增 72 条索引）
- 更新 last-updated 时间戳（256 个词条）
- 自动更新相关词条链接（60 个词条）

### 🎨 风格（格式优化）

- 统一触发警告卡片样式
    - 内容居中对齐([09aafcf](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/09aafcf))
    - 调整卡片尺寸适配网页显示([115b4fa](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/115b4fa))
    - 确保 PDF 导出兼容性([cc4c458](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/cc4c458))
- 修正索引导航跳转 404 问题([debe96b](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/debe96b))
- 优化混合型系统词条结构([d358046](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/d358046))
- 修复 Subsystem.md 位置和格式问题([1031114](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/1031114))

### 🔨 开发者体验

- 添加 Claude 项目配置文件([880fa5e](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/880fa5e))
- 更新 .gitignore 忽略 .claude 目录([70b1001](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/70b1001))

— 由 Git 提交记录和 dev 分支合并整理生成

## v2.1.0 (2025-10-04)

### ✨ 新增

- 维护“超级破碎者”词条([394a5f6](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/394a5f6b3d463d274904173448b528545c0ec5a0))
- 新增词条「去现实化」「内部沟通」，并更新「结构性解离理论」与相关索引([0b1e156](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/0b1e1568bb61035a1c8e1ad2040fc838b2b9ea59))
- 新增词条「习得性无助」([9bd6bfe](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/9bd6bfea818bdc6d9268026a7c9135c2ebd1c9e6))
- 删除过时的 Codex 上下文与计划文件，简化项目结构([5e3890f](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/5e3890f2d019fcd170b6bf6396a1322e7b67c8c1))
- 更新 `.gitignore` 以包含 Codex 相关文件([4c248ba](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/4c248bab4679422035a266672ddc749c44391798))
- 按照拼音的方式优化搜索([3645a0e](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/3645a0e0aa1f1bb0fc43cf7f8dbcc5fc297263dd))

### 🐛 修复（链接/引用/格式）

- 修正标题别名提取并重建搜索索引([3645a0e](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/3645a0e0aa1f1bb0fc43cf7f8dbcc5fc297263dd))
- 同义词与元数据维护：补全《独立性》词条同义词，修正 synonyms 配置（[2e9b455](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/2e9b455800607bcfc6e8313ad102e00b70ca0c5d)，[61329aa](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/61329aa0579ffbad3149b8315d1cb2e3e24e6733)）
- 标签与搜索相关修复与优化：调整标签匹配/优化过滤、修复标签页功能（代表性提交：[8c2612c](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/8c2612cf976a0422a431b3d1fb6226acfcabdcba)，[37f83b3](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/37f83b3256f5405be4054d7807068518bb20b961)）
- 自动化与 CI：修复 GitHub CI 与自动化维护脚本缺陷（[e0e4743](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/e0e4743e805e45e9135d8650c5b4aeab104243cf)，[337e805](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/337e805e116ef059dd6860db37796bf3d821a001)）

### 📝 文档与索引（不影响语义）

- 更新管理员维护手册([df15786](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/df15786c86c9f3991c01f31014e8a46d02df420b))

### 📦 杂务（脚本/CI/批处理）

- 修复 `change.log` 命名错误([cdf6325](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/cdf6325f8a6b0dad3b50963af6835bd3625443f3))
- 更新维护脚本与管理员指南([58dffa3](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/58dffa350ef01d361cd3d8203d406e80b4a8c751))
- 安装文档检查依赖([bcc546a](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/bcc546ad233d518859e22c3cb211bb6c653c5075))
- 维护自动化脚本与标签索引模块([24cb674](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/24cb67477e18eb3a3224271d7341068959c96e92))

— 由 Git 提交记录自动生成

## v2.0.0 (2025-10-04)

### ✨ 新增

- 增加 Windows 本地维护批处理脚本([9c66ea0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/9c66ea09b38696af2e5fa8028df366d91be0bbe1))
- PDF 导出目录复用 `index.md`，并同步导出结构与索引顺序（[1b21db2](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/1b21db29fd86ac651e7271ed4c81098f32741c06)，[61eed04](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/61eed0496b91a6a64aa8a8fff44041f782ae4884)）
- 重新生成各词条 **tags** 与“相关条目”区块([72abcdd](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/72abcdd4b46c53356972db07d97058be9832f8d8))
- 更新术语表并新增神经多样性链接；工具脚本支持生成标签索引([fa3295f](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/fa3295f1d2feb8d98f0f0f21a76227b676173e61))
- 优化远端分支清理脚本：加入安全分支切换与干运行（dry-run）([58fa841](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/58fa84198746ae8b4d925d676894da5eef2955eb))
- 新增：神经多样性与感官调节词条([95707e8](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/95707e8213fee4e9342b3f77385aebea9eaa35b3))
- 调整标签清单的版式以提升可读性([39915c7](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/39915c75ce6e746aec7089c2ca801cef659fa4a4))

### 🐛 修复（链接/引用/格式）

- 补充“弦羽分类”相关索引（合并重复修复）（[2e62e6e](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/2e62e6e5de753948416e4fa67ec6fd10395d62e5)，[9c96b19](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/9c96b19b2063e5a5ae9d4221106f8bbde49a0ef2)）
- 将 `retag_and_related.py` 纳入更新命令，修复执行缺失([1667fec](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/1667fec4a3fb5b1f7571a077b814cbbd7020329d))
- 扩展 frontmatter `updated` 字段兼容性；修复多行标签解析与类型转换（[0dd4584](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/0dd4584963f785d4fd00227ee7eec433ea5d3fc5)，[992e0ab](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/992e0ab4964abe81f14cf8252614e2d15b256f86)，[2ad3f10](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/2ad3f10cc15adb0c47b9a7d8966bc1349741d4e1)）
- 隐藏 Docsify 前端对 frontmatter 元数据的渲染（合并重复修复）（[0184635](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/018463576239e617794752e4a41b479f1697e3dc)，[07cd27e](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/07cd27ea2aa4d7e00e3761a475598637cdceb7d9)）
- 表格展示与响应式修复（PC 端显示、术语表布局与全局化）（代表性提交：[8f35457](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/8f35457606235fb347bc99e2ba97c130bb71dd0d)，[9c19d3d](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/9c19d3decf53f650139f944c5d961783f7d84c08)）
- 修正“最近更新”链接路径（合并重复修复）（[8ba3e1a](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/8ba3e1acb1bc9ffb77801f339214026410aa7f99)，[a80b8d0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/a80b8d01d57be097bc93df87ec40b9af7889e554)）
- 移除不必要的 `_sidebar.md` 忽略配置([d6e30ae](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/d6e30ae55aa9522c8f1dc454003aa5ce1a4c4546))
- 标签列表格式化（焦虑/双相障碍）([d7cd081](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/d7cd08171085c51f0135817841a43a55393b0ceb))
- 更新贡献与开发约定（markdownlint 要求等）并同步校对报告生成时间([cc3bd32](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/cc3bd32b4512adfa3c9acc4504009f5aa01b9693))
- 补全部分诊断词条模板章节([3a3ee06](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/3a3ee069405c635fb871a0786d83aa07f3090e56))

### 📝 文档与索引（不影响语义）

- 重构部分诊断词条的章节结构([fa22795](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/fa2279556fb71a8be24caaabe85be614faa1efa9))
- 补充链接检查脚本的使用说明([216ccfa](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/216ccfafaa7cf94c08c392df9d43d8eff1f450c1))
- 统一若干文档的小幅格式修正（代表性提交：[871d44a](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/871d44af70fb509a96bd669d04c42df4294e3efc)，[295d04f](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/295d04fd52f5b33bd5a7b3a4c754d1b19d2ae8c9)）

### 🔧 重构（不改变内容含义）

- **（破坏性变更）** 迁移为 **tags** 管理模式，统一词条目录结构([d267385](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/d2673853f61b5a4a6eab17e325baa899c826c0e4))

### 📦 杂务（脚本/CI/批处理）

- 删除旧版更新脚本 `update.cmd`([e085f51](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/e085f51f0cba2d934cd310a5d221a45308b2e356))

### 🎨 风格（空格/缩进/行尾等）

- 统一多处空行与段落间距，提升可读性([34b979f](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/34b979ff29c77a15691ef511365fa6bf79e67040))

— 由 Git 提交记录自动生成

## v1.3.4 (2025-10-03)

### ✨ 新增

- feat: 添加弦羽理论生态位分类法及相关系统条目([a4a1724](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/a4a17243500114d96c05b31cb2f1894a7d98a712))
- feat: 关于我们是最好朋友的事([aa101e1](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/aa101e1ed4eaa34af2d19b7cb6ac36c61894489e))
- feat: 添加远端分支清理脚本([999cf69](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/999cf690c324a9b21a4be54f211ce57cf347b66a))
- （合并）新增/更新若干占位或示例条目（[b865b47](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/b865b475cfde93eb60ef1f9d5acee83e7cdae9bb)，[d070503](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/d070503d57195e32ae2c82a53883ac9372153213)）

### 🐛 修复（链接/引用/格式）

- fix: 添加触发警示并更新系统定义，提升可读性([0f292a2](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/0f292a2d56b95c55c35bf24d7382dbe8b35d34fd))
- fix: 替换条目中的中文路径链接([d0e9cb8](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/d0e9cb8787f76ee18f1839557893051a4f0e4ed4))
- fix: 更新自动校对报告时间；移除无效检查项与标题格式问题([ebdb19f](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/ebdb19f0afa1a11dd913225549c2ce4056f908d8))
- fix: 更新术语表，补充缺失条目并修复格式([0ceffc2](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/0ceffc2a83b59c4a5b59ea72fe583dba71da2d6c))
- fix: 启用更新脚本以生成“最后更新时间”([f2fc449](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/f2fc4490291b7d194803a5996b888fcb719d0114))
- fix: 依据校对报告微调部分词条结构([8fa7e77](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/8fa7e77231da264ea958989b01f2a288ecf12995))
- fix: 更新页脚维护者信息，补充系统名称([dcc184a](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/dcc184a9f15205147baf7fb36aea445d2ca985a4))
- fix: 修正条目模板与更新日志的排版([350382e](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/350382e7cdaa5efedf0024eb6d79521c8ed0cdaa))
- fix: 调整 DID 共病术语([4b43c4b](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/4b43c4b56da041de1523af7b72556adab03fb8ca))

### 📝 文档与索引（不影响语义）

- 术语表与布局改造：区分桌面/移动展示并重构为移动友好（[81d3cf6](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/81d3cf69d7678a0c9842bd0b2060b0032d0d9a3a)，[578b068](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/578b0681ef9ac6e2fd70700c38f94614694866ab)）
- 文档结构与索引：更新 README 的仓库结构概览与文档位置/链接（[301047e](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/301047e0d2ee39cfe5d3f1885bf09bf4923a8ceb)，[9e9a502](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/9e9a502db310380b9ca69670454282612ec7e24e)）
- 贡献/运维文档：新增 GitHub 提交流程与管理员指南（[d4ffb8e](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/d4ffb8e109cfb526240bb6ece8c6d4d88e0988a8)，[eb58ef4](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/eb58ef455737cff072a33c9419a4ed99ab125aea)）
- 自动化与导出：同步自动化工具与 PDF 导出文档到 docs([8790314](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/8790314176ca70f58ff5226faecde43a639c3a27))
- AGENTS 规则：补充前端资产脚本注释与贡献约定（[fa85303](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/fa85303ddee6df569f93b86f233ccfcae8233642)，[c383990](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/c38399026fb8e256b8c319a3ac32e6fb074d9605)）
- CI 徽章与状态：替换为 shields.io 并修正状态链接（[bea3510](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/bea35103b1ecc502d3d3cb564a9f97c21ff9f88d)，[7709dd0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/7709dd031ae81a9c8a94cc874ec2c8e9242dd322)）
- 术语表分类与常规小修：拆分类别、补充与微调（[6f12fb6](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/6f12fb62d77b74fb0a9db38d691e9574e682e1dc)，[b8304e3](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/b8304e35b6269e049e0268cd20cd62ca4da38ffc)）
- 语法与排版：统一 Markdown 与文档格式([7033eea](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/7033eeac4b08469e8faa13f795827b4cab1ec87f))
- 贡献指南与模板：补充条目规范与自检清单([49d8375](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/49d8375beb86c5b1ea14804edaf38cafc1595e29))

### 📦 杂务（脚本/CI/批处理）

- chore: 调整校对脚本目录([cdae64f](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/cdae64f3e38b210c764c19b4de76818240b7eb2d))

— 由 Git 提交记录自动生成

## v1.3.3 (2025-10-03)

### ✨ 新增

- 重构图帕词条结构并补充研究说明([5f4f526](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/5f4f5261336202d8f3a4a0759b4854d35dec33a0))
- 拆分解离词条并新增功能性与病理性内容([1f66649](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/1f66649771c6c6cad29ec990e7a98b2ec0bef49f))
- 新增谵妄词条并强化定向障碍关联([02a5dda](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/02a5ddacc77157da63c4bd45699544e9262a9902))
- 补充解离主题条目的相关链接([a793724](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/a7937241f81256040e416f8b758aa9fbef7b5eb6))
- 更新更新日志([fdd952f](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/fdd952f8c54f169c5ac7218b3691ece0715e66d0))

### 🐛 修复（链接/引用/格式）

- 完善移动端搜索结果后的侧边栏收起([c00ac19](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/c00ac19c554578f31d102ce0466045cba932ece4))
- 防止搜索框在移动端触发侧边栏收起([81c01d0](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/81c01d0524b6f2dbac8788f2e1ce1945b9b3eab7))

### 📝 文档与索引（不影响语义）

- 补充弦羽理论触发模型细节([7a54653](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/7a546532747250efa645d1c02148f399c3390acb))
- 补充触发并发风险提醒([70bd9e6](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/70bd9e648c07d6639a3843278aa09ad4ac655bf3))

### 📦 杂务（脚本/CI/批处理）

- 更新 last-updated 索引([39001d1](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/39001d195db07b5f88ad63842dd02e9f53db322b))

— 由 Git 提交记录自动生成

## v1.3.2 (2025-10-03)

### ✨ 新增

- 更新创伤和解离性身份障碍条目，整合定义、特征及实务建议([15c663e](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/15c663e2a3df00d045047df35c64fa306f0eb9fe))
- 更新 OSDD、DPDR、抑郁障碍及条目贡献指南，增加定义、特征及实务建议([9438267](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/94382673a5cf9373e9fdae4409d8acf07129ea94))
- 更新 DID 和闪回条目，补充定义、特征及实务建议([55b8133](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/55b81335070bca5694124efcbaae9918f80fba37))
- 新增 PTSD 条目([fc3068e](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/fc3068e0c3737247b489562a24950c5a684fd36e))
- 更新 OCD 条目([f8e8c2c](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/f8e8c2c92f3d94b8896a5143cb6e7285bd7920e6))
- 新增“交换”条目([76af9f5](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/76af9f52e230d2b710d32f4672ba81c211ee7b9d))
- 更新里空间和条目模板([3ac7f75](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/3ac7f7586183134b7abcc15798736ca346137d26))
- 新增“共前台”和“偏重”条目([215c07e](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/215c07e5b1a5398cb10ab7e8bf7e511a459e7f15))
- 新增“侵入性思维”条目([bbdc85e](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/bbdc85e478b72f69c5ea8a2e3f9fbb75590bacaf))
- 更新 ANP-EP 模型([180e810](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/180e810831c12ad917490fe0d587044705ec2dc1))
- 新增“超级破碎（Polyfragmented）”条目([3be416c](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/3be416ccef567df69776fc0e034e211f48e892b2))
- 更新冥想与接地条目（[ca49692](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/ca496924df32b04267a27f8971950250f66cc9b7)，[6bd286f](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/6bd286f4c746e8248ad68d0480e55a110933fb67)）
- 更新 T 语条目（[f4310e6](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/f4310e6229fbe1719c96853ba3352a04038880f0)，[d54730c](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/d54730c99da1b58bc00bf967c5166b679b0635c4)）
- 新增“头压”条目([f8e4575](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/f8e4575a142b94f8ae4fbc0d4303a8ed2a3af9e8))
- 更新投射、内投射、外投射条目([f9dcd31](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/f9dcd3133cf113f7a469ec429830958eae0a3245))
- 扩充核心板块速览内容([38e74cc](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/38e74ccc5af53d72607d3a188e81e274746676b1))

### 🐛 修复（链接/引用/格式）

- 更新“头压”条目并修复 md 文件链接问题([3b980b5](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/3b980b5c6fa48eb4b7b758bb3b64172618b2e57e))
- 重写 PDF 导出中的词条链接([4c11d83](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/4c11d835e7ddfcea3d92f61b9062dafbf7d9d9ac))
- 修正贡献指南 URL 错误([df06f22](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/df06f221a10bd0d0e9b6a0a2133e663ed071381e))
- 调整侧边栏标题与搜索栏顺序([95dd0e8](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/95dd0e8411783ed9c6748bf2d3c99778b14f7b55))
- 修正“最近更新”页面的词条标题显示([d5b2aaf](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/d5b2aafde506c8b33ae3c6639bf13abd2c294694))
- 更新“莉莉丝”术语([d30531b](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/d30531bcf5a41afa2b7a29bc5a31f4380926de51))

### 📦 杂务（脚本/CI/批处理）

- 强制更新 last-updated 索引([2c78f0c](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/2c78f0ceab0f92726781935c6788216baf5857e6))

— 由 Git 提交记录自动生成

## v1.3.1 (2025-10-02)

### ✨ 新增

- 首页展示最近更新入口([8886c97](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/8886c9767ab5436969af8ab5bc1b4c9819944b7e))
- 增加最近更新页面自动生成脚本([fcccd0a](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/fcccd0affce8ed84459079c3903d93467f76d1ba))
- 在 PDF 导出中渲染最后更新时间([8b5475f](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/8b5475f0f93cb49441fd744b5fcbd636437f3aa1))
- 显示词条最后更新时间([cfe1729](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/cfe172935a2b7efe54eaad0efb15708a7b45c498))

### 🐛 修复（链接/引用/格式）

- 修复 changelog.md 输出问题([8b6d0db](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/8b6d0db719a8b49966b40185f646ef82dd454711))
- 调整站点标题后缀显示([8431f3e](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/8431f3e800c5b0373f1f7157058e74ae83c3647a))

### 📝 文档与索引（不影响语义）

- 修改 changelog 文档([1c36386](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/1c363866d4c4376b500ba8a74440d44210b643eb))
- 更新 README 中工具说明([e231636](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/e231636bf955f18caef92521e60f40bb030bb529))

### 🔧 重构（不改变内容含义）

- 移除 Docsify 最后更新功能([441ec22](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/441ec22aee1f7ccdbf760c68475a2968f1711f3a))

### 🎨 风格（空格/缩进/行尾等）

- 调整 agents 配置与站点 SVG 图标（[9cb4db5](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/9cb4db5b5deec0e8516ebf0ea85c1009561aaf28)，[e231636](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/e231636bf955f18caef92521e60f40bb030bb529)）

— 由 Git 提交记录自动生成

## v1.3.0 (2025-10-02)

### ✨ 新增

- 支持输出最新标签到 HEAD 的简化日志([289f802](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/289f802b7e0951c888cc2d29e8f014822712e96b))
- 首页快速入口卡片化改版([51600ed](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/51600edd830ca05dbe91837d266bcc48a7590d99))
- 优化中英文排版间距([18db44a](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/18db44a2c21884131c30a7c002fd589b1d568469))
- 重构主页布局与样式([3d09e03](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/3d09e038c81fb0af4974e9dfaf3712507725a8af))
- mainpage 编辑改进([64ad6bc](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/64ad6bce90fa0ce92cc53a54c3709726326e6857))

### 🐛 修复（链接/引用/格式）

- 修正 404 页面对 `.md` 直链的跳转([744dc37](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/744dc37e5e325d72a3099a1bf66056bccf0881fc))
- 修复 mainpage 显示问题([98e8a41](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/98e8a41739826ab88232dcbc6736aff56bf79ca6))
- 修复主页主按钮在不同主题下的可见性([7bdecf1](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/7bdecf1d406bfeb26b52861413be8d4e24dc9b96))
- 优化主页按钮与快速入口布局([0adca3c](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/0adca3c6a9ed732e852066988f654a40fd729cac))
- 调整主页按钮与快速入口文案([0583549](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/05835490c5fd4d64fa9b1b964d6e4655e9f03a00))
- 调整暗色模式快速入口下拉样式([b489d86](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/b489d869493d5323dd8289797324f6be44356b41))
- 修复链接与文件重命名引用问题([8ccea60](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/8ccea609de7fe5d3c51bfed97d2ba645dbb51fa0))
- 修复 GitHub Active 检查及 Lint 错误（[d443fb9](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/d443fb9930238fed5336351de13b89e803270653)，[ef4efcb](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/ef4efcb9a49c65166effe5b1f1689d9018131ee8)，[66433d2](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/66433d2d6c2b3c5a498abb2b2e2e8f2cda8684ec)）
- 主页快速入口显示 bug 修复（[2144eab](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/2144eabdc9882912f1123533e5e559ceba352b40)，[7ae6f63](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/7ae6f63859dcc69aaaaac8a84f3f910df50e9e03)）
- bugfix: Main_Page 修复([7acb79d](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/7acb79d2f5b67af0462b39f31c50970ebe961e72))

### 📝 文档与索引（不影响语义）

- 在 README 添加自动化维护章节([25d9484](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/25d94849a0a393783a9b38cd872080b48bc355d6))
- 修改首页描述([03ec264](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/03ec264c1cdd45eea4f098c07abd20d588270947))
- 更新 README、AGENTS 与 CONTRIBUTING 说明（[b81dfaa](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/b81dfaa3b645d974b7197fd53633e6992eeb672d)，[46e7a38](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/46e7a38ceb326afedf24a9ac60943e1b42c6a781)，[440bc42](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/440bc4207600a4ab2f64af4f873162628e413ffc)）

### 🔧 重构（不改变内容含义）

- 将主页迁移为 HTML 页面([57a28a7](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/57a28a7d7c8fda4701432cb114550bec941dc7d2))

### 🎨 风格（空格/缩进/行尾等）

- 修改图标样式([0352260](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/03522608cd8a6c4ad40f94ac48990d3aab762177))
- 重设计主页面页脚([774472d](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/774472d7a2ad9bdbaaa58f2180f18bab6ce9d927))

## v1.2.4 (2025-10-02)

### ✨ 新增

- 优化 PDF 封面并提升暗黑模式对比度([3b9b997](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/3b9b9978a36cef7a2fcdda6d55b6db9831842da7))

### 🐛 修复（链接/引用/格式）

- 修复 README([17e10f8](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/17e10f8c71902daac9afc8d3b73873c96d09e99f))
- 修复链接问题([b0d378c](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/b0d378c5a5e52172b7a0ad6f1b933b8b2462b4fa))
- 本地化最后更新时间插件([bff6afe](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/bff6afe9d97ac6fc011a949e4da841006eac9111))
- 修复 Docsify 最后更新时间占位符([7d86299](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/7d8629913b1c819ec084c4f7cb5ffc2d37fec715))

### 📦 杂务（脚本/CI/批处理）

- 添加 changlog([255fbff](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/255fbffde42896029c2e846349f391685ce1d475))
- 新增 GitHub 社区配置([44d6392](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/44d63921b2d553f219002a30468fd31ca2057720))
- 修改 agents([35a9f2a](https://github.com/mps-team-cn/Multiple_personality_system_wiki/commit/35a9f2a8f25c33519da52178c53c0f3a10557e30))

## v1.2.3 (2025-10-01)

### ✨ 新增

- 引入 Docsify 首页与在线浏览支持；补充“后台/里空间”等术语词条。

### 🐛 修复

- 修复 PDF 导出重复标题与若干导出异常。
- 修正首页与文档页 404、直链跳转、导航加载等问题。
- 调整暗黑模式下的侧边栏与配色一致性。
- 使用 SVG favicon 以规避 PR 限制；新增 404 跳转处理。

### 📝 文档 / 结构

- 修正 ANP-EP 模型、内部空间等词条的索引与互链。
- 调整多意识体基础词条路径并配置映射。
- 更新 README 与站点文案。

### 📦 杂务

- 保留/清理 Docsify 相关辅助与站点文件。

---

## v1.2 (2025-09-30)

### 📝 文档

- 在 README 新增“系统语录”，并统一词条标题格式。
- 润色《前言》，修复 PDF 导出缺少“前言”的问题。
- 完善 ADHD、精神分裂症等诊断描述；调整抑郁障碍词条标题。
- 新增/完善：Tulpa（图帕）、宿主等词条与命名统一。

### 🐛 修复 / 改进

- 统一入口与导航，修复首页/导航加载及直达链接 404。

### 📚 术语与索引

- 补充并维护语录、索引与若干文档条目的一致性。

---

## v1.1 (2025-09-30)

### ✨ 新增

- 新增“解离”与“侵入性思维/强迫相关”词条，并纳入索引。

---

## v1.0 (2025-09-30)

### ✨ PDF 导出（新增/改进）

- 新增“一键导出 Wiki 为 PDF”的脚本与流程。
- 支持自定义封面与目录，目录与 README 索引对齐；条目间自动分页。
- 新增忽略清单与目录构建修复（即使 README 被忽略也能正确导出）。

### 🐛 PDF 导出（修复）

- 修复中文字体不显示、LaTeX 封面格式、封面特殊字符转义等问题。
- 修复 Windows 11 环境下的导出错误、目录结构/项目根路径解析等问题。

### 📝 文档

- 新增/维护：DID（含 DSM-5 诊断标准）、CPTSD、Meditation 等词条；

  将 OSDD、Partial DID 等条目纳入 `index`/README 索引；
  多处 README/条目内容与格式修正（含病理学相关内容维护）。

### 🗂️ 结构与规范

- 调整与归档：按主题重组 `entries/` 目录结构；
- 新增贡献指南（CONTRIBUTING/AGENTS 等），统一写作与提交流程。

---

— 由 Git 提交记录自动整理（合并同类项、去除纯合并/无信息提交）
