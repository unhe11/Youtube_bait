import pytest
from models import Video, ReportResult
from reporters.clickbait_reporter import ClickbaitReporter

def test_clickbait_reporter_filters_correctly():
    videos = [
        Video('Видео 1', 18.2, 35),
        Video('Видео 2', 9.5, 82),
        Video('Видео 3', 25.0, 22),
    ]

    reporter = ClickbaitReporter()
    result = reporter.generate(videos)

    assert len(result.videos) == 2
    assert result.videos[0].title == 'Видео 3'
    assert result.videos[1].title == 'Видео 1'

def test_clickbait_reporter_empty_result():
    videos = [
        Video("Normal Video", 10.0, 50.0),  # CTR < 15
        Video("Another Normal", 12.0, 60.0)   # retention > 40
    ]
    reporter = ClickbaitReporter()
    result = reporter.generate(videos)
    assert len(result.videos) == 0  # Явная проверка длины списка

