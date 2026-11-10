__version__ = "0.2.0"

from .exceptions import (
  DataDirectoryAccessError,
  GetEbookException,
  AdeptError,
  AdeptAuthFailedError,
  AdeptResetPWRequiredError,
)

__all__ = [
  "__version__",
  "data",
  "DataDirectoryAccessError",
  "GetEbookException",
  "AdeptError",
  "AdeptAuthFailedError",
  "AdeptResetPWRequiredError",
]
from . import db

data = db.DBData()

if not data.check_or_create_dir():
  raise DataDirectoryAccessError()

data.load()
