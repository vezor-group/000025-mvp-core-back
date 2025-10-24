from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class ApiKey:
    id: str
    account_id: str
    name: str
    key_hash: str
    scopes: List[str]
    status: str
    created_at: datetime
