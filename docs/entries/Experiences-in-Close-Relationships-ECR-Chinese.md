---
title: 亲密关系经历量表中文版（Experiences in Close Relationships, ECR）
tags:

    - scale:ECR
    - scale:评估量表
    - theory:成人依恋
    - theory:依恋理论

topic: 理论与分类
synonyms:

    - 亲密关系经历量表
    - ECR
    - ECR中文版
    - Experiences in Close Relationships
    - 成人依恋量表
    - 依恋焦虑量表
    - 依恋回避量表

description: 亲密关系经历量表中文版（ECR）是成人依恋研究中的常用自评工具，包含依恋焦虑与依恋回避两个维度，适合教育性自我观察与研究资料整理。
updated: 2026-06-15
search:
  boost: 1.5
hide:

    - toc

extra_css:

    - assets/ecr.css

extra_javascript:

    - assets/ecr.js

comments: true
---

# 亲密关系经历量表中文版（Experiences in Close Relationships, ECR）

!!! danger "重要声明"
本页面仅用于教育、自我观察与资料整理，**不构成心理诊断、伴侣评判或治疗建议**。ECR 描述的是亲密关系中的依恋焦虑与依恋回避倾向，不应用来给自己、伴侣或系统成员贴固定标签。

!!! note "版本说明"
下方在线题项为基于 ECR 中文版结构的 **教育性改写版**，用于帮助理解计分方式与维度含义。正式研究、论文写作或临床评估请回到李同归、加藤和生（2006）发表的中文版原文与授权要求。

## 概述

**亲密关系经历量表（Experiences in Close Relationships Inventory, ECR）** 由 Brennan、Clark 与 Shaver 在整合多种成人依恋自评量表后编制，常被用作成人浪漫关系依恋研究中的标准化工具。中文版由李同归、加藤和生修订，发表于《心理学报》2006 年第 38 卷第 3 期。

ECR 采用两个连续维度描述成人依恋：

- **依恋焦虑（Attachment Anxiety）**：担心被拒绝、被抛弃、对方不够在乎自己，常表现为反复确认与关系不安。
- **依恋回避（Attachment Avoidance）**：对亲密、依赖、暴露脆弱或寻求支持感到不自在，常表现为拉开距离或降低情感表达。

低焦虑、低回避通常更接近[安全型成人依恋](Adult-Attachment.md)；高焦虑或高回避则提示个体在亲密关系压力下可能更常使用不同的不安全依恋策略。

## 评分说明

!!! tip "使用说明"

    - 请依据你在 **恋爱或亲密关系中的一般体验** 作答，而不是只看某一次冲突。
    - 每题采用 `1-7` 分：`1 = 非常不同意`，`7 = 非常同意`。
    - 标注“反向计分”的题目会自动换算为 `8 - 原始分`。
    - 两个维度各 18 题，页面显示的是各维度平均分，范围 `1-7`。

## 在线评估

<div id="ecr-app" class="ecr-app">

<div class="ecr-meta">
  <div class="ecr-hint">评分范围 1-7（1=非常不同意，7=非常同意）· 结果仅在本地浏览器即时计算</div>
  <div class="ecr-actions">
    <button id="ecr-reset" class="md-button" type="button">重置</button>
  </div>
</div>

<div class="ecr-divider"></div>

