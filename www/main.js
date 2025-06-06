// 数据源URL
const 数据源地址 = 'https://raw.githubusercontent.com/mrnfqrbl/sd-tag-public/main/data/%E6%8F%90%E7%A4%BA%E8%AF%8D.json';
const 分类映射数据源地址 = 'https://raw.githubusercontent.com/mrnfqrbl/sd-tag-public/main/data/%E5%88%86%E7%B1%BB%E6%95%B0%E6%8D%AE%E6%98%A0%E5%B0%84.json';

// 获取页面元素
const 搜索框 = document.getElementById('搜索框');
const 标签列表容器 = document.getElementById('标签列表');
const 提示词列表容器 = document.getElementById('提示词列表');
const 分类导航栏容器 = document.getElementById('分类导航栏');
const 已选标签区域容器 = document.getElementById('已选标签区域');

// 全局数据存储
let 提示词数据 = []; // 存储从数据源获取的提示词数据
let 所有标签 = new Set(); // 存储所有不重复的标签
let 选中的标签 = new Set(); // 存储用户选中的标签
let 分类映射 = {}; // 存储标签到分类的映射关系
let 分类字典 = {}; // 存储分类ID到分类名称的映射关系
let 当前分类 = null; // 存储当前选中的分类
let 过滤后的提示词数据 = []; // 存储经过筛选后的提示词数据

const 其他分类ID = "其他"; // 其他分类的ID
const 其他分类名称 = "其他"; // 其他分类的名称

// -------------------- 数据获取与初始化 --------------------

/**
 * 初始化应用，按顺序获取数据、分类映射并渲染页面。
 */
async function 初始化应用() {
    try {
        await 获取数据();
        await 获取分类映射数据();
        const 分类ID列表 = Object.keys(分类字典);
        if (分类ID列表.length > 0) {
            当前分类 = 分类ID列表[0];
            console.log(`默认选择分类: ${当前分类}`);
        }
        渲染页面();
    } catch (错误) {
        console.error('应用初始化失败:', 错误);
        提示词列表容器.textContent = '应用初始化失败，请检查数据源和网络连接。';
    }
}

/**
 * 从数据源地址获取提示词数据。
 */
async function 获取数据() {
    try {
        console.log('开始获取提示词数据...');
        const 响应 = await fetch(数据源地址);

        // 检查响应状态码
        if (!响应.ok) {
            throw new Error(`获取数据失败，状态码: ${响应.status}`);
        }

        const jsonData = await 响应.json();

        // 检查数据结构
        if (typeof jsonData !== 'object' || jsonData === null) {
            throw new Error('数据结构不正确，不是一个有效的 JSON 对象。');
        }

        // 将嵌套字典的值转换为数组
        提示词数据 = Object.values(jsonData);

        // 检查转换后的数据是否是数组
        if (!Array.isArray(提示词数据)) {
            throw new Error('转换后的数据不是数组，请检查数据源。');
        }

        console.log('提示词数据获取成功:', 提示词数据);
    } catch (错误) {
        console.error('获取提示词数据失败:', 错误);
        throw 错误; // 抛出错误，以便在初始化应用中处理
    }
}

/**
 * 从分类映射数据源地址获取分类映射和分类字典数据。
 */
async function 获取分类映射数据() {
    try {
        console.log('开始获取分类映射数据...');
        const 响应 = await fetch(分类映射数据源地址);
        const 分类数据 = await 响应.json();
        分类映射 = 分类数据["词语分类映射"] || {};
        分类字典 = 分类数据["分类字典"] || {};

        // 添加 "其他" 分类
        分类字典[其他分类ID] = 其他分类名称;

        console.log('分类映射数据获取成功:', 分类数据);
        console.log('分类映射:', 分类映射);
        console.log('分类字典:', 分类字典);
    } catch (错误) {
        console.error('获取分类映射数据失败:', 错误);
        // 可以选择是否继续，或者显示错误信息
    }
}

// -------------------- 页面渲染 --------------------

/**
 * 渲染页面的主要元素：分类导航栏、标签列表、已选标签区域和提示词列表。
 */
function 渲染页面() {
    console.log('开始渲染页面...');
    渲染分类导航栏();
    提取所有标签();
    渲染标签列表();
    渲染已选标签区域();
    更新过滤后的提示词数据();
    渲染提示词列表();
    console.log('页面渲染完成。');
}

/**
 * 渲染分类导航栏，允许用户按分类筛选标签和提示词。
 */
