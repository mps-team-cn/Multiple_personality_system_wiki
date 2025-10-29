---
title: 抑郁自评量表（Self-Rating Depression Scale, SDS）
tags:
    - scale:SDS
    - scale:评估量表
    - guide:诊断与临床
topic: 诊断与临床
synonyms:
    - 抑郁自评量表
    - SDS
    - Zung抑郁量表
    - Self-Rating Depression Scale
description: 抑郁自评量表（SDS）是由Zung于1965年编制的自评量表，包含20个项目，采用1-4分四级评分系统，用于评估抑郁症状的严重程度及其在治疗中的变化，适合抑郁症状的初步筛查与治疗效果评估。
updated: 2025-10-29
search:
  boost: 1.5
hide:
    - toc
comments: true
---

# 抑郁自评量表（Self-Rating Depression Scale, SDS）

!!! danger "重要声明"
    本量表仅用于教育与自我筛查，**不构成临床诊断**。若分数较高且伴随明显抑郁症状，请及时寻求精神科或临床心理专业评估。本量表不能替代专业的临床诊断。

!!! warning "危机求助资源"
    **若您正在经历严重抑郁、自杀想法或其他急性心理危机，请立即寻求帮助：**

    - **全国24小时心理援助热线**：400-161-9995 / 010-82951332
    - **北京心理危机研究与干预中心**：010-82951332
    - **上海心理援助热线**：021-962525 / 021-12320-5
    - **广州心理危机干预中心**：020-81899120
    - **深圳心理危机干预热线**：0755-25629459
    - **紧急情况请拨打急救电话 120 或直接前往最近的医院急诊科**

    您的生命很宝贵，专业帮助随时可得。

## 概述

**抑郁自评量表（SDS）** 由美国杜克大学医学院的 William W. K. Zung 于 1965 年编制，是目前国际上应用最广泛的抑郁症状自评工具之一。量表包含 20 个项目，评估个体在过去一周内的抑郁症状体验，涵盖情感、躯体和心理症状等多个维度。

量表采用四级评分系统（1-4分），通过粗分和标准分（粗分×1.25）来评估抑郁程度，适用于抑郁症状的初步筛查、治疗效果监测和症状变化追踪。

## 评分说明

!!! tip "使用说明"

    - 每题采用 **1-4 分** 四级评分：
        - **1 = 没有或很少时间**（过去一周内，出现这类情况的日子不超过一天）
        - **2 = 小部分时间**（过去一周内，有1-2天有过这类情况）
        - **3 = 相当多时间**（过去一周内，3-4天有过这类情况）
        - **4 = 绝大部分或全部时间**（过去一周内，有5-7天有过这类情况）
    - 请根据 **过去一周（包括今天）** 的实际体验作答
    - 建议按直觉作答，尽量不要反复修改
    - 完成所有题目后，系统将自动计算粗分和标准分

## 在线评估

<!-- 样式与脚本由 mkdocs.yml 的 extra_css / extra_javascript 注入 -->

<div id="sds-app" class="sds-app">

<div class="sds-meta">
  <div class="sds-hint">评分范围 1–4（1=没有或很少，4=绝大部分或全部时间）· SDS 标准</div>
  <div class="sds-actions">
    <button id="sds-reset" class="md-button">重置</button>
  </div>
</div>

<div class="sds-divider"></div>

