---
title: 症状自评量表修订版（Symptom Checklist-90-Revised, SCL-90-R）
tags:
  - scale:SCL-90-R
  - scale:评估量表
  - guide:诊断与临床
topic: 诊断与临床
synonyms:
  - 症状自评量表
  - SCL-90
  - SCL90
  - SCL-90-R
  - Symptom Checklist-90
  - Symptom Checklist-90-Revised
description: 症状自评量表修订版（SCL-90-R）是一个广泛使用的心理健康筛查工具，采用0-4分评分系统，评估躯体化、强迫、人际敏感、抑郁、焦虑、敌对、恐怖、偏执和精神病性等九个症状维度，用于心理症状的全面筛查与评估。本版本为国际通用的SCL-90-R版本，与中国常模版本在评分系统和题目分配上有所差异。
updated: 2025-10-26
search:
  boost: 1.5
hide:
  - toc
comments: true
---

# 症状自评量表修订版（Symptom Checklist-90-Revised, SCL-90-R）

!!! danger "重要声明"
    本量表仅用于教育与自我筛查，**不构成临床诊断**。若分数较高且伴随明显心理症状，请及时寻求精神科或临床心理专业评估。本量表不能替代专业的临床诊断。

!!! warning "危机求助资源"
    **若您正在经历自杀想法、自伤冲动或伤害他人的念头，请立即寻求帮助：**

    - **全国24小时心理援助热线**：400-161-9995 / 010-82951332
    - **北京心理危机研究与干预中心**：010-82951332
    - **上海心理援助热线**：021-962525 / 021-12320-5
    - **广州心理危机干预中心**：020-81899120
    - **深圳心理危机干预热线**：0755-25629459
    - **紧急情况请拨打急救电话 120 或直接前往最近的医院急诊科**

    您的生命很宝贵，专业帮助随时可得。

## 概述

**症状自评量表修订版（SCL-90-R）** 由 Derogatis 于 1977 年在原始 SCL-90（1975）基础上修订而成，是目前国际上使用最广泛的心理健康筛查量表之一。量表包含 90 个项目，评估个体在过去一周内的心理症状体验，涵盖九个症状维度：

- **躯体化（Somatization）**：以躯体不适表达心理痛苦的倾向
- **强迫症状（Obsessive-Compulsive）**：强迫思维与强迫行为
- **人际敏感（Interpersonal Sensitivity）**：人际交往中的不适感与自卑感
- **抑郁（Depression）**：抑郁情绪与相关症状
- **焦虑（Anxiety）**：焦虑情绪与躯体焦虑表现
- **敌对（Hostility）**：愤怒、攻击性与敌意
- **恐怖（Phobic Anxiety）**：对特定情境的恐惧反应
- **偏执（Paranoid Ideation）**：多疑、被害感与关系妄想倾向
- **精神病性（Psychoticism）**：孤独、精神病性症状倾向

量表计算三个总体指标：

- **总体严重指数（Global Severity Index, GSI）**：所有90项的平均分，是最重要的总体指标
- **阳性项目数（Positive Symptom Total, PST）**：评分 ≥ 1 分的项目数
- **阳性症状均分（Positive Symptom Distress Index, PSDI）**：阳性项目的平均分

此外还计算**总分（Total Score）**作为辅助参考（90项得分之和）

!!! info "版本说明"
    **本词条采用 SCL-90-R（修订版）标准**，使用 **0-4 分评分系统**。中国常模版本（王征宇，1984）采用 1-5 分评分系统，且部分维度的题目分配有所不同。如需使用中国常模进行临床解释，请参考相应的评分标准和常模数据。

## 评分说明

!!! tip "使用说明"

    - 每题采用 **0-4 分** 五级评分（SCL-90-R 标准）：
        - **0 = 没有（NOT AT ALL）**
        - **1 = 很轻（A LITTLE BIT）**
        - **2 = 中等（MODERATELY）**
        - **3 = 偏重（QUITE A BIT）**
        - **4 = 严重（EXTREMELY）**
    - 请根据 **过去一周（包括今天）** 的实际体验作答
    - 建议按直觉作答，尽量不要反复修改
    - 完成所有题目后，系统将自动计算各维度分数

## 在线评估

<!-- 样式与脚本由 mkdocs.yml 的 extra_css / extra_javascript 注入 -->

<div id="scl90-app" class="scl90-app">

<div class="scl90-meta">
  <div class="scl90-hint">评分范围 0–4（0=没有，4=严重）· SCL-90-R 标准</div>
  <div class="scl90-actions">
    <button id="scl90-reset" class="md-button">重置</button>
  </div>
</div>

<div class="scl90-divider"></div>

