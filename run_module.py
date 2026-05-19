#!/usr/bin/env python3
"""
通用模块启动脚本 - 可以运行项目中的任何Python模块
确保在正确的虚拟环境和路径下运行
"""

import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="运行项目中的Python模块")
    parser.add_argument("module", help="要运行的模块路径（如：rag.rag_server 或 rag/rag_server.py）")
    args = parser.parse_args()

    # 获取项目根目录
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

    # 添加项目根目录到 Python 路径
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"Python 路径: {sys.path}")

    try:
        # 处理模块路径
        module_path = args.module
        if module_path.endswith('.py'):
            # 移除 .py 扩展名
            module_path = module_path[:-3]
        # 替换路径分隔符
        module_path = module_path.replace('/', '.').replace('\\', '.')

        print(f"\n正在运行模块: {module_path}")

        # 导入并运行模块
        __import__(module_path)

    except Exception as e:
        print(f"\n❌ 错误: {type(e).__name__}: {e}")
        import traceback
        print(f"\n详细错误信息:\n{traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()
