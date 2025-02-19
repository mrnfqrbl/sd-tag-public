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

    def 生成Markdown(节点, 层级=0):
        """
        递归生成 Markdown 内容。

        参数:
            节点 (dict): 当前节点。
            层级 (int): 当前节点的层级。

        返回值:
            str: 当前节点的 Markdown 内容。
        """

        缩进 = '  ' * 层级  # 缩进
        标题等级 = '#' * (层级 + 1)  # 标题等级
        节点ID = 节点['id']
        节点标题 = 节点['描述'] if '描述' in 节点 else 节点['主题'] # 使用描述或主题作为标题
        markdown = f"{缩进}{标题等级} [{节点标题}](#{节点ID})\n\n"  # 标题和锚点

        for 键, 值 in 节点.items():
            if 键 == '英语提示词':
                markdown += f"{缩进}**{键}:**\n\n"
                markdown += f"{缩进}```text\n{值}\n{缩进}```\n\n" # 使用代码块包裹
            elif 键 not in ['id', 'parent_id', 'type']:  # 排除特定键
                markdown += f"{缩进}**{键}:** {值}\n\n"

        return markdown

    def 生成目录(数据):
        """
        生成 Markdown 目录。

        参数:
            数据 (list): JSON 数据。

        返回值:
            str: Markdown 目录。
        """

        目录 = "## 目录\n\n"

        def 添加目录条目(节点, 层级=0):
            """
            递归添加目录条目。

            参数:
                节点 (dict): 当前节点。
                层级 (int): 当前节点的层级。
            """
            缩进 = '  ' * 层级
            节点ID = 节点['id']
            节点标题 = 节点['描述'] if '描述' in 节点 else 节点['主题']  # 使用描述或主题作为标题
            nonlocal 目录  # 允许修改外部变量 目录
            目录 += f"{缩进}- [{节点标题}](#{节点ID})\n"

            # 递归处理子节点 (这里假设子节点是通过 parent_id 关联的)
            for 子节点 in [n for n in 数据 if n.get('parent_id') == 节点ID]:
                添加目录条目(子节点, 层级 + 1)

        # 从根节点开始生成目录
        for 根节点 in [n for n in 数据 if n.get('parent_id') is None]:
            添加目录条目(根节点)

        return 目录

    # 生成目录
    目录 = 生成目录(数据)

    # 生成内容
    内容 = ""
    for 根节点 in [n for n in 数据 if n.get('parent_id') is None]:
        内容 += 生成Markdown(根节点)

        def 添加子节点内容(节点, 层级=1):
            """
            递归添加子节点内容。

            参数:
                节点 (dict): 当前节点。
                层级 (int): 当前节点的层级。
            """
            nonlocal 内容
            for 子节点 in [n for n in 数据 if n.get('parent_id') == 节点['id']]:
                内容 += 生成Markdown(子节点, 层级)
                添加子节点内容(子节点, 层级 + 1)

        添加子节点内容(根节点)

    # 写入 Markdown 文件
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
        if 文件名.endswith(".json") or 文件名.endswith(".txt"):  # 检查是否为 JSON 或 TXT 文件
            JSON文件路径 = os.path.join(目录路径, 文件名)
            MD文件名 = 文件名.rsplit('.', 1)[0] + ".md"  # 将扩展名改为 .md
            MD文件路径 = os.path.join(目录路径, MD文件名)
            try:
                JSON转MD(JSON文件路径, MD文件路径)
                print(f"已将 {JSON文件路径} 转换为 {MD文件路径}")
            except Exception as e:
                print(f"处理 {JSON文件路径} 时发生错误: {e}")

# 示例用法：
if __name__ == "__main__":
    目录 = "./tags/2025-2-19"  # 当前目录，可以替换为你的实际目录
    处理目录(目录)
