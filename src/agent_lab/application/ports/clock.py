"""時刻取得ポート。"""

from abc import ABC, abstractmethod
from datetime import datetime


class ClockPort(ABC):
    """現在時刻を提供するポート。"""

    @abstractmethod
    def now(self) -> datetime:
        """現在時刻を返す。"""
