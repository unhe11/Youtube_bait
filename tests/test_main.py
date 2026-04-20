import pytest
from unittest.mock import patch
from main import main

def test_main_function():
    # Мокаем sys.argv с корректными аргументами CLI
    with patch('sys.argv', ['main.py', '--files', 'test.csv', '--report', 'clickbait']):
        # Мокаем read_all_files, чтобы он возвращал пустой список без ошибок
        with patch('readers.read_all_files', return_value=[]):
            # Мокаем sys.exit, чтобы перехватить возможный выход
            with patch('sys.exit') as mock_exit:
                # Вызываем main() из main.py
                main()
                # Проверяем, что sys.exit был вызван с кодом 2 (из‑за ошибки файла)
                mock_exit.assert_called_with(2)
