# Changelog

[English](CHANGELOG.md) | **Português (Brasil)**

## 3.0.0 - Não lançado

### Adicionado
- repositório dedicado `kmansur/zabbix-dovecot`;
- exports Zabbix 7.0 e 8.0 em diretórios padronizados;
- contagem de usuários IMAP/POP3 ativos;
- máximo de conexões ativas por usuário;
- monitoramento da versão do coletor;
- exemplos sudoers de privilégio mínimo para FreeBSD e Linux;
- documentação bilíngue;
- testes de regressão do coletor e validação estática dos templates;
- CI GitHub Actions e CodeQL.

### Alterado
- nome técnico e visível padronizado para `Dovecot by Zabbix agent`;
- exports renomeados para `dovecot-by-zabbix-agent.yaml`;
- coletor executado como usuário não privilegiado do Zabbix Agent;
- elevação limitada ao comando exato `doveadm who -1` somente quando necessário;
- checks IMAP e POP3 passam a validar o protocolo;
- IMAPS e POP3S permanecem checks de conectividade TCP;
- triggers de tempo de resposta possuem histerese de recuperação;
- layout do repositório alinhado aos demais projetos Zabbix independentes.

### Preservado
- UUID do template;
- item keys e UUIDs existentes sempre que possível;
- caminho instalado `/usr/local/scripts/dovecot_stats.sh`;
- arquivos históricos do Zabbix 5.0 em `legacy/`.

### Segurança
- nunca conceder sudo ao coletor completo;
- nunca reduzir permissões de arquivos protegidos de autenticação/SQL apenas para checksum.
