# 外部依赖函数使用说明（短句版）

只列外部安装包函数。
重点是 LangChain 生态。
不含项目内函数。
不含 Python 标准库函数。

## `langchain_core.tools.tool`
`tool` 是装饰器。
它把普通函数注册成 Agent 工具。
本项目多个工具都用它。
例如 `rag_summarize`、`get_weather`。
常见写法是 `@tool(description="...")`。

## `streamlit.chat_message`
`st.chat_message` 用于渲染对话消息。
它负责显示用户和助手内容。
在 `app.py` 中调用频繁。
常与 `.write()` 一起使用。

## `langchain.agents.create_agent`
`create_agent` 用于创建 Agent。
它接收模型、工具和中间件。
本项目在 `agent/react_agent.py` 中使用。
这是智能体初始化入口。

## `langchain_core.prompts.PromptTemplate.from_template`
这个函数把文本变成提示词模板。
本项目在 RAG 服务里使用它。
先读取 prompt 文本。
再构建模板对象。

## `langchain_core.output_parsers.StrOutputParser`
它把模型输出转成纯字符串。
常放在链路最后一段。
本项目用它统一输出格式。
这样前端更容易显示。

## `langchain_chroma.Chroma`
`Chroma` 用于连接向量库。
本项目用它保存知识向量。
也用它做向量检索。
它是知识库核心依赖。

## `langchain_text_splitters.RecursiveCharacterTextSplitter`
它用于切分长文档。
可设置分块大小和重叠。
本项目在入库前先切分文本。
这会影响召回质量。

## `langchain_community.document_loaders.PyPDFLoader`
它用于加载 PDF 文件。
输出是 `Document` 列表。
本项目通过它导入 PDF 知识。
之后再切分并入向量库。

## `langchain_community.document_loaders.TextLoader`
它用于加载文本文件。
同样输出 `Document` 列表。
本项目用它导入 `.txt` 数据。
流程与 PDF 类似。

## `langchain_community.chat_models.tongyi.ChatTongyi`
它用于创建通义聊天模型。
本项目在模型工厂中实例化它。
Agent 和 RAG 都会复用该模型。
它是主生成模型。

## `langchain_community.embeddings.DashScopeEmbeddings`
它用于创建嵌入模型。
本项目把它传给 Chroma。
文档会先被向量化。
再用于相似度检索。

## `langchain.agents.middleware.wrap_tool_call`
它是工具调用中间件装饰器。
本项目用它包裹 `monitor_tool`。
用于记录工具调用日志。
也可做异常处理。

## `langchain.agents.middleware.before_model`
它在模型调用前触发。
本项目用它记录上下文日志。
这样更容易排查问题。
可观测性更好。

## `langchain.agents.middleware.dynamic_prompt`
它用于动态切换系统提示词。
本项目根据 `report` 标记切换。
普通问答用默认提示词。
报告模式用专用提示词。

## `langgraph.runtime.Runtime`
它主要用于类型标注。
本项目在中间件签名中使用。
用于访问 runtime 上下文。
有助于提升可读性。

## `langchain.tools.tool_node.ToolCallRequest`
它描述一次工具调用请求。
本项目在中间件参数中标注该类型。
可明确请求结构。
也方便调试。

## `langchain_core.messages.ToolMessage`
它是工具消息类型。
本项目在返回类型标注中使用。
用于说明中间件返回结构。
便于后续链路处理。

## `yaml.load`（PyYAML）
它用于解析 YAML 配置。
本项目读取多个 `.yml` 文件。
解析结果是 Python 字典。
用于驱动模型与检索配置。

## `streamlit` 其他常用函数
`st.title` 设置页面标题。
`st.divider` 绘制分割线。
`st.chat_input` 获取用户输入。
`st.spinner` 显示加载状态。
`st.empty` 创建可更新占位块。

## 说明
统计来自当前源码。
若后续改代码，建议同步更新。
