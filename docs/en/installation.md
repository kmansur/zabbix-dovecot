# Installation

## 1. Install the collector
FreeBSD:
```sh
install -d -o root -g wheel -m 0755 /usr/local/scripts
install -o root -g wheel -m 0755 scripts/dovecot_stats.sh /usr/local/scripts/dovecot_stats.sh
```

Linux normally uses `root:root`.

## 2. Install the UserParameter
Install `config/userparameter_dovecot.conf` in an include directory loaded by Zabbix Agent or Agent 2. Confirm the active include path in the local agent configuration rather than assuming a distribution-specific directory.

## 3. Test direct Dovecot access
Run `doveadm who -1` as the Zabbix user. If it works, do not install a sudoers rule.

If access fails because the Dovecot anvil socket is restricted, install only the matching file from `config/sudoers.d/` and validate it with `visudo -cf`.

## 4. Test collector keys
```sh
/usr/local/scripts/dovecot_stats.sh stats
/usr/local/scripts/dovecot_stats.sh version
/usr/local/scripts/dovecot_stats.sh collector-version
```

Then test the UserParameters through the installed agent binary.

## 5. Import
Import the YAML matching the Zabbix version, review the import diff, link the template, and inspect Latest data before enabling production alerting.

## Linux configuration macros
The historical defaults point to FreeBSD-style paths. On Linux, override `{$DOVECOT.CONF.FILE}` and `{$DOVECOT.SQL.CONF.FILE}` for the actual package paths.

Do not weaken protected file permissions to make checksum items readable.
