---
title: 多维解离量表（MID‑60）
topic: 诊断与临床
tags:
    - 诊断与临床
    - 解离
    - 量表
    - MID
    - MID-60

hide:
    - toc

updated: 2025-10-19
search:
  boost: 1.5
---

# 多维解离量表（MID‑60）

!!! warning "重要声明"
    本工具仅作教育与自我筛查参考,**不构成临床诊断**。若分数较高且合并显著痛苦/功能受损,请尽快咨询精神科/临床心理专业人士。

!!! tip "使用说明"

    - 每一道题用滑块选择 0–10:表示该体验出现的频率,0 表示"从不",10 表示"总是"。
    - 建议按直觉作答;尽量不要反复修改,以首次直觉为准。可在最后点击"计算分数"。

<!-- 样式与脚本由 mkdocs.yml 的 extra_css / extra_javascript 注入 -->

<div id="mid60-app" class="mid60-app">

<div class="mid60-meta">
  <div class="mid60-hint">范围 0–10,步长 1(可拖动或方向键微调)</div>
  <div class="mid60-actions">
    <button id="mid60-reset" class="md-button">重置</button>
  </div>
</div>

<div class="mid60-divider"></div>

<!-- 题目区域 -->
<table class="mid60-table">
  <colgroup>
    <col style="width:2.2rem">
    <col>
    <col style="width:15rem">
  </colgroup>
  <thead>
    <tr><th>#</th><th>描述</th><th>频率</th></tr>
  </thead>
  <tbody>
    <tr class="mid60-item"><td class="no">1</td><td>
      忘记当天早些时候做过的事情
    </td><td>
      <div class="mid60-ctrl"><input id="item1" type="range" min="0" max="10" step="1" value="0"><output for="item1" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">2</td><td>
      有一种情绪(例如恐惧、悲伤、愤怒、快乐),但感觉它不像是"你的"情绪
    </td><td>
      <div class="mid60-ctrl"><input id="item2" type="range" min="0" max="10" step="1" value="0"><output for="item2" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">3</td><td>
      在你脑海中听到一个孩子的声音
    </td><td>
      <div class="mid60-ctrl"><input id="item3" type="range" min="0" max="10" step="1" value="0"><output for="item3" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">4</td><td>
      如此生动地重新经历创伤事件,以至于完全失去与你实际所在位置的联系(也就是说,你认为你"回到了那里和那时")
    </td><td>
      <div class="mid60-ctrl"><input id="item4" type="range" min="0" max="10" step="1" value="0"><output for="item4" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">5</td><td>
      吞咽困难(没有已知的医学原因)
    </td><td>
      <div class="mid60-ctrl"><input id="item5" type="range" min="0" max="10" step="1" value="0"><output for="item5" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">6</td><td>
      有恍惚状态的发作,你盯着空间看,失去对周围正在发生的事情的意识
    </td><td>
      <div class="mid60-ctrl"><input id="item6" type="range" min="0" max="10" step="1" value="0"><output for="item6" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">7</td><td>
      被告知你最近做过的事情,但完全不记得做过这些事情
    </td><td>
      <div class="mid60-ctrl"><input id="item7" type="range" min="0" max="10" step="1" value="0"><output for="item7" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">8</td><td>
      不记得上一顿饭吃了什么,甚至不记得是否吃过饭
    </td><td>
      <div class="mid60-ctrl"><input id="item8" type="range" min="0" max="10" step="1" value="0"><output for="item8" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">9</td><td>
      周围的事物感觉不真实
    </td><td>
      <div class="mid60-ctrl"><input id="item9" type="range" min="0" max="10" step="1" value="0"><output for="item9" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">10</td><td>
      暂时无法看见(好像你失明了)没有已知的医学原因
    </td><td>
      <div class="mid60-ctrl"><input id="item10" type="range" min="0" max="10" step="1" value="0"><output for="item10" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">11</td><td>
      在"走过日常生活的形式"时,感到与自己的行为非常疏离
    </td><td>
      <div class="mid60-ctrl"><input id="item11" type="range" min="0" max="10" step="1" value="0"><output for="item11" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">12</td><td>
      对你真正是谁感到不确定
    </td><td>
      <div class="mid60-ctrl"><input id="item12" type="range" min="0" max="10" step="1" value="0"><output for="item12" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">13</td><td>
      感觉其他人、物体或你周围的世界不真实
    </td><td>
      <div class="mid60-ctrl"><input id="item13" type="range" min="0" max="10" step="1" value="0"><output for="item13" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">14</td><td>
      瘫痪或无法移动(没有已知的医学原因)
    </td><td>
      <div class="mid60-ctrl"><input id="item14" type="range" min="0" max="10" step="1" value="0"><output for="item14" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">15</td><td>
      因闪回而困扰,以至于很难起床面对一天
    </td><td>
      <div class="mid60-ctrl"><input id="item15" type="range" min="0" max="10" step="1" value="0"><output for="item15" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">16</td><td>
      不记得 5 岁之后童年的大部分时光
    </td><td>
      <div class="mid60-ctrl"><input id="item16" type="range" min="0" max="10" step="1" value="0"><output for="item16" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">17</td><td>
      感到与周围的一切都断开了连接
    </td><td>
      <div class="mid60-ctrl"><input id="item17" type="range" min="0" max="10" step="1" value="0"><output for="item17" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">18</td><td>
      暂时无法听见(好像你失聪了)(没有已知的医学原因)
    </td><td>
      <div class="mid60-ctrl"><input id="item18" type="range" min="0" max="10" step="1" value="0"><output for="item18" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">19</td><td>
      感觉你的过去有些片段缺失了
    </td><td>
      <div class="mid60-ctrl"><input id="item19" type="range" min="0" max="10" step="1" value="0"><output for="item19" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">20</td><td>
      立即忘记别人告诉你的话
    </td><td>
      <div class="mid60-ctrl"><input id="item20" type="range" min="0" max="10" step="1" value="0"><output for="item20" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">21</td><td>
      行走困难(没有已知的医学原因)
    </td><td>
      <div class="mid60-ctrl"><input id="item21" type="range" min="0" max="10" step="1" value="0"><output for="item21" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">22</td><td>
      在你脑海中听到一个想要你伤害自己的声音
    </td><td>
      <div class="mid60-ctrl"><input id="item22" type="range" min="0" max="10" step="1" value="0"><output for="item22" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">23</td><td>
      对你真正是谁感到非常困惑
    </td><td>
      <div class="mid60-ctrl"><input id="item23" type="range" min="0" max="10" step="1" value="0"><output for="item23" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">24</td><td>
      感觉你生命早期发生了重要的事情,但你记不起来
    </td><td>
      <div class="mid60-ctrl"><input id="item24" type="range" min="0" max="10" step="1" value="0"><output for="item24" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">25</td><td>
      感觉好像你透过雾看世界,所以人和物体感觉遥远或不清晰
    </td><td>
      <div class="mid60-ctrl"><input id="item25" type="range" min="0" max="10" step="1" value="0"><output for="item25" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">26</td><td>
      有癫痫发作,但医生找不到原因
    </td><td>
      <div class="mid60-ctrl"><input id="item26" type="range" min="0" max="10" step="1" value="0"><output for="item26" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">27</td><td>
      进入恍惚状态太多(或太长时间),以至于它干扰了你的日常活动和责任
    </td><td>
      <div class="mid60-ctrl"><input id="item27" type="range" min="0" max="10" step="1" value="0"><output for="item27" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">28</td><td>
      话语从你嘴里流出,好像它们不在你的控制之中
    </td><td>
      <div class="mid60-ctrl"><input id="item28" type="range" min="0" max="10" step="1" value="0"><output for="item28" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">29</td><td>
      感觉你的记忆中有很大的空白
    </td><td>
      <div class="mid60-ctrl"><input id="item29" type="range" min="0" max="10" step="1" value="0"><output for="item29" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">30</td><td>
      进入恍惚状态持续数小时
    </td><td>
      <div class="mid60-ctrl"><input id="item30" type="range" min="0" max="10" step="1" value="0"><output for="item30" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">31</td><td>
      不好的记忆进入你的脑海,你无法摆脱它们
    </td><td>
      <div class="mid60-ctrl"><input id="item31" type="range" min="0" max="10" step="1" value="0"><output for="item31" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">32</td><td>
      在不知不觉中飘入恍惚状态
    </td><td>
      <div class="mid60-ctrl"><input id="item32" type="range" min="0" max="10" step="1" value="0"><output for="item32" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">33</td><td>
      话语从你嘴里说出来,但你没有说它们;你不知道这些话从哪里来
    </td><td>
      <div class="mid60-ctrl"><input id="item33" type="range" min="0" max="10" step="1" value="0"><output for="item33" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">34</td><td>
      几乎记不起你的过去
    </td><td>
      <div class="mid60-ctrl"><input id="item34" type="range" min="0" max="10" step="1" value="0"><output for="item34" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">35</td><td>
      当你生气时,做或说一些你(冷静下来后)不记得的事情
    </td><td>
      <div class="mid60-ctrl"><input id="item35" type="range" min="0" max="10" step="1" value="0"><output for="item35" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">36</td><td>
      感觉你有多重人格
    </td><td>
      <div class="mid60-ctrl"><input id="item36" type="range" min="0" max="10" step="1" value="0"><output for="item36" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">37</td><td>
      在你脑海中听到一个声音,它骂你(例如,懦夫、愚蠢、妓女、荡妇、婊子等)
    </td><td>
      <div class="mid60-ctrl"><input id="item37" type="range" min="0" max="10" step="1" value="0"><output for="item37" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">38</td><td>
      记忆力差给你带来严重困难
    </td><td>
      <div class="mid60-ctrl"><input id="item38" type="range" min="0" max="10" step="1" value="0"><output for="item38" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">39</td><td>
      你内心有其他人(或部分),他们有自己的名字
    </td><td>
      <div class="mid60-ctrl"><input id="item39" type="range" min="0" max="10" step="1" value="0"><output for="item39" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">40</td><td>
      如此生动地重新经历过去的创伤,以至于你看到它、听到它、闻到它等
    </td><td>
      <div class="mid60-ctrl"><input id="item40" type="range" min="0" max="10" step="1" value="0"><output for="item40" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">41</td><td>
      连续几天进入恍惚状态
    </td><td>
      <div class="mid60-ctrl"><input id="item41" type="range" min="0" max="10" step="1" value="0"><output for="item41" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">42</td><td>
      发现你改变了外表(例如,剪了头发,或改变了发型,或换了衣服,或化了妆等),但不记得这样做过
    </td><td>
      <div class="mid60-ctrl"><input id="item42" type="range" min="0" max="10" step="1" value="0"><output for="item42" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">43</td><td>
      因忘记太多而感到困扰或不安
    </td><td>
      <div class="mid60-ctrl"><input id="item43" type="range" min="0" max="10" step="1" value="0"><output for="item43" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">44</td><td>
      在你脑海中听到一个想要你死的声音
    </td><td>
      <div class="mid60-ctrl"><input id="item44" type="range" min="0" max="10" step="1" value="0"><output for="item44" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">45</td><td>
      突然发现自己在家里某个奇怪的地方(例如,壁橱里、床下、蜷缩在地板上等),不知道自己是怎么到那里的
    </td><td>
      <div class="mid60-ctrl"><input id="item45" type="range" min="0" max="10" step="1" value="0"><output for="item45" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">46</td><td>
      感觉好像你内心有某种东西控制着你的行为和言语
    </td><td>
      <div class="mid60-ctrl"><input id="item46" type="range" min="0" max="10" step="1" value="0"><output for="item46" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">47</td><td>
      完全忘记如何做一些你很清楚如何做的事情(例如,如何开车、如何阅读、如何使用电脑、如何弹钢琴等)
    </td><td>
      <div class="mid60-ctrl"><input id="item47" type="range" min="0" max="10" step="1" value="0"><output for="item47" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">48</td><td>
      突然发现自己在某个地方(例如,在海滩、在工作、在夜总会、在你的车里等),不记得你是怎么到那里的
    </td><td>
      <div class="mid60-ctrl"><input id="item48" type="range" min="0" max="10" step="1" value="0"><output for="item48" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">49</td><td>
      感觉你内心有另一个人,如果它愿意,它可以出来说话
    </td><td>
      <div class="mid60-ctrl"><input id="item49" type="range" min="0" max="10" step="1" value="0"><output for="item49" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">50</td><td>
      "清醒过来"发现你做了一些你不记得做过的事情(例如,打碎了东西、割伤了自己、打扫了整个房子等)
    </td><td>
      <div class="mid60-ctrl"><input id="item50" type="range" min="0" max="10" step="1" value="0"><output for="item50" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">51</td><td>
      难以保持清醒而不进入恍惚状态
    </td><td>
      <div class="mid60-ctrl"><input id="item51" type="range" min="0" max="10" step="1" value="0"><output for="item51" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">52</td><td>
      突然不知道如何做你的工作
    </td><td>
      <div class="mid60-ctrl"><input id="item52" type="range" min="0" max="10" step="1" value="0"><output for="item52" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">53</td><td>
      你的身体突然感觉好像它不是真的你的
    </td><td>
      <div class="mid60-ctrl"><input id="item53" type="range" min="0" max="10" step="1" value="0"><output for="item53" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">54</td><td>
      连续几天被闪回困扰
    </td><td>
      <div class="mid60-ctrl"><input id="item54" type="range" min="0" max="10" step="1" value="0"><output for="item54" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">55</td><td>
      对你的情绪感到困惑或疑惑
    </td><td>
      <div class="mid60-ctrl"><input id="item55" type="range" min="0" max="10" step="1" value="0"><output for="item55" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">56</td><td>
      在你脑海中听到一个声音,它告诉你"闭嘴"
    </td><td>
      <div class="mid60-ctrl"><input id="item56" type="range" min="0" max="10" step="1" value="0"><output for="item56" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">57</td><td>
      你内心有另一个部分,它有与你不同的记忆、行为和感受
    </td><td>
      <div class="mid60-ctrl"><input id="item57" type="range" min="0" max="10" step="1" value="0"><output for="item57" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">58</td><td>
      有时你"醒来"发现手中有药片或剃刀刀片(或其他伤害自己的东西)
    </td><td>
      <div class="mid60-ctrl"><input id="item58" type="range" min="0" max="10" step="1" value="0"><output for="item58" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">59</td><td>
      在你脑海中听到一个声音,它说你不好、没有价值或失败
    </td><td>
      <div class="mid60-ctrl"><input id="item59" type="range" min="0" max="10" step="1" value="0"><output for="item59" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">60</td><td>
      有一个非常愤怒的部分"出来"并说和做你永远不会做或说的事情
    </td><td>
      <div class="mid60-ctrl"><input id="item60" type="range" min="0" max="10" step="1" value="0"><output for="item60" class="mid60-badge">0</output></div>
    </td></tr>
  </tbody>
