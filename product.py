from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    id: Optional[int] = None
    price: float = 0.0
    name: str = ""
    weight: float = 0.0
    size: float = 0.0