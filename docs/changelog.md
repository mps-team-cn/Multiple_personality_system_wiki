# 更新日志

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
  - 参考 System-Operations.md 的格式
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
  - 新增支持：*-Guide.md, *-Operations.md, DSM-ICD-*.md, Glossary.md
  - 导览页面无 frontmatter 时使用简化处理
  - 现在 PDF 导出包含所有 8 个导览/索引页面

## v3.1.0 (2025-10-06)

### ✨ 新功能

- **全站启用 TOC 在左侧显示，隐藏导航树**（[ed12ffc](https://github.com/kuliantnt/plurality_wiki/commit/ed12ffc)）
  - 使用 CSS 隐藏左侧导航树
  - 将页面目录（TOC）移到左侧显示
  - 所有页面（包括搜索结果）都有一致的 TOC 显示
  - 内容区域更宽敞，阅读体验更好

### 🐛 修复

- **禁用 toc.integrate 确保所有页面都显示左侧导航**（[6612b21](https://github.com/kuliantnt/plurality_wiki/commit/6612b21)）
  - 修复通过搜索访问的词条页面没有左侧导航的问题
  - 移除 toc.integrate 配置项，避免导航不一致

- **修复 Markdown 加粗格式在 MkDocs Material 中的渲染问题**
  - 修复 `**[text](url)**` 格式不正确渲染（[批量修复 14 个文件，67 处问题](https://github.com/kuliantnt/plurality_wiki/commit/[commit_hash])）
  - 修复列表中加粗文本缺少空格的问题
  - 统一使用全角括号和冒号
  - 创建自动修复工具 `tools/fix_bold_format.py`
  - 更新 CONTRIBUTING.md 和 TEMPLATE_ENTRY.md 添加格式规范

### 📝 文档

- **更新贡献指南添加 MkDocs Material 兼容性格式规范**
  - 详细说明加粗链接、列表格式、括号和冒号的正确用法
  - 提供错误和正确示例对比
  - 添加自动修复工具使用说明

### 🔧 工具

- **新增 Markdown 格式自动修复工具**（`tools/fix_bold_format.py`）
  - 自动修复加粗链接格式
  - 自动修复列表加粗间距
  - 自动转换半角括号为全角
  - 自动修正冒号格式
  - 支持批量处理并生成详细报告

---

## v3.0.0 (2025-10-06)

### ✨ 重大更新

- **为所有医疗相关词条添加统一警告框**（[aa0b3f6](https://github.com/kuliantnt/plurality_wiki/commit/aa0b3f6)）
  - 新增统一格式的触发警告和免责声明
  - 覆盖 40 个医疗相关词条
    - 诊断类 (20个): DID, OSDD, PTSD, CPTSD, 精神分裂症, 双相障碍, 边缘型人格障碍等
    - 症状/现象类 (12个): 解离, 人格解体, 现实解体, 闪回, 侵入性思维等
    - 治疗/干预类 (8个): 创伤, 地面化, 情绪调节, 应激反应等
    - 理论模型类 (2个): 结构性解离理论, ANP/EP模型
  - 移除旧格式警告文字,统一使用 MkDocs admonitions 样式
  - 提供一致的用户体验和法律免责保护

### 🔧 前端优化

- **将核心主题改为扁平列表布局**（[47adc36](https://github.com/kuliantnt/plurality_wiki/commit/47adc36)）
  - 优化主页核心主题展示布局
  - 改善移动端和桌面端的阅读体验

- **优化主页核心主题展示**（[c5655bb](https://github.com/kuliantnt/plurality_wiki/commit/c5655bb)）
  - 增强首页视觉层次
  - 改进核心概念的可发现性

### 🐛 修复

- **修复标签索引生成脚本的链接路径问题**（[78b2356](https://github.com/kuliantnt/plurality_wiki/commit/78b2356)）
  - 解决标签索引中的链接错误
  - 确保所有标签页面正确跳转

- **修正导览页面内部链接路径**（[e6a2e29](https://github.com/kuliantnt/plurality_wiki/commit/e6a2e29)）
  - 修复导航链接 404 问题
  - 统一链接路径规范

- **修正 Cloudflare Pages 构建脚本依赖文件路径**（[5f76cce](https://github.com/kuliantnt/plurality_wiki/commit/5f76cce)）
  - 解决 CI/CD 构建失败问题
  - 确保自动部署正常运行

### 📝 文档与内容

- **重构系统运作导览与导航**（[2adc852](https://github.com/kuliantnt/plurality_wiki/commit/2adc852)）
  - 优化系统运作相关文档结构
  - 改进导航体验和内容组织

- **为所有词条添加主题分类标签并优化标签索引排序**（[51b8c80](https://github.com/kuliantnt/plurality_wiki/commit/51b8c80)）
  - 实现全站词条主题分类
  - 优化标签索引的排序算法
  - 提升内容可发现性

### 🗂️ 重构

- **删除根目录 entries/ 文件夹**（[9616690](https://github.com/kuliantnt/plurality_wiki/commit/9616690)）
  - 完成文件结构迁移
  - 统一所有词条位置到 `docs/entries/`
  - 简化项目结构

### 📦 杂务

- 自动运行 `generate_tags_index.py` 更新标签索引
- 自动运行 `fix_md.py` 修复 Markdown 格式
- 清理无用文件和目录

### ⚠️ 破坏性变更

- 根目录 `entries/` 文件夹已删除,所有词条现位于 `docs/entries/`
- 部分内部链接路径已更新,旧书签可能失效

— 由 Git 提交记录整理生成

## v2.2.0 (2025-10-05)

### 🔧 重构（重大更新）

- **完成 tools 目录重构第二阶段**
  - 新增三大核心处理器模块（[9e19aec](https://github.com/kuliantnt/plurality_wiki/commit/9e19aec)）
    - `processors/markdown.py` - 基于 fix_md.py 重构,支持 7 种 Markdown lint 规则
    - `processors/links.py` - 基于 check_links.py 重构,完整的链接完整性检查
    - `processors/tags.py` - 基于 retag_and_related.py 重构,智能标签提取与规范化
  - 完整的 Python 类型提示和数据类支持
  - 统一的配置管理和日志系统
  - 详细的 API 文档和使用示例

- **完成 tools 目录重构第一阶段** - 基础设施建设（[6e39282](https://github.com/kuliantnt/plurality_wiki/commit/6e39282)）
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

- **修复标签重建脚本导致的无意义排序变更**（[9e19aec](https://github.com/kuliantnt/plurality_wiki/commit/9e19aec)）
  - 问题：浮点数精度导致每次执行 `retag_and_related.py` 时相关词条顺序发生微小变化
  - 解决：在 `retag_and_related.py:664-670` 实现多级排序键
    - 将分数四舍五入到 6 位小数避免浮点数微小差异
    - 添加英文标题和路径作为次要排序键确保完全稳定
  - 影响：消除了大量词条的无意义 Git diff,保持仓库整洁
  - 详细文档：新增 `docs/RETAG_STABILITY_FIX.md` 记录问题分析和解决方案

### ✨ 新增

- **增强本地维护脚本功能**（[9e19aec](https://github.com/kuliantnt/plurality_wiki/commit/9e19aec)）
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

- **优化 .gitignore 配置**（[9e19aec](https://github.com/kuliantnt/plurality_wiki/commit/9e19aec)）
  - 添加完整的 Python 缓存规则（`__pycache__/`、`*.py[cod]` 等）
  - 清理已跟踪的 Python 缓存文件
  - 移除冗余的特定路径配置

### 📝 文档

- **更新工具文档** `docs/tools/README.md`（[9e19aec](https://github.com/kuliantnt/plurality_wiki/commit/9e19aec)）
  - 新增"核心处理器模块(重构后)"章节
  - 详细的 API 文档和使用示例
    - `MarkdownProcessor` 类完整说明
    - `LinkProcessor` 类完整说明
    - `TagProcessor` 类完整说明
  - 更新 `run_local_updates` 脚本文档
    - 完整的 8 个执行步骤说明
    - 所有 `--skip-*` 选项文档
    - Windows 和 Linux/macOS 使用示例

- **新增技术文档** `docs/RETAG_STABILITY_FIX.md`（[9e19aec](https://github.com/kuliantnt/plurality_wiki/commit/9e19aec)）
  - 问题描述：排序不稳定的技术原因
  - 解决方案：浮点数精度处理和多级排序
  - 代码对比：修改前后的详细对比
  - 验证结果：测试脚本和稳定性验证

- **更新重构计划** `tools/REFACTORING_PLAN.md`（[6e39282](https://github.com/kuliantnt/plurality_wiki/commit/6e39282)）
  - 标记 Phase 1（基础设施）为已完成
  - 标记 Phase 2（处理器模块）为已完成
  - 详细的实现进度和下一步计划

### 📦 杂务（自动更新）

- 更新搜索索引（新增 72 条索引）
- 更新 last-updated 时间戳（256 个词条）
- 自动更新相关词条链接（60 个词条）

### 🎨 风格（格式优化）

- 统一触发警告卡片样式
  - 内容居中对齐（[09aafcf](https://github.com/kuliantnt/plurality_wiki/commit/09aafcf)）
  - 调整卡片尺寸适配网页显示（[115b4fa](https://github.com/kuliantnt/plurality_wiki/commit/115b4fa)）
  - 确保 PDF 导出兼容性（[cc4c458](https://github.com/kuliantnt/plurality_wiki/commit/cc4c458)）
- 修正索引导航跳转 404 问题（[debe96b](https://github.com/kuliantnt/plurality_wiki/commit/debe96b)）
- 优化混合型系统词条结构（[d358046](https://github.com/kuliantnt/plurality_wiki/commit/d358046)）
- 修复 Subsystem.md 位置和格式问题（[1031114](https://github.com/kuliantnt/plurality_wiki/commit/1031114)）

### 🔨 开发者体验

- 添加 Claude 项目配置文件（[880fa5e](https://github.com/kuliantnt/plurality_wiki/commit/880fa5e)）
- 更新 .gitignore 忽略 .claude 目录（[70b1001](https://github.com/kuliantnt/plurality_wiki/commit/70b1001)）

— 由 Git 提交记录和 dev 分支合并整理生成

## v2.1.0 (2025-10-04)

### ✨ 新增

- 维护“超级破碎者”词条（[394a5f6](https://github.com/kuliantnt/plurality_wiki/commit/394a5f6b3d463d274904173448b528545c0ec5a0)）
- 新增词条「去现实化」「内部沟通」，并更新「结构性解离理论」与相关索引（[0b1e156](https://github.com/kuliantnt/plurality_wiki/commit/0b1e1568bb61035a1c8e1ad2040fc838b2b9ea59)）
- 新增词条「习得性无助」（[9bd6bfe](https://github.com/kuliantnt/plurality_wiki/commit/9bd6bfea818bdc6d9268026a7c9135c2ebd1c9e6)）
- 删除过时的 Codex 上下文与计划文件，简化项目结构（[5e3890f](https://github.com/kuliantnt/plurality_wiki/commit/5e3890f2d019fcd170b6bf6396a1322e7b67c8c1)）
- 更新 `.gitignore` 以包含 Codex 相关文件（[4c248ba](https://github.com/kuliantnt/plurality_wiki/commit/4c248bab4679422035a266672ddc749c44391798)）
- 按照拼音的方式优化搜索（[3645a0e](https://github.com/kuliantnt/plurality_wiki/commit/3645a0e0aa1f1bb0fc43cf7f8dbcc5fc297263dd)）

### 🐛 修复（链接/引用/格式）

- 修正标题别名提取并重建搜索索引（[3645a0e](https://github.com/kuliantnt/plurality_wiki/commit/3645a0e0aa1f1bb0fc43cf7f8dbcc5fc297263dd)）
- 同义词与元数据维护：补全《独立性》词条同义词，修正 synonyms 配置（[2e9b455](https://github.com/kuliantnt/plurality_wiki/commit/2e9b455800607bcfc6e8313ad102e00b70ca0c5d)，[61329aa](https://github.com/kuliantnt/plurality_wiki/commit/61329aa0579ffbad3149b8315d1cb2e3e24e6733)）
- 标签与搜索相关修复与优化：调整标签匹配/优化过滤、修复标签页功能（代表性提交：[8c2612c](https://github.com/kuliantnt/plurality_wiki/commit/8c2612cf976a0422a431b3d1fb6226acfcabdcba)，[37f83b3](https://github.com/kuliantnt/plurality_wiki/commit/37f83b3256f5405be4054d7807068518bb20b961)）
- 自动化与 CI：修复 GitHub CI 与自动化维护脚本缺陷（[e0e4743](https://github.com/kuliantnt/plurality_wiki/commit/e0e4743e805e45e9135d8650c5b4aeab104243cf)，[337e805](https://github.com/kuliantnt/plurality_wiki/commit/337e805e116ef059dd6860db37796bf3d821a001)）

### 📝 文档与索引（不影响语义）

- 更新管理员维护手册（[df15786](https://github.com/kuliantnt/plurality_wiki/commit/df15786c86c9f3991c01f31014e8a46d02df420b)）

### 📦 杂务（脚本/CI/批处理）

- 修复 `change.log` 命名错误（[cdf6325](https://github.com/kuliantnt/plurality_wiki/commit/cdf6325f8a6b0dad3b50963af6835bd3625443f3)）
- 更新维护脚本与管理员指南（[58dffa3](https://github.com/kuliantnt/plurality_wiki/commit/58dffa350ef01d361cd3d8203d406e80b4a8c751)）
- 安装文档检查依赖（[bcc546a](https://github.com/kuliantnt/plurality_wiki/commit/bcc546ad233d518859e22c3cb211bb6c653c5075)）
- 维护自动化脚本与标签索引模块（[24cb674](https://github.com/kuliantnt/plurality_wiki/commit/24cb67477e18eb3a3224271d7341068959c96e92)）

— 由 Git 提交记录自动生成

## v2.0.0 (2025-10-04)

### ✨ 新增

- 增加 Windows 本地维护批处理脚本（[9c66ea0](https://github.com/kuliantnt/plurality_wiki/commit/9c66ea09b38696af2e5fa8028df366d91be0bbe1)）
- PDF 导出目录复用 `index.md`，并同步导出结构与索引顺序（[1b21db2](https://github.com/kuliantnt/plurality_wiki/commit/1b21db29fd86ac651e7271ed4c81098f32741c06)，[61eed04](https://github.com/kuliantnt/plurality_wiki/commit/61eed0496b91a6a64aa8a8fff44041f782ae4884)）
- 重新生成各词条 **tags** 与“相关条目”区块（[72abcdd](https://github.com/kuliantnt/plurality_wiki/commit/72abcdd4b46c53356972db07d97058be9832f8d8)）
- 更新术语表并新增神经多样性链接；工具脚本支持生成标签索引（[fa3295f](https://github.com/kuliantnt/plurality_wiki/commit/fa3295f1d2feb8d98f0f0f21a76227b676173e61)）
- 优化远端分支清理脚本：加入安全分支切换与干运行（dry-run）（[58fa841](https://github.com/kuliantnt/plurality_wiki/commit/58fa84198746ae8b4d925d676894da5eef2955eb)）
- 新增：神经多样性与感官调节词条（[95707e8](https://github.com/kuliantnt/plurality_wiki/commit/95707e8213fee4e9342b3f77385aebea9eaa35b3)）
- 调整标签清单的版式以提升可读性（[39915c7](https://github.com/kuliantnt/plurality_wiki/commit/39915c75ce6e746aec7089c2ca801cef659fa4a4)）

### 🐛 修复（链接/引用/格式）

- 补充“弦羽分类”相关索引（合并重复修复）（[2e62e6e](https://github.com/kuliantnt/plurality_wiki/commit/2e62e6e5de753948416e4fa67ec6fd10395d62e5)，[9c96b19](https://github.com/kuliantnt/plurality_wiki/commit/9c96b19b2063e5a5ae9d4221106f8bbde49a0ef2)）
- 将 `retag_and_related.py` 纳入更新命令，修复执行缺失（[1667fec](https://github.com/kuliantnt/plurality_wiki/commit/1667fec4a3fb5b1f7571a077b814cbbd7020329d)）
- 扩展 frontmatter `updated` 字段兼容性；修复多行标签解析与类型转换（[0dd4584](https://github.com/kuliantnt/plurality_wiki/commit/0dd4584963f785d4fd00227ee7eec433ea5d3fc5)，[992e0ab](https://github.com/kuliantnt/plurality_wiki/commit/992e0ab4964abe81f14cf8252614e2d15b256f86)，[2ad3f10](https://github.com/kuliantnt/plurality_wiki/commit/2ad3f10cc15adb0c47b9a7d8966bc1349741d4e1)）
- 隐藏 Docsify 前端对 frontmatter 元数据的渲染（合并重复修复）（[0184635](https://github.com/kuliantnt/plurality_wiki/commit/018463576239e617794752e4a41b479f1697e3dc)，[07cd27e](https://github.com/kuliantnt/plurality_wiki/commit/07cd27ea2aa4d7e00e3761a475598637cdceb7d9)）
- 表格展示与响应式修复（PC 端显示、术语表布局与全局化）（代表性提交：[8f35457](https://github.com/kuliantnt/plurality_wiki/commit/8f35457606235fb347bc99e2ba97c130bb71dd0d)，[9c19d3d](https://github.com/kuliantnt/plurality_wiki/commit/9c19d3decf53f650139f944c5d961783f7d84c08)）
- 修正“最近更新”链接路径（合并重复修复）（[8ba3e1a](https://github.com/kuliantnt/plurality_wiki/commit/8ba3e1acb1bc9ffb77801f339214026410aa7f99)，[a80b8d0](https://github.com/kuliantnt/plurality_wiki/commit/a80b8d01d57be097bc93df87ec40b9af7889e554)）
- 移除不必要的 `_sidebar.md` 忽略配置（[d6e30ae](https://github.com/kuliantnt/plurality_wiki/commit/d6e30ae55aa9522c8f1dc454003aa5ce1a4c4546)）
- 标签列表格式化（焦虑/双相障碍）（[d7cd081](https://github.com/kuliantnt/plurality_wiki/commit/d7cd08171085c51f0135817841a43a55393b0ceb)）
- 更新贡献与开发约定（markdownlint 要求等）并同步校对报告生成时间（[cc3bd32](https://github.com/kuliantnt/plurality_wiki/commit/cc3bd32b4512adfa3c9acc4504009f5aa01b9693)）
- 补全部分诊断词条模板章节（[3a3ee06](https://github.com/kuliantnt/plurality_wiki/commit/3a3ee069405c635fb871a0786d83aa07f3090e56)）

### 📝 文档与索引（不影响语义）

- 重构部分诊断词条的章节结构（[fa22795](https://github.com/kuliantnt/plurality_wiki/commit/fa2279556fb71a8be24caaabe85be614faa1efa9)）
- 补充链接检查脚本的使用说明（[216ccfa](https://github.com/kuliantnt/plurality_wiki/commit/216ccfafaa7cf94c08c392df9d43d8eff1f450c1)）
- 统一若干文档的小幅格式修正（代表性提交：[871d44a](https://github.com/kuliantnt/plurality_wiki/commit/871d44af70fb509a96bd669d04c42df4294e3efc)，[295d04f](https://github.com/kuliantnt/plurality_wiki/commit/295d04fd52f5b33bd5a7b3a4c754d1b19d2ae8c9)）

### 🔧 重构（不改变内容含义）

- **（破坏性变更）**迁移为 **tags** 管理模式，统一词条目录结构（[d267385](https://github.com/kuliantnt/plurality_wiki/commit/d2673853f61b5a4a6eab17e325baa899c826c0e4)）

### 📦 杂务（脚本/CI/批处理）

- 删除旧版更新脚本 `update.cmd`（[e085f51](https://github.com/kuliantnt/plurality_wiki/commit/e085f51f0cba2d934cd310a5d221a45308b2e356)）

### 🎨 风格（空格/缩进/行尾等）

- 统一多处空行与段落间距，提升可读性（[34b979f](https://github.com/kuliantnt/plurality_wiki/commit/34b979ff29c77a15691ef511365fa6bf79e67040)）

— 由 Git 提交记录自动生成

## v1.3.4 (2025-10-03)

### ✨ 新增

- feat: 添加弦羽理论生态位分类法及相关系统条目（[a4a1724](https://github.com/kuliantnt/plurality_wiki/commit/a4a17243500114d96c05b31cb2f1894a7d98a712)）
- feat: 关于我们是最好朋友的事（[aa101e1](https://github.com/kuliantnt/plurality_wiki/commit/aa101e1ed4eaa34af2d19b7cb6ac36c61894489e)）
- feat: 添加远端分支清理脚本（[999cf69](https://github.com/kuliantnt/plurality_wiki/commit/999cf690c324a9b21a4be54f211ce57cf347b66a)）
- （合并）新增/更新若干占位或示例条目（[b865b47](https://github.com/kuliantnt/plurality_wiki/commit/b865b475cfde93eb60ef1f9d5acee83e7cdae9bb)，[d070503](https://github.com/kuliantnt/plurality_wiki/commit/d070503d57195e32ae2c82a53883ac9372153213)）

### 🐛 修复（链接/引用/格式）

- fix: 添加触发警示并更新系统定义，提升可读性（[0f292a2](https://github.com/kuliantnt/plurality_wiki/commit/0f292a2d56b95c55c35bf24d7382dbe8b35d34fd)）
- fix: 替换条目中的中文路径链接（[d0e9cb8](https://github.com/kuliantnt/plurality_wiki/commit/d0e9cb8787f76ee18f1839557893051a4f0e4ed4)）
- fix: 更新自动校对报告时间；移除无效检查项与标题格式问题（[ebdb19f](https://github.com/kuliantnt/plurality_wiki/commit/ebdb19f0afa1a11dd913225549c2ce4056f908d8)）
- fix: 更新术语表，补充缺失条目并修复格式（[0ceffc2](https://github.com/kuliantnt/plurality_wiki/commit/0ceffc2a83b59c4a5b59ea72fe583dba71da2d6c)）
- fix: 启用更新脚本以生成“最后更新时间”（[f2fc449](https://github.com/kuliantnt/plurality_wiki/commit/f2fc4490291b7d194803a5996b888fcb719d0114)）
- fix: 依据校对报告微调部分词条结构（[8fa7e77](https://github.com/kuliantnt/plurality_wiki/commit/8fa7e77231da264ea958989b01f2a288ecf12995)）
- fix: 更新页脚维护者信息，补充系统名称（[dcc184a](https://github.com/kuliantnt/plurality_wiki/commit/dcc184a9f15205147baf7fb36aea445d2ca985a4)）
- fix: 修正条目模板与更新日志的排版（[350382e](https://github.com/kuliantnt/plurality_wiki/commit/350382e7cdaa5efedf0024eb6d79521c8ed0cdaa)）
- fix: 调整 DID 共病术语（[4b43c4b](https://github.com/kuliantnt/plurality_wiki/commit/4b43c4b56da041de1523af7b72556adab03fb8ca)）

### 📝 文档与索引（不影响语义）

- 术语表与布局改造：区分桌面/移动展示并重构为移动友好（[81d3cf6](https://github.com/kuliantnt/plurality_wiki/commit/81d3cf69d7678a0c9842bd0b2060b0032d0d9a3a)，[578b068](https://github.com/kuliantnt/plurality_wiki/commit/578b0681ef9ac6e2fd70700c38f94614694866ab)）
- 文档结构与索引：更新 README 的仓库结构概览与文档位置/链接（[301047e](https://github.com/kuliantnt/plurality_wiki/commit/301047e0d2ee39cfe5d3f1885bf09bf4923a8ceb)，[9e9a502](https://github.com/kuliantnt/plurality_wiki/commit/9e9a502db310380b9ca69670454282612ec7e24e)）
- 贡献/运维文档：新增 GitHub 提交流程与管理员指南（[d4ffb8e](https://github.com/kuliantnt/plurality_wiki/commit/d4ffb8e109cfb526240bb6ece8c6d4d88e0988a8)，[eb58ef4](https://github.com/kuliantnt/plurality_wiki/commit/eb58ef455737cff072a33c9419a4ed99ab125aea)）
- 自动化与导出：同步自动化工具与 PDF 导出文档到 docs（[8790314](https://github.com/kuliantnt/plurality_wiki/commit/8790314176ca70f58ff5226faecde43a639c3a27)）
- AGENTS 规则：补充前端资产脚本注释与贡献约定（[fa85303](https://github.com/kuliantnt/plurality_wiki/commit/fa85303ddee6df569f93b86f233ccfcae8233642)，[c383990](https://github.com/kuliantnt/plurality_wiki/commit/c38399026fb8e256b8c319a3ac32e6fb074d9605)）
- CI 徽章与状态：替换为 shields.io 并修正状态链接（[bea3510](https://github.com/kuliantnt/plurality_wiki/commit/bea35103b1ecc502d3d3cb564a9f97c21ff9f88d)，[7709dd0](https://github.com/kuliantnt/plurality_wiki/commit/7709dd031ae81a9c8a94cc874ec2c8e9242dd322)）
- 术语表分类与常规小修：拆分类别、补充与微调（[6f12fb6](https://github.com/kuliantnt/plurality_wiki/commit/6f12fb62d77b74fb0a9db38d691e9574e682e1dc)，[b8304e3](https://github.com/kuliantnt/plurality_wiki/commit/b8304e35b6269e049e0268cd20cd62ca4da38ffc)）
- 语法与排版：统一 Markdown 与文档格式（[7033eea](https://github.com/kuliantnt/plurality_wiki/commit/7033eeac4b08469e8faa13f795827b4cab1ec87f)）
- 贡献指南与模板：补充条目规范与自检清单（[49d8375](https://github.com/kuliantnt/plurality_wiki/commit/49d8375beb86c5b1ea14804edaf38cafc1595e29)）

### 📦 杂务（脚本/CI/批处理）

- chore: 调整校对脚本目录（[cdae64f](https://github.com/kuliantnt/plurality_wiki/commit/cdae64f3e38b210c764c19b4de76818240b7eb2d)）

— 由 Git 提交记录自动生成

## v1.3.3 (2025-10-03)

### ✨ 新增

- 重构图帕词条结构并补充研究说明（[5f4f526](https://github.com/kuliantnt/plurality_wiki/commit/5f4f5261336202d8f3a4a0759b4854d35dec33a0)）
- 拆分解离词条并新增功能性与病理性内容（[1f66649](https://github.com/kuliantnt/plurality_wiki/commit/1f66649771c6c6cad29ec990e7a98b2ec0bef49f)）
- 新增谵妄词条并强化定向障碍关联（[02a5dda](https://github.com/kuliantnt/plurality_wiki/commit/02a5ddacc77157da63c4bd45699544e9262a9902)）
- 补充解离主题条目的相关链接（[a793724](https://github.com/kuliantnt/plurality_wiki/commit/a7937241f81256040e416f8b758aa9fbef7b5eb6)）
- 更新更新日志（[fdd952f](https://github.com/kuliantnt/plurality_wiki/commit/fdd952f8c54f169c5ac7218b3691ece0715e66d0)）

### 🐛 修复（链接/引用/格式）

- 完善移动端搜索结果后的侧边栏收起（[c00ac19](https://github.com/kuliantnt/plurality_wiki/commit/c00ac19c554578f31d102ce0466045cba932ece4)）
- 防止搜索框在移动端触发侧边栏收起（[81c01d0](https://github.com/kuliantnt/plurality_wiki/commit/81c01d0524b6f2dbac8788f2e1ce1945b9b3eab7)）

### 📝 文档与索引（不影响语义）

- 补充弦羽理论触发模型细节（[7a54653](https://github.com/kuliantnt/plurality_wiki/commit/7a546532747250efa645d1c02148f399c3390acb)）
- 补充触发并发风险提醒（[70bd9e6](https://github.com/kuliantnt/plurality_wiki/commit/70bd9e648c07d6639a3843278aa09ad4ac655bf3)）

### 📦 杂务（脚本/CI/批处理）

- 更新 last-updated 索引（[39001d1](https://github.com/kuliantnt/plurality_wiki/commit/39001d195db07b5f88ad63842dd02e9f53db322b)）

— 由 Git 提交记录自动生成

## v1.3.2 (2025-10-03)

### ✨ 新增

- 更新创伤和解离性身份障碍条目，整合定义、特征及实务建议（[15c663e](https://github.com/kuliantnt/plurality_wiki/commit/15c663e2a3df00d045047df35c64fa306f0eb9fe)）
- 更新 OSDD、DPDR、抑郁障碍及条目贡献指南，增加定义、特征及实务建议（[9438267](https://github.com/kuliantnt/plurality_wiki/commit/94382673a5cf9373e9fdae4409d8acf07129ea94)）
- 更新 DID 和闪回条目，补充定义、特征及实务建议（[55b8133](https://github.com/kuliantnt/plurality_wiki/commit/55b81335070bca5694124efcbaae9918f80fba37)）
- 新增 PTSD 条目（[fc3068e](https://github.com/kuliantnt/plurality_wiki/commit/fc3068e0c3737247b489562a24950c5a684fd36e)）
- 更新 OCD 条目（[f8e8c2c](https://github.com/kuliantnt/plurality_wiki/commit/f8e8c2c92f3d94b8896a5143cb6e7285bd7920e6)）
- 新增“交换”条目（[76af9f5](https://github.com/kuliantnt/plurality_wiki/commit/76af9f52e230d2b710d32f4672ba81c211ee7b9d)）
- 更新里空间和条目模板（[3ac7f75](https://github.com/kuliantnt/plurality_wiki/commit/3ac7f7586183134b7abcc15798736ca346137d26)）
- 新增“共前台”和“偏重”条目（[215c07e](https://github.com/kuliantnt/plurality_wiki/commit/215c07e5b1a5398cb10ab7e8bf7e511a459e7f15)）
- 新增“侵入性思维”条目（[bbdc85e](https://github.com/kuliantnt/plurality_wiki/commit/bbdc85e478b72f69c5ea8a2e3f9fbb75590bacaf)）
- 更新 ANP-EP 模型（[180e810](https://github.com/kuliantnt/plurality_wiki/commit/180e810831c12ad917490fe0d587044705ec2dc1)）
- 新增“超级破碎（Polyfragmented）”条目（[3be416c](https://github.com/kuliantnt/plurality_wiki/commit/3be416ccef567df69776fc0e034e211f48e892b2)）
- 更新冥想与接地条目（[ca49692](https://github.com/kuliantnt/plurality_wiki/commit/ca496924df32b04267a27f8971950250f66cc9b7)，[6bd286f](https://github.com/kuliantnt/plurality_wiki/commit/6bd286f4c746e8248ad68d0480e55a110933fb67)）
- 更新 T 语条目（[f4310e6](https://github.com/kuliantnt/plurality_wiki/commit/f4310e6229fbe1719c96853ba3352a04038880f0)，[d54730c](https://github.com/kuliantnt/plurality_wiki/commit/d54730c99da1b58bc00bf967c5166b679b0635c4)）
- 新增“头压”条目（[f8e4575](https://github.com/kuliantnt/plurality_wiki/commit/f8e4575a142b94f8ae4fbc0d4303a8ed2a3af9e8)）
- 更新投射、内投射、外投射条目（[f9dcd31](https://github.com/kuliantnt/plurality_wiki/commit/f9dcd3133cf113f7a469ec429830958eae0a3245)）
- 扩充核心板块速览内容（[38e74cc](https://github.com/kuliantnt/plurality_wiki/commit/38e74ccc5af53d72607d3a188e81e274746676b1)）

### 🐛 修复（链接/引用/格式）

- 更新“头压”条目并修复 md 文件链接问题（[3b980b5](https://github.com/kuliantnt/plurality_wiki/commit/3b980b5c6fa48eb4b7b758bb3b64172618b2e57e)）
- 重写 PDF 导出中的词条链接（[4c11d83](https://github.com/kuliantnt/plurality_wiki/commit/4c11d835e7ddfcea3d92f61b9062dafbf7d9d9ac)）
- 修正贡献指南 URL 错误（[df06f22](https://github.com/kuliantnt/plurality_wiki/commit/df06f221a10bd0d0e9b6a0a2133e663ed071381e)）
- 调整侧边栏标题与搜索栏顺序（[95dd0e8](https://github.com/kuliantnt/plurality_wiki/commit/95dd0e8411783ed9c6748bf2d3c99778b14f7b55)）
- 修正“最近更新”页面的词条标题显示（[d5b2aaf](https://github.com/kuliantnt/plurality_wiki/commit/d5b2aafde506c8b33ae3c6639bf13abd2c294694)）
- 更新“莉莉丝”术语（[d30531b](https://github.com/kuliantnt/plurality_wiki/commit/d30531bcf5a41afa2b7a29bc5a31f4380926de51)）

### 📦 杂务（脚本/CI/批处理）

- 强制更新 last-updated 索引（[2c78f0c](https://github.com/kuliantnt/plurality_wiki/commit/2c78f0ceab0f92726781935c6788216baf5857e6)）

— 由 Git 提交记录自动生成

## v1.3.1 (2025-10-02)

### ✨ 新增

- 首页展示最近更新入口（[8886c97](https://github.com/kuliantnt/plurality_wiki/commit/8886c9767ab5436969af8ab5bc1b4c9819944b7e)）
- 增加最近更新页面自动生成脚本（[fcccd0a](https://github.com/kuliantnt/plurality_wiki/commit/fcccd0affce8ed84459079c3903d93467f76d1ba)）
- 在 PDF 导出中渲染最后更新时间（[8b5475f](https://github.com/kuliantnt/plurality_wiki/commit/8b5475f0f93cb49441fd744b5fcbd636437f3aa1)）
- 显示词条最后更新时间（[cfe1729](https://github.com/kuliantnt/plurality_wiki/commit/cfe172935a2b7efe54eaad0efb15708a7b45c498)）

### 🐛 修复（链接/引用/格式）

- 修复 changelog.md 输出问题（[8b6d0db](https://github.com/kuliantnt/plurality_wiki/commit/8b6d0db719a8b49966b40185f646ef82dd454711)）
- 调整站点标题后缀显示（[8431f3e](https://github.com/kuliantnt/plurality_wiki/commit/8431f3e800c5b0373f1f7157058e74ae83c3647a)）

### 📝 文档与索引（不影响语义）

- 修改 changelog 文档（[1c36386](https://github.com/kuliantnt/plurality_wiki/commit/1c363866d4c4376b500ba8a74440d44210b643eb)）
- 更新 README 中工具说明（[e231636](https://github.com/kuliantnt/plurality_wiki/commit/e231636bf955f18caef92521e60f40bb030bb529)）

### 🔧 重构（不改变内容含义）

- 移除 Docsify 最后更新功能（[441ec22](https://github.com/kuliantnt/plurality_wiki/commit/441ec22aee1f7ccdbf760c68475a2968f1711f3a)）

### 🎨 风格（空格/缩进/行尾等）

- 调整 agents 配置与站点 SVG 图标（[9cb4db5](https://github.com/kuliantnt/plurality_wiki/commit/9cb4db5b5deec0e8516ebf0ea85c1009561aaf28)，[e231636](https://github.com/kuliantnt/plurality_wiki/commit/e231636bf955f18caef92521e60f40bb030bb529)）

— 由 Git 提交记录自动生成

## v1.3.0 (2025-10-02)

### ✨ 新增

- 支持输出最新标签到 HEAD 的简化日志（[289f802](https://github.com/kuliantnt/plurality_wiki/commit/289f802b7e0951c888cc2d29e8f014822712e96b)）
- 首页快速入口卡片化改版（[51600ed](https://github.com/kuliantnt/plurality_wiki/commit/51600edd830ca05dbe91837d266bcc48a7590d99)）
- 优化中英文排版间距（[18db44a](https://github.com/kuliantnt/plurality_wiki/commit/18db44a2c21884131c30a7c002fd589b1d568469)）
- 重构主页布局与样式（[3d09e03](https://github.com/kuliantnt/plurality_wiki/commit/3d09e038c81fb0af4974e9dfaf3712507725a8af)）
- mainpage 编辑改进（[64ad6bc](https://github.com/kuliantnt/plurality_wiki/commit/64ad6bce90fa0ce92cc53a54c3709726326e6857)）

### 🐛 修复（链接/引用/格式）

- 修正 404 页面对 `.md` 直链的跳转（[744dc37](https://github.com/kuliantnt/plurality_wiki/commit/744dc37e5e325d72a3099a1bf66056bccf0881fc)）
- 修复 mainpage 显示问题（[98e8a41](https://github.com/kuliantnt/plurality_wiki/commit/98e8a41739826ab88232dcbc6736aff56bf79ca6)）
- 修复主页主按钮在不同主题下的可见性（[7bdecf1](https://github.com/kuliantnt/plurality_wiki/commit/7bdecf1d406bfeb26b52861413be8d4e24dc9b96)）
- 优化主页按钮与快速入口布局（[0adca3c](https://github.com/kuliantnt/plurality_wiki/commit/0adca3c6a9ed732e852066988f654a40fd729cac)）
- 调整主页按钮与快速入口文案（[0583549](https://github.com/kuliantnt/plurality_wiki/commit/05835490c5fd4d64fa9b1b964d6e4655e9f03a00)）
- 调整暗色模式快速入口下拉样式（[b489d86](https://github.com/kuliantnt/plurality_wiki/commit/b489d869493d5323dd8289797324f6be44356b41)）
- 修复链接与文件重命名引用问题（[8ccea60](https://github.com/kuliantnt/plurality_wiki/commit/8ccea609de7fe5d3c51bfed97d2ba645dbb51fa0)）
- 修复 GitHub Active 检查及 Lint 错误（[d443fb9](https://github.com/kuliantnt/plurality_wiki/commit/d443fb9930238fed5336351de13b89e803270653)，[ef4efcb](https://github.com/kuliantnt/plurality_wiki/commit/ef4efcb9a49c65166effe5b1f1689d9018131ee8)，[66433d2](https://github.com/kuliantnt/plurality_wiki/commit/66433d2d6c2b3c5a498abb2b2e2e8f2cda8684ec)）
- 主页快速入口显示 bug 修复（[2144eab](https://github.com/kuliantnt/plurality_wiki/commit/2144eabdc9882912f1123533e5e559ceba352b40)，[7ae6f63](https://github.com/kuliantnt/plurality_wiki/commit/7ae6f63859dcc69aaaaac8a84f3f910df50e9e03)）
- bugfix: Main_Page 修复（[7acb79d](https://github.com/kuliantnt/plurality_wiki/commit/7acb79d2f5b67af0462b39f31c50970ebe961e72)）

### 📝 文档与索引（不影响语义）

- 在 README 添加自动化维护章节（[25d9484](https://github.com/kuliantnt/plurality_wiki/commit/25d94849a0a393783a9b38cd872080b48bc355d6)）
- 修改首页描述（[03ec264](https://github.com/kuliantnt/plurality_wiki/commit/03ec264c1cdd45eea4f098c07abd20d588270947)）
- 更新 README、AGENTS 与 CONTRIBUTING 说明（[b81dfaa](https://github.com/kuliantnt/plurality_wiki/commit/b81dfaa3b645d974b7197fd53633e6992eeb672d)，[46e7a38](https://github.com/kuliantnt/plurality_wiki/commit/46e7a38ceb326afedf24a9ac60943e1b42c6a781)，[440bc42](https://github.com/kuliantnt/plurality_wiki/commit/440bc4207600a4ab2f64af4f873162628e413ffc)）

### 🔧 重构（不改变内容含义）

- 将主页迁移为 HTML 页面（[57a28a7](https://github.com/kuliantnt/plurality_wiki/commit/57a28a7d7c8fda4701432cb114550bec941dc7d2)）

### 🎨 风格（空格/缩进/行尾等）

- 修改图标样式（[0352260](https://github.com/kuliantnt/plurality_wiki/commit/03522608cd8a6c4ad40f94ac48990d3aab762177)）
- 重设计主页面页脚（[774472d](https://github.com/kuliantnt/plurality_wiki/commit/774472d7a2ad9bdbaaa58f2180f18bab6ce9d927)）

## v1.2.4 (2025-10-02)

### ✨ 新增

- 优化 PDF 封面并提升暗黑模式对比度（[3b9b997](https://github.com/kuliantnt/plurality_wiki/commit/3b9b9978a36cef7a2fcdda6d55b6db9831842da7)）

### 🐛 修复（链接/引用/格式）

- 修复 README（[17e10f8](https://github.com/kuliantnt/plurality_wiki/commit/17e10f8c71902daac9afc8d3b73873c96d09e99f)）
- 修复链接问题（[b0d378c](https://github.com/kuliantnt/plurality_wiki/commit/b0d378c5a5e52172b7a0ad6f1b933b8b2462b4fa)）
- 本地化最后更新时间插件（[bff6afe](https://github.com/kuliantnt/plurality_wiki/commit/bff6afe9d97ac6fc011a949e4da841006eac9111)）
- 修复 Docsify 最后更新时间占位符（[7d86299](https://github.com/kuliantnt/plurality_wiki/commit/7d8629913b1c819ec084c4f7cb5ffc2d37fec715)）

### 📦 杂务（脚本/CI/批处理）

- 添加 changlog（[255fbff](https://github.com/kuliantnt/plurality_wiki/commit/255fbffde42896029c2e846349f391685ce1d475)）
- 新增 GitHub 社区配置（[44d6392](https://github.com/kuliantnt/plurality_wiki/commit/44d63921b2d553f219002a30468fd31ca2057720)）
- 修改 agents（[35a9f2a](https://github.com/kuliantnt/plurality_wiki/commit/35a9f2a8f25c33519da52178c53c0f3a10557e30)）

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
- 调整多重意识体基础词条路径并配置映射。
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
