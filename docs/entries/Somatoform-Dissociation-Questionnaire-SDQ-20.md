---
description: 躯体形式解离问卷（SDQ‑20）中文交互版，评估躯体解离症状的严重程度，含 SDQ-5 简化版，自评筛查与教育用途。
hide:

- toc

search:
  boost: 1.5
synonyms:

- 躯体形式解离问卷
- 躯体解离问卷
- Somatoform Dissociation Questionnaire
- SDQ-20
- SDQ20
- SDQ-5

tags:

- scale:SDQ-20
- scale:评估量表
- dx:解离障碍
- guide:诊断与临床

title: 躯体形式解离问卷（Somatoform Dissociation Questionnaire‑20, SDQ‑20）
topic: 诊断与临床
updated: 2025-10-21
---

# 躯体形式解离问卷（Somatoform Dissociation Questionnaire‑20, SDQ‑20）

!!! danger "重要声明"
    本量表仅用于教育与自我筛查，**不构成临床诊断**。若分数较高且伴随明显躯体解离症状，请及时寻求精神科或临床心理专业评估。部分症状可能由躯体疾病引起，请务必排除器质性病因。

## 概述

**躯体形式解离问卷（SDQ‑20）** 由 Nijenhuis、Spinhoven、Van Dyck、Van der Hart 和 Vanderlinden 于 1996 年编制，是评估躯体解离症状严重程度的专业工具。它评估个体在过去一年中出现的各类躯体解离体验，包括：

- **感觉异常**：麻木、疼痛敏感度改变、感官功能异常
- **运动障碍**：瘫痪、僵硬、吞咽或说话困难
- **知觉变化**：视觉、听觉、嗅觉、味觉的异常体验
- **其他躯体症状**：排尿困难、生殖器疼痛、类癫痫发作等

SDQ-20 是一个 **单维度量表**，测量躯体解离作为一个整体构念。量表具有高内部一致性（Cronbach's α 通常 >0.90）。

## 评分说明

!!! tip "使用说明"

    - 每题采用 **1-5 分** 李克特量表评分：
        - **1 = 完全没有**
        - **2 = 有一点**
        - **3 = 中等**
        - **4 = 相当多**
        - **5 = 非常多**
    - 请根据 **过去一年** 的实际体验作答
    - 建议按直觉作答，尽量不要反复修改
    - 原版问卷要求若评分 2-5 分，需标注"医生是否认为此症状由躯体疾病解释"（本在线版为简化版）

## 在线评估

<!-- 样式与脚本由 mkdocs.yml 的 extra_css / extra_javascript 注入 -->

<div id="sdq20-app" class="sdq20-app">

<div class="sdq20-meta">
  <div class="sdq20-hint">评分范围 1–5（1=完全没有，5=非常多）</div>
  <div class="sdq20-actions">
    <button id="sdq20-reset" class="md-button">重置</button>
  </div>
</div>

<div class="sdq20-divider"></div>

