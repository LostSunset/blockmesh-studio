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
from ..i18n import tr


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
        self._group = QGroupBox(tr("mesh_params"))
        group_layout = QGridLayout(self._group)
        group_layout.setSpacing(12)

        row = 0

        # 尺度因子
        self._scale_label = QLabel(tr("scale_factor"))
        group_layout.addWidget(self._scale_label, row, 0)
        self._scale_spin = QDoubleSpinBox()
        self._scale_spin.setRange(0.001, 1000)
        self._scale_spin.setDecimals(3)
        self._scale_spin.setValue(1.0)
        self._scale_spin.setSingleStep(0.1)
        self._scale_spin.setToolTip(tr("tip_scale"))
        group_layout.addWidget(self._scale_spin, row, 1)
        self._scale_hint = QLabel(tr("scale_hint"))
        self._scale_hint.setObjectName("subtitleLabel")
        group_layout.addWidget(self._scale_hint, row, 2)
        row += 1

        # 層數
        self._layers_label = QLabel(tr("num_layers"))
        group_layout.addWidget(self._layers_label, row, 0)
        self._layers_spin = QSpinBox()
        self._layers_spin.setRange(2, 500)
        self._layers_spin.setValue(100)
        self._layers_spin.setToolTip(tr("tip_layers"))
        group_layout.addWidget(self._layers_spin, row, 1)
        self._layers_hint = QLabel(tr("layers_hint"))
        self._layers_hint.setObjectName("subtitleLabel")
        group_layout.addWidget(self._layers_hint, row, 2)
        row += 1

        # 徑向網格數
        self._radial_label = QLabel(tr("radial_cells"))
        group_layout.addWidget(self._radial_label, row, 0)
        self._radial_spin = QSpinBox()
        self._radial_spin.setRange(1, 200)
        self._radial_spin.setValue(25)
        self._radial_spin.setToolTip(tr("tip_radial"))
        group_layout.addWidget(self._radial_spin, row, 1)
        self._radial_hint = QLabel(tr("radial_hint"))
        self._radial_hint.setObjectName("subtitleLabel")
        group_layout.addWidget(self._radial_hint, row, 2)
        row += 1

        # 圓周方向網格數
        self._circum_label = QLabel(tr("circum_cells"))
        group_layout.addWidget(self._circum_label, row, 0)
        self._circum_spin = QSpinBox()
        self._circum_spin.setRange(4, 800)
        self._circum_spin.setValue(400)
        self._circum_spin.setSingleStep(4)
        self._circum_spin.setToolTip(tr("tip_circum"))
        group_layout.addWidget(self._circum_spin, row, 1)
        self._circum_hint = QLabel(tr("circum_hint"))
        self._circum_hint.setObjectName("subtitleLabel")
        group_layout.addWidget(self._circum_hint, row, 2)
        row += 1

        # 軸向網格數
        self._axial_label = QLabel(tr("axial_cells"))
        group_layout.addWidget(self._axial_label, row, 0)
        self._axial_spin = QSpinBox()
        self._axial_spin.setRange(1, 200)
        self._axial_spin.setValue(2)
        self._axial_spin.setToolTip(tr("tip_axial"))
        group_layout.addWidget(self._axial_spin, row, 1)
        self._axial_hint = QLabel(tr("axial_hint"))
        self._axial_hint.setObjectName("subtitleLabel")
        group_layout.addWidget(self._axial_hint, row, 2)

        layout.addWidget(self._group)

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

    def retranslateUi(self) -> None:
        """重新翻譯 UI"""
        self._group.setTitle(tr("mesh_params"))
        self._scale_label.setText(tr("scale_factor"))
        self._scale_hint.setText(tr("scale_hint"))
        self._layers_label.setText(tr("num_layers"))
        self._layers_hint.setText(tr("layers_hint"))
        self._radial_label.setText(tr("radial_cells"))
        self._radial_hint.setText(tr("radial_hint"))
        self._circum_label.setText(tr("circum_cells"))
        self._circum_hint.setText(tr("circum_hint"))
        self._axial_label.setText(tr("axial_cells"))
        self._axial_hint.setText(tr("axial_hint"))

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
