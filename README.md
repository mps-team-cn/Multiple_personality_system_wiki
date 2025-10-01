# plurality_wiki

[![license](https://img.shields.io/badge/license-CC--BY--SA--4.0-blue)](#)
![status](https://img.shields.io/badge/status-Alpha-orange)
![docsify](https://img.shields.io/badge/built_with-Docsify-5B8DEF)

> 面向贡献者与开发者的仓库说明。面向读者的简明介绍请访问 [`README_wiki.md`](README_wiki.md) 或在线站点。

---

## 在线文档

- **Docsify 站点**：<https://kuliantnt.github.io/plurality_wiki/>
- **面向公众的概览**：见 [`README_wiki.md`](README_wiki.md)，与站点首页保持同步。

---

## 项目概览

本仓库以 Markdown 维护与多重意识体系统相关的知识条目，提供统一的术语、实践与参考资料。
条目内容不替代临床诊断或专业支持，其目标是：**建立共同语言 → 提升理解 → 降低误用风险 → 促进协作**。

---

## 仓库结构

```
entries/
├─ 诊断与临床/           # 诊断框架、症状与相关障碍
├─ 系统角色与类型/       # 身份类型与角色分工
├─ 系统体验与机制/       # 体验维度、机制与状态
└─ 实践与支持/           # 方法论、工具与互助
tools/
└─ pdf_export/           # PDF 导出脚本与说明
```

- `entries/诊断与临床/`：精神医学诊断、创伤与症状说明。
- `entries/系统角色与类型/`：系统内常见的身份类型与角色分工。
- `entries/系统体验与机制/`：系统运作体验、机制与状态变化。
- `entries/实践与支持/`：实践方法、互助工具与支持策略。

全局索引位于 [`index.md`](index.md)，确保新增或调整词条时同步更新。

---

## 本地开发与预览

1. **克隆项目**

   ```bash
   git clone https://github.com/<your_org>/plurality_wiki.git
   cd plurality_wiki
   ```

2. **安装并启动 Docsify（可选）**

   ```bash
   npm install -g docsify-cli # 若已全局安装可跳过
   docsify serve .            # 或使用 npx docsify serve .
   ```

   访问 `http://localhost:3000` 查看实时预览。

3. **导出 PDF（可选）**
   按照 `tools/pdf_export/README_pdf_output.md` 运行脚本，生成带封面与目录的 PDF 合集。

---

## 贡献指南

1. **提交方式**：优先通过 Pull Request；简单问题可新建 Issue。
2. **新增词条**：遵循下方写作规范模板，将文件放入合适的 `entries/` 子目录，并在 `index.md` 与 `README_wiki.md` 需要的位置添加链接或简介。
3. **提交说明**：PR 中列出改动动机、主要变更、潜在风险与相关链接。
4. **推荐标签**：`type:entry` / `type:edit` / `type:reorg` / `risk:content` / `needs:review`。

---

## 写作规范

```markdown
# 术语（英文 / 缩写）

**一句话定义**：——清晰、可操作的定义。

## 核心要点

- 适用范围 / 边界
- 与相近概念的区分
- 临床/社区语境差异（如适用）

## 机制与证据

- 可验证的模型/路径
- 证据等级（文献/共识/经验）与风险提示

## 实务与观察

- 观察维度与记录建议（量表/日记字段/事件触发）
- 干预与自助：流程化步骤与注意事项

## 相关条目

- 参见：条目 A、条目 B

## 参考与延伸阅读

\[1] 作者. 年份. 标题. 期刊/出版社（如有 DOI/链接请附）
```

- 优先给出**中文名 + 英文名/缩写**，首次出现加粗。
- 明确**语境差异**（临床/社区/研究），避免混用。
- 对可能引发风险的内容加注 **⚠ 风险提示** 与**不建议的做法**。
- 采用脚注式或参考文献列表，标明来源与证据水平（如：系统综述 > RCT > 队列 > 专家共识 > 经验）。

---

## 许可证

默认使用 **CC BY-SA 4.0**。如条目另有声明，请以条目内许可为准；衍生作品应采用相同协议共享。
