---
description: Zung焦虑自评量表（SAS）中文交互版，含20项焦虑症状评估，适用于成人焦虑症状的自评筛查与教育用途。
hide:
  - toc
search:
  boost: 1.5
synonyms:
  - 焦虑自评量表
  - Self-Rating Anxiety Scale
  - Zung焦虑量表
  - SAS
  - 焦虑量表
tags:
  - scale:SAS
  - scale:评估量表
  - dx:焦虑障碍
  - guide:诊断与临床
title: 焦虑自评量表（Self-Rating Anxiety Scale, SAS）
topic: 诊断与临床
updated: 2025-10-29
---

# 焦虑自评量表（Self-Rating Anxiety Scale, SAS）

!!! danger "重要声明"
    本量表仅用于教育与自我筛查，**不构成临床诊断**。若分数较高且伴随持续焦虑情绪、躯体不适或功能受损，请及时寻求精神科或临床心理专业评估。

## 概述

**焦虑自评量表（SAS）** 由Zung于1971年编制，是国际常用的焦虑症状筛查工具。它评估个体在过去一周内出现的焦虑相关感受和躯体症状的频率，涵盖心理情绪、躯体症状、行为表现等多个维度。

!!! tip "使用说明"
    - 根据过去一周的实际感受选择每个描述的频度
    - 正向题：1=没有或很少时间，2=小部分时间，3=相当多时间，4=绝大部分或全部时间
    - 反向题（带*号）：4=没有或很少时间，3=小部分时间，2=相当多时间，1=绝大部分或全部时间
    - 建议按直觉作答；尽量不要反复修改，以首次直觉为准。可在最后点击"计算分数"。

<!-- 样式与脚本由 mkdocs.yml 的 extra_css / extra_javascript 注入 -->

<div id="sas-app" class="sas-app">

<div class="sas-meta">
  <div class="sas-hint">选择过去一周内各种感受出现的频度</div>
  <div class="sas-actions">
    <button id="sas-reset" class="md-button">重置</button>
  </div>
</div>

<div class="sas-divider"></div>

<table class="sas-table">
  <caption>SAS 焦虑自评量表题目与评分</caption>
  <colgroup>
    <col style="width:2.2rem">
    <col>
    <col style="width:25rem">
  </colgroup>
  <thead>
    <tr><th scope="col">#</th><th scope="col">描述</th><th scope="col">频度</th></tr>
  </thead>
  <tbody>
    <tr class="sas-item">
      <td class="no">1</td>
      <td>我觉得比平常容易紧张或着急</td>
      <td>
        <div class="sas-ctrl">
          <input id="item1" type="range" min="1" max="4" step="1" value="1">
          <output for="item1" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">2</td>
      <td>我无缘无故地感到害怕</td>
      <td>
        <div class="sas-ctrl">
          <input id="item2" type="range" min="1" max="4" step="1" value="1">
          <output for="item2" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">3</td>
      <td>我容易心里烦乱或觉得惊恐</td>
      <td>
        <div class="sas-ctrl">
          <input id="item3" type="range" min="1" max="4" step="1" value="1">
          <output for="item3" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">4</td>
      <td>我觉得我可能将要发疯</td>
      <td>
        <div class="sas-ctrl">
          <input id="item4" type="range" min="1" max="4" step="1" value="1">
          <output for="item4" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">5</td>
      <td>我觉得一切都很好，也不会发生什么不幸*</td>
      <td>
        <div class="sas-ctrl">
          <input id="item5" type="range" min="1" max="4" step="1" value="4">
          <output for="item5" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">6</td>
      <td>我手脚发抖打颤</td>
      <td>
        <div class="sas-ctrl">
          <input id="item6" type="range" min="1" max="4" step="1" value="1">
          <output for="item6" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">7</td>
      <td>我因为头痛、颈痛和背痛而苦恼</td>
      <td>
        <div class="sas-ctrl">
          <input id="item7" type="range" min="1" max="4" step="1" value="1">
          <output for="item7" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">8</td>
      <td>我感觉容易衰弱和疲乏</td>
      <td>
        <div class="sas-ctrl">
          <input id="item8" type="range" min="1" max="4" step="1" value="1">
          <output for="item8" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">9</td>
      <td>我得心平气和，并且容易安静坐着*</td>
      <td>
        <div class="sas-ctrl">
          <input id="item9" type="range" min="1" max="4" step="1" value="4">
          <output for="item9" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">10</td>
      <td>我觉得心跳得很快</td>
      <td>
        <div class="sas-ctrl">
          <input id="item10" type="range" min="1" max="4" step="1" value="1">
          <output for="item10" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">11</td>
      <td>我因为一阵阵头晕而苦恼</td>
      <td>
        <div class="sas-ctrl">
          <input id="item11" type="range" min="1" max="4" step="1" value="1">
          <output for="item11" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">12</td>
      <td>我有晕倒发作，或觉得要晕倒似的</td>
      <td>
        <div class="sas-ctrl">
          <input id="item12" type="range" min="1" max="4" step="1" value="1">
          <output for="item12" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">13</td>
      <td>我吸气呼气都感到很容易*</td>
      <td>
        <div class="sas-ctrl">
          <input id="item13" type="range" min="1" max="4" step="1" value="4">
          <output for="item13" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">14</td>
      <td>我的手脚麻木和刺痛</td>
      <td>
        <div class="sas-ctrl">
          <input id="item14" type="range" min="1" max="4" step="1" value="1">
          <output for="item14" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">15</td>
      <td>我因为胃痛和消化不良而苦恼</td>
      <td>
        <div class="sas-ctrl">
          <input id="item15" type="range" min="1" max="4" step="1" value="1">
          <output for="item15" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">16</td>
      <td>我常常要小便</td>
      <td>
        <div class="sas-ctrl">
          <input id="item16" type="range" min="1" max="4" step="1" value="1">
          <output for="item16" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">17</td>
      <td>我的手脚常常是干燥温暖的*</td>
      <td>
        <div class="sas-ctrl">
          <input id="item17" type="range" min="1" max="4" step="1" value="4">
          <output for="item17" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">18</td>
      <td>我脸红发热</td>
      <td>
        <div class="sas-ctrl">
          <input id="item18" type="range" min="1" max="4" step="1" value="1">
          <output for="item18" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">19</td>
      <td>我容易入睡并且一夜睡得很好*</td>
      <td>
        <div class="sas-ctrl">
          <input id="item19" type="range" min="1" max="4" step="1" value="4">
          <output for="item19" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>

    <tr class="sas-item">
      <td class="no">20</td>
      <td>我做恶梦</td>
      <td>
        <div class="sas-ctrl">
          <input id="item20" type="range" min="1" max="4" step="1" value="1">
          <output for="item20" class="sas-badge" aria-live="polite" aria-label="当前项频度">没有或很少时间</output>
        </div>
      </td>
    </tr>
  </tbody>
