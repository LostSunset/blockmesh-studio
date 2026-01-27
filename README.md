# BlockMesh Studio

[![CI](https://github.com/LostSunset/blockmesh-studio/actions/workflows/ci.yml/badge.svg)](https://github.com/LostSunset/blockmesh-studio/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/LostSunset/blockmesh-studio.svg)](https://github.com/LostSunset/blockmesh-studio/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/LostSunset/blockmesh-studio.svg)](https://github.com/LostSunset/blockmesh-studio/network)
[![GitHub issues](https://img.shields.io/github/issues/LostSunset/blockmesh-studio.svg)](https://github.com/LostSunset/blockmesh-studio/issues)

OpenFOAM blockMeshDict 網格生成工具

採用 **PySide6** 開發，**無印良品風格**設計

## ✨ 功能

- 📊 **Excel 轉換**：將 2D 流道數據轉換為 3D 圓柱網格
- 🔵 **圓柱網格**：參數化圓柱形網格生成
- 🎛️ **邊界層控制**：內外壁邊界層網格設定

## 📋 系統需求

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) 套件管理器（推薦）

## 🚀 快速開始

### 1. 建立環境

```bash
# 建立虛擬環境
uv venv .venv --python 3.10

# 啟動環境
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# 安裝依賴
uv pip install PySide6 pandas numpy scipy openpyxl
```

### 2. 啟動應用程式

```bash
python -m src.main
```

## 📁 專案結構

```
src/
├── main.py              # 入口點
├── core/                # 核心邏輯
│   ├── mesh_generator.py
│   ├── cylinder_mesh.py
│   └── excel_reader.py
├── models/              # 資料模型
│   └── mesh_params.py
└── ui/                  # 使用者介面
    ├── main_window.py
    ├── widgets/
    └── resources/
        └── muji_style.qss
```

## 📖 使用說明

### Excel 轉換

1. 選擇包含 X, Y, Z 座標的 Excel 檔案
2. 設定網格參數（層數、徑向/圓周/軸向網格數）
3. 可選：啟用邊界層控制
4. 點擊「生成」產生 blockMeshDict

### 圓柱網格

1. 設定幾何參數（半徑、高度、內方形邊長）
2. 設定網格參數
3. 點擊「生成」產生 blockMeshDict

## 🌐 正體中文支援

- 所有檔案使用 UTF-8 編碼
- 完整支援正體中文介面

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=LostSunset/blockmesh-studio&type=Date)](https://star-history.com/#LostSunset/blockmesh-studio&Date)

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 授權

[MIT License](LICENSE)
