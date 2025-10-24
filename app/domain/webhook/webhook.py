from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Webhook:
    id: str
    account_id: str
    url: str
    secret: str
    events: List[str]
    status: str
    created_at: datetime
