IMPORT_MESSAGE = """\
To use this tool, remove the line raising the import error and add
your GMail address and password to the variables listed below.
It assumes you are migrating from an "OLD_" account to a "NEW_"
account.

When adding your password, make sure to use an application specific
password (ASP) if you have two-factor authentication enabled for
your account.
"""
raise ImportError(IMPORT_MESSAGE)

# Be careful not to commit your password to GitHub. To ensure that
# this won't occur, you can run
#     git update-index --assume-unchanged account_settings.py
# and then your repository will ignore all your changes.
# Reference: http://blog.pagebakers.nl/2009/01/29/
OLD_USERNAME = 'username@example.com'
OLD_PASSWORD = ''
NEW_USERNAME = 'username@example.com'
NEW_PASSWORD = ''
