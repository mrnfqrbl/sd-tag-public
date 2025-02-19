import json
import os

def JSON转MD(JSON文件路径, MD文件路径):
    """
    将 JSON 文件转换为 Markdown 文件，保持树状结构并生成目录。

    参数:
        JSON文件路径 (str): JSON 文件路径。
        MD文件路径 (str): 输出 Markdown 文件路径。
    """

    with open(JSON文件路径, 'r', encoding='utf-8') as f:
        数据 = json.load(f)

    def 生成Markdown(节点):
        """
        生成 Markdown 内容，不再处理缩进。

        参数:
            节点 (dict): 当前节点。

        返回值:
            str: 当前节点的 Markdown 内容。
        """

        节点ID = 节点['id']
        节点标题 = 节点['描述'] if '描述' in 节点 else 节点['主题']
        markdown = f"### [{节点标题}](#{节点ID})\n\n"  # 标题和锚点

        for 键, 值 in 节点.items():
            if 键 == '英语提示词':
                markdown += f"**{键}:**\n\n"
                markdown += f"```text\n{值}\n```\n\n"
            elif 键 not in ['id', 'parent_id', 'type']:
                markdown += f"**{键}:** {值}\n\n"

        return markdown

    def 生成目录(数据, 最大递归深度=20):
        """
        生成 Markdown 目录，负责处理缩进以保持层次结构。

        参数:
            数据 (list): JSON 数据。
            最大递归深度 (int): 允许的最大递归深度，防止无限递归。

        返回值:
            str: Markdown 目录。
        """

        目录 = "## 目录\n\n"

        def 添加目录条目(节点, 层级=0, 已访问节点=None):
            """
            递归添加目录条目。

            参数:
                节点 (dict): 当前节点。
                层级 (int): 当前节点的层级。
                已访问节点 (set): 已经访问过的节点 ID 集合，用于检测循环依赖。
            """
            if 已访问节点 is None:
                已访问节点 = set()

            if 节点['id'] in 已访问节点:
                print(f"检测到循环依赖，跳过节点: {节点['id']}")
                return  # 跳过循环依赖的节点

            if 层级 > 最大递归深度:
                print(f"达到最大递归深度，跳过节点: {节点['id']}")
                return  # 达到最大递归深度，停止递归

            缩进 = '  ' * 层级
            节点ID = 节点['id']
            节点标题 = 节点['描述'] if '描述' in 节点 else 节点['主题']
            nonlocal 目录
            目录 += f"{缩进}- [{节点标题}](#{节点ID})\n"

            已访问节点.add(节点['id'])  # 标记当前节点为已访问

            for 子节点 in [n for n in 数据 if n.get('parent_id') == 节点ID]:
                添加目录条目(子节点, 层级 + 1, 已访问节点)

        for 根节点 in [n for n in 数据 if n.get('parent_id') is None]:
            添加目录条目(根节点)

        return 目录

    内容 = ""
    目录 = 生成目录(数据)  # 先生成目录

    def 添加子节点内容(节点, 层级=1, 已访问节点=None):
        """
        递归添加子节点内容。

        参数:
            节点 (dict): 当前节点。
            层级 (int): 当前节点的层级。
            已访问节点 (set): 已经访问过的节点 ID 集合，用于检测循环依赖。
        """
        nonlocal 内容

        if 已访问节点 is None:
            已访问节点 = set()

        if 节点['id'] in 已访问节点:
            print(f"检测到循环依赖，跳过节点: {节点['id']}")
            return  # 跳过循环依赖的节点

        已访问节点.add(节点['id'])  # 标记当前节点为已访问

        for 子节点 in [n for n in 数据 if n.get('parent_id') == 节点['id']]:
            内容 += 生成Markdown(子节点)
            添加子节点内容(子节点, 层级 + 1, 已访问节点)

    for 根节点 in [n for n in 数据 if n.get('parent_id') is None]:
        内容 += 生成Markdown(根节点)
        添加子节点内容(根节点)

    with open(MD文件路径, 'w', encoding='utf-8') as f:
        f.write(目录)
        f.write(内容)


def 处理目录(目录路径):
    """
    处理指定目录下的所有 JSON 文件，并将转换后的 Markdown 文件保存在该目录下。

    参数:
        目录路径 (str): 要处理的目录路径。
    """
    for 文件名 in os.listdir(目录路径):
        if 文件名.endswith(".json") or 文件名.endswith(".txt"):
            JSON文件路径 = os.path.join(目录路径, 文件名)
            MD文件名 = 文件名.rsplit('.', 1)[0] + ".md"
            MD文件路径 = os.path.join(目录路径, MD文件名)
            try:
                JSON转MD(JSON文件路径, MD文件路径)
                print(f"已将 {JSON文件路径} 转换为 {MD文件路径}")
            except Exception as e:
                print(f"处理 {JSON文件路径} 时发生错误: {e}")


if __name__ == "__main__":
    目录 = "./tags/2025-2-19"  # 当前目录，可以替换为你的实际目录
    处理目录(目录)
