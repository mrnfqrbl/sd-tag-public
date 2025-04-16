// 数据源URL
const 数据源URL = 'https://raw.githubusercontent.com/mrnfqrbl/sd-tag-public/main/data/%E6%8F%90%E7%A4%BA%E8%AF%8D.json'; // 替换成你的JSON数据URL

// 获取页面元素
const 搜索框 = document.getElementById('搜索框');
const 标签列表 = document.getElementById('标签列表');
const 提示词列表 = document.getElementById('提示词列表');

// 全局数据存储
let 数据 = [];
let 所有标签 = new Set(); // 使用Set来保证标签的唯一性
let 选中的标签 = new Set();

// 从URL获取JSON数据
async function 获取数据() {
    try {
        const 响应 = await fetch(数据源URL);
        数据 = await 响应.json();
        渲染页面();
    } catch (错误) {
        console.error('获取数据失败:', 错误);
        提示词列表.textContent = '获取数据失败，请检查URL和网络连接。';
    }
}

// 渲染页面
function 渲染页面() {
    提取所有标签();
    渲染标签();
    渲染提示词();
}

// 提取所有标签
function 提取所有标签() {
    for (const key in 数据) {
        if (数据.hasOwnProperty(key)) {
            const 条目 = 数据[key];
            条目.标签.forEach(标签 => 所有标签.add(标签));
        }
    }
}

// 渲染标签
function 渲染标签() {
    标签列表.innerHTML = ''; // 清空标签列表
    所有标签.forEach(标签 => {
        const 标签元素 = document.createElement('span');
        标签元素.classList.add('标签');
        标签元素.textContent = 标签;
        标签元素.addEventListener('click', () => 切换标签(标签));
        标签列表.appendChild(标签元素);
    });
}

// 切换标签选中状态
function 切换标签(标签) {
    if (选中的标签.has(标签)) {
        选中的标签.delete(标签);
    } else {
        选中的标签.add(标签);
    }
    渲染标签(); // 重新渲染标签，更新选中状态
    渲染提示词(); // 重新渲染提示词，应用筛选
}

// 渲染提示词
function 渲染提示词() {
    提示词列表.innerHTML = ''; // 清空提示词列表

    for (const key in 数据) {
        if (数据.hasOwnProperty(key)) {
            const 条目 = 数据[key];

            // 筛选逻辑：如果选择了标签，则必须包含所有选中的标签
            const 是否显示 = 选中的标签.size === 0 || Array.from(选中的标签).every(标签 => 条目.标签.includes(标签));

            // 搜索逻辑：分离、模糊和精确搜索
            const 搜索词 = 搜索框.value.toLowerCase();
            const 搜索条件 = 解析搜索词(搜索词);
            let 是否匹配搜索 = true;

            if (搜索条件.length > 0) {
                是否匹配搜索 = 搜索条件.every(条件 => {
                    let 字段匹配 = false;
                    for (const 字段 in 条目) {
                        if (条目.hasOwnProperty(字段)) {
                            const 值 = 条目[字段];
                            if (typeof 值 === 'string') {
                                if (条件.精确) {
                                    字段匹配 = 值.toLowerCase() === 条件.词;
                                } else {
                                    字段匹配 = 值.toLowerCase().includes(条件.词);
                                }
                            } else if (Array.isArray(值)) {
                                字段匹配 = 值.some(item => typeof item === 'string' && (条件.精确 ? item.toLowerCase() === 条件.词 : item.toLowerCase().includes(条件.词)));
                            }
                            if (字段匹配) break; // 找到匹配字段，跳出字段循环
                        }
                    }
                    return 字段匹配; // 所有搜索条件必须匹配
                });
            }

            if (是否显示 && 是否匹配搜索) {
                const 提示词容器 = document.createElement('div');
                提示词容器.classList.add('提示词容器');
                提示词容器.textContent = 条目.提示词;

                // 点击复制功能
                提示词容器.addEventListener('click', () => {
                    navigator.clipboard.writeText(条目.提示词)
                        .then(() => {
                            alert('提示词已复制到剪贴板！');
                        })
                        .catch(错误 => {
                            console.error('复制提示词失败:', 错误);
                            alert('复制提示词失败，请手动复制。');
                        });
                });

                提示词列表.appendChild(提示词容器);
            }
        }
    }

    // 更新标签的选中状态
    document.querySelectorAll('.标签').forEach(标签元素 => {
        const 标签 = 标签元素.textContent;
        if (选中的标签.has(标签)) {
            标签元素.classList.add('选中');
        } else {
            标签元素.classList.remove('选中');
        }
    });
}

// 解析搜索词：空格分隔，引号精确搜索
function 解析搜索词(搜索词) {
    const 条件 = [];
    const 匹配项 = 搜索词.matchAll(/"([^"]*)"|(\S+)/g); // 匹配引号内的内容或非空白字符
    for (const 匹配 of 匹配项) {
        if (匹配[1]) {
            条件.push({ 词: 匹配[1].toLowerCase(), 精确: true }); // 引号内的内容，精确搜索
        } else if (匹配[2]) {
            条件.push({ 词: 匹配[2].toLowerCase(), 精确: false }); // 非引号内的内容，模糊搜索
        }
    }
    return 条件;
}

// 搜索框事件监听
搜索框.addEventListener('input', 渲染提示词);

// 页面加载时获取数据
获取数据();
