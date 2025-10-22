---
title: 学术引用规范
description: 定义 MPS Wiki 词条引用标准,涵盖证据分级、引用格式、来源核查流程,确保所有信息可追溯且经得起验证。
---

# 学术引用规范

为确保词条 **严谨、无歧义、可追溯** ，所有断言必须配备引用。

---

## 1. 证据与来源分级

### 1.1 一级来源（必选优先）

**权威性最高，诊断相关内容必须引用** ：

- **ICD-11 官方浏览器**
    - ICD-11 Browser（MMS 版本）
    - Reference Guide
    - Clinical Descriptions and Diagnostic Requirements（CDDR）

- **DSM-5-TR**
    - 原文与 APA 官方资料
    - Fact Sheets
    - 官方页面

### 1.2 二级来源（可补充）

**用于补充背景与综述** ：

- 权威综述（StatPearls, UpToDate）
- 教科书（需注明版本与出版年份）
- 权威期刊论文（需同行评审）

### 1.3 三级来源（仅限背景）

**仅用于提供背景信息，不可作为主要依据** ：

- 社群 Wiki
- 媒体报道
- 博客、论坛

---

## 2. 引用规则

!!! warning "强制要求"
    涉及诊断、病理学、流行病学断言， **必须引用至少 1 个一级来源** 。

### 2.1 就近引用

- 每个可核查断言 **就近给出引用**
- 可使用脚注或段尾引用
- 避免整段文字只在末尾给一个引用

### 2.2 引用内容要求

每个引用必须包含：

1. **来源名称**
2. **版本/日期**
3. **访问日期** （在线资源）
4. **页码/章节** （书籍/PDF）

---

## 3. 引用格式

### 3.1 基本格式

```markdown
> [原文引用]

**来源**：[来源名称]（[版本]，访问日期：YYYY-MM-DD）
```

### 3.2 ICD-11 引用示例

```markdown
> "The presence of two or more distinct personality states..."
> （存在两个或以上身份状态...）

**来源**：WHO ICD-11 Browser, 6B64 解离性身份障碍（MMS 2025-01，访问日期：2025-10-03）
```

### 3.3 DSM-5-TR 引用示例

```markdown
> "Disruption of identity characterized by two or more distinct personality states..."
> （以两个或以上不同的人格状态为特征的身份中断...）

**来源**：APA DSM-5-TR, 解离性身份障碍 300.14 (F44.81)（第 5 版，2022 年文本修订）
```

### 3.4 学术文献引用示例

```markdown
研究表明，DID 患者的大脑活动模式在不同人格状态下存在显著差异[^1]。

[^1]: Reinders, A. A. T. S., et al. (2016). "Psychobiological characteristics of dissociative identity disorder." *Psychological Medicine*, 46(1), 53-70.
```

---

## 4. 翻译要求

### 4.1 中文翻译

- 如为中文翻译，必须同时给出 **英文原文**
- 原文长度 **≤25 词**
- 超过 25 词的需摘录关键部分

### 4.2 译者标注

翻译内容需标明译者或校对：

```markdown
> "Two or more distinct personality states..."
> （两个或以上不同的人格状态...）

**来源**：WHO ICD-11, 6B64（MMS 2025-01）
**译者**：XXX（校对：XXX）
```

---

## 5. 数据与图表

### 5.1 数据引用

引用统计数据时，必须标明：

- **统计口径**
- **时间范围**
- **样本来源**
- **数据来源**

**示例** ：

```markdown
根据 2020 年美国流行病学调查，DID 的终生患病率约为 1.5%[^1]。

[^1]: Johnson, J. G., et al. (2020). "Prevalence of dissociative disorders in community samples." *Journal of Psychiatric Research*, 45(8), 1037-1045.
样本：美国成年人群（N=2,426），时间：2018-2019
```

### 5.2 图表引用

- 图片、图表必须注明 **来源与许可**
- 原创图表需标明"原创"
- 改编图表需注明"改编自..."

**示例** ：

```markdown
![解离谱系示意图](../assets/figures/dissociation-spectrum.svg)

**来源**：改编自 Van der Hart, O., et al. (2006). *The Haunted Self*, p. 45
**许可**：CC BY-SA 4.0
```

---

## 6. 争议性内容

### 6.1 并列不同观点

对有争议的研究，需并列不同观点：

```markdown

## 关于 DID 的成因

### 观点一：创伤理论

创伤理论认为 DID 源于童年严重创伤[^1]。

[^1]: Putnam, F. W. (1997). *Dissociation in Children and Adolescents.*

### 观点二：社会认知模型

部分学者认为 DID 可能受到社会文化与治疗过程的影响[^2]。

[^2]: Spanos, N. P. (1994). "Multiple identity enactments and multiple personality disorder."
```

### 6.2 标注证据等级

```markdown
!!! info "证据等级"

    - **强证据**：多项 RCT 研究支持
    - **中等证据**：部分观察性研究支持
    - **弱证据**：个案报告或理论推测

```

---

## 7. 常用权威入口

### 7.1 一级来源

| 来源 | 链接 | 说明 |
|------|------|------|
| WHO ICD-11 Browser | [https://icd.who.int/browse11](https://icd.who.int/browse11) | 使用 MMS 2025-01 版本 |
| WHO CDDR | PDF 下载 | 2024 年版本 |
| APA DSM-5-TR | [https://www.psychiatry.org/](https://www.psychiatry.org/) | 官方 Fact Sheets |

### 7.2 二级来源

| 来源 | 链接 | 说明 |
|------|------|------|
| StatPearls | [https://www.ncbi.nlm.nih.gov/books/NBK](https://www.ncbi.nlm.nih.gov/books/NBK) | 免费医学教科书 |
| UpToDate | [https://www.uptodate.com/](https://www.uptodate.com/) | 临床决策支持 |

---

## 8. 检查清单

提交前请确认：

- [ ] 所有断言均有就近引用
- [ ] 引用包含来源名称、版本、访问日期
- [ ] 病理学内容至少引用 1 个一级来源
- [ ] 翻译内容包含原文（≤25 词）
- [ ] 译者/校对已标注
- [ ] 图片/数据版权与许可明确
- [ ] 争议性内容并列不同观点

---

## 相关文档

- [编写规范](writing-guidelines.md)
- [诊断临床规范](clinical-guidelines.md)
- [技术约定](technical-conventions.md)
- [PR 流程](pr-workflow.md)
