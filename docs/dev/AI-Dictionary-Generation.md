# AI 辅助生成搜索词典指南

## 概述

本文档说明如何利用 AI 从大规模搜索索引（3MB+）中生成高质量的自定义词典，以优化中文分词和搜索体验。

## 问题背景

- **现状**: MkDocs 搜索索引约 3MB，包含大量词条、术语和复合词
- **目标**: 生成 `data/user_dict.txt`，改善 jieba 分词效果
- **挑战**: 索引数据超出 AI 单次处理的上下文窗口限制

## 技术约束

### 上下文窗口限制

| 模型              | 上下文窗口     | 3MB 文本        | 可行性  |
| ----------------- | -------------- | --------------- | ------- |
| Claude 3.5 Sonnet | 200K tokens    | ~750K-1M tokens | ❌ 超出 |
| 分批处理          | 200K tokens/批 | 分 4-5 批       | ✅ 可行 |

### 数据特征

- **格式**: JSON（MkDocs 搜索索引）
- **内容**: 文档标题、正文、锚点、元数据
- **语言**: 简体中文为主，含专业术语和英文缩写

## 解决方案设计

### 核心策略

采用 **预处理 + AI 精选 + 增量优化** 三阶段流程：

```text
搜索索引 (3MB)
    ↓
[阶段 1] 统计分析 → 候选词列表 (500KB)
    ↓
[阶段 2] AI 审核 → 精选词典 (200KB)
    ↓
[阶段 3] 测试优化 → 最终词典
```

## 实施步骤

### 阶段 1: 索引分析与候选词提取

#### 1.1 分析索引结构

```bash
python tools/analyze_search_index.py \
  --input site/search/search_index.json \
  --output data/analysis_report.json \
  --stats
```

**输出内容**:

- 文档数量、总字数
- 高频词组统计（2-5 字）
- 专业术语分布
- 潜在误切分案例

#### 1.2 生成候选词列表

```bash
python tools/extract_dict_candidates.py \
  --input site/search/search_index.json \
  --output data/candidates.txt \
  --min-freq 3 \
  --min-length 2 \
  --max-length 8
```

**筛选规则**:

- ✅ 出现频率 ≥ 3 次
- ✅ 长度 2-8 字符
- ✅ 包含中文字符
- ❌ 排除纯数字/标点
- ❌ 排除单字词

**预期输出**:

```text
多重人格 5000
解离性身份障碍 3200
共同意识 2800
系统内沟通 2100
...
```

### 阶段 2: AI 辅助审核与优化

#### 2.1 分批准备

```bash
python tools/split_candidates.py \
  --input data/candidates.txt \
  --batch-size 100 \
  --output data/batches/
```

每批次约 50-100KB（约 15K-30K tokens），确保在上下文窗口内。

#### 2.2 AI 审核提示词

对每个批次使用以下 Prompt:

```markdown

# 任务：优化多重人格系统 Wiki 的搜索词典

## 输入数据

以下是从搜索索引提取的候选词及其频率：

[批次数据]

## 审核标准

1. **保留**: 专业术语、复合词、易误切分词
2. **优化**: 调整词频权重（建议范围 100-10000）
3. **补充**: 添加同义词、缩写、常见变体
4. **删除**: 通用词、无意义组合、过长短语

## 输出格式

词条 词频 词性（可选）

## 示例

解离性身份障碍 5000 n
DID 5000
多重人格 3000 n
系统内沟通 2000
前台人格 2000
```

#### 2.3 批量执行

```bash

# 手动或脚本化执行

for batch in data/batches/*.txt; do
  echo "处理: $batch"
  # 将批次内容提交给 AI
  # 保存 AI 输出到 data/reviewed/
done
```

#### 2.4 合并结果

```bash
python tools/merge_reviewed_batches.py \
  --input data/reviewed/ \
  --output data/user_dict_draft.txt \
  --deduplicate \
  --sort-by-freq
```

### 阶段 3: 测试与优化

#### 3.1 词典格式验证

```bash
python tools/validate_dict.py \
  --input data/user_dict_draft.txt \
  --check-encoding \
  --check-duplicates \
  --check-format
```

#### 3.2 分词效果测试

```bash
python tools/test_dict_segmentation.py \
  --dict data/user_dict_draft.txt \
  --test-corpus docs/entries/*.md \
  --output data/segmentation_test.json
```

**测试指标**:

- 专业术语完整性
- 复合词识别率
- 搜索匹配准确度

#### 3.3 A/B 对比

```bash

# 对比原词典与新词典

python tools/compare_dict_performance.py \
  --old data/user_dict.txt \
  --new data/user_dict_draft.txt \
  --queries data/test_queries.txt
```

#### 3.4 部署

```bash

# 备份原词典

cp data/user_dict.txt data/user_dict.backup.txt

# 应用新词典

cp data/user_dict_draft.txt data/user_dict.txt

# 重新构建搜索索引

mkdocs build
```

## 工具脚本列表

| 脚本                          | 功能             | 状态   |
| ----------------------------- | ---------------- | ------ |
| `analyze_search_index.py`     | 分析索引统计     | 待实现 |
| `extract_dict_candidates.py`  | 提取候选词       | 待实现 |
| `split_candidates.py`         | 分批处理         | 待实现 |
| `merge_reviewed_batches.py`   | 合并 AI 审核结果 | 待实现 |
| `validate_dict.py`            | 词典格式验证     | 待实现 |
| `test_dict_segmentation.py`   | 分词效果测试     | 待实现 |
| `compare_dict_performance.py` | 性能对比         | 待实现 |

## 预期效果

- ✅ 专业术语准确切分（如 "解离性身份障碍" 不被拆分）
- ✅ 复合词完整保留（如 "系统内沟通"）
- ✅ 搜索结果更精准（减少误匹配）
- ✅ 支持缩写和同义词（如 "DID" → "解离性身份障碍"）

## 注意事项

### 质量控制

1. **人工抽查**: AI 审核后随机抽查 10% 条目
1. **灰度测试**: 先在测试环境验证效果
1. **版本管理**: 保留历史词典版本以便回滚

### 性能考虑

- 词典大小建议控制在 50-200KB
- 避免过多低频词（增加内存占用）
- 优先保留高频专业术语

### 维护策略

- 每季度重新分析索引
- 跟踪新增词条和术语
- 监控搜索日志，发现遗漏词汇

## 参考资料

- [jieba 分词文档](https://github.com/fxsjy/jieba)
- [MkDocs 搜索配置](https://www.mkdocs.org/user-guide/configuration/#search)
- 中文分词最佳实践（待创建）

## 更新记录

- 2025-01-XX: 初始版本
- 待更新: 实际执行结果和优化建议
