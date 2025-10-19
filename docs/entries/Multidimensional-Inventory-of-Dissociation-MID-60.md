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

!!! info "速览 Clinician's Summary"

    **多维解离量表（MID‑60）**是一个自评筛查工具,用于评估解离体验的频率与严重程度,涵盖[解离性身份障碍（DID）](DID.md)、[其他特定解离障碍（OSDD）](OSDD.md)、人格解体/现实解体障碍（DP/DR）、解离性失忆、[创伤后应激障碍（PTSD）](PTSD.md)及功能性神经症状障碍（转换障碍）等相关症状。

    **计分方法**:受试者对 60 道题目按 0–10 评分（0=从不,10=总是）,**总分 = 全体 60 题均值 × 10（范围 0–100%）**。**临界值 >21%** 表示临床显著症状。量表还提供 12 个子量表分数,每个子量表对应特定诊断类别,各有其临界值。

    **解读边界**:MID‑60 属于**筛查级工具**,不能替代正式诊断。分数需结合具体困扰与功能受损情况讨论;高分不等同诊断,低分亦不排除个别情境下的显著困扰。进一步评估需使用诊断级工具。

!!! warning "重要声明"
    本工具仅作教育与自我筛查参考,**不构成临床诊断**。若分数较高且合并显著痛苦/功能受损,请尽快咨询精神科/临床心理专业人士。

