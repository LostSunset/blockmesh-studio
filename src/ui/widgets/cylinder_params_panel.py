# -*- coding: utf-8 -*-
"""
圓柱網格參數面板元件
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
)
from PySide6.QtCore import Signal

from ...models.mesh_params import CylinderMeshParams


class CylinderParamsPanel(QWidget):
    """圓柱網格參數設定面板"""

    # 參數變更信號
    paramsChanged = Signal(CylinderMeshParams)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """設定 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 幾何參數群組
        geom_group = QGroupBox("幾何參數")
        geom_layout = QGridLayout(geom_group)
        geom_layout.setSpacing(12)

        row = 0

        # 內方形邊長
        geom_layout.addWidget(QLabel("內方形邊長："), row, 0)
        self._square_spin = QDoubleSpinBox()
        self._square_spin.setRange(0.01, 10)
        self._square_spin.setDecimals(3)
        self._square_spin.setValue(0.3)
        self._square_spin.setSingleStep(0.1)
        geom_layout.addWidget(self._square_spin, row, 1)
        row += 1

        # 內方形曲率
        geom_layout.addWidget(QLabel("內方形曲率："), row, 0)
        self._curve_spin = QDoubleSpinBox()
        self._curve_spin.setRange(0.01, 10)
        self._curve_spin.setDecimals(3)
        self._curve_spin.setValue(0.4)
        self._curve_spin.setSingleStep(0.1)
        geom_layout.addWidget(self._curve_spin, row, 1)
        hint = QLabel("必須大於內方形邊長")
        hint.setObjectName("subtitleLabel")
        geom_layout.addWidget(hint, row, 2)
        row += 1

        # 圓柱半徑
        geom_layout.addWidget(QLabel("圓柱半徑："), row, 0)
        self._radius_spin = QDoubleSpinBox()
        self._radius_spin.setRange(0.1, 100)
        self._radius_spin.setDecimals(3)
        self._radius_spin.setValue(1.8)
        self._radius_spin.setSingleStep(0.1)
        geom_layout.addWidget(self._radius_spin, row, 1)
        row += 1

        # 圓柱高度
        geom_layout.addWidget(QLabel("圓柱高度："), row, 0)
        self._height_spin = QDoubleSpinBox()
        self._height_spin.setRange(0.1, 1000)
        self._height_spin.setDecimals(3)
        self._height_spin.setValue(5.33)
        self._height_spin.setSingleStep(0.5)
        geom_layout.addWidget(self._height_spin, row, 1)
        row += 1

        # 底面 X 座標
        geom_layout.addWidget(QLabel("底面 X 座標："), row, 0)
        self._base_x_spin = QDoubleSpinBox()
        self._base_x_spin.setRange(-1000, 1000)
        self._base_x_spin.setDecimals(3)
        self._base_x_spin.setValue(-1.8)
        self._base_x_spin.setSingleStep(0.5)
        geom_layout.addWidget(self._base_x_spin, row, 1)

        layout.addWidget(geom_group)

        # 網格參數群組
        mesh_group = QGroupBox("網格參數")
        mesh_layout = QGridLayout(mesh_group)
        mesh_layout.setSpacing(12)

        row = 0

        # 內方形網格數
        mesh_layout.addWidget(QLabel("內方形網格數："), row, 0)
        self._ns_spin = QSpinBox()
        self._ns_spin.setRange(1, 200)
        self._ns_spin.setValue(30)
        mesh_layout.addWidget(self._ns_spin, row, 1)
        row += 1

        # 內方形到圓形網格數
        mesh_layout.addWidget(QLabel("內圓環網格數："), row, 0)
        self._ni_spin = QSpinBox()
        self._ni_spin.setRange(1, 200)
        self._ni_spin.setValue(30)
        mesh_layout.addWidget(self._ni_spin, row, 1)
        row += 1

        # 高度方向網格數
        mesh_layout.addWidget(QLabel("高度方向網格數："), row, 0)
        self._nh_spin = QSpinBox()
        self._nh_spin.setRange(1, 1000)
        self._nh_spin.setValue(120)
        mesh_layout.addWidget(self._nh_spin, row, 1)

        layout.addWidget(mesh_group)
        layout.addStretch()

    def _connect_signals(self) -> None:
        """連接信號"""
        for spin in [
            self._square_spin,
            self._curve_spin,
            self._radius_spin,
            self._height_spin,
            self._base_x_spin,
            self._ns_spin,
            self._ni_spin,
            self._nh_spin,
        ]:
            spin.valueChanged.connect(self._emit_params)

    def _emit_params(self) -> None:
        """發射參數變更信號"""
        self.paramsChanged.emit(self.getParams())

    def getParams(self) -> CylinderMeshParams:
        """取得目前參數"""
        return CylinderMeshParams(
            inner_square_side=self._square_spin.value(),
            inner_square_curve=self._curve_spin.value(),
            radius=self._radius_spin.value(),
            height=self._height_spin.value(),
            base_x=self._base_x_spin.value(),
            n_cells_square=self._ns_spin.value(),
            n_cells_inner=self._ni_spin.value(),
            n_cells_height=self._nh_spin.value(),
        )

    def setParams(self, params: CylinderMeshParams) -> None:
        """設定參數"""
        self._square_spin.setValue(params.inner_square_side)
        self._curve_spin.setValue(params.inner_square_curve)
        self._radius_spin.setValue(params.radius)
        self._height_spin.setValue(params.height)
        self._base_x_spin.setValue(params.base_x)
        self._ns_spin.setValue(params.n_cells_square)
        self._ni_spin.setValue(params.n_cells_inner)
        self._nh_spin.setValue(params.n_cells_height)
