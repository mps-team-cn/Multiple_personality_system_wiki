# Google Indexing API 工具 - 测试清单

使用本清单验证 Google Indexing API 工具的完整功能。

## 前置准备

### 环境设置

- [ ] Python 3.8+ 已安装
- [ ] 虚拟环境已创建并激活
- [ ] 依赖已安装: `pip install -r requirements.txt`

### Service Account 配置

- [ ] Google Cloud 项目已创建
- [ ] Indexing API 已启用
- [ ] Service Account 已创建
- [ ] JSON 密钥已下载
- [ ] Service Account 已添加到 Search Console(权限: Owner)

## 基础功能测试

### 1. URL 生成测试

```bash
# 测试 URL 生成
python3 tools/generate_seo_urls.py
```

**预期结果**:

- [ ] 成功生成 URL 列表
- [ ] 包含优先级 1 的核心页面(约 15 个)
- [ ] 包含优先级 2 的高优先级词条(约 58 个)
- [ ] 输出文件 `seo_priority_urls.txt` 已创建

### 2. 帮助信息测试

```bash
# 查看帮助信息
python3 tools/submit_to_google_indexing.py --help
```

**预期结果**:

- [ ] 显示完整的参数说明
- [ ] 显示使用示例
- [ ] 显示环境变量说明

### 3. Dry-run 测试

```bash
# Dry-run 模式
export GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'
python3 tools/submit_to_google_indexing.py --max-priority 1 --dry-run
```

**预期结果**:

- [ ] 显示 "DRY-RUN" 模式提示
- [ ] 列出待提交的 URL
- [ ] 显示 "[DRY-RUN] 将提交: ..." 日志
- [ ] 不实际发送 API 请求
- [ ] 不创建 `google_indexing_log.json`

### 4. 优先级过滤测试

```bash
# 只提取优先级 1
python3 tools/submit_to_google_indexing.py --max-priority 1 --dry-run

# 优先级 1-2
python3 tools/submit_to_google_indexing.py --max-priority 2 --dry-run
```

**预期结果**:

- [ ] 优先级 1: 约 15 个 URL
- [ ] 优先级 1-2: 约 73 个 URL
- [ ] URL 按优先级排序(优先级 1 在前)

### 5. 数量限制测试

```bash
# 限制 5 个
python3 tools/submit_to_google_indexing.py --limit 5 --dry-run
```

**预期结果**:

- [ ] 只显示前 5 个 URL
- [ ] 日志显示 "限制提交数量为: 5 个"

## 认证测试

### 6. 环境变量认证

```bash
# 设置环境变量
export GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'

# 测试认证
python3 tools/submit_to_google_indexing.py --max-priority 1 --limit 1 --dry-run
```

**预期结果**:

- [ ] 成功加载凭证
- [ ] 日志显示 "从环境变量 GOOGLE_SERVICE_ACCOUNT_JSON 加载凭证"
- [ ] 无认证错误

### 7. 文件路径认证

```bash
# 测试文件认证
python3 tools/submit_to_google_indexing.py \
  --credentials ~/.config/gcloud/wiki-indexing-credentials.json \
  --max-priority 1 --limit 1 --dry-run
```

**预期结果**:

- [ ] 成功加载凭证
- [ ] 日志显示 "从文件加载凭证: ..."
- [ ] 无认证错误

### 8. 凭证缺失测试

```bash
# 清除环境变量
unset GOOGLE_SERVICE_ACCOUNT_JSON

# 不提供凭证
python3 tools/submit_to_google_indexing.py --dry-run
```

**预期结果**:

- [ ] 显示错误: "未提供凭证"
- [ ] 提示使用 `--credentials` 或环境变量
- [ ] 程序退出

## API 提交测试

### 9. 单个 URL 提交测试

```bash
# 提交 1 个 URL
python3 tools/submit_to_google_indexing.py --max-priority 1 --limit 1
```

**预期结果**:

- [ ] 显示待提交 URL
- [ ] 要求确认 (y/N)
- [ ] 成功提交: "✓ 成功提交: ..."
- [ ] 创建 `google_indexing_log.json`
- [ ] 显示提交摘要

### 10. 批量提交测试

```bash
# 提交优先级 1 的所有 URL
python3 tools/submit_to_google_indexing.py --max-priority 1
```

**预期结果**:

