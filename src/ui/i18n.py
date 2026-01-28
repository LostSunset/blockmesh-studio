# -*- coding: utf-8 -*-
"""
國際化 (i18n) 翻譯模組
Internationalization translation module
"""

from typing import Dict

# 翻譯字典
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "zh_TW": {
        # Window
        "app_title": "BlockMesh Studio",
        "app_subtitle": "OpenFOAM blockMeshDict 網格生成工具",
        # Tabs
        "tab_excel": "流道轉換",
        "tab_cylinder": "圓柱網格",
        # File section
        "file_settings": "檔案設定",
        "data_file": "資料檔案：",
        "output_file": "輸出檔案：",
        "output_settings": "輸出設定",
        "select_data": "選擇流道數據檔案 (Excel/CSV/TXT)...",
        "output_path": "輸出 blockMeshDict 路徑...",
        "browse": "瀏覽...",
        # Mesh params
        "mesh_params": "網格參數設定",
        "scale_factor": "尺度因子：",
        "scale_hint": "控制整體網格的尺度比例",
        "num_layers": "層數（Z軸截面數）：",
        "layers_hint": "值越大，Z 方向取樣越密集",
        "radial_cells": "徑向網格數：",
        "radial_hint": "內壁到外壁的網格密度",
        "circum_cells": "圓周方向網格數：",
        "circum_hint": "需為 4 的倍數",
        "axial_cells": "軸向網格數：",
        "axial_hint": "每段 Z 方向的網格密度",
        # Boundary layer
        "boundary_layer": "邊界層控制",
        "enable_bl": "啟用邊界層控制",
        "inner_thickness": "內壁邊界層厚度：",
        "outer_thickness": "外壁邊界層厚度：",
        "thickness_hint": "相對於徑向距離的比例",
        "inner_layers": "內壁邊界層層數：",
        "outer_layers": "外壁邊界層層數：",
        "expansion_ratio": "邊界層擴展比：",
        "expansion_hint": "每層相對於上一層的厚度比例",
        # Cylinder params
        "geometry_params": "幾何參數",
        "square_side": "內方形邊長：",
        "square_curve": "內方形曲率：",
        "curve_hint": "必須大於內方形邊長",
        "radius": "圓柱半徑：",
        "height": "圓柱高度：",
        "base_x": "底面 X 座標：",
        "mesh_params_cyl": "網格參數",
        "square_cells": "內方形網格數：",
        "inner_cells": "內圓環網格數：",
        "height_cells": "高度方向網格數：",
        # Data info panel
        "data_info": "資料說明",
        "coord_system": "座標系統",
        "coord_desc": (
            "• X 軸：流道高度方向（軸向）\n"
            "• Y 軸：徑向位置\n"
            "• Z 軸：流道發展方向\n\n"
            "資料會自動依 X 座標平均值分離為內外曲線"
        ),
        "data_format": "資料格式",
        "format_desc": (
            "支援格式：Excel (.xlsx/.xls)、CSV、TXT\n\n"
            "檔案需包含三欄：X, Y, Z 座標\n"
            "可有或無標題行（自動偵測）"
        ),
        "data_statistics": "資料統計",
        "total_points": "總點數：",
        "inner_points": "內曲線點數：",
        "outer_points": "外曲線點數：",
        "x_range": "X 範圍：",
        "y_range": "Y 範圍：",
        "z_range": "Z 範圍：",
        "no_data": "尚未載入資料",
        # Info
        "info": "說明",
        "excel_info": (
            "此工具將流道點位數據轉換為 3D 圓柱網格。\n\n"
            "支援格式：Excel (.xlsx/.xls)、CSV、TXT\n\n"
            "步驟：\n"
            "1. 選擇包含流道點位的資料檔案\n"
            "2. 檢查資料統計資訊\n"
            "3. 設定網格參數\n"
            "4. 點擊「生成」創建 blockMeshDict"
        ),
        "cylinder_info": (
            "此工具生成以 X 軸為高度方向的圓柱形網格。\n\n"
            "網格結構：\n"
            "• 中心為正方形核心區域\n"
            "• 四周為扇形過渡區域\n"
            "• 外圈為圓形邊界\n\n"
            "邊界設定：\n"
            "• inlet：底面（X = 底面座標）\n"
            "• outlet：頂面（X = 底面座標 + 高度）\n"
            "• Enclosure：圓柱外壁"
        ),
        # Tooltips
        "tip_scale": "縮放整體網格尺寸，1.0 表示原始尺寸",
        "tip_layers": "沿 Z 軸方向的取樣層數，決定網格軸向解析度",
        "tip_radial": "從內壁到外壁的網格數量",
        "tip_circum": "圓周方向的網格數量，必須是 4 的倍數",
        "tip_axial": "每個 Z 方向段落內的網格數量",
        "tip_bl_thickness": "邊界層厚度，以徑向距離比例表示 (0~1)",
        "tip_bl_layers": "邊界層內的網格層數",
        "tip_expansion": "相鄰邊界層間的厚度比例，通常設定 1.1~1.5",
        # Buttons
        "generate": "生成",
        "close": "關閉",
        "load_data": "載入資料",
        # Status
        "ready": "就緒",
        "reading_data": "正在讀取資料檔案...",
        "data_loaded": "資料已載入：",
        "generating": "正在生成 blockMeshDict...",
        "generated": "已生成：",
        "failed": "生成失敗",
        # Messages
        "success": "成功",
        "warning": "警告",
        "error": "錯誤",
        "param_error": "參數錯誤",
        "select_data_file": "請選擇資料檔案",
        "set_output_path": "請設定輸出檔案路徑",
        "file_not_found": "檔案不存在：",
        "process_error": "處理過程中發生錯誤：",
        "success_msg": "已成功生成 blockMeshDict 檔案：",
        "unsupported_format": "不支援的檔案格式",
        # Language
        "language": "語言",
    },
    "en": {
        # Window
        "app_title": "BlockMesh Studio",
        "app_subtitle": "OpenFOAM blockMeshDict Mesh Generation Tool",
        # Tabs
        "tab_excel": "Flow Channel",
        "tab_cylinder": "Cylinder Mesh",
        # File section
        "file_settings": "File Settings",
        "data_file": "Data File:",
        "output_file": "Output File:",
        "output_settings": "Output Settings",
        "select_data": "Select flow channel data file (Excel/CSV/TXT)...",
        "output_path": "Output blockMeshDict path...",
        "browse": "Browse...",
        # Mesh params
        "mesh_params": "Mesh Parameters",
        "scale_factor": "Scale Factor:",
        "scale_hint": "Controls overall mesh scale ratio",
        "num_layers": "Number of Layers (Z-axis sections):",
        "layers_hint": "Higher value = denser Z sampling",
        "radial_cells": "Radial Cells:",
        "radial_hint": "Mesh density from inner to outer wall",
        "circum_cells": "Circumferential Cells:",
        "circum_hint": "Must be multiple of 4",
        "axial_cells": "Axial Cells:",
        "axial_hint": "Mesh density per Z segment",
        # Boundary layer
        "boundary_layer": "Boundary Layer Control",
        "enable_bl": "Enable Boundary Layer Control",
        "inner_thickness": "Inner Wall BL Thickness:",
        "outer_thickness": "Outer Wall BL Thickness:",
        "thickness_hint": "Ratio relative to radial distance",
        "inner_layers": "Inner Wall BL Layers:",
        "outer_layers": "Outer Wall BL Layers:",
        "expansion_ratio": "BL Expansion Ratio:",
        "expansion_hint": "Thickness ratio between layers",
        # Cylinder params
        "geometry_params": "Geometry Parameters",
        "square_side": "Inner Square Side:",
        "square_curve": "Inner Square Curve:",
        "curve_hint": "Must be greater than inner square side",
        "radius": "Cylinder Radius:",
        "height": "Cylinder Height:",
        "base_x": "Base X Coordinate:",
        "mesh_params_cyl": "Mesh Parameters",
        "square_cells": "Inner Square Cells:",
        "inner_cells": "Inner Ring Cells:",
        "height_cells": "Height Cells:",
        # Data info panel
        "data_info": "Data Info",
        "coord_system": "Coordinate System",
        "coord_desc": (
            "• X-axis: Flow channel height (axial)\n"
            "• Y-axis: Radial position\n"
            "• Z-axis: Flow development direction\n\n"
            "Data is split into inner/outer curves by avg X value"
        ),
        "data_format": "Data Format",
        "format_desc": (
            "Supported: Excel (.xlsx/.xls), CSV, TXT\n\n"
            "File must contain 3 columns: X, Y, Z coordinates\n"
            "Header row auto-detected"
        ),
        "data_statistics": "Data Statistics",
        "total_points": "Total Points:",
        "inner_points": "Inner Curve Points:",
        "outer_points": "Outer Curve Points:",
        "x_range": "X Range:",
        "y_range": "Y Range:",
        "z_range": "Z Range:",
        "no_data": "No data loaded",
        # Info
        "info": "Info",
        "excel_info": (
            "Convert flow channel data to 3D cylindrical mesh.\n\n"
            "Supported: Excel (.xlsx/.xls), CSV, TXT\n\n"
            "Steps:\n"
            "1. Select data file with flow channel points\n"
            "2. Check data statistics\n"
            "3. Set mesh parameters\n"
            "4. Click 'Generate' to create blockMeshDict"
        ),
        "cylinder_info": (
            "Generate cylindrical mesh with X-axis as height.\n\n"
            "Mesh structure:\n"
            "• Center: square core region\n"
            "• Surround: fan-shaped transition\n"
            "• Outer: circular boundary\n\n"
            "Boundaries:\n"
            "• inlet: bottom face (X = base)\n"
            "• outlet: top face (X = base + height)\n"
            "• Enclosure: cylinder outer wall"
        ),
        # Tooltips
        "tip_scale": "Scale overall mesh size, 1.0 = original size",
        "tip_layers": "Sampling layers along Z-axis, affects axial resolution",
        "tip_radial": "Number of cells from inner to outer wall",
        "tip_circum": "Circumferential cells, must be multiple of 4",
        "tip_axial": "Cells per Z-direction segment",
        "tip_bl_thickness": "Boundary layer thickness ratio (0~1)",
        "tip_bl_layers": "Number of layers in boundary layer",
        "tip_expansion": "Thickness ratio between adjacent BL layers (1.1~1.5)",
        # Buttons
        "generate": "Generate",
        "close": "Close",
        "load_data": "Load Data",
        # Status
        "ready": "Ready",
        "reading_data": "Reading data file...",
        "data_loaded": "Data loaded: ",
        "generating": "Generating blockMeshDict...",
        "generated": "Generated: ",
        "failed": "Generation failed",
        # Messages
        "success": "Success",
        "warning": "Warning",
        "error": "Error",
        "param_error": "Parameter Error",
        "select_data_file": "Please select a data file",
        "set_output_path": "Please set output file path",
        "file_not_found": "File not found: ",
        "process_error": "Error during processing: ",
        "success_msg": "Successfully generated blockMeshDict: ",
        "unsupported_format": "Unsupported file format",
        # Language
        "language": "Language",
    },
}


class Translator:
    """翻譯器類別"""

    _instance = None
    _current_lang = "zh_TW"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> "Translator":
        """獲取單例實例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def current_language(self) -> str:
        """當前語言"""
        return self._current_lang

    @current_language.setter
    def current_language(self, lang: str) -> None:
        """設定當前語言"""
        if lang in TRANSLATIONS:
            self._current_lang = lang

    def translate(self, key: str) -> str:
        """翻譯指定的 key"""
        return TRANSLATIONS.get(self._current_lang, {}).get(key, key)

    def available_languages(self) -> list:
        """可用語言列表"""
        return list(TRANSLATIONS.keys())


# 全域翻譯函數
def tr(key: str) -> str:
    """翻譯快捷函數"""
    return Translator.get_instance().translate(key)


def set_language(lang: str) -> None:
    """設定語言"""
    Translator.get_instance().current_language = lang


def get_language() -> str:
    """獲取當前語言"""
    return Translator.get_instance().current_language
