#!/usr/bin/env python3
"""
测试脚本：验证直接运行其他文件时导入 langchain 是否失败
"""

import sys
import os

print("当前Python执行路径:", sys.executable)
print("sys.path:", sys.path)
print()

try:
    import langchain
    print("OK langchain 导入成功!")
    print(f"langchain 版本: {langchain.__version__}")
except Exception as e:
    print(f"ERROR langchain 导入失败: {type(e).__name__}: {e}")
    import traceback
    print(f"\n详细错误:\n{traceback.format_exc()}")

print()
try:
    import langchain_core
    print("OK langchain_core 导入成功!")
    print(f"langchain_core 版本: {langchain_core.__version__}")
except Exception as e:
    print(f"ERROR langchain_core 导入失败: {type(e).__name__}: {e}")

print()
try:
    from rag import vector_store
    print("OK vector_store 导入成功!")
except Exception as e:
    print(f"ERROR vector_store 导入失败: {type(e).__name__}: {e}")
    import traceback
    print(f"\n详细错误:\n{traceback.format_exc()}")

print()
try:
    from model import factory
    print("OK factory 导入成功!")
except Exception as e:
    print(f"ERROR factory 导入失败: {type(e).__name__}: {e}")
    import traceback
    print(f"\n详细错误:\n{traceback.format_exc()}")

print()
try:
    from rag.rag_server import RagSummarizeService
    print("OK RagSummarizeService 导入成功!")
except Exception as e:
    print(f"ERROR RagSummarizeService 导入失败: {type(e).__name__}: {e}")
    import traceback
    print(f"\n详细错误:\n{traceback.format_exc()}")
