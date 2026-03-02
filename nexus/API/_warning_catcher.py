import warnings

from datetime import datetime
from typing import TextIO
from pathlib import Path
from loguru import logger

class WarningHandler:
    """Warning Handler"""
    def __init__(self) -> None:
        self.raw_showwarning = warnings.showwarning
    
    def inject(self) -> None:
        warnings.showwarning = self.warning_handler
    
    def remove(self) -> None:
        warnings.showwarning = self.raw_showwarning
    
    def warning_handler(
            self,
            message: Warning | str,
            category: type[Warning],
            filename: str,
            lineno: int,
            file: TextIO | None = None,
            line: str | None = None
        ) -> None:
        warning_time = datetime.now()
        file_path = Path(filename)

        # 记录异常日志
        logger.warning(
            (
                "Warning: \n"
                "{warning_name}\n"
                "    - Warning time: \n"
                "        {warning_time}\n"
                "    - Raised from:\n"
                "        {raiser}:{lineno}\n"
                "    - Message: \n"
                "        {message}\n"
            ),
            warning_name = category.__name__,
            warning_time = warning_time.strftime("%Y-%m-%d %H:%M:%S"),
            message = message,
            raiser = file_path.as_posix(),
            lineno = lineno,
        )