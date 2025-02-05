import requests
import json
import os

API_KEY = "AIzaSyD0gTs8v3DxAF1VHTy3NxQMbQJROq04vMc"  # 将 YOUR_API_KEY 替换为你的实际 API 密钥
API_URL = "https://gemini-api.mrnf.xyz/v1/models"  # 你尝试访问的 API 端点
CHAT_URL = "https://gemini-api.mrnf.xyz/v1/chat/completions"  # OpenAI 格式的聊天 API 端点
OUTPUT_FILE = "models.json"  # 输出文件名

def 保存json到文件(数据, 文件名):
    """将 JSON 数据格式化并保存到文件"""
    try:
        with open(文件名, 'w', encoding='utf-8') as f:
            json.dump(数据, f, indent=4, ensure_ascii=False)
        print(f"JSON 数据已保存到 {文件名}")
    except Exception as e:
        print(f"保存 JSON 数据到文件时出错：{e}")

def 与api聊天(提示, api_key):
    """与API进行聊天 (OpenAI 格式)"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gemini-2.0-flash-exp",  # 替换为你的模型名称
        "messages": [{"role": "user", "content": 提示}]
    }

    try:
        response = requests.post(CHAT_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"聊天请求失败：{e}")
        if response is not None:
            print(f"响应状态码：{response.status_code}")
            try:
                print(f"响应内容：{response.text}")
            except:
                pass
        return None

def 读取文件内容(文件路径):
    """读取指定文件的内容，并返回字符串"""
    内容 = ""
    if os.path.exists(文件路径):
        try:
            with open(文件路径, "r", encoding="utf-8") as 文件:
                内容 = 文件.read()
                print("文件读取成功！")
        except Exception as e:
            print(f"读取文件时发生错误: {e}")
    else:
        print(f"文件不存在: {文件路径}")
    return 内容
#
# # ------------------- 获取模型列表 -------------------
# # 尝试使用请求头传递 API 密钥 (Authorization: Bearer)
# headers = {
#     "Authorization": f"Bearer {API_KEY}"
# }
#
# response = None  # 初始化 response 变量
#
# try:
#     response = requests.get(API_URL, headers=headers)
#     response.raise_for_status()  # 如果响应状态码不是 2xx，则抛出异常
#
#     data = response.json()
#     print("成功获取模型列表：")
#     保存json到文件(data, OUTPUT_FILE)
#
# except requests.exceptions.RequestException as e:
#     print(f"请求失败：{e}")
#     if response is not None:
#         print(f"响应状态码：{response.status_code}")
#         try:
#             print(f"响应内容：{response.text}")
#         except:
#             pass
#
# # 如果使用请求头传递 API 密钥失败，尝试使用查询参数
# if response is None or response.status_code == 403:
#     print("尝试使用查询参数传递 API 密钥...")
#     try:
#         response = requests.get(API_URL, params={"apikey": API_KEY})
#         response.raise_for_status()
#
#         data = response.json()
#         print("成功获取模型列表：")
#         保存json到文件(data, OUTPUT_FILE)
#
#     except requests.exceptions.RequestException as e:
#         print(f"请求失败：{e}")
#         if response is not None:
#             print(f"响应状态码：{response.status_code}")
#             try:
#                 print(f"响应内容：{response.text}")
#             except:
#                 pass
#
# # 如果以上方法都失败，则输出提示
# if response is None or response.status_code == 403:
#     print("请检查 API 密钥是否正确，并参考 API 文档了解正确的传递方式。")

# ------------------- 聊天功能 -------------------

# 定义文件路径
文件路径 = "./tags生成规范/规范-0.1.md"

# 读取文件内容
md = 读取文件内容(文件路径)
inputt=md+"生成：r18=yes,r18-type=all,数量=10"
print(inputt)

if md:
  chat_response = 与api聊天(md, API_KEY)
  if chat_response:
     print("聊天 API 响应:", chat_response)
