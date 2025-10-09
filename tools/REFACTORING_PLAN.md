# Tools 目录重构计划

## 📋 重构概览

本文档记录了 tools 目录的重构过程，目标是提升代码质量、可维护性和开发效率。

## 🎯 重构目标

1. **代码质量提升**
   - 消除代码重复
   - 统一架构设计
   - 增强错误处理
   - 提高测试覆盖率

2. **功能整合**
   - 合并相似功能
   - 提取公共模块
   - 统一接口设计

3. **开发体验改善**
   - 简化配置管理
   - 统一日志记录
   - 提供清晰的 CLI 接口

## 📁 新目录结构

```text
tools/
├── core/                 # 核心共享模块
│   ├── __init__.py      # 模块导出
│   ├── frontmatter.py   # 统一的 Frontmatter 解析
│   ├── config.py        # 配置管理系统
│   ├── logger.py        # 日志记录机制
│   └── utils.py         # 通用工具函数
├── processors/          # 内容处理器
│   ├── __init__.py
│   ├── markdown.py      # Markdown 处理器
│   ├── links.py         # 链接处理器
│   └── tags.py          # 标签处理器
├── generators/          # 生成器模块
│   ├── __init__.py
│   ├── search_index.py  # 搜索索引生成
│   ├── tags_index.py    # 标签索引生成
│   └── changelog.py     # 变更日志生成
├── validators/          # 校验器模块
│   ├── __init__.py
│   └── content.py       # 内容校验器
├── cli/                 # CLI 接口
│   ├── __init__.py
│   └── main.py          # 统一 CLI 入口
├── config.json          # 默认配置文件
├── REFACTORING_PLAN.md  # 本文档
└── [原有脚本]           # 保留的脚本（逐步迁移）
```

## 🏗️ 核心模块详解

### 1. Core 模块

#### frontmatter.py

- **功能** : 统一的 YAML frontmatter 解析
- **特性** :
  - 支持严格和宽松模式
  - 完整的错误处理
  - 支持多种字段类型
  - 向后兼容性

#### config.py

- **功能** : 配置管理系统
- **特性** :
  - 支持多种配置来源（文件、环境变量）
  - 类型安全的数据类
  - 自动路径解析
  - 配置验证

#### logger.py

- **功能** : 统一日志记录
- **特性** :
  - 可配置的日志级别和格式
  - 文件轮转支持
  - 多处理器支持
  - 性能友好的日志缓存

#### utils.py

- **功能** : 通用工具函数
- **特性** :
  - 文件操作工具
  - 文本处理工具
  - 装饰器（计时、重试等）
  - 数据处理工具

### 2. Processors 模块

#### markdown.py（待实现）

- 基于 `fix_markdown.py` 重构
- 支持可配置的修复规则
- 批量处理能力
- 预览模式

#### links.py（待实现）

- 基于 `check_links.py` 重构
- 支持白名单配置
- 内外链接分类检查
- 修复建议

#### tags.py（待实现）

- 整合标签相关功能
- 基于 `retag_and_related.py` 和 `generate_tags_index.py`
- 智能标签提取
- 相关性分析

### 3. Generators 模块

#### search_index.py（待实现）

- 基于 `build_search_index.py` 重构
- 支持多种搜索格式
- 增量更新能力
- 性能优化

#### tags_index.py（待实现）

- 基于 `generate_tags_index.py` 重构
- 支持自定义排序
- 分组显示
- 统计信息

#### changelog.py（待实现）

- 基于 `gen_changelog_by_tags.py` 重构
- 支持多种输出格式
- 自定义过滤规则
- 模板化输出

### 4. Validators 模块

#### content.py（待实现）

- 基于 `gen-validation-report.py` 重构
- 全面的内容校验
- 可配置的规则
- 详细的报告生成

### 5. CLI 模块

#### main.py

- 统一的命令行接口
- 子命令支持
- 全局选项处理
- 友好的错误提示

## 📅 实施计划

### 第一阶段：基础设施（已完成 ✅）

- [x] 创建新的目录结构
- [x] 实现核心模块
- [x] 建立配置系统
- [x] 统一日志记录
- [x] 创建 CLI 框架

### 第二阶段：处理器实现（已完成 ✅）