!!! tip "使用说明"

    - 每一道题用滑块选择 0–10:表示该体验出现的频率,0 表示"从不",10 表示"总是"。
    - 建议按直觉作答;尽量不要反复修改,以首次直觉为准。
    - **计分方法**:总分 = 全体 60 题均值 × 10（范围 0–100%）,临界值 >21% 表示临床显著症状。

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
      忘记当天较早时做过的事情
    </td><td>
      <div class="mid60-ctrl"><input id="item1" type="range" min="0" max="10" step="1" value="0"><output for="item1" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">2</td><td>
      出现某种情绪(如恐惧/悲伤/愤怒/快乐),但感觉它不像是"你的"情绪
    </td><td>
      <div class="mid60-ctrl"><input id="item2" type="range" min="0" max="10" step="1" value="0"><output for="item2" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">3</td><td>
      在脑海中听到一个孩子的声音
    </td><td>
      <div class="mid60-ctrl"><input id="item3" type="range" min="0" max="10" step="1" value="0"><output for="item3" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">4</td><td>
      如此生动地重新经历创伤事件,以至于完全失去与当下所在之处的联系(仿佛你回到当时彼处)
    </td><td>
      <div class="mid60-ctrl"><input id="item4" type="range" min="0" max="10" step="1" value="0"><output for="item4" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">5</td><td>
      吞咽困难(无已知医学原因)
    </td><td>
      <div class="mid60-ctrl"><input id="item5" type="range" min="0" max="10" step="1" value="0"><output for="item5" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">6</td><td>
      出现恍惚(出神),你盯着某处发呆,对周围正在发生的事失去觉察
    </td><td>
      <div class="mid60-ctrl"><input id="item6" type="range" min="0" max="10" step="1" value="0"><output for="item6" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">7</td><td>
      别人说你最近做过某些事,但你完全不记得
    </td><td>
      <div class="mid60-ctrl"><input id="item7" type="range" min="0" max="10" step="1" value="0"><output for="item7" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">8</td><td>
      不记得上一顿吃了什么,甚至不记得是否吃过
    </td><td>
      <div class="mid60-ctrl"><input id="item8" type="range" min="0" max="10" step="1" value="0"><output for="item8" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">9</td><td>
      周围的事物感觉不真实
    </td><td>
      <div class="mid60-ctrl"><input id="item9" type="range" min="0" max="10" step="1" value="0"><output for="item9" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">10</td><td>
      一时看不见(仿佛失明,无已知医学原因)
    </td><td>
      <div class="mid60-ctrl"><input id="item10" type="range" min="0" max="10" step="1" value="0"><output for="item10" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">11</td><td>
      走过场般做日常事,却强烈感到与自己的行为疏离
    </td><td>
      <div class="mid60-ctrl"><input id="item11" type="range" min="0" max="10" step="1" value="0"><output for="item11" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">12</td><td>
      对你究竟是谁感到不确定
    </td><td>
      <div class="mid60-ctrl"><input id="item12" type="range" min="0" max="10" step="1" value="0"><output for="item12" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">13</td><td>
      他人、物体或周围世界让你感到不真实
    </td><td>
      <div class="mid60-ctrl"><input id="item13" type="range" min="0" max="10" step="1" value="0"><output for="item13" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">14</td><td>
      瘫痪或无法移动(无已知医学原因)
    </td><td>
      <div class="mid60-ctrl"><input id="item14" type="range" min="0" max="10" step="1" value="0"><output for="item14" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">15</td><td>
      被闪回困扰到难以起床开始一天
    </td><td>
      <div class="mid60-ctrl"><input id="item15" type="range" min="0" max="10" step="1" value="0"><output for="item15" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">16</td><td>
      不记得 5 岁之后童年的大部分时光
    </td><td>
      <div class="mid60-ctrl"><input id="item16" type="range" min="0" max="10" step="1" value="0"><output for="item16" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">17</td><td>
      感到与周围一切都断开连接
    </td><td>
      <div class="mid60-ctrl"><input id="item17" type="range" min="0" max="10" step="1" value="0"><output for="item17" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">18</td><td>
      一时听不见(仿佛失聪,无已知医学原因)
    </td><td>
      <div class="mid60-ctrl"><input id="item18" type="range" min="0" max="10" step="1" value="0"><output for="item18" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">19</td><td>
      感到你的过去有片段缺失
    </td><td>
      <div class="mid60-ctrl"><input id="item19" type="range" min="0" max="10" step="1" value="0"><output for="item19" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">20</td><td>
      别人刚说过的话你立刻就忘
    </td><td>
      <div class="mid60-ctrl"><input id="item20" type="range" min="0" max="10" step="1" value="0"><output for="item20" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">21</td><td>
      行走困难(无已知医学原因)
    </td><td>
      <div class="mid60-ctrl"><input id="item21" type="range" min="0" max="10" step="1" value="0"><output for="item21" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">22</td><td>
      在脑海中听到一个声音想要你伤害自己
    </td><td>
      <div class="mid60-ctrl"><input id="item22" type="range" min="0" max="10" step="1" value="0"><output for="item22" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">23</td><td>
      对你究竟是谁感到非常困惑
    </td><td>
      <div class="mid60-ctrl"><input id="item23" type="range" min="0" max="10" step="1" value="0"><output for="item23" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">24</td><td>
      觉得生命早期发生过重要事情,但想不起来
    </td><td>
      <div class="mid60-ctrl"><input id="item24" type="range" min="0" max="10" step="1" value="0"><output for="item24" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">25</td><td>
      感到像隔着雾看世界,人和物体显得遥远或不清晰
    </td><td>
      <div class="mid60-ctrl"><input id="item25" type="range" min="0" max="10" step="1" value="0"><output for="item25" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">26</td><td>
      出现发作/抽搐,但医生找不到原因(提示PNES可能)
    </td><td>
      <div class="mid60-ctrl"><input id="item26" type="range" min="0" max="10" step="1" value="0"><output for="item26" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">27</td><td>
      过于频繁或持续太久地进入恍惚(出神),以至于干扰日常活动/责任
    </td><td>
      <div class="mid60-ctrl"><input id="item27" type="range" min="0" max="10" step="1" value="0"><output for="item27" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">28</td><td>
      话语自己从你口中说出,仿佛不受你的控制
    </td><td>
      <div class="mid60-ctrl"><input id="item28" type="range" min="0" max="10" step="1" value="0"><output for="item28" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">29</td><td>
      感到你的记忆有很大的空白
    </td><td>
      <div class="mid60-ctrl"><input id="item29" type="range" min="0" max="10" step="1" value="0"><output for="item29" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">30</td><td>
      恍惚(出神)可持续数小时
    </td><td>
      <div class="mid60-ctrl"><input id="item30" type="range" min="0" max="10" step="1" value="0"><output for="item30" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">31</td><td>
      不好的记忆涌入脑海,难以摆脱
    </td><td>
      <div class="mid60-ctrl"><input id="item31" type="range" min="0" max="10" step="1" value="0"><output for="item31" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">32</td><td>
      不知不觉就滑入恍惚(出神)
    </td><td>
      <div class="mid60-ctrl"><input id="item32" type="range" min="0" max="10" step="1" value="0"><output for="item32" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">33</td><td>
      话从你口中说出,但你并未主动说;你不知道它们从何而来
    </td><td>
      <div class="mid60-ctrl"><input id="item33" type="range" min="0" max="10" step="1" value="0"><output for="item33" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">34</td><td>
      几乎记不起你的过去
    </td><td>
      <div class="mid60-ctrl"><input id="item34" type="range" min="0" max="10" step="1" value="0"><output for="item34" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">35</td><td>
      生气时做过或说过的事,冷静后不记得
    </td><td>
      <div class="mid60-ctrl"><input id="item35" type="range" min="0" max="10" step="1" value="0"><output for="item35" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">36</td><td>
      感觉你有多重人格
    </td><td>
      <div class="mid60-ctrl"><input id="item36" type="range" min="0" max="10" step="1" value="0"><output for="item36" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">37</td><td>
      在脑海中听到辱骂你的声音(如"懦弱/愚蠢/下贱/婊子"等)
    </td><td>
      <div class="mid60-ctrl"><input id="item37" type="range" min="0" max="10" step="1" value="0"><output for="item37" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">38</td><td>
      记忆差给你带来严重困难
    </td><td>
      <div class="mid60-ctrl"><input id="item38" type="range" min="0" max="10" step="1" value="0"><output for="item38" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">39</td><td>
      你内在还有他人(或部分),他们有各自的名字
    </td><td>
      <div class="mid60-ctrl"><input id="item39" type="range" min="0" max="10" step="1" value="0"><output for="item39" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">40</td><td>
      极其生动地重历过往创伤,仿佛能看见/听见/闻到它
    </td><td>
      <div class="mid60-ctrl"><input id="item40" type="range" min="0" max="10" step="1" value="0"><output for="item40" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">41</td><td>
      连续数天处于恍惚(出神)
    </td><td>
      <div class="mid60-ctrl"><input id="item41" type="range" min="0" max="10" step="1" value="0"><output for="item41" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">42</td><td>
      发现自己改变了外表(剪/换了发型、衣服、化妆等),却不记得这样做过
    </td><td>
      <div class="mid60-ctrl"><input id="item42" type="range" min="0" max="10" step="1" value="0"><output for="item42" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">43</td><td>
      因忘记太多而困扰或不安
    </td><td>
      <div class="mid60-ctrl"><input id="item43" type="range" min="0" max="10" step="1" value="0"><output for="item43" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">44</td><td>
      在脑海中听到一个声音要你去死
    </td><td>
      <div class="mid60-ctrl"><input id="item44" type="range" min="0" max="10" step="1" value="0"><output for="item44" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">45</td><td>
      突然发现自己在家中奇怪的地方(壁橱里、床下、蜷缩在地上等),不知道如何到那里
    </td><td>
      <div class="mid60-ctrl"><input id="item45" type="range" min="0" max="10" step="1" value="0"><output for="item45" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">46</td><td>
      感到内在有某种东西在控制你的行为与言语
    </td><td>
      <div class="mid60-ctrl"><input id="item46" type="range" min="0" max="10" step="1" value="0"><output for="item46" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">47</td><td>
      完全忘记如何做你本会做的事(如开车、阅读、用电脑、弹琴等)
    </td><td>
      <div class="mid60-ctrl"><input id="item47" type="range" min="0" max="10" step="1" value="0"><output for="item47" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">48</td><td>
      突然发现自己身处某处(海滩、工作地、夜店、车里等),不记得如何到达
    </td><td>
      <div class="mid60-ctrl"><input id="item48" type="range" min="0" max="10" step="1" value="0"><output for="item48" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">49</td><td>
      感到内在有另一个人,若它愿意,它可以出来说话
    </td><td>
      <div class="mid60-ctrl"><input id="item49" type="range" min="0" max="10" step="1" value="0"><output for="item49" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">50</td><td>
      "回过神来"发现你做过一些不记得做过的事(打碎东西、自伤、打扫整屋等)
    </td><td>
      <div class="mid60-ctrl"><input id="item50" type="range" min="0" max="10" step="1" value="0"><output for="item50" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">51</td><td>
      很难保持清醒而不进入恍惚(出神)
    </td><td>
      <div class="mid60-ctrl"><input id="item51" type="range" min="0" max="10" step="1" value="0"><output for="item51" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">52</td><td>
      突然不知道如何开展你的工作
    </td><td>
      <div class="mid60-ctrl"><input id="item52" type="range" min="0" max="10" step="1" value="0"><output for="item52" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">53</td><td>
      你的身体突然感觉不像是你的
    </td><td>
      <div class="mid60-ctrl"><input id="item53" type="range" min="0" max="10" step="1" value="0"><output for="item53" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">54</td><td>
      连续几天被闪回困扰
    </td><td>
      <div class="mid60-ctrl"><input id="item54" type="range" min="0" max="10" step="1" value="0"><output for="item54" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">55</td><td>
      对你的情绪感到困惑或拿不准
    </td><td>
      <div class="mid60-ctrl"><input id="item55" type="range" min="0" max="10" step="1" value="0"><output for="item55" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">56</td><td>
      在脑海中听到一个声音对你说"闭嘴"
    </td><td>
      <div class="mid60-ctrl"><input id="item56" type="range" min="0" max="10" step="1" value="0"><output for="item56" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">57</td><td>
      你内在有另一个部分,它的记忆、行为和感受与你不同
    </td><td>
      <div class="mid60-ctrl"><input id="item57" type="range" min="0" max="10" step="1" value="0"><output for="item57" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">58</td><td>
      有时"回过神来"发现手里拿着药片或刀片(或其他自伤物品)
    </td><td>
      <div class="mid60-ctrl"><input id="item58" type="range" min="0" max="10" step="1" value="0"><output for="item58" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">59</td><td>
      在脑海中听到一个声音说你不好、没有价值或是个失败者
    </td><td>
      <div class="mid60-ctrl"><input id="item59" type="range" min="0" max="10" step="1" value="0"><output for="item59" class="mid60-badge">0</output></div>
    </td></tr>

    <tr class="mid60-item"><td class="no">60</td><td>
      有一个非常愤怒的部分"出来",它会说/做你从不会说/做的事
    </td><td>
      <div class="mid60-ctrl"><input id="item60" type="range" min="0" max="10" step="1" value="0"><output for="item60" class="mid60-badge">0</output></div>
    </td></tr>
  </tbody>
