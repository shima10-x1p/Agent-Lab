"""UTC 基準の Clock 実装。"""

from datetime import UTC, datetime

from agent_lab.application.ports.clock import ClockPort


class UtcClock(ClockPort):
    """UTC 現在時刻を返す Clock 実装。"""

    def now(self) -> datetime:
        """UTC の現在時刻を返す。
        
        Returns:
            UTC の現在時刻。
        """
        return datetime.now(tz=UTC)
