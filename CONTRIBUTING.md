# Contributing

**English** | [Português (Brasil)](CONTRIBUTING.pt-BR.md)

Contributions, bug reports, documentation improvements, and Dovecot/Zabbix compatibility reports are welcome.

## Workflow
1. Create a branch from `main`.
2. Make one focused change.
3. Preserve existing template UUIDs and item keys for backward-compatible changes.
4. Update English and Brazilian Portuguese documentation together.
5. Run the validation suite.
6. Open a pull request.

Recommended branch names: `feature/*`, `fix/*`, `docs/*`, `refactor/*`, `test/*`, `ci/*`, `chore/*`.

## Local validation

```sh
python -m pip install -r requirements-dev.txt
sh -n scripts/dovecot_stats.sh
sh tests/test_collector.sh
python -m compileall -q tools
ruff check tools
python tools/validate_templates.py
python tools/validate_docs.py
```

A release must also be imported and tested in the target Zabbix versions. Static CI is not a substitute for real Zabbix import/upgrade testing.

## Security rules
- do not grant sudo to the collector script;
- do not introduce flexible UserParameters;
- do not pass arbitrary macro values as commands;
- do not expose usernames, client addresses, credentials, or mailbox names;
- do not weaken Dovecot credential-file permissions to satisfy checksum monitoring.