<!-- 题目区域 -->
<table class="scl90-table">
  <caption>SCL-90 题目与评分</caption>
  <colgroup>
    <col style="width:2.2rem">
    <col>
    <col style="width:15rem">
  </colgroup>
  <thead>
    <tr><th scope="col">#</th><th scope="col">症状描述（过去一周的体验）</th><th scope="col">评分（0-4）</th></tr>
  </thead>
  <tbody>
    <tr class="scl90-item"><td class="no">1</td><td>
      头痛
    </td><td>
      <div class="scl90-ctrl"><input id="item1" type="range" min="0" max="4" step="1" value="0"><output for="item1" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">2</td><td>
      神经过敏，心中不踏实
    </td><td>
      <div class="scl90-ctrl"><input id="item2" type="range" min="0" max="4" step="1" value="0"><output for="item2" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">3</td><td>
      头脑中有不必要的想法或字句盘旋
    </td><td>
      <div class="scl90-ctrl"><input id="item3" type="range" min="0" max="4" step="1" value="0"><output for="item3" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">4</td><td>
      头昏或昏倒
    </td><td>
      <div class="scl90-ctrl"><input id="item4" type="range" min="0" max="4" step="1" value="0"><output for="item4" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">5</td><td>
      对异性的兴趣减退
    </td><td>
      <div class="scl90-ctrl"><input id="item5" type="range" min="0" max="4" step="1" value="0"><output for="item5" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">6</td><td>
      对旁人责备求全
    </td><td>
      <div class="scl90-ctrl"><input id="item6" type="range" min="0" max="4" step="1" value="0"><output for="item6" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">7</td><td>
      感到别人能控制您的思想
    </td><td>
      <div class="scl90-ctrl"><input id="item7" type="range" min="0" max="4" step="1" value="0"><output for="item7" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">8</td><td>
      责怪别人制造麻烦
    </td><td>
      <div class="scl90-ctrl"><input id="item8" type="range" min="0" max="4" step="1" value="0"><output for="item8" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">9</td><td>
      忘记性大
    </td><td>
      <div class="scl90-ctrl"><input id="item9" type="range" min="0" max="4" step="1" value="0"><output for="item9" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">10</td><td>
      担心自己的衣饰整齐及仪态的端正
    </td><td>
      <div class="scl90-ctrl"><input id="item10" type="range" min="0" max="4" step="1" value="0"><output for="item10" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">11</td><td>
      容易烦恼和激动
    </td><td>
      <div class="scl90-ctrl"><input id="item11" type="range" min="0" max="4" step="1" value="0"><output for="item11" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">12</td><td>
      胸痛
    </td><td>
      <div class="scl90-ctrl"><input id="item12" type="range" min="0" max="4" step="1" value="0"><output for="item12" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">13</td><td>
      害怕空旷的场所或街道
    </td><td>
      <div class="scl90-ctrl"><input id="item13" type="range" min="0" max="4" step="1" value="0"><output for="item13" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">14</td><td>
      感到自己的精力下降，活动减慢
    </td><td>
      <div class="scl90-ctrl"><input id="item14" type="range" min="0" max="4" step="1" value="0"><output for="item14" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">15</td><td>
      想结束自己的生命
    </td><td>
      <div class="scl90-ctrl"><input id="item15" type="range" min="0" max="4" step="1" value="0"><output for="item15" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">16</td><td>
      听到旁人听不到的声音
    </td><td>
      <div class="scl90-ctrl"><input id="item16" type="range" min="0" max="4" step="1" value="0"><output for="item16" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">17</td><td>
      发抖
    </td><td>
      <div class="scl90-ctrl"><input id="item17" type="range" min="0" max="4" step="1" value="0"><output for="item17" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">18</td><td>
      感到大多数人都不可信任
    </td><td>
      <div class="scl90-ctrl"><input id="item18" type="range" min="0" max="4" step="1" value="0"><output for="item18" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">19</td><td>
      胃口不好
    </td><td>
      <div class="scl90-ctrl"><input id="item19" type="range" min="0" max="4" step="1" value="0"><output for="item19" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">20</td><td>
      容易哭泣
    </td><td>
      <div class="scl90-ctrl"><input id="item20" type="range" min="0" max="4" step="1" value="0"><output for="item20" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">21</td><td>
      同异性相处时感到害羞不自在
    </td><td>
      <div class="scl90-ctrl"><input id="item21" type="range" min="0" max="4" step="1" value="0"><output for="item21" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">22</td><td>
      感到受骗，中了圈套或有人想抓住您
    </td><td>
      <div class="scl90-ctrl"><input id="item22" type="range" min="0" max="4" step="1" value="0"><output for="item22" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">23</td><td>
      无缘无故地突然感到害怕
    </td><td>
      <div class="scl90-ctrl"><input id="item23" type="range" min="0" max="4" step="1" value="0"><output for="item23" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">24</td><td>
      自己不能控制地大发脾气
    </td><td>
      <div class="scl90-ctrl"><input id="item24" type="range" min="0" max="4" step="1" value="0"><output for="item24" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">25</td><td>
      怕单独出门
    </td><td>
      <div class="scl90-ctrl"><input id="item25" type="range" min="0" max="4" step="1" value="0"><output for="item25" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">26</td><td>
      经常责怪自己
    </td><td>
      <div class="scl90-ctrl"><input id="item26" type="range" min="0" max="4" step="1" value="0"><output for="item26" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">27</td><td>
      腰痛
    </td><td>
      <div class="scl90-ctrl"><input id="item27" type="range" min="0" max="4" step="1" value="0"><output for="item27" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">28</td><td>
      感到难以完成任务
    </td><td>
      <div class="scl90-ctrl"><input id="item28" type="range" min="0" max="4" step="1" value="0"><output for="item28" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">29</td><td>
      感到孤独
    </td><td>
      <div class="scl90-ctrl"><input id="item29" type="range" min="0" max="4" step="1" value="0"><output for="item29" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">30</td><td>
      感到苦闷
    </td><td>
      <div class="scl90-ctrl"><input id="item30" type="range" min="0" max="4" step="1" value="0"><output for="item30" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">31</td><td>
      过分担忧
    </td><td>
      <div class="scl90-ctrl"><input id="item31" type="range" min="0" max="4" step="1" value="0"><output for="item31" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">32</td><td>
      对事物不感兴趣
    </td><td>
      <div class="scl90-ctrl"><input id="item32" type="range" min="0" max="4" step="1" value="0"><output for="item32" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">33</td><td>
      感到害怕
    </td><td>
      <div class="scl90-ctrl"><input id="item33" type="range" min="0" max="4" step="1" value="0"><output for="item33" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">34</td><td>
      您的感情容易受到伤害
    </td><td>
      <div class="scl90-ctrl"><input id="item34" type="range" min="0" max="4" step="1" value="0"><output for="item34" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">35</td><td>
      旁人能知道您的私下想法
    </td><td>
      <div class="scl90-ctrl"><input id="item35" type="range" min="0" max="4" step="1" value="0"><output for="item35" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">36</td><td>
      感到别人不理解您、不同情您
    </td><td>
      <div class="scl90-ctrl"><input id="item36" type="range" min="0" max="4" step="1" value="0"><output for="item36" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">37</td><td>
      感到人们对您不友好，不喜欢您
    </td><td>
      <div class="scl90-ctrl"><input id="item37" type="range" min="0" max="4" step="1" value="0"><output for="item37" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">38</td><td>
      做事必须做得很慢以保证做得正确
    </td><td>
      <div class="scl90-ctrl"><input id="item38" type="range" min="0" max="4" step="1" value="0"><output for="item38" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">39</td><td>
      心跳得很厉害
    </td><td>
      <div class="scl90-ctrl"><input id="item39" type="range" min="0" max="4" step="1" value="0"><output for="item39" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">40</td><td>
      恶心或胃部不舒服
    </td><td>
      <div class="scl90-ctrl"><input id="item40" type="range" min="0" max="4" step="1" value="0"><output for="item40" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">41</td><td>
      感到比不上他人
    </td><td>
      <div class="scl90-ctrl"><input id="item41" type="range" min="0" max="4" step="1" value="0"><output for="item41" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">42</td><td>
      肌肉酸痛
    </td><td>
      <div class="scl90-ctrl"><input id="item42" type="range" min="0" max="4" step="1" value="0"><output for="item42" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">43</td><td>
      感到有人在监视您、谈论您
    </td><td>
      <div class="scl90-ctrl"><input id="item43" type="range" min="0" max="4" step="1" value="0"><output for="item43" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">44</td><td>
      难以入睡
    </td><td>
      <div class="scl90-ctrl"><input id="item44" type="range" min="0" max="4" step="1" value="0"><output for="item44" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">45</td><td>
      做事必须反复检查
    </td><td>
      <div class="scl90-ctrl"><input id="item45" type="range" min="0" max="4" step="1" value="0"><output for="item45" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">46</td><td>
      难以作出决定
    </td><td>
      <div class="scl90-ctrl"><input id="item46" type="range" min="0" max="4" step="1" value="0"><output for="item46" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">47</td><td>
      怕乘电车、公共汽车、地铁或火车
    </td><td>
      <div class="scl90-ctrl"><input id="item47" type="range" min="0" max="4" step="1" value="0"><output for="item47" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">48</td><td>
      呼吸有困难
    </td><td>
      <div class="scl90-ctrl"><input id="item48" type="range" min="0" max="4" step="1" value="0"><output for="item48" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">49</td><td>
      一阵阵发冷或发热
    </td><td>
      <div class="scl90-ctrl"><input id="item49" type="range" min="0" max="4" step="1" value="0"><output for="item49" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">50</td><td>
      因为感到害怕而避开某些东西、场合或活动
    </td><td>
      <div class="scl90-ctrl"><input id="item50" type="range" min="0" max="4" step="1" value="0"><output for="item50" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">51</td><td>
      脑子变空了
    </td><td>
      <div class="scl90-ctrl"><input id="item51" type="range" min="0" max="4" step="1" value="0"><output for="item51" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">52</td><td>
      身体发麻或刺痛
    </td><td>
      <div class="scl90-ctrl"><input id="item52" type="range" min="0" max="4" step="1" value="0"><output for="item52" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">53</td><td>
      喉咙有梗塞感
    </td><td>
      <div class="scl90-ctrl"><input id="item53" type="range" min="0" max="4" step="1" value="0"><output for="item53" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">54</td><td>
      感到前途没有希望
    </td><td>
      <div class="scl90-ctrl"><input id="item54" type="range" min="0" max="4" step="1" value="0"><output for="item54" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">55</td><td>
      不能集中注意力
    </td><td>
      <div class="scl90-ctrl"><input id="item55" type="range" min="0" max="4" step="1" value="0"><output for="item55" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">56</td><td>
      感到身体的某一部分软弱无力
    </td><td>
      <div class="scl90-ctrl"><input id="item56" type="range" min="0" max="4" step="1" value="0"><output for="item56" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">57</td><td>
      感到紧张或容易紧张
    </td><td>
      <div class="scl90-ctrl"><input id="item57" type="range" min="0" max="4" step="1" value="0"><output for="item57" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">58</td><td>
      感到手或脚发重
    </td><td>
      <div class="scl90-ctrl"><input id="item58" type="range" min="0" max="4" step="1" value="0"><output for="item58" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">59</td><td>
      想到死亡的事
    </td><td>
      <div class="scl90-ctrl"><input id="item59" type="range" min="0" max="4" step="1" value="0"><output for="item59" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">60</td><td>
      吃得太多
    </td><td>
      <div class="scl90-ctrl"><input id="item60" type="range" min="0" max="4" step="1" value="0"><output for="item60" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">61</td><td>
      当别人看着您或谈论您时感到不自在
    </td><td>
      <div class="scl90-ctrl"><input id="item61" type="range" min="0" max="4" step="1" value="0"><output for="item61" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">62</td><td>
      有一些不属于您自己的想法
    </td><td>
      <div class="scl90-ctrl"><input id="item62" type="range" min="0" max="4" step="1" value="0"><output for="item62" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">63</td><td>
      有想打人或伤害他人的冲动
    </td><td>
      <div class="scl90-ctrl"><input id="item63" type="range" min="0" max="4" step="1" value="0"><output for="item63" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">64</td><td>
      醒得太早
    </td><td>
      <div class="scl90-ctrl"><input id="item64" type="range" min="0" max="4" step="1" value="0"><output for="item64" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">65</td><td>
      必须反复洗手、点数或触摸某些东西
    </td><td>
      <div class="scl90-ctrl"><input id="item65" type="range" min="0" max="4" step="1" value="0"><output for="item65" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">66</td><td>
      睡得不稳不深
    </td><td>
      <div class="scl90-ctrl"><input id="item66" type="range" min="0" max="4" step="1" value="0"><output for="item66" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">67</td><td>
      有想摔坏或破坏东西的冲动
    </td><td>
      <div class="scl90-ctrl"><input id="item67" type="range" min="0" max="4" step="1" value="0"><output for="item67" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">68</td><td>
      有一些别人没有的想法
    </td><td>
      <div class="scl90-ctrl"><input id="item68" type="range" min="0" max="4" step="1" value="0"><output for="item68" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">69</td><td>
      感到对别人神经过敏
    </td><td>
      <div class="scl90-ctrl"><input id="item69" type="range" min="0" max="4" step="1" value="0"><output for="item69" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">70</td><td>
      在商店或电影院等人多的地方感到不自在
    </td><td>
      <div class="scl90-ctrl"><input id="item70" type="range" min="0" max="4" step="1" value="0"><output for="item70" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">71</td><td>
      感到任何事情都很困难
    </td><td>
      <div class="scl90-ctrl"><input id="item71" type="range" min="0" max="4" step="1" value="0"><output for="item71" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">72</td><td>
      一阵阵恐惧或惊恐
    </td><td>
      <div class="scl90-ctrl"><input id="item72" type="range" min="0" max="4" step="1" value="0"><output for="item72" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">73</td><td>
      感到在公共场合吃东西很不舒服
    </td><td>
      <div class="scl90-ctrl"><input id="item73" type="range" min="0" max="4" step="1" value="0"><output for="item73" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">74</td><td>
      经常与人争论
    </td><td>
      <div class="scl90-ctrl"><input id="item74" type="range" min="0" max="4" step="1" value="0"><output for="item74" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">75</td><td>
      单独一人时神经很紧张
    </td><td>
      <div class="scl90-ctrl"><input id="item75" type="range" min="0" max="4" step="1" value="0"><output for="item75" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">76</td><td>
      别人对您的成绩没有作出恰当的评价
    </td><td>
      <div class="scl90-ctrl"><input id="item76" type="range" min="0" max="4" step="1" value="0"><output for="item76" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">77</td><td>
      即使和别人在一起也感到孤单
    </td><td>
      <div class="scl90-ctrl"><input id="item77" type="range" min="0" max="4" step="1" value="0"><output for="item77" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">78</td><td>
      感到坐立不安心神不定
    </td><td>
      <div class="scl90-ctrl"><input id="item78" type="range" min="0" max="4" step="1" value="0"><output for="item78" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">79</td><td>
      感到自己没有什么价值
    </td><td>
      <div class="scl90-ctrl"><input id="item79" type="range" min="0" max="4" step="1" value="0"><output for="item79" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">80</td><td>
      感到熟悉的东西变得陌生或不像是真的
    </td><td>
      <div class="scl90-ctrl"><input id="item80" type="range" min="0" max="4" step="1" value="0"><output for="item80" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">81</td><td>
      大叫或摔东西
    </td><td>
      <div class="scl90-ctrl"><input id="item81" type="range" min="0" max="4" step="1" value="0"><output for="item81" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">82</td><td>
      害怕会在公共场合昏倒
    </td><td>
      <div class="scl90-ctrl"><input id="item82" type="range" min="0" max="4" step="1" value="0"><output for="item82" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">83</td><td>
      感到别人想占您的便宜
    </td><td>
      <div class="scl90-ctrl"><input id="item83" type="range" min="0" max="4" step="1" value="0"><output for="item83" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">84</td><td>
      为一些有关性的想法而很苦恼
    </td><td>
      <div class="scl90-ctrl"><input id="item84" type="range" min="0" max="4" step="1" value="0"><output for="item84" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">85</td><td>
      您认为应该因为自己的过错而受到惩罚
    </td><td>
      <div class="scl90-ctrl"><input id="item85" type="range" min="0" max="4" step="1" value="0"><output for="item85" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">86</td><td>
      感到要赶快把事情做完
    </td><td>
      <div class="scl90-ctrl"><input id="item86" type="range" min="0" max="4" step="1" value="0"><output for="item86" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">87</td><td>
      感到自己的身体有严重问题
    </td><td>
      <div class="scl90-ctrl"><input id="item87" type="range" min="0" max="4" step="1" value="0"><output for="item87" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">88</td><td>
      从未感到和其他人很亲近
    </td><td>
      <div class="scl90-ctrl"><input id="item88" type="range" min="0" max="4" step="1" value="0"><output for="item88" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">89</td><td>
      感到自己有罪
    </td><td>
      <div class="scl90-ctrl"><input id="item89" type="range" min="0" max="4" step="1" value="0"><output for="item89" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>

    <tr class="scl90-item"><td class="no">90</td><td>
      感到自己的脑子有毛病
    </td><td>
      <div class="scl90-ctrl"><input id="item90" type="range" min="0" max="4" step="1" value="0"><output for="item90" class="scl90-badge" aria-live="polite" aria-label="当前项评分">0</output></div>
    </td></tr>
  </tbody>