- [ ] 显示所有待提交 URL
- [ ] 要求确认
- [ ] 逐个提交并显示进度
- [ ] 所有 URL 成功提交
- [ ] 更新 `google_indexing_log.json`
- [ ] 显示完整摘要

### 11. 错误处理测试

#### 权限错误 (403)

```bash
# 使用未授权的 Service Account
python3 tools/submit_to_google_indexing.py --max-priority 1 --limit 1
```

**预期结果**:

- [ ] 显示 "✗ 权限不足 (403)"
- [ ] 提示检查 Search Console 权限
- [ ] 不重试
- [ ] 继续处理其他 URL

#### 配额超限 (429)

```bash
# 超过每日配额后提交
python3 tools/submit_to_google_indexing.py --limit 250
```

**预期结果**:

- [ ] 前 200 个成功
- [ ] 显示 "⚠ 配额超限 (429)"
- [ ] 自动重试 3 次
- [ ] 最终显示 "达到最大重试次数"
- [ ] 或显示 "达到每日配额限制"

## 查询功能测试

### 12. URL 索引状态查询

```bash
# 查询单个 URL
python3 tools/submit_to_google_indexing.py \
  --query https://wiki.mpsteam.cn/entries/DID
```

**预期结果**:

- [ ] 显示 "查询 URL 索引状态"
- [ ] 成功返回索引元数据(如果已索引)
- [ ] 或显示 "URL 未被索引"(如果未索引)
- [ ] 不执行提交操作

### 13. 未索引 URL 查询

```bash
# 查询未提交的 URL
python3 tools/submit_to_google_indexing.py \
  --query https://wiki.mpsteam.cn/entries/New-Entry
```

**预期结果**:

- [ ] 显示 "URL 未被索引"
- [ ] 无错误信息

## 日志和输出测试

### 14. 日志文件验证

```bash
# 提交后检查日志
cat google_indexing_log.json
```

**预期结果**:

- [ ] JSON 格式正确
- [ ] 包含 `timestamp` 字段
- [ ] 包含 `stats` 对象(submitted, failed, skipped)
- [ ] 包含 `submitted_urls` 数组

### 15. 详细日志测试

```bash
# 启用 verbose 模式
python3 tools/submit_to_google_indexing.py \
  --max-priority 1 --limit 5 --verbose --dry-run
```

**预期结果**:

- [ ] 显示调试级别日志
- [ ] 包含详细的执行步骤
- [ ] 显示 API 请求详情

### 16. 提交摘要验证

```bash
# 查看提交摘要
python3 tools/submit_to_google_indexing.py --max-priority 1
```

**预期结果**:

- [ ] 显示总计 URL 数量
- [ ] 显示成功/失败/跳过统计
- [ ] 显示执行时间
- [ ] 如有失败,显示警告信息

## 边界情况测试

### 17. 空 URL 列表

```bash
# 使用不存在的优先级
python3 tools/submit_to_google_indexing.py --max-priority 0 --dry-run
```

**预期结果**:

- [ ] 显示 "没有找到符合条件的 URL"
- [ ] 程序正常退出

### 18. 大批量提交

```bash
# 提交所有 URL
python3 tools/submit_to_google_indexing.py --max-priority 5 --dry-run
```

**预期结果**:

- [ ] 正确处理所有 URL
- [ ] 显示配额警告(如超过 200 个)
- [ ] 性能良好

### 19. 网络错误模拟

```bash
# 断开网络后提交
python3 tools/submit_to_google_indexing.py --max-priority 1 --limit 1
```

**预期结果**:

- [ ] 显示网络错误
- [ ] 自动重试 3 次
- [ ] 最终标记为失败
- [ ] 不崩溃

## CI/CD 集成测试

### 20. GitHub Actions 模拟

```bash
# 模拟 GitHub Actions 环境
export GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'
export MAX_PRIORITY=2
export LIMIT=50

python3 tools/submit_to_google_indexing.py \
  --max-priority $MAX_PRIORITY \
  --limit $LIMIT
```

**预期结果**:

- [ ] 成功从环境变量读取凭证
- [ ] 正确应用参数
- [ ] 生成日志文件供上传

### 21. Workflow 文件验证

```bash
# 检查 workflow 语法
# (需要 GitHub CLI)
gh workflow view .github/workflows/google-indexing.yml.example
```

**预期结果**:

