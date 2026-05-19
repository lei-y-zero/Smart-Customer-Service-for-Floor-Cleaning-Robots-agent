# 学习顺序（新手版）

目标：看懂这个项目里“用户提问 -> Agent 决策 -> 工具调用 -> RAG 检索 -> 最终回复”的完整链路。

## 第 0 步：先看整体结构
1. 前端入口：`app.py`
2. Agent 组装：`agent/react_agent.py`
3. 工具集合：`agent/tools/agent_tools.py`
4. 中间件：`agent/tools/middleware.py`
5. RAG 主链：`rag/rag_server.py`
6. 向量库与入库：`rag/vector_store.py`
7. 配置与提示词：`config/*.yml`、`prompt/*.txt`

## 第 1 步：看用户消息怎么进入系统
打开：`annotated/app_commented.py`

你要重点看：
1. `st.chat_input()` 怎么拿到用户输入。
2. 消息怎么放进 `st.session_state["message"]`。
3. 怎么调用 `execute_stream()` 获得流式回复。
4. 怎么把回复实时渲染到页面。

看完你应该知道：前端只做“收消息 + 展示消息”，不做智能决策。

## 第 2 步：看 Agent 怎么组装
打开：`annotated/react_agent_commented.py`

你要重点看：
1. `create_agent(...)` 的四个核心参数：`model / system_prompt / tools / middleware`。
2. `execute_stream()` 里如何拼 `messages` 上下文。
3. `context={"report": False}` 是怎么参与中间件逻辑的。

看完你应该知道：Agent 是总调度器，决定何时用哪个工具。

## 第 3 步：看 Agent 能做哪些动作
打开：`annotated/agent_tools_commented.py`

你要重点看：
1. `@tool` 的作用（把函数暴露给 Agent）。
2. `rag_summarize()` 如何桥接到 RAG 服务。
3. `get_user_id / get_weather / fetch_external_data` 这类业务工具。
4. `generate_external_data()` 如何读取 CSV 并缓存。

看完你应该知道：工具是 Agent 的“手和脚”。

## 第 4 步：看 RAG 一次调用的完整链路
打开：`annotated/rag_server_commented.py`

你要重点看：
1. `retriever.invoke(query)` 如何召回文档。
2. `context` 怎么拼接（把召回内容喂给模型）。
3. `PromptTemplate | model | StrOutputParser` 这条链。
4. `chain.invoke({"input": query, "context": context})` 的最终生成。

看完你应该知道：RAG 的本质是“先查资料，再让模型基于资料回答”。

## 第 5 步：看知识库如何入库与检索
打开：`annotated/vector_store_commented.py`

你要重点看：
1. `Chroma(...)` 如何初始化向量库。
2. `RecursiveCharacterTextSplitter` 如何切分文档。
3. `txt_loader/pdf_loader` 如何把文件转为 `Document`。
4. `add_documents(...)` 如何写入向量库。
5. `as_retriever(k=...)` 如何得到检索器。

看完你应该知道：RAG 的效果很大程度取决于“入库质量 + 切分参数 + 检索参数”。

## 第 6 步：看中间件（进阶）
打开：`agent/tools/middleware.py`

你要重点看：
1. `monitor_tool`：工具调用监控与上下文标记。
2. `log_before_model`：模型调用前日志。
3. `report_prompt_switch`：根据 context 动态切换提示词。

看完你应该知道：中间件决定了“可观测性”和“多场景切换能力”。

## 第 7 步：看配置与提示词（非常重要）
1. 模型配置：`config/rag.yml`
2. 向量库配置：`config/chroma.yml`
3. 提示词路径：`config/prompts.yml`
4. 主提示词：`prompt/main_prompt_path.txt`
5. RAG 提示词：`prompt/rag_summarize_prompt.txt`
6. 报告提示词：`prompt/report_prompt.txt`

看完你应该知道：这个项目大量行为不是写死在代码里，而是由提示词与配置驱动。

## 一条完整调用链（你可以背下来）
1. 用户在页面输入问题。
2. `app.py` 收到问题并调用 `ReactAgent.execute_stream()`。
3. Agent 读取系统提示词，判断是否需要工具。
4. 若需知识检索，调用 `rag_summarize` 工具。
5. `RagSummarizeService` 先检索，再拼上下文，再生成回答。
6. 结果回到 Agent，Agent 组织成最终答复。
7. `app.py` 流式显示给用户，并写入会话历史。

## 建议的学习节奏
1. 先跑通页面，看到“能聊起来”。
2. 再打日志，观察一次工具调用全过程。
3. 然后改一个小配置（比如 `k` 或 `chunk_size`）看效果变化。
4. 最后再改提示词，体验 Agent 行为变化。

---

如果你刚接触 LangChain，建议先把“Agent + Tool + RAG”这三个概念彻底吃透。
这个项目正好是这三者组合的实战模板。
