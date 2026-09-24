# Validation and homologation

## Repository checks
```sh
python -m pip install -r requirements-dev.txt
sh -n scripts/dovecot_stats.sh
sh tests/test_collector.sh
python -m compileall -q tools
ruff check tools
python tools/validate_templates.py
python tools/validate_docs.py
```

## Host checks
Confirm:
- collector owned by an administrative account;
- mode 0755 and not writable by the Zabbix user;
- direct `doveadm who -1` works when possible;
- sudoers, if needed, permits only the exact command;
- collector JSON never includes usernames;
- collector runtime stays below the Zabbix Agent timeout.

## Zabbix homologation
Test both a fresh import and, when applicable, an in-place upgrade from the previous template. Review Latest data, triggers, graphs, macros, service checks, and configuration checksums.

Do not promote 3.0.0 to a production release until the import/upgrade behavior has been accepted.
