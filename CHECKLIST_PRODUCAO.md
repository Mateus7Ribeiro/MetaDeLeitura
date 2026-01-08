# Mesa Literária v3.0 - Checklist de Produção

## 📋 Pré-Deploy

### Servidor
- [ ] Servidor Linux configurado (Ubuntu 20.04+)
- [ ] Acesso SSH configurado
- [ ] Firewall configurado (80, 443, 22)
- [ ] Swap configurado (mínimo 2GB)
- [ ] Sistema atualizado (`apt update && apt upgrade`)

### Software
- [ ] Python 3.8+ instalado
- [ ] MySQL/MariaDB instalado e configurado
- [ ] Nginx instalado
- [ ] Supervisor instalado
- [ ] Git instalado
- [ ] Certbot instalado (para SSL)

### Banco de Dados
- [ ] Database `meta_leitura` criada
- [ ] Usuário do banco criado com permissões
- [ ] Charset: utf8mb4
- [ ] Collation: utf8mb4_unicode_ci
- [ ] Backup inicial realizado

---

## 🔐 Segurança

### Chaves e Senhas
- [ ] SECRET_KEY gerada (64+ caracteres hexadecimais)
- [ ] Senha do banco forte e única
- [ ] Senha do usuário do sistema forte
- [ ] Credenciais armazenadas com segurança

### Configuração
- [ ] `.env` criado com todas as variáveis
- [ ] `.env` com permissões 600 (`chmod 600 .env`)
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `DEBUG = False`
- [ ] HTTPS configurado e funcionando

### Firewall
- [ ] UFW ou iptables configurado
- [ ] Apenas portas necessárias abertas
- [ ] Fail2Ban instalado e configurado
- [ ] Rate limiting configurado no Nginx

---

## 📦 Aplicação

### Código
- [ ] Repositório clonado na branch `prod_V3`
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Gunicorn instalado

### Diretórios
- [ ] `logs/` criado
- [ ] `backups/` criado
- [ ] `static/uploads/profiles/` criado
- [ ] Permissões corretas (`chmod 777 static/uploads/`)

### Banco de Dados
- [ ] Conexão testada
- [ ] Migrações executadas (`python migrate_add_user_fields.py`)
- [ ] Estrutura verificada (`DESCRIBE users;`)
- [ ] Dados de teste criados (opcional)

---

## ⚙️ Configuração de Serviços

### Gunicorn
- [ ] `gunicorn_config.py` configurado
- [ ] Número de workers adequado
- [ ] Bind address correto (127.0.0.1:5000)
- [ ] Logs configurados
- [ ] Testado manualmente

### Supervisor
- [ ] Configuração copiada para `/etc/supervisor/conf.d/`
- [ ] `supervisorctl reread` executado
- [ ] `supervisorctl update` executado
- [ ] Serviço iniciado (`supervisorctl start meta_leitura`)
- [ ] Status verificado (`supervisorctl status`)

### Nginx
- [ ] Configuração copiada para `/etc/nginx/sites-available/`
- [ ] Symlink criado em `/etc/nginx/sites-enabled/`
- [ ] Domínio configurado corretamente
- [ ] Syntax check executado (`nginx -t`)
- [ ] Nginx recarregado (`systemctl reload nginx`)

### SSL/TLS
- [ ] Certbot executado para o domínio
- [ ] Certificado obtido com sucesso
- [ ] Auto-renovação configurada
- [ ] HTTPS funcionando
- [ ] HTTP redireciona para HTTPS
- [ ] HSTS configurado

---

## 🧪 Testes

### Funcionalidades Básicas
- [ ] Página inicial carrega
- [ ] Login funciona
- [ ] Registro funciona
- [ ] Criação de livro funciona
- [ ] Upload de foto funciona
- [ ] Troca de senha funciona

### Leituras Coletivas
- [ ] Criação de leitura coletiva funciona
- [ ] Adicionar livros funciona
- [ ] Aderir funciona
- [ ] Atualizar progresso funciona
- [ ] Gráfico exibe corretamente
- [ ] Livros aparecem em "Minhas Leituras"

### Perfis
- [ ] Visualização de perfil funciona
- [ ] Upload de foto funciona
- [ ] Edição de nome funciona
- [ ] Lista de seguidores funciona
- [ ] Lista de seguindo funciona
- [ ] Paginação funciona

### Performance
- [ ] Tempo de resposta < 500ms
- [ ] Imagens carregam rápido
- [ ] Sem erros 500
- [ ] Logs não mostram erros

---

## 📊 Monitoramento

### Logs
- [ ] Logs da aplicação funcionando
- [ ] Rotação de logs configurada
- [ ] Acesso aos logs configurado
- [ ] Nível de log apropriado (INFO em produção)

### Uptime
- [ ] Monitoramento configurado (UptimeRobot, Pingdom, etc.)
- [ ] Alertas configurados
- [ ] Email de notificação configurado
- [ ] Healthcheck endpoint funcionando

### Backup
- [ ] Script de backup testado
- [ ] Cron job configurado
- [ ] Backup manual realizado
- [ ] Restauração testada
- [ ] Retenção de backups configurada

---

## 🔄 Manutenção

### Documentação
- [ ] README.md atualizado
- [ ] DEPLOY_PRODUCTION.md revisado
- [ ] Credenciais documentadas (em local seguro)
- [ ] Procedimentos de emergência documentados

### Automatização
- [ ] Backup agendado (cron)
- [ ] Limpeza de logs agendada
- [ ] Monitoramento configurado
- [ ] Alertas configurados

### Acesso
- [ ] Chaves SSH configuradas
- [ ] Usuários necessários criados
- [ ] Permissões verificadas
- [ ] 2FA habilitado (se disponível)

---

## ✅ Validação Final

### Checklist de Lançamento
- [ ] Todos os itens acima verificados
- [ ] Testes de carga realizados
- [ ] Testes de segurança realizados
- [ ] Documentação completa
- [ ] Equipe treinada
- [ ] Plano de rollback preparado
- [ ] Backup pré-deploy realizado
- [ ] DNS configurado corretamente
- [ ] CDN configurado (se aplicável)
- [ ] Email/notificações funcionando

### Go-Live
- [ ] Migração de dados (se necessário)
- [ ] Verificação de integridade
- [ ] Monitoramento ativo
- [ ] Equipe de plantão disponível
- [ ] Comunicação aos usuários
- [ ] Changelog publicado

---

## 🚨 Procedimentos de Emergência

### Rollback
```bash
# 1. Parar aplicação
sudo supervisorctl stop meta_leitura

# 2. Restaurar código anterior
git checkout <commit_anterior>

# 3. Restaurar banco (se necessário)
gunzip < backups/db_backup_YYYYMMDD.sql.gz | mysql -u user -p database

# 4. Reiniciar
sudo supervisorctl start meta_leitura
```

### Contatos de Emergência
- [ ] Lista de contatos atualizada
- [ ] Telefones configurados
- [ ] Escalação definida

---

## 📝 Notas

### Data de Deploy: _______________

### Responsável: _______________

### Observações:
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

**Versão:** 3.0  
**Última atualização:** Janeiro 2026