- [x] 实现 MarkdownProcessor
- [x] 整合 fix_markdown.py 功能（MD009, MD012, MD022, MD028, MD031, MD032, MD034, MD037, MD040, MD047）
- [x] 整合 fix_bold_format.py 功能（加粗空格、链接括号、加粗链接）
- [x] 整合 fix_list_bold_colon.py 功能（列表加粗冒号格式）
- [x] 实现 LinkProcessor
- [x] 实现 TagProcessor
- [x] 功能测试（2025-10-07）
- [ ] 单元测试编写（待定）

### 第三阶段：生成器实现（部分取消 ⚠️）

- [x] ~~重构搜索索引生成器~~ - MkDocs Material search 插件自动处理
- [x] ~~重构标签索引生成器~~ - MkDocs Material tags 插件自动处理
- [ ] 重构变更日志生成器 - 保留 `gen_changelog_by_tags.py`
- [ ] 性能测试和优化

### 第四阶段：校验器实现（待定 ⏳）

- [ ] 实现内容校验器
- [ ] 配置化规则系统
- [ ] 报告模板系统

### 第五阶段：迁移和集成（待定 ⏳）

- [ ] 逐步迁移现有脚本
- [ ] 向后兼容性保证
- [ ] 文档更新
- [ ] 用户培训

## 🔄 迁移策略

### 现有脚本处理

1. **保留策略**
   - 在重构完成前保留所有现有脚本
   - 新旧系统并行运行
   - 逐步验证新系统稳定性

2. **迁移顺序**
   - ✅ `fix_markdown.py` → `processors/markdown.py` (2025-10-07)
   - ✅ `fix_bold_format.py` → `processors/markdown.py` (2025-10-07)
   - ✅ `fix_list_bold_colon.py` → `processors/markdown.py` (2025-10-07)
   - ✅ `check_links.py` → `processors/links.py`
   - ✅ ~~`generate_tags_index.py` + `retag_and_related.py` → `processors/tags.py`~~ - 已废弃，移至 `deprecated/`
   - ~~`build_search_index.py` → `generators/search_index.py`~~ - MkDocs 插件替代
   - `gen-validation-report.py` → `validators/content.py`
   - `gen_changelog_by_tags.py` → `generators/changelog.py`

3. **兼容性保证**
   - 保留原有命令行接口
   - 提供迁移工具
   - 详细的变更日志

## 🧪 测试策略

### 单元测试

- 每个模块独立测试
- 覆盖率目标：90%+
- Mock 外部依赖

### 集成测试

- 端到端功能测试
- 性能基准测试
- 错误场景测试

### 回归测试

- 对比新旧系统输出
- 确保功能一致性
- 性能对比分析

## 📊 性能目标

- **启动时间** : < 1秒
- **处理速度** : 提升 30%+
- **内存使用** : 减少 20%+
- **并发支持** : 多线程处理

## 🔧 使用示例

### 基本用法

```bash

# 修复 Markdown 格式

python -m tools.cli.main fix-md entries/

# 检查链接

python -m tools.cli.main check-links --root .

# 生成搜索索引

python -m tools.cli.main search-index --output assets/search-index.json

# 生成标签索引

python -m tools.cli.main tags-index

# 校验内容

python -m tools.cli.main validate --strict

# 启动预览

python -m tools.cli.main preview --port 4173 --docsify
```

### 高级用法

```bash

# 使用自定义配置

python -m tools.cli.main --config custom.json fix-md

# 详细输出

python -m tools.cli.main --verbose validate

# 预览模式

python -m tools.cli.main fix-md --dry-run
```

## 📝 注意事项

1. **依赖管理** : 新模块可能需要额外的 Python 包
2. **配置迁移** : 现有配置可能需要调整
3. **路径处理** : 确保跨平台兼容性
4. **文档更新** : 及时更新用户文档

## 🤝 贡献指南

1. **开发规范** : 遵循 PEP 8 和项目编码规范
2. **测试要求** : 新功能必须包含测试
3. **文档更新** : 重大变更需要更新文档
4. **向后兼容** : 避免破坏性变更

## 📚 相关文档

- [贡献指南](../docs/CONTRIBUTING/index.md)
- [维护者手册](../docs/ADMIN_GUIDE.md)
- [工具使用说明](../docs/tools/README.md)
- [API 文档](../docs/API.md) (待创建)

---

**最后更新** : 2025-10-05
**维护者** : Plurality Wiki Team
