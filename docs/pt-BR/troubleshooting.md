# Troubleshooting

## Coletor retorna status 0
Execute o coletor como usuário Zabbix e depois teste `doveadm who -1` diretamente.

## sudo solicita senha
Confira o caminho real do `doveadm` e valide o sudoers escolhido com `visudo -cf`.

## Item de checksum unsupported
Não altere permissões de arquivos protegidos de autenticação. Desabilite ou sobrescreva o item quando a leitura segura não for apropriada.

## IMAPS/POP3S verifica apenas TCP
É intencional. O template usa checks de protocolo para IMAP/POP3 sem TLS e checks de conectividade TCP nas portas criptografadas.
