# BlockMesh Studio

[![CI](https://github.com/LostSunset/blockmesh-studio/actions/workflows/ci.yml/badge.svg)](https://github.com/LostSunset/blockmesh-studio/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/LostSunset/blockmesh-studio.svg)](https://github.com/LostSunset/blockmesh-studio/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/LostSunset/blockmesh-studio.svg)](https://github.com/LostSunset/blockmesh-studio/network)
[![GitHub issues](https://img.shields.io/github/issues/LostSunset/blockmesh-studio.svg)](https://github.com/LostSunset/blockmesh-studio/issues)

**OpenFOAM blockMeshDict mesh generation tool**

Built with **PySide6** and **MUJI-style** minimalist design

[English](#english) | [正體中文](#正體中文)

---

## English

### ✨ Features

- 📊 **Excel Converter**: Convert 2D flow channel data to 3D cylindrical mesh
- 🔵 **Cylinder Mesh**: Parametric cylindrical mesh generation
- 🎛️ **Boundary Layer Control**: Inner/outer wall boundary layer mesh settings

### 📋 Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

### 🚀 Quick Start

#### 1. Setup Environment

```bash
# Create virtual environment
uv venv .venv --python 3.10

# Activate
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# Install dependencies
uv pip install PySide6 pandas numpy scipy openpyxl
```

#### 2. Launch Application

```bash
python -m src.main
```

### 📁 Project Structure

```
src/
├── main.py              # Entry point
├── core/                # Core logic
│   ├── mesh_generator.py
│   ├── cylinder_mesh.py
│   └── excel_reader.py
├── models/              # Data models
│   └── mesh_params.py
└── ui/                  # User interface
    ├── main_window.py
    ├── widgets/
    └── resources/
        └── muji_style.qss
```

### 📖 Usage

#### Excel Converter
1. Select Excel file with X, Y, Z coordinates
2. Set mesh parameters (layers, radial/circumferential/axial cells)
3. Optional: Enable boundary layer control
4. Click "Generate" to create blockMeshDict

#### Cylinder Mesh
1. Set geometry parameters (radius, height, inner square side)
2. Set mesh parameters
3. Click "Generate" to create blockMeshDict

---

## 正體中文

### ✨ 功能

- 📊 **Excel 轉換**：將 2D 流道數據轉換為 3D 圓柱網格
- 🔵 **圓柱網格**：參數化圓柱形網格生成
- 🎛️ **邊界層控制**：內外壁邊界層網格設定

### 📋 系統需求

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) 套件管理器（推薦）

### 🚀 快速開始

#### 1. 建立環境

```bash
# 建立虛擬環境
uv venv .venv --python 3.10

# 啟動環境
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# 安裝依賴
uv pip install PySide6 pandas numpy scipy openpyxl
```

#### 2. 啟動應用程式

```bash
python -m src.main
```

### 📖 使用說明

#### Excel 轉換
1. 選擇包含 X, Y, Z 座標的 Excel 檔案
2. 設定網格參數（層數、徑向/圓周/軸向網格數）
3. 可選：啟用邊界層控制
4. 點擊「生成」產生 blockMeshDict

#### 圓柱網格
1. 設定幾何參數（半徑、高度、內方形邊長）
2. 設定網格參數
3. 點擊「生成」產生 blockMeshDict

---

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=LostSunset/blockmesh-studio&type=Date)](https://star-history.com/#LostSunset/blockmesh-studio&Date)

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

[MIT License](LICENSE)