</table>

<div class="mid60-divider"></div>

<div id="mid60-results" class="mid60-results">
  <div><strong>平均分</strong>:<span id="mid60-avg" class="mid60-badge">0.0</span>%</div>
  <div class="mid60-progress" aria-label="MID-60 平均分可视化" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
    <div id="mid60-bar" class="bar" style="width:0%"></div>
  </div>
  <div class="mid60-legend"><span>0</span><span>7</span><span>14</span><span>21</span><span>30</span><span>40</span><span>64</span><span>100</span></div>
  <div class="mid60-note">临床解读:<span id="mid60-level">无解离体验</span></div>

  <div class="mid60-divider"></div>

  <div id="mid60-safety-alert" class="mid60-safety-alert" style="display:none; background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 1rem; margin: 1rem 0; border-radius: 4px;">
    <strong>⚠️ 安全提示</strong>:您在自伤/自杀相关题目（第 22/44/58 题）上的评分较高。如果您当前存在自伤或伤害他人的意念,请立即寻求帮助:<br>
    • 24 小时心理危机热线:010-82951332（北京）<br>
    • 全国心理援助热线:400-161-9995<br>
    • 或访问我们的 <a href="../Crisis-Resources.md" style="color: #d9534f; font-weight: bold;">危机资源页面</a> 获取更多紧急支持资源
  </div>

  <div class="mid60-divider"></div>

  <!-- 诊断分类子量表 -->
  <div class="mid60-section-title">解离性身份障碍（DID）</div>
  <div class="mid60-subgrid">
    <div class="mid60-subcard">
      <div class="label" title="近期事件的遗忘症（Amnesia for recent events）- 临界值: 10%">近期遗忘（Amnesia）</div>
      <div class="row"><span class="mid60-badge" id="mid60-amnesia-val">0.0</span><span class="cutoff">临界值: 10%</span></div>
      <div class="mid60-progress" aria-label="近期遗忘子量表" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-describedby="mid60-amnesia-val">
        <div id="mid60-amnesia-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>

  <div class="mid60-section-title">DID 与 OSDD</div>
  <div class="mid60-subgrid">
    <div class="mid60-subcard">
      <div class="label" title="对替换人格和自我状态的主观意识（Awareness of alter personalities）- 临界值: 20%">替换人格意识（Alter awareness）</div>
      <div class="row"><span class="mid60-badge" id="mid60-alter-val">0.0</span><span class="cutoff">临界值: 20%</span></div>
      <div class="mid60-progress" aria-label="替换人格意识子量表" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-describedby="mid60-alter-val">
        <div id="mid60-alter-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
    <div class="mid60-subcard">
      <div class="label" title="愤怒侵入（Angry intrusions）- 临界值: 18%">愤怒侵入（Angry intrusions）</div>
      <div class="row"><span class="mid60-badge" id="mid60-angry-val">0.0</span><span class="cutoff">临界值: 18%</span></div>
      <div class="mid60-progress" aria-label="愤怒侵入子量表" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-describedby="mid60-angry-val">
        <div id="mid60-angry-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
    <div class="mid60-subcard">
      <div class="label" title="迫害性侵入（Persecutory intrusions）- 临界值: 18%">迫害侵入（Persecutory intrusions）</div>
      <div class="row"><span class="mid60-badge" id="mid60-persec-val">0.0</span><span class="cutoff">临界值: 18%</span></div>
      <div class="mid60-progress" aria-label="迫害侵入子量表" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-describedby="mid60-persec-val">
        <div id="mid60-persec-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>

  <div class="mid60-section-title">人格解体/现实解体障碍（DP/DR）</div>
  <div class="mid60-subgrid">
    <div class="mid60-subcard">
      <div class="label" title="人格解体/现实解体（Depersonalization/Derealization）- 临界值: 20%">人格解体/现实解体（DP/DR）</div>
      <div class="row"><span class="mid60-badge" id="mid60-dpdr-val">0.0</span><span class="cutoff">临界值: 20%</span></div>
      <div class="mid60-progress" aria-label="人格解体/现实解体子量表" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-describedby="mid60-dpdr-val">
        <div id="mid60-dpdr-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>

  <div class="mid60-section-title">解离性失忆</div>
  <div class="mid60-subgrid">
    <div class="mid60-subcard">
      <div class="label" title="对严重记忆问题的痛苦（Distress from severe memory problems）- 临界值: 30%">记忆困扰（Memory distress）</div>
      <div class="row"><span class="mid60-badge" id="mid60-distress-val">0.0</span><span class="cutoff">临界值: 30%</span></div>
      <div class="mid60-progress" aria-label="记忆困扰子量表" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-describedby="mid60-distress-val">
        <div id="mid60-distress-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
    <div class="mid60-subcard">
      <div class="label" title="自传体记忆丧失（Loss of autobiographical memory）- 临界值: 34%">自传记忆丧失（Autobiographical memory loss）</div>
      <div class="row"><span class="mid60-badge" id="mid60-autobio-val">0.0</span><span class="cutoff">临界值: 34%</span></div>
      <div class="mid60-progress" aria-label="自传记忆丧失子量表" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-describedby="mid60-autobio-val">
        <div id="mid60-autobio-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>

  <div class="mid60-section-title">创伤后应激障碍（PTSD）</div>
  <div class="mid60-subgrid">
    <div class="mid60-subcard">
      <div class="label" title="闪回（Flashbacks）- 临界值: 16%">闪回（Flashbacks）</div>
      <div class="row"><span class="mid60-badge" id="mid60-flash-val">0.0</span><span class="cutoff">临界值: 16%</span></div>
      <div class="mid60-progress" aria-label="闪回子量表" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-describedby="mid60-flash-val">
        <div id="mid60-flash-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>

  <div class="mid60-section-title">功能性神经症状障碍（FNSD/转换障碍）</div>
  <div class="mid60-subgrid">
    <div class="mid60-subcard">
      <div class="label" title="功能性神经症状（躯体症状）- 临界值: 10%">功能性神经症状</div>
      <div class="row"><span class="mid60-badge" id="mid60-body-val">0.0</span><span class="cutoff">临界值: 10%</span></div>
      <div class="mid60-progress" aria-label="功能性神经症状子量表" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-describedby="mid60-body-val">
        <div id="mid60-body-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
    <div class="mid60-subcard">
      <div class="label" title="心因性非癫痫发作（PNES）- 临界值: 10%">心因性非癫痫发作（PNES）</div>
      <div class="row"><span class="mid60-badge" id="mid60-seizure-val">0.0</span><span class="cutoff">临界值: 10%</span></div>
      <div class="mid60-progress" aria-label="心因性非癫痫发作子量表" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-describedby="mid60-seizure-val">
        <div id="mid60-seizure-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>

  <div class="mid60-section-title">一般解离子量表</div>
  <div class="mid60-subgrid">
    <div class="mid60-subcard">
      <div class="label" title="恍惚（Trance states）- 临界值: 11.7%">恍惚（Trance）</div>
      <div class="row"><span class="mid60-badge" id="mid60-trance-val">0.0</span><span class="cutoff">临界值: 11.7%</span></div>
      <div class="mid60-progress" aria-label="恍惚子量表" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-describedby="mid60-trance-val">
        <div id="mid60-trance-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
    <div class="mid60-subcard">
      <div class="label" title="自我困惑（Identity confusion）- 临界值: 33.3%">自我困惑（Identity confusion）</div>
      <div class="row"><span class="mid60-badge" id="mid60-confuse-val">0.0</span><span class="cutoff">临界值: 33.3%</span></div>
      <div class="mid60-progress" aria-label="自我困惑子量表" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-describedby="mid60-confuse-val">
        <div id="mid60-confuse-bar" class="bar" style="width:0%"></div>
      </div>
    </div>
  </div>
