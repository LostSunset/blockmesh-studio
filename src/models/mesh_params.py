# -*- coding: utf-8 -*-
"""
網格參數資料模型

定義網格生成所需的參數資料類別
"""

from dataclasses import dataclass


@dataclass
class MeshParameters:
    """網格基本參數"""

    # 尺度因子
    scale_factor: float = 1.0

    # 層數（Z軸方向的截面數）
    num_layers: int = 100

    # 徑向網格數（內壁到外壁）
    n_cells_radial: int = 25

    # 圓周方向網格數（需為4的倍數）
    n_cells_circum: int = 400

    # 軸向網格數（每段Z方向）
    n_cells_axial: int = 2

    def validate(self) -> tuple[bool, str]:
        """驗證參數有效性"""
        if self.scale_factor <= 0:
            return False, "尺度因子必須大於 0"
        if self.num_layers < 2:
            return False, "層數必須至少為 2"
        if self.n_cells_radial < 1:
            return False, "徑向網格數必須至少為 1"
        if self.n_cells_circum < 4 or self.n_cells_circum % 4 != 0:
            return False, "圓周方向網格數必須是 4 的倍數且至少為 4"
        if self.n_cells_axial < 1:
            return False, "軸向網格數必須至少為 1"
        return True, ""


@dataclass
class BoundaryLayerParams:
    """邊界層參數"""

    # 是否啟用邊界層
    enabled: bool = False

    # 內壁邊界層厚度（相對於徑向距離的比例）
    inner_thickness: float = 0.02

    # 外壁邊界層厚度（相對於徑向距離的比例）
    outer_thickness: float = 0.02

    # 內壁邊界層層數
    inner_layers: int = 5

    # 外壁邊界層層數
    outer_layers: int = 5

    # 邊界層擴展比（每層相對於上一層的厚度比例）
    expansion_ratio: float = 1.2

    def validate(self) -> tuple[bool, str]:
        """驗證參數有效性"""
        if not self.enabled:
            return True, ""

        if self.inner_thickness <= 0 or self.inner_thickness >= 1:
            return False, "內壁邊界層厚度必須大於 0 且小於 1"
        if self.outer_thickness <= 0 or self.outer_thickness >= 1:
            return False, "外壁邊界層厚度必須大於 0 且小於 1"
        if self.inner_thickness + self.outer_thickness >= 1:
            return False, "內外壁邊界層厚度總和必須小於 1"
        if self.inner_layers < 1:
            return False, "內壁邊界層層數必須至少為 1"
        if self.outer_layers < 1:
            return False, "外壁邊界層層數必須至少為 1"
        if self.expansion_ratio <= 1:
            return False, "邊界層擴展比必須大於 1"

        return True, ""


@dataclass
class CylinderMeshParams:
    """圓柱網格參數（取代 M4 模板）"""

    # 內方形邊長的一半
    inner_square_side: float = 0.3

    # 內方形曲率（必須略大於 inner_square_side）
    inner_square_curve: float = 0.4

    # 圓柱半徑
    radius: float = 1.8

    # 圓柱高度（X 方向）
    height: float = 5.33

    # 底面起始 X 座標
    base_x: float = -1.8

    # 內方形網格數
    n_cells_square: int = 30

    # 內方形到圓形之間的網格數
    n_cells_inner: int = 30

    # 高度方向網格數
    n_cells_height: int = 120

    def validate(self) -> tuple[bool, str]:
        """驗證參數有效性"""
        if self.inner_square_side <= 0:
            return False, "內方形邊長必須大於 0"
        if self.inner_square_curve <= self.inner_square_side:
            return False, "內方形曲率必須大於內方形邊長"
        if self.radius <= self.inner_square_curve:
            return False, "圓柱半徑必須大於內方形曲率"
        if self.height <= 0:
            return False, "圓柱高度必須大於 0"
        if self.n_cells_square < 1:
            return False, "內方形網格數必須至少為 1"
        if self.n_cells_inner < 1:
            return False, "內方形到圓形網格數必須至少為 1"
        if self.n_cells_height < 1:
            return False, "高度方向網格數必須至少為 1"

        return True, ""

    @property
    def outlet_x(self) -> float:
        """計算出口 X 座標"""
        return self.base_x + self.height