<!-- 题目区域 -->
<table class="sds-table">
  <caption>SDS 题目与评分</caption>
  <colgroup>
    <col style="width:3rem">
    <col>
    <col style="width:auto; min-width:20rem">
  </colgroup>
  <thead>
    <tr><th scope="col">#</th><th scope="col">症状描述（过去一周的体验）</th><th scope="col">评分（1-4）</th></tr>
  </thead>
  <tbody>
    <tr class="sds-item"><td class="no">1</td><td>
      我觉得闷闷不乐，情绪低沉
    </td><td>
      <div class="sds-ctrl">
        <select id="item1">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item1" class="sds-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">2</td><td>
      我觉得一天之中早晨最好 *
    </td><td>
      <div class="sds-ctrl">
        <select id="item2">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item2" class="sds-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">3</td><td>
      我一阵阵哭出来或觉得想哭
    </td><td>
      <div class="sds-ctrl">
        <select id="item3">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item3" class="sds-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">4</td><td>
      我晚上睡眠不好
    </td><td>
      <div class="sds-ctrl">
        <select id="item4">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item4" class="sds-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">5</td><td>
      我吃得跟平常一样多 *
    </td><td>
      <div class="sds-ctrl">
        <select id="item5">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item5" class="sds-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">6</td><td>
      我与异性密切接触时和以往一样感到愉快 *
    </td><td>
      <div class="sds-ctrl">
        <select id="item6">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item6" class="sds-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">7</td><td>
      我发觉我的体重在下降
    </td><td>
      <div class="sds-ctrl">
        <select id="item7">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item7" class="sds-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">8</td><td>
      我有便秘的苦恼
    </td><td>
      <div class="sds-ctrl">
        <select id="item8">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item8" class="sds-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">9</td><td>
      我心跳比平时快
    </td><td>
      <div class="sds-ctrl">
        <select id="item9">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item9" class="sds-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">10</td><td>
      我无缘无故地感到疲乏
    </td><td>
      <div class="sds-ctrl">
        <select id="item10">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item10" class="sds-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">11</td><td>
      我的头脑跟平常一样清楚 *
    </td><td>
      <div class="sds-ctrl">
        <select id="item11">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item11" class="sds-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">12</td><td>
      我觉得经常做的事情并没有困难 *
    </td><td>
      <div class="sds-ctrl">
        <select id="item12">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item12" class="sds-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">13</td><td>
      我觉得不安而平静不下来
    </td><td>
      <div class="sds-ctrl">
        <select id="item13">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item13" class="sds-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">14</td><td>
      我对将来抱有希望 *
    </td><td>
      <div class="sds-ctrl">
        <select id="item14">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item14" class="sds-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">15</td><td>
      我比平常容易生气激动
    </td><td>
      <div class="sds-ctrl">
        <select id="item15">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item15" class="sds-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">16</td><td>
      我觉得作出决定是容易的 *
    </td><td>
      <div class="sds-ctrl">
        <select id="item16">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item16" class="sds-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">17</td><td>
      我觉得自己是个有用的人，有人需要我 *
    </td><td>
      <div class="sds-ctrl">
        <select id="item17">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item17" class="sds-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">18</td><td>
      我的生活过得很有意思 *
    </td><td>
      <div class="sds-ctrl">
        <select id="item18">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item18" class="sds-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">19</td><td>
      我认为如果我死了，别人会生活得好些
    </td><td>
      <div class="sds-ctrl">
        <select id="item19">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item19" class="sds-badge" aria-live="polite" aria-label="当前项评分">1</output>
      </div>
    </td></tr>

    <tr class="sds-item"><td class="no">20</td><td>
      平常感兴趣的事我仍然照样感兴趣 *
    </td><td>
      <div class="sds-ctrl">
        <select id="item20">
          <option value="1">没有或很少时间</option>
          <option value="2">小部分时间</option>
          <option value="3">相当多时间</option>
          <option value="4">绝大部分或全部时间</option>
        </select>
        <output for="item20" class="sds-badge" aria-live="polite" aria-label="当前项评分">4</output>
      </div>
    </td></tr>
  </tbody>
</table>

<div class="sds-note" style="margin-top:.5rem;padding:.5rem .8rem;background:color-mix(in srgb,#ff9800 8%,transparent);border-left:3px solid #ff9800;border-radius:.4rem;">
  <strong>* 反向计分题目：</strong>题目 2、5、6、11、12、14、16、17、18、20 为反向计分题（选择"没有或很少时间"得4分，"绝大部分或全部时间"得1分），系统会自动处理反向计分。
</div>

<div class="sds-divider"></div>

