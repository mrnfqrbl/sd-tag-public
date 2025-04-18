import io
from PIL import Image
from PIL import PngImagePlugin
import numpy as np
import time

import numpy as np  # 导入 numpy 库
def 预设文本块(文本块大小列表=[1, 10, 100]):
    """预设文本块."""

    文本块查找表 = {}
    for 文本块大小_KB in 文本块大小列表:
        # 生成文本数据
        文本数据 = "This is some random text data. " * (文本块大小_KB * 1024 *1024 // len("This is some random text data. "))

        # 创建最小 PNG 图像
        宽度 = 1
        高度 = 1
        图像数据 = np.zeros((高度, 宽度, 3), dtype=np.uint8)  # 黑色
        图像 = Image.fromarray(图像数据)

        # 创建元数据
        元数据 = PngImagePlugin.PngInfo()
        元数据.add_text("comment", 文本数据)

        # 保存为 PNG (禁用优化)
        缓冲区 = io.BytesIO()
        图像.save(缓冲区, "PNG", optimize=False, compress_level=0, pnginfo=元数据)
        文件大小 = len(缓冲区.getvalue())

        # 存储到查找表
        文本块查找表[文本块大小_KB] = (文本数据, 文件大小)

    return 文本块查找表

def 生成目标大小的PNG图像(目标大小_MB, 文本块查找表):
    """生成目标大小的 PNG 图像."""

    目标大小_字节 = 目标大小_MB * 1024 * 1024

    # 贪心算法选择文本块
    选择的文本块 = []
    剩余大小 = 目标大小_字节
    for 文本块大小_KB in sorted(文本块查找表.keys(), reverse=True):
        文本数据, 文件大小 = 文本块查找表[文本块大小_KB]
        while 剩余大小 >= 文件大小:
            选择的文本块.append(文本块大小_KB)
            剩余大小 -= 文件大小

    # 创建最小 PNG 图像
    宽度 = 1
    高度 = 1
    图像数据 = np.zeros((高度, 宽度, 3), dtype=np.uint8)  # 黑色
    图像 = Image.fromarray(图像数据)

    # 创建元数据
    元数据 = PngImagePlugin.PngInfo()
    for 文本块大小_KB in 选择的文本块:
        文本数据, 文件大小 = 文本块查找表[文本块大小_KB]
        元数据.add_text("comment", 文本数据)

    # 保存为 PNG (禁用优化)
    缓冲区 = io.BytesIO()
    图像.save(缓冲区, "PNG", optimize=False, compress_level=0, pnginfo=元数据)
    文件大小 = len(缓冲区.getvalue())

    return 图像, 文件大小

# 参数设置
目标大小_MB = 5# 目标文件大小 155MB
文本块大小列表 = [1, 10, 100]  # 文本块大小列表

# 预设文本块
文本块查找表 = 预设文本块(文本块大小列表)

# 记录开始时间
开始时间 = time.time()

# 生成图像
图像, 文件大小 = 生成目标大小的PNG图像(目标大小_MB, 文本块查找表)

# 记录结束时间
结束时间 = time.time()

# 打印文件大小和耗时
print(f"文件大小：{文件大小 / (1024 * 1024):.2f} MB")
print(f"耗时：{结束时间 - 开始时间:.2f} 秒")

# 显示图像 (可选)
# 图像.show()
