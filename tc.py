import json
import re
import os

def 加载文件(文件路径: str, 类型: str="") -> iter:
    """
    创建一个生成器，每次调用都返回 JSON 文件中的下一个字典。
    同时，将字典中 "中文说明" 和 "英语提示词" 字段的值中的 {xxx} 和 {{xxx}} 进行替换。

    Args:
       文件路径 (str): JSON 文件的路径。
       类型 (str): 指定类型，默认为空字符串。

    Yields:
        dict or None: JSON 文件中的下一个字典，或 None 如果没有更多数据。
    """
    try:
        with open(文件路径, "r", encoding="utf-8") as 文件:
            数据 = json.load(文件)

        if isinstance(数据, list):
            for 项目 in 数据:
                if isinstance(项目, dict):
                    if 类型=="sd":
                        # 修改 "中文说明" 字段
                        if "中文说明" in 项目:
                            项目["中文说明"] = re.sub(r"\{\{([^}]+)}}", r"(\1:1.5)", 项目["中文说明"])
                            项目["中文说明"] = re.sub(r"\{([^}]+)}", r"(\1:1.2)", 项目["中文说明"])

                        # 修改 "英语提示词" 字段
                        if "英语提示词" in 项目:
                            项目["英语提示词"] = re.sub(r"\{\{([^}]+)}}", r"(\1:1.5)", 项目["英语提示词"])
                            项目["英语提示词"] = re.sub(r"\{([^}]+)}", r"(\1:1.2)", 项目["英语提示词"])

                    yield 项目
                else:
                    print(f"警告：JSON 文件中包含非字典元素：{项目}")
            yield None  # 所有字典读取完毕后返回 None
        else:
            print("警告：JSON 文件内容不是列表，请检查文件格式。")
            yield None  # 如果 JSON 内容不是列表，返回 None

    except FileNotFoundError:
        print(f"错误：文件未找到：{文件路径}")
        yield None
    except json.JSONDecodeError:
        print(f"错误：JSON 文件解码失败，请检查文件内容：{文件路径}")
        yield None
    except Exception as e:
        print(f"发生未知错误：{e}")
        yield None


if __name__ == "__main__":
    文件路径列表 = ["ai-t.json", "ai-t-r18.json", "ai-t-r18g.json"]  # 替换为你的 JSON 文件路径
    for 文件路径 in 文件路径列表:
        json读取器 = 加载文件(文件路径, "sd")
        markdown输出 = ""
        输出文件名 = os.path.splitext(文件路径)[0] + ".md"

        while True:
            下一个字典 = next(json读取器)
            if 下一个字典 is None:
                print(f"JSON 文件 {文件路径} 读取完毕。")
                break
            else:
                markdown输出 += f"# {下一个字典['主题']}\n"
                markdown输出 += f"## {下一个字典['中文说明']}\n"
                markdown输出 += f"```\n{下一个字典['英语提示词']}\n```\n"
                markdown输出 += "---\n"  # 分隔符

        with open(输出文件名, "w", encoding="utf-8") as md文件:
            md文件.write(markdown输出)
        print(f"Markdown 数据已保存到 {输出文件名} 文件。")
