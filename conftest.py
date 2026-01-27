# -*- coding: utf-8 -*-
"""
pytest 全域配置
確保 UTF-8 編碼支援正體中文
"""
import os
import sys


def pytest_configure(config):
    """
    pytest 啟動時設定環境變數，確保 UTF-8 輸出
    Python 3.14 預設已使用 UTF-8 模式
    """
    # 設定 IO 編碼（Python 3.14 中 PYTHONUTF8 可能無需設定）
    os.environ["PYTHONIOENCODING"] = "utf-8"
    
    # Windows 終端編碼設定
    if sys.platform == "win32":
        os.environ["PYTHONLEGACYWINDOWSSTDIO"] = "0"
        # 嘗試設定 Windows 終端為 UTF-8
        try:
            import subprocess
            subprocess.run(["chcp", "65001"], shell=True, capture_output=True)
        except Exception:
            pass

