---
title: 患者健康问卷-9（Patient Health Questionnaire-9，PHQ-9）
tags:

    - scale:PHQ-9
    - scale:评估量表
    - dx:抑郁障碍
    - guide:诊断与临床

topic: 诊断与临床
synonyms:

    - PHQ-9
    - phq-9
    - phq9
    - 患者健康问卷-9
    - 抑郁筛查量表
    - Patient Health Questionnaire-9

description: 患者健康问卷-9（PHQ-9）是常用的抑郁筛查与严重度评估工具，9题、0-27分，适合初步整理情绪低落、兴趣下降、疲乏与自伤想法等线索。
updated: 2026-03-28
search:
  boost: 1.5
hide:

    - toc

comments: true
---

# 患者健康问卷-9（Patient Health Questionnaire-9，PHQ-9）

!!! danger "重要声明"
    本量表仅用于教育与自我筛查，**不构成临床诊断**。若分数较高，或第 9 题涉及“不如死掉/伤害自己”的想法出现阳性反应，请尽快联系精神科或临床心理专业人员。

!!! warning "危机求助资源"
    **若您正在经历强烈绝望、自伤冲动或自杀想法，请立即寻求线下帮助：**

    - **全国24小时心理援助热线**：400-161-9995 / 010-82951332
    - **北京心理危机研究与干预中心**：010-82951332
    - **上海心理援助热线**：021-962525 / 021-12320-5
    - **广州心理危机干预中心**：020-81899120
    - **深圳心理危机干预热线**：0755-25629459
    - **紧急情况请拨打 120，或直接前往最近的医院急诊科**

## 概述

**PHQ-9** 是目前国际上最常用的抑郁自评工具之一，用于评估 **过去两周** 内的抑郁症状频率与严重程度。它既可作为初步筛查工具，也常用于治疗过程中的症状追踪。

PHQ-9 共 9 题，每题按 `0-3` 分计分，总分范围 `0-27`。根据 `PHQ and GAD-7 Instructions`，PHQ 家族量表（包括 PHQ-9、GAD-7）已处于 **public domain**，可用于复制、翻译、展示与分发。

## 评分说明

!!! tip "使用说明"

    - 请根据 **过去两周** 的实际体验作答
    - 每题按 `0-3` 分评分：
        - `0 = 完全没有`
        - `1 = 几天`
        - `2 = 一半以上天数`
        - `3 = 几乎天天`
    - 总分 `0-27`
    - 常见分界：`5 / 10 / 15 / 20`
    - **第 9 题不论总分高低，只要大于 0 都值得认真对待**

## 在线评估

<div id="phq9-app" class="brief-scale-app">

<div class="brief-scale-meta">
  <div class="brief-scale-hint">评分范围 0–3（0=完全没有，3=几乎天天）· 过去两周</div>
  <div class="brief-scale-actions">
    <button id="phq9-reset" class="md-button" type="button">重置</button>
  </div>
</div>

<div class="brief-scale-divider"></div>

