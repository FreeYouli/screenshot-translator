# -*- coding: utf-8 -*-
import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

DEFAULT_CONFIG = {
    "hotkey": "ctrl+shift+z",
    "hotkey_input": "ctrl+shift+x",
    "tesseract_path": r"D:\Tesseract-OCR\tesseract.exe",
    "tesseract_lang": "chi_sim+eng",
    "ocr_config": "--oem 3 --psm 6",
    "max_retries": 2,
    "translate_from": "auto",
    "translate_to": "zh-CN"
}


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            merged = DEFAULT_CONFIG.copy()
            merged.update(cfg)
            return merged
        except (json.JSONDecodeError, IOError):
            pass
    return dict(DEFAULT_CONFIG)


def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
