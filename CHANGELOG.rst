Changelog
=========

0.2.0 (2026-11-10)
------------------

Breaking:

- ``login.login`` (via ``api_call.SignInDirect``) now raises when the server rejects a sign-in, instead of logging the error and returning. Code that called it expecting no exception must catch ``adl.AdeptError``.

Added:

- ``AdeptError``, ``AdeptAuthFailedError`` and ``AdeptResetPWRequiredError``, with messages that say what to do (including the ByteBooks migration). These and ``GetEbookException`` are exported from ``adl``.
- ``adl.__version__``.
- ``adl.py`` prints these errors and exits with status 1 instead of showing a traceback.

0.1.0
-----

Everything up to commit ``e0ac4ad``, before adl had a version number.