</table>

<div class="scl90-divider"></div>

<!-- 结果区域 -->
<div class="scl90-results" id="scl90-results">
  <div class="scl90-section-title">评估结果</div>

  <!-- 主要指标：GSI -->
  <div>
    <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:.4rem;">
      <strong>总体严重指数（GSI）</strong>
      <span style="font-size:1.3rem; font-weight:700; color:var(--md-primary-fg-color);" id="scl90-gsi">0.00</span>
    </div>
    <div class="scl90-progress" role="progressbar" aria-valuemin="0" aria-valuemax="4" aria-valuenow="0">
      <div class="bar" id="scl90-gsi-bar" style="width:0%"></div>
    </div>
    <div class="scl90-legend">
      <span>0.00（最低）</span>
      <span>4.00（最高）</span>
    </div>
    <div class="scl90-hint">90项的平均分，反映整体心理症状严重程度</div>
  </div>

  <div class="scl90-divider"></div>

  <!-- 总体指标 -->
  <div class="scl90-subgrid">
    <div class="scl90-subcard">
      <div class="label">阳性项目数（PST）</div>
      <div class="row">
        <output class="scl90-badge" id="scl90-pst">0</output>
      </div>
      <div class="scl90-hint">评分 ≥ 1 分的项目数</div>
    </div>
    <div class="scl90-subcard">
      <div class="label">阳性症状均分（PSDI）</div>
      <div class="row">
        <output class="scl90-badge" id="scl90-psdi">0.00</output>
      </div>
      <div class="scl90-hint">阳性项目的平均分</div>
    </div>
    <div class="scl90-subcard">
      <div class="label">总分（辅助参考）</div>
      <div class="row">
        <output class="scl90-badge" id="scl90-total">0</output>
      </div>
      <div class="scl90-hint">所有项目得分之和</div>
    </div>
  </div>

  <div class="scl90-divider"></div>

  <!-- 九个维度 -->
  <div class="scl90-section-title">九个症状维度</div>

  <div class="scl90-dimension">
    <div class="dim-header">
      <strong>躯体化（Somatization）</strong>
      <output class="scl90-badge" id="scl90-som">0.00</output>
    </div>
    <div class="scl90-progress" role="progressbar" aria-valuemin="0" aria-valuemax="4" aria-valuenow="0">
      <div class="bar" id="scl90-som-bar" style="width:0%"></div>
    </div>
    <div class="scl90-hint">12 题：1, 4, 12, 27, 40, 42, 48, 49, 52, 53, 56, 58</div>
  </div>

  <div class="scl90-dimension">
    <div class="dim-header">
      <strong>强迫症状（Obsessive-Compulsive）</strong>
      <output class="scl90-badge" id="scl90-oc">0.00</output>
    </div>
    <div class="scl90-progress" role="progressbar" aria-valuemin="0" aria-valuemax="4" aria-valuenow="0">
      <div class="bar" id="scl90-oc-bar" style="width:0%"></div>
    </div>
    <div class="scl90-hint">10 题：3, 9, 10, 28, 38, 45, 46, 51, 55, 65</div>
  </div>

  <div class="scl90-dimension">
    <div class="dim-header">
      <strong>人际敏感（Interpersonal Sensitivity）</strong>
      <output class="scl90-badge" id="scl90-is">0.00</output>
    </div>
    <div class="scl90-progress" role="progressbar" aria-valuemin="0" aria-valuemax="4" aria-valuenow="0">
      <div class="bar" id="scl90-is-bar" style="width:0%"></div>
    </div>
    <div class="scl90-hint">9 题：6, 21, 34, 36, 37, 41, 61, 69, 73</div>
  </div>

  <div class="scl90-dimension">
    <div class="dim-header">
      <strong>抑郁（Depression）</strong>
      <output class="scl90-badge" id="scl90-dep">0.00</output>
    </div>
    <div class="scl90-progress" role="progressbar" aria-valuemin="0" aria-valuemax="4" aria-valuenow="0">
      <div class="bar" id="scl90-dep-bar" style="width:0%"></div>
    </div>
    <div class="scl90-hint">12 题：5, 14, 20, 22, 26, 29, 30, 31, 32, 54, 71, 79</div>
  </div>

  <div class="scl90-dimension">
    <div class="dim-header">
      <strong>焦虑（Anxiety）</strong>
      <output class="scl90-badge" id="scl90-anx">0.00</output>
    </div>
    <div class="scl90-progress" role="progressbar" aria-valuemin="0" aria-valuemax="4" aria-valuenow="0">
      <div class="bar" id="scl90-anx-bar" style="width:0%"></div>
    </div>
    <div class="scl90-hint">9 题：17, 23, 33, 39, 57, 72, 78, 80, 86</div>
  </div>

  <div class="scl90-dimension">
    <div class="dim-header">
      <strong>敌对（Hostility）</strong>
      <output class="scl90-badge" id="scl90-hos">0.00</output>
    </div>
    <div class="scl90-progress" role="progressbar" aria-valuemin="0" aria-valuemax="4" aria-valuenow="0">
      <div class="bar" id="scl90-hos-bar" style="width:0%"></div>
    </div>
    <div class="scl90-hint">6 题：11, 24, 63, 67, 74, 81</div>
  </div>

  <div class="scl90-dimension">
    <div class="dim-header">
      <strong>恐怖（Phobic Anxiety）</strong>
      <output class="scl90-badge" id="scl90-phob">0.00</output>
    </div>
    <div class="scl90-progress" role="progressbar" aria-valuemin="0" aria-valuemax="4" aria-valuenow="0">
      <div class="bar" id="scl90-phob-bar" style="width:0%"></div>
    </div>
    <div class="scl90-hint">7 题：13, 25, 47, 50, 70, 75, 82</div>
  </div>

  <div class="scl90-dimension">
    <div class="dim-header">
      <strong>偏执（Paranoid Ideation）</strong>
      <output class="scl90-badge" id="scl90-par">0.00</output>
    </div>
    <div class="scl90-progress" role="progressbar" aria-valuemin="0" aria-valuemax="4" aria-valuenow="0">
      <div class="bar" id="scl90-par-bar" style="width:0%"></div>
    </div>
    <div class="scl90-hint">6 题：8, 18, 43, 68, 76, 83</div>
  </div>

  <div class="scl90-dimension">
    <div class="dim-header">
      <strong>精神病性（Psychoticism）</strong>
      <output class="scl90-badge" id="scl90-psy">0.00</output>
    </div>
    <div class="scl90-progress" role="progressbar" aria-valuemin="0" aria-valuemax="4" aria-valuenow="0">
      <div class="bar" id="scl90-psy-bar" style="width:0%"></div>
    </div>
    <div class="scl90-hint">10 题：7, 16, 35, 62, 77, 84, 85, 87, 88, 90</div>
  </div>

  <div class="scl90-divider"></div>

  <div class="scl90-note">
    <strong>示例参考区间</strong>（基于 SCL-90-R，0-4 分制，仅供研究参考，不可作为诊断阈值）：
  </div>
  <ul class="scl90-note">
    <li><strong>GSI ≥ 0.57（男性）/ 0.64（女性）</strong>：可能存在明显心理症状<span style="opacity:.7;font-size:.8em;">（示例区间；基于 Derogatis 等研究）</span></li>
    <li><strong>阳性项目数（PST）</strong>：临床样本平均约 40-50 项<span style="opacity:.7;font-size:.8em;">（示例数据）</span></li>
    <li><strong>阳性症状均分（PSDI）≥ 1.50</strong>：阳性症状程度偏重<span style="opacity:.7;font-size:.8em;">（示例区间）</span></li>
    <li><strong>因子分 ≥ 1.00</strong>：该维度症状可能达到中等程度<span style="opacity:.7;font-size:.8em;">（示例区间）</span></li>
  </ul>
  <div class="scl90-note" style="margin-top:.5rem;padding:.5rem;background:color-mix(in srgb,var(--md-default-fg-color) 5%,transparent);border-radius:.4rem;">
    <strong>⚠️ 阈值使用注意：</strong>SCL-90-R 采用 0-4 分制，与中国常模版本（1-5 分制）的阈值不可直接对照。上述区间基于国际研究数据，实际应用需参考适用的标准化常模或专业解释。不同地区、年代、人群的常模差异较大。
  </div>

  <div class="scl90-note" style="margin-top:.8rem;padding:.6rem;background:color-mix(in srgb,#409eff 8%,transparent);border-left:3px solid #409eff;border-radius:.4rem;">
    <strong>📊 中国常模版本对照：</strong>中国常模（王征宇，1984）采用 1-5 分评分系统，常见阈值为：GSI ≥ 1.78、总分 ≥ 160、阳性项目数 ≥ 43、因子分 ≥ 2.0。部分维度题目分配也与 SCL-90-R 有所不同。如需使用中国常模进行临床解释，请参考相应的评分标准。
  </div>

  <div class="scl90-divider"></div>

  <div class="scl90-note" style="padding:.6rem;background:color-mix(in srgb,#f56c6c 8%,transparent);border-left:3px solid #f56c6c;border-radius:.4rem;">
    <strong>🆘 危机干预提示：</strong>若您在题目 15（想结束自己的生命）、59（想到死亡的事）、63（有想打人或伤害他人的冲动）、67（有想摔坏或破坏东西的冲动）上评分较高（≥3分），或正在经历强烈的自杀/自伤/伤人念头，<strong>请立即寻求专业帮助</strong>：
  </div>
  <ul class="scl90-note" style="margin-top:.3rem;">
    <li><strong>全国24小时心理援助热线</strong>：400-161-9995 / 010-82951332</li>
    <li><strong>紧急情况请拨打 120 或直接前往最近的医院急诊科</strong></li>
  </ul>

  <div class="scl90-divider"></div>

  <div class="scl90-note">
    <strong>重要提示：</strong>
  </div>
  <ul class="scl90-note">
    <li>本量表仅作为初步筛查工具，不能替代专业临床诊断</li>
    <li>SCL-90 是症状学量表，高分提示心理困扰，但不能直接诊断精神障碍</li>
    <li>若评分较高或症状显著影响生活，建议寻求精神科或临床心理专业评估</li>
    <li>不同研究和地区的常模可能有所差异，解释需结合具体情况</li>
    <li>本在线版为教育用途，临床使用请采用标准化纸笔版或专业软件</li>
  </ul>
