20tab-nullmailer
================

An smtpd python class to inject mails in the nullmailer spool system


To bind it on address 127.0.0.1:1025 just run it:

```sh
python 20tab_nullmailer.py
```

otherwise just use its class

```py
import asyncore
from 20tab_nullmailer import Nullmailer

# bind it on port 8025
server = Nullmailer(('127.0.0.1', 8025), False)
asyncore.loop()
```