</table>

<div class="sas-divider"></div>

<div id="sas-results" class="sas-results">
  <div><strong>粗分</strong>：<span id="sas-raw" class="sas-badge">20</span> / 80</div>
  <div><strong>标准分</strong>：<span id="sas-standard" class="sas-badge">25.0</span> / 100</div>
  <div class="sas-progress" aria-label="SAS 标准分可视化">
    <div id="sas-bar" class="bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="25" style="width:25%"></div>
  </div>
  <div class="sas-legend"><span>25</span><span>50</span><span>59</span><span>69</span><span>100</span></div>
  <div class="sas-note">焦虑程度：<span id="sas-level">正常范围</span></div>
</div>

</div>

!!! info "分数解释（参考Zung, 1971；仅作筛查）"

    **标准分 = 粗分 × 1.25（取整数部分）**

    - **25-49分**：正常范围（无明显焦虑症状）
    - **50-59分**：轻度焦虑
    - **60-69分**：中度焦虑
    - **70分及以上**：重度焦虑

    注：分界值用于筛查与研究，不同研究可能采用略有不同的阈值设定。任何分数均需结合主观痛苦与功能受损综合判断，**不直接等同临床诊断**。

!!! note "评分方法说明"

    - **正向题（15题）**：1、2、3、4、6、7、8、10、11、12、14、15、16、18、20
      - 1=没有或很少时间，2=小部分时间，3=相当多时间，4=绝大部分或全部时间

    - **反向题（5题，带*号）**：5、9、13、17、19
      - 4=没有或很少时间，3=小部分时间，2=相当多时间，1=绝大部分或全部时间

    - **粗分范围**：20-80分
    - **标准分范围**：25-100分

!!! info "版本与来源"
    本中文版参考 Zung (1971) 原版焦虑自评量表进行教育性改编，结合国内临床常用版本进行翻译与优化。

---

## 临床应用注意事项

### 适用人群
- 具有焦虑症状的成年人（包括门诊及住院患者）
- 用于焦虑症状的初步筛查和严重程度评估
- 治疗过程中的症状变化追踪

### 使用限制
- 不能代替全面的临床访谈来确定焦虑症的诊断
- 测试结果仅供参考，不作为正式诊断标准
- 需考虑个体对躯体症状的关注程度和表达方式差异

### 结果解释原则
- 分数越高，焦虑症状越严重
- 需结合个体的主观痛苦程度、社会功能受损情况综合判断
- 重点关注惊恐发作相关条目的阳性结果
- 建议定期重复测量以评估症状变化趋势

---

## 相关词条

- [广泛性焦虑量表-7（GAD-7）](GAD-7.md)
- [抑郁自评量表（SDS）](Self-Rating-Depression-Scale-SDS.md)
- [贝克焦虑量表（BAI）](Beck-Anxiety-Inventory.md)
- [焦虑障碍](Anxiety-Disorders.md)
- [临床诊断导览](../guides/Clinical-Diagnosis-Guide.md)

---

## 参考文献

- Zung, W. W. (1971). A rating instrument for anxiety disorders. *Psychosomatics, 12*(6), 371-379.
- 张明园 (1998). 精神科评定量表手册. 湖南科学技术出版社.
- 汪向东, 王希林, 马弘 (1999). 心理卫生评定量表手册. 中国心理卫生杂志.