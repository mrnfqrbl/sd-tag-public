import gec
import traceback
import sys
async def files_list(self, 路径,子:False):
    if 子:
        logger.info("这是子调用")
    # logger.info(f"初始路径: {路径}")
    # 移除路径开头的 / 或 \

    if not 路径:
        路径 = '.'
    while 路径.startswith('/') or 路径.startswith('\\'):
        路径 = 路径[1:]

    路径 = 路径.replace('/', '\\')  # 替换所有 / 为 \



    if 路径=='\\' or not 路径:
        logger.info(f"路径: {路径}")
        查询路径=self.文件存储根目录
    else:

        查询路径 = os.path.join(self.文件存储根目录, 路径)  # 使用 os.path.join 拼接路径
    logger.info(f"查询路径: {查询路径}")


    files = []
    tasks = []
    try:

        for file_name in os.listdir(查询路径):
            file_path = os.path.join(查询路径, file_name)
            tasks.append(self.get_info(file_path))
        logger.info(":11111")
        files = await asyncio.gather(*tasks)

        files.sort(key=lambda x: (x['type'] == 'file', x['name'].lower()))
        self.文件列表缓存 = files
        logger.info(f"这里是文件列表返回前一秒")

        return files
    except FileNotFoundError as e:

        if 子:
            logger.error(f"子查询路径: {查询路径}")
            logger.error(f"子错误信息: 文件或目录不存在")
        else:

            logger.error(f"查询路径: {查询路径}")
            logger.error(f"错误信息: 文件或目录不存在")

        异常类型 = type(e)
        异常实例 = e
        回溯堆栈 = e.__traceback__

        #gec.全局异常处理(异常类型=异常类型,异常实例=异常实例,回溯堆栈=回溯堆栈)
        return {"status": "error", "message": "文件或目录不存在"}
    except Exception as e:
        logger.error(f"查询路径: {查询路径}")
        logger.error(f"错误信息: {e}")
        return {"status": "error", "message": str(e)}


#除以零结果 =
def 除以零结果():
    try:
        a = 1 / 0
        return a
    except Exception as e:
        异常类型 = type(e)
        异常实例 = e
        回溯堆栈 = e.__traceback__

        gec.全局异常处理(异常类型 =异常类型,异常实例=异常实例,回溯堆栈=回溯堆栈)

除以零结果()

import json
import re
import os

def 加载文件(文件路径: str, 文件类型: str = "sd"):
    """
    加载 JSON 文件，并根据文件类型返回生成器。

    Args:
        文件路径 (str): 要加载的 JSON 文件路径。
        文件类型 (str): 指定文件类型，默认为 "sd"。

    Yields:
        dict: JSON 文件中的每个字典。
    """
    try:
        with open(文件路径, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    # 检查字典是否符合指定的格式
                    if (
                            isinstance(item, dict)
                            and "唯一id" in item
                            and "主题" in item
                            and "中文说明" in item
                            and "英语提示词" in item
                            and isinstance(item["唯一id"], str)
                            and isinstance(item["主题"], str)
                            and isinstance(item["中文说明"], str)
                            and isinstance(item["英语提示词"], str)
                            and re.match(r"^\d{4}\.\d{2}\.\d{2}--\d{5}$", item["唯一id"])  # 检查唯一id的格式
                    ):
                        yield item
                    else:
                        print(f"警告：JSON 文件 {文件路径} 中的条目不符合指定的格式，已跳过。")
                        continue  # 跳过不符合格式的条目
            elif isinstance(data, dict):
                # 检查字典是否符合指定的格式
                if (
                        "唯一id" in data
                        and "主题" in data
                        and "中文说明" in data
                        and "英语提示词" in data
                        and isinstance(data["唯一id"], str)
                        and isinstance(data["主题"], str)
                        and isinstance(data["中文说明"], str)
                        and isinstance(data["英语提示词"], str)
                        and re.match(r"^\d{4}\.\d{2}\.\d{2}--\d{5}$", data["唯一id"])  # 检查唯一id的格式
                ):
                    yield data
                else:
                    print(f"警告：JSON 文件 {文件路径} 不符合指定的格式，已跳过。")
                    yield None
            else:
                print(f"警告：JSON 文件 {文件路径} 内容不是列表或字典，已跳过。")
                yield None
    except FileNotFoundError:
        print(f"错误：文件未找到：{文件路径}")
        yield None
    except json.JSONDecodeError:
        print(f"错误：JSON 文件解码失败，请检查文件内容：{文件路径}")
        yield None
    except Exception as e:
        print(f"发生未知错误：{e}")
        yield None


def 处理目录(目录路径: str, 文件类型: str = "sd"):
    """
    处理指定目录下的所有 JSON 文件，并将结果保存到与输入目录相同的目录。

    Args:
        目录路径 (str): 要处理的目录路径。
        文件类型 (str): 指定文件类型，默认为 "sd"。
    """
    # 如果输入目录为空，则使用当前目录
    if not 目录路径:
        目录路径 = "."
        print(f"输入目录为空，使用当前目录: {os.getcwd()}")

    # 使用输入目录作为输出目录
    输出目录 = 目录路径

    # 确保输出目录存在
    if not os.path.exists(输出目录):
        os.makedirs(输出目录)

    for 文件名 in os.listdir(目录路径):
        文件路径 = os.path.join(目录路径, 文件名)
        # 确保只处理文件，忽略目录
        if os.path.isfile(文件路径):
            # 确保只处理 JSON 文件
            if 文件名.lower().endswith(".json"):
                输出文件名 = os.path.splitext(文件名)[0] + ".md"
                输出文件路径 = os.path.join(输出目录, 输出文件名)

                markdown输出 = ""
                json读取器 = 加载文件(文件路径, 文件类型)
                序号 = 1
                符合格式的数据 = False  # 标记是否有符合格式的数据

                while True:
                    下一个字典 = next(json读取器, None)
                    if 下一个字典 is None:
                        print(f"JSON 文件 {文件路径} 读取完毕。")
                        break
                    else:
                        符合格式的数据 = True  # 至少有一个符合格式的数据
                        markdown输出 += f"# 序号：{序号}\n"
                        markdown输出 += f"## {下一个字典['主题']}\n"
                        markdown输出 += f"### {下一个字典['中文说明']}\n"
                        markdown输出 += f"```\n{下一个字典['英语提示词']}\n```\n"
                        markdown输出 += "---\n"  # 分隔符
                        序号 += 1

                # 只有当存在符合格式的数据时才写入 Markdown 文件
                if 符合格式的数据:
                    with open(输出文件路径, "w", encoding="utf-8") as md文件:
                        md文件.write(markdown输出)
                    print(f"Markdown 数据已保存到 {输出文件路径} 文件。")
                else:
                    print(f"JSON 文件 {文件路径} 不包含任何符合格式的数据，跳过生成 Markdown 文件。")
                    # 可选：删除已存在的 Markdown 文件，如果需要的话
                    # if os.path.exists(输出文件路径):
                    #     os.remove(输出文件路径)
            else:
                print(f"跳过非 JSON 文件: {文件路径}")
        else:
            print(f"跳过目录: {文件路径}")

if __name__ == "__main__":
    输入目录 = "tags/2025-2-19"  # 替换为你的 JSON 文件所在目录，为空则使用当前目录
    # 输入目录=""
    处理目录(输入目录, "sd")
