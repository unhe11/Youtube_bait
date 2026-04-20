import pytest
from unittest.mock import patch
from io import StringIO
from pathlib import Path
from models import Video
from readers import read_csv_file, read_all_files


def test_read_csv_file_single_video():
    # Создаём CSV в памяти
    csv_data = '''title,ctr,retention_rate
Video 1,18.2,35'''
    file_obj = StringIO(csv_data)

    # Мокаем открытие файла
    with patch('builtins.open', return_value=file_obj):
        videos = read_csv_file(Path('dummy.csv'))

    assert len(videos) == 1
    assert videos[0].title == 'Video 1'
    assert videos[0].ctr == 18.2
    assert videos[0].retention_rate == 35

def test_read_csv_file_multiple_videos():
    csv_data = '''title,ctr,retention_rate
Video 1,18.2,35
Video 2,22.5,28
Video 3,9.5,82'''
    file_obj = StringIO(csv_data)

    with patch('builtins.open', return_value=file_obj):
        videos = read_csv_file(Path('dummy.csv'))

    assert len(videos) == 3
    assert videos[1].ctr == 22.5

def test_read_csv_file_invalid_data():
    csv_data = '''title,ctr,retention_rate
Video 1,invalid,35'''
    file_obj = StringIO(csv_data)

    with patch('builtins.open', return_value=file_obj):
        videos = read_csv_file(Path('invalid.csv'))

    assert len(videos) == 0  # Строка с ошибкой пропускается



def test_read_all_files():
    # Мокаем функцию read_csv_file
    with patch('readers.read_csv_file') as mock_read:
        # Настраиваем моки для двух файлов
        mock_read.side_effect = [
            [Video("File1 Video", 20.0, 30.0)],
            [Video("File2 Video", 25.0, 25.0)]
        ]

        # Вызываем функцию с фиктивными путями
        result = read_all_files(['file1.csv', 'file2.csv'])

    # Проверяем результат
    assert len(result) == 2
    assert result[0].title == "File1 Video"
    assert result[1].title == "File2 Video"