</div>

</div>

## 量表信息

### 开发与信效度

- **原作者**：Derogatis, L. R. (1975)
- **修订版本**：SCL-90-R (1977)
- **内部一致性**：各因子 Cronbach's α 在 0.77-0.90 之间
- **重测信度**：0.78-0.90（一周间隔）
- **中国常模**：由王征宇等于 1984 年引入并建立常模

### 量表结构

SCL-90-R 包含九个症状维度，每个维度包含若干题目：

1. **躯体化（12 题）**：题目 1, 4, 12, 27, 40, 42, 48, 49, 52, 53, 56, 58
2. **强迫症状（10 题）**：题目 3, 9, 10, 28, 38, 45, 46, 51, 55, 65
3. **人际敏感（9 题）**：题目 6, 21, 34, 36, 37, 41, 61, 69, 73
4. **抑郁（12 题）**：题目 5, 14, 20, 22, 26, 29, 30, 31, 32, 54, 71, 79
5. **焦虑（9 题）**：题目 17, 23, 33, 39, 57, 72, 78, 80, 86
6. **敌对（6 题）**：题目 11, 24, 63, 67, 74, 81
7. **恐怖（7 题）**：题目 13, 25, 47, 50, 70, 75, 82
8. **偏执（6 题）**：题目 8, 18, 43, 68, 76, 83
9. **精神病性（10 题）**：题目 7, 16, 35, 62, 77, 84, 85, 87, 88, 90
10. **其他项目（7 题）**：题目 19, 44, 59, 60, 64, 66, 89（不计入九个因子，仅计入总分和 GSI）

