# 截图翻译工具

**玩外服游戏遇到外国人？截屏即译，无需切出游戏。**

截图 → OCR → 翻译 → 复制到剪贴板，一键完成。支持截图翻译和输入翻译两种模式，离线翻译引擎，自动缓存结果。

> 适用场景：外服游戏实时交流、外文软件界面阅读、生肉漫画/文档快速理解——任何不方便复制粘贴到网页翻译的地方。

## 功能

| 快捷键 | 功能 |
|--------|------|
| Ctrl+Shift+Z | **截图翻译**：拖拽框选屏幕区域 → OCR 识别 → 翻译 → 弹窗 + 自动复制 |
| Ctrl+Shift+X | **输入翻译**：弹出输入框 → 输入中文 → 翻译为英文 → 弹窗 + 自动复制 |
| — | 系统托盘图标：右键菜单可访问截图翻译、输入翻译、设置、退出 |
| — | 设置窗口：修改快捷键、Tesseract 路径、OCR 语言、重试次数，自动保存到 config.json |

## 安装

```bash
# 克隆仓库
git clone https://github.com/FreeYouli/screenshot-translator.git
cd screenshot-translator

# 安装依赖
pip install -r requirements.txt
```

### 可选依赖

- **系统托盘**：`pip install pystray`，未安装时自动降级为命令行模式
- **剪贴板加速**：`pip install pyperclip`，未安装时自动使用 Windows `clip` 命令

### Tesseract-OCR 引擎

1. 从 [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki) 下载安装包
2. 安装时勾选**中文简体语言包（chi_sim）**
3. 默认路径 `D:\Tesseract-OCR\tesseract.exe`，可在设置中修改

## 系统要求

- Python 3.8+
- Windows（全局快捷键依赖 `keyboard` 库）
- 管理员权限（全局快捷键需要）

## 使用

```bash
# 请以管理员身份运行
python main.py
```

首次运行自动生成 `config.json`，配置文件位于项目根目录。

### 系统托盘

安装 `pystray` 后启动会在系统托盘显示图标，右键菜单包含：

- **截图翻译 (Ctrl+Shift+Z)** — 触发截图翻译流程
- **输入翻译 (Ctrl+Shift+X)** — 弹出输入翻译窗口
- **设置** — 打开设置 GUI
- **退出** — 退出程序

未安装 `pystray` 时自动切换为命令行监听模式。

### 设置 GUI

在设置窗口中可修改：

- 截图翻译快捷键（默认 Ctrl+Shift+Z）
- 输入翻译快捷键（默认 Ctrl+Shift+X）
- Tesseract 安装路径
- OCR 语言包（默认 chi_sim+eng）
- 重试次数（OCR 失败时自动重试）

修改后点击"保存"自动写入 `config.json`，下次触发时生效。

## 项目结构

```
screenshot-translator/
├── main.py          入口，热键监听，系统托盘
├── config.py        配置管理（config.json 读写）
├── screenshot.py    区域截图（mss）
├── ocr.py           文字识别（Tesseract OCR，失败自动重试）
├── translation.py   翻译引擎（离线，缓存结果）
├── gui.py           界面（区域选择、结果窗口、输入窗口、设置窗口）
├── clipboard.py     剪贴板操作
├── config.json      用户配置（自动生成，.gitignore 忽略）
├── requirements.txt 依赖清单
├── .gitignore       Git 忽略规则
└── LICENSE          开源许可证（MIT）
```

## 配置

`config.json` 示例：

```json
{
  "hotkey": "ctrl+shift+z",
  "hotkey_input": "ctrl+shift+x",
  "tesseract_path": "D:\Tesseract-OCR\tesseract.exe",
  "tesseract_lang": "chi_sim+eng",
  "max_retries": 2
}
```

缺失的配置项自动使用默认值，无需手动创建文件。

## 许可协议

MIT License
