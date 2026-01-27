# -*- coding: utf-8 -*-
"""
Excel 資料讀取模組

讀取 Excel 流道數據並進行預處理
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, Optional
from scipy.interpolate import interp1d


class ExcelReader:
    """Excel 流道數據讀取器"""

    def __init__(self, file_path: str | Path):
        """
        初始化讀取器

        Args:
            file_path: Excel 檔案路徑
        """
        self.file_path = Path(file_path)
        self._data: Optional[np.ndarray] = None
        self._inner_points: Optional[np.ndarray] = None
        self._outer_points: Optional[np.ndarray] = None

    def read(self) -> np.ndarray:
        """
        讀取 Excel 數據

        Returns:
            點位座標陣列 (N x 3)

        Raises:
            FileNotFoundError: 檔案不存在
            ValueError: 資料格式錯誤
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"檔案不存在: {self.file_path}")

        # 讀取 Excel 資料（無標題行）
        df = pd.read_excel(
            self.file_path, header=None, names=["X", "Y", "Z"], engine="openpyxl"
        )

        # 確保至少有三列資料
        if df.shape[1] < 3:
            raise ValueError("Excel 檔案應至少包含三列資料 (X, Y, Z)")

        # 取前三列作為 X, Y, Z 座標
        self._data = df.iloc[:, 0:3].values.astype(float)

        # 按 Z 座標排序
        self._data = self._data[self._data[:, 2].argsort()]

        return self._data

    def separate_curves(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        分離內外曲線

        Returns:
            (inner_points, outer_points): 內外曲線點位
        """
        if self._data is None:
            self.read()

        # 計算平均 X 值，用於區分內外曲線
        avg_x = np.mean(self._data[:, 0])

        # 分離內外曲線
        self._inner_points = self._data[self._data[:, 0] < avg_x]
        self._outer_points = self._data[self._data[:, 0] >= avg_x]

        # 確保按 Z 座標排序
        self._inner_points = self._inner_points[self._inner_points[:, 2].argsort()]
        self._outer_points = self._outer_points[self._outer_points[:, 2].argsort()]

        return self._inner_points, self._outer_points

    def create_interpolation(self, points: np.ndarray) -> interp1d:
        """
        創建 Z 到 X 的插值函數

        Args:
            points: 點位座標陣列

        Returns:
            插值函數
        """
        z_coords = points[:, 2]
        x_coords = points[:, 0]

        return interp1d(
            z_coords,
            x_coords,
            kind="linear",
            bounds_error=False,
            fill_value="extrapolate",
        )

    def sample_layers(self, num_layers: int) -> Tuple[list, list]:
        """
        對內外曲線進行層採樣

        Args:
            num_layers: 採樣層數

        Returns:
            (inner_samples, outer_samples): 內外曲線採樣點
        """
        if self._inner_points is None or self._outer_points is None:
            self.separate_curves()

        # 找出 Z 座標範圍
        min_z = np.min(self._data[:, 2])
        max_z = np.max(self._data[:, 2])

        # 創建均勻分布的 Z 層
        z_layers = np.linspace(min_z, max_z, num_layers)

        # 創建插值函數
        inner_interp = self.create_interpolation(self._inner_points)
        outer_interp = self.create_interpolation(self._outer_points)

        # 對每一層進行採樣
        inner_samples = []
        outer_samples = []

        for z in z_layers:
            inner_x = float(inner_interp(z))
            outer_x = float(outer_interp(z))

            inner_samples.append([inner_x, 0.0, float(z)])
            outer_samples.append([outer_x, 0.0, float(z)])

        return inner_samples, outer_samples

    @property
    def data(self) -> Optional[np.ndarray]:
        """原始資料"""
        return self._data

    @property
    def inner_points(self) -> Optional[np.ndarray]:
        """內曲線點位"""
        return self._inner_points

    @property
    def outer_points(self) -> Optional[np.ndarray]:
        """外曲線點位"""
        return self._outer_points

    @property
    def z_range(self) -> Tuple[float, float]:
        """Z 座標範圍"""
        if self._data is None:
            raise ValueError("請先讀取資料")
        return float(np.min(self._data[:, 2])), float(np.max(self._data[:, 2]))
