from models import ReportResult, Video

class ClickbaitReporter:
    def generate(self, videos):
        filtered = [
            video for video in videos
            if video.ctr > 15 and video.retention_rate < 40
        ]
        # Сортировка по убыванию CTR
        filtered.sort(key=lambda x: x.ctr, reverse=True)
        return ReportResult(videos=filtered)
