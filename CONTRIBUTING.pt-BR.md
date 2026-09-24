# Contribuindo

[English](CONTRIBUTING.md) | **Português (Brasil)**

Contribuições, bugs, melhorias de documentação e relatórios de compatibilidade Dovecot/Zabbix são bem-vindos.

## Fluxo
1. Crie uma branch a partir de `main`.
2. Faça uma alteração focada.
3. Preserve UUIDs e item keys existentes em alterações compatíveis.
4. Atualize a documentação EN e pt-BR em conjunto.
5. Execute a suíte de validação.
6. Abra um pull request.

Branches recomendadas: `feature/*`, `fix/*`, `docs/*`, `refactor/*`, `test/*`, `ci/*`, `chore/*`.

## Validação local

```sh
python -m pip install -r requirements-dev.txt
sh -n scripts/dovecot_stats.sh
sh tests/test_collector.sh
python -m compileall -q tools
ruff check tools
python tools/validate_templates.py
python tools/validate_docs.py
```

Uma release também deve ser importada e testada nas versões Zabbix de destino. CI estático não substitui teste real de importação/upgrade.

## Segurança
- não conceder sudo ao coletor;
- não criar UserParameters flexíveis;
- não usar valores arbitrários de macros como comandos;
- não expor usernames, endereços, credenciais ou mailboxes;
- não reduzir permissões de arquivos de credenciais para satisfazer checksums.
