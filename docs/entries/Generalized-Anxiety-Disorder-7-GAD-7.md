---
title: 广泛性焦虑量表-7（Generalized Anxiety Disorder-7，GAD-7）
tags:
  - scale:GAD-7
  - scale:评估量表
  - dx:焦虑障碍
  - guide:诊断与临床
topic: 诊断与临床
synonyms:
  - GAD-7
  - gad-7
  - gad7
  - 广泛性焦虑量表-7
  - 焦虑筛查量表
  - Generalized Anxiety Disorder-7
description: 广泛性焦虑量表-7（GAD-7）是常用的焦虑筛查与严重度评估工具，7题、0-21分，适合初步整理紧张、担忧失控、难以放松与烦躁等症状线索。
updated: 2026-03-28
search:
  boost: 1.5
hide:
  - toc
comments: true
---

# 广泛性焦虑量表-7（Generalized Anxiety Disorder-7，GAD-7）

!!! danger "重要声明"
    本量表仅用于教育与自我筛查，**不构成临床诊断**。高分提示焦虑症状值得进一步评估，但不能直接等同于广泛性焦虑障碍诊断。

!!! warning "危机求助资源"
    **若您正在经历持续惊恐、极端痛苦、无法保证自身安全或明显失眠恶化，请尽快联系线下专业帮助：**

    - **全国24小时心理援助热线**：400-161-9995 / 010-82951332
    - **北京心理危机研究与干预中心**：010-82951332
    - **上海心理援助热线**：021-962525 / 021-12320-5
    - **广州心理危机干预中心**：020-81899120
    - **深圳心理危机干预热线**：0755-25629459
    - **紧急情况请拨打 120，或直接前往最近的医院急诊科**

## 概述

**GAD-7** 是一个 7 题的焦虑筛查与严重度评估工具，用于评估**过去两周**的担忧、紧张、放松困难与烦躁程度。虽然它最初是为广泛性焦虑障碍开发的，但在临床中也常用来初步观察惊恐、社交焦虑与创伤相关焦虑线索。

GAD-7 每题按 `0-3` 分计分，总分范围 `0-21`。`PHQ and GAD-7 Instructions` 说明 PHQ 家族量表（含 GAD-7）处于 **public domain**，可复制、翻译、展示与分发。

## 评分说明

!!! tip "使用说明"
    - 请根据**过去两周**的实际体验作答
    - 每题按 `0-3` 分评分：
        - `0 = 完全没有`
        - `1 = 几天`
        - `2 = 一半以上天数`
        - `3 = 几乎天天`
    - 总分 `0-21`
    - 常见分界：`5 / 10 / 15`
    - **总分 ≥ 10** 常被视作值得进一步评估的阈值

## 在线评估

<div id="gad7-app" class="brief-scale-app">

<div class="brief-scale-meta">
  <div class="brief-scale-hint">评分范围 0–3（0=完全没有，3=几乎天天）· 过去两周</div>
  <div class="brief-scale-actions">
    <button id="gad7-reset" class="md-button" type="button">重置</button>
  </div>
</div>

<div class="brief-scale-divider"></div>

<table class="brief-scale-table">
  <caption>GAD-7 题目与评分</caption>
  <colgroup>
    <col style="width:3rem">
    <col>
    <col style="width:auto; min-width:20rem">
  </colgroup>
  <thead>
    <tr><th scope="col">#</th><th scope="col">症状描述（过去两周）</th><th scope="col">评分（0-3）</th></tr>
  </thead>
  <tbody>
    <tr class="brief-scale-item gad7-item"><td class="brief-scale-no">1</td><td>感到紧张、焦虑或烦躁</td><td><div class="brief-scale-ctrl"><select id="gad7-item1"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="gad7-item1">0</output></div></td></tr>
    <tr class="brief-scale-item gad7-item"><td class="brief-scale-no">2</td><td>无法停止或控制担忧</td><td><div class="brief-scale-ctrl"><select id="gad7-item2"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="gad7-item2">0</output></div></td></tr>
    <tr class="brief-scale-item gad7-item"><td class="brief-scale-no">3</td><td>对各种事情担忧过多</td><td><div class="brief-scale-ctrl"><select id="gad7-item3"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="gad7-item3">0</output></div></td></tr>
    <tr class="brief-scale-item gad7-item"><td class="brief-scale-no">4</td><td>很难放松下来</td><td><div class="brief-scale-ctrl"><select id="gad7-item4"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="gad7-item4">0</output></div></td></tr>
    <tr class="brief-scale-item gad7-item"><td class="brief-scale-no">5</td><td>由于坐立不安而难以安静坐着</td><td><div class="brief-scale-ctrl"><select id="gad7-item5"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="gad7-item5">0</output></div></td></tr>
    <tr class="brief-scale-item gad7-item"><td class="brief-scale-no">6</td><td>变得容易烦恼或急躁</td><td><div class="brief-scale-ctrl"><select id="gad7-item6"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="gad7-item6">0</output></div></td></tr>
    <tr class="brief-scale-item gad7-item"><td class="brief-scale-no">7</td><td>感到好像将有可怕的事情发生</td><td><div class="brief-scale-ctrl"><select id="gad7-item7"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="gad7-item7">0</output></div></td></tr>
  </tbody>
</table>

<div class="brief-scale-field">
  <label for="gad7-impairment">这些问题在多大程度上影响了你的工作、家务或与人相处？（不计入总分）</label>
  <select id="gad7-impairment">
    <option value="">暂不选择</option>
    <option value="none">完全不困难</option>
    <option value="somewhat">有点困难</option>
    <option value="very">非常困难</option>
    <option value="extremely">极度困难</option>
  </select>
</div>

<div class="brief-scale-divider"></div>

<div class="brief-scale-results" id="gad7-results">
  <div class="brief-scale-section-title">评估结果</div>

  <div class="brief-scale-score-card">
    <div>
      <div class="brief-scale-score-label">总分</div>
      <div class="brief-scale-hint">范围：0-21 分</div>
    </div>
    <div class="brief-scale-score-value" id="gad7-raw-score">0</div>
  </div>

  <div>
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.4rem;">
      <strong>严重度</strong>
      <span id="gad7-severity" class="brief-scale-status minimal">无或极轻</span>
    </div>
    <div class="brief-scale-progress" id="gad7-progress" role="progressbar" aria-valuemin="0" aria-valuemax="21" aria-valuenow="0">
      <div class="bar" id="gad7-progress-bar"></div>
    </div>
    <div class="brief-scale-legend">
      <span>0-4 无或极轻</span>
      <span>15-21 重度</span>
    </div>
  </div>

  <div class="brief-scale-grid">
    <div class="brief-scale-score-card">
      <div>
        <div class="brief-scale-score-label">GAD-2 子分</div>
        <div class="brief-scale-hint">前两题相加，常见阳性阈值为 ≥ 3</div>
      </div>
      <div class="brief-scale-score-value" id="gad7-gad2">0/6</div>
    </div>
    <div class="brief-scale-score-card">
      <div>
        <div class="brief-scale-score-label">高频症状条目数</div>
        <div class="brief-scale-hint">按 ≥2 分统计，帮助看焦虑是否已较频繁出现</div>
      </div>
      <div class="brief-scale-score-value" id="gad7-positive-count">0/7</div>
    </div>
    <div class="brief-scale-score-card">
      <div>
        <div class="brief-scale-score-label">功能影响</div>
        <div class="brief-scale-hint">附加题，不计入总分</div>
      </div>
      <div class="brief-scale-score-value" id="gad7-impairment-text">未选择</div>
    </div>
  </div>

  <div class="brief-scale-score-card">
    <div>
      <div class="brief-scale-score-label">筛查提示</div>
      <div class="brief-scale-hint" id="gad7-cutoff-label">进一步评估阈值：总分 ≥ 10</div>
    </div>
    <div class="brief-scale-score-value" id="gad7-cutoff">未达到常见进一步评估阈值</div>
  </div>

  <div class="brief-scale-score-card">
    <div class="brief-scale-score-label">解释提示</div>
    <div class="brief-scale-hint" id="gad7-screening-hint">当前未达到 GAD-7 的常见进一步评估阈值。</div>
  </div>

  <div class="brief-scale-score-card">
    <div class="brief-scale-score-label">完成进度</div>
    <div class="brief-scale-score-value" id="gad7-completion">7/7 (100%)</div>
  </div>

  <div id="gad7-safety-alert" class="brief-scale-score-card" style="display:none;border-left:3px solid #f56c6c;">
    <div>
      <div class="brief-scale-score-label">🆘 强烈焦虑提示</div>
      <div class="brief-scale-hint">若焦虑已明显影响睡眠、工作、学习或躯体状态，建议尽快联系专业人员进一步评估，并排除惊恐、物质因素与躯体疾病。</div>
    </div>
    <div class="brief-scale-score-value">建议尽快求助</div>
  </div>

  <div class="brief-scale-divider"></div>

  <div class="brief-scale-note">
    <strong>常见分界参考：</strong>
  </div>
  <ul class="brief-scale-note">
    <li><strong>0-4 分</strong>：无或极轻</li>
    <li><strong>5-9 分</strong>：轻度焦虑</li>
    <li><strong>10-14 分</strong>：中度焦虑</li>
    <li><strong>15-21 分</strong>：重度焦虑</li>
  </ul>
