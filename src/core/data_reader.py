# -*- coding: utf-8 -*-
"""
資料讀取模組

支援多種格式的流道點位資料讀取：
- Excel (.xlsx, .xls)
- CSV (.csv)
- TXT (.txt) - 空格/Tab 分隔
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple, Optional
from dataclasses import dataclass

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy.interpolate import interp1d


@dataclass
class DataStatistics:
    """資料統計資訊"""

    total_points: int
    inner_points: int
    outer_points: int
    x_range: Tuple[float, float]
    y_range: Tuple[float, float]
    z_range: Tuple[float, float]
    avg_x: float

    def to_dict(self) -> dict:
        """轉換為字典"""
        return {
            "total_points": self.total_points,
            "inner_points": self.inner_points,
            "outer_points": self.outer_points,
            "x_range": self.x_range,
            "y_range": self.y_range,
            "z_range": self.z_range,
            "avg_x": self.avg_x,
        }


class DataReader:
    """
    通用資料讀取器

    支援格式：
    - Excel (.xlsx, .xls)
    - CSV (.csv)
    - TXT (.txt) - 空格或 Tab 分隔

    資料格式要求：
    - 三欄資料：X, Y, Z 座標
    - 無標題行（或自動偵測）
    """

    SUPPORTED_EXTENSIONS = {".xlsx", ".xls", ".csv", ".txt"}

    def __init__(self, file_path: str):
        """
        初始化資料讀取器

        Args:
            file_path: 資料檔案路徑
        """
        self.file_path = Path(file_path)
        self._points: Optional[NDArray] = None
        self._inner_points: Optional[NDArray] = None
        self._outer_points: Optional[NDArray] = None
        self._statistics: Optional[DataStatistics] = None
        self._inner_interp: Optional[Tuple] = None
        self._outer_interp: Optional[Tuple] = None

    @classmethod
    def get_file_filter(cls) -> str:
        """取得檔案對話框的過濾器字串"""
        return (
            "All Supported Files (*.xlsx *.xls *.csv *.txt);;"
            "Excel Files (*.xlsx *.xls);;"
            "CSV Files (*.csv);;"
            "Text Files (*.txt);;"
            "All Files (*.*)"
        )

    @classmethod
    def is_supported(cls, file_path: str) -> bool:
        """檢查檔案格式是否支援"""
        ext = Path(file_path).suffix.lower()
        return ext in cls.SUPPORTED_EXTENSIONS

    def read(self) -> NDArray:
        """
        讀取資料檔案

        Returns:
            NDArray: 形狀為 (N, 3) 的座標陣列
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"檔案不存在: {self.file_path}")

        ext = self.file_path.suffix.lower()

        if ext in (".xlsx", ".xls"):
            self._points = self._read_excel()
        elif ext == ".csv":
            self._points = self._read_csv()
        elif ext == ".txt":
            self._points = self._read_txt()
        else:
            raise ValueError(f"不支援的檔案格式: {ext}")

        self._process_points()
        return self._points

    def _read_excel(self) -> NDArray:
        """讀取 Excel 檔案"""
        df = pd.read_excel(self.file_path, header=None)
        return self._extract_coordinates(df)

    def _read_csv(self) -> NDArray:
        """讀取 CSV 檔案"""
        # 嘗試自動偵測分隔符
        df = pd.read_csv(self.file_path, header=None, sep=None, engine="python")
        return self._extract_coordinates(df)

    def _read_txt(self) -> NDArray:
        """讀取 TXT 檔案（空格/Tab 分隔）"""
        df = pd.read_csv(self.file_path, header=None, sep=r"\s+", engine="python")
        return self._extract_coordinates(df)

    def _extract_coordinates(self, df: pd.DataFrame) -> NDArray:
        """從 DataFrame 中提取座標"""
        # 檢查是否有標題行（第一行是否為數值）
        first_row = df.iloc[0]
        try:
            # 嘗試轉換第一行為數值
            pd.to_numeric(first_row)
        except (ValueError, TypeError):
            # 第一行不是數值，視為標題行
            df = df.iloc[1:]

        if df.shape[1] < 3:
            raise ValueError(f"資料需要至少 3 欄 (X, Y, Z)，目前只有 {df.shape[1]} 欄")

        # 取前三欄作為 X, Y, Z
        points = df.iloc[:, :3].astype(float).values
        return points

    def _process_points(self) -> None:
        """處理點位資料：排序並分離內外曲線"""
        if self._points is None:
            return

        # 按 Z 座標排序
        sorted_indices = self._points[:, 2].argsort()
        self._points = self._points[sorted_indices]

        # 計算平均 X 值用於分離內外曲線
        avg_x = np.mean(self._points[:, 0])

        # 分離內外曲線
        self._inner_points = self._points[self._points[:, 0] < avg_x]
        self._outer_points = self._points[self._points[:, 0] >= avg_x]

        # 確保按 Z 排序
        self._inner_points = self._inner_points[self._inner_points[:, 2].argsort()]
        self._outer_points = self._outer_points[self._outer_points[:, 2].argsort()]

        # 計算統計資訊
        self._statistics = DataStatistics(
            total_points=len(self._points),
            inner_points=len(self._inner_points),
            outer_points=len(self._outer_points),
            x_range=(float(self._points[:, 0].min()), float(self._points[:, 0].max())),
            y_range=(float(self._points[:, 1].min()), float(self._points[:, 1].max())),
            z_range=(float(self._points[:, 2].min()), float(self._points[:, 2].max())),
            avg_x=float(avg_x),
        )

        # 建立插值函數
        self._create_interpolators()

    def _create_interpolators(self) -> None:
        """建立插值函數"""
        if self._inner_points is None or self._outer_points is None:
            return

        # 內曲線插值
        z_inner = self._inner_points[:, 2]
        self._inner_interp = (
            interp1d(
                z_inner,
                self._inner_points[:, 0],
                kind="linear",
                fill_value="extrapolate",
            ),
            interp1d(
                z_inner,
                self._inner_points[:, 1],
                kind="linear",
                fill_value="extrapolate",
            ),
        )

        # 外曲線插值
        z_outer = self._outer_points[:, 2]
        self._outer_interp = (
            interp1d(
                z_outer,
                self._outer_points[:, 0],
                kind="linear",
                fill_value="extrapolate",
            ),
            interp1d(
                z_outer,
                self._outer_points[:, 1],
                kind="linear",
                fill_value="extrapolate",
            ),
        )

    @property
    def statistics(self) -> Optional[DataStatistics]:
        """取得資料統計資訊"""
        return self._statistics

    @property
    def inner_points(self) -> Optional[NDArray]:
        """取得內曲線點位"""
        return self._inner_points

    @property
    def outer_points(self) -> Optional[NDArray]:
        """取得外曲線點位"""
        return self._outer_points

    def sample_layers(self, num_layers: int) -> Tuple[NDArray, NDArray]:
        """
        在指定層數上取樣內外曲線

        Args:
            num_layers: 取樣層數

        Returns:
            Tuple[NDArray, NDArray]: (內曲線取樣, 外曲線取樣)
        """
        if self._inner_interp is None or self._outer_interp is None:
            raise RuntimeError("請先呼叫 read() 讀取資料")

        # 決定 Z 範圍
        z_min = max(self._inner_points[:, 2].min(), self._outer_points[:, 2].min())
        z_max = min(self._inner_points[:, 2].max(), self._outer_points[:, 2].max())

        # 均勻取樣
        z_samples = np.linspace(z_min, z_max, num_layers)

        # 內曲線取樣
        inner_samples = np.column_stack(
            [
                self._inner_interp[0](z_samples),
                self._inner_interp[1](z_samples),
                z_samples,
            ]
        )

        # 外曲線取樣
        outer_samples = np.column_stack(
            [
                self._outer_interp[0](z_samples),
                self._outer_interp[1](z_samples),
                z_samples,
            ]
        )

        return inner_samples, outer_samples


# 保持向後相容
ExcelReader = DataReader
