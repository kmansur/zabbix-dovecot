# Política de Segurança

[English](SECURITY.md) | **Português (Brasil)**

## Versão suportada
Correções de segurança são desenvolvidas sobre a candidata/release atualmente mantida.

## Relato
Não publique credenciais, hostnames de produção, IPs públicos de gerenciamento, usernames de sessões ou logs privados em issue pública. Para vulnerabilidades, prefira GitHub Security Advisories.

## Modelo de segurança
O coletor executa como usuário não privilegiado do Zabbix. Quando não houver acesso direto ao socket anvil do Dovecot, somente o comando exato `doveadm who -1` pode ser liberado via sudo sem senha.

Nunca permita:
- o coletor completo via sudo;
- `doveadm` sem argumentos restritos;
- `sh`, `bash`, Python, Perl ou outros interpretadores no sudoers do projeto;
- UserParameters flexíveis;
- execução arbitrária de comandos através de macros Zabbix;
- redução de permissões em arquivos com credenciais apenas para checksum.

O coletor retorna somente contadores agregados e não retorna usernames.
