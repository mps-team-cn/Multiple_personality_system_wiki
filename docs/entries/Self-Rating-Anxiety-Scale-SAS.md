---
title: 焦虑自评量表（Self-Rating Anxiety Scale, SAS）
tags:

    - scale:SAS
    - scale:评估量表
    - guide:诊断与临床

topic: 诊断与临床
synonyms:

    - 焦虑自评量表
    - SAS
    - Zung焦虑量表
    - Self-Rating Anxiety Scale

description: 焦虑自评量表（SAS）是由Zung于1971年编制的自评量表，包含20个项目，采用1-4分四级评分系统，用于评估焦虑症状的严重程度及其在治疗中的变化，适合焦虑症状的初步筛查与治疗监测。
updated: 2025-10-29
search:
  boost: 1.5
hide:

    - toc

comments: true
---

# 焦虑自评量表（Self-Rating Anxiety Scale, SAS）

!!! danger "重要声明"
    本量表仅用于教育与自我筛查，**不构成临床诊断**。若分数较高且伴随明显焦虑症状，请及时寻求精神科或临床心理专业评估。本量表不能替代专业的临床诊断。

!!! warning "危机求助资源"
    **若您正在经历严重焦虑、惊恐发作或其他急性心理危机，请立即寻求帮助：**

    - **全国24小时心理援助热线**：400-161-9995 / 010-82951332
    - **北京心理危机研究与干预中心**：010-82951332
    - **上海心理援助热线**：021-962525 / 021-12320-5
    - **广州心理危机干预中心**：020-81899120
    - **深圳心理危机干预热线**：0755-25629459
    - **紧急情况请拨打急救电话 120 或直接前往最近的医院急诊科**

    您的健康很重要，专业帮助随时可得。

## 概述

**焦虑自评量表（SAS）** 由华裔心理学家 William W. K. Zung 于 1971 年编制，是目前临床上广泛使用的焦虑症状评估工具之一。量表包含 20 个项目，评估个体在过去一周内的焦虑症状体验，涵盖心理焦虑和躯体焦虑两大维度。

量表采用四级评分系统（1-4分），通过粗分和标准分（粗分×1.25）来评估焦虑程度，适用于焦虑症状的初步筛查、治疗效果监测和症状变化追踪。

## 评分说明

!!! tip "使用说明"

    - 每题采用 **1-4 分** 四级评分：
        - **1 = 没有或很少时间**
        - **2 = 小部分时间**
        - **3 = 相当多时间**
        - **4 = 绝大部分或全部时间**
    - 请根据 **过去一周（包括今天）** 的实际体验作答
    - 建议按直觉作答，尽量不要反复修改
    - 完成所有题目后，系统将自动计算粗分和标准分

## 在线评估

<!-- 样式与脚本由 mkdocs.yml 的 extra_css / extra_javascript 注入 -->

<div id="sas-app" class="sas-app">

<div class="sas-meta">
  <div class="sas-hint">评分范围 1–4（1=没有或很少，4=绝大部分或全部时间）· SAS 标准</div>
  <div class="sas-actions">
    <button id="sas-reset" class="md-button">重置</button>
  </div>
</div>

<div class="sas-divider"></div>

