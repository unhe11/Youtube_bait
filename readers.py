import csv
from pathlib import Path
from models import Video

def read_csv_file(filepath: Path) -> list[Video]:
    videos = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    title = row['title']
                    ctr = float(row['ctr'])
                    retention_rate = float(row['retention_rate'])
                    videos.append(Video(title, ctr, retention_rate))
                except (ValueError, KeyError):
                    # Пропускаем строки с некорректными данными
                    continue
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    return videos


def read_all_files(filepaths: list[Path]) -> list[Video]:
    all_videos = []
    for filepath in filepaths:
        videos = read_csv_file(filepath)
        all_videos.extend(videos)
    return all_videos
