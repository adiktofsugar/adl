from .exceptions import (
  DataDirectoryAccessError,
  GetEbookException,
  AdeptError,
  AdeptAuthFailedError,
  AdeptResetPWRequiredError,
)
from . import db

data = db.DBData()

if not data.check_or_create_dir():
  raise DataDirectoryAccessError()

data.load()
