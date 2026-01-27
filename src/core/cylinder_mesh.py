# -*- coding: utf-8 -*-
"""
圓柱網格生成器模組

將 M4 模板功能完全轉換為 Python 實作
生成以 X 軸為高度方向的圓柱形 blockMeshDict
"""

import math
from pathlib import Path
from typing import Tuple

from ..models.mesh_params import CylinderMeshParams


class CylinderMeshGenerator:
    """圓柱網格生成器"""

    # OpenFOAM blockMeshDict 檔案頭模板
    HEADER_TEMPLATE = """/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  v2212                                 |
|   \\\\  /    A nd           | Website:  www.openfoam.com                      |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
// 圓柱網格 - X 軸為高度方向，Y-Z 平面為圓形截面

scale   1.0;

"""

    def __init__(self, params: CylinderMeshParams):
        """
        初始化生成器

        Args:
            params: 圓柱網格參數
        """
        self.params = params

        # 預計算角度值（度）
        self._angles = [-45, -135, 135, 45]  # 四個角點
        self._edge_angles = [0, -90, 180, 90]  # 邊中點

    def generate(self, output_file: str | Path) -> str:
        """
        生成 blockMeshDict 檔案

        Args:
            output_file: 輸出檔案路徑

        Returns:
            生成的 blockMeshDict 內容
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        content = self._build_content()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return content

    def _build_content(self) -> str:
        """構建完整的 blockMeshDict 內容"""
        lines = [self.HEADER_TEMPLATE]

        # 頂點
        lines.append(self._build_vertices())

        # 塊
        lines.append(self._build_blocks())

        # 邊緣
        lines.append(self._build_edges())

        # 邊界
        lines.append(self._build_patches())

        # 結尾
        lines.append("mergePatchPairs\n(\n);\n")
        lines.append(
            "\n// ************************************************************************* //\n"
        )

        return "".join(lines)

    def _calc_vertex(
        self, is_outer: bool, angle_idx: int, x_pos: float
    ) -> Tuple[float, float, float]:
        """
        計算頂點座標

        Args:
            is_outer: 是否為外圈（圓形）頂點
            angle_idx: 角度索引 (0-3)
            x_pos: X 座標（高度位置）

        Returns:
            (x, y, z) 座標
        """
        p = self.params
        angle_deg = self._angles[angle_idx]
        angle_rad = math.radians(angle_deg)

        if is_outer:
            # 外圈（圓形）頂點
            y = p.radius * math.cos(angle_rad)
            z = p.radius * math.sin(angle_rad)
        else:
            # 內方形頂點
            s = p.inner_square_side
            # 根據象限決定座標
            if angle_idx == 0:  # -45°
                y, z = s, -s
            elif angle_idx == 1:  # -135°
                y, z = -s, -s
            elif angle_idx == 2:  # 135°
                y, z = -s, s
            else:  # 45°
                y, z = s, s

        return (x_pos, y, z)

    def _calc_edge_point(
        self, is_outer: bool, edge_idx: int, x_pos: float
    ) -> Tuple[float, float, float]:
        """
        計算邊緣中點座標（用於弧線）

        Args:
            is_outer: 是否為外圈
            edge_idx: 邊緣索引 (0-3)
            x_pos: X 座標

        Returns:
            (x, y, z) 座標
        """
        p = self.params
        angle_deg = self._edge_angles[edge_idx]
        angle_rad = math.radians(angle_deg)

        if is_outer:
            y = p.radius * math.cos(angle_rad)
            z = p.radius * math.sin(angle_rad)
        else:
            sc = p.inner_square_curve
            y = sc * math.cos(angle_rad)
            z = sc * math.sin(angle_rad)

        return (x_pos, y, z)

    def _build_vertices(self) -> str:
        """構建頂點定義"""
        p = self.params
        lines = ["vertices\n(\n"]

        # 底面頂點 (b = bottom, x = base_x)
        lines.append("    // 底面頂點 (x = base_x)\n")

        # 內方形頂點 s0b-s3b
        for i in range(4):
            x, y, z = self._calc_vertex(False, i, p.base_x)
            lines.append(f"    ({x:.6f} {y:.6f} {z:.6f})  // s{i}b = {i}\n")

        # 外圈頂點 r0b-r3b
        for i in range(4):
            x, y, z = self._calc_vertex(True, i, p.base_x)
            lines.append(f"    ({x:.6f} {y:.6f} {z:.6f})  // r{i}b = {i + 4}\n")

        # 頂面頂點 (t = top, x = outlet_x)
        lines.append("\n    // 頂面頂點 (x = outlet_x)\n")

        # 內方形頂點 s0t-s3t
        for i in range(4):
            x, y, z = self._calc_vertex(False, i, p.outlet_x)
            lines.append(f"    ({x:.6f} {y:.6f} {z:.6f})  // s{i}t = {i + 8}\n")

        # 外圈頂點 r0t-r3t
        for i in range(4):
            x, y, z = self._calc_vertex(True, i, p.outlet_x)
            lines.append(f"    ({x:.6f} {y:.6f} {z:.6f})  // r{i}t = {i + 12}\n")

        lines.append(");\n\n")
        return "".join(lines)

    def _build_blocks(self) -> str:
        """構建塊定義"""
        p = self.params
        ns = p.n_cells_square
        ni = p.n_cells_inner
        nh = p.n_cells_height

        lines = ["blocks\n(\n"]

        # 中心方形塊 (block0)
        lines.append("    // block0: 中心方形\n")
        lines.append(
            f"    hex (1 0 3 2 9 8 11 10) square ({ns} {ns} {nh}) simpleGrading (1 1 1)\n"
        )

        # 四個扇形塊 (block1-4)
        # block1: s0-r0-r3-s3
        lines.append("\n    // block1-4: 內圓環四個扇形\n")
        lines.append(
            f"    hex (0 4 7 3 8 12 15 11) innerCircle ({ni} {ns} {nh}) simpleGrading (1 1 1)\n"
        )
        lines.append(
            f"    hex (3 7 6 2 11 15 14 10) innerCircle ({ni} {ns} {nh}) simpleGrading (1 1 1)\n"
        )
        lines.append(
            f"    hex (2 6 5 1 10 14 13 9) innerCircle ({ni} {ns} {nh}) simpleGrading (1 1 1)\n"
        )
        lines.append(
            f"    hex (1 5 4 0 9 13 12 8) innerCircle ({ni} {ns} {nh}) simpleGrading (1 1 1)\n"
        )

        lines.append(");\n\n")
        return "".join(lines)

    def _build_edges(self) -> str:
        """構建邊緣定義（圓弧）"""
        p = self.params
        lines = ["edges\n(\n"]

        # 底面圓弧
        lines.append("    // 底面外圈弧\n")
        for i in range(4):
            v1 = 4 + (i + 1) % 4
            v2 = 4 + i
            x, y, z = self._calc_edge_point(True, i, p.base_x)
            lines.append(f"    arc {v1} {v2} ({x:.6f} {y:.6f} {z:.6f})\n")

        # 頂面圓弧
        lines.append("\n    // 頂面外圈弧\n")
        for i in range(4):
            v1 = 12 + (i + 1) % 4
            v2 = 12 + i
            x, y, z = self._calc_edge_point(True, i, p.outlet_x)
            lines.append(f"    arc {v1} {v2} ({x:.6f} {y:.6f} {z:.6f})\n")

        # 底面內方形弧（輕微彎曲）
        lines.append("\n    // 底面內方形弧\n")
        for i in range(4):
            v1 = (i + 1) % 4
            v2 = i
            x, y, z = self._calc_edge_point(False, i, p.base_x)
            lines.append(f"    arc {v1} {v2} ({x:.6f} {y:.6f} {z:.6f})\n")

        # 頂面內方形弧
        lines.append("\n    // 頂面內方形弧\n")
        for i in range(4):
            v1 = 8 + (i + 1) % 4
            v2 = 8 + i
            x, y, z = self._calc_edge_point(False, i, p.outlet_x)
            lines.append(f"    arc {v1} {v2} ({x:.6f} {y:.6f} {z:.6f})\n")

        lines.append(");\n\n")
        return "".join(lines)

    def _build_patches(self) -> str:
        """構建邊界 patch 定義"""
        lines = ["boundary\n(\n"]

        # 外壁 (Enclosure)
        lines.append(
            "    Enclosure\n    {\n        type patch;\n        faces\n        (\n"
        )
        for i in range(4):
            v1 = 4 + i
            v2 = 4 + (i + 1) % 4
            v3 = 12 + (i + 1) % 4
            v4 = 12 + i
            lines.append(f"            ({v1} {v2} {v3} {v4})\n")
        lines.append("        );\n    }\n\n")

        # 入口 (inlet) - 底面
        lines.append(
            "    inlet\n    {\n        type patch;\n        faces\n        (\n"
        )
        # 中心方形
        lines.append("            (0 1 2 3)\n")
        # 四個扇形
        lines.append("            (0 3 7 4)\n")
        lines.append("            (3 2 6 7)\n")
        lines.append("            (2 1 5 6)\n")
        lines.append("            (1 0 4 5)\n")
        lines.append("        );\n    }\n\n")

        # 出口 (outlet) - 頂面
        lines.append(
            "    outlet\n    {\n        type patch;\n        faces\n        (\n"
        )
        # 中心方形
        lines.append("            (8 11 10 9)\n")
        # 四個扇形
        lines.append("            (8 12 15 11)\n")
        lines.append("            (11 15 14 10)\n")
        lines.append("            (10 14 13 9)\n")
        lines.append("            (9 13 12 8)\n")
        lines.append("        );\n    }\n")

        lines.append(");\n\n")
        return "".join(lines)