<table class="ecr-table">
  <caption>ECR 中文版教育性题项与评分</caption>
  <colgroup>
    <col style="width:3rem">
    <col>
    <col style="width:auto; min-width:17rem">
  </colgroup>
  <thead>
    <tr><th scope="col">#</th><th scope="col">关系体验描述</th><th scope="col">评分</th></tr>
  </thead>
  <tbody>
    <tr class="ecr-item" data-item="1" data-subscale="avoidance"><td class="ecr-no">1</td><td>总的来说，我不喜欢让恋人知道自己内心深处的感觉。<span class="ecr-dim">回避</span></td><td><div class="ecr-ctrl"><select id="ecr-item1"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item1">-</output></div></td></tr>
    <tr class="ecr-item" data-item="2" data-subscale="anxiety"><td class="ecr-no">2</td><td>我担心我会被抛弃。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item2"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item2">-</output></div></td></tr>
    <tr class="ecr-item" data-item="3" data-subscale="avoidance" data-reverse="true"><td class="ecr-no">3</td><td>我觉得跟恋人亲近是一件惬意的事情。<span class="ecr-dim">回避</span> <span class="ecr-reverse">反向计分</span></td><td><div class="ecr-ctrl"><select id="ecr-item3"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item3">-</output></div></td></tr>
    <tr class="ecr-item" data-item="4" data-subscale="anxiety"><td class="ecr-no">4</td><td>我很担心我的恋爱关系。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item4"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item4">-</output></div></td></tr>
    <tr class="ecr-item" data-item="5" data-subscale="avoidance"><td class="ecr-no">5</td><td>当恋人开始要跟我亲近时，我发现自己在退缩。<span class="ecr-dim">回避</span></td><td><div class="ecr-ctrl"><select id="ecr-item5"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item5">-</output></div></td></tr>
    <tr class="ecr-item" data-item="6" data-subscale="anxiety"><td class="ecr-no">6</td><td>我担心恋人不会像我关心他／她那样关心我。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item6"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item6">-</output></div></td></tr>
    <tr class="ecr-item" data-item="7" data-subscale="avoidance"><td class="ecr-no">7</td><td>当恋人希望跟我非常亲近时，我会觉得不自在。<span class="ecr-dim">回避</span></td><td><div class="ecr-ctrl"><select id="ecr-item7"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item7">-</output></div></td></tr>
    <tr class="ecr-item" data-item="8" data-subscale="anxiety"><td class="ecr-no">8</td><td>我有点担心会失去恋人。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item8"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item8">-</output></div></td></tr>
    <tr class="ecr-item" data-item="9" data-subscale="avoidance"><td class="ecr-no">9</td><td>我觉得对恋人开诚布公，不是一件很舒服的事情。<span class="ecr-dim">回避</span></td><td><div class="ecr-ctrl"><select id="ecr-item9"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item9">-</output></div></td></tr>
    <tr class="ecr-item" data-item="10" data-subscale="anxiety"><td class="ecr-no">10</td><td>我常常希望恋人对我的感情和我对恋人的感情一样强烈。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item10"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item10">-</output></div></td></tr>
    <tr class="ecr-item" data-item="11" data-subscale="avoidance"><td class="ecr-no">11</td><td>我想与恋人亲近，但我又总是会退缩不前。<span class="ecr-dim">回避</span></td><td><div class="ecr-ctrl"><select id="ecr-item11"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item11">-</output></div></td></tr>
    <tr class="ecr-item" data-item="12" data-subscale="anxiety"><td class="ecr-no">12</td><td>我常常想与恋人形影不离，但有时这样会把恋人吓跑。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item12"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item12">-</output></div></td></tr>
    <tr class="ecr-item" data-item="13" data-subscale="avoidance"><td class="ecr-no">13</td><td>当恋人跟我过分亲密的时候，我会感到内心紧张。<span class="ecr-dim">回避</span></td><td><div class="ecr-ctrl"><select id="ecr-item13"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item13">-</output></div></td></tr>
    <tr class="ecr-item" data-item="14" data-subscale="anxiety"><td class="ecr-no">14</td><td>我担心一个人独处。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item14"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item14">-</output></div></td></tr>
    <tr class="ecr-item" data-item="15" data-subscale="avoidance" data-reverse="true"><td class="ecr-no">15</td><td>我愿意把内心的想法和感觉告诉恋人，我觉得这是一件自在的事情。<span class="ecr-dim">回避</span> <span class="ecr-reverse">反向计分</span></td><td><div class="ecr-ctrl"><select id="ecr-item15"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item15">-</output></div></td></tr>
    <tr class="ecr-item" data-item="16" data-subscale="anxiety"><td class="ecr-no">16</td><td>我想跟恋人非常亲密的愿望，有时会把恋人吓跑。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item16"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item16">-</output></div></td></tr>
    <tr class="ecr-item" data-item="17" data-subscale="avoidance"><td class="ecr-no">17</td><td>我试图避免与恋人变得太亲近。<span class="ecr-dim">回避</span></td><td><div class="ecr-ctrl"><select id="ecr-item17"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item17">-</output></div></td></tr>
    <tr class="ecr-item" data-item="18" data-subscale="anxiety"><td class="ecr-no">18</td><td>我需要恋人一再地保证他／她是爱我的。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item18"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item18">-</output></div></td></tr>
    <tr class="ecr-item" data-item="19" data-subscale="avoidance" data-reverse="true"><td class="ecr-no">19</td><td>我觉得我比较容易与恋人亲近。<span class="ecr-dim">回避</span> <span class="ecr-reverse">反向计分</span></td><td><div class="ecr-ctrl"><select id="ecr-item19"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item19">-</output></div></td></tr>
    <tr class="ecr-item" data-item="20" data-subscale="anxiety"><td class="ecr-no">20</td><td>我觉得自己在要求恋人更多地表现出他／她的感觉，以及对恋爱关系的投入程度。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item20"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item20">-</output></div></td></tr>
    <tr class="ecr-item" data-item="21" data-subscale="avoidance"><td class="ecr-no">21</td><td>我发现让我依赖恋人，是一件困难的事情。<span class="ecr-dim">回避</span></td><td><div class="ecr-ctrl"><select id="ecr-item21"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item21">-</output></div></td></tr>
    <tr class="ecr-item" data-item="22" data-subscale="anxiety" data-reverse="true"><td class="ecr-no">22</td><td>我并不是常常担心被恋人抛弃。<span class="ecr-dim">焦虑</span> <span class="ecr-reverse">反向计分</span></td><td><div class="ecr-ctrl"><select id="ecr-item22"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item22">-</output></div></td></tr>
    <tr class="ecr-item" data-item="23" data-subscale="avoidance"><td class="ecr-no">23</td><td>我倾向于不跟恋人过分亲密。<span class="ecr-dim">回避</span></td><td><div class="ecr-ctrl"><select id="ecr-item23"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item23">-</output></div></td></tr>
    <tr class="ecr-item" data-item="24" data-subscale="anxiety"><td class="ecr-no">24</td><td>如果我无法得到恋人的注意和关心，我会心烦意乱或者生气。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item24"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item24">-</output></div></td></tr>
    <tr class="ecr-item" data-item="25" data-subscale="avoidance" data-reverse="true"><td class="ecr-no">25</td><td>我跟恋人什么事情都讲。<span class="ecr-dim">回避</span> <span class="ecr-reverse">反向计分</span></td><td><div class="ecr-ctrl"><select id="ecr-item25"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item25">-</output></div></td></tr>
    <tr class="ecr-item" data-item="26" data-subscale="anxiety"><td class="ecr-no">26</td><td>我发现恋人并不愿意像我所想的那样跟我亲近。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item26"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item26">-</output></div></td></tr>
    <tr class="ecr-item" data-item="27" data-subscale="avoidance" data-reverse="true"><td class="ecr-no">27</td><td>我经常与恋人讨论我所遇到的问题以及我关心的事情。<span class="ecr-dim">回避</span> <span class="ecr-reverse">反向计分</span></td><td><div class="ecr-ctrl"><select id="ecr-item27"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item27">-</output></div></td></tr>
    <tr class="ecr-item" data-item="28" data-subscale="anxiety"><td class="ecr-no">28</td><td>如果我还没有恋人的话，我会感到有点焦虑和不安。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item28"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item28">-</output></div></td></tr>
    <tr class="ecr-item" data-item="29" data-subscale="avoidance" data-reverse="true"><td class="ecr-no">29</td><td>我觉得依赖恋人是很自在的事情。<span class="ecr-dim">回避</span> <span class="ecr-reverse">反向计分</span></td><td><div class="ecr-ctrl"><select id="ecr-item29"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item29">-</output></div></td></tr>
    <tr class="ecr-item" data-item="30" data-subscale="anxiety"><td class="ecr-no">30</td><td>如果恋人不能像我所希望的那样在我身边，我会感到灰心丧气。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item30"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item30">-</output></div></td></tr>
    <tr class="ecr-item" data-item="31" data-subscale="avoidance" data-reverse="true"><td class="ecr-no">31</td><td>我并不在意从恋人那里寻找安慰、听取劝告和得到帮助。<span class="ecr-dim">回避</span> <span class="ecr-reverse">反向计分</span></td><td><div class="ecr-ctrl"><select id="ecr-item31"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item31">-</output></div></td></tr>
    <tr class="ecr-item" data-item="32" data-subscale="anxiety"><td class="ecr-no">32</td><td>如果在我需要的时候，恋人却不在我身边，我会感到沮丧。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item32"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item32">-</output></div></td></tr>
    <tr class="ecr-item" data-item="33" data-subscale="avoidance" data-reverse="true"><td class="ecr-no">33</td><td>在需要的时候，我向恋人求助是很有用的。<span class="ecr-dim">回避</span> <span class="ecr-reverse">反向计分</span></td><td><div class="ecr-ctrl"><select id="ecr-item33"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item33">-</output></div></td></tr>
    <tr class="ecr-item" data-item="34" data-subscale="anxiety"><td class="ecr-no">34</td><td>当恋人不赞同我时，我觉得确实是我不好。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item34"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item34">-</output></div></td></tr>
    <tr class="ecr-item" data-item="35" data-subscale="avoidance" data-reverse="true"><td class="ecr-no">35</td><td>我会在很多事情上向恋人求助，包括寻求安慰和得到承诺。<span class="ecr-dim">回避</span> <span class="ecr-reverse">反向计分</span></td><td><div class="ecr-ctrl"><select id="ecr-item35"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item35">-</output></div></td></tr>
    <tr class="ecr-item" data-item="36" data-subscale="anxiety"><td class="ecr-no">36</td><td>当恋人不花时间和我在一起时，我会感到怨恨。<span class="ecr-dim">焦虑</span></td><td><div class="ecr-ctrl"><select id="ecr-item36"><option value="">请选择</option><option value="1">1 非常不同意</option><option value="2">2</option><option value="3">3</option><option value="4">4 中间</option><option value="5">5</option><option value="6">6</option><option value="7">7 非常同意</option></select><output class="ecr-badge" for="ecr-item36">-</output></div></td></tr>
  </tbody>
