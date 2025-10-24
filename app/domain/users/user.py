from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: str
    account_id: str
    name: str
    email: str
    phone: Optional[str]
    role: str
    status: str
    last_login_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
