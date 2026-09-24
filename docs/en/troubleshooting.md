# Troubleshooting

## Collector returns status 0
Run the collector as the Zabbix user and then test `doveadm who -1` directly.

## sudo asks for a password
Verify the actual `doveadm` path and validate the selected sudoers file with `visudo -cf`.

## Checksum item is unsupported
Do not change permissions on protected authentication files. Disable or override the checksum item for that host when safe read access is not appropriate.

## IMAPS/POP3S reports only TCP status
This is intentional. The template uses protocol-aware checks for plain IMAP/POP3 and TCP connectivity checks for the encrypted ports.
