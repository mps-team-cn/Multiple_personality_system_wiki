---
description: Zung抑郁自评量表（SDS）中文交互版，含20项抑郁症状评估，适用于成人抑郁症状的自评筛查与教育用途。
hide:
  - toc
search:
  boost: 1.5
synonyms:
  - 抑郁自评量表
  - Self-Rating Depression Scale
  - Zung抑郁量表
  - SDS
  - 抑郁量表
tags:
  - scale:SDS
  - scale:评估量表
  - dx:抑郁障碍
  - guide:诊断与临床
title: 抑郁自评量表（Self-Rating Depression Scale, SDS）
topic: 诊断与临床
updated: 2025-10-29
---

# 抑郁自评量表（Self-Rating Depression Scale, SDS）

!!! danger "重要声明"
    本量表仅用于教育与自我筛查，**不构成临床诊断**。若分数较高且伴随持续抑郁情绪、兴趣减退或功能受损，请及时寻求精神科或临床心理专业评估。

## 概述

**抑郁自评量表（SDS）** 由美国杜克大学心理学家William W.K. Zung于1965年编制，是国际常用的抑郁症状筛查工具。它评估个体在过去一周内出现的抑郁相关感受和症状的频率，包含情感、躯体、心理和行为等多个维度。

!!! tip "使用说明"
    - 根据过去一周的实际感受选择每个描述的频度
    - 正向题：1=没有或很少时间，2=少部分时间，3=相当多时间，4=绝大部分时间
    - 反向题（带*号）：4=没有或很少时间，3=少部分时间，2=相当多时间，1=绝大部分时间
    - 建议按直觉作答；尽量不要反复修改，以首次直觉为准。可在最后点击"计算分数"。

<!-- 样式与脚本由 mkdocs.yml 的 extra_css / extra_javascript 注入 -->

<div id="sds-app" class="sds-app">

<div class="sds-meta">
  <div class="sds-hint">选择过去一周内各种感受出现的频度</div>
  <div class="sds-actions">
    <button id="sds-reset" class="md-button">重置</button>
  </div>
</div>

<div class="sds-divider"></div>

<table class="sds-table">
  <caption>SDS 抑郁自评量表题目与评分</caption>
  <colgroup>
    <col style="width:2.2rem">
    <col>
    <col style="width:25rem">
  </colgroup>
  <thead>
    <tr><th scope="col">#</th><th scope="col">描述</th><th scope="col">频度</th></tr>
  </thead>
  <tbody>
    <tr class="sds-item">
      <td class="no">1</td>
      <td>我觉得闷闷不乐，情绪低沉</td>
      <td>
        <div class="sds-ctrl">
          <input id="item1" type="range" min="1" max="4" step="1" value="1">
          <output for="item1" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">2</td>
      <td>我觉得一天中早晨最好*</td>
      <td>
        <div class="sds-ctrl">
          <input id="item2" type="range" min="1" max="4" step="1" value="4">
          <output for="item2" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">3</td>
      <td>一阵阵哭出来或觉得想哭</td>
      <td>
        <div class="sds-ctrl">
          <input id="item3" type="range" min="1" max="4" step="1" value="1">
          <output for="item3" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">4</td>
      <td>我晚上睡眠不好</td>
      <td>
        <div class="sds-ctrl">
          <input id="item4" type="range" min="1" max="4" step="1" value="1">
          <output for="item4" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">5</td>
      <td>我吃得跟平常一样多*</td>
      <td>
        <div class="sds-ctrl">
          <input id="item5" type="range" min="1" max="4" step="1" value="4">
          <output for="item5" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">6</td>
      <td>我与异性密切接触时和以往一样感到愉快*</td>
      <td>
        <div class="sds-ctrl">
          <input id="item6" type="range" min="1" max="4" step="1" value="4">
          <output for="item6" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">7</td>
      <td>我发觉我的体重在下降</td>
      <td>
        <div class="sds-ctrl">
          <input id="item7" type="range" min="1" max="4" step="1" value="1">
          <output for="item7" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">8</td>
      <td>我有便秘的苦恼</td>
      <td>
        <div class="sds-ctrl">
          <input id="item8" type="range" min="1" max="4" step="1" value="1">
          <output for="item8" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">9</td>
      <td>心跳比平常快</td>
      <td>
        <div class="sds-ctrl">
          <input id="item9" type="range" min="1" max="4" step="1" value="1">
          <output for="item9" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">10</td>
      <td>我无缘无故地感到疲乏</td>
      <td>
        <div class="sds-ctrl">
          <input id="item10" type="range" min="1" max="4" step="1" value="1">
          <output for="item10" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">11</td>
      <td>我的头脑和平常一样清楚*</td>
      <td>
        <div class="sds-ctrl">
          <input id="item11" type="range" min="1" max="4" step="1" value="4">
          <output for="item11" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">12</td>
      <td>我觉得经常做的事情并没有困难*</td>
      <td>
        <div class="sds-ctrl">
          <input id="item12" type="range" min="1" max="4" step="1" value="4">
          <output for="item12" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">13</td>
      <td>我觉得不安而平静不下来</td>
      <td>
        <div class="sds-ctrl">
          <input id="item13" type="range" min="1" max="4" step="1" value="1">
          <output for="item13" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">14</td>
      <td>我对未来抱有希望*</td>
      <td>
        <div class="sds-ctrl">
          <input id="item14" type="range" min="1" max="4" step="1" value="4">
          <output for="item14" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">15</td>
      <td>我比平常容易生气激动</td>
      <td>
        <div class="sds-ctrl">
          <input id="item15" type="range" min="1" max="4" step="1" value="1">
          <output for="item15" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">16</td>
      <td>我觉得做出决定是容易的*</td>
      <td>
        <div class="sds-ctrl">
          <input id="item16" type="range" min="1" max="4" step="1" value="4">
          <output for="item16" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">17</td>
      <td>我觉得自己是个有用的人，有人需要我*</td>
      <td>
        <div class="sds-ctrl">
          <input id="item17" type="range" min="1" max="4" step="1" value="4">
          <output for="item17" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">18</td>
      <td>我的生活过得很有意思*</td>
      <td>
        <div class="sds-ctrl">
          <input id="item18" type="range" min="1" max="4" step="1" value="4">
          <output for="item18" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">19</td>
      <td>我认为如果我死了，别人会生活得更好</td>
      <td>
        <div class="sds-ctrl">
          <input id="item19" type="range" min="1" max="4" step="1" value="1">
          <output for="item19" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sds-item">
      <td class="no">20</td>
      <td>平常感兴趣的事我仍然感兴趣*</td>
      <td>
        <div class="sds-ctrl">
          <input id="item20" type="range" min="1" max="4" step="1" value="4">
          <output for="item20" class="sds-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>
  </tbody>