</table>

<div class="ecr-divider"></div>

<div id="ecr-results" class="ecr-results">
  <div class="ecr-section-title">评估结果</div>

  <div class="ecr-grid">
    <div class="ecr-score-card">
      <div>
        <div class="ecr-score-label">依恋焦虑均分</div>
        <div class="ecr-hint">18 题平均，范围 1-7</div>
        <div class="ecr-progress" aria-label="依恋焦虑均分可视化"><div id="ecr-anxiety-bar" class="bar"></div></div>
      </div>
      <div><div class="ecr-score-value" id="ecr-anxiety-score">-</div><div id="ecr-anxiety-level" class="ecr-status mid">未完成</div></div>
    </div>
    <div class="ecr-score-card">
      <div>
        <div class="ecr-score-label">依恋回避均分</div>
        <div class="ecr-hint">18 题平均，范围 1-7</div>
        <div class="ecr-progress" aria-label="依恋回避均分可视化"><div id="ecr-avoidance-bar" class="bar"></div></div>
      </div>
      <div><div class="ecr-score-value" id="ecr-avoidance-score">-</div><div id="ecr-avoidance-level" class="ecr-status mid">未完成</div></div>
    </div>
  </div>

  <div class="ecr-score-card">
    <div>
      <div class="ecr-score-label">二维参考</div>
      <div class="ecr-hint" id="ecr-pattern">完成全部题目后显示二维参考。</div>
    </div>
    <div class="ecr-score-value" id="ecr-completion">0/36</div>
  </div>
