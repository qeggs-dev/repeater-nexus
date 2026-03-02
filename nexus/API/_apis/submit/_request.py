from pydantic import BaseModel
from typing import Any

class SubmitRequest(BaseModel):
    """
    Submit Request
    """
    content: dict[str, Any]
    timeout: int | float | None = None