# -*- coding: utf-8 -*-
"""
檔案選擇器元件
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import Signal


class FileSelector(QWidget):
    """檔案選擇器元件"""

    # 檔案變更信號
    fileChanged = Signal(str)

    def __init__(
        self,
        parent=None,
        mode: str = "open",  # "open" 或 "save"
        file_filter: str = "所有檔案 (*.*)",
        default_name: str = "",
        placeholder: str = "",
    ):
        """
        初始化檔案選擇器

        Args:
            parent: 父元件
            mode: 選擇模式 ("open" 或 "save")
            file_filter: 檔案過濾器
            default_name: 預設檔名
            placeholder: 輸入框佔位符
        """
        super().__init__(parent)

        self._mode = mode
        self._file_filter = file_filter
        self._default_name = default_name

        self._setup_ui(placeholder)

    def _setup_ui(self, placeholder: str) -> None:
        """設定 UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # 路徑輸入框
        self._path_edit = QLineEdit()
        self._path_edit.setPlaceholderText(placeholder)
        self._path_edit.textChanged.connect(self._on_text_changed)
        layout.addWidget(self._path_edit, 1)

        # 瀏覽按鈕
        self._browse_btn = QPushButton("瀏覽...")
        self._browse_btn.setObjectName("browseButton")
        self._browse_btn.clicked.connect(self._on_browse)
        layout.addWidget(self._browse_btn)

    def _on_browse(self) -> None:
        """處理瀏覽按鈕點擊"""
        if self._mode == "open":
            path, _ = QFileDialog.getOpenFileName(
                self, "選擇檔案", "", self._file_filter
            )
        else:
            path, _ = QFileDialog.getSaveFileName(
                self, "儲存檔案", self._default_name, self._file_filter
            )

        if path:
            self.setPath(path)

    def _on_text_changed(self, text: str) -> None:
        """處理文字變更"""
        self.fileChanged.emit(text)

    def path(self) -> str:
        """取得目前路徑"""
        return self._path_edit.text()

    def setPath(self, path: str) -> None:
        """設定路徑"""
        self._path_edit.setText(path)

    def setPlaceholder(self, text: str) -> None:
        """設定佔位符"""
        self._path_edit.setPlaceholderText(text)

    def clear(self) -> None:
        """清除路徑"""
        self._path_edit.clear()
