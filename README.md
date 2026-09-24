# Dovecot by Zabbix agent

[![CI](https://github.com/kmansur/zabbix-dovecot/actions/workflows/ci.yml/badge.svg)](https://github.com/kmansur/zabbix-dovecot/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kmansur/zabbix-dovecot/actions/workflows/security.yml/badge.svg)](https://github.com/kmansur/zabbix-dovecot/actions/workflows/security.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**English** | [Português (Brasil)](README.pt-BR.md)

Zabbix template for monitoring Dovecot on FreeBSD and Linux through Zabbix Agent/Agent 2. It uses a small POSIX shell collector, a JSON master item with dependent items, protocol-aware service checks, and least-privilege access to Dovecot session statistics.

> **Status:** development candidate **3.0.0**. Repository CI validates the collector and template structure. Import/upgrade behavior must still be verified in a homologation Zabbix instance before production rollout.

## Design goals

- preserve existing Dovecot item keys and UUIDs whenever practical;
- keep the monitored-host collector small, auditable, and dependency-light;
- run the collector as the unprivileged Zabbix agent user;
- escalate only the exact read-only `doveadm who -1` command when direct socket access is unavailable;
- execute one session query per collection and derive dependent metrics from the same JSON payload;
- avoid sending usernames, client addresses, or mailbox data to Zabbix;
- support common FreeBSD and Linux Dovecot paths;
- maintain separate Zabbix 7.0 and 8.0 exports.

## Compatibility

| Component | Status |
| --- | --- |
| Zabbix 7.0 LTS | Export maintained; homologation required before production |
| Zabbix 8.0 | Export maintained; homologation required before production |
| FreeBSD | Supported common path layout |
| Linux | Supported common path layout |
| Dovecot 2.3 / 2.4 | Collector design compatible; validate on the target host |

The historical Zabbix 5.0 files are preserved under `legacy/`. There is no maintained Zabbix 6.0 export in this repository.

## Monitored data

The template monitors:

- collector availability and last error;
- collector version;
- active IMAP connections;
- active POP3 connections;
- total active IMAP/POP3 connections;
- unique users with active IMAP/POP3 sessions;
- maximum concurrent IMAP/POP3 connections for one user;
- Dovecot version;
- Dovecot master process count;
- IMAP, IMAPS, POP3, and POP3S service availability;
- service response time;
- selected Dovecot configuration file checksums.

The collector uses usernames only in memory to calculate aggregate counters. Usernames are not returned in the JSON payload.

## Security model

The collector runs as the Zabbix agent user. **Do not grant sudo permission to the collector script.**

It first tries:

```text
doveadm who -1
```

without privilege escalation. If access to the Dovecot anvil socket is denied, it retries only that exact command with `sudo -n`.

FreeBSD example:

```sudoers
zabbix ALL=(root) NOPASSWD: /usr/local/bin/doveadm who -1
```

Linux example:

```sudoers
zabbix ALL=(root) NOPASSWD: /usr/bin/doveadm who -1
```

Do not use unrestricted `doveadm`, shell interpreters, flexible UserParameters, or a sudo rule for `dovecot_stats.sh`.

## Repository layout

```text
.github/                 CI, CodeQL and contribution templates
config/                  UserParameter and least-privilege sudoers examples
docs/
├── en/                  English documentation
└── pt-BR/               Brazilian Portuguese documentation
legacy/zabbix-5.0/       Preserved historical Zabbix 5.0 files
scripts/                 Production POSIX shell collector
templates/
├── 7.0/                 Zabbix 7.0 export
└── 8.0/                 Zabbix 8.0 export
tests/                   Collector regression tests and fixtures
tools/                   Static template/documentation validators
```

## Quick start

Install the collector as an administrator-owned executable:

```sh
install -o root -g wheel -m 0755 scripts/dovecot_stats.sh /usr/local/scripts/dovecot_stats.sh
```

On Linux, use the appropriate root group, normally `root`.

Install `config/userparameter_dovecot.conf` in the Zabbix Agent/Agent 2 include directory.

Test direct access to `doveadm who -1` as the Zabbix user. Install one of the sudoers examples only when direct access fails because of socket permissions.

Then test:

```sh
/usr/local/scripts/dovecot_stats.sh stats
/usr/local/scripts/dovecot_stats.sh version
/usr/local/scripts/dovecot_stats.sh collector-version
```

Import the YAML matching the target Zabbix version:

```text
templates/7.0/dovecot-by-zabbix-agent.yaml
templates/8.0/dovecot-by-zabbix-agent.yaml
```

See [installation](docs/en/installation.md) and [migration](docs/en/migration.md) for the complete procedure.

## Important configuration note

The default configuration-file macros retain the historical FreeBSD-oriented paths to avoid changing existing deployments unexpectedly. Linux hosts should override the configuration-file macros with the paths used by their Dovecot package.

Never weaken permissions on credential-bearing SQL/authentication files merely to make a checksum item readable.

## Development

```sh
python -m pip install -r requirements-dev.txt
sh -n scripts/dovecot_stats.sh
sh tests/test_collector.sh
python tools/validate_templates.py
python tools/validate_docs.py
ruff check tools
```

## Versioning

The current development candidate is `3.0.0`. A GitHub Release will be the production distribution point after import/upgrade and runtime homologation are completed.

## License

MIT. See [LICENSE](LICENSE).

Maintainer: Karim Mansur / Net Tech.
