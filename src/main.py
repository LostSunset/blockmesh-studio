# -*- coding: utf-8 -*-
"""
BlockMesh Studio 應用程式入口

OpenFOAM blockMeshDict 網格生成工具
採用 PySide6 與無印良品風格設計
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from .ui.main_window import MainWindow


def main():
    """應用程式入口"""
    # 啟用高 DPI 縮放
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("BlockMesh Studio")
    app.setApplicationVersion("0.3.0")
    app.setOrganizationName("BlockMesh Studio")

    # 設定預設字型
    font = app.font()
    current_size = font.pointSize()
    if current_size <= 0:
        font.setPointSize(10)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
