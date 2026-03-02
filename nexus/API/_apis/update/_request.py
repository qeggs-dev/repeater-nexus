from pydantic import BaseModel
from typing import Any

class UpdateRequest(BaseModel):
    """
    Update Request
    """
    content: dict[str, Any]
    timeout: int | float | None = None