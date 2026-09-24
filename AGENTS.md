# AGENTS.md — zabbix-dovecot

## Scope
This repository contains the standalone Dovecot monitoring project for Zabbix.

## Priority
Security > operational safety > backward compatibility > performance > simplicity > convenience.

## Naming
- repository: `zabbix-dovecot`
- template: `Dovecot by Zabbix agent`
- vendor: `Net Tech`
- collector: `scripts/dovecot_stats.sh`
- installed collector: `/usr/local/scripts/dovecot_stats.sh`
- exports: `templates/7.0/dovecot-by-zabbix-agent.yaml` and `templates/8.0/dovecot-by-zabbix-agent.yaml`

## Compatibility
Preserve the template UUID, item UUIDs, item keys, and macros unless a breaking change is intentional, justified, documented, and tested.

## Security
The collector must run unprivileged. Never sudo the full collector. Only the exact read-only `doveadm who -1` command may receive sudo permission when required.

Do not introduce flexible UserParameters, `system.run[]`, arbitrary command construction, or credential exposure.

## Privacy
Do not return usernames, client IP addresses, mailbox names, passwords, or other session identifiers to Zabbix. Aggregate metrics are allowed.

## Runtime
The monitored host must not require Python. Production collection remains POSIX shell + awk. Python dependencies are development/CI only.

## Documentation
Maintain English and Brazilian Portuguese documentation together.

## Validation
Run:
```sh
sh -n scripts/dovecot_stats.sh
sh tests/test_collector.sh
python tools/validate_templates.py
python tools/validate_docs.py
ruff check tools
```
