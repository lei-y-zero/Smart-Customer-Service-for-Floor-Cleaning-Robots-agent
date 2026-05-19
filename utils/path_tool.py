"""
为整个项目提供绝对路径
"""
import os
def get_project_root()->str:
    #当前文件绝对路径
    current_file=os.path.abspath(__file__)

    #工程的根目录，先获取当前文件目录
    current_dir=os.path.dirname(current_file)
    #获取工程根目录
    current_root=os.path.dirname((current_dir))

    return current_root

def get_abs_path(relative_path:str)->str:
    #输入绝对路径获得相对路
    #relative_path相对路径
    if relative_path:
        project_root=get_project_root()
        return os.path.join(project_root,relative_path)
    else:
        print("错误")
        return ""

if __name__=='__main__':
    print(get_abs_path("data"))