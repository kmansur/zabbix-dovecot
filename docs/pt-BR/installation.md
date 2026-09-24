# Instalação

## 1. Instale o coletor
FreeBSD:
```sh
install -d -o root -g wheel -m 0755 /usr/local/scripts
install -o root -g wheel -m 0755 scripts/dovecot_stats.sh /usr/local/scripts/dovecot_stats.sh
```

Em Linux, normalmente utilize `root:root`.

## 2. Instale o UserParameter
Instale `config/userparameter_dovecot.conf` em um diretório de include carregado pelo Zabbix Agent ou Agent 2. Confirme o include ativo na configuração local em vez de assumir um caminho específico da distribuição.

## 3. Teste o acesso direto ao Dovecot
Execute `doveadm who -1` como usuário Zabbix. Se funcionar, não instale regra sudoers.

Se falhar por permissão do socket anvil, instale somente o arquivo correspondente de `config/sudoers.d/` e valide com `visudo -cf`.

## 4. Teste o coletor
```sh
/usr/local/scripts/dovecot_stats.sh stats
/usr/local/scripts/dovecot_stats.sh version
/usr/local/scripts/dovecot_stats.sh collector-version
```

Depois teste as UserParameters pelo binário do Agent instalado.

## 5. Importe
Importe o YAML correspondente à versão Zabbix, revise o diff do importador, vincule o template e valide Latest data antes de habilitar alertas de produção.

## Macros em Linux
Os defaults históricos usam caminhos típicos de FreeBSD. Em Linux, sobrescreva `{$DOVECOT.CONF.FILE}` e `{$DOVECOT.SQL.CONF.FILE}` com os caminhos reais.

Não reduza permissões de arquivos protegidos para permitir checksum.
