from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    id: Optional[int]
    name: str
    sku: str
    quantity: int
    price: float
    category: Optional[str] = None
    
    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if self.price <= 0:
            raise ValueError("Price must be positive")