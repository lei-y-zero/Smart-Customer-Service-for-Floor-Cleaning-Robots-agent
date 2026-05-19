# 智扫通 - 扫地机器人智能客服

基于 RAG + LangChain 的扫地机器人智能问答系统。

## 功能

- **产品咨询**：推荐、选购指导、功能介绍
- **故障排查**：常见问题诊断与解决
- **维护保养**：使用与维护建议
- **使用报告**：根据用户数据生成个性化报告

## 技术栈

- **LLM**: 阿里云 DashScope (qwen3-max)
- **Embedding**: text-embedding-v4
- **向量数据库**: ChromaDB
- **框架**: LangChain + LangGraph
- **前端**: Streamlit

## 目录结构

```
├── agent/              # Agent 核心（ReAct 模式）
│   └── tools/          # 工具函数
├── config/             # 配置文件
├── data/               # 知识库原始文件
├── model/              # 模型工厂
├── prompt/             # 提示词模板
├── rag/                # RAG 服务
├── utils/              # 工具类
└── app.py              # Streamlit 前端
```

## 快速启动

```bash
# 安装依赖
pip install -r requirements.txt

# 设置 API Key
export DASHSCOPE_API_KEY=your_api_key

# 启动服务
streamlit run app.py --server.port 8501
```

## 部署

已部署至云服务器：`http://162.211.183.231:8501`