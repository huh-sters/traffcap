from typing import Dict, Any
from pydantic import BaseModel
import json


class Metric(BaseModel):
    type: str = ""
    help: str = ""
    data: Dict[str, Any] = {}
    value: float = 0

    def __str__(self) -> str:
        data = json.dumps(self.data)
        return (
            f"# HELP {self.type} {self.help}\n"
            f"# TYPE {self.type} gauge\n"
            f"{self.type}{data} {self.value}"
        )