- [ ] YAML 语法正确
- [ ] 输入参数定义完整
- [ ] 步骤逻辑正确

## 安全性测试

### 22. 凭证文件保护

```bash
# 检查 .gitignore
grep -E "service-account|credentials|google_indexing_log" .gitignore
```

**预期结果**:

- [ ] `*service-account*.json` 已忽略
- [ ] `*credentials*.json` 已忽略
- [ ] `google_indexing_log.json` 已忽略

### 23. 凭证不泄露

```bash
# 运行 dry-run 并检查输出
python3 tools/submit_to_google_indexing.py --dry-run 2>&1 | grep -i "private_key"
```

**预期结果**:

- [ ] 输出中不包含 `private_key`
- [ ] 不泄露敏感信息

## 文档完整性测试

### 24. 文档存在性检查

```bash
# 检查所有文档文件
ls -lh docs/dev/Google-Indexing-*.md
ls -lh tools/README_GOOGLE_INDEXING.md
ls -lh examples/google_indexing_example.sh
```

**预期结果**:

- [ ] `Google-Indexing-API-Guide.md` 存在
- [ ] `Google-Indexing-Quick-Start.md` 存在
- [ ] `Google-Indexing-API-Implementation-Summary.md` 存在
- [ ] `Google-Indexing-Testing-Checklist.md` 存在
- [ ] `README_GOOGLE_INDEXING.md` 存在
- [ ] `google_indexing_example.sh` 存在

### 25. 示例脚本测试

```bash
# 运行示例脚本
bash examples/google_indexing_example.sh
```

**预期结果**:

- [ ] 脚本可执行
- [ ] 显示 5 个场景
- [ ] 每个场景可单独执行
- [ ] 无语法错误

## 工具索引更新验证

### 26. 工具索引检查

```bash
# 检查工具索引
grep -A 5 "SEO 优化" docs/dev/Tools-Index.md
```

**预期结果**:

- [ ] 包含 `generate_seo_urls.py`
- [ ] 包含 `submit_to_google_indexing.py`
- [ ] 描述准确

## 性能测试

### 27. 执行时间测试

```bash
# 测试 100 个 URL 的执行时间
time python3 tools/submit_to_google_indexing.py \
  --max-priority 2 --limit 100 --dry-run
```

**预期结果**:

- [ ] 执行时间合理(< 5 秒 for dry-run)
- [ ] 内存使用正常
- [ ] CPU 使用率正常

### 28. 并发安全测试

```bash
# 同时运行多个实例(不推荐,但测试稳定性)
python3 tools/submit_to_google_indexing.py --limit 5 --dry-run &
python3 tools/submit_to_google_indexing.py --limit 5 --dry-run &
wait
```

**预期结果**:

- [ ] 两个实例都成功执行
- [ ] 无竞态条件
- [ ] 日志不混乱

## 回归测试

### 29. 现有工具兼容性

```bash
# 确认 generate_seo_urls.py 仍正常工作
python3 tools/generate_seo_urls.py > /dev/null
echo $?
```

**预期结果**:

- [ ] 退出码为 0
- [ ] 无错误输出

### 30. 依赖冲突检查

```bash
# 检查依赖兼容性
pip check
```

**预期结果**:

- [ ] 无依赖冲突
- [ ] 所有包兼容

## 测试总结

### 必须通过的测试(Critical)

- [ ] 1. URL 生成测试
- [ ] 2. 帮助信息测试
- [ ] 3. Dry-run 测试
- [ ] 6. 环境变量认证
- [ ] 9. 单个 URL 提交测试
- [ ] 14. 日志文件验证
- [ ] 22. 凭证文件保护

### 推荐通过的测试(Recommended)

- [ ] 4. 优先级过滤测试
- [ ] 5. 数量限制测试
- [ ] 7. 文件路径认证
- [ ] 10. 批量提交测试
- [ ] 12. URL 索引状态查询
- [ ] 15. 详细日志测试
- [ ] 24. 文档存在性检查

### 可选测试(Optional)

- [ ] 11. 错误处理测试(需要特殊环境)
- [ ] 18. 大批量提交
- [ ] 20. GitHub Actions 模拟
- [ ] 27. 执行时间测试

---

**测试完成日期**: ___________

**测试人员**: ___________

**测试结果**: □ 全部通过 □ 部分通过 □ 失败

**备注**:
