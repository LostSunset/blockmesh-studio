# -*- coding: utf-8 -*-
"""
資料說明面板元件

顯示座標系統說明、資料格式說明，以及載入後的資料統計
"""

from typing import Optional

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QGridLayout,
)
from PySide6.QtCore import Qt

from ..i18n import tr
from ...core.data_reader import DataStatistics


class DataInfoPanel(QWidget):
    """資料說明面板"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._statistics: Optional[DataStatistics] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """設定 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # 座標系統說明
        self._coord_group = QGroupBox(tr("coord_system"))
        coord_layout = QVBoxLayout(self._coord_group)
        self._coord_desc = QLabel(tr("coord_desc"))
        self._coord_desc.setWordWrap(True)
        self._coord_desc.setTextFormat(Qt.TextFormat.PlainText)
        coord_layout.addWidget(self._coord_desc)
        layout.addWidget(self._coord_group)

        # 資料格式說明
        self._format_group = QGroupBox(tr("data_format"))
        format_layout = QVBoxLayout(self._format_group)
        self._format_desc = QLabel(tr("format_desc"))
        self._format_desc.setWordWrap(True)
        self._format_desc.setTextFormat(Qt.TextFormat.PlainText)
        format_layout.addWidget(self._format_desc)
        layout.addWidget(self._format_group)

        # 資料統計
        self._stats_group = QGroupBox(tr("data_statistics"))
        stats_layout = QGridLayout(self._stats_group)
        stats_layout.setSpacing(8)

        row = 0

        # 總點數
        self._total_label = QLabel(tr("total_points"))
        stats_layout.addWidget(self._total_label, row, 0)
        self._total_value = QLabel("-")
        self._total_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        stats_layout.addWidget(self._total_value, row, 1)
        row += 1

        # 內曲線點數
        self._inner_label = QLabel(tr("inner_points"))
        stats_layout.addWidget(self._inner_label, row, 0)
        self._inner_value = QLabel("-")
        self._inner_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        stats_layout.addWidget(self._inner_value, row, 1)
        row += 1

        # 外曲線點數
        self._outer_label = QLabel(tr("outer_points"))
        stats_layout.addWidget(self._outer_label, row, 0)
        self._outer_value = QLabel("-")
        self._outer_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        stats_layout.addWidget(self._outer_value, row, 1)
        row += 1

        # X 範圍
        self._x_range_label = QLabel(tr("x_range"))
        stats_layout.addWidget(self._x_range_label, row, 0)
        self._x_range_value = QLabel("-")
        self._x_range_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        stats_layout.addWidget(self._x_range_value, row, 1)
        row += 1

        # Y 範圍
        self._y_range_label = QLabel(tr("y_range"))
        stats_layout.addWidget(self._y_range_label, row, 0)
        self._y_range_value = QLabel("-")
        self._y_range_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        stats_layout.addWidget(self._y_range_value, row, 1)
        row += 1

        # Z 範圍
        self._z_range_label = QLabel(tr("z_range"))
        stats_layout.addWidget(self._z_range_label, row, 0)
        self._z_range_value = QLabel("-")
        self._z_range_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        stats_layout.addWidget(self._z_range_value, row, 1)

        layout.addWidget(self._stats_group)

    def retranslateUi(self) -> None:
        """重新翻譯 UI"""
        self._coord_group.setTitle(tr("coord_system"))
        self._coord_desc.setText(tr("coord_desc"))
        self._format_group.setTitle(tr("data_format"))
        self._format_desc.setText(tr("format_desc"))
        self._stats_group.setTitle(tr("data_statistics"))
        self._total_label.setText(tr("total_points"))
        self._inner_label.setText(tr("inner_points"))
        self._outer_label.setText(tr("outer_points"))
        self._x_range_label.setText(tr("x_range"))
        self._y_range_label.setText(tr("y_range"))
        self._z_range_label.setText(tr("z_range"))

    def setStatistics(self, stats: Optional[DataStatistics]) -> None:
        """設定資料統計"""
        self._statistics = stats

        if stats is None:
            self._total_value.setText("-")
            self._inner_value.setText("-")
            self._outer_value.setText("-")
            self._x_range_value.setText("-")
            self._y_range_value.setText("-")
            self._z_range_value.setText("-")
        else:
            self._total_value.setText(str(stats.total_points))
            self._inner_value.setText(str(stats.inner_points))
            self._outer_value.setText(str(stats.outer_points))
            self._x_range_value.setText(
                f"{stats.x_range[0]:.3f} ~ {stats.x_range[1]:.3f}"
            )
            self._y_range_value.setText(
                f"{stats.y_range[0]:.3f} ~ {stats.y_range[1]:.3f}"
            )
            self._z_range_value.setText(
                f"{stats.z_range[0]:.3f} ~ {stats.z_range[1]:.3f}"
            )

    def clearStatistics(self) -> None:
        """清除資料統計"""
        self.setStatistics(None)

    @property
    def statistics(self) -> Optional[DataStatistics]:
        """取得目前的資料統計"""
        return self._statistics