</div>

</div>

## 解释框架

ECR 的重点不是把人固定分型，而是观察亲密关系压力下的两条策略轴线。为了便于理解，可以把两个维度粗略放入四象限：

| 依恋焦虑 | 依恋回避 | 参考模式    | 常见关系策略                                     |
| -------- | -------- | ----------- | ------------------------------------------------ |
| 低       | 低       | 安全型      | 能在亲近、独立、求助与边界之间较灵活切换         |
| 高       | 低       | 焦虑-沉溺型 | 更担心被抛弃，常需要确认与稳定回应               |
| 低       | 高       | 疏离-回避型 | 更重视独立，亲密或依赖增加时可能拉开距离         |
| 高       | 高       | 恐惧-回避型 | 同时渴望亲密又害怕亲密，可能在靠近和撤离之间摆荡 |

!!! warning "不要把分数当成关系判决"
ECR 分数会受当前关系状态、冲突频率、创伤触发、文化表达方式、关系对象和作答时情绪影响。它适合帮助发现“我在关系压力下如何保护自己”，不适合用来证明某个人“有问题”。

## 量表信息

- **原量表**：Experiences in Close Relationships Inventory（ECR）
- **原始结构**：36 题，依恋焦虑 18 题，依恋回避 18 题
- **评分方式**：1-7 分自评，部分题目反向计分后分别计算两个维度均分
- **中文版研究样本**：371 名中国大学生接受测试，其中 231 名有恋爱经历者进入主要分析；59 名被试在 4 周后重测
- **信度摘要**：李同归、加藤和生（2006）报告中文版依恋回避与依恋焦虑的内部一致性系数分别为 0.82、0.77，重测信度分别为 0.71、0.72
- **效度摘要**：研究报告 ECR 中文版与 RQ、自尊、他人观、STAI、SAD 及恋人评定结果呈现符合理论预期的相关模式