</div>

</div>

!!! info "分数解释（与 NovoPsych 一致,筛查用途）"

    - **0–7%**: 无解离体验
    - **7–14%**: 很少有诊断意义的解离体验
    - **15–20%**: 轻度解离症状。可能存在 PTSD 或轻度解离障碍（如解离性失忆、人格解体/现实解体障碍）
    - **21–30%**: 可能存在解离障碍和/或 PTSD **（临界值 >21% 表示临床显著症状）**
    - **31–40%**: 可能存在解离障碍（如 OSDD 或 DID）和 PTSD
    - **41–64%**: 可能患有 DID 或严重解离障碍和 PTSD
    - **64%+**: 严重的解离和创伤后症状。高分也可能反映神经质、寻求注意的行为、症状夸大或装病,或精神病

    **样例均值参考**（帮助理解分数语义）:

    - 普通大学生样本:平均分约 **13%**
    - DID 临床样本:平均分约 **51%**

    **重要提示**:分数需要结合具体困扰与功能受损情况讨论;**高分≠诊断,低分≠无碍**。睡眠不足、物质影响时建议暂缓作答。

!!! note "子量表说明（依据 NovoPsych 公示资料）"

    MID-60 提供与不同诊断相关的子量表信息,帮助临床医生形成可能诊断的印象:

    ### 解离性身份障碍（DID）
    - **近期遗忘**（Amnesia for recent events）- 题目 42, 45, 48, 58 - 临界值 = **10%**

    ### DID 与 OSDD
    - **替换人格意识**（Awareness of alter personalities）- 题目 3, 36, 39, 49, 57 - 临界值 = **20%**
    - **愤怒侵入**（Angry intrusions）- 题目 28, 33, 35, 46, 60 - 临界值 = **18%**
    - **迫害侵入**（Persecutory intrusions）- 题目 22, 37, 44, 56, 59 - 临界值 = **18%**

    ### 人格解体/现实解体障碍（DP/DR）
    - **人格解体/现实解体**（Depersonalization/Derealization）- 题目 2, 7, 9, 13, 25, 47, 50, 53 - 临界值 = **20%**

    ### 解离性失忆
    - **记忆困扰**（Memory distress）- 题目 1, 8, 20, 38, 43, 52 - 临界值 = **30%**
    - **自传记忆丧失**（Autobiographical memory loss）- 题目 16, 19, 24, 29, 34 - 临界值 = **34%**

    ### 创伤后应激障碍（PTSD）
    - **闪回**（Flashbacks）- 题目 4, 15, 31, 40, 54 - 临界值 = **16%**

    ### 功能性神经症状障碍（FNSD/转换障碍）
    - **功能性神经症状**（Functional neurological symptoms）- 题目 5, 10, 14, 18 - 临界值 = **10%**
    - **心因性非癫痫发作**（PNES - Psychogenic Non-Epileptic Seizures）- 题目 26 - 临界值 = **10%**

    ### 一般解离子量表
    - **恍惚**（Trance states）- 题目 21, 27, 30, 32, 41, 51 - 临界值 = **11.7%**
    - **自我困惑**（Identity confusion）- 题目 6, 11, 12, 17, 23, 55 - 临界值 = **33.3%**

