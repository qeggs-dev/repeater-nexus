from pydantic import BaseModel
from typing import Any

class SubmitRequest(BaseModel):
    """
    Submit Request
    """
    content: Any
    timeout: int | float | None = None