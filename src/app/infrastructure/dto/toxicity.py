from dataclasses import dataclass


@dataclass
class ToxicStatsDTO:
    telegram_id: int
    full_name: str
    toxic_ratio: float

    def __str__(self):
        return f"{self.full_name} - {int(self.toxic_ratio * 100)}%"