<!-- 题目区域 -->
<table class="sas-table">
  <caption>SAS 题目与评分</caption>
  <colgroup>
    <col style="width:3rem">
    <col>
    <col style="width:auto; min-width:20rem">
  </colgroup>
  <thead>
    <tr><th scope="col">#</th><th scope="col">症状描述（过去一周的体验）</th><th scope="col">评分（1-4）</th></tr>
  </thead>
  <tbody>
    <tr class="sas-item"><td class="no">1</td><td>
      我觉得比平常容易紧张和着急
    </td><td>
      <div class="sas-ctrl">
        <select id="item1">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item1" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">2</td><td>
      我无缘无故地感到害怕
    </td><td>
      <div class="sas-ctrl">
        <select id="item2">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item2" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">3</td><td>
      我容易心里烦乱或觉得惊恐
    </td><td>
      <div class="sas-ctrl">
        <select id="item3">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item3" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">4</td><td>
      我觉得我可能将要发疯
    </td><td>
      <div class="sas-ctrl">
        <select id="item4">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item4" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">5</td><td>
      我觉得一切都很好，也不会发生什么不幸 *
    </td><td>
      <div class="sas-ctrl">
        <select id="item5">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item5" class="sas-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">6</td><td>
      我手脚发抖打颤
    </td><td>
      <div class="sas-ctrl">
        <select id="item6">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item6" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">7</td><td>
      我因为头痛、颈痛和背痛而苦恼
    </td><td>
      <div class="sas-ctrl">
        <select id="item7">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item7" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">8</td><td>
      我感觉容易衰弱和疲乏
    </td><td>
      <div class="sas-ctrl">
        <select id="item8">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item8" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">9</td><td>
      我觉得心平气和，并且容易安静坐着 *
    </td><td>
      <div class="sas-ctrl">
        <select id="item9">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item9" class="sas-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">10</td><td>
      我觉得心跳得很快
    </td><td>
      <div class="sas-ctrl">
        <select id="item10">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item10" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">11</td><td>
      我因为一阵阵头晕而苦恼
    </td><td>
      <div class="sas-ctrl">
        <select id="item11">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item11" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">12</td><td>
      我有晕倒发作，或觉得要晕倒似的
    </td><td>
      <div class="sas-ctrl">
        <select id="item12">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item12" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">13</td><td>
      我吸气呼气都感到很容易 *
    </td><td>
      <div class="sas-ctrl">
        <select id="item13">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item13" class="sas-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">14</td><td>
      我手脚麻木和刺痛
    </td><td>
      <div class="sas-ctrl">
        <select id="item14">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item14" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">15</td><td>
      我因为胃痛和消化不良而苦恼
    </td><td>
      <div class="sas-ctrl">
        <select id="item15">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item15" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">16</td><td>
      我常常要小便
    </td><td>
      <div class="sas-ctrl">
        <select id="item16">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item16" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">17</td><td>
      我的手常常是干燥温暖的 *
    </td><td>
      <div class="sas-ctrl">
        <select id="item17">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item17" class="sas-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">18</td><td>
      我脸红发热
    </td><td>
      <div class="sas-ctrl">
        <select id="item18">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item18" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">19</td><td>
      我容易入睡并且睡得很好 *
    </td><td>
      <div class="sas-ctrl">
        <select id="item19">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item19" class="sas-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>

    <tr class="sas-item"><td class="no">20</td><td>
      我做噩梦
    </td><td>
      <div class="sas-ctrl">
        <select id="item20">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item20" class="sas-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>
  </tbody>
</table>

<div class="sas-note" style="margin-top:.5rem;padding:.5rem .8rem;background:color-mix(in srgb,#9c27b0 8%,transparent);border-left:3px solid #9c27b0;border-radius:.4rem;">
  <strong>* 反向计分题目：</strong>题目 5、9、13、17、19 为反向计分题（选择"没有或很少时间"得4分，"绝大部分或全部时间"得1分），系统会自动处理反向计分。
</div>

<div class="sas-divider"></div>

