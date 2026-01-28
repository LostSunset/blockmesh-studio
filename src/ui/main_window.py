# -*- coding: utf-8 -*-
"""
主視窗模組

BlockMesh Studio 主應用程式視窗
採用無印良品風格設計，支援中英文切換
"""

from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QLabel,
    QPushButton,
    QMessageBox,
    QGroupBox,
    QScrollArea,
    QStatusBar,
    QFrame,
    QComboBox,
)
from PySide6.QtCore import Qt

from .widgets.file_selector import FileSelector
from .widgets.mesh_params_panel import MeshParamsPanel
from .widgets.boundary_layer_panel import BoundaryLayerPanel
from .widgets.cylinder_params_panel import CylinderParamsPanel
from .widgets.data_info_panel import DataInfoPanel
from .resources import get_stylesheet
from .i18n import tr, set_language, get_language

from ..core.data_reader import DataReader
from ..core.mesh_generator import MeshGenerator
from ..core.cylinder_mesh import CylinderMeshGenerator
from ..models.mesh_params import MeshParameters, BoundaryLayerParams, CylinderMeshParams


class MainWindow(QMainWindow):
    """主視窗"""

    def __init__(self):
        super().__init__()

        self._mesh_params = MeshParameters()
        self._bl_params = BoundaryLayerParams()
        self._cylinder_params = CylinderMeshParams()
        self._data_reader = None

        self._setup_window()
        self._setup_ui()
        self._apply_style()
        self._setup_tooltips()

    def _setup_window(self) -> None:
        """設定視窗屬性"""
        self.setWindowTitle(tr("app_title"))
        self.setMinimumSize(820, 900)
        self.resize(900, 1000)

    def _setup_ui(self) -> None:
        """設定 UI"""
        # 中央元件
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # 標題列（含語言切換）
        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        self._title = QLabel(tr("app_title"))
        self._title.setObjectName("titleLabel")
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(self._title)

        self._subtitle = QLabel(tr("app_subtitle"))
        self._subtitle.setObjectName("subtitleLabel")
        self._subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(self._subtitle)

        header_layout.addLayout(title_layout, 1)

        # 語言切換
        lang_layout = QVBoxLayout()
        self._lang_label = QLabel(tr("language") + ":")
        self._lang_label.setObjectName("subtitleLabel")
        lang_layout.addWidget(self._lang_label)

        self._lang_combo = QComboBox()
        self._lang_combo.addItem("正體中文", "zh_TW")
        self._lang_combo.addItem("English", "en")
        self._lang_combo.setCurrentIndex(0 if get_language() == "zh_TW" else 1)
        self._lang_combo.currentIndexChanged.connect(self._on_language_changed)
        lang_layout.addWidget(self._lang_combo)

        header_layout.addLayout(lang_layout)
        main_layout.addLayout(header_layout)

        # 分隔線
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Plain)
        main_layout.addWidget(line)

        # 分頁
        self._tabs = QTabWidget()
        main_layout.addWidget(self._tabs, 1)

        # 流道轉換分頁
        self._setup_flow_channel_tab()

        # 圓柱網格分頁
        self._setup_cylinder_tab()

        # 狀態列
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        self._status_bar.showMessage(tr("ready"))

    def _setup_flow_channel_tab(self) -> None:
        """設定流道轉換分頁"""
        self._flow_tab = QWidget()
        layout = QVBoxLayout(self._flow_tab)
        layout.setSpacing(16)

        # 捲動區域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(16)

        # 檔案選擇區
        self._file_group = QGroupBox(tr("file_settings"))
        file_layout = QVBoxLayout(self._file_group)
        file_layout.setSpacing(12)

        # 資料檔案
        self._data_label = QLabel(tr("data_file"))
        file_layout.addWidget(self._data_label)
        self._data_selector = FileSelector(
            mode="open",
            file_filter=DataReader.get_file_filter(),
            placeholder=tr("select_data"),
        )
        self._data_selector.fileChanged.connect(self._on_data_file_changed)
        file_layout.addWidget(self._data_selector)

        # 輸出檔案
        self._output_label = QLabel(tr("output_file"))
        file_layout.addWidget(self._output_label)
        self._output_selector = FileSelector(
            mode="save",
            file_filter="All Files (*);;Dict Files (*.dict)",
            default_name="blockMeshDict",
            placeholder=tr("output_path"),
        )
        file_layout.addWidget(self._output_selector)

        scroll_layout.addWidget(self._file_group)

        # 資料說明面板
        self._data_info_panel = DataInfoPanel()
        scroll_layout.addWidget(self._data_info_panel)

        # 網格參數
        self._mesh_panel = MeshParamsPanel()
        self._mesh_panel.paramsChanged.connect(self._on_mesh_params_changed)
        scroll_layout.addWidget(self._mesh_panel)

        # 邊界層參數
        self._bl_panel = BoundaryLayerPanel()
        self._bl_panel.paramsChanged.connect(self._on_bl_params_changed)
        scroll_layout.addWidget(self._bl_panel)

        # 說明
        self._flow_info_group = QGroupBox(tr("info"))
        info_layout = QVBoxLayout(self._flow_info_group)
        self._flow_info_text = QLabel(tr("excel_info"))
        self._flow_info_text.setWordWrap(True)
        info_layout.addWidget(self._flow_info_text)
        scroll_layout.addWidget(self._flow_info_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # 按鈕區
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self._flow_close_btn = QPushButton(tr("close"))
        self._flow_close_btn.clicked.connect(self.close)
        btn_layout.addWidget(self._flow_close_btn)

        self._flow_generate_btn = QPushButton(tr("generate"))
        self._flow_generate_btn.setObjectName("primaryButton")
        self._flow_generate_btn.clicked.connect(self._on_generate_flow)
        btn_layout.addWidget(self._flow_generate_btn)

        layout.addLayout(btn_layout)

        self._tabs.addTab(self._flow_tab, tr("tab_excel"))

    def _setup_cylinder_tab(self) -> None:
        """設定圓柱網格分頁"""
        self._cylinder_tab = QWidget()
        layout = QVBoxLayout(self._cylinder_tab)
        layout.setSpacing(16)

        # 捲動區域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(16)

        # 輸出檔案
        self._cyl_file_group = QGroupBox(tr("output_settings"))
        file_layout = QVBoxLayout(self._cyl_file_group)

        self._cyl_output_label = QLabel(tr("output_file"))
        file_layout.addWidget(self._cyl_output_label)
        self._cylinder_output = FileSelector(
            mode="save",
            file_filter="All Files (*);;Dict Files (*.dict)",
            default_name="blockMeshDict",
            placeholder=tr("output_path"),
        )
        file_layout.addWidget(self._cylinder_output)
        scroll_layout.addWidget(self._cyl_file_group)

        # 圓柱參數
        self._cylinder_panel = CylinderParamsPanel()
        self._cylinder_panel.paramsChanged.connect(self._on_cylinder_params_changed)
        scroll_layout.addWidget(self._cylinder_panel)

        # 說明
        self._cyl_info_group = QGroupBox(tr("info"))
        info_layout = QVBoxLayout(self._cyl_info_group)
        self._cyl_info_text = QLabel(tr("cylinder_info"))
        self._cyl_info_text.setWordWrap(True)
        info_layout.addWidget(self._cyl_info_text)
        scroll_layout.addWidget(self._cyl_info_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # 按鈕區
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self._cyl_close_btn = QPushButton(tr("close"))
        self._cyl_close_btn.clicked.connect(self.close)
        btn_layout.addWidget(self._cyl_close_btn)

        self._cyl_generate_btn = QPushButton(tr("generate"))
        self._cyl_generate_btn.setObjectName("primaryButton")
        self._cyl_generate_btn.clicked.connect(self._on_generate_cylinder)
        btn_layout.addWidget(self._cyl_generate_btn)

        layout.addLayout(btn_layout)

        self._tabs.addTab(self._cylinder_tab, tr("tab_cylinder"))

    def _setup_tooltips(self) -> None:
        """設定工具提示"""
        # 由 mesh_params_panel 和 boundary_layer_panel 內部處理
        pass

    def _apply_style(self) -> None:
        """套用樣式表"""
        stylesheet = get_stylesheet()
        if stylesheet:
            self.setStyleSheet(stylesheet)

    def _on_language_changed(self, index: int) -> None:
        """處理語言變更"""
        lang = self._lang_combo.itemData(index)
        set_language(lang)
        self._retranslate_ui()

    def _retranslate_ui(self) -> None:
        """重新翻譯所有 UI 元素"""
        # 視窗標題
        self.setWindowTitle(tr("app_title"))
        self._title.setText(tr("app_title"))
        self._subtitle.setText(tr("app_subtitle"))
        self._lang_label.setText(tr("language") + ":")

        # 分頁標題
        self._tabs.setTabText(0, tr("tab_excel"))
        self._tabs.setTabText(1, tr("tab_cylinder"))

        # 流道分頁
        self._file_group.setTitle(tr("file_settings"))
        self._data_label.setText(tr("data_file"))
        self._output_label.setText(tr("output_file"))
        self._data_selector.setPlaceholder(tr("select_data"))
        self._output_selector.setPlaceholder(tr("output_path"))
        self._flow_info_group.setTitle(tr("info"))
        self._flow_info_text.setText(tr("excel_info"))
        self._flow_close_btn.setText(tr("close"))
        self._flow_generate_btn.setText(tr("generate"))

        # 圓柱分頁
        self._cyl_file_group.setTitle(tr("output_settings"))
        self._cyl_output_label.setText(tr("output_file"))
        self._cylinder_output.setPlaceholder(tr("output_path"))
        self._cyl_info_group.setTitle(tr("info"))
        self._cyl_info_text.setText(tr("cylinder_info"))
        self._cyl_close_btn.setText(tr("close"))
        self._cyl_generate_btn.setText(tr("generate"))

        # 子面板
        self._data_selector.retranslateUi()
        self._output_selector.retranslateUi()
        self._cylinder_output.retranslateUi()
        self._data_info_panel.retranslateUi()
        self._mesh_panel.retranslateUi()
        self._bl_panel.retranslateUi()
        self._cylinder_panel.retranslateUi()

        # 狀態列
        self._status_bar.showMessage(tr("ready"))

    def _on_data_file_changed(self, path: str) -> None:
        """處理資料檔案路徑變更"""
        if not path:
            self._data_info_panel.clearStatistics()
            return

        # 檢查檔案格式
        if not DataReader.is_supported(path):
            QMessageBox.warning(self, tr("warning"), tr("unsupported_format"))
            return

        # 嘗試載入資料
        try:
            self._status_bar.showMessage(tr("reading_data"))
            self._data_reader = DataReader(path)
            self._data_reader.read()

            # 更新統計資訊
            self._data_info_panel.setStatistics(self._data_reader.statistics)

            # 自動設定輸出路徑
            p = Path(path)
            case_dir = p.parent / p.stem
            system_dir = case_dir / "system"
            self._output_selector.setPath(str(system_dir / "blockMeshDict"))

            self._status_bar.showMessage(
                tr("data_loaded")
                + f"{self._data_reader.statistics.total_points} "
                + tr("total_points").rstrip("：:")
            )

        except Exception as e:
            QMessageBox.warning(self, tr("error"), tr("process_error") + f"\n{e}")
            self._data_info_panel.clearStatistics()
            self._status_bar.showMessage(tr("ready"))

    def _on_mesh_params_changed(self, params: MeshParameters) -> None:
        """處理網格參數變更"""
        self._mesh_params = params

    def _on_bl_params_changed(self, params: BoundaryLayerParams) -> None:
        """處理邊界層參數變更"""
        self._bl_params = params

    def _on_cylinder_params_changed(self, params: CylinderMeshParams) -> None:
        """處理圓柱參數變更"""
        self._cylinder_params = params

    def _on_generate_flow(self) -> None:
        """生成流道轉換的 blockMeshDict"""
        data_path = self._data_selector.path()
        output_path = self._output_selector.path()

        if not data_path:
            QMessageBox.warning(self, tr("warning"), tr("select_data_file"))
            return

        if not output_path:
            QMessageBox.warning(self, tr("warning"), tr("set_output_path"))
            return

        # 驗證參數
        valid, msg = self._mesh_params.validate()
        if not valid:
            QMessageBox.warning(self, tr("param_error"), msg)
            return

        valid, msg = self._bl_params.validate()
        if not valid:
            QMessageBox.warning(self, tr("param_error"), msg)
            return

        try:
            self._status_bar.showMessage(tr("reading_data"))

            # 讀取資料（如果還沒讀取）
            if self._data_reader is None:
                self._data_reader = DataReader(data_path)
                self._data_reader.read()

            inner_samples, outer_samples = self._data_reader.sample_layers(
                self._mesh_params.num_layers
            )

            self._status_bar.showMessage(tr("generating"))

            # 生成網格
            generator = MeshGenerator(self._mesh_params, self._bl_params)
            generator.generate(inner_samples, outer_samples, output_path)

            self._status_bar.showMessage(tr("generated") + output_path)
            QMessageBox.information(
                self, tr("success"), tr("success_msg") + f"\n{output_path}"
            )

        except FileNotFoundError as e:
            QMessageBox.critical(self, tr("error"), tr("file_not_found") + str(e))
            self._status_bar.showMessage(tr("failed"))
        except Exception as e:
            QMessageBox.critical(self, tr("error"), tr("process_error") + f"\n{e}")
            self._status_bar.showMessage(tr("failed"))

    def _on_generate_cylinder(self) -> None:
        """生成圓柱網格的 blockMeshDict"""
        output_path = self._cylinder_output.path()

        if not output_path:
            QMessageBox.warning(self, tr("warning"), tr("set_output_path"))
            return

        # 驗證參數
        valid, msg = self._cylinder_params.validate()
        if not valid:
            QMessageBox.warning(self, tr("param_error"), msg)
            return

        try:
            self._status_bar.showMessage(tr("generating"))

            generator = CylinderMeshGenerator(self._cylinder_params)
            generator.generate(output_path)

            self._status_bar.showMessage(tr("generated") + output_path)
            QMessageBox.information(
                self, tr("success"), tr("success_msg") + f"\n{output_path}"
            )

        except Exception as e:
            QMessageBox.critical(self, tr("error"), tr("process_error") + f"\n{e}")
            self._status_bar.showMessage(tr("failed"))
