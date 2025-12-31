---
aliases:
  - War Game
cssclasses:
  - Linux
---
## Bandit
---
### Level 0

SSH was designed for [Unix-like](https://en.wikipedia.org/wiki/Unix-like "Unix-like") operating systems as a replacement for [Telnet](https://en.wikipedia.org/wiki/Telnet "Telnet") and [unsecured](https://en.wikipedia.org/wiki/Computer_security "Computer security") remote [Unix shell](https://en.wikipedia.org/wiki/Unix_shell "Unix shell") protocols, such as the Berkeley [Remote Shell](https://en.wikipedia.org/wiki/Remote_Shell "Remote Shell") (rsh) and the related [rlogin](https://en.wikipedia.org/wiki/Rlogin "Rlogin") and [rexec](https://en.wikipedia.org/wiki/Rexec "Rexec") protocols, which all use insecure, [plaintext](https://en.wikipedia.org/wiki/Plaintext "Plaintext") methods of authentication, such as [passwords](https://en.wikipedia.org/wiki/Password "Password").


> [!NOTE] Defination
> SSH uses [public-key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography "Public-key cryptography") to [authenticate](https://en.wikipedia.org/wiki/Authenticate "Authenticate") the remote computer and allow it to authenticate the user, if necessary.


> [!IMPORTANT] OpenSSH 
> On [Unix-like](https://en.wikipedia.org/wiki/Unix-like "Unix-like") systems, the list of authorized public keys is typically stored in the home directory of the user that is allowed to log in remotely, in the file `~/.ssh/authorized_keys`.
> The [ssh-keygen](https://en.wikipedia.org/wiki/Ssh-keygen "Ssh-keygen") utility produces the public and private keys, always in pairs.





