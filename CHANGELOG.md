# Changelog

**English** | [Português (Brasil)](CHANGELOG.pt-BR.md)

## 3.0.0 - Unreleased

### Added
- dedicated `kmansur/zabbix-dovecot` repository;
- Zabbix 7.0 and 8.0 exports under standardized version directories;
- active IMAP/POP3 user count;
- maximum active connections per user;
- collector version monitoring;
- FreeBSD and Linux least-privilege sudoers examples;
- bilingual project documentation;
- collector regression tests and static template validation;
- GitHub Actions CI and CodeQL workflows.

### Changed
- standardized the technical and visible template name to `Dovecot by Zabbix agent`;
- standardized export filenames to `dovecot-by-zabbix-agent.yaml`;
- collector runs as the unprivileged Zabbix agent user;
- privilege escalation is limited to the exact read-only `doveadm who -1` command only when direct access fails;
- plain IMAP and POP3 checks use protocol-aware Zabbix service checks;
- IMAPS and POP3S remain TCP connectivity checks;
- response-time triggers include recovery hysteresis;
- repository layout now matches the maintainer's standalone Zabbix projects.

### Preserved
- existing template UUID;
- existing item keys and UUIDs wherever practical;
- `/usr/local/scripts/dovecot_stats.sh` installation path;
- Zabbix 5.0 historical files under `legacy/`.

### Security
- never grant sudo permission to the full collector;
- never weaken protected authentication/SQL file permissions for checksum monitoring.
