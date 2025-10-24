from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class AuditLog:
    id: str
    account_id: str
    user_id: str
    action: str
    entity_type: str
    entity_id: str
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