<!-- 结果区域 -->
<div class="sas-results" id="sas-results">
  <div class="sas-section-title">评估结果</div>

  <!-- 主要指标 -->
  <div class="sas-score-card">
    <div>
      <div class="sas-score-label">粗分（20题原始分相加）</div>
      <div class="sas-hint">范围：20-80分</div>
    </div>
    <div class="sas-score-value" id="sas-raw-score">20</div>
  </div>

  <div class="sas-score-card">
    <div>
      <div class="sas-score-label">标准分（粗分 × 1.25）</div>
      <div class="sas-hint">范围：25-100分</div>
    </div>
    <div class="sas-score-value" id="sas-standard-score">25</div>
  </div>

  <!-- 进度条 -->
  <div>
    <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:.4rem;">
      <strong>焦虑程度</strong>
      <span style="font-size:1.1rem; font-weight:700;" id="sas-anxiety">正常</span>
    </div>
    <div class="sas-progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
      <div class="bar" id="sas-progress-bar" style="width:0%"></div>
    </div>
    <div class="sas-legend">
      <span>正常（&lt;50）</span>
      <span>重度焦虑（≥70）</span>
    </div>
  </div>

  <div class="sas-divider"></div>

  <!-- 子量表分析 -->
  <div class="sas-section-title">子量表分析</div>

  <div class="sas-subscale-grid">
    <div class="sas-subscale-card">
      <div class="sas-subscale-title">心理焦虑</div>
      <div class="sas-subscale-score">
        <span>分数</span>
        <span class="sas-subscale-value" id="sas-mental-score">8/32</span>
      </div>
      <div class="sas-subscale-bar">
        <div class="fill" id="sas-mental-bar" style="width:0%"></div>
      </div>
      <div class="sas-hint">心理紧张、担忧、恐惧等症状</div>
    </div>

    <div class="sas-subscale-card">
      <div class="sas-subscale-title">躯体焦虑</div>
      <div class="sas-subscale-score">
        <span>分数</span>
        <span class="sas-subscale-value" id="sas-physical-score">6/24</span>
      </div>
      <div class="sas-subscale-bar">
        <div class="fill" id="sas-physical-bar" style="width:0%"></div>
      </div>
      <div class="sas-hint">心悸、头晕、躯体不适等症状</div>
    </div>

    <div class="sas-subscale-card">
      <div class="sas-subscale-title">精神运动性</div>
      <div class="sas-subscale-score">
        <span>分数</span>
        <span class="sas-subscale-value" id="sas-motor-score">5/20</span>
      </div>
      <div class="sas-subscale-bar">
        <div class="fill" id="sas-motor-bar" style="width:0%"></div>
      </div>
      <div class="sas-hint">坐立不安、静息困难等症状</div>
    </div>
  </div>

  <div class="sas-divider"></div>

  <!-- 完成进度 -->
  <div class="sas-score-card">
    <div class="sas-score-label">完成进度</div>
    <div class="sas-score-value" id="sas-completion">20/20 (100%)</div>
  </div>

  <div class="sas-divider"></div>

  <div class="sas-note">
    <strong>中国常模参考区间：</strong>
  </div>
  <ul class="sas-note">
    <li><strong>标准分 &lt; 50</strong>：正常范围</li>
    <li><strong>标准分 50-59</strong>：轻度焦虑</li>
    <li><strong>标准分 60-69</strong>：中度焦虑</li>
    <li><strong>标准分 ≥ 70</strong>：重度焦虑</li>
  </ul>

  <!-- 安全提示 -->
  <div id="sas-safety-alert" class="sas-note" style="display:none;margin-top:.8rem;padding:.6rem;background:color-mix(in srgb,#f56c6c 8%,transparent);border-left:3px solid #f56c6c;border-radius:.4rem;">
    <strong>🆘 建议寻求专业帮助：</strong>您的评分提示可能存在中度或重度焦虑症状。建议及时咨询精神科医生或心理健康专业人员进行进一步评估和治疗。
  </div>

  <div class="sas-divider"></div>

  <div class="sas-note">
    <strong>重要提示：</strong>
  </div>
  <ul class="sas-note">
    <li>本量表仅作为初步筛查工具，不能替代专业临床诊断</li>
    <li>SAS 是症状学量表，高分提示焦虑症状，但不能直接诊断焦虑障碍</li>
    <li>若评分较高或症状显著影响生活，建议寻求精神科或临床心理专业评估</li>
    <li>量表可用于治疗过程中的症状监测，追踪治疗效果</li>
    <li>本在线版为教育用途，临床使用请采用标准化纸笔版或专业软件</li>
  </ul>
</div>

</div>

## 量表信息

### 开发与信效度

