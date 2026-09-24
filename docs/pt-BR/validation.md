# Validação e homologação

## Checks do repositório
```sh
python -m pip install -r requirements-dev.txt
sh -n scripts/dovecot_stats.sh
sh tests/test_collector.sh
python -m compileall -q tools
ruff check tools
python tools/validate_templates.py
python tools/validate_docs.py
```

## Checks no host
Confirme:
- coletor pertencente a conta administrativa;
- modo 0755 e sem escrita para o usuário Zabbix;
- `doveadm who -1` direto sempre que possível;
- sudoers, se necessário, limitado ao comando exato;
- JSON sem usernames;
- execução abaixo do timeout do Agent.

## Homologação Zabbix
Teste importação nova e, quando aplicável, upgrade in-place do template anterior. Revise Latest data, triggers, graphs, macros, service checks e checksums.

Não promova 3.0.0 para produção antes da aceitação do comportamento de importação/upgrade.
