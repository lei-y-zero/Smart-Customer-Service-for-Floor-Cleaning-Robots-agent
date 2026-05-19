# 从 LangChain 导入 create_agent，用于组装 Agent
from langchain.agents import create_agent

# 导入模型实例（在 model/factory.py 中创建）
from model.factory import chat_model
# 导入系统提示词加载函数
from utils.prompt_loader import load_system_prompts
# 导入工具函数（星号导入会把文件里工具都带进来）
from agent.tools.agent_tools import *
# 导入中间件函数和报告模式触发工具
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch, fill_context_for_report


# 定义 ReactAgent 类，封装 Agent 的创建和调用
class ReactAgent:
    # 构造函数：初始化一个完整可用的 Agent
    def __init__(self):
        # create_agent 会把模型、提示词、工具、中间件整合起来
        self.agent = create_agent(
            # 指定底层大模型
            model=chat_model,
            # 指定系统提示词（控制整体行为）
            system_prompt=load_system_prompts(),
            # 指定 Agent 可调用的工具列表
            tools=[
                rag_summarize,
                get_weather,
                get_user_id,
                get_user_location,
                get_current_mouth,
                fetch_external_data,
                fill_context_for_report,
            ],
            # 指定中间件（工具监控、模型前日志、动态提示词）
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )

    # 流式执行函数：输入当前问题 + 历史记录，输出流式文本
    def execute_stream(self, query: str, history: list = None):
        # 先准备 Agent 需要的消息结构
        input_dict = {"messages": []}

        # 如果有历史消息，就先追加历史
        if history:
            # 逐条把 history 转成 LangChain 消息字典
            for msg in history:
                input_dict["messages"].append({"role": msg["role"], "content": msg["content"]})

        # 把当前用户问题追加到消息末尾
        input_dict["messages"].append({"role": "user", "content": query})

        # 调用 agent.stream 开启流式推理
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            # 取这一轮 chunk 中最后一条消息（通常是最新输出）
            latest_message = chunk["messages"][-1]
            # 只有有内容时才输出，避免空块
            if latest_message.content:
                # 去掉首尾空白，并补一个换行
                yield latest_message.content.strip() + "\n"


# 仅当此文件直接运行时执行（调试用）
if __name__ == "__main__":
    # 创建 Agent 实例
    agent = ReactAgent()
    # 发送一条测试问题，观察流式输出
    for chunk in agent.execute_stream("生成使用报告"):
        # end="" 避免 print 自动换行，flush=True 立刻刷新控制台
        print(chunk, end="", flush=True)
