import sys
import argparse
from pathlib import Path
from readers import read_all_files
from reporters.clickbait_reporter import ClickbaitReporter
from tabulate import tabulate
from models import Video, ReportResult



def create_parser():
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Генератор отчётов по видео на YouTube"
    )
    parser.add_argument(
        '--files',
        nargs='+',
        type=Path,
        required=True,
        help='Список CSV‑файлов с данными о видео'
    )
    parser.add_argument(
        '--report',
        type=str,
        required=True,
        choices=['clickbait'],
        help='Тип отчёта для генерации'
    )
    return parser



def display_report(report_result: ReportResult):
    """Отображает отчёт в табличном формате."""
    if not report_result.videos:
        print("Нет данных для отображения.")
        return

    table_data = [
        [video.title, f"{video.ctr:.1f}", f"{video.retention_rate:.1f}"]
        for video in report_result.videos
    ]

    headers = ["Название видео", "CTR (%)", "Удержание (%)"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))



def main():
    parser = create_parser()
    args = parser.parse_args()

    # Инициализируем videos до try-блока
    videos = []

    try:
        videos = read_all_files(args.files)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(2)  # ОШИБКА ФАЙЛА — код 2

    if args.report == 'clickbait':
        reporter = ClickbaitReporter()
        report_result = reporter.generate(videos)
        display_report(report_result)
    else:
        print(f"Неизвестный тип отчёта: {args.report}", file=sys.stderr)
        sys.exit(1)




if __name__ == "__main__":
    main()
