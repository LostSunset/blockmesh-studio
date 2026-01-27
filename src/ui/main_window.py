# -*- coding: utf-8 -*-
"""
主視窗模組

BlockMesh Studio 主應用程式視窗
採用無印良品風格設計
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
)
from PySide6.QtCore import Qt

from .widgets.file_selector import FileSelector
from .widgets.mesh_params_panel import MeshParamsPanel
from .widgets.boundary_layer_panel import BoundaryLayerPanel
from .widgets.cylinder_params_panel import CylinderParamsPanel
from .resources import get_stylesheet

from ..core.excel_reader import ExcelReader
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

        self._setup_window()
        self._setup_ui()
        self._apply_style()

    def _setup_window(self) -> None:
        """設定視窗屬性"""
        self.setWindowTitle("BlockMesh Studio")
        self.setMinimumSize(720, 800)
        self.resize(800, 900)

    def _setup_ui(self) -> None:
        """設定 UI"""
        # 中央元件
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # 標題
        title = QLabel("BlockMesh Studio")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        subtitle = QLabel("OpenFOAM blockMeshDict 網格生成工具")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle)

        # 分隔線
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Plain)
        main_layout.addWidget(line)

        # 分頁
        self._tabs = QTabWidget()
        main_layout.addWidget(self._tabs, 1)

        # Excel 轉換分頁
        self._setup_excel_tab()

        # 圓柱網格分頁
        self._setup_cylinder_tab()

        # 狀態列
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        self._status_bar.showMessage("就緒")

    def _setup_excel_tab(self) -> None:
        """設定 Excel 轉換分頁"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)

        # 捲動區域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(16)

        # 檔案選擇區
        file_group = QGroupBox("檔案設定")
        file_layout = QVBoxLayout(file_group)
        file_layout.setSpacing(12)

        # Excel 檔案
        excel_label = QLabel("Excel 檔案：")
        file_layout.addWidget(excel_label)
        self._excel_selector = FileSelector(
            mode="open",
            file_filter="Excel 檔案 (*.xlsx *.xls);;所有檔案 (*.*)",
            placeholder="選擇包含流道數據的 Excel 檔案...",
        )
        self._excel_selector.fileChanged.connect(self._on_excel_changed)
        file_layout.addWidget(self._excel_selector)

        # 輸出檔案
        output_label = QLabel("輸出檔案：")
        file_layout.addWidget(output_label)
        self._output_selector = FileSelector(
            mode="save",
            file_filter="所有檔案 (*);;Dict 檔案 (*.dict)",
            default_name="blockMeshDict",
            placeholder="輸出 blockMeshDict 路徑...",
        )
        file_layout.addWidget(self._output_selector)

        scroll_layout.addWidget(file_group)

        # 網格參數
        self._mesh_panel = MeshParamsPanel()
        self._mesh_panel.paramsChanged.connect(self._on_mesh_params_changed)
        scroll_layout.addWidget(self._mesh_panel)

        # 邊界層參數
        self._bl_panel = BoundaryLayerPanel()
        self._bl_panel.paramsChanged.connect(self._on_bl_params_changed)
        scroll_layout.addWidget(self._bl_panel)

        # 說明
        info_group = QGroupBox("說明")
        info_layout = QVBoxLayout(info_group)
        info_text = QLabel(
            "此工具將 Excel 中的 2D 流道點位數據轉換為 3D 圓柱網格。\n\n"
            "1. 選擇包含流道點位的 Excel 檔案\n"
            "2. 設定網格參數\n"
            "3. 可選：設定邊界層參數以優化近壁面網格\n"
            "4. 點擊「生成」按鈕創建 blockMeshDict 檔案\n\n"
            "注意：Excel 檔案需包含 X, Y, Z 三列座標"
        )
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        scroll_layout.addWidget(info_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # 按鈕區
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        close_btn = QPushButton("關閉")
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)

        generate_btn = QPushButton("生成")
        generate_btn.setObjectName("primaryButton")
        generate_btn.clicked.connect(self._on_generate_excel)
        btn_layout.addWidget(generate_btn)

        layout.addLayout(btn_layout)

        self._tabs.addTab(tab, "Excel 轉換")

    def _setup_cylinder_tab(self) -> None:
        """設定圓柱網格分頁"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)

        # 捲動區域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(16)

        # 輸出檔案
        file_group = QGroupBox("輸出設定")
        file_layout = QVBoxLayout(file_group)

        output_label = QLabel("輸出檔案：")
        file_layout.addWidget(output_label)
        self._cylinder_output = FileSelector(
            mode="save",
            file_filter="所有檔案 (*);;Dict 檔案 (*.dict)",
            default_name="blockMeshDict",
            placeholder="輸出 blockMeshDict 路徑...",
        )
        file_layout.addWidget(self._cylinder_output)
        scroll_layout.addWidget(file_group)

        # 圓柱參數
        self._cylinder_panel = CylinderParamsPanel()
        self._cylinder_panel.paramsChanged.connect(self._on_cylinder_params_changed)
        scroll_layout.addWidget(self._cylinder_panel)

        # 說明
        info_group = QGroupBox("說明")
        info_layout = QVBoxLayout(info_group)
        info_text = QLabel(
            "此工具生成以 X 軸為高度方向的圓柱形網格。\n\n"
            "網格結構：\n"
            "• 中心為正方形核心區域\n"
            "• 四周為扇形過渡區域\n"
            "• 外圈為圓形邊界\n\n"
            "邊界設定：\n"
            "• inlet：底面（X = 底面座標）\n"
            "• outlet：頂面（X = 底面座標 + 高度）\n"
            "• Enclosure：圓柱外壁"
        )
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        scroll_layout.addWidget(info_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # 按鈕區
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        close_btn = QPushButton("關閉")
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)

        generate_btn = QPushButton("生成")
        generate_btn.setObjectName("primaryButton")
        generate_btn.clicked.connect(self._on_generate_cylinder)
        btn_layout.addWidget(generate_btn)

        layout.addLayout(btn_layout)

        self._tabs.addTab(tab, "圓柱網格")

    def _apply_style(self) -> None:
        """套用樣式表"""
        stylesheet = get_stylesheet()
        if stylesheet:
            self.setStyleSheet(stylesheet)

    def _on_excel_changed(self, path: str) -> None:
        """處理 Excel 路徑變更"""
        if path:
            # 自動設定輸出路徑
            p = Path(path)
            case_dir = p.parent / p.stem
            system_dir = case_dir / "system"
            self._output_selector.setPath(str(system_dir / "blockMeshDict"))

    def _on_mesh_params_changed(self, params: MeshParameters) -> None:
        """處理網格參數變更"""
        self._mesh_params = params

    def _on_bl_params_changed(self, params: BoundaryLayerParams) -> None:
        """處理邊界層參數變更"""
        self._bl_params = params

    def _on_cylinder_params_changed(self, params: CylinderMeshParams) -> None:
        """處理圓柱參數變更"""
        self._cylinder_params = params

    def _on_generate_excel(self) -> None:
        """生成 Excel 轉換的 blockMeshDict"""
        excel_path = self._excel_selector.path()
        output_path = self._output_selector.path()

        if not excel_path:
            QMessageBox.warning(self, "警告", "請選擇 Excel 檔案")
            return

        if not output_path:
            QMessageBox.warning(self, "警告", "請設定輸出檔案路徑")
            return

        # 驗證參數
        valid, msg = self._mesh_params.validate()
        if not valid:
            QMessageBox.warning(self, "參數錯誤", msg)
            return

        valid, msg = self._bl_params.validate()
        if not valid:
            QMessageBox.warning(self, "參數錯誤", msg)
            return

        try:
            self._status_bar.showMessage("正在讀取 Excel 檔案...")

            # 讀取 Excel
            reader = ExcelReader(excel_path)
            reader.read()
            inner_samples, outer_samples = reader.sample_layers(
                self._mesh_params.num_layers
            )

            self._status_bar.showMessage("正在生成 blockMeshDict...")

            # 生成網格
            generator = MeshGenerator(self._mesh_params, self._bl_params)
            generator.generate(inner_samples, outer_samples, output_path)

            self._status_bar.showMessage(f"已生成：{output_path}")
            QMessageBox.information(
                self, "成功", f"已成功生成 blockMeshDict 檔案：\n{output_path}"
            )

        except FileNotFoundError as e:
            QMessageBox.critical(self, "錯誤", f"檔案不存在：{e}")
            self._status_bar.showMessage("生成失敗")
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"處理過程中發生錯誤：\n{e}")
            self._status_bar.showMessage("生成失敗")

    def _on_generate_cylinder(self) -> None:
        """生成圓柱網格的 blockMeshDict"""
        output_path = self._cylinder_output.path()

        if not output_path:
            QMessageBox.warning(self, "警告", "請設定輸出檔案路徑")
            return

        # 驗證參數
        valid, msg = self._cylinder_params.validate()
        if not valid:
            QMessageBox.warning(self, "參數錯誤", msg)
            return

        try:
            self._status_bar.showMessage("正在生成圓柱網格...")

            generator = CylinderMeshGenerator(self._cylinder_params)
            generator.generate(output_path)

            self._status_bar.showMessage(f"已生成：{output_path}")
            QMessageBox.information(
                self, "成功", f"已成功生成 blockMeshDict 檔案：\n{output_path}"
            )

        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"處理過程中發生錯誤：\n{e}")
            self._status_bar.showMessage("生成失敗")
