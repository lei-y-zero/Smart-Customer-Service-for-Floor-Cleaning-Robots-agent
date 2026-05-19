
"""
Agent 工具模块 - 包含各种工具函数
"""
import os
import random
from utils.config_handler import agent_conf
from rag.rag_server import RagSummarizeService
from langchain_core.tools import tool
from utils.path_tool import get_abs_path
from utils.logger_handler import logger


rag=RagSummarizeService()
month_arr = ["2025-01","2025-02","2025-03","2025-04","2025-05","2025-06","2025-07","2025-08","2025-09","2025-10","2025-11","2025-12"]
user_ids=["1001","1002","1003","1004","1005","1006","1007","1008","1009","1010"]
external_data={}

@tool(description="从向量储存中检索参考资料")
def rag_summarize(query:str)->str:
    return rag.rag_summarize(query)

@tool(description="获取指定城市天气，用字符串返回")
def get_weather(city:str)->str:
    return f"{city}天气为晴天，气温26摄氏度，4小时内没有降雨"

@tool(description="获取用户所在城市，用字符串返回")
def get_user_location()->str:
    return random.choice(["深圳", "合肥", "杭州"])

@tool(description="获取用户id，用字符串返回")
def get_user_id()->str:
    return random.choice(user_ids)

@tool(description="获取当前月份，用字符串返回")
def get_current_mouth()->str:
    return random.choice(month_arr)

def generate_external_data():
    if not external_data:
        external_path=get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_path):
            raise FileNotFoundError(f"外部数据{external_path}不存在")

    with open(external_path,"r",encoding='utf-8')as f:
        for line in f.readlines()[1:]:
            arr:list[str]=line.strip().split(",")

            # user_id: str=arr[0].replace(__old='"', __now='')
            # feature: str=arr[1].replace(__old='"', __now='')
            # efficiency: str=arr[2].replace(__old='"', __now='')
            # consumables: str=arr[3].replace(__old='"', __now='')
            # comparison: str=arr[4].replace(__old='"', __now='')
            # time:str=arr[5].replace(__old='"', __now='')
            user_id: str = arr[0].replace('"', '')
            feature: str = arr[1].replace('"', '')
            efficiency: str = arr[2].replace('"', '')
            consumables: str = arr[3].replace('"', '')
            comparison: str = arr[4].replace('"', '')
            time: str = arr[5].replace('"', '')

            if user_id not in external_data:
                external_data[user_id]={}

            external_data[user_id][time]={
                "特征": feature,
                "效率": efficiency,
                "耗材": consumables,
                "对比": comparison,
            }


@tool(description="获取指定用户的指定月份的使用记录")
def fetch_external_data(user_id:str,mouth:str)->str:
    generate_external_data()

    try:
        return external_data[user_id][mouth]
    except KeyError:
        logger.warning(f"[fetch_external_data]未能检索到用户：{user_id}在{mouth}的使用记录")
        return ""

if __name__ == '__main__':
    print(fetch_external_data("1001", "2025-01"))