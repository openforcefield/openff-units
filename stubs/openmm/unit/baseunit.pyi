from typing import Any

class BaseUnit:
    def __init__(self, base_dim: Any, name: str, symbol: str): ...
    @property
    def name(self) -> str: ...