<table class="brief-scale-table">
  <caption>PHQ-9 题目与评分</caption>
  <colgroup>
    <col style="width:3rem">
    <col>
    <col style="width:auto; min-width:20rem">
  </colgroup>
  <thead>
    <tr><th scope="col">#</th><th scope="col">症状描述（过去两周）</th><th scope="col">评分（0-3）</th></tr>
  </thead>
  <tbody>
    <tr class="brief-scale-item phq9-item"><td class="brief-scale-no">1</td><td>做事时提不起劲或没有乐趣</td><td><div class="brief-scale-ctrl"><select id="phq9-item1"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="phq9-item1">0</output></div></td></tr>
    <tr class="brief-scale-item phq9-item"><td class="brief-scale-no">2</td><td>感到情绪低落、沮丧或绝望</td><td><div class="brief-scale-ctrl"><select id="phq9-item2"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="phq9-item2">0</output></div></td></tr>
    <tr class="brief-scale-item phq9-item"><td class="brief-scale-no">3</td><td>入睡困难、睡不安，或睡眠过多</td><td><div class="brief-scale-ctrl"><select id="phq9-item3"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="phq9-item3">0</output></div></td></tr>
    <tr class="brief-scale-item phq9-item"><td class="brief-scale-no">4</td><td>感觉疲倦或没有活力</td><td><div class="brief-scale-ctrl"><select id="phq9-item4"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="phq9-item4">0</output></div></td></tr>
    <tr class="brief-scale-item phq9-item"><td class="brief-scale-no">5</td><td>食欲不振，或吃太多</td><td><div class="brief-scale-ctrl"><select id="phq9-item5"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="phq9-item5">0</output></div></td></tr>
    <tr class="brief-scale-item phq9-item"><td class="brief-scale-no">6</td><td>觉得自己很糟，或觉得自己很失败，让自己或家人失望</td><td><div class="brief-scale-ctrl"><select id="phq9-item6"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="phq9-item6">0</output></div></td></tr>
    <tr class="brief-scale-item phq9-item"><td class="brief-scale-no">7</td><td>对事物专注有困难，例如阅读或看视频时难以集中注意力</td><td><div class="brief-scale-ctrl"><select id="phq9-item7"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="phq9-item7">0</output></div></td></tr>
    <tr class="brief-scale-item phq9-item"><td class="brief-scale-no">8</td><td>动作或说话变得很慢；或正好相反，烦躁得坐不住、比平时动得更多</td><td><div class="brief-scale-ctrl"><select id="phq9-item8"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="phq9-item8">0</output></div></td></tr>
    <tr class="brief-scale-item phq9-item"><td class="brief-scale-no">9</td><td>有不如死掉，或用某种方式伤害自己的想法</td><td><div class="brief-scale-ctrl"><select id="phq9-item9"><option value="0">完全没有</option><option value="1">几天</option><option value="2">一半以上天数</option><option value="3">几乎天天</option></select><output class="brief-scale-badge" for="phq9-item9">0</output></div></td></tr>
  </tbody>
</table>

<div class="brief-scale-field">
  <label for="phq9-impairment">这些问题在多大程度上影响了你的工作、家务或与人相处？（不计入总分）</label>
  <select id="phq9-impairment">
    <option value="">暂不选择</option>
    <option value="none">完全不困难</option>
    <option value="somewhat">有点困难</option>
    <option value="very">非常困难</option>
    <option value="extremely">极度困难</option>
  </select>
</div>

<div class="brief-scale-divider"></div>

