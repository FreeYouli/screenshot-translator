# -*- coding: utf-8 -*-
import sys
import io
import os
import threading
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from config import load_config, save_config
from screenshot import take_region_screenshot
from ocr import ocr_text, check_tesseract, check_language
from translation import translate
from gui import select_region, show_result, input_translate, show_settings
import keyboard


def main_flow(config):
    print("=" * 50)
    print(f"  {datetime.now().strftime('%H:%M:%S')}  触发截图翻译")
    print("=" * 50)

    print("[1/4] 请用鼠标拖拽选择区域...")
    region = select_region()
    if region is None:
        print("用户取消")
        return
    print(f"选择区域：{region}")

    print("[2/4] 正在截图...")
    try:
        cropped = take_region_screenshot(region)
    except Exception as e:
        print(f"截图失败：{e}")
        return
    print("截图完成")

    print("[3/4] 正在识别文字...")
    retries = config.get("max_retries", 2)
    text = ocr_text(cropped, config, retries)
    if not text:
        print("未识别到文字")
        show_result("（未识别到文字）", "请确保截图区域包含清晰文字")
        return
    print(f"识别结果：{text[:60]}...")

    print("[4/4] 正在翻译...")
    translated = translate(text)
    print(f"翻译结果：{translated[:60]}...")

    print("打开结果窗口")
    show_result(text, translated)
    print("等待下次触发...")


def start_listener(config):
    import threading as _thr
    print()
    print("截图翻译工具已启动")
    print(f"  按 {config['hotkey']} 触发截图翻译")
    print(f"  按 {config['hotkey_input']} 触发输入翻译")
    print("  按 Ctrl+C 退出程序")
    print()

    def on_hotkey():
        t = _thr.Thread(target=main_flow, args=(config,), daemon=True)
        t.start()

    def on_input_hotkey():
        t = _thr.Thread(target=input_translate, daemon=True)
        t.start()

    keyboard.add_hotkey(config["hotkey"], on_hotkey)
    keyboard.add_hotkey(config["hotkey_input"], on_input_hotkey)

    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("\\n程序已退出")


def start_with_tray(config):
    tray = None
    try:
        import pystray
        from PIL import Image as PilImage

        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            icon_img = PilImage.open(icon_path)
        else:
            icon_img = PilImage.new("RGB", (64, 64), (70, 130, 180))

        def on_screenshot(icon, item):
            t = threading.Thread(target=main_flow, args=(config,), daemon=True)
            t.start()

        def on_input(icon, item):
            t = threading.Thread(target=input_translate, daemon=True)
            t.start()

        def on_settings(icon, item):
            t = threading.Thread(target=lambda: show_settings(
                config, save_config), daemon=True)
            t.start()

        def on_exit(icon, item):
            icon.stop()
            os._exit(0)

        menu = pystray.Menu(
            pystray.MenuItem("截图翻译 (Ctrl+Shift+Z)", on_screenshot),
            pystray.MenuItem("输入翻译 (Ctrl+Shift+X)", on_input),
            pystray.MenuItem("设置", on_settings),
            pystray.MenuItem("退出", on_exit),
        )

        tray = pystray.Icon("截图翻译工具", icon_img, "截图翻译工具", menu)

        import keyboard as _kb
        _kb.add_hotkey(config["hotkey"], on_screenshot)
        _kb.add_hotkey(config["hotkey_input"], on_input)

        tray.run()
    except ImportError:
        print("pystray 未安装，使用命令行模式")
        start_listener(config)


if __name__ == "__main__":
    config = load_config()

    print("=" * 50)
    print("    截图翻译工具 v2.0")
    print("=" * 50)
    print()

    ok = check_tesseract(config)
    if not ok:
        print(f"! 未找到 Tesseract：{config.get('tesseract_path', '')}")
        print("  请在设置中修改路径，或安装 Tesseract-OCR")
        print()

    missing_langs = check_language(config.get("tesseract_lang", ""), config)
    if missing_langs:
        print(f"! 以下 OCR 语言包未检测到：{', '.join(missing_langs)}")
        print("  请安装后重试，否则识别可能不准确")
        print()

    print(f"  截图翻译：{config['hotkey']}")
    print(f"  输入翻译：{config['hotkey_input']}")
    print(f"  Tesseract：{config.get('tesseract_path', '')}")
    print(f"  OCR 语言：{config.get('tesseract_lang', '')}")
    print(f"  重试次数：{config.get('max_retries', 2)}")
    print()
    print("请以管理员身份运行此脚本（否则全局快捷键可能无效）")
    print()

    start_with_tray(config)
