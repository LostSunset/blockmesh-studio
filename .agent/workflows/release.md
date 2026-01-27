---
description: Automated release workflow - run tests, update README, tag version, push to GitHub
---
# Release Workflow

// turbo-all

自動化發布流程，執行測試、更新 README、標記版本並推送到 GitHub。

## 使用方式

執行此 workflow 前請提供版本號，例如：`/release v0.2.1`

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
編輯 `pyproject.toml` 和 `src/__init__.py` 中的版本號

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

## 注意事項

- 確保所有測試通過後再發布
- 版本號格式遵循 Semantic Versioning (vX.Y.Z)
- 發布前確認 README 已更新