function 渲染分类导航栏() {
    console.log('开始渲染分类导航栏...');
    分类导航栏容器.innerHTML = ''; // 清空分类导航栏

    for (const 分类ID in 分类字典) {
        if (分类字典.hasOwnProperty(分类ID)) {
            const 分类名称 = 分类字典[分类ID];
            const 分类按钮 = 创建分类按钮(分类ID, 分类名称);
            分类导航栏容器.appendChild(分类按钮);
            console.log(`添加分类按钮: ${分类名称} (ID: ${分类ID})`);
        }
    }
    console.log('分类导航栏渲染完成。');
}

/**
 * 创建一个分类按钮元素。
 * @param {string} 分类ID - 分类ID.
 * @param {string} 分类名称 - 分类名称.
 * @returns {HTMLButtonElement} - 创建的分类按钮元素.
 */
function 创建分类按钮(分类ID, 分类名称) {
    const 分类按钮 = document.createElement('button');
    分类按钮.textContent = 分类名称;
    分类按钮.addEventListener('click', () => 切换分类(分类ID));
    // 根据当前分类，决定是否添加 data-被选择 属性
    if (分类ID === 当前分类) {
        分类按钮.dataset.被选择 = "true"; // 添加 data-被选择 属性
        console.log(`默认选中分类按钮: ${分类名称} (ID: ${分类ID})`);
    }
    return 分类按钮;
}

/**
 * 切换当前选中的分类，并更新标签列表和提示词列表。
 * @param {string} 分类ID - 要切换到的分类ID.
 */
function 切换分类(分类ID) {
    console.log(`切换分类到: ${分类ID}`);
    当前分类 = 分类ID;
    渲染分类导航栏(); // 重新渲染分类导航栏
    渲染标签列表(); // 重新渲染标签列表，应用分类筛选
    更新过滤后的提示词数据(); // 更新过滤后的提示词数据
    渲染提示词列表(); // 重新渲染提示词列表，应用分类筛选
}

/**
 * 从提示词数据中提取所有不重复的标签。
 */
function 提取所有标签() {
    console.log('开始提取所有标签...');
    所有标签.clear(); // 清空所有标签

    // 检查数据类型
    if (!Array.isArray(提示词数据)) {
        console.error('提示词数据不是数组，无法提取标签。');
        return; // 停止提取标签
    }

    提示词数据.forEach(条目 => {
        条目.标签.forEach(标签 => 所有标签.add(标签));
    });
    console.log('所有标签提取完成:', 所有标签);

    // 将不在分类映射中的标签添加到 "其他" 分类
    所有标签.forEach(标签 => {
        if (分类映射[标签] === undefined) {
            分类映射[标签] = 其他分类ID;
            console.log(`将标签 "${标签}" 添加到 "其他" 分类`);
        }
    });
}

/**
 * 渲染标签列表，根据当前选中的分类进行筛选。
 */
function 渲染标签列表() {
    console.log('开始渲染标签列表...');
    标签列表容器.innerHTML = ''; // 清空标签列表

    所有标签.forEach(标签 => {
        // 如果有当前分类，则只显示属于该分类的标签
        console.log(`标签`,标签);
        console.log(`标签映射`,分类映射[标签]);
        console.log(`当前分类`,当前分类);

        if (当前分类 && String(分类映射[标签]) !== 当前分类) {
            console.log(`跳过标签 "${标签}"，不属于当前分类 "${当前分类}"`);
            return; // 跳过不属于当前分类的标签
        }

        const 标签元素 = 创建标签元素(标签);
        标签列表容器.appendChild(标签元素);
    });
    console.log('标签列表渲染完成。');
}

/**
 * 创建一个标签元素。
 * @param {string} 标签 - 标签名称.
 * @returns {HTMLSpanElement} - 创建的标签元素.
 */
function 创建标签元素(标签) {
    const 标签元素 = document.createElement('span');
    标签元素.classList.add('标签');
    标签元素.textContent = `${标签} (${统计标签数量(标签)})`; // 显示标签和数量
    标签元素.addEventListener('click', () => 切换标签(标签));

    // 根据标签是否被选中来设置样式
    if (选中的标签.has(标签)) {
        标签元素.classList.add('选中');
    }

    return 标签元素;
}

/**
 * 统计包含特定标签的提示词条目数量。
 * @param {string} 标签 - 要统计的标签.
 * @returns {number} - 包含该标签的提示词条目数量.
 */