!!! warning "工具分级与诊断边界"

    ### 筛查级 vs 诊断级工具

    - **MID-60**:属于**筛查级自评量表**,用于初步识别解离症状,**不能替代正式临床诊断**
    - **[DES-II](Dissociative-Experiences-Scale-DES-II.md)**:同样属于**筛查级工具**,用于快速评估解离体验
    - **SCID-D**（解离障碍结构化临床访谈）:属于**诊断级结构化访谈**,由专业临床医生实施,用于确立正式诊断
    - **DDIS**（解离障碍访谈量表）:属于**诊断级访谈量表**,用于系统评估解离障碍及相关诊断

    ### 使用建议

    1. **MID-60 作为筛查起点**:如果总分 >21% 或任一子量表超过临界值,建议寻求专业评估
    2. **进一步诊断需求**:由具备资质的精神科医生或临床心理师使用 SCID-D 或 DDIS 进行正式诊断
    3. **多维度综合评估**:诊断需结合病史、功能受损、症状持续时间等多方面信息

    **重要提示**:MID-60 结果应始终与临床专业知识结合使用,**高分≠确诊,低分≠排除诊断**。

!!! tip "常见误差与注意事项"

    **评分时请注意避免以下常见误差**:

    1. **高分≠诊断**:分数只是筛查指标,不能单独作为诊断依据
    2. **低分≠无碍**:某些高功能个体可能低估或掩盖症状
    3. **情境影响**:以下情况建议暂缓作答:
        - 睡眠不足或极度疲劳时
        - 物质影响下（酒精、药物等）
        - 急性应激或情绪危机期间
    4. **回忆偏差**:请基于**最近一个月**的真实体验作答,而非极端情况或单次事件
    5. **社会期待效应**:诚实作答比"正确"作答更重要,本工具不存储个人数据