<!-- 题目区域 -->
<table class="sdq20-table">
  <caption>SDQ‑20 题目与评分</caption>
  <colgroup>
    <col style="width:2.2rem">
    <col>
    <col style="width:15rem">
  </colgroup>
  <thead>
    <tr><th scope="col">#</th><th scope="col">描述（过去一年的体验）</th><th scope="col">评分（1-5）</th></tr>
  </thead>
  <tbody>
    <tr class="sdq20-item"><td class="no">1</td><td>
      我小便困难。
    </td><td>
      <div class="sdq20-ctrl"><input id="item1" type="range" min="1" max="5" step="1" value="1"><output for="item1" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">2</td><td>
      我不喜欢平常喜欢的味道。（女性：非怀孕或经期时）
    </td><td>
      <div class="sdq20-ctrl"><input id="item2" type="range" min="1" max="5" step="1" value="1"><output for="item2" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">3</td><td>
      我听到近处的声音好像来自很远。
    </td><td>
      <div class="sdq20-ctrl"><input id="item3" type="range" min="1" max="5" step="1" value="1"><output for="item3" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">4</td><td>
      我小便时疼痛。
    </td><td>
      <div class="sdq20-ctrl"><input id="item4" type="range" min="1" max="5" step="1" value="1"><output for="item4" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">5</td><td>
      我的身体或某一部位麻木。
    </td><td>
      <div class="sdq20-ctrl"><input id="item5" type="range" min="1" max="5" step="1" value="1"><output for="item5" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">6</td><td>
      人或物看起来比平常更大。
    </td><td>
      <div class="sdq20-ctrl"><input id="item6" type="range" min="1" max="5" step="1" value="1"><output for="item6" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">7</td><td>
      我出现一次类似癫痫发作的情况。
    </td><td>
      <div class="sdq20-ctrl"><input id="item7" type="range" min="1" max="5" step="1" value="1"><output for="item7" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">8</td><td>
      我的身体或某一部位对疼痛不敏感。
    </td><td>
      <div class="sdq20-ctrl"><input id="item8" type="range" min="1" max="5" step="1" value="1"><output for="item8" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">9</td><td>
      我不喜欢平常喜欢的气味。
    </td><td>
      <div class="sdq20-ctrl"><input id="item9" type="range" min="1" max="5" step="1" value="1"><output for="item9" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">10</td><td>
      我生殖器疼痛（非性生活时）。
    </td><td>
      <div class="sdq20-ctrl"><input id="item10" type="range" min="1" max="5" step="1" value="1"><output for="item10" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">11</td><td>
      我会一阵子听不见（好像耳聋）。
    </td><td>
      <div class="sdq20-ctrl"><input id="item11" type="range" min="1" max="5" step="1" value="1"><output for="item11" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">12</td><td>
      我会一阵子看不见（好像失明）。
    </td><td>
      <div class="sdq20-ctrl"><input id="item12" type="range" min="1" max="5" step="1" value="1"><output for="item12" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">13</td><td>
      我看到周围事物与平常不同（例如像通过隧道看，或只能看到物体的一部分）。
    </td><td>
      <div class="sdq20-ctrl"><input id="item13" type="range" min="1" max="5" step="1" value="1"><output for="item13" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">14</td><td>
      我的嗅觉比平常好很多或差很多（即使没有感冒）。
    </td><td>
      <div class="sdq20-ctrl"><input id="item14" type="range" min="1" max="5" step="1" value="1"><output for="item14" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">15</td><td>
      感觉我的身体或某一部位好像消失了。
    </td><td>
      <div class="sdq20-ctrl"><input id="item15" type="range" min="1" max="5" step="1" value="1"><output for="item15" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">16</td><td>
      我不能吞咽，或只能费很大力气才能吞咽。
    </td><td>
      <div class="sdq20-ctrl"><input id="item16" type="range" min="1" max="5" step="1" value="1"><output for="item16" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">17</td><td>
      我连续几晚睡不着，但白天依然很活跃。
    </td><td>
      <div class="sdq20-ctrl"><input id="item17" type="range" min="1" max="5" step="1" value="1"><output for="item17" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">18</td><td>
      我不能说话（或只能费很大力气说话），或者只能耳语。
    </td><td>
      <div class="sdq20-ctrl"><input id="item18" type="range" min="1" max="5" step="1" value="1"><output for="item18" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">19</td><td>
      我会暂时瘫痪一会儿。
    </td><td>
      <div class="sdq20-ctrl"><input id="item19" type="range" min="1" max="5" step="1" value="1"><output for="item19" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>

    <tr class="sdq20-item"><td class="no">20</td><td>
      我会暂时变得僵硬一会儿。
    </td><td>
      <div class="sdq20-ctrl"><input id="item20" type="range" min="1" max="5" step="1" value="1"><output for="item20" class="sdq20-badge" aria-live="polite" aria-label="当前项评分">1</output></div>
    </td></tr>
  </tbody>
</table>

