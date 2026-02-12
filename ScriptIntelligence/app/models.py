
from dataclasses import dataclass
from typing import List

@dataclass
class User:
    id: int
    name: str
    email: str

@dataclass
class Order:
    order_id: int
    user_email: str
    product_name: str
    quantity: int