!!! info "版本差异说明"
    **中国常模版本**（王征宇，1984）的维度题目分配有所不同：

    - 人际敏感包含题目 21, 34, 36, 37, 41, 61, 69, 73, 76（含76）
    - 抑郁包含题目 14, 15, 20, 26, 29, 30, 32, 54, 59, 64, 71, 79, 89（13题）
    - 焦虑包含题目 2, 17, 23, 33, 39, 57, 72, 78, 80, 86（含2）
    - 敌对包含题目 6, 11, 24, 63, 67, 74（含6，不含81）

    请根据所用评分系统选择相应的题目分配。

### 计分方法

1. **因子分**：各维度所含题目得分的平均值
2. **总分**：90 个项目得分之和
3. **阳性项目数（PST）**：评分 ≥ 2 分的项目总数
4. **阳性症状均分（PSDI）**：阳性项目得分总和 ÷ 阳性项目数

### 临床应用

SCL-90 主要用于：

1. **心理健康筛查**：识别可能存在心理困扰的个体
2. **症状评估**：评估心理症状的严重程度和分布
3. **治疗监测**：评估治疗过程中症状的变化
4. **流行病学调查**：大规模心理健康状况调查

## 参考文献

1. Derogatis, L. R. (1975). The SCL-90-R. Clinical Psychometric Research.

