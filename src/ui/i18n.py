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
        "tab_excel": "Excel 轉換",
        "tab_cylinder": "圓柱網格",
        # File section
        "file_settings": "檔案設定",
        "excel_file": "Excel 檔案：",
        "output_file": "輸出檔案：",
        "output_settings": "輸出設定",
        "select_excel": "選擇包含流道數據的 Excel 檔案...",
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
        # Info
        "info": "說明",
        "excel_info": (
            "此工具將 Excel 中的 2D 流道點位數據轉換為 3D 圓柱網格。\n\n"
            "1. 選擇包含流道點位的 Excel 檔案\n"
            "2. 設定網格參數\n"
            "3. 可選：設定邊界層參數以優化近壁面網格\n"
            "4. 點擊「生成」按鈕創建 blockMeshDict 檔案\n\n"
            "注意：Excel 檔案需包含 X, Y, Z 三列座標"
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
        # Buttons
        "generate": "生成",
        "close": "關閉",
        # Status
        "ready": "就緒",
        "reading_excel": "正在讀取 Excel 檔案...",
        "generating": "正在生成 blockMeshDict...",
        "generated": "已生成：",
        "failed": "生成失敗",
        # Messages
        "success": "成功",
        "warning": "警告",
        "error": "錯誤",
        "param_error": "參數錯誤",
        "select_excel_file": "請選擇 Excel 檔案",
        "set_output_path": "請設定輸出檔案路徑",
        "file_not_found": "檔案不存在：",
        "process_error": "處理過程中發生錯誤：",
        "success_msg": "已成功生成 blockMeshDict 檔案：",
        # Language
        "language": "語言",
    },
    "en": {
        # Window
        "app_title": "BlockMesh Studio",
        "app_subtitle": "OpenFOAM blockMeshDict Mesh Generation Tool",
        # Tabs
        "tab_excel": "Excel Converter",
        "tab_cylinder": "Cylinder Mesh",
        # File section
        "file_settings": "File Settings",
        "excel_file": "Excel File:",
        "output_file": "Output File:",
        "output_settings": "Output Settings",
        "select_excel": "Select Excel file with flow channel data...",
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
        # Info
        "info": "Info",
        "excel_info": (
            "This tool converts 2D flow channel data from Excel to 3D cylindrical mesh.\n\n"
            "1. Select Excel file with flow channel points\n"
            "2. Set mesh parameters\n"
            "3. Optional: Set boundary layer parameters\n"
            "4. Click 'Generate' to create blockMeshDict\n\n"
            "Note: Excel file should contain X, Y, Z coordinates"
        ),
        "cylinder_info": (
            "This tool generates cylindrical mesh with X-axis as height direction.\n\n"
            "Mesh structure:\n"
            "• Center: square core region\n"
            "• Surround: fan-shaped transition\n"
            "• Outer: circular boundary\n\n"
            "Boundaries:\n"
            "• inlet: bottom face (X = base coordinate)\n"
            "• outlet: top face (X = base + height)\n"
            "• Enclosure: cylinder outer wall"
        ),
        # Buttons
        "generate": "Generate",
        "close": "Close",
        # Status
        "ready": "Ready",
        "reading_excel": "Reading Excel file...",
        "generating": "Generating blockMeshDict...",
        "generated": "Generated: ",
        "failed": "Generation failed",
        # Messages
        "success": "Success",
        "warning": "Warning",
        "error": "Error",
        "param_error": "Parameter Error",
        "select_excel_file": "Please select an Excel file",
        "set_output_path": "Please set output file path",
        "file_not_found": "File not found: ",
        "process_error": "Error during processing: ",
        "success_msg": "Successfully generated blockMeshDict: ",
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
