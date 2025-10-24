from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class ScheduledChange:
    plan_id: str
    effective_date: datetime
    reason: Optional[str] = None


@dataclass
class Cancellation:
    reason: str
    effective_date: datetime
    feedback: Optional[str] = None


@dataclass
class Subscription:
    id: str
    account_id: str
    plan_id: str
    status: str
    start_date: datetime
    trial_ends_at: Optional[datetime]
    next_billing_at: Optional[datetime]
    current_period_end: Optional[datetime]
    scheduled_change: Optional[ScheduledChange]
    cancellation: Optional[Cancellation]