2. Derogatis, L. R., & Cleary, P. A. (1977). Confirmation of the dimensional structure of the SCL-90: A study in construct validation. *Journal of Clinical Psychology*, 33(4), 981-989.

3. 王征宇, 迟玉芬, 张作记 (1984). 症状自评量表（SCL-90）. *上海精神医学*, 2(2), 68-70.

4. 汪向东, 王希林, 马弘 (1999). 心理卫生评定量表手册（增订版）. 中国心理卫生杂志社.

## 相关词条

- [DSM-5-TR 评估量表总览](DSM-5TR-Scales.md)
- [解离经验量表（DES-II）](Dissociative-Experiences-Scale-DES-II.md)
- [躯体形式解离问卷（SDQ-20）](Somatoform-Dissociation-Questionnaire-SDQ-20.md)
- [多维解离量表（MID-60）](Multidimensional-Inventory-of-Dissociation-MID-60.md)
- [抑郁障碍（Depressive Disorders）](Depressive-Disorders.md)
- [焦虑障碍（Anxiety Disorders）](Anxiety-Disorders.md)
- [强迫症（OCD）](OCD.md)

## 外部链接

- [Pearson Clinical - SCL-90-R](https://www.pearsonassessments.com/)（官方出版商）
- [中国心理卫生杂志](http://www.cjmh.cn/)
