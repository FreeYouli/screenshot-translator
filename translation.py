# -*- coding: utf-8 -*-
import sys
import re

_translation_cache = {}


def translate(text, source="auto", target="zh-CN"):
    """
    Translate text using the translate library (pip install translate).
    Caches results in _translation_cache dict.
    """
    if not text:
        return ""

    cache_key = (text, source, target)
    cached = _translation_cache.get(cache_key)
    if cached is not None:
        return cached

    # Local file is translation.py, not translate.py, so no naming conflict
    try:
        from translate import Translator
    except ImportError:
        info = (            "\n[翻译错误] 翻译库 (translate) 未找到\n"
            "  请运行:  pip install translate\n"
            "  当前 Python: " + sys.executable + "\n"
        )
        _translation_cache[cache_key] = info.strip()
        return _translation_cache[cache_key]

    try:
        if source == "auto":
            has_chinese = bool(re.search(r"[\u4e00-\u9fff]", text))
            src, tgt = ("zh", "en") if has_chinese else ("en", "zh")
        else:
            src, tgt = source, target

        translator = Translator(from_lang=src, to_lang=tgt)
        result = translator.translate(text)
        _translation_cache[cache_key] = result
        return result
    except Exception as e:
        _translation_cache[cache_key] = f"[翻译错误] {e}"
        return _translation_cache[cache_key]


def clear_cache():
    _translation_cache.clear()
