#!/bin/bash
# BlockMesh Studio 測試執行腳本
# 確保 UTF-8 編碼支援正體中文

echo "============================================"
echo "   BlockMesh Studio 測試執行器"
echo "============================================"

# 設定 UTF-8 環境變數（Python 3.14 已內建 UTF-8 模式）
export PYTHONIOENCODING=utf-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

echo ""
echo "正在執行測試..."
echo ""

uv run pytest -v --tb=short "$@"

echo ""
echo "============================================"
echo "   測試執行完成"
echo "============================================"
