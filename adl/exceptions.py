class GetEbookException(Exception):
    def __init__(self, filepath:str, message:str):
        super().__init__(f"Could not get ebook {filepath} - {message}")

class DataDirectoryAccessError(Exception):
    def __init__(self):
        super().__init__("Error accessing data directory!")

BYTEBOOKS_HELP_URL = "https://dtsbytebooks.com/transition-help"

class AdeptError(Exception):
    """An <error> reply from an Adobe ADEPT server.

    `data` is the raw error string, e.g. "E_AUTH_FAILED http://.../SignInDirect CUS05051",
    and `code` is its first word.
    """
    def __init__(self, data:str, message:str|None=None):
        self.data = data
        self.code = data.split()[0] if data else ""
        if message is None:
            message = "Adobe server returned an error"
        super().__init__(f"{message} (server said: {data})")

class AdeptAuthFailedError(AdeptError):
    def __init__(self, data:str):
        if "CUS05051" in data:
            message = (
                "Sign-in failed: wrong email or password. Since June 23, 2026 Adobe ID sign-in "
                "is handled by ByteBooks, so use your ByteBooks email and password "
                f"(see {BYTEBOOKS_HELP_URL})"
            )
        elif "LOGIN_FAILED" in data:
            message = (
                "Sign-in failed. This usually means two-factor authentication is on for the "
                "account; ADEPT sign-in can't send a 2FA code, so turn 2FA off and try again"
            )
        else:
            message = "Sign-in failed: the server rejected the credentials"
        super().__init__(data, message)

class AdeptResetPWRequiredError(AdeptError):
    def __init__(self, data:str):
        super().__init__(
            data,
            "Sign-in failed: this Adobe ID hasn't been moved to ByteBooks yet. Go to "
            f"{BYTEBOOKS_HELP_URL}, set a new password using the same email (so your books "
            "carry over), then sign in again with the new password",
        )

_ADEPT_ERRORS = {
    "E_AUTH_FAILED": AdeptAuthFailedError,
    "E_ADEPT_RESET_PW_REQUIRED": AdeptResetPWRequiredError,
}

def adept_error(data:str) -> AdeptError:
    """The most specific AdeptError for the server's error string."""
    code = data.split()[0] if data else ""
    cls = _ADEPT_ERRORS.get(code)
    return cls(data) if cls else AdeptError(data)
