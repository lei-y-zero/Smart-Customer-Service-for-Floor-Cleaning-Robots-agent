from utils.prompt_loader import load_report_prompts
from langchain.agents import AgentState
from langgraph.runtime import Runtime
from langchain_core.tools import tool
from run_rag_server import result
from utils.logger_handler import logger
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt
from langchain.tools.tool_node import ToolCallRequest
from typing import Callable
from langgraph.types import Command
from langchain_core.messages import ToolMessage
from langchain.agents.middleware import ModelRequest


@tool(description="无入参，无返回值，调用后触发中间键自动为报告生成的场景注入上下文信息，为后续提示词切换注入上下文信息")
def fill_context_for_report():
    return "fill_context_for_report 已调用"

@wrap_tool_call
def monitor_tool(
        #请求的数据封装
        request: ToolCallRequest,
        #执行的函数本身
        handler: Callable[[ToolCallRequest],ToolMessage | Command]
)->ToolMessage | Command:  #工具执行的监控
    """工具执行监控中间件：记录工具调用的名称和参数，并在成功时标记报告生成场景。"""
    logger.info(f"[toll monitor]: 执行工具：{request.tool_call['name']}")
    logger.info(f"[toll monitor]: 传入参数：{request.tool_call['args']}")

    try:
        result=handler(request)
        logger.info(f"[toll monitor]: 工具：{request.tool_call['name']}调用成功")

        if request.tool_call['name']=="fill_context_for_report":
            request.runtime.context["report"]=True


        return result
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败，原因：{str(e)}")
        raise e

@before_model
def log_before_model(
        state:AgentState,  #整个 agent 中的状态信息
        runtime:Runtime,    #记录了整个执行过程中的上下文信息
):
    """模型调用前日志记录中间件：在模型即将执行前输出当前消息状态和最后一条消息内容。"""

    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}条消息")
    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content.strip()}")
    return None

@dynamic_prompt
def report_prompt_switch(request:ModelRequest):
    """动态提示词切换中间件：根据 runtime context 中的 report 标志位切换报告生成提示词。"""

    is_report = request.runtime.context.get("report", False)
    if is_report:
        return load_report_prompts()
    # 不要返回 None，保持默认系统提示词
    return request.system_message.content if hasattr(request, 'system_message') and request.system_message else None