</table>

<div class="sds-divider"></div>

<div id="sds-results" class="sds-results">
  <div><strong>粗分</strong>：<span id="sds-raw" class="sds-badge">20</span> / 80</div>
  <div><strong>标准分</strong>：<span id="sds-standard" class="sds-badge">25.0</span> / 100</div>
  <div class="sds-progress" aria-label="SDS 标准分可视化">
    <div id="sds-bar" class="bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="25" style="width:25%"></div>
  </div>
  <div class="sds-legend"><span>25</span><span>50</span><span>62</span><span>72</span><span>100</span></div>
  <div class="sds-note">抑郁程度：<span id="sds-level">正常范围</span></div>
</div>

</div>

!!! info "分数解释（参考Zung, 1965；仅作筛查）"

    **标准分 = 粗分 × 1.25**

    - **25-49分**：正常范围（无抑郁症状）
    - **50-62分**：轻度抑郁
    - **63-72分**：中度抑郁
    - **73分及以上**：重度抑郁

    注：分界值用于筛查与研究，不同研究可能采用略有不同的阈值设定。任何分数均需结合主观痛苦与功能受损综合判断，**不直接等同临床诊断**。

!!! note "评分方法说明"

    - **正向题（10题）**：1、3、4、7、8、9、10、13、15、19
      - 1=没有或很少时间，2=少部分时间，3=相当多时间，4=绝大部分时间

    - **反向题（10题，带*号）**：2、5、6、11、12、14、16、17、18、20
      - 4=没有或很少时间，3=少部分时间，2=相当多时间，1=绝大部分时间

    - **粗分范围**：20-80分
    - **标准分范围**：25-100分

!!! info "版本与来源"
    本中文版参考 William W.K. Zung (1965) 原版抑郁自评量表进行教育性改编，结合国内临床常用版本进行翻译与优化。

---

## 临床应用注意事项

### 适用人群
- 具有抑郁症状的成年人（包括门诊及住院患者）
- 用于抑郁症状的初步筛查和严重程度评估
- 治疗过程中的症状变化追踪

### 使用限制
- 对严重迟缓症状的抑郁患者，评定可能有困难
- 文化程度较低或智力水平稍差的人使用效果不佳
- 不能代替全面的临床访谈来确定抑郁症的诊断
- 测试结果仅供参考，不作为正式诊断标准

### 结果解释原则
- 分数越高，抑郁症状越严重
- 需结合个体的主观痛苦程度、社会功能受损情况综合判断
- 重点关注自杀意念相关条目（如第19题）的阳性结果
- 建议定期重复测量以评估症状变化趋势

---

## 相关词条

- [病人健康问卷-9（PHQ-9）](PHQ-9.md)
- [广泛性焦虑量表-7（GAD-7）](GAD-7.md)
- [贝克抑郁自评量表（BDI）](Beck-Depression-Inventory.md)
- [抑郁障碍](Depressive-Disorders.md)
- [临床诊断导览](../guides/Clinical-Diagnosis-Guide.md)

---

## 参考文献

- Zung, W. W. (1965). A self-rating depression scale. *Archives of General Psychiatry, 12*(1), 63-70.
- 张明园 (1998). 精神科评定量表手册. 湖南科学技术出版社.
- 汪向东, 王希林, 马弘 (1999). 心理卫生评定量表手册. 中国心理卫生杂志.