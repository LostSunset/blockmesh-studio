---
description: Automated release workflow - run tests, update README, tag version, push to GitHub
---
# Release Workflow

// turbo-all

自動化發布流程，執行測試、更新版本號、標記並推送到 GitHub。

## 使用方式

執行此 workflow：`/release v0.2.2`

## 步驟

### 1. 啟動環境
```bash
cd d:\SynologyDrive\Learning\CAD_Mesh_tool\00_blockmesh-studio
.venv314\Scripts\activate
```

### 2. 執行 lint 檢查並自動修復
```bash
ruff check src/ --fix
ruff format src/
```

### 3. 執行測試
```bash
python -m pytest tests/ -v
```

### 4. 更新版本號
更新以下兩個檔案中的版本號：
- `pyproject.toml` 中的 `version = "X.Y.Z"`
- `src/__init__.py` 中的 `__version__ = "X.Y.Z"`

### 5. 提交變更
```bash
git add -A
git commit -m "chore: release <VERSION>"
```

### 6. 標記版本
```bash
git tag -a <VERSION> -m "Release <VERSION>"
```

### 7. 推送到 GitHub
```bash
git push origin main
git push origin --tags
```

## 版本規則

遵循 Semantic Versioning：
- **MAJOR** (X.0.0)：重大功能變更、不相容 API 變更
- **MINOR** (0.X.0)：新增功能、向下相容
- **PATCH** (0.0.X)：bug 修復、小幅改進

每次推送更新都需要增加版本號：
- bug 修復：增加 PATCH
- 新功能：增加 MINOR
- 重大變更：增加 MAJOR
