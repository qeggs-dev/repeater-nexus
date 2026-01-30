from pydantic import BaseModel
from typing import Any

class UpdateRequest(BaseModel):
    """
    Update Request
    """
    content: Any
    timeout: int | float | None = None