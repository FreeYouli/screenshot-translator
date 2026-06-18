# 截图翻译工具

截图 -> OCR -> 翻译 -> 显示结果，全流程一键完成。

## 功能

| 快捷键 | 功能 |
|--------|------|
| Ctrl+Shift+Z | 截图翻译：框选区域 → OCR → 翻译 → 弹窗 + 自动复制 |
| Ctrl+Shift+X | 输入翻译：弹窗输入中文 → 翻译为英文 |

## 依赖

pip install keyboard mss pytesseract Pillow translate pyperclip

还需要安装 Tesseract-OCR 引擎：
https://github.com/UB-Mannheim/tesseract/wiki

## 使用

请以管理员身份运行（否则全局快捷键可能无效）：
python main.py

首次运行会自动生成 config.json，可在系统托盘菜单中修改设置。

## 项目结构

screenshot_tools/
  main.py         入口
  config.py       配置管理
  screenshot.py   区域截图 (mss)
  ocr.py          文字识别 (Tesseract)
  translation.py  离线翻译 + 缓存
  gui.py          界面 (tkinter)
  clipboard.py    剪贴板
  config.json     配置文件（自动生成）
  .gitignore
