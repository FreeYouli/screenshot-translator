# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import re

from clipboard import copy_to_clipboard
from translation import translate


def select_region():
    start_x = start_y = end_x = end_y = 0
    rect_id = None
    selected = [False]

    def on_mouse_down(event):
        nonlocal start_x, start_y, rect_id
        start_x, start_y = event.x_root, event.y_root
        rect_id = canvas.create_rectangle(
            start_x, start_y, start_x, start_y,
            outline="red", width=2
        )

    def on_mouse_move(event):
        nonlocal end_x, end_y
        end_x, end_y = event.x_root, event.y_root
        if rect_id:
            canvas.coords(rect_id, start_x, start_y, end_x, end_y)

    def on_mouse_up(event):
        nonlocal end_x, end_y
        end_x, end_y = event.x_root, event.y_root
        selected[0] = True
        root.quit()

    root = tk.Tk()
    root.title("截图翻译")
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    root.geometry(f"{screen_w}x{screen_h}+0+0")
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.3)

    canvas = tk.Canvas(root, width=screen_w, height=screen_h, cursor="cross")
    canvas.pack()
    canvas.create_text(screen_w // 2, 30,
                       text="拖拽选择区域  |  ESC 取消",
                       fill="white", font=("微软雅黑", 16, "bold"))

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_move)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)
    root.bind("<Escape>", lambda e: root.quit())

    root.mainloop()

    x1 = min(start_x, end_x)
    y1 = min(start_y, end_y)
    x2 = max(start_x, end_x)
    y2 = max(start_y, end_y)
    root.destroy()

    if not selected[0] or (x2 - x1) < 5 or (y2 - y1) < 5:
        return None
    return (x1, y1, x2, y2)


def show_result(original, translated, on_retranslate=None):
    copy_to_clipboard(translated)

    root = tk.Tk()
    root.title("截图翻译结果")
    root.geometry("650x450")
    root.attributes("-topmost", True)

    tk.Label(root, text="【原文】",
             font=("微软雅黑", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    txt_orig = ScrolledText(root, height=5, wrap=tk.WORD, font=("微软雅黑", 10))
    txt_orig.pack(fill="both", padx=10, pady=5, expand=True)
    txt_orig.insert("1.0", original)
    txt_orig.config(state="disabled")

    tk.Frame(root, height=2, bg="gray").pack(fill="x", padx=10, pady=5)

    tk.Label(root, text="【译文】（已自动复制到剪贴板）",
             font=("微软雅黑", 11, "bold")).pack(anchor="w", padx=10)
    txt_trans = ScrolledText(root, height=5, wrap=tk.WORD, font=("微软雅黑", 10))
    txt_trans.pack(fill="both", padx=10, pady=5, expand=True)
    txt_trans.insert("1.0", translated)
    txt_trans.config(state="disabled")

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    def do_retranslate():
        has_chinese = bool(re.search(r"[\\u4e00-\\u9fff]", original))
        old_window = root
        if has_chinese:
            result = translate(original, source="zh", target="en")
        else:
            result = translate(original, source="en", target="zh")
        old_window.destroy()
        show_result(original, result)

    tk.Button(btn_frame, text="关闭", command=root.destroy,
              width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="切换方向重译", command=do_retranslate,
              width=12).pack(side=tk.LEFT, padx=5)

    root.mainloop()


def input_translate():
    """弹出输入框，输入中文翻译成英文"""
    def do_translate():
        text = input_box.get("1.0", "end-1c").strip()
        if not text:
            return
        print("输入文字：" + text[:60])
        result = translate(text, source="zh", target="en")
        print("翻译结果：" + result[:60])
        root.destroy()
        show_result(text, result)

    root = tk.Tk()
    root.title("输入翻译（中->英）")
    root.geometry("500x300")
    root.attributes("-topmost", True)
    tk.Label(root, text="请输入中文：",
             font=("微软雅黑", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    input_box = ScrolledText(root, height=5, wrap=tk.WORD, font=("微软雅黑", 10))
    input_box.pack(fill="both", padx=10, pady=5, expand=True)
    input_box.focus()
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="翻译", command=do_translate,
              width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="关闭", command=root.destroy,
              width=10).pack(side=tk.LEFT, padx=5)
    root.mainloop()


def show_settings(current_config, on_save):
    root = tk.Tk()
    root.title("截图翻译 - 设置")
    root.geometry("480x380")
    root.attributes("-topmost", True)

    vars_hotkey = tk.StringVar(value=current_config.get("hotkey", "ctrl+shift+z"))
    vars_hotkey_input = tk.StringVar(value=current_config.get("hotkey_input", "ctrl+shift+x"))
    vars_tesseract = tk.StringVar(value=current_config.get("tesseract_path", ""))
    vars_lang = tk.StringVar(value=current_config.get("tesseract_lang", "chi_sim+eng"))
    vars_retries = tk.IntVar(value=current_config.get("max_retries", 2))

    row = 0

    def add_row(text, var, row, show=None):
        tk.Label(root, text=text, anchor="w", font=("微软雅黑", 10)).grid(
            row=row, column=0, sticky="w", padx=10, pady=5)
        entry = tk.Entry(root, textvariable=var, font=("微软雅黑", 10),
                         width=40, show=show)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        return entry

    add_row("截图翻译快捷键:", vars_hotkey, 0)
    add_row("输入翻译快捷键:", vars_hotkey_input, 1)
    add_row("Tesseract 路径:", vars_tesseract, 2)
    add_row("OCR 语言:", vars_lang, 3)
    tk.Label(root, text="重试次数:", anchor="w", font=("微软雅黑", 10)).grid(
        row=4, column=0, sticky="w", padx=10, pady=5)
    tk.Spinbox(root, from_=0, to=5, textvariable=vars_retries, width=5,
               font=("微软雅黑", 10)).grid(row=4, column=1, sticky="w", padx=10, pady=5)

    status_label = tk.Label(root, text="", fg="green", font=("微软雅黑", 9))
    status_label.grid(row=5, column=0, columnspan=2, pady=5)

    def do_save():
        new_cfg = {
            "hotkey": vars_hotkey.get().strip(),
            "hotkey_input": vars_hotkey_input.get().strip(),
            "tesseract_path": vars_tesseract.get().strip(),
            "tesseract_lang": vars_lang.get().strip(),
            "max_retries": vars_retries.get(),
        }
        on_save(new_cfg)
        status_label.config(text="已保存", fg="green")
        root.after(1200, root.destroy)

    tk.Button(root, text="保存", command=do_save, width=12,
              font=("微软雅黑", 10)).grid(row=6, column=0, columnspan=2, pady=15)

    root.columnconfigure(1, weight=1)
    root.mainloop()
    return current_config
