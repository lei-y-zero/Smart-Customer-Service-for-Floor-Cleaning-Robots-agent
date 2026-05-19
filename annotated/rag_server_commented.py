"""总结服务类：接收用户提问，先检索参考资料，再让模型基于资料生成回答。"""

# 导入 Document 类型（用于类型标注）
from xml.dom.minidom import Document

# 导入字符串输出解析器，把模型输出转为 str
from langchain_core.output_parsers import StrOutputParser
# 导入向量库服务，用于获取 retriever
from rag.vector_store import VectorStoreService
# 导入 RAG 提示词加载函数
from utils.prompt_loader import load_rag_prompts
# 导入提示词模板类
from langchain_core.prompts import PromptTemplate
# 导入聊天模型实例
from model.factory import chat_model


# RAG 总结服务类
class RagSummarizeService(object):
    # 初始化：准备检索器、提示词、模型、链路
    def __init__(self):
        # 保存向量库服务类（注意这里保存的是类，不是实例）
        self.vector_store = VectorStoreService
        # 创建向量库服务实例并拿到 retriever
        self.retriever = self.vector_store().get_retriever()
        # 读取 RAG 专用提示词文本
        self.prompt_text = load_rag_prompts()
        # 把文本提示词编译为 PromptTemplate
        self.prompt_templete = PromptTemplate.from_template(self.prompt_text)
        # 保存模型对象
        self.model = chat_model
        # 初始化 chain（后续直接 invoke）
        self.chain = self._init_chain()

    # 组装 chain：Prompt -> Model -> StrOutputParser
    def _init_chain(self):
        # 使用管道写法串联三段逻辑
        chain = self.prompt_templete | self.model | StrOutputParser()
        # 返回组装好的链对象
        return chain

    # 仅做检索：输入 query，返回相关文档列表
    def retriever_docs(self, query: str) -> list[Document]:
        # 调用 retriever 的 invoke 执行向量召回
        return self.retriever.invoke(query)

    # 完整 RAG：检索 -> 拼接上下文 -> 调模型总结
    def rag_summarize(self, query: str) -> str:
        # 第一步：召回相关文档
        context_docs = self.retriever_docs(query)

        # 第二步：准备上下文字符串
        context = ""
        # 用于给参考文档编号
        counter = 0
        # 遍历所有召回文档
        for doc in context_docs:
            # 编号累加
            counter += 1
            # 拼接“文档内容 + 元数据”到上下文
            context += f"【参考资料{counter}】参考资料: {doc.page_content} | 参考原数据: {doc.metadata}\n"

        # 第三步：把 query + context 喂给 chain 并返回最终文本
        return self.chain.invoke(
            {
                # 对应提示词中的 input 变量
                "input": query,
                # 对应提示词中的 context 变量
                "context": context,
            }
        )


# 文件直接运行时执行下面测试代码
if __name__ == "__main__":
    # 创建服务实例
    rag = RagSummarizeService()
    # 发起测试问题并打印回答
    print(rag.rag_summarize("小户型适合什么样的扫地机器人"))
