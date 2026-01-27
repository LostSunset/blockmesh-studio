# -*- coding: utf-8 -*-
"""
UTF-8 中文支援測試
驗證正體中文在 pytest 中能正確顯示
"""
import os
import sys


class TestUTF8Support:
    """測試 UTF-8 編碼支援"""

    def test_chinese_string_display(self):
        """測試正體中文字串能正確顯示"""
        message = "這是一段正體中文測試訊息"
        assert "正體中文" in message
        print(f"\n✅ 中文輸出測試: {message}")

    def test_chinese_assertion_message(self):
        """測試 assertion 錯誤訊息能正確顯示中文"""
        expected = "預期值"
        actual = "預期值"
        assert expected == actual, f"錯誤：預期 '{expected}'，但得到 '{actual}'"

    def test_utf8_mode_enabled(self):
        """測試 Python 已使用 UTF-8 模式"""
        # Python 3.14+ 預設已啟用 UTF-8 模式
        # 驗證標準輸出編碼為 UTF-8
        stdout_encoding = sys.stdout.encoding
        assert 'utf' in stdout_encoding.lower(), f"stdout 編碼應為 UTF-8，但得到 '{stdout_encoding}'"
        
        # 驗證預設檔案系統編碼為 UTF-8
        fs_encoding = sys.getfilesystemencoding()
        assert 'utf' in fs_encoding.lower(), f"檔案系統編碼應為 UTF-8，但得到 '{fs_encoding}'"

    def test_file_encoding_read(self, tmp_path):
        """測試讀取含中文的檔案"""
        test_content = "測試內容：正體中文\n第二行：繁體字"
        test_file = tmp_path / "test_chinese.txt"
        
        # 寫入檔案（明確指定 UTF-8）
        test_file.write_text(test_content, encoding="utf-8")
        
        # 讀取檔案（明確指定 UTF-8）
        read_content = test_file.read_text(encoding="utf-8")
        
        assert read_content == test_content, "檔案內容應相符"
        print(f"\n✅ 讀取的中文內容: {read_content}")

    def test_chinese_diff_output(self):
        """測試中文差異輸出（用於驗證 pytest 差異顯示）"""
        list1 = ["項目一", "項目二", "項目三"]
        list2 = ["項目一", "項目二", "項目三"]
        assert list1 == list2, "清單內容應相符"
