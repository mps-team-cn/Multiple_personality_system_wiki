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

    - 每一道题用滑块选择 0–100%：表示你在日常生活中出现该体验的时间比例。
    - 建议按直觉作答；可在最后点击“计算分数”。

<!-- 样式与脚本由 mkdocs.yml 的 extra_css / extra_javascript 注入 -->

<div id="des2-app" class="des2-app">

<div class="des2-meta">
  <div class="des2-hint">范围 0–100，步长 10（可拖动或方向键微调）</div>
  <div class="des2-actions">
    <button id="des2-calc" class="md-button md-button--primary">计算分数</button>
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
      有时会沉浸在想象/活动中，以至于忽略周围发生的事。
    </td><td>
      <div class="des2-ctrl"><input id="item1" type="range" min="0" max="100" step="10" value="0"><output for="item1" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">2</td><td>
      看电影/阅读/听音乐时，会感觉自己仿佛“置身其中”。
    </td><td>
      <div class="des2-ctrl"><input id="item2" type="range" min="0" max="100" step="10" value="0"><output for="item2" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">3</td><td>
      曾在走神或分心后，发现自己走到了某个地方，却不记得中间过程。
    </td><td>
      <div class="des2-ctrl"><input id="item3" type="range" min="0" max="100" step="10" value="0"><output for="item3" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">4</td><td>
      与人交谈时，突然意识到自己刚才“走神了”，不记得刚刚说了什么。
    </td><td>
      <div class="des2-ctrl"><input id="item4" type="range" min="0" max="100" step="10" value="0"><output for="item4" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">5</td><td>
      日记、文字或其他物品上有自己的笔迹/痕迹，但不记得何时完成。
    </td><td>
      <div class="des2-ctrl"><input id="item5" type="range" min="0" max="100" step="10" value="0"><output for="item5" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">6</td><td>
      有些事情明明熟悉，但一时想不起来自己是否做过/经历过。
    </td><td>
      <div class="des2-ctrl"><input id="item6" type="range" min="0" max="100" step="10" value="0"><output for="item6" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">7</td><td>
      曾有片刻感到“我不像我”或“周围世界不真实/恍惚”。
    </td><td>
      <div class="des2-ctrl"><input id="item7" type="range" min="0" max="100" step="10" value="0"><output for="item7" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">8</td><td>
      照镜子时有一瞬间觉得自己像是“陌生人”。
    </td><td>
      <div class="des2-ctrl"><input id="item8" type="range" min="0" max="100" step="10" value="0"><output for="item8" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">9</td><td>
      阅读时“走神”，回过神来需要回读一段，才意识到没看进去。
    </td><td>
      <div class="des2-ctrl"><input id="item9" type="range" min="0" max="100" step="10" value="0"><output for="item9" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">10</td><td>
      曾突然出现在一个地点，却不清楚/不记得自己怎么到这儿的。
    </td><td>
      <div class="des2-ctrl"><input id="item10" type="range" min="0" max="100" step="10" value="0"><output for="item10" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">11</td><td>
      有时对外界声音/人声“没反应”，像是注意完全沉入内在活动。
    </td><td>
      <div class="des2-ctrl"><input id="item11" type="range" min="0" max="100" step="10" value="0"><output for="item11" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">12</td><td>
      感到自己像在旁观/梦里，身体或环境不真实、遥远或“像电影”。
    </td><td>
      <div class="des2-ctrl"><input id="item12" type="range" min="0" max="100" step="10" value="0"><output for="item12" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">13</td><td>
      发现随身物品被移动/出现，但不记得自己放置或取得过它们。
    </td><td>
      <div class="des2-ctrl"><input id="item13" type="range" min="0" max="100" step="10" value="0"><output for="item13" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">14</td><td>
      被音乐/自然/艺术等深深吸引，注意力长时间沉浸其中。
    </td><td>
      <div class="des2-ctrl"><input id="item14" type="range" min="0" max="100" step="10" value="0"><output for="item14" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">15</td><td>
      开车/通勤时“到点了才回神”，对途中细节记忆很少或断续。
    </td><td>
      <div class="des2-ctrl"><input id="item15" type="range" min="0" max="100" step="10" value="0"><output for="item15" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">16</td><td>
      别人提起某段对话/事件时，你几乎没有印象或完全不记得。
    </td><td>
      <div class="des2-ctrl"><input id="item16" type="range" min="0" max="100" step="10" value="0"><output for="item16" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">17</td><td>
      情绪或场景很投入时，会忘记时间流逝，像“短暂消失在世界外”。
    </td><td>
      <div class="des2-ctrl"><input id="item17" type="range" min="0" max="100" step="10" value="0"><output for="item17" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">18</td><td>
      回忆时会出现非常生动的画面/声音/触感，仿佛重新“经历了一遍”。
    </td><td>
      <div class="des2-ctrl"><input id="item18" type="range" min="0" max="100" step="10" value="0"><output for="item18" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">19</td><td>
      在熟悉地点一时间“认不出来”或感觉格外陌生/与以往不同。
    </td><td>
      <div class="des2-ctrl"><input id="item19" type="range" min="0" max="100" step="10" value="0"><output for="item19" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">20</td><td>
      专注做事/创作时进入“心流”，对外界刺激反应明显下降。
    </td><td>
      <div class="des2-ctrl"><input id="item20" type="range" min="0" max="100" step="10" value="0"><output for="item20" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">21</td><td>
      经常做白日梦/内在想象延展，沉浸其中难以立即抽离。
    </td><td>
      <div class="des2-ctrl"><input id="item21" type="range" min="0" max="100" step="10" value="0"><output for="item21" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">22</td><td>
      听到别人说话，偶尔会像“从远处传来”，自己像在“隔层之外”。
    </td><td>
      <div class="des2-ctrl"><input id="item22" type="range" min="0" max="100" step="10" value="0"><output for="item22" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">23</td><td>
      发现自己拥有某些物品/消费记录，但完全不记得获得/下单过。
    </td><td>
      <div class="des2-ctrl"><input id="item23" type="range" min="0" max="100" step="10" value="0"><output for="item23" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">24</td><td>
      他人告诉你：你曾做/说过某些事，但你对那段经历毫无印象。
    </td><td>
      <div class="des2-ctrl"><input id="item24" type="range" min="0" max="100" step="10" value="0"><output for="item24" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">25</td><td>
      情绪或生理高压下，感觉自己“像不在身体里”或“在旁边看着自己”。
    </td><td>
      <div class="des2-ctrl"><input id="item25" type="range" min="0" max="100" step="10" value="0"><output for="item25" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">26</td><td>
      在群体/场合中，短暂觉得他人或环境像“舞台布景/模糊不真实”。
    </td><td>
      <div class="des2-ctrl"><input id="item26" type="range" min="0" max="100" step="10" value="0"><output for="item26" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">27</td><td>
      聆听音乐/故事时，脑中出现“如临其境”的画面与情节延展。
    </td><td>
      <div class="des2-ctrl"><input id="item27" type="range" min="0" max="100" step="10" value="0"><output for="item27" class="des2-badge">0</output>%</div>
    </td></tr>

    <tr class="des2-item"><td class="no">28</td><td>
      回想童年/过去的你，偶尔感觉那像“另一个人”的人生经历。
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

!!! info "分数解释（简要）"

    - 0–9：低范围 —— 可结合当前困扰、睡眠/药物/应激因素等综合判断。
    - 10–19：轻度 —— 建议持续自我观察，必要时咨询专业人士。
    - 20–29：中等 —— 建议进行进一步临床评估与功能影响讨论。
    - ≥ 30：较高 —— 建议尽快寻求专业评估（分数仅作筛查，不等同诊断）。

!!! note "子量表与算法说明（依据通用做法/NovoPsych 公示资料）"

    - 总分：28 题取平均（0–100）
    - 子量表（各 6 题，均为平均分）：
        - 记忆缺失（Amnesia）：3、4、5、8、25、26
        - 人格/现实解体（DP/DR）：7、11、12、13、27、28
        - 沉浸吸收（Absorption）：2、14、15、17、18、20
    - 注：分数仅作筛查用途，解释需结合情境、痛苦程度与功能受损。

!!! quote "参考"
    Bernstein EM, Putnam FW. Development, reliability, and validity of a dissociation scale. J Nerv Ment Dis. 1986.
