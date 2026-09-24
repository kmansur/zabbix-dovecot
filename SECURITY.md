# Security Policy

**English** | [Português (Brasil)](SECURITY.pt-BR.md)

## Supported version
Security fixes are developed against the current maintained candidate/release.

## Reporting
Do not publish credentials, production hostnames, public management addresses, usernames from mailbox sessions, or private logs in a public issue. Prefer GitHub Security Advisories for vulnerabilities.

## Security model
The collector runs as the unprivileged Zabbix user. When direct access to the Dovecot anvil socket is unavailable, only the exact `doveadm who -1` command may be allowed through passwordless sudo.

Never permit:
- the collector itself through sudo;
- unrestricted `doveadm`;
- `sh`, `bash`, Python, Perl, or other interpreters through the project sudoers rule;
- flexible UserParameters for this project;
- arbitrary command execution through Zabbix macros;
- weaker permissions on credential-bearing Dovecot files merely for checksum monitoring.

The collector emits only aggregate counters and does not return usernames.
