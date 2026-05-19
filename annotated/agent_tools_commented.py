"""Agent 工具模块：定义“模型可以调用的动作函数”"""

# 导入 os，用于判断文件是否存在
import os
# 导入 random，用于模拟返回随机值
import random

# 导入 Agent 配置
from utils.config_handler import agent_conf
# 导入 RAG 服务，后面工具会调用它
from rag.rag_server import RagSummarizeService
# 导入 @tool 装饰器，把函数注册成 LangChain 工具
from langchain_core.tools import tool
# 导入路径工具，把相对路径转绝对路径
from utils.path_tool import get_abs_path
# 导入日志器
from utils.logger_handler import logger

# 全局初始化一个 RAG 服务对象
rag = RagSummarizeService()
# 模拟月份列表（注意这是示例数据）
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"]
# 模拟用户 ID 列表
user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010"]
# 外部数据缓存字典
external_data = {}


# 把 RAG 能力封装成工具：给定 query，返回检索总结结果
@tool(description="从向量储存中检索参考资料")
def rag_summarize(query: str) -> str:
    # 直接调用 RAG 服务
    return rag.rag_summarize(query)


# 天气工具（当前实现是静态示例，不是真实天气 API）
@tool(description="获取指定城市天气，用字符串返回")
def get_weather(city: str) -> str:
    # 返回固定模板字符串
    return f"{city}天气为晴天，气温26摄氏度，4小时内没有降雨"


# 获取用户位置工具（示例：随机返回）
@tool(description="获取用户所在城市，用字符串返回")
def get_user_location() -> str:
    # 随机返回一个城市
    return random.choice(["深圳", "合肥", "杭州"])


# 获取用户 ID 工具（示例：随机返回）
@tool(description="获取用户id，用字符串返回")
def get_user_id() -> str:
    # 随机返回一个用户 ID
    return random.choice(user_ids)


# 获取当前月份工具（函数名 mouth 实际语义是 month）
@tool(description="获取当前月份，用字符串返回")
def get_current_mouth() -> str:
    # 随机返回一个月份
    return random.choice(month_arr)


# 读取 external csv，并把数据缓存到 external_data
def generate_external_data():
    # 如果缓存已存在，直接返回，避免重复读取
    if external_data:
        return

    # 读取配置里的外部数据路径，并转绝对路径
    external_path = get_abs_path(agent_conf["external_data_path"])

    # 文件不存在就抛异常
    if not os.path.exists(external_path):
        raise FileNotFoundError(f"外部数据 {external_path} 不存在")

    # 打开 csv 文件
    with open(external_path, "r", encoding="utf-8") as f:
        # 跳过表头，从第二行开始读取
        for line in f.readlines()[1:]:
            # 按逗号拆分成字段数组
            arr: list[str] = line.strip().split(",")

            # 逐列取值并去除双引号
            user_id: str = arr[0].replace('"', "")
            feature: str = arr[1].replace('"', "")
            efficiency: str = arr[2].replace('"', "")
            consumables: str = arr[3].replace('"', "")
            comparison: str = arr[4].replace('"', "")
            time: str = arr[5].replace('"', "")

            # 若该用户首次出现，先初始化字典
            if user_id not in external_data:
                external_data[user_id] = {}

            # 按 user_id + month 存储该月记录
            external_data[user_id][time] = {
                "特征": feature,
                "效率": efficiency,
                "耗材": consumables,
                "对比": comparison,
            }


# 外部记录查询工具：根据 user_id 和 mouth（月）查询
@tool(description="获取指定用户的指定月份的使用记录")
def fetch_external_data(user_id: str, mouth: str) -> str:
    # 先确保外部数据已加载
    generate_external_data()

    # 尝试读取缓存中的记录
    try:
        return external_data[user_id][mouth]
    # 查不到就记录警告并返回空字符串
    except KeyError:
        logger.warning(f"[fetch_external_data] 未能检索到用户 {user_id} 在 {mouth} 的使用记录")
        return ""


# 本文件独立运行时的调试入口
if __name__ == "__main__":
    # 打印一个示例查询
    print(fetch_external_data("1001", "2025-01"))
