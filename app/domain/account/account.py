from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Account:
    id: str
    name: str
    document: str
    status: str
    created_at: datetime
    updated_at: datetime
