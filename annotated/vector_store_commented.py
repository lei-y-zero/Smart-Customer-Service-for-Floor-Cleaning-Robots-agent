# 导入 os，用于文件与目录判断
import os
# 导入 Document 类型（用于类型标注）
from xml.dom.minidom import Document

# 导入日志对象
from utils.logger_handler import logger
# 导入文件处理函数：txt/pdf 加载、目录过滤、md5 计算
from utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
# 导入路径工具（相对路径转绝对路径）
from utils.path_tool import get_abs_path
# 导入 Chroma 向量库封装
from langchain_chroma import Chroma
# 导入文本切分器
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 导入 Chroma 配置
from utils.config_handler import chroma_conf
# 导入嵌入模型
from model.factory import embed_model


# 向量库服务：负责“入库 + 检索器创建”
class VectorStoreService:
    # 构造函数：初始化向量库和切分器
    def __init__(self):
        # 初始化 Chroma 向量库对象
        self.vector_store = Chroma(
            # 指定集合名
            collection_name=chroma_conf["collection_name"],
            # 指定文本转向量函数
            embedding_function=embed_model,
            # 指定向量库持久化目录
            persist_directory=chroma_conf["persist_directory"],
        )
        # 初始化递归字符切分器
        self.spliter = RecursiveCharacterTextSplitter(
            # 每个分片最大长度
            chunk_size=chroma_conf["chunk_size"],
            # 分片重叠长度
            chunk_overlap=chroma_conf["chunk_overlap"],
            # 优先分隔符顺序
            separators=chroma_conf["separators"],
            # 长度函数
            length_function=len,
        )

    # 获取检索器对象（给 RAG 查询用）
    def get_retriever(self):
        # k 代表每次返回多少条最相关文档
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    # 把 data 目录文档加载进向量库
    def load_document(self):
        # 内部函数：检查某个 md5 是否已存在
        def check_md5_hex(md5_for_check: str):
            # 如果 md5 记录文件不存在，就先创建一个空文件
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                # 文件刚创建，说明当前 md5 肯定未处理
                return False
            # 打开 md5 记录文件
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                # 逐行读取历史 md5
                for line in f.readlines():
                    # 去掉行尾空白
                    line = line.strip()
                    # 相同就说明已处理
                    if line == md5_for_check:
                        return True
                # 全部读完也没匹配，说明未处理
                return False

        # 内部函数：保存一个新 md5 到记录文件
        def save_md5_hex(md5_for_check: str):
            # 以追加模式写入 md5
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        # 内部函数：根据文件后缀选择对应加载器
        def get_file_documents(read_path: str):
            # txt 文件走 txt_loader
            if read_path.endswith("txt"):
                return txt_loader(read_path)
            # pdf 文件走 pdf_loader
            if read_path.endswith("pdf"):
                return pdf_loader(read_path)
            # 其他后缀不处理，返回空列表
            return []

        # 扫描 data 目录下允许后缀的文件路径
        allowed_file_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"]),
        )

        # 遍历每个候选文件
        for path in allowed_file_path:
            # 计算当前文件 md5
            md5_hex = get_file_md5_hex(path)

            # 如果 md5 已存在，说明文件已经入库过，直接跳过
            if check_md5_hex(md5_hex):
                logger.info(f"加载知识库 {path} 内容已在知识库中，跳过")
                continue

            # 进入真正入库流程
            try:
                # 把文件加载为 Document 列表
                documents: list[Document] = get_file_documents(path)

                # 如果没有可用文档，记录警告并跳过
                if not documents:
                    logger.warning(f"[加载知识库]{path} 中没有有效文本，跳过")
                    continue

                # 对文档做切分
                split_document: list[Document] = self.spliter.split_documents(documents)

                # 切分后仍为空，记录警告并跳过
                if not split_document:
                    logger.warning(f"[加载知识库]{path} 切片后没有有效文本，跳过")
                    continue

                # 把切分后的文档写入向量库
                self.vector_store.add_documents(split_document)

                # 记录 md5，避免下次重复入库
                save_md5_hex(md5_hex)

                # 记录成功日志
                logger.info(f"[加载知识库]{path} 内容入库成功")

            # 某个文件失败时仅记录错误，不影响其他文件
            except Exception as e:
                logger.error(f"[加载知识库]{path} 加载失败，{str(e)}", exc_info=True)
                continue


# 文件直接运行时执行以下调试代码
if __name__ == "__main__":
    # 创建向量库服务实例
    vs = VectorStoreService()
    # 执行文档入库
    vs.load_document()
    # 获取 retriever
    retriever = vs.get_retriever()
    # 做一次测试检索
    res = retriever.invoke("迷路")
    # 打印检索到的每条文本
    for r in res:
        print(r.page_content)
        print("-" * 20)