</div>

</div>

## 量表信息

### 开发与用途

- **原作者**：Spitzer, R. L., Kroenke, K., Williams, J. B. W., & Löwe, B.
- **题目数量**：7 题
- **时间范围**：过去 2 周
- **评分系统**：每题 `0-3` 分，总分 `0-21`
- **主要用途**：焦虑症状初筛、严重度评估、治疗过程追踪
- **公开使用**：根据 `PHQ and GAD-7 Instructions`，GAD-7 可复制、翻译、展示与分发

### 解释要点

- `GAD-7` 主要反映**担忧与紧张症状的频率**
- **总分 ≥ 10** 常被用作值得进一步评估的阈值
- 前两题构成 `GAD-2`，常用于更短的焦虑初筛
- GAD-7 分高并不只见于 GAD，也可能出现在**惊恐障碍、社交焦虑、PTSD 或长期高压状态**

## 适合和哪些页面一起宣传

- [DSM-5-TR 评估量表总览](DSM-5TR-Scales.md)
- [焦虑自评量表（SAS）](Self-Rating-Anxiety-Scale-SAS.md)
- [广泛性焦虑障碍（GAD）](Generalized-Anxiety-Disorder-GAD.md)
- [惊恐障碍（Panic Disorder）](Panic-Disorder.md)
- [创伤后应激障碍（PTSD）](PTSD.md)

## 参考与延伸阅读

1. Spitzer, R. L., Kroenke, K., Williams, J. B. W., & Löwe, B. (2006). A brief measure for assessing generalized anxiety disorder: the GAD-7. *Archives of Internal Medicine*, 166(10), 1092-1097.
2. Kroenke, K., Spitzer, R. L., Williams, J. B. W., Monahan, P. O., & Löwe, B. (2007). Anxiety disorders in primary care: prevalence, impairment, comorbidity, and detection. *Annals of Internal Medicine*, 146(5), 317-325.
3. Kroenke, K., Spitzer, R. L., Williams, J. B. W., & Löwe, B. (2010). The Patient Health Questionnaire somatic, anxiety, and depressive symptom scales: a systematic review. *General Hospital Psychiatry*, 32(4), 345-359.
4. Patient Health Questionnaire (PHQ) and GAD-7 Instructions. The Joint Commission / PHQ Screeners.
