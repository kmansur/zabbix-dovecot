# Migration from the legacy repository

Source:
`kmansur/Zabbix_Templates/Dovecot`

Destination:
`kmansur/zabbix-dovecot`

Repository-only changes:
- dedicated standalone repository;
- standardized export filename `dovecot-by-zabbix-agent.yaml`;
- technical/visible template name changed from `Template App Dovecot` to `Dovecot by Zabbix agent`;
- current template support limited to 7.0 and 8.0;
- historical Zabbix 5.0 content preserved under `legacy/`.

Host-side compatibility:
- collector installation path remains `/usr/local/scripts/dovecot_stats.sh`;
- UserParameter keys remain unchanged;
- template UUID remains unchanged;
- existing item keys and UUIDs are preserved wherever practical.

Version 3.0 also changes the privilege model: do not sudo the collector. Allow only the exact `doveadm who -1` command if direct access is unavailable.

Before upgrading an existing template, import into homologation and inspect whether the existing template is updated rather than duplicated. Review the IMAP/POP3 service-check key changes carefully.