<div class="brief-scale-results" id="phq9-results">
  <div class="brief-scale-section-title">评估结果</div>

  <div class="brief-scale-score-card">
    <div>
      <div class="brief-scale-score-label">总分</div>
      <div class="brief-scale-hint">范围：0-27 分</div>
    </div>
    <div class="brief-scale-score-value" id="phq9-raw-score">0</div>
  </div>

  <div>
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.4rem;">
      <strong>严重度</strong>
      <span id="phq9-severity" class="brief-scale-status none">无或极轻</span>
    </div>
    <div class="brief-scale-progress" id="phq9-progress" role="progressbar" aria-valuemin="0" aria-valuemax="27" aria-valuenow="0">
      <div class="bar" id="phq9-progress-bar"></div>
    </div>
    <div class="brief-scale-legend">
      <span>0-4 无或极轻</span>
      <span>20-27 重度</span>
    </div>
  </div>

  <div class="brief-scale-grid">
    <div class="brief-scale-score-card">
      <div>
        <div class="brief-scale-score-label">PHQ-2 子分</div>
        <div class="brief-scale-hint">前两题相加，常见阳性阈值为 ≥ 3</div>
      </div>
      <div class="brief-scale-score-value" id="phq9-phq2">0/6</div>
    </div>
    <div class="brief-scale-score-card">
      <div>
        <div class="brief-scale-score-label">阳性症状条目数</div>
        <div class="brief-scale-hint">筛查算法中通常按 ≥2 分计；第 9 题 ≥1 也计入</div>
      </div>
      <div class="brief-scale-score-value" id="phq9-positive-count">0/9</div>
    </div>
    <div class="brief-scale-score-card">
      <div>
        <div class="brief-scale-score-label">功能影响</div>
        <div class="brief-scale-hint">附加题，不计入总分</div>
      </div>
      <div class="brief-scale-score-value" id="phq9-impairment-text">未选择</div>
    </div>
    <div class="brief-scale-score-card">
      <div>
        <div class="brief-scale-score-label">第 9 题风险提示</div>
        <div class="brief-scale-hint">只要大于 0 就值得进一步评估</div>
      </div>
      <div class="brief-scale-score-value" id="phq9-item9">未见阳性反应</div>
    </div>
  </div>

  <div class="brief-scale-score-card">
    <div>
      <div class="brief-scale-score-label">筛查提示</div>
      <div class="brief-scale-hint" id="phq9-cutoff-label">进一步评估阈值：总分 ≥ 10</div>
    </div>
    <div class="brief-scale-score-value" id="phq9-cutoff">未达到常见进一步评估阈值</div>
  </div>

  <div class="brief-scale-score-card">
    <div class="brief-scale-score-label">PHQ 模块算法提示</div>
    <div class="brief-scale-hint" id="phq9-screening-hint">当前未达到 PHQ 抑郁模块的常见阳性筛查阈值。</div>
  </div>

  <div class="brief-scale-score-card">
    <div class="brief-scale-score-label">完成进度</div>
    <div class="brief-scale-score-value" id="phq9-completion">9/9 (100%)</div>
  </div>

  <div id="phq9-safety-alert" class="brief-scale-score-card" style="display:none;border-left:3px solid #f56c6c;">
    <div>
      <div class="brief-scale-score-label">🆘 安全提示</div>
      <div class="brief-scale-hint">若第 9 题出现阳性反应，或总分较高且伴明显绝望/停不下来的自责，请尽快联系线下专业人员或可信任的人。</div>
    </div>
    <div class="brief-scale-score-value">建议立即求助</div>
  </div>

  <div class="brief-scale-divider"></div>

  <div class="brief-scale-note">
    <strong>常见分界参考：</strong>
  </div>
  <ul class="brief-scale-note">
    <li><strong>0-4 分</strong>：无或极轻</li>
    <li><strong>5-9 分</strong>：轻度抑郁</li>
    <li><strong>10-14 分</strong>：中度抑郁</li>
    <li><strong>15-19 分</strong>：中重度抑郁</li>
    <li><strong>20-27 分</strong>：重度抑郁</li>
  </ul>
</div>

</div>

## 量表信息

### 开发与用途

- **原作者**：Kroenke, K., Spitzer, R. L., & Williams, J. B. W.
- **题目数量**：9 题
- **时间范围**：过去 2 周
- **评分系统**：每题 `0-3` 分，总分 `0-27`
- **主要用途**：抑郁症状初筛、严重度分层、治疗过程追踪
- **公开使用**：根据 `PHQ and GAD-7 Instructions`，PHQ 家族量表处于 public domain，可复制、翻译、展示与分发

### 解释要点

- `PHQ-9` 是 **症状量表**，不是诊断本身
- **总分 ≥ 10** 常被用作“值得进一步评估”的阈值
- 第 1 题和第 2 题构成 `PHQ-2`，适合超简短初筛
- **第 9 题只要有分数，就需要认真看待风险与安全**

## 适合和哪些页面一起宣传

- [DSM-5-TR 评估量表总览](DSM-5TR-Scales.md)
- [抑郁自评量表（SDS）](Self-Rating-Depression-Scale-SDS.md)
- [重性抑郁障碍（MDD）](Major-Depressive-Disorder-MDD.md)
- [重度抑郁发作（MDE）](Major-Depressive-Episode-MDE.md)
- [持续性抑郁障碍（PDD）](Persistent-Depressive-Disorder-PDD.md)

## 参考与延伸阅读

1. Kroenke, K., Spitzer, R. L., & Williams, J. B. W. (2001). The PHQ-9: Validity of a brief depression severity measure. *Journal of General Internal Medicine*, 16(9), 606-613.
2. Kroenke, K., & Spitzer, R. L. (2002). The PHQ-9: A new depression diagnostic and severity measure. *Psychiatric Annals*, 32(9), 509-521.
3. Kroenke, K., Spitzer, R. L., Williams, J. B. W., & Löwe, B. (2010). The Patient Health Questionnaire somatic, anxiety, and depressive symptom scales: a systematic review. *General Hospital Psychiatry*, 32(4), 345-359.
4. Patient Health Questionnaire (PHQ) and GAD-7 Instructions. The Joint Commission / PHQ Screeners.
