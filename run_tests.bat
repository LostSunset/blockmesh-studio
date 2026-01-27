@echo off
chcp 65001 >nul
REM BlockMesh Studio 測試執行腳本
REM 確保 UTF-8 編碼支援正體中文

echo ============================================
echo    BlockMesh Studio 測試執行器
echo ============================================

REM 設定 UTF-8 環境變數（Python 3.14 已內建 UTF-8 模式）
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=0

REM 啟動虛擬環境並執行測試
echo.
echo 正在執行測試...
echo.

uv run pytest -v --tb=short %*

echo.
echo ============================================
echo    測試執行完成
echo ============================================
