# Dovecot by Zabbix agent

[![CI](https://github.com/kmansur/zabbix-dovecot/actions/workflows/ci.yml/badge.svg)](https://github.com/kmansur/zabbix-dovecot/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kmansur/zabbix-dovecot/actions/workflows/security.yml/badge.svg)](https://github.com/kmansur/zabbix-dovecot/actions/workflows/security.yml)
[![Licença: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[English](README.md) | **Português (Brasil)**

Template Zabbix para monitoramento do Dovecot em FreeBSD e Linux através do Zabbix Agent/Agent 2. Utiliza um pequeno coletor POSIX shell, um item mestre JSON com itens dependentes, checks de serviço conscientes do protocolo e acesso de privilégio mínimo às estatísticas de sessão do Dovecot.

> **Status:** candidata de desenvolvimento **3.0.0**. O CI do repositório valida o coletor e a estrutura dos templates. O comportamento de importação/upgrade ainda deve ser confirmado em uma instância Zabbix de homologação antes do uso em produção.

## Objetivos de projeto

- preservar as item keys e UUIDs existentes sempre que tecnicamente possível;
- manter o coletor pequeno, auditável e com poucas dependências;
- executar o coletor como usuário não privilegiado do Zabbix Agent;
- elevar privilégio somente para o comando exato e somente leitura `doveadm who -1` quando necessário;
- executar uma única consulta de sessões por coleta e derivar as métricas do mesmo JSON;
- não enviar usernames, endereços de clientes ou dados de mailbox ao Zabbix;
- suportar os caminhos comuns do Dovecot em FreeBSD e Linux;
- manter exports separados para Zabbix 7.0 e 8.0.

## Compatibilidade

| Componente | Status |
| --- | --- |
| Zabbix 7.0 LTS | Export mantido; homologação obrigatória antes de produção |
| Zabbix 8.0 | Export mantido; homologação obrigatória antes de produção |
| FreeBSD | Layout de caminhos comum suportado |
| Linux | Layout de caminhos comum suportado |
| Dovecot 2.3 / 2.4 | Arquitetura compatível; validar no host de destino |

Os arquivos históricos do Zabbix 5.0 permanecem em `legacy/`. Não há export Zabbix 6.0 mantido neste repositório.

## Dados monitorados

- disponibilidade e último erro do coletor;
- versão do coletor;
- conexões IMAP;
- conexões POP3;
- total de conexões IMAP/POP3;
- usuários únicos com sessões IMAP/POP3 ativas;
- máximo de conexões simultâneas de um único usuário;
- versão do Dovecot;
- processo master do Dovecot;
- disponibilidade de IMAP, IMAPS, POP3 e POP3S;
- tempo de resposta dos serviços;
- checksum de arquivos de configuração selecionados.

Os usernames são usados apenas em memória para calcular métricas agregadas e não são retornados no JSON.

## Segurança

O coletor executa como usuário do Zabbix Agent. **Não conceda sudo ao script do coletor.**

Primeiro ele tenta `doveadm who -1` sem elevação. Se o socket do Dovecot não permitir a consulta, tenta somente o mesmo comando exato usando `sudo -n`.

FreeBSD:

```sudoers
zabbix ALL=(root) NOPASSWD: /usr/local/bin/doveadm who -1
```

Linux:

```sudoers
zabbix ALL=(root) NOPASSWD: /usr/bin/doveadm who -1
```

Não libere `doveadm` sem argumentos restritos, shells, UserParameters flexíveis ou sudo para `dovecot_stats.sh`.

## Estrutura

```text
.github/                 CI, CodeQL e templates de contribuição
config/                  UserParameter e exemplos sudoers
docs/
├── en/                  Documentação em inglês
└── pt-BR/               Documentação em português do Brasil
legacy/zabbix-5.0/       Arquivos históricos Zabbix 5.0
scripts/                 Coletor POSIX shell usado em produção
templates/
├── 7.0/                 Export Zabbix 7.0
└── 8.0/                 Export Zabbix 8.0
tests/                   Testes e fixtures do coletor
tools/                   Validadores estáticos
```

## Início rápido

Instale o coletor:

```sh
install -o root -g wheel -m 0755 scripts/dovecot_stats.sh /usr/local/scripts/dovecot_stats.sh
```

Em Linux, normalmente utilize `root:root`.

Instale `config/userparameter_dovecot.conf` no diretório de includes do Zabbix Agent/Agent 2.

Teste primeiro `doveadm who -1` diretamente como usuário `zabbix`. Instale o sudoers correspondente somente se o acesso direto falhar por permissão.

Importe o YAML da sua versão:

```text
templates/7.0/dovecot-by-zabbix-agent.yaml
templates/8.0/dovecot-by-zabbix-agent.yaml
```

Veja [instalação](docs/pt-BR/installation.md) e [migração](docs/pt-BR/migration.md).

## Observação importante sobre configuração

Os macros de arquivos de configuração mantêm os caminhos historicamente usados em FreeBSD para não quebrar instalações existentes. Em Linux, ajuste os macros para os caminhos reais usados pelo pacote do Dovecot.

Nunca reduza as permissões de arquivos que contêm credenciais apenas para permitir um item de checksum.

## Desenvolvimento

```sh
python -m pip install -r requirements-dev.txt
sh -n scripts/dovecot_stats.sh
sh tests/test_collector.sh
python tools/validate_templates.py
python tools/validate_docs.py
ruff check tools
```

## Versionamento

A versão candidata atual é `3.0.0`. A distribuição para produção será feita por GitHub Release depois da homologação de importação/upgrade e execução.

## Licença

MIT. Consulte [LICENSE](LICENSE).

Mantenedor: Karim Mansur / Net Tech.
