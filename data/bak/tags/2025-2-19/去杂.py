import json

def decrypt_string(encrypted_string):
    """
    解密字符串，移除随机插入的特殊符号。

    Args:
      encrypted_string: 加密后的字符串。

    Returns:
      解密后的字符串。
    """
    special_symbols = ['&', '*', '#', '@', '￥', '%']
    decrypted_string = ""
    for char in encrypted_string:
        if char not in special_symbols:
            decrypted_string += char
    return decrypted_string

def process_json_file_in_place(file_path):
    """
    读取 JSON 文件，解密指定字段，并将结果保存回同一个文件。

    Args:
      file_path: JSON 文件路径。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 遍历 JSON 数据，解密 "中文说明" 和 "英语提示词" 字段
        for item in data:
            for key, value in item.items():
                if isinstance(value, str) and (key == "中文说明" or key == "英语提示词" or key =="唯一id" or key == "主题"):
                    item[key] = decrypt_string(value)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"JSON 文件已处理并保存到 {file_path}")

    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到")
    except json.JSONDecodeError:
        print(f"错误：文件 {file_path} 不是有效的 JSON 文件")
    except Exception as e:
        print(f"发生错误：{e}")

# 示例用法
json_file = "小竹瑟瑟.json"  # 替换为你的 JSON 文件名

process_json_file_in_place(json_file)