- **原作者**：Zung, W. W. K. (1971)
- **题目数量**：20 题
- **评分系统**：1-4 分四级评分
- **反向计分题**：5 题（题目 5、9、13、17、19）
- **内部一致性**：Cronbach's α 约 0.82-0.92
- **重测信度**：0.75-0.85（一周间隔）
- **中国常模**：已建立中国常模，分界值为标准分 50 分

### 量表结构

SAS 包含 20 个项目，可分为三个维度：

1. **心理焦虑**（8 题）：题目 1, 3, 7, 8, 15, 16, 18, 20
    - 评估心理紧张、担忧、恐惧等症状

2. **躯体焦虑**（6 题）：题目 2, 4, 6, 10, 12, 14
    - 评估心悸、头晕、发抖、晕厥等躯体症状

3. **精神运动性焦虑**（6 题）：题目 5, 9, 11, 13, 17, 19（含反向题）
    - 评估坐立不安、静息困难等症状

### 计分方法

1. **正向计分题**（15 题）：
    - 1 = 没有或很少时间
    - 2 = 小部分时间
    - 3 = 相当多时间
    - 4 = 绝大部分或全部时间

2. **反向计分题**（5 题：5、9、13、17、19）：
    - 1 = 绝大部分或全部时间（记 4 分）
    - 2 = 相当多时间（记 3 分）
    - 3 = 小部分时间（记 2 分）
    - 4 = 没有或很少时间（记 1 分）

3. **计算方法**：
    - **粗分**：20 个项目得分之和（范围 20-80）
    - **标准分**：粗分 × 1.25，四舍五入取整（范围 25-100）

### 结果解释

根据中国常模（吴文源等，1990）：

- **标准分 < 50**：正常范围
- **标准分 50-59**：轻度焦虑
- **标准分 60-69**：中度焦虑
- **标准分 ≥ 70**：重度焦虑

### 临床应用

SAS 主要用于：

1. **焦虑症状筛查**：识别可能存在焦虑症状的个体
2. **症状严重度评估**：评估焦虑症状的严重程度
3. **治疗效果监测**：评估治疗过程中焦虑症状的变化
4. **流行病学调查**：大规模焦虑症状调查

### 适用人群

- 成年人（18 岁及以上）
- 具有焦虑症状或疑似焦虑障碍的个体
- 需要治疗监测的焦虑症患者

### 使用注意事项

1. **不能替代诊断**：SAS 是筛查工具，不能单独用于诊断焦虑障碍
2. **需专业解释**：高分需结合临床访谈和其他评估工具综合判断
3. **文化差异**：不同地区、文化背景的常模可能有所差异
4. **反向计分**：使用时需注意反向计分题的处理

## 参考文献

1. Zung, W. W. K. (1971). A rating instrument for anxiety disorders. *Psychosomatics*, 12(6), 371-379.

2. 吴文源, 王焕林 (1990). 焦虑自评量表（SAS）的理论基础与研究应用. *中华神经科杂志*, 23(6), 348-349.

3. 汪向东, 王希林, 马弘 (1999). 心理卫生评定量表手册（增订版）. 中国心理卫生杂志社.

4. Olatunji, B. O., Deacon, B. J., Abramowitz, J. S., & Tolin, D. F. (2006). Dimensionality of somatic complaints: Factor structure and psychometric properties of the Self-Rating Anxiety Scale. *Journal of Anxiety Disorders*, 20(5), 543-561.

## 相关词条

- [DSM-5-TR 评估量表总览](DSM-5TR-Scales.md)
- [抑郁自评量表（SDS）](Self-Rating-Depression-Scale-SDS.md)
- [症状自评量表修订版（SCL-90-R）](Symptom-Checklist-90-SCL-90.md)
- [焦虑障碍（Anxiety Disorders）](Anxiety-Disorders.md)
- [惊恐障碍（Panic Disorder）](Panic-Disorder.md)
- [广泛性焦虑障碍（GAD）](Generalized-Anxiety-Disorder-GAD.md)

## 外部链接

- [中国心理卫生杂志](http://www.cjmh.cn/)
- [心理测量学专业资源](https://www.apa.org/science/programs/testing)