## 在多意识体与创伤语境中的使用

在 DID、OSDD 或其他具有明显部分化体验的人身上，ECR 的作答可能受到“谁在前台”“正在回忆哪段关系”“哪个成员负责亲密/防御”影响。因此建议：

- 如果不同成员的关系策略差异明显，可分别记录“谁在作答”和当时状态；
- 把结果作为[成人依恋](Adult-Attachment.md)与[依恋创伤](Attachment-Trauma.md)讨论的入口，而不是系统整体的固定标签；
- 若作答过程引发强烈情绪、解离或关系冲动，先使用[接地](Grounding.md)与稳定策略，再继续整理关系议题；
- 治疗中应由专业人员结合访谈、关系史、创伤史和功能状态综合理解。

## 相关条目

- [成人依恋（Adult Attachment）](Adult-Attachment.md)
- [依恋理论（Attachment Theory）](Attachment-Theory.md)
- [依恋创伤（Attachment Trauma）](Attachment-Trauma.md)
- [情绪调节（Emotion Regulation）](Emotion-Regulation.md)
- [移情与反移情（Transference and Countertransference）](Transference-Countertransference.md)

## 参考与延伸阅读

1. Brennan, K. A., Clark, C. L., & Shaver, P. R. (1998). Self-report measurement of adult attachment: An integrative overview. In J. A. Simpson & W. S. Rholes (Eds.), _Attachment Theory and Close Relationships_ (pp. 46-76). Guilford Press.
2. 李同归, & 加藤和生. (2006). 成人依恋的测量: 亲密关系经历量表（ECR）中文版. _心理学报_, 38(3), 399-406.
3. Bartholomew, K., & Horowitz, L. M. (1991). Attachment styles among young adults: A test of a four-category model. _Journal of Personality and Social Psychology_, 61(2), 226-244.
4. Fraley, R. C., Waller, N. G., & Brennan, K. A. (2000). An item response theory analysis of self-report measures of adult attachment. _Journal of Personality and Social Psychology_, 78(2), 350-365.
