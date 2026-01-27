# BlockMesh Studio 開發指南

本文件說明專案的開發流程、自動化工具和發布流程。

## 🛠️ 開發環境

### 套件管理
使用 **uv** 管理套件：
```bash
# 安裝依賴
uv pip install PySide6 pandas numpy scipy openpyxl

# 開發依賴
uv pip install ruff pytest pytest-cov
```

### 程式碼品質

使用 **ruff** 進行 lint 和格式化：
```bash
# 檢查並自動修復
ruff check src/ --fix

# 格式化
ruff format src/
```

## 🚀 發布流程

### 自動化發布 (推薦)

使用 `/release` workflow：
```
/release v0.2.1
```

此 workflow 會自動：
1. 執行 lint 檢查
2. 執行測試
3. 提交變更
4. 標記版本
5. 推送到 GitHub

### 手動發布

```bash
# 1. 確保程式碼品質
ruff check src/ --fix
ruff format src/
pytest tests/ -v

# 2. 更新版本號
# 編輯 pyproject.toml 和 src/__init__.py

# 3. 提交並標記
git add -A
git commit -m "chore: release v0.2.1"
git tag -a v0.2.1 -m "Release v0.2.1"

# 4. 推送
git push origin main
git push origin --tags
```

## 📁 專案結構

```
blockmesh-studio/
├── src/
│   ├── main.py          # 應用程式入口
│   ├── core/            # 核心邏輯
│   ├── models/          # 資料模型
│   └── ui/              # PySide6 介面
├── tests/               # 測試
├── .agent/workflows/    # Agent workflows
│   └── release.md       # 發布 workflow
└── CLAUDE.md            # 本文件
```

## 🔧 常用指令

| 指令 | 說明 |
|------|------|
| `python -m src.main` | 啟動應用程式 |
| `pytest tests/ -v` | 執行測試 |
| `ruff check src/ --fix` | Lint 並自動修復 |
| `ruff format src/` | 格式化程式碼 |

## 🧪 測試

使用 **send_command_input** 方式執行測試（已記憶）。
