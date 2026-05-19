import yaml
from utils.path_tool import get_abs_path
# 直接在 config_handler.py 中实现路径获取函数，避免任何导入问题
# def get_project_root() -> str:
#     current_file = os.path.abspath(__file__)
#     current_dir = os.path.dirname(current_file)
#     project_root = os.path.dirname(current_dir)
#     return project_root
#
# def get_abs_path(relative_path: str) -> str:
#     if relative_path:
#         project_root = get_project_root()
#         return os.path.join(project_root, relative_path)
#     else:
#         print("路径不能为空")
#         return ""

def load_rag_config(config_path:str=get_abs_path("config/rag.yml"),encoding:str='utf-8'):
    with open(config_path,"r",encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)


def load_chroma_config(config_path:str=get_abs_path("config/chroma.yml"),encoding:str='utf-8'):
    with open(config_path,"r",encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)

def load_prompts_config(config_path:str=get_abs_path("config/prompts.yml"),encoding:str='utf-8'):
    with open(config_path,"r",encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)

def load_agent_config(config_path:str=get_abs_path("config/agent.yml"),encoding:str='utf-8'):
    with open(config_path,"r",encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)

rag_conf=load_rag_config()
chroma_conf=load_chroma_config()
prompts_conf=load_prompts_config()
agent_conf=load_agent_config()

if __name__=='__main__':
    print(rag_conf["chat_model_name"])