??? example "子量表—题号—临界值对照表（开发者参考）"

    本对照表便于核对与二次开发,所有临界值均为百分数（0–100%）:

    | 子量表英文名 | 子量表中文名 | 题号 | 临界值 | 诊断关联 |
    |------------|------------|------|--------|---------|
    | Amnesia for recent events | 近期遗忘 | 42, 45, 48, 58 | 10% | DID |
    | Awareness of alter personalities | 替换人格意识 | 3, 36, 39, 49, 57 | 20% | DID/OSDD |
    | Angry intrusions | 愤怒侵入 | 28, 33, 35, 46, 60 | 18% | DID/OSDD |
    | Persecutory intrusions | 迫害侵入 | 22, 37, 44, 56, 59 | 18% | DID/OSDD |
    | Depersonalization/Derealization | 人格解体/现实解体 | 2, 7, 9, 13, 25, 47, 50, 53 | 20% | DP/DR |
    | Memory distress | 记忆困扰 | 1, 8, 20, 38, 43, 52 | 30% | 解离性失忆 |
    | Autobiographical memory loss | 自传记忆丧失 | 16, 19, 24, 29, 34 | 34% | 解离性失忆 |
    | Flashbacks | 闪回 | 4, 15, 31, 40, 54 | 16% | PTSD |
    | Functional neurological symptoms | 功能性神经症状 | 5, 10, 14, 18 | 10% | FNSD/转换障碍 |
    | PNES | 心因性非癫痫发作 | 26 | 10% | FNSD/转换障碍 |
    | Trance states | 恍惚 | 21, 27, 30, 32, 41, 51 | 11.7% | 一般解离 |
    | Identity confusion | 自我困惑 | 6, 11, 12, 17, 23, 55 | 33.3% | 一般解离 |

    **计分公式**:子量表分数 = 对应题目均值 × 10（范围 0–100%）

!!! quote "参考"
    Dell, P. F. (2006). The Multidimensional Inventory of Dissociation (MID): A Comprehensive measure of pathological dissociation. *Journal of Trauma & Dissociation, 7*(2), 77-106.

    Dell, P. F., & Lawson, D. (2009). Empirically guided revision of experiences of possession and related phenomena: A cross-cultural examination. *Journal of Trauma & Dissociation, 10*(4), 436-456.
