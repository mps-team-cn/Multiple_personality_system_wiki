---
title: 解离经验量表（DES‑II）
topic: 诊断与临床
tags:

    - 诊断与临床
    - 解离
    - 量表
    - DES
    - DES-II

hide:
  # - navigation  # 隐藏左侧导航栏

    - toc         # 隐藏右侧目录（可选，如果也想隐藏右侧

updated: 2025-10-18
search:
  boost: 1.5
---

# 解离经验量表（DES‑II）

!!! warning "重要声明"
    本工具仅作教育与自我筛查参考，**不构成临床诊断**。若分数较高且合并显著痛苦/功能受损，请尽快咨询精神科/临床心理专业人士。

!!! tip "使用说明"

    - 每一道题用滑块选择 0–100%：表示在日常生活中出现该体验的时间比例。
    - 建议按直觉作答；尽量不要反复修改，以首次直觉为准。可在最后点击“计算分数”。

<!-- 样式与脚本由 mkdocs.yml 的 extra_css / extra_javascript 注入 -->

<div id="des2-app" class="des2-app">

<div class="des2-meta">
  <div class="des2-hint">范围 0–100，步长 10（可拖动或方向键微调）</div>
  <div class="des2-actions">
    <!-- <button id="des2-calc" class="md-button md-button--primary">计算分数</button> -->
    <button id="des2-reset" class="md-button">重置</button>
    <!-- <button id="des2-fill-10" class="md-button">示例：全部 10%</button>
    <button id="des2-fill-20" class="md-button">示例：全部 20%</button>
    <button id="des2-fill-30" class="md-button">示例：全部 30%</button> -->
  </div>
</div>

<!-- 结果区域移至题目表之后显示 -->

<div class="des2-divider"></div>

<!-- 题目区域：为避免外部依赖，直接内嵌（中文表述经通俗化处理） -->

<table class="des2-table">
  <colgroup>
    <col style="width:2.2rem">
    <col>
    <col style="width:17rem">
  </colgroup>
  <thead>
    <tr><th>#</th><th>描述</th><th>比例（%）</th></tr>
  </thead>
  <tbody>
    <tr class="des2-item"><td class="no">1</td><td>
      我会沉浸在想法或正在做的事里，以致一时忽略周围正在发生的事情。
    </td><td>
      <div class="des2-ctrl"><input id="item1" type="range" min="0" max="100" step="10" value="0"><output for="item1" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">2</td><td>
      当我看电影、阅读或听音乐时，常会有仿佛身临其境的感觉。
    </td><td>
      <div class="des2-ctrl"><input id="item2" type="range" min="0" max="100" step="10" value="0"><output for="item2" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">3</td><td>
      我曾在走神后发现自己已经到了某处，却不太记得中间的过程。
    </td><td>
      <div class="des2-ctrl"><input id="item3" type="range" min="0" max="100" step="10" value="0"><output for="item3" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">4</td><td>
      与人交谈时，我会突然意识到自己刚才走神了，并不太记得刚刚说了什么。
    </td><td>
      <div class="des2-ctrl"><input id="item4" type="range" min="0" max="100" step="10" value="0"><output for="item4" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">5</td><td>
      我发现有自己写下的字迹或留下的痕迹，但不太记得何时完成。
    </td><td>
      <div class="des2-ctrl"><input id="item5" type="range" min="0" max="100" step="10" value="0"><output for="item5" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">6</td><td>
      我会对一些事情感到很熟悉，却一时想不起自己是否真的做过或经历过。
    </td><td>
      <div class="des2-ctrl"><input id="item6" type="range" min="0" max="100" step="10" value="0"><output for="item6" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">7</td><td>
      我有过片刻觉得自己不像自己，或周围世界不真实的体验。
    </td><td>
      <div class="des2-ctrl"><input id="item7" type="range" min="0" max="100" step="10" value="0"><output for="item7" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">8</td><td>
      照镜子时，我曾短暂觉得镜中的自己像个陌生人。
    </td><td>
      <div class="des2-ctrl"><input id="item8" type="range" min="0" max="100" step="10" value="0"><output for="item8" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">9</td><td>
      阅读时我会走神，回过神来需要回读一段才发现没看进去。
    </td><td>
      <div class="des2-ctrl"><input id="item9" type="range" min="0" max="100" step="10" value="0"><output for="item9" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">10</td><td>
      我曾突然意识到自己已经在某个地点，却对如何到达那儿记不清。
    </td><td>
      <div class="des2-ctrl"><input id="item10" type="range" min="0" max="100" step="10" value="0"><output for="item10" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">11</td><td>
      我会深度专注于内在活动或手头的事，以至一时对外界声音反应很少。
    </td><td>
      <div class="des2-ctrl"><input id="item11" type="range" min="0" max="100" step="10" value="0"><output for="item11" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">12</td><td>
      我会有像在旁观或在梦里的感觉，身体或环境显得不真实或疏离。
    </td><td>
      <div class="des2-ctrl"><input id="item12" type="range" min="0" max="100" step="10" value="0"><output for="item12" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">13</td><td>
      我发现随身物品被移动或出现，但不太记得自己曾放置或拿取它们。
    </td><td>
      <div class="des2-ctrl"><input id="item13" type="range" min="0" max="100" step="10" value="0"><output for="item13" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">14</td><td>
      我会被音乐、自然或艺术深深吸引，注意力长时间沉浸其中。
    </td><td>
      <div class="des2-ctrl"><input id="item14" type="range" min="0" max="100" step="10" value="0"><output for="item14" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">15</td><td>
      开车或通勤时，我会“回过神来才到站”，对途中细节记忆很少。
    </td><td>
      <div class="des2-ctrl"><input id="item15" type="range" min="0" max="100" step="10" value="0"><output for="item15" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">16</td><td>
      当他人提起某次谈话或事件时，我几乎没有印象或完全想不起来。
    </td><td>
      <div class="des2-ctrl"><input id="item16" type="range" min="0" max="100" step="10" value="0"><output for="item16" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">17</td><td>
      当我情绪或场景投入时，会明显忘记时间的流逝。
    </td><td>
      <div class="des2-ctrl"><input id="item17" type="range" min="0" max="100" step="10" value="0"><output for="item17" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">18</td><td>
      回忆时我会出现非常生动的画面或感觉，像重新经历了一遍。
    </td><td>
      <div class="des2-ctrl"><input id="item18" type="range" min="0" max="100" step="10" value="0"><output for="item18" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">19</td><td>
      在熟悉的地方，我有时会突然感觉格外陌生或与以往不同。
    </td><td>
      <div class="des2-ctrl"><input id="item19" type="range" min="0" max="100" step="10" value="0"><output for="item19" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">20</td><td>
      当我专注或创作时，会进入心流，对外界刺激的反应明显减少。
    </td><td>
      <div class="des2-ctrl"><input id="item20" type="range" min="0" max="100" step="10" value="0"><output for="item20" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">21</td><td>
      我经常进行白日梦或内在想象，沉浸其中后不易立刻抽离。
    </td><td>
      <div class="des2-ctrl"><input id="item21" type="range" min="0" max="100" step="10" value="0"><output for="item21" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">22</td><td>
      我有时会觉得别人说话像从远处传来，自己像隔着一层。
    </td><td>
      <div class="des2-ctrl"><input id="item22" type="range" min="0" max="100" step="10" value="0"><output for="item22" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">23</td><td>
      我发现自己拥有某些物品或消费记录，但完全不记得获取或下单。
    </td><td>
      <div class="des2-ctrl"><input id="item23" type="range" min="0" max="100" step="10" value="0"><output for="item23" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">24</td><td>
      他人告诉我曾做过或说过一些事，但我对那段经历毫无印象。
    </td><td>
      <div class="des2-ctrl"><input id="item24" type="range" min="0" max="100" step="10" value="0"><output for="item24" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">25</td><td>
      在强烈情绪或压力下，我会出现记忆空白或片段不连贯。
    </td><td>
      <div class="des2-ctrl"><input id="item25" type="range" min="0" max="100" step="10" value="0"><output for="item25" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">26</td><td>
      在社交场合或活动中，我有时对发生过的片段记不清或想不起来。
    </td><td>
      <div class="des2-ctrl"><input id="item26" type="range" min="0" max="100" step="10" value="0"><output for="item26" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">27</td><td>
      聆听音乐或故事时，我的脑中会自发浮现如临其境的画面与情节。
    </td><td>
      <div class="des2-ctrl"><input id="item27" type="range" min="0" max="100" step="10" value="0"><output for="item27" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">28</td><td>
      回想过去的自己时，我偶尔会有像在回看另一个人的生活的感觉。
    </td><td>
      <div class="des2-ctrl"><input id="item28" type="range" min="0" max="100" step="10" value="0"><output for="item28" class="des2-badge">0</output>%</div>
    </td></tr>
  </tbody>
