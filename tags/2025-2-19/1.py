import re
import os

def unescape_markdown(text):
    """
    移除为了防止Markdown渲染而添加的转义符和特殊处理。
    """

    # 1. 移除代码块的 &`\``\`text 和 &`\``\` 前缀/后缀
    text = re.sub(r"&`\\`\\`\\`text\n", "", text)
    text = re.sub(r"&`\\`\\`\\`", "", text)

    # 2. 移除转义的反斜杠
    text = text.replace("\\#", "#")
    text = text.replace("\\*", "*")
    text = text.replace("\\_", "_")
    text = text.replace("\\`", "`")
    text = text.replace("\\\\", "\\")  # 恢复原本的反斜杠

    # 3. 恢复HTML实体 (这里只处理了 < 和 >，可以根据需要添加更多)
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")

    return text

# 获取输入文件名
input_filename = "fase.md"

try:
    # 读取文件内容
    with open(input_filename, "r", encoding="utf-8") as f:
        escaped_markdown = f.read()

    # 反转义Markdown
    unescaped_markdown = unescape_markdown(escaped_markdown)

    # 构建输出文件名
    base, ext = os.path.splitext(input_filename)
    output_filename = base + "_restored" + ext

    # 保存到文件
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(unescaped_markdown)
    print(f"已将恢复后的 Markdown 保存到: {output_filename}")

except FileNotFoundError:
    print(f"错误: 文件未找到: {input_filename}")
except Exception as e:
    print(f"发生错误: {e}")
