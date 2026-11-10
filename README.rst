ADL
===

Download ebooks from Adobe .acsm files, and transfer them to your ebook reader.

This tool intends to provide some basic functions to handle books protected by Adobe ADEPT DRM.
On Windows, MacOS, Android, Adobe provides Adobe Digital Editions (ADE) for such functionalities. Unfortunately, there is no Linux version of ADE. Wine is reported to work but I did not have much success.

This program is a command-line tool to perform the same tasks. It was tested only on Linux.

Note that, unlike some other tools, adl will not try to remove the DRM.

What it does
------------
- Allow you to login with your Adobe ID. You can log in as anonymous with some restrictions (see below)
- Activate a new ebook reader that supports Adobe ADEPT DRM
- Download your epub from the acsm file. 

If your book is protected by DRM, you will obtain an encrypted epub. 
If your device is activated with the same user as the one used to download the book, it will be able to read this encrypted file. Just copy it on the device.

What it will not do
-------------------
- Remove the DRM from your book

Disclaimer
----------
This tool is suited above all to my purpose. It has not been tested extensively, nor in any other setup. Use at your own risks.

License
-------
This tool is published under the GPLv3

Requirements
============

- python 3.6

Install dependencies::

  pip install -r requirements.txt


How to use
==========

Login
-----
Use::

  ./adl.py login -u <email>

You only need to login once, to exchange encryption keys.

Since June 23, 2026, Adobe ID sign-in is handled by ByteBooks (Wipro now runs Adobe's ebook services). The protocol and servers are unchanged, but the email and password must be those of a ByteBooks account. If your Adobe ID hasn't been moved over yet, sign-in fails until you set a new password at https://dtsbytebooks.com/transition-help, using the same email so your books carry over. Accounts with two-factor authentication turned on can't sign in this way.

I recommend to login with an Adobe ID (which can be created on Adobe website). It is possible to login as Anonymous, but be aware that you may lose access to your book if something goes wrong during download. Also, you will not be able to download it again if you ever lose the private key (or if you use another client). With an Adobe ID, the keys and the books are attached to your account: you can login from somewhere else and get them back.
As far as I understand, it is also possible to use other IDs to log in, but this is not supported yet.

You can login several times if you have several accounts.

Download a book
---------------

Download a book with::

  ./adl.py get -f <file.acsm>

Manage accounts
---------------

In case you have logged in several times, list your current accounts with::

  ./adl.py account list

And change the currently used account with::

  ./adl.py account use <account urn>

Activate a device
-----------------

Mount the root of your device somewhere, and select the account you want to use. Then::

  ./adl.py device register <mountpoint>

Several cases may occur:
- The device has never been activated with ADE (or adl): activate the device
- The device has already been activated for your user: nothing will be done on your device, but adl's db will be updated
- The device has already been activated for an unknown user: nothing will be done, to avoid losing access to books on the device

Transfer the downloaded book to the device
------------------------------------------

Not (yet ?) handled by adl, but you just have to copy it on the device's filesystem. On my readers, the books can be put anywhere.

Using adl as a library
======================

``import adl`` creates and loads ``~/.adl``. The modules (``adl.login``, ``adl.epub_get``, ``adl.account``, ...) are what ``adl.py`` uses.

Errors
------

When an Adobe server rejects a sign-in, ``adl.login.login`` raises instead of logging and returning. All of these can be imported from ``adl``:

- ``AdeptError``: any error reply from the server. ``.code`` is the error code (e.g. ``E_AUTH_FAILED``) and ``.data`` the server's full error string. The message says what went wrong and, where possible, what to do about it.
- ``AdeptAuthFailedError`` (``E_AUTH_FAILED``): wrong email or password, or two-factor authentication is on.
- ``AdeptResetPWRequiredError`` (``E_ADEPT_RESET_PW_REQUIRED``): the Adobe ID hasn't been moved to ByteBooks yet.
- ``GetEbookException``: ``epub_get.get_ebook`` couldn't download the book.

For example::

  import adl
  from adl import login

  try:
    login.login(user, password)
  except adl.AdeptResetPWRequiredError:
    ...  # send the user to https://dtsbytebooks.com/transition-help
  except adl.AdeptError as e:
    print(e)

See ``CHANGELOG.rst`` for changes that affect code using adl.