<!-- 结果区域 -->
<div class="sds-results" id="sds-results">
  <div class="sds-section-title">评估结果</div>

  <!-- 主要指标 -->
  <div class="sds-score-card">
    <div>
      <div class="sds-score-label">粗分（20题原始分相加）</div>
      <div class="sds-hint">范围：20-80分</div>
    </div>
    <div class="sds-score-value" id="sds-raw-score">20</div>
  </div>

  <div class="sds-score-card">
    <div>
      <div class="sds-score-label">标准分（粗分 × 1.25）</div>
      <div class="sds-hint">范围：25-100分</div>
    </div>
    <div class="sds-score-value" id="sds-standard-score">25</div>
  </div>

  <!-- 进度条 -->
  <div>
    <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:.4rem;">
      <strong>抑郁程度</strong>
      <span style="font-size:1.1rem; font-weight:700;" id="sds-severity">无抑郁</span>
    </div>
    <div class="sds-progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
      <div class="bar" id="sds-progress-bar" style="width:0%"></div>
    </div>
    <div class="sds-legend">
      <span>无抑郁（&lt;53）</span>
      <span>重度抑郁（≥73）</span>
    </div>
  </div>

  <div class="sds-divider"></div>

  <!-- 抑郁指数 -->
  <div class="sds-score-card">
    <div>
      <div class="sds-score-label">抑郁指数</div>
      <div class="sds-hint">粗分 / 80（满分）</div>
    </div>
    <div class="sds-score-value" id="sds-index">25.0%</div>
  </div>

  <!-- 完成进度 -->
  <div class="sds-score-card">
    <div class="sds-score-label">完成进度</div>
    <div class="sds-score-value" id="sds-completion">20/20 (100%)</div>
  </div>

  <div class="sds-divider"></div>

  <div class="sds-note">
    <strong>中国常模参考区间：</strong>
  </div>
  <ul class="sds-note">
    <li><strong>标准分 &lt; 53</strong>：正常范围（无抑郁）</li>
    <li><strong>标准分 53-62</strong>：轻度抑郁</li>
    <li><strong>标准分 63-72</strong>：中度抑郁</li>
    <li><strong>标准分 ≥ 73</strong>：重度抑郁</li>
  </ul>

  <!-- 安全提示 -->
  <div id="sds-safety-alert" class="sds-note" style="display:none;margin-top:.8rem;padding:.6rem;background:color-mix(in srgb,#f56c6c 8%,transparent);border-left:3px solid #f56c6c;border-radius:.4rem;">
    <strong>🆘 建议寻求专业帮助：</strong>您的评分提示可能存在中度或重度抑郁症状。建议及时咨询精神科医生或心理健康专业人员进行进一步评估和治疗。若您有自杀想法，请立即拨打危机热线或前往最近的医院急诊科。
  </div>

  <div class="sds-divider"></div>

  <div class="sds-note" style="padding:.6rem;background:color-mix(in srgb,#f56c6c 8%,transparent);border-left:3px solid #f56c6c;border-radius:.4rem;">
    <strong>⚠️ 自杀风险警示：</strong>若您在题目 19（我认为如果我死了，别人会生活得好些）上评分较高（≥3分），或正在经历自杀想法，<strong>请立即寻求专业帮助</strong>：
  </div>
  <ul class="sds-note" style="margin-top:.3rem;">
    <li><strong>全国24小时心理援助热线</strong>：400-161-9995 / 010-82951332</li>
    <li><strong>紧急情况请拨打 120 或直接前往最近的医院急诊科</strong></li>
  </ul>

  <div class="sds-divider"></div>

  <div class="sds-note">
    <strong>重要提示：</strong>
  </div>
  <ul class="sds-note">
    <li>本量表仅作为初步筛查工具，不能替代专业临床诊断</li>
    <li>SDS 是症状学量表，高分提示抑郁症状，但不能直接诊断抑郁障碍</li>
    <li>若评分较高或症状显著影响生活，建议寻求精神科或临床心理专业评估</li>
    <li>量表可用于治疗过程中的症状监测，追踪治疗效果</li>
    <li>本在线版为教育用途，临床使用请采用标准化纸笔版或专业软件</li>
  </ul>
</div>

</div>

## 量表信息

### 开发与信效度

- **原作者**：Zung, W. W. K. (1965)
- **题目数量**：20 题
- **评分系统**：1-4 分四级评分
- **反向计分题**：10 题（题目 2、5、6、11、12、14、16、17、18、20）
- **内部一致性**：Cronbach's α 约 0.79-0.92
- **重测信度**：0.68-0.85（一周间隔）
- **中国常模**：已建立中国常模，分界值为标准分 53 分

### 量表结构

SDS 包含 20 个项目，涵盖抑郁症状的多个维度：

1. **情感症状**（6 题）：题目 1, 3, 13, 15, 19, 以及反向题 14
   - 评估情绪低落、哭泣、易激惹、无望感等

