# sshmap
SSH Tool For OSINT and then Cracking.

`Linux Systems Only`

![example](https://github.com/0bliss/sshmap/blob/main/sshmap.png)

# Usage:
```
Scanner Syntax:
    scanner start/stop/status                 - Sarts/stops/shows status of the scanner.
    scanner timeout <interger_in_seconds>     - Sts timeout to wait for each possible SSH server. Dont set too low.
    Scanner port <new_op_port>                - Scanner operating port. currently only uses one at a time.
    scanner adduser/rmuser <user_to_add>      - Ad users/remove users from try list. The more you add the longer it takes.
    scanner log <new_log_file>                - Canges the scanner log file to write to at the end.
Load Syntax:
    load iplist <path_to_list_of_ips.txt>     - Text File of plain text IP addresses you may have to automatically check for SSH servers.
Exit Syntax:
    exit                                      - Closes the program.
```
More Soon...
