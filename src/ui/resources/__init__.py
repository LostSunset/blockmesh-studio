# -*- coding: utf-8 -*-
"""
UI 資源模組
"""

from pathlib import Path


def get_stylesheet() -> str:
    """載入 MUJI 風格樣式表"""
    style_path = Path(__file__).parent / "muji_style.qss"

    if style_path.exists():
        return style_path.read_text(encoding="utf-8")

    return ""
