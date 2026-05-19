# 导入 Streamlit，用来搭建 Web 聊天页面
import streamlit as st
# 导入我们自己封装的 Agent
from agent.react_agent import ReactAgent

# 设置页面标题
st.title("智能扫地机器人客服")
# 添加分隔线，让页面更清晰
st.divider()

# 如果会话里还没有 agent，就创建一个
if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

# 如果会话里还没有消息列表，就初始化为空列表
if "message" not in st.session_state:
    st.session_state["message"] = []

# 把历史消息渲染出来
for message in st.session_state["message"]:
    # role 决定显示成 user 还是 assistant
    st.chat_message(message["role"]).write(message["content"])

# 显示输入框，等待用户输入
prompt = st.chat_input()

# 用户有输入时才继续处理
if prompt:
    # 先在页面显示用户输入
    st.chat_message("user").write(prompt)
    # 再把这条用户消息加入历史
    st.session_state["message"].append({"role": "user", "content": prompt})

    # 用于缓存流式输出分片（可选）
    response_message = []

    # 显示“思考中”加载状态
    with st.spinner("智能客服思考中..."):
        # 把问题和历史消息交给 Agent，拿到流式生成器
        res_stream = st.session_state["agent"].execute_stream(prompt, st.session_state["message"])

        # 定义一个辅助函数：边消费边缓存
        def capture(generator, cache_list):
            # 逐块遍历生成器输出
            for chunk in generator:
                # 缓存这块文本
                cache_list.append(chunk)
                # 把这块文本继续往外返回
                yield chunk

        # 用于拼接最终完整回复
        full_response = ""

        # 打开 assistant 的消息容器
        with st.chat_message("assistant"):
            # 创建可重复刷新的占位符
            message_placeholder = st.empty()
            # 逐块处理流式结果
            for chunk in capture(res_stream, response_message):
                # 把每块追加到完整结果
                full_response += chunk
                # 实时刷新，末尾加“▌”模拟打字效果
                message_placeholder.markdown(full_response + "▌")
            # 结束后再渲染一次干净文本
            message_placeholder.markdown(full_response)

        # 把 assistant 的完整回复写入历史，供下一轮上下文使用
        st.session_state["message"].append({"role": "assistant", "content": full_response})