</table>

<div class="des2-divider"></div>

<div id="des2-results" class="des2-results">
  <div><strong>总均分</strong>：<span id="des2-avg" class="des2-badge">0.0</span> / 100</div>
  <div class="des2-progress" aria-label="DES-II 平均分可视化">
    <div id="des2-bar" class="bar" style="width:0%"></div>
  </div>
  <div class="des2-legend"><span>0</span><span>10</span><span>20</span><span>30</span><span>50</span><span>100</span></div>
  <div class="des2-note">参考解读：<span id="des2-level">低（仍需结合具体困扰与功能评估）</span></div>

  <div class="des2-divider"></div>
  <div class="des2-subgrid">
    <div class="des2-subcard">
      <div class="label">记忆缺失（Amnesia）</div>
      <div class="row"><span class="des2-badge" id="des2-amn-val">0.0</span></div>
      <div class="des2-progress" aria-label="Amnesia 子量表">
        <div id="des2-amn-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
    <div class="des2-subcard">
      <div class="label">人格/现实解体（DP/DR）</div>
      <div class="row"><span class="des2-badge" id="des2-dpdr-val">0.0</span></div>
      <div class="des2-progress" aria-label="DP/DR 子量表">
        <div id="des2-dpdr-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
    <div class="des2-subcard">
      <div class="label">沉浸吸收（Absorption）</div>
      <div class="row"><span class="des2-badge" id="des2-abs-val">0.0</span></div>
      <div class="des2-progress" aria-label="Absorption 子量表">
        <div id="des2-abs-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>
</div>

<!-- 说明块已按需移除，保留纯交互结果区域 -->

</div>

!!! info "分数解释（与 NovoPsych 一致，筛查用途）"

    0–11 低 · 12–19 轻度 · 20–29 中度 · 30–45 高 · ≥46 极高。

    分数需要结合具体困扰与功能受损讨论；高分并不等同诊断，低分亦不排除个别情境下的显著困扰。

!!! note "子量表与算法说明（依据通用做法/NovoPsych 公示资料）"

    - 总分：28 题取平均（0–100）
    - 子量表（各 6 题，均为平均分）：
        - 记忆缺失（Amnesia）：3、4、5、8、25、26
        - 人格/现实解体（DP/DR）：7、11、12、13、27、28
        - 沉浸吸收（Absorption）：2、14、15、17、18、20
    - 注：分数仅作筛查用途，解释需结合情境、痛苦程度与功能受损。

!!! quote "参考"
    Bernstein EM, Putnam FW. Development, reliability, and validity of a dissociation scale. J Nerv Ment Dis. 1986.
