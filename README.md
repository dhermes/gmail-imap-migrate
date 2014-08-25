Python IMAP Migrate Tool
========================

This tool can be used to migrate mail from a retired Gmail account
to a new one. It was written when my wife changed her email
after our wedding.

There are other suggested [methods][1], but I found two key issues
with these tools (and also wanted to learn a bit about IMAP):
- I could not track progress easily during the large migration
- After Thunderbird froze, it could not (easily) pick up where it left off

#### How to Use

To use this tool, remove the line raising the import error and add
your GMail address and password to the variables listed below.
It assumes you are migrating from an `OLD_` account to a `NEW_`
account.

When adding your password, make sure to use an application specific
password (ASP) if you have two-factor authentication enabled for
your account.

This text borrowed from [`account_settings.py`][3].

#### Thing to Notice

If you use this tool and update `account_settings.py` with your own data,
be careful not to commit your password to GitHub. To ensure that
this won't occur, you can [run][3]
```
git update-index --assume-unchanged account_settings.py
```
and then your repository will ignore all your changes.

[1]: http://www.howtogeek.com/148036/how-to-migrate-your-google-account-to-a-new-one/
[2]: https://github.com/dhermes/gmail-imap-migrate/blob/master/account_settings.py
[3]: http://blog.pagebakers.nl/2009/01/29/
