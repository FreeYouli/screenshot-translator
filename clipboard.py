# -*- coding: utf-8 -*-
import os
import subprocess
import tempfile


def copy_to_clipboard(text):
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        pass
    try:
        tmp = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".txt", encoding="utf-8")
        tmp.write(text)
        tmp.close()
        subprocess.run(f'type "{tmp.name}" | clip', shell=True, capture_output=True)
        os.unlink(tmp.name)
        return True
    except Exception:
        return False
