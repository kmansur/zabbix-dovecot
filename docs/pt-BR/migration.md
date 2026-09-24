# Migração do repositório legado

Origem:
`kmansur/Zabbix_Templates/Dovecot`

Destino:
`kmansur/zabbix-dovecot`

Mudanças somente de repositório:
- repositório independente;
- export padronizado como `dovecot-by-zabbix-agent.yaml`;
- nome técnico/visível alterado de `Template App Dovecot` para `Dovecot by Zabbix agent`;
- suporte atual concentrado em Zabbix 7.0 e 8.0;
- conteúdo histórico Zabbix 5.0 preservado em `legacy/`.

Compatibilidade no host:
- caminho do coletor permanece `/usr/local/scripts/dovecot_stats.sh`;
- keys das UserParameters permanecem;
- UUID do template permanece;
- item keys e UUIDs existentes são preservados sempre que possível.

A versão 3.0 também altera o modelo de privilégio: não execute o coletor via sudo. Libere somente o comando exato `doveadm who -1` quando o acesso direto não funcionar.

Antes de atualizar um template existente, importe em homologação e confira se o template existente é atualizado em vez de duplicado. Revise especialmente as mudanças das keys de service check IMAP/POP3.
