from dataclasses import dataclass
from datetime import datetime


@dataclass
class Usage:
    id: str
    account_id: str
    period_start: datetime
    period_end: datetime
    messages_count: int
    groups_count: int
    storage_bytes: int
