# -*- coding: utf-8 -*-
"""
網格生成器模組

將 Excel 流道數據轉換為 OpenFOAM blockMeshDict 格式
"""

import math
from pathlib import Path
from typing import List, Tuple, Optional

from ..models.mesh_params import MeshParameters, BoundaryLayerParams


class MeshGenerator:
    """網格生成器"""

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

scale {scale};

// 流道參數，基於 Excel 數據
// The data is in mm, keep unit consistent

"""

    def __init__(
        self,
        mesh_params: MeshParameters,
        boundary_layer_params: Optional[BoundaryLayerParams] = None,
    ):
        """
        初始化網格生成器

        Args:
            mesh_params: 網格參數
            boundary_layer_params: 邊界層參數（可選）
        """
        self.mesh_params = mesh_params
        self.bl_params = boundary_layer_params or BoundaryLayerParams()

    def generate(
        self,
        inner_samples: List[List[float]],
        outer_samples: List[List[float]],
        output_file: str | Path,
    ) -> None:
        """
        生成 blockMeshDict 檔案

        Args:
            inner_samples: 內曲線採樣點 [[x, y, z], ...]
            outer_samples: 外曲線採樣點 [[x, y, z], ...]
            output_file: 輸出檔案路徑
        """
        if self.bl_params.enabled:
            inner_bl, outer_bl = self._calculate_boundary_layer_points(
                inner_samples, outer_samples
            )
            self._generate_with_boundary_layer(
                inner_samples, outer_samples, inner_bl, outer_bl, output_file
            )
        else:
            self._generate_standard(inner_samples, outer_samples, output_file)

    def _generate_standard(
        self,
        inner_samples: List[List[float]],
        outer_samples: List[List[float]],
        output_file: str | Path,
    ) -> None:
        """生成標準 blockMeshDict（無邊界層）"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            # 寫入檔案頭
            f.write(self.HEADER_TEMPLATE.format(scale=self.mesh_params.scale_factor))

            # 寫入頂點
            self._write_vertices(f, inner_samples, outer_samples)

            # 寫入單元塊
            self._write_blocks(f, len(inner_samples))

            # 寫入邊緣
            self._write_edges(f, inner_samples, outer_samples)

            # 寫入邊界
            self._write_boundaries(f, len(inner_samples))

            # 結束檔案
            f.write(");\n\nmergePatchPairs\n(\n);\n\n")
            f.write(
                "// ************************************************************************* //\n"
            )

    def _write_vertices(
        self, f, inner_samples: List[List[float]], outer_samples: List[List[float]]
    ) -> None:
        """寫入頂點定義"""
        f.write("vertices\n(\n")

        for i, (inner, outer) in enumerate(zip(inner_samples, outer_samples)):
            z = inner[2]
            inner_r = inner[0]
            outer_r = outer[0]

            # 內圈頂點（4個，90度間隔）
            f.write(f"    // 層 {i + 1} - 內圈頂點，z = {z:.3f}\n")
            f.write(f"    ({inner_r:.6f}  0.000000  {z:.6f})  // 頂點 {i * 8 + 0}\n")
            f.write(f"    (0.000000  {inner_r:.6f}  {z:.6f})  // 頂點 {i * 8 + 1}\n")
            f.write(f"    ({-inner_r:.6f}  0.000000  {z:.6f})  // 頂點 {i * 8 + 2}\n")
            f.write(f"    (0.000000  {-inner_r:.6f}  {z:.6f})  // 頂點 {i * 8 + 3}\n")

            # 外圈頂點（4個，90度間隔）
            f.write(f"    // 層 {i + 1} - 外圈頂點，z = {z:.3f}\n")
            f.write(f"    ({outer_r:.6f}  0.000000  {z:.6f})  // 頂點 {i * 8 + 4}\n")
            f.write(f"    (0.000000  {outer_r:.6f}  {z:.6f})  // 頂點 {i * 8 + 5}\n")
            f.write(f"    ({-outer_r:.6f}  0.000000  {z:.6f})  // 頂點 {i * 8 + 6}\n")
            f.write(f"    (0.000000  {-outer_r:.6f}  {z:.6f})  // 頂點 {i * 8 + 7}\n")

        f.write(");\n\n")

    def _write_blocks(self, f, num_layers: int) -> None:
        """寫入單元塊定義"""
        f.write("blocks\n(\n")

        n_radial = self.mesh_params.n_cells_radial
        n_circum_quad = self.mesh_params.n_cells_circum // 4
        n_axial = self.mesh_params.n_cells_axial

        for i in range(num_layers - 1):
            f.write(f"    // 連接層 {i + 1} 和層 {i + 2} 的塊\n")

            # 四個象限的 hex 塊
            for quad in range(4):
                v0 = i * 8 + quad
                v1 = i * 8 + (quad + 1) % 4
                v4 = i * 8 + 4 + quad
                v5 = i * 8 + 4 + (quad + 1) % 4
                v0n = (i + 1) * 8 + quad
                v1n = (i + 1) * 8 + (quad + 1) % 4
                v4n = (i + 1) * 8 + 4 + quad
                v5n = (i + 1) * 8 + 4 + (quad + 1) % 4

                f.write(f"    hex ({v0} {v4} {v5} {v1} {v0n} {v4n} {v5n} {v1n}) ")
                f.write(
                    f"({n_radial} {n_circum_quad} {n_axial}) simpleGrading (1 1 1)\n"
                )

        f.write(");\n\n")

    def _write_edges(
        self, f, inner_samples: List[List[float]], outer_samples: List[List[float]]
    ) -> None:
        """寫入邊緣定義（圓弧）"""
        f.write("edges\n(\n")

        sqrt_half = math.sqrt(0.5)

        for i, (inner, outer) in enumerate(zip(inner_samples, outer_samples)):
            z = inner[2]
            inner_r = inner[0]
            outer_r = outer[0]

            inner_diag = inner_r * sqrt_half
            outer_diag = outer_r * sqrt_half

            # 內圈弧
            f.write(f"    // 層 {i + 1} - 內圈弧，z = {z:.3f}\n")
            f.write(
                f"    arc {i * 8 + 0} {i * 8 + 1} ({inner_diag:.6f} {inner_diag:.6f} {z:.6f})\n"
            )
            f.write(
                f"    arc {i * 8 + 1} {i * 8 + 2} ({-inner_diag:.6f} {inner_diag:.6f} {z:.6f})\n"
            )
            f.write(
                f"    arc {i * 8 + 2} {i * 8 + 3} ({-inner_diag:.6f} {-inner_diag:.6f} {z:.6f})\n"
            )
            f.write(
                f"    arc {i * 8 + 3} {i * 8 + 0} ({inner_diag:.6f} {-inner_diag:.6f} {z:.6f})\n"
            )

            # 外圈弧
            f.write(f"    // 層 {i + 1} - 外圈弧，z = {z:.3f}\n")
            f.write(
                f"    arc {i * 8 + 4} {i * 8 + 5} ({outer_diag:.6f} {outer_diag:.6f} {z:.6f})\n"
            )
            f.write(
                f"    arc {i * 8 + 5} {i * 8 + 6} ({-outer_diag:.6f} {outer_diag:.6f} {z:.6f})\n"
            )
            f.write(
                f"    arc {i * 8 + 6} {i * 8 + 7} ({-outer_diag:.6f} {-outer_diag:.6f} {z:.6f})\n"
            )
            f.write(
                f"    arc {i * 8 + 7} {i * 8 + 4} ({outer_diag:.6f} {-outer_diag:.6f} {z:.6f})\n"
            )

        f.write(");\n\n")

    def _write_boundaries(self, f, num_layers: int) -> None:
        """寫入邊界定義"""
        f.write("boundary\n(\n")

        # 入口邊界
        f.write("    inlet\n    {\n        type patch;\n        faces\n        (\n")
        f.write("            // 底面（第一層）\n")
        for quad in range(4):
            v0 = quad
            v1 = (quad + 1) % 4
            v4 = 4 + quad
            v5 = 4 + (quad + 1) % 4
            f.write(f"            ({v0} {v4} {v5} {v1})\n")
        f.write("        );\n    }\n")

        # 出口邊界
        last = num_layers - 1
        f.write("    outlet\n    {\n        type patch;\n        faces\n        (\n")
        f.write("            // 頂面（最後一層）\n")
        for quad in range(4):
            v0 = last * 8 + quad
            v1 = last * 8 + (quad + 1) % 4
            v4 = last * 8 + 4 + quad
            v5 = last * 8 + 4 + (quad + 1) % 4
            f.write(f"            ({v0} {v1} {v5} {v4})\n")
        f.write("        );\n    }\n")

        # 內壁邊界
        f.write("    innerWall\n    {\n        type wall;\n        faces\n        (\n")
        for i in range(num_layers - 1):
            for quad in range(4):
                v0 = i * 8 + quad
                v1 = i * 8 + (quad + 1) % 4
                v0n = (i + 1) * 8 + quad
                v1n = (i + 1) * 8 + (quad + 1) % 4
                f.write(f"            ({v0} {v1} {v1n} {v0n})\n")
        f.write("        );\n    }\n")

        # 外壁邊界
        f.write("    outerWall\n    {\n        type wall;\n        faces\n        (\n")
        for i in range(num_layers - 1):
            for quad in range(4):
                v4 = i * 8 + 4 + quad
                v5 = i * 8 + 4 + (quad + 1) % 4
                v4n = (i + 1) * 8 + 4 + quad
                v5n = (i + 1) * 8 + 4 + (quad + 1) % 4
                f.write(f"            ({v4} {v4n} {v5n} {v5})\n")
        f.write("        );\n    }\n")

    def _calculate_layer_ratios(
        self, num_layers: int, expansion_ratio: float
    ) -> List[float]:
        """計算邊界層各層的累積比例"""
        if num_layers == 1:
            return [1.0]

        layer_thicknesses = [1.0]
        for i in range(1, num_layers):
            layer_thicknesses.append(layer_thicknesses[-1] * expansion_ratio)

        total = sum(layer_thicknesses)

        cumulative = 0.0
        ratios = []
        for t in layer_thicknesses:
            cumulative += t
            ratios.append(cumulative / total)

        return ratios

    def _calculate_boundary_layer_points(
        self, inner_samples: List[List[float]], outer_samples: List[List[float]]
    ) -> Tuple[List[List[List[float]]], List[List[List[float]]]]:
        """計算邊界層點位"""
        inner_bl_samples = []
        outer_bl_samples = []

        inner_ratios = self._calculate_layer_ratios(
            self.bl_params.inner_layers, self.bl_params.expansion_ratio
        )
        outer_ratios = self._calculate_layer_ratios(
            self.bl_params.outer_layers, self.bl_params.expansion_ratio
        )

        for inner_pt, outer_pt in zip(inner_samples, outer_samples):
            inner_x, _, z = inner_pt
            outer_x = outer_pt[0]

            radial_distance = outer_x - inner_x
            inner_bl_thickness = radial_distance * self.bl_params.inner_thickness
            outer_bl_thickness = radial_distance * self.bl_params.outer_thickness

            # 內壁邊界層點位
            inner_layer_pts = [[inner_x, 0.0, z]]
            for ratio in inner_ratios:
                x = inner_x + ratio * inner_bl_thickness
                inner_layer_pts.append([x, 0.0, z])
            inner_bl_samples.append(inner_layer_pts)

            # 外壁邊界層點位
            outer_layer_pts = [[outer_x, 0.0, z]]
            for ratio in outer_ratios:
                x = outer_x - ratio * outer_bl_thickness
                outer_layer_pts.append([x, 0.0, z])
            outer_bl_samples.append(outer_layer_pts)

        return inner_bl_samples, outer_bl_samples

    def _generate_with_boundary_layer(
        self,
        inner_samples: List[List[float]],
        outer_samples: List[List[float]],
        inner_bl_samples: List[List[List[float]]],
        outer_bl_samples: List[List[List[float]]],
        output_file: str | Path,
    ) -> None:
        """生成包含邊界層的 blockMeshDict"""
        # 暫時使用標準生成（完整邊界層實作較複雜）
        # TODO: 完整實作邊界層網格生成
        self._generate_standard(inner_samples, outer_samples, output_file)
