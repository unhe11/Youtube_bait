from dataclasses import dataclass
from typing import List

@dataclass
class Video:
    title: str
    ctr: float
    retention_rate: float

@dataclass
class ReportResult:
    videos: List[Video]