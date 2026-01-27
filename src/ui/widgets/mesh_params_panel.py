# -*- coding: utf-8 -*-
"""
網格參數面板元件
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

from ...models.mesh_params import MeshParameters


class MeshParamsPanel(QWidget):
    """網格參數設定面板"""

    # 參數變更信號
    paramsChanged = Signal(MeshParameters)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """設定 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 群組框
        group = QGroupBox("網格參數設定")
        group_layout = QGridLayout(group)
        group_layout.setSpacing(12)

        row = 0

        # 尺度因子
        group_layout.addWidget(QLabel("尺度因子："), row, 0)
        self._scale_spin = QDoubleSpinBox()
        self._scale_spin.setRange(0.001, 1000)
        self._scale_spin.setDecimals(3)
        self._scale_spin.setValue(1.0)
        self._scale_spin.setSingleStep(0.1)
        group_layout.addWidget(self._scale_spin, row, 1)
        hint = QLabel("控制整體網格的尺度比例")
        hint.setObjectName("subtitleLabel")
        group_layout.addWidget(hint, row, 2)
        row += 1

        # 層數
        group_layout.addWidget(QLabel("層數（Z軸截面數）："), row, 0)
        self._layers_spin = QSpinBox()
        self._layers_spin.setRange(2, 500)
        self._layers_spin.setValue(100)
        group_layout.addWidget(self._layers_spin, row, 1)
        hint = QLabel("值越大，Z 方向取樣越密集")
        hint.setObjectName("subtitleLabel")
        group_layout.addWidget(hint, row, 2)
        row += 1

        # 徑向網格數
        group_layout.addWidget(QLabel("徑向網格數："), row, 0)
        self._radial_spin = QSpinBox()
        self._radial_spin.setRange(1, 200)
        self._radial_spin.setValue(25)
        group_layout.addWidget(self._radial_spin, row, 1)
        hint = QLabel("內壁到外壁的網格密度")
        hint.setObjectName("subtitleLabel")
        group_layout.addWidget(hint, row, 2)
        row += 1

        # 圓周方向網格數
        group_layout.addWidget(QLabel("圓周方向網格數："), row, 0)
        self._circum_spin = QSpinBox()
        self._circum_spin.setRange(4, 800)
        self._circum_spin.setValue(400)
        self._circum_spin.setSingleStep(4)
        group_layout.addWidget(self._circum_spin, row, 1)
        hint = QLabel("需為 4 的倍數")
        hint.setObjectName("subtitleLabel")
        group_layout.addWidget(hint, row, 2)
        row += 1

        # 軸向網格數
        group_layout.addWidget(QLabel("軸向網格數："), row, 0)
        self._axial_spin = QSpinBox()
        self._axial_spin.setRange(1, 200)
        self._axial_spin.setValue(2)
        group_layout.addWidget(self._axial_spin, row, 1)
        hint = QLabel("每段 Z 方向的網格密度")
        hint.setObjectName("subtitleLabel")
        group_layout.addWidget(hint, row, 2)

        layout.addWidget(group)

    def _connect_signals(self) -> None:
        """連接信號"""
        self._scale_spin.valueChanged.connect(self._emit_params)
        self._layers_spin.valueChanged.connect(self._emit_params)
        self._radial_spin.valueChanged.connect(self._emit_params)
        self._circum_spin.valueChanged.connect(self._emit_params)
        self._axial_spin.valueChanged.connect(self._emit_params)

    def _emit_params(self) -> None:
        """發射參數變更信號"""
        self.paramsChanged.emit(self.getParams())

    def getParams(self) -> MeshParameters:
        """取得目前參數"""
        return MeshParameters(
            scale_factor=self._scale_spin.value(),
            num_layers=self._layers_spin.value(),
            n_cells_radial=self._radial_spin.value(),
            n_cells_circum=self._circum_spin.value(),
            n_cells_axial=self._axial_spin.value(),
        )

    def setParams(self, params: MeshParameters) -> None:
        """設定參數"""
        self._scale_spin.setValue(params.scale_factor)
        self._layers_spin.setValue(params.num_layers)
        self._radial_spin.setValue(params.n_cells_radial)
        self._circum_spin.setValue(params.n_cells_circum)
        self._axial_spin.setValue(params.n_cells_axial)
