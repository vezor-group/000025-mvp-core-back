from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class BillingCycle:
    interval: str  # monthly, yearly, etc.
    interval_count: int


@dataclass
class Plan:
    id: str
    code: str
    name: str
    type: str
    price_brl: float
    billing_cycle: BillingCycle
    limits: Dict[str, Any]
    features: List[str]
    status: str
