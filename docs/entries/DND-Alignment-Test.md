---
title: D&D 阵营测试（Dungeons & Dragons Alignment Test）
tags:

  - culture:D&D阵营
  - culture:桌面角色扮演游戏（TRPG）

topic: 文化与表现
synonyms:

  - D&D 阵营测试
  - DnD 阵营测试
  - 九宫格阵营测试
  - Dungeons & Dragons Alignment Test

description: D&D 九宫格阵营测试中文交互版，通过 36 道角色扮演情境题，从守序—混乱与善良—邪恶两条轴线生成阵营结果和详细得分。
updated: 2026-08-26
extra_css:

  - assets/dnd-alignment-test.css

extra_javascript:

  - assets/dnd-alignment-test.js

comments: true
---

# D&D 阵营测试（Dungeons & Dragons Alignment Test）

!!! info "娱乐性角色扮演工具"
    本测试用于 **D&D 角色塑造、内部成员自我表达和轻量讨论**，不是心理测验，也不能用于判断人格、诊断、危险性或道德品质。“邪恶”是 D&D 阵营系统中的游戏术语，不等于现实中的坏人。

## 使用说明

- 共 36 题，分为家庭、朋友、集体、国家、刑罚与财富六组情境。
- 请以某个角色、某位系统成员或整个系统的共同立场作答；同一轮测试中尽量保持视角一致。
- 每题只能选择一个最接近的选项。全部完成后点击“生成阵营报告”。
- 所有计算均在当前浏览器内完成，页面不会上传或保存答案。

<div id="dnd-alignment-app" class="dnd-alignment-app">
  <div class="dnd-alignment-toolbar">
    <label class="dnd-alignment-name" for="dnd-alignment-respondent">
      <span>作答者或角色名（可选）</span>
      <input id="dnd-alignment-respondent" type="text" maxlength="40" placeholder="例如：整个系统、成员 A、跑团角色名">
    </label>
    <div class="dnd-alignment-progress" aria-live="polite">
      <span id="dnd-alignment-progress-text">已完成 0 / 36</span>
      <div class="dnd-alignment-progress-track" role="progressbar" aria-valuemin="0" aria-valuemax="36" aria-valuenow="0">
        <div id="dnd-alignment-progress-bar" class="dnd-alignment-progress-bar"></div>
      </div>
    </div>
  </div>

  <form id="dnd-alignment-form" novalidate>
    <div id="dnd-alignment-questions"></div>
    <div id="dnd-alignment-error" class="dnd-alignment-error" role="alert" hidden></div>
    <div class="dnd-alignment-actions">
      <button class="md-button md-button--primary" type="submit">生成阵营报告</button>
      <button id="dnd-alignment-reset" class="md-button" type="button">重置</button>
    </div>
  </form>

  <section id="dnd-alignment-result" class="dnd-alignment-result" aria-live="polite" tabindex="-1" hidden>
    <div class="dnd-alignment-result-heading">
      <div>
        <div class="dnd-alignment-eyebrow">阵营测试结果</div>
        <h2 id="dnd-alignment-result-title">尚未生成</h2>
        <p id="dnd-alignment-result-subtitle" class="dnd-alignment-result-subtitle"></p>
      </div>
      <button id="dnd-alignment-copy" class="md-button" type="button">复制结果</button>
    </div>
    <p id="dnd-alignment-result-description"></p>

    <div class="dnd-alignment-axis-grid">
      <div class="dnd-alignment-axis-card">
        <h3>秩序轴</h3>
        <div id="dnd-alignment-order-scores"></div>
      </div>
      <div class="dnd-alignment-axis-card">
        <h3>道德轴</h3>
        <div id="dnd-alignment-moral-scores"></div>
      </div>
    </div>

    <h3>九阵营详细得分</h3>
    <div id="dnd-alignment-grid" class="dnd-alignment-grid" aria-label="九阵营得分表"></div>
    <p class="dnd-alignment-result-note">分数只反映这轮答案在本测试规则下的相对倾向。若多个方向接近，可把结果理解为边界位置，而非固定标签。</p>
  </section>
</div>

<noscript>
此互动测试需要启用 JavaScript 才能显示题目并计算结果。
</noscript>

## 在系统内使用

同一系统的不同成员可以分别测试并记录作答视角，再比较彼此在“规则与自主”“照顾他人与自我保护”等情境中的偏好。差异本身不代表冲突或优劣，更适合用作内部沟通的开场问题。

!!! warning "避免过度解释"
    阵营结果不能证明某位成员的身份真实性，也不代表稳定的人格结构。情境题的选项有限，现实决策还会受到安全、能力、关系和信息条件影响。

## 计分方法

每个选项为守序、秩序中立、混乱、善良、道德中立或邪恶方向增加 `1–2` 分。结果页会根据题库动态计算各方向满分并按比例显示得分条；当前道德中立的满分为 `23` 分，其余五个方向均为 `24` 分。

最终阵营沿用经典测试的两轴判定：先分别比较守序／秩序中立／混乱与善良／道德中立／邪恶，再组合成九宫格结果。单独最高时正常采用该方向；中立与单侧精确并列、两个极端精确并列且中立更低、三方完全同分时，为兼容九宫格均以中立作为 canonical 轴向，但结果页会分别标记“边界”“特殊平局”或“无明显单一倾向”，并自动列出所有并列方向组合成的候选阵营。两个轴同时并列时会保留全部组合，不会只显示其中一个轴的边界。九阵营详细得分仅用于展示各组合的相对分数，不参与最终阵营竞争；相近但未同分的分数不按边界处理。

## 来源与许可

1. [《Hero Builder's Guidebook》在线阅览](https://anyflip.com/kpthp/ftnf/basic/51-72)：Wizards of the Coast 于 2000 年出版，ISBN `978-0-7869-1647-4`；书中 “Selecting an Alignment”（书页 51–54）是 36 道测试题、各选项计分及两轴判定规则的原始依据。
2. [PA D&D：What D&D Alignment Is Your PC?](https://www.padnd.com/alignment_test2.php)：36 道题目及选项的英文网页版本；本页中文题目据此重新翻译。
3. [BUG 研发中心：官方版 DnD 阵营测试](https://unnamed42.github.io/2016-06-30-%E5%AE%98%E6%96%B9%E7%89%88DnD%E9%98%B5%E8%90%A5%E6%B5%8B%E8%AF%95.html)及[其公开源码](https://github.com/unnamed42/unnamed42.github.io/blob/master/2016-06-30-%E5%AE%98%E6%96%B9%E7%89%88DnD%E9%98%B5%E8%90%A5%E6%B5%8B%E8%AF%95.html)：作为既有中文实现的交叉参考；计分有出入时以原书为准。
4. 测试题与计分沿用经典 D&D 36 题阵营测试，阵营释义参考 D&D 2024（5R）；本页不是“D&D 5R 官方阵营测试”。
5. 本页重新实现交互、无障碍提示和结果展示；相关实现依参考页面标示的 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.zh-hans) 许可共享。

“Dungeons & Dragons”及相关名称归其权利人所有；本页面与 Wizards of the Coast 无隶属或背书关系。
