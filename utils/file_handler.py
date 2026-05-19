import os
import hashlib

from langchain_community.document_loaders import PyPDFLoader, TextLoader

from utils.logger_handler import logger
from langchain_core.documents import Document
def get_file_md5_hex(filepath:str):  #获取文件md516进制字符

    if not os.path.exists(filepath):
        logger.error(f"[md5计算]文件{filepath}不存在")

    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]路径{filepath}不是文件")

    md5_obj=hashlib.md5()

    chunk_size=4096 #4kb分片，防止文件过大

    try:
        with open(filepath,'rb')as f:
            while chunk :=f.read(chunk_size): #：= 先定义后判断
                md5_obj.update(chunk)

            md5_hex=md5_obj.hexdigest()
            return md5_hex

    except Exception as e:
        logger.error(f"计算机文件{filepath}md5失败,{str(e)}")
        return  None


def listdir_with_allowed_type(path:str,allowed_types:list):  #返回文件夹内的文件列表
    files=[]
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return []

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path,f))
    return tuple(files)


def pdf_loader(file_path:str,passwd=None)->list[Document]:
    return PyPDFLoader(file_path,passwd).load()

def txt_loader(filepath:str )-> list[Document]:
    return  TextLoader(filepath,encoding='utf-8').load()

