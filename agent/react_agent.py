from aiohttp.web_middlewares import middleware
from langchain.agents import create_agent

from model.factory import chat_model
import streamlit
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tools import *
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch, fill_context_for_report


class ReactAgent:
    def __init__(self):
        self.agent=create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[rag_summarize,get_weather,get_user_id,get_user_location,get_current_mouth,
                   fetch_external_data,fill_context_for_report],
            middleware=[monitor_tool,log_before_model,report_prompt_switch],
        )

    def execute_stream(self, query: str, history: list = None):
        """
        执行流式查询，支持历史上下文

        Args:
            query: 当前查询内容
            history: 历史会话上下文，格式为 [{"role": "user/assistant", "content": "消息内容"}]
        """
        input_dict = {"messages": []}

        # 添加历史上下文
        if history:
            for msg in history:
                input_dict["messages"].append({"role": msg["role"], "content": msg["content"]})

        # 添加当前查询
        input_dict["messages"].append({"role": "user", "content": query})

        # 第三个参数context就是上下文runtime的信息，就是提示词做切换的标记
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip() + "\n"

if __name__ == '__main__':
    agent=ReactAgent()

    for chunk in agent.execute_stream("生成使用报告"):
        print(chunk,end="",flush=True)