2. **躯体症状**（8 题）：题目 4, 7, 8, 9, 10, 以及反向题 2, 5, 6
   - 评估睡眠障碍、食欲改变、体重下降、心悸、疲乏等

3. **心理症状**（6 题）：题目 16（反向）, 17（反向）, 18（反向）, 20（反向）, 11（反向）, 12（反向）
   - 评估思维迟缓、决策困难、无价值感、兴趣丧失等

### 计分方法

1. **正向计分题**（10 题：1, 3, 4, 7, 8, 9, 10, 13, 15, 19）：
   - 1 = 没有或很少时间
   - 2 = 小部分时间
   - 3 = 相当多时间
   - 4 = 绝大部分或全部时间

2. **反向计分题**（10 题：2, 5, 6, 11, 12, 14, 16, 17, 18, 20）：
   - 1 = 绝大部分或全部时间（记 4 分）
   - 2 = 相当多时间（记 3 分）
   - 3 = 小部分时间（记 2 分）
   - 4 = 没有或很少时间（记 1 分）

3. **计算方法**：
   - **粗分**：20 个项目得分之和（范围 20-80）
   - **标准分**：粗分 × 1.25，四舍五入取整（范围 25-100）
   - **抑郁指数**：粗分 / 80（满分）

### 结果解释

根据中国常模（李洁等，1990）：

- **标准分 < 53**：正常范围（无抑郁）
- **标准分 53-62**：轻度抑郁
- **标准分 63-72**：中度抑郁
- **标准分 ≥ 73**：重度抑郁

!!! note "其他常用标准"
    - **粗分正常上限**：41 分
    - **标准分 ≥ 50**：中国常模认为有抑郁症状
    - **标准分 ≥ 70**：美国常模认为有临床意义的抑郁

### 临床应用

SDS 主要用于：

1. **抑郁症状筛查**：识别可能存在抑郁症状的个体
2. **症状严重度评估**：评估抑郁症状的严重程度
3. **治疗效果监测**：评估治疗过程中抑郁症状的变化
4. **流行病学调查**：大规模抑郁症状调查

### 适用人群

- 成年人（18 岁及以上）
- 具有抑郁症状或疑似抑郁障碍的个体
- 需要治疗监测的抑郁症患者

### 使用注意事项

1. **不能替代诊断**：SDS 是筛查工具，不能单独用于诊断抑郁障碍
2. **需专业解释**：高分需结合临床访谈和其他评估工具综合判断
3. **文化差异**：不同地区、文化背景的常模可能有所差异
4. **反向计分**：使用时需注意反向计分题的处理
5. **自杀风险**：题目 19 涉及自杀想法，高分需特别关注

## 参考文献

1. Zung, W. W. K. (1965). A Self-Rating Depression Scale. *Archives of General Psychiatry*, 12(1), 63-70.

2. 李洁, 张明园 (1990). 抑郁自评量表（SDS）在心理咨询中的应用. *中国心理卫生杂志*, 4(4), 164-167.

3. 汪向东, 王希林, 马弘 (1999). 心理卫生评定量表手册（增订版）. 中国心理卫生杂志社.

4. Jokelainen, J., Timonen, M., Keinänen-Kiukaanniemi, S., Härkänen, T., Jurvelin, H., & Suija, K. (2019). Validation of the Zung self-rating depression scale (SDS) in older adults. *Scandinavian Journal of Primary Health Care*, 37(3), 353-357.

5. Dunstan, D. A., & Scott, N. (2020). Norms for Zung's Self-rating Anxiety Scale. *BMC Psychiatry*, 20(1), 90.

## 相关词条

- [DSM-5-TR 评估量表总览](DSM-5TR-Scales.md)
- [焦虑自评量表（SAS）](Self-Rating-Anxiety-Scale-SAS.md)
- [症状自评量表修订版（SCL-90-R）](Symptom-Checklist-90-SCL-90.md)
- [抑郁障碍（Depressive Disorders）](Depressive-Disorders.md)
- [重性抑郁障碍（MDD）](Major-Depressive-Disorder.md)
- [持续性抑郁障碍（PDD）](Persistent-Depressive-Disorder.md)

## 外部链接

- [中国心理卫生杂志](http://www.cjmh.cn/)
- [心理测量学专业资源](https://www.apa.org/science/programs/testing)