function 统计标签数量(标签) {
    return 提示词数据.filter(条目 => 条目.标签.includes(标签)).length;
}

/**
 * 渲染已选标签区域，显示当前选中的标签，点击可以取消选择。
 */
function 渲染已选标签区域() {
    console.log('开始渲染已选标签区域...');
    已选标签区域容器.innerHTML = ''; // 清空已选标签区域

    选中的标签.forEach(标签 => {
        const 已选标签元素 = 创建已选标签元素(标签);
        已选标签区域容器.appendChild(已选标签元素);
    });
    console.log('已选标签区域渲染完成。');
}

/**
 * 创建一个已选标签元素。
 * @param {string} 标签 - 标签名称.
 * @returns {HTMLSpanElement} - 创建的已选标签元素.
 */
function 创建已选标签元素(标签) {
    const 已选标签元素 = document.createElement('span');
    已选标签元素.classList.add('已选标签');
    已选标签元素.textContent = 标签;
    已选标签元素.addEventListener('click', () => 切换标签(标签)); // 点击取消选中
    return 已选标签元素;
}

/**
 * 渲染提示词列表，显示经过筛选后的提示词数据。
 */
function 渲染提示词列表() {
    console.log('开始渲染提示词列表...');
    提示词列表容器.innerHTML = ''; // 清空提示词列表

    过滤后的提示词数据.forEach(条目 => {
        const 项容器 = 创建项容器(条目); // 创建包含提示词和标签的项容器
        提示词列表容器.appendChild(项容器);
    });
    console.log('提示词列表渲染完成。');
}

/**
 * 创建一个包含提示词和标签预览的项容器元素。
 * @param {object} 条目 - 包含提示词和标签的数据条目.
 * @returns {HTMLDivElement} - 创建的项容器元素.
 */
function 创建项容器(条目) {
    const 项容器 = document.createElement('div');
    项容器.classList.add('项容器');

    // 创建提示词容器
    const 提示词容器 = document.createElement('div');
    提示词容器.classList.add('提示词容器');
    提示词容器.textContent = 条目.提示词;
    提示词容器.addEventListener('click', () => 复制提示词到剪贴板(条目.提示词)); // 点击复制功能
    项容器.appendChild(提示词容器);

    // 创建标签预览容器
    const 标签预览容器 = document.createElement('div');
    标签预览容器.classList.add('标签预览容器');
    条目.标签.forEach(标签 => {
        const 标签容器 = 创建标签容器(标签); // 创建包含单个标签的容器
        标签预览容器.appendChild(标签容器);
    });
    项容器.appendChild(标签预览容器);

    return 项容器;
}

/**
 * 创建一个包含单个标签的容器元素，并添加点击复制功能。
 * @param {string} 标签 - 标签名称.
 * @returns {HTMLSpanElement} - 创建的标签容器元素.
 */
function 创建标签容器(标签) {
    const 标签容器 = document.createElement('span');
    标签容器.classList.add('标签容器');

    const 标签元素 = document.createElement('span');
    标签元素.classList.add('标签预览');
    标签元素.textContent = 标签;
    标签容器.appendChild(标签元素);

    标签容器.addEventListener('click', () => 复制提示词到剪贴板(标签)); // 点击复制标签
    return 标签容器;
}

/**
 * 将提示词复制到剪贴板。
 * @param {string} 提示词 - 要复制的提示词.
 */
function 复制提示词到剪贴板(提示词) {
    navigator.clipboard.writeText(提示词)
        .then(() => {
            显示水印提示('已复制到剪贴板！');
        })
        .catch(错误 => {
            console.error('复制失败:', 错误);
            alert('复制失败，请手动复制。'); // 如果复制失败，仍然弹出窗口
        });
}

function 显示水印提示(消息) {
    // 创建水印元素
    const 水印 = document.createElement('div');
    水印.textContent = 消息;
    水印.style.position = 'fixed';
    水印.style.top = '20%';
    水印.style.left = '50%';
    水印.style.transform = 'translate(-50%, -50%)';
    水印.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    水印.style.color = '#fff';
    水印.style.padding = '10px 20px';
    水印.style.borderRadius = '5px';
    水印.style.zIndex = '9999'; // 确保在最上层
    水印.style.opacity = '0'; // 初始透明度为 0
    水印.style.transition = 'opacity 0.5s ease-in-out'; // 添加过渡效果

    // 将水印添加到 body 中
    document.body.appendChild(水印);

    // 逐渐显示水印
    setTimeout(() => {
        水印.style.opacity = '1';
    }, 10); // 稍微延迟一下，确保过渡效果生效

    // 5 秒后隐藏水印
    setTimeout(() => {
        水印.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(水印); // 移除水印元素
        }, 500); // 等待过渡效果完成再移除
    }, 5000);
}