<!-- 结果区域 -->
<div class="sdq20-results" id="sdq20-results">
  <div class="sdq20-section-title">评估结果</div>

  <div>
    <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:.4rem;">
      <strong>总分（SDQ-20）</strong>
      <span style="font-size:1.3rem; font-weight:700; color:var(--md-primary-fg-color);" id="sdq20-score">20</span>
    </div>
    <div class="sdq20-progress" role="progressbar" aria-valuemin="20" aria-valuemax="100" aria-valuenow="20">
      <div class="bar" id="sdq20-bar" style="width:0%"></div>
    </div>
    <div class="sdq20-legend">
      <span>20（最低）</span>
      <span>100（最高）</span>
    </div>
  </div>

  <div class="sdq20-note">
    <strong>解释：</strong><span id="sdq20-level">低躯体解离症状（结合具体困扰评估）</span>
  </div>

  <div class="sdq20-divider"></div>

  <!-- SDQ-5 子集 -->
  <div class="sdq20-subgrid">
    <div class="sdq20-subcard">
      <div class="label">SDQ-5 简化版</div>
      <div class="row">
        <div class="sdq20-progress" style="flex:1;" role="progressbar" aria-valuemin="5" aria-valuemax="25" aria-valuenow="5">
          <div class="bar" id="sdq20-sdq5-bar" style="width:0%"></div>
        </div>
        <output class="sdq20-badge" id="sdq20-sdq5">5</output>
      </div>
      <div class="sdq20-legend">
        <span>5（最低）</span>
        <span>25（最高）</span>
      </div>
      <div class="sdq20-hint" style="margin-top:.5rem;">
        SDQ-5 由题目 4、8、13、15、18 组成，用于快速筛查
      </div>
    </div>
  </div>

  <div class="sdq20-divider"></div>

  <div class="sdq20-note">
    <strong>参考区间</strong>（基于研究文献，仅供参考，非诊断标准）：
  </div>
  <ul class="sdq20-note">
    <li><strong>&ge;50 分</strong>：高度躯体解离症状，常见于 DID（分离性身份障碍）</li>
    <li><strong>40-49 分</strong>：显著躯体解离症状，常见于 DDNOS/OSDD（其他特定/非特定解离障碍）</li>
    <li><strong>30-39 分</strong>：中度躯体解离症状，可能存在解离障碍或其他精神障碍</li>
    <li><strong>&lt;30 分</strong>：较低躯体解离症状，但仍需结合临床评估</li>
  </ul>

  <div class="sdq20-divider"></div>

  <div class="sdq20-note">
    <strong>重要提示：</strong>
  </div>
  <ul class="sdq20-note">
    <li>本量表仅作为初步筛查工具，不能替代专业临床诊断</li>
    <li>躯体解离症状可能与多种因素相关，包括创伤史、解离障碍、转换障碍等</li>
    <li>部分症状可能由躯体疾病引起，务必进行医学检查排除器质性病因</li>
    <li>若评分较高或症状显著影响生活，建议寻求精神科或临床心理专业评估</li>
    <li>原版问卷要求标注"医生是否认为症状由躯体疾病解释"，在线版为简化版</li>
  </ul>
</div>

</div>

## 量表信息

### 开发与信效度

- **原作者**：Nijenhuis, E. R. S., Spinhoven, P., Van Dyck, R., Van der Hart, O., & Vanderlinden, J. (1996)
- **版权**：© 1998 Nijenhuis, Van der Hart & Vanderlinden
- **内部一致性**：Cronbach's α 通常 >0.90
- **结构**：单维度量表，测量躯体解离作为统一构念
- **题目来源**：从 75 个临床观察到的躯体解离症状中筛选出最具区分度的 20 题

### SDQ-5 简化版

SDQ-5 是从 SDQ-20 演化而来的简化版本，由第 **4、8、13、15、18** 题组成：

- 4. 我小便时疼痛
- 8. 我的身体或某一部位对疼痛不敏感
- 13. 我看到周围事物与平常不同
- 15. 感觉我的身体或某一部位好像消失了
- 18. 我不能说话（或只能费很大力气说话），或者只能耳语

SDQ-5 适用于需要快速筛查的场景。

### 临床应用

SDQ-20 主要用于：

1. **解离障碍筛查**：识别可能存在躯体解离症状的个体
2. **创伤评估**：躯体解离常与创伤史相关，尤其是儿童期虐待
3. **鉴别诊断**：帮助区分解离障碍与转换障碍、躯体形式障碍等
4. **治疗监测**：评估治疗过程中躯体解离症状的变化

## 参考文献

1. Nijenhuis, E. R. S., Spinhoven, P., Van Dyck, R., Van der Hart, O., & Vanderlinden, J. (1996). The development and psychometric characteristics of the Somatoform Dissociation Questionnaire (SDQ-20). *Journal of Nervous and Mental Disease*, 184(11), 688-694.

2. Nijenhuis, E. R. S., Spinhoven, P., Van Dyck, R., Van der Hart, O., & Vanderlinden, J. (1998). Degree of somatoform and psychological dissociation in dissociative disorder is correlated with reported trauma. *Journal of Traumatic Stress*, 11(4), 711-730.

3. Nijenhuis, E. R. S. (2000). Somatoform dissociation: Major symptoms of dissociative disorders. *Journal of Trauma & Dissociation*, 1(4), 7-32.

## 相关词条

- [解离性身份障碍 （DID）](DID.md)
- [解离经验量表 （DES-II）](Dissociative-Experiences-Scale-DES-II.md)
- [多维解离量表 （MID-60）](Multidimensional-Inventory-of-Dissociation-MID-60.md)
- [创伤 （Trauma）](Trauma.md)

## 外部链接

- [SDQ-20 官方页面](https://www.enijenhuis.nl/sdq20)（原作者网站）
- [European Society for Trauma and Dissociation （ESTD）](https://www.estd.org/)
