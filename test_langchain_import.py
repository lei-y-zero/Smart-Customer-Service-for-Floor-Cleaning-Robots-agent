#!/usr/bin/env python3
"""
测试 langchain 的导入结构和可用模块
"""

import sys
import os

print("当前Python解释器:", sys.executable)
print("Python版本:", sys.version)
print()

try:
    import langchain
    print("langchain 包已导入")
    print(f"langchain 版本: {langchain.__version__}")

    # 检查 langchain 的目录结构
    print(f"\nlangchain 包路径: {langchain.__path__}")

    import langchain_core
    print(f"\nlangchain_core 版本: {langchain_core.__version__}")

    import langchain_community
    print(f"langchain_community 版本: {langchain_community.__version__}")

    import langchain_text_splitters
    print(f"langchain_text_splitters 版本: {langchain_text_splitters.__version__}")

    import langchain_chroma
    print(f"langchain_chroma 版本: {langchain_chroma.__version__}")

except Exception as e:
    print(f"导入错误: {type(e).__name__}: {e}")
    import traceback
    print(f"\n详细错误信息:\n{traceback.format_exc()}")

print()
print("-" * 50)

try:
    # 列出 langchain 目录下的所有内容
    if 'langchain' in globals():
        langchain_path = langchain.__path__[0]
        print(f"langchain 目录内容: {os.listdir(langchain_path)}")
except Exception as e:
    print(f"无法访问 langchain 目录: {e}")

print()
print("-" * 50)

try:
    if 'langchain_community' in globals():
        langchain_community_path = langchain_community.__path__[0]
        print(f"langchain_community 目录内容: {os.listdir(langchain_community_path)}")
except Exception as e:
    print(f"无法访问 langchain_community 目录: {e}")