// -------------------- 数据筛选与搜索 --------------------

/**
 * 更新过滤后的提示词数据，根据选中的标签、当前分类和搜索框内容进行筛选。
 */
function 更新过滤后的提示词数据() {
    console.log('开始更新过滤后的提示词数据...');
    过滤后的提示词数据 = 提示词数据.filter(条目 => 满足筛选条件(条目));
    console.log('过滤后的提示词数据更新完成，数量:', 过滤后的提示词数据.length);
}

/**
 * 检查一个提示词条目是否满足当前的筛选条件。
 * @param {object} 条目 - 要检查的提示词条目.
 * @returns {boolean} - 如果条目满足筛选条件，则返回true，否则返回false.
 */
function 满足筛选条件(条目) {
    return 满足标签筛选(条目) && 满足分类筛选(条目) && 满足搜索筛选(条目);
}

/**
 * 检查一个提示词条目是否满足标签筛选条件。
 * @param {object} 条目 - 要检查的提示词条目.
 * @returns {boolean} - 如果条目满足标签筛选条件，则返回true，否则返回false.
 */
function 满足标签筛选(条目) {
    // 筛选逻辑：如果选择了标签，则必须包含所有选中的标签
    return 选中的标签.size === 0 || Array.from(选中的标签).every(标签 => 条目.标签.includes(标签));
}

/**
 * 检查一个提示词条目是否满足分类筛选条件。
 * @param {object} 条目 - 要检查的提示词条目.
 * @returns {boolean} - 如果条目满足分类筛选条件，则返回true，否则返回false.
 */
function 满足分类筛选(条目) {
    // 如果有当前分类，则只显示属于该分类的条目
    return !当前分类 || 条目.标签.some(标签 => 分类映射[标签] == 当前分类);
}

/**
 * 检查一个提示词条目是否满足搜索筛选条件。
 * @param {object} 条目 - 要检查的提示词条目.
 * @returns {boolean} - 如果条目满足搜索筛选条件，则返回true，否则返回false.
 */
function 满足搜索筛选(条目) {
    const 搜索词 = 搜索框.value.toLowerCase();
    const 搜索条件 = 解析搜索词(搜索词);

    if (搜索条件.length === 0) {
        return true; // 没有搜索条件，所有条目都匹配
    }

    return 搜索条件.every(条件 => {
        return Object.keys(条目).some(字段 => {
            const 值 = 条目[字段];
            if (typeof 值 === 'string') {
                return 条件.精确 ? 值.toLowerCase() === 条件.词 : 值.toLowerCase().includes(条件.词);
            } else if (Array.isArray(值)) {
                return 值.some(item => typeof item === 'string' && (条件.精确 ? item.toLowerCase() === 条件.词 : item.toLowerCase().includes(条件.词)));
            }
            return false; // 字段不是字符串或字符串数组，不匹配
        });
    });
}

/**
 * 解析搜索词，将搜索词按空格分隔，并识别引号内的精确搜索词。
 * @param {string} 搜索词 - 要解析的搜索词.
 * @returns {array} - 解析后的搜索条件数组，每个条件包含词和是否精确搜索的标志.
 */
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

// -------------------- 事件监听 --------------------

/**
 * 切换标签的选中状态，并更新页面。
 * @param {string} 标签 - 要切换的标签名称.
 */
function 切换标签(标签) {
    console.log(`切换标签 "${标签}" 的选中状态`);
    if (选中的标签.has(标签)) {
        选中的标签.delete(标签);
        console.log(`取消选中标签: ${标签}`);
    } else {
        选中的标签.add(标签);
        console.log(`选中标签: ${标签}`);
    }
    渲染标签列表(); // 重新渲染标签列表，更新选中状态
    渲染已选标签区域(); // 重新渲染已选标签区域
    更新过滤后的提示词数据(); // 更新过滤后的提示词数据
    渲染提示词列表(); // 重新渲染提示词列表，应用筛选
}

// 搜索框事件监听
搜索框.addEventListener('input', () => {
    更新过滤后的提示词数据();
    渲染提示词列表();
});

// -------------------- 应用启动 --------------------

// 页面加载时初始化应用
初始化应用();
