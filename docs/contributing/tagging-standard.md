---
title: 标签规范 Tagging Standard v2.0
description: 详细阐述 MPS Wiki 标签体系,含分面前缀规则、命名格式、分配流程与自动校验要点,指导贡献者维护一致的标签数据。
---

# MPS Wiki 标签规范（Tagging Standard v2.0）

> 统一的标签体系，适用于所有词条 Frontmatter 的 `tags:` 字段。面向贡献者与自动化代理（Agents/Scripts）。

---

## ✅ 1. 通用规则（General Rules）

!!! info "标签基本要求"
    - 使用“分面前缀 + 名称”格式：`prefix:名称`
    - 中文为主，英文缩写放在全角括号中：例如 `dx:解离性身份障碍（DID）`
    - 每个词条最多 5 个标签（≤ 5）
    - 标签必须来自下方分面体系（见 2. 分面体系）
    - 同义与历史标签通过 `data/tags_alias.yaml` 统一映射，不直接使用别名
    - 提交前必须通过自动校验（tag validator）

!!! danger "禁止的标签形式"
    - 没有前缀的标签（如 `DID`, `CBT`）
    - 页面标题型标签（如 `Tulpa 完全创造指南·基础篇`）
    - 模糊集合词（如 `核心概念`, `导览`）
    - 含空格、句号或英文半角括号 `()` 的标签

---

## 🧭 2. 分面体系（Faceted Prefix System）

| 前缀 | 含义 | 示例 |
|------|------|------|
| `dx:` | 诊断与分类（Diagnostic Category） | `dx:解离性身份障碍（DID）`, `dx:PTSD`, `dx:人格障碍` |
| `sx:` | 症状与现象（Symptoms） | `sx:闪回`, `sx:时间丢失`, `sx:去现实化` |
| `tx:` | 治疗与干预（Treatment） | `tx:CBT`, `tx:EMDR`, `tx:IFS`, `tx:阶段性治疗原则` |
| `scale:` | 量表与工具（Scales & Measures） | `scale:DES-II`, `scale:MID-60` |
| `theory:` | 理论与模型（Theoretical Model） | `theory:ANP-EP 模型`, `theory:结构性解离理论` |
| `ops:` | 系统运作机制（System Operation） | `ops:切换`, `ops:混合`, `ops:权限`, `ops:共前台` |
| `role:` | 系统角色/身份（System Roles） | `role:宿主`, `role:保护者`, `role:迫害者`, `role:创造者` |
| `community:` | 社群与文化身份（Community & Plural Terms） | `community:Tulpa`, `community:Median`, `community:Alterhuman` |
| `guide:` | 导览与自助资源（Guides & Resources） | `guide:危机干预`, `guide:自我照护工具箱` |
| `history:` | 历史术语（Historical Term） | `history:癔症`, `history:Transvestism` |
| `misuse:` | 误用与俗称（Misused Term） | `misuse:人格分裂` |
| `bio:` | 生物/脑刺激治疗（Biological Treatments） | `bio:MECT`, `bio:CES` |
| `sleep:` | 睡眠障碍（Sleep Disorders） | `sleep:失眠障碍`, `sleep:昼夜节律紊乱` |
| `dev:` | 神经发育与学习障碍（Neurodevelopmental） | `dev:孤独症谱系`, `dev:特定学习障碍` |
| `culture:` | 文化与表现（Cultural Depictions） | `culture:〈分裂〉形象分析`, `culture:〈西比尔〉原型` |
| `meta:` | 索引与站务（Meta/Index） | `meta:术语表`, `meta:导览` |

---

## 🧱 3. 命名格式（Naming Format）

| 规则 | 示例 | 反例 |
|------|------|------|
| 中文 + 英文括注 | `dx:解离性身份障碍（DID）` | `dx:解离性身份障碍（DID）` |
| 保留必要缩写 | `scale:DES-II` | `scale:DES` |
| 不含空格 | `role:宿主` | `role: 宿主` |
| 全角中文括号 | `（DID）` | `(DID)` |
| 前缀全小写 | `theory:` | `Theory:` |
| 无重复内容 | `dx:焦虑障碍` | `dx:焦虑障碍（Anxiety Disorder）` |

---

## 🧩 4. 标签分配逻辑（Assignment Logic）

| 类型 | 必备分面 | 示例 |
|------|----------|------|
| 临床诊断词条 | `dx:` + `theory:` + 可选 `tx:` | `dx:解离性身份障碍（DID）`, `theory:结构性解离理论`, `tx:阶段性治疗原则` |
| 系统机制词条 | `ops:` + 可选 `role:` | `ops:切换`, `role:前台` |
| 角色词条 | `role:` + `ops:` 或 `theory:` | `role:宿主`, `ops:执行控制` |
| 疗法与干预 | `tx:` + `theory:` | `tx:EMDR`, `theory:创伤记忆处理` |
| 社群与文化类 | `community:` + 可选 `culture:` | `community:Tulpa`, `culture:虚拟偶像现象` |
| 历史/误用类 | `history:` 或 `misuse:` | `history:癔症`, `misuse:人格分裂` |
| 工具与量表 | `scale:` + `dx:` | `scale:MID-60`, `dx:解离性身份障碍（DID）` |

---

## ⚙️ 5. 自动化校验要求（For CI / Agents）

!!! warning "提交/PR/agent 生成均需满足"
    - 至少 1 个标签包含合法前缀
    - 标签总数 ≤ 5
    - 不存在未定义前缀
    - 不使用别名（alias 必须由 `data/tags_alias.yaml` 映射到规范名）
    - 标签的“名称部分”不得与页面 `title` 完全相同
    - 每个标签必须匹配正则：`^[a-z]+:[^\s()]+$`（禁止空格与英文半角括号）

### 本地校验命令

```bash
# 检查整个词条目录（推荐）
python3 tools/check_tags.py docs/entries/

# 检查单个文件
python3 tools/check_tags.py docs/entries/DID.md

# 显示详细信息
python3 tools/check_tags.py --verbose docs/entries/
```

---

## 📎 附：别名映射（tags_alias.yaml）

- 路径：`data/tags_alias.yaml`
- 结构：`旧名/同义 -> 规范名`
- 示例：

```yaml
# data/tags_alias.yaml
DID: dx:解离性身份障碍（DID）
Tulpa: community:Tulpa
人格分裂: misuse:人格分裂
MPD: history:MPD
焦虑: dx:焦虑障碍
```

---

## 🔗 相关文档

- `docs/TEMPLATE_ENTRY.md` — 词条 Frontmatter 模板与说明
- `docs/dev/Tools-Index.md` — 工具与脚本总览（含 Tag Validator）
- `AGENTS.md` — 代理/脚本必须遵循的强制规范
