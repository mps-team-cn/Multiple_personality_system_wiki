#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 markdown.py 处理器的所有功能
"""

import os
import sys
from pathlib import Path

# 添加 tools 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.processors.markdown import MarkdownProcessor

# 测试用例
TEST_CASES = [
    # 测试1: 列表标记空格 (CUSTOM001)
    {
        "name": "列表标记空格",
        "input": "-项目1\n*项目2\n1.项目3",
        "should_fix": ["- 项目1", "* 项目2", "1. 项目3"]
    },
    # 测试2: 代码块周围空行 (MD031)
    {
        "name": "代码块周围空行",
        "input": "文本\n```python\ncode\n```\n文本",
        "should_fix": ["", "```python"]
    },
    # 测试3: 列表周围空行 (MD032)
    {
        "name": "列表周围空行",
        "input": "文本\n- 项目1\n- 项目2\n文本",
        "should_fix": ["", "- 项目1"]
    },
    # 测试4: 强调标记空格 (MD037)
    {
        "name": "强调标记空格",
        "input": "** 加粗 ** 和 * 斜体 *",
        "should_fix": ["**加粗**", "*斜体*"]
    },
    # 测试5: 中文加粗空格 (CUSTOM002)
    {
        "name": "中文加粗空格",
        "input": "**中文文本**后面",
        "should_fix": ["**中文文本** 后面"]
    },
    # 测试6: 列表加粗冒号 (CUSTOM003)
    {
        "name": "列表加粗冒号",
        "input": "- **术语**: 定义\n- **概念**：说明",
        "should_fix": ["- **术语** : 定义", "- **概念** : 说明"]
    },
    # 测试7: 链接括号 (CUSTOM004)
    {
        "name": "链接括号",
        "input": "（[链接](url)）",
        "should_fix": ["([链接](url))"]
    },
    # 测试8: 链接前冒号 (CUSTOM005)
    {
        "name": "链接前冒号",
        "input": "参考:[链接](url)",
        "should_fix": ["参考：[链接](url)"]
    },
    # 测试9: 加粗链接
    {
        "name": "加粗链接",
        "input": "**[链接](url)**",
        "should_fix": ["[**链接**](url)"]
    },
    # 测试10: 组合测试
    {
        "name": "组合测试",
        "input": """文本
-**术语**:定义
```python
code
```
文本""",
        "should_fix": ["- **术语** : 定义", "", "```python"]
    }
]

def run_tests():
    """运行所有测试"""
    processor = MarkdownProcessor()
    passed = 0
    failed = 0

    print("=" * 60)
    print("Markdown Processor 功能测试")
    print("=" * 60)

    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n测试 {i}: {test_case['name']}")
        print("-" * 60)
        print(f"输入:\n{test_case['input']}\n")

        # 处理文本
        result = processor.process(test_case['input'])
        print(f"输出:\n{result}\n")

        # 检查是否包含预期的修复
        all_found = True
        for expected in test_case['should_fix']:
            if expected not in result:
                print(f"[X] 未找到预期内容: {expected}")
                all_found = False

        if all_found:
            print(f"[PASS] 测试通过")
            passed += 1
        else:
            print(f"[FAIL] 测试失败")
            failed += 1

    # 总结
    print("\n" + "=" * 60)
    print(f"测试总结: {passed} 通过, {failed} 失败")
    print("=" * 60)

    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