</table>

<div class="mid60-divider"></div>

<div id="mid60-results" class="mid60-results">
  <div><strong>平均分</strong>:<span id="mid60-avg" class="mid60-badge">0.0</span>%</div>
  <div class="mid60-progress" aria-label="MID-60 平均分可视化">
    <div id="mid60-bar" class="bar" style="width:0%"></div>
  </div>
  <div class="mid60-legend"><span>0</span><span>7</span><span>14</span><span>21</span><span>30</span><span>40</span><span>64</span><span>100</span></div>
  <div class="mid60-note">临床解读:<span id="mid60-level">无解离体验</span></div>

  <div class="mid60-divider"></div>

  <!-- 诊断分类子量表 -->
  <div class="mid60-section-title">解离性身份障碍 (DID)</div>
  <div class="mid60-subgrid">
    <div class="mid60-subcard">
      <div class="label" title="近期事件的遗忘症 - 临界值: 10">近期遗忘 Amnesia</div>
      <div class="row"><span class="mid60-badge" id="mid60-amnesia-val">0.0</span><span class="cutoff">临界值: 10</span></div>
      <div class="mid60-progress" aria-label="近期遗忘子量表">
        <div id="mid60-amnesia-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>

  <div class="mid60-section-title">DID 与 OSDD-1</div>
  <div class="mid60-subgrid">
    <div class="mid60-subcard">
      <div class="label" title="对替换人格和自我状态的主观意识 - 临界值: 20">替换人格意识</div>
      <div class="row"><span class="mid60-badge" id="mid60-alter-val">0.0</span><span class="cutoff">临界值: 20</span></div>
      <div class="mid60-progress" aria-label="替换人格意识子量表">
        <div id="mid60-alter-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
    <div class="mid60-subcard">
      <div class="label" title="愤怒侵入 - 临界值: 18">愤怒侵入</div>
      <div class="row"><span class="mid60-badge" id="mid60-angry-val">0.0</span><span class="cutoff">临界值: 18</span></div>
      <div class="mid60-progress" aria-label="愤怒侵入子量表">
        <div id="mid60-angry-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
    <div class="mid60-subcard">
      <div class="label" title="迫害性侵入 - 临界值: 18">迫害侵入</div>
      <div class="row"><span class="mid60-badge" id="mid60-persec-val">0.0</span><span class="cutoff">临界值: 18</span></div>
      <div class="mid60-progress" aria-label="迫害侵入子量表">
        <div id="mid60-persec-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>

  <div class="mid60-section-title">人格解体/现实解体障碍</div>
  <div class="mid60-subgrid">
    <div class="mid60-subcard">
      <div class="label" title="人格解体/现实解体 - 临界值: 20">DP/DR</div>
      <div class="row"><span class="mid60-badge" id="mid60-dpdr-val">0.0</span><span class="cutoff">临界值: 20</span></div>
      <div class="mid60-progress" aria-label="DP/DR 子量表">
        <div id="mid60-dpdr-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>

  <div class="mid60-section-title">解离性失忆</div>
  <div class="mid60-subgrid">
    <div class="mid60-subcard">
      <div class="label" title="对严重记忆问题的痛苦 - 临界值: 30">记忆困扰</div>
      <div class="row"><span class="mid60-badge" id="mid60-distress-val">0.0</span><span class="cutoff">临界值: 30</span></div>
      <div class="mid60-progress" aria-label="记忆困扰子量表">
        <div id="mid60-distress-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
    <div class="mid60-subcard">
      <div class="label" title="自传体记忆丧失 - 临界值: 34">自传记忆丧失</div>
      <div class="row"><span class="mid60-badge" id="mid60-autobio-val">0.0</span><span class="cutoff">临界值: 34</span></div>
      <div class="mid60-progress" aria-label="自传记忆丧失子量表">
        <div id="mid60-autobio-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>

  <div class="mid60-section-title">创伤后应激障碍 (PTSD)</div>
  <div class="mid60-subgrid">
    <div class="mid60-subcard">
      <div class="label" title="闪回 - 临界值: 16">闪回</div>
      <div class="row"><span class="mid60-badge" id="mid60-flash-val">0.0</span><span class="cutoff">临界值: 16</span></div>
      <div class="mid60-progress" aria-label="闪回子量表">
        <div id="mid60-flash-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>

  <div class="mid60-section-title">转换障碍</div>
  <div class="mid60-subgrid">
    <div class="mid60-subcard">
      <div class="label" title="身体症状 - 临界值: 10">躯体症状</div>
      <div class="row"><span class="mid60-badge" id="mid60-body-val">0.0</span><span class="cutoff">临界值: 10</span></div>
      <div class="mid60-progress" aria-label="躯体症状子量表">
        <div id="mid60-body-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
    <div class="mid60-subcard">
      <div class="label" title="假性癫痫发作 - 临界值: 10">假性癫痫</div>
      <div class="row"><span class="mid60-badge" id="mid60-seizure-val">0.0</span><span class="cutoff">临界值: 10</span></div>
      <div class="mid60-progress" aria-label="假性癫痫子量表">
        <div id="mid60-seizure-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>

  <div class="mid60-section-title">一般解离子量表</div>
  <div class="mid60-subgrid">
    <div class="mid60-subcard">
      <div class="label" title="恍惚 - 临界值: 11.7">恍惚 Trance</div>
      <div class="row"><span class="mid60-badge" id="mid60-trance-val">0.0</span><span class="cutoff">临界值: 11.7</span></div>
      <div class="mid60-progress" aria-label="恍惚子量表">
        <div id="mid60-trance-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
    <div class="mid60-subcard">
      <div class="label" title="自我困惑 - 临界值: 33.3">自我困惑</div>
      <div class="row"><span class="mid60-badge" id="mid60-confuse-val">0.0</span><span class="cutoff">临界值: 33.3</span></div>
      <div class="mid60-progress" aria-label="自我困惑子量表">
        <div id="mid60-confuse-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>
</div>

</div>

!!! info "分数解释(与 NovoPsych 一致,筛查用途)"

    - **0–7**: 无解离体验
    - **7–14**: 很少有诊断意义的解离体验
    - **15–20**: 轻度解离症状。可能存在 PTSD 或轻度解离障碍(如解离性失忆、人格解体/现实解体障碍)
    - **21–30**: 可能存在解离障碍和/或 PTSD
    - **31–40**: 可能存在解离障碍(如 OSDD-1 或 DID)和 PTSD
    - **41–64**: 可能患有 DID 或严重解离障碍和 PTSD
    - **64+**: 严重的解离和创伤后症状。高分也可能反映神经质、寻求注意的行为、症状夸大或装病,或精神病

    **临界值**: >21% 表示临床显著症状。

    分数需要结合具体困扰与功能受损讨论;高分并不等同诊断,低分亦不排除个别情境下的显著困扰。

!!! note "子量表说明(依据 NovoPsych 公示资料)"

    MID-60 提供与不同诊断相关的子量表信息,帮助临床医生形成可能诊断的印象:

    ### 解离性身份障碍 (DID)
    - **近期遗忘** (题目 42, 45, 48, 58) - 临界值 = 10

    ### DID 与 OSDD-1
    - **替换人格意识** (题目 3, 36, 39, 49, 57) - 临界值 = 20
    - **愤怒侵入** (题目 28, 33, 35, 46, 60) - 临界值 = 18
    - **迫害侵入** (题目 22, 37, 44, 56, 59) - 临界值 = 18

    ### 人格解体/现实解体障碍
    - **DP/DR** (题目 2, 7, 9, 13, 25, 47, 50, 53) - 临界值 = 20

    ### 解离性失忆
    - **记忆困扰** (题目 1, 8, 20, 38, 43, 52) - 临界值 = 30
    - **自传记忆丧失** (题目 16, 19, 24, 29, 34) - 临界值 = 34

    ### 创伤后应激障碍 (PTSD)
    - **闪回** (题目 4, 15, 31, 40, 54) - 临界值 = 16

    ### 转换障碍
    - **躯体症状** (题目 5, 10, 14, 18) - 临界值 = 10
    - **假性癫痫** (题目 26) - 临界值 = 10

    ### 一般解离子量表
    - **恍惚** (题目 21, 27, 30, 32, 41, 51) - 临界值 = 11.7
    - **自我困惑** (题目 6, 11, 12, 17, 23, 55) - 临界值 = 33.3

!!! warning "重要提示"
    MID-60 用于筛查目的,**不应作为诊断的唯一依据**,应始终与临床专业知识结合使用。进一步评估可以通过 DSM-5 解离障碍结构化临床访谈 (SCID-D) 或解离障碍访谈量表 (DDIS) 进行。

!!! quote "参考"
    Dell, P. F. (2006). The Multidimensional Inventory of Dissociation (MID): A Comprehensive measure of pathological dissociation. *Journal of Trauma & Dissociation, 7*(2), 77-106.

    Dell, P. F., & Lawson, D. (2009). Empirically guided revision of experiences of possession and related phenomena: A cross-cultural examination. *Journal of Trauma & Dissociation, 10*(4), 436-456.
