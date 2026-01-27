# -*- coding: utf-8 -*-
"""
邊界層參數面板元件
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
)
from PySide6.QtCore import Signal

from ...models.mesh_params import BoundaryLayerParams
from ..i18n import tr


class BoundaryLayerPanel(QWidget):
    """邊界層參數設定面板"""

    # 參數變更信號
    paramsChanged = Signal(BoundaryLayerParams)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
        self._update_enabled_state()

    def _setup_ui(self) -> None:
        """設定 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 群組框
        self._group = QGroupBox(tr("boundary_layer"))
        group_layout = QVBoxLayout(self._group)

        # 啟用複選框
        self._enabled_check = QCheckBox(tr("enable_bl"))
        group_layout.addWidget(self._enabled_check)

        # 參數容器
        self._params_widget = QWidget()
        params_layout = QGridLayout(self._params_widget)
        params_layout.setSpacing(12)
        params_layout.setContentsMargins(0, 8, 0, 0)

        row = 0

        # 內壁邊界層厚度
        self._inner_thickness_label = QLabel(tr("inner_thickness"))
        params_layout.addWidget(self._inner_thickness_label, row, 0)
        self._inner_thickness_spin = QDoubleSpinBox()
        self._inner_thickness_spin.setRange(0.01, 0.5)
        self._inner_thickness_spin.setDecimals(3)
        self._inner_thickness_spin.setValue(0.02)
        self._inner_thickness_spin.setSingleStep(0.01)
        params_layout.addWidget(self._inner_thickness_spin, row, 1)
        self._inner_thickness_hint = QLabel(tr("thickness_hint"))
        self._inner_thickness_hint.setObjectName("subtitleLabel")
        params_layout.addWidget(self._inner_thickness_hint, row, 2)
        row += 1

        # 外壁邊界層厚度
        self._outer_thickness_label = QLabel(tr("outer_thickness"))
        params_layout.addWidget(self._outer_thickness_label, row, 0)
        self._outer_thickness_spin = QDoubleSpinBox()
        self._outer_thickness_spin.setRange(0.01, 0.5)
        self._outer_thickness_spin.setDecimals(3)
        self._outer_thickness_spin.setValue(0.02)
        self._outer_thickness_spin.setSingleStep(0.01)
        params_layout.addWidget(self._outer_thickness_spin, row, 1)
        self._outer_thickness_hint = QLabel(tr("thickness_hint"))
        self._outer_thickness_hint.setObjectName("subtitleLabel")
        params_layout.addWidget(self._outer_thickness_hint, row, 2)
        row += 1

        # 內壁邊界層層數
        self._inner_layers_label = QLabel(tr("inner_layers"))
        params_layout.addWidget(self._inner_layers_label, row, 0)
        self._inner_layers_spin = QSpinBox()
        self._inner_layers_spin.setRange(1, 20)
        self._inner_layers_spin.setValue(5)
        params_layout.addWidget(self._inner_layers_spin, row, 1)
        row += 1

        # 外壁邊界層層數
        self._outer_layers_label = QLabel(tr("outer_layers"))
        params_layout.addWidget(self._outer_layers_label, row, 0)
        self._outer_layers_spin = QSpinBox()
        self._outer_layers_spin.setRange(1, 20)
        self._outer_layers_spin.setValue(5)
        params_layout.addWidget(self._outer_layers_spin, row, 1)
        row += 1

        # 邊界層擴展比
        self._expansion_label = QLabel(tr("expansion_ratio"))
        params_layout.addWidget(self._expansion_label, row, 0)
        self._expansion_spin = QDoubleSpinBox()
        self._expansion_spin.setRange(1.01, 2.0)
        self._expansion_spin.setDecimals(2)
        self._expansion_spin.setValue(1.2)
        self._expansion_spin.setSingleStep(0.05)
        params_layout.addWidget(self._expansion_spin, row, 1)
        self._expansion_hint = QLabel(tr("expansion_hint"))
        self._expansion_hint.setObjectName("subtitleLabel")
        params_layout.addWidget(self._expansion_hint, row, 2)

        group_layout.addWidget(self._params_widget)
        layout.addWidget(self._group)

    def _connect_signals(self) -> None:
        """連接信號"""
        self._enabled_check.toggled.connect(self._update_enabled_state)
        self._enabled_check.toggled.connect(self._emit_params)
        self._inner_thickness_spin.valueChanged.connect(self._emit_params)
        self._outer_thickness_spin.valueChanged.connect(self._emit_params)
        self._inner_layers_spin.valueChanged.connect(self._emit_params)
        self._outer_layers_spin.valueChanged.connect(self._emit_params)
        self._expansion_spin.valueChanged.connect(self._emit_params)

    def _update_enabled_state(self) -> None:
        """更新啟用狀態"""
        enabled = self._enabled_check.isChecked()
        self._params_widget.setEnabled(enabled)

    def _emit_params(self) -> None:
        """發射參數變更信號"""
        self.paramsChanged.emit(self.getParams())

    def retranslateUi(self) -> None:
        """重新翻譯 UI"""
        self._group.setTitle(tr("boundary_layer"))
        self._enabled_check.setText(tr("enable_bl"))
        self._inner_thickness_label.setText(tr("inner_thickness"))
        self._outer_thickness_label.setText(tr("outer_thickness"))
        self._inner_thickness_hint.setText(tr("thickness_hint"))
        self._outer_thickness_hint.setText(tr("thickness_hint"))
        self._inner_layers_label.setText(tr("inner_layers"))
        self._outer_layers_label.setText(tr("outer_layers"))
        self._expansion_label.setText(tr("expansion_ratio"))
        self._expansion_hint.setText(tr("expansion_hint"))

    def getParams(self) -> BoundaryLayerParams:
        """取得目前參數"""
        return BoundaryLayerParams(
            enabled=self._enabled_check.isChecked(),
            inner_thickness=self._inner_thickness_spin.value(),
            outer_thickness=self._outer_thickness_spin.value(),
            inner_layers=self._inner_layers_spin.value(),
            outer_layers=self._outer_layers_spin.value(),
            expansion_ratio=self._expansion_spin.value(),
        )

    def setParams(self, params: BoundaryLayerParams) -> None:
        """設定參數"""
        self._enabled_check.setChecked(params.enabled)
        self._inner_thickness_spin.setValue(params.inner_thickness)
        self._outer_thickness_spin.setValue(params.outer_thickness)
        self._inner_layers_spin.setValue(params.inner_layers)
        self._outer_layers_spin.setValue(params.outer_layers)
        self._expansion_spin.setValue(params.expansion_ratio)
