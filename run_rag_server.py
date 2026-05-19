#!/usr/bin/env python3
"""
项目启动脚本 - 确保在正确的虚拟环境和路径下运行
"""

import sys
import os

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 添加项目根目录到 Python 路径
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print(f"项目根目录: {PROJECT_ROOT}")
print(f"Python 路径: {sys.path}")
print()

try:
    # 导入并运行 RAG 服务
    from rag.rag_server import RagSummarizeService
    print("OK 成功导入 RagSummarizeService")

    # 测试运行
    print("\n启动 RAG 服务测试:")
    print("-" * 50)
    rag = RagSummarizeService()
    result = rag.rag_summarize("小户型适合什么样的扫地机器人")
    print(f"\nOK 回复成功:\n{result}")

except Exception as e:
    print(f"\nERROR 错误: {type(e).__name__}: {e}")
    import traceback
    print(f"\n详细错误信息:\n{traceback.format_exc()}")
    sys.exit(1)
