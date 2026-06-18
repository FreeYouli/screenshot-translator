# -*- coding: utf-8 -*-
import os
import pytesseract


def check_tesseract(config):
    path = config.get("tesseract_path", "")
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        return True
    return False


def check_language(lang, config):
    try:
        langs = pytesseract.get_languages(config=config.get("ocr_config", ""))
        parts = lang.split("+")
        missing = [p for p in parts if p not in langs]
        return missing
    except Exception:
        return [lang]


def ocr_text(image, config, retries=0):
    lang = config.get("tesseract_lang", "chi_sim+eng")
    custom_config = config.get("ocr_config", "--oem 3 --psm 6")
    for attempt in range(max(1, retries + 1)):
        try:
            text = pytesseract.image_to_string(
                image, lang=lang, config=custom_config)
            return text.strip()
        except Exception as e:
            if attempt < retries:
                continue
            return ""
    return ""
