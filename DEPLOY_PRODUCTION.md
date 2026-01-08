# Mesa Literária v3.0 - Guia de Deploy para Produção

## 📋 Índice

1. [Requisitos](#requisitos)
2. [Preparação](#preparação)
3. [Deploy](#deploy)
4. [Configuração do Servidor](#configuração-do-servidor)
5. [Manutenção](#manutenção)
6. [Troubleshooting](#troubleshooting)

---

## 🔧 Requisitos

### Sistema Operacional
- Ubuntu 20.04+ (recomendado)
- Debian 10+
- CentOS 8+
- Windows Server 2019+ (com WSL2)

### Software
- Python 3.8+
- MySQL 5.7+ ou MariaDB 10.3+
- Nginx ou Apache
- Git
- Supervisor (recomendado para gerenciamento de processos)

### Recursos Mínimos
- **CPU:** 1 vCore
- **RAM:** 1GB
- **Disco:** 10GB
- **Banda:** 100Mbps

### Recursos Recomendados
- **CPU:** 2 vCores
- **RAM:** 2GB
- **Disco:** 20GB SSD
- **Banda:** 1Gbps

---

## 🎯 Preparação

### 1. Clonar o Repositório

```bash
cd /var/www
git clone https://github.com/seu-usuario/MetaDeLeitura.git
cd MetaDeLeitura
git checkout prod_V3
```

### 2. Criar Usuário do Sistema

```bash
sudo useradd -r -s /bin/bash -d /var/www/MetaDeLeitura meta_leitura
sudo chown -R meta_leitura:meta_leitura /var/www/MetaDeLeitura
```

### 3. Configurar Banco de Dados

```sql
-- Conectar ao MySQL como root
CREATE DATABASE meta_leitura CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'meta_leitura_user'@'localhost' IDENTIFIED BY 'senha_forte_aqui';
GRANT ALL PRIVILEGES ON meta_leitura.* TO 'meta_leitura_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Configurar Variáveis de Ambiente

```bash
cp .env.production .env
nano .env
```

Edite o arquivo `.env`:

```bash
# SEGURANÇA - Gere uma chave forte!
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# BANCO DE DADOS
DB_HOST=localhost
DB_PORT=3306
DB_NAME=meta_leitura
DB_USER=meta_leitura_user
DB_PASSWORD=sua_senha_segura
```

---

## 🚀 Deploy

### Opção 1: Script Automático

```bash
chmod +x deploy.sh
./deploy.sh
```

### Opção 2: Manual

#### 1. Criar Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

#### 2. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # Para produção
```

#### 3. Criar Diretórios

```bash
mkdir -p logs
mkdir -p static/uploads/profiles
mkdir -p backups
```

#### 4. Executar Migrações

```bash
python migrate_add_user_fields.py
```

#### 5. Configurar Permissões

```bash
chmod -R 755 static/
chmod -R 777 static/uploads/
chmod 755 logs/
```

---

## ⚙️ Configuração do Servidor

### Gunicorn (WSGI Server)

#### 1. Criar arquivo de configuração

`/var/www/MetaDeLeitura/gunicorn_config.py`:

```python
import multiprocessing

# Servidor
bind = "127.0.0.1:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "meta_leitura"

# Server mechanics
daemon = False
pidfile = "gunicorn.pid"
user = "meta_leitura"
group = "meta_leitura"
umask = 0o007
```

#### 2. Testar Gunicorn

```bash
gunicorn -c gunicorn_config.py run:app
```

### Supervisor (Gerenciador de Processos)

#### 1. Instalar Supervisor

```bash
sudo apt-get install supervisor
```

#### 2. Criar configuração

`/etc/supervisor/conf.d/meta_leitura.conf`:

```ini
[program:meta_leitura]
directory=/var/www/MetaDeLeitura
command=/var/www/MetaDeLeitura/venv/bin/gunicorn -c gunicorn_config.py run:app
user=meta_leitura
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/www/MetaDeLeitura/logs/supervisor_error.log
stdout_logfile=/var/www/MetaDeLeitura/logs/supervisor_access.log
environment=FLASK_ENV="production"
```

#### 3. Ativar e Iniciar

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start meta_leitura
sudo supervisorctl status meta_leitura
```

### Nginx (Reverse Proxy)

#### 1. Instalar Nginx

```bash
sudo apt-get install nginx
```

#### 2. Criar configuração

`/etc/nginx/sites-available/meta_leitura`:

```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    # Redirecionar para HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name seu-dominio.com www.seu-dominio.com;

    # Certificados SSL (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Logs
    access_log /var/log/nginx/meta_leitura_access.log;
    error_log /var/log/nginx/meta_leitura_error.log;

    # Arquivos estáticos
    location /static {
        alias /var/www/MetaDeLeitura/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Upload de arquivos
    location /static/uploads {
        alias /var/www/MetaDeLeitura/static/uploads;
        expires 7d;
    }

    # Proxy para Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Segurança
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Limites
    client_max_body_size 5M;
}
```

#### 3. Ativar site

```bash
sudo ln -s /etc/nginx/sites-available/meta_leitura /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL com Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
sudo systemctl reload nginx
```

---

## 🔄 Manutenção

### Backup Automático

Criar script `/var/www/MetaDeLeitura/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/www/MetaDeLeitura/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup do banco
mysqldump -u meta_leitura_user -p'senha' meta_leitura | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup de uploads
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz static/uploads/

# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete
```

Adicionar ao cron:

```bash
crontab -e
# Adicionar:
0 2 * * * /var/www/MetaDeLeitura/backup.sh
```

### Atualização da Aplicação

```bash
cd /var/www/MetaDeLeitura

# Backup
./backup.sh

# Atualizar código
git pull origin prod_V3

# Atualizar dependências
source venv/bin/activate
pip install -r requirements.txt

# Executar migrações
python migrate_add_user_fields.py

# Reiniciar aplicação
sudo supervisorctl restart meta_leitura
```

### Monitoramento de Logs

```bash
# Logs da aplicação
tail -f logs/gunicorn_error.log

# Logs do Nginx
tail -f /var/log/nginx/meta_leitura_error.log

# Logs do Supervisor
tail -f logs/supervisor_error.log
```

### Limpeza de Logs

```bash
# Rotação automática de logs
sudo nano /etc/logrotate.d/meta_leitura
```

Adicionar:

```
/var/www/MetaDeLeitura/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 640 meta_leitura meta_leitura
    sharedscripts
    postrotate
        supervisorctl restart meta_leitura > /dev/null
    endscript
}
```

---

## 🔍 Troubleshooting

### Problema: Aplicação não inicia

**Verificar logs:**
```bash
tail -f logs/gunicorn_error.log
tail -f logs/supervisor_error.log
```

**Verificar permissões:**
```bash
ls -la /var/www/MetaDeLeitura
```

**Testar manualmente:**
```bash
source venv/bin/activate
python run.py
```

### Problema: Erro 502 Bad Gateway

**Verificar se Gunicorn está rodando:**
```bash
sudo supervisorctl status meta_leitura
ps aux | grep gunicorn
```

**Reiniciar Gunicorn:**
```bash
sudo supervisorctl restart meta_leitura
```

**Verificar configuração do Nginx:**
```bash
sudo nginx -t
```

### Problema: Uploads não funcionam

**Verificar permissões:**
```bash
ls -la static/uploads/
chmod -R 777 static/uploads/
```

**Verificar tamanho máximo:**
- Nginx: `client_max_body_size`
- App: `MAX_CONTENT_LENGTH`

### Problema: Conexão com banco falha

**Testar conexão:**
```bash
mysql -h localhost -u meta_leitura_user -p meta_leitura
```

**Verificar .env:**
```bash
cat .env | grep DB_
```

**Verificar logs do MySQL:**
```bash
sudo tail -f /var/log/mysql/error.log
```

### Problema: Sessões não persistem

**Verificar SECRET_KEY:**
```bash
grep SECRET_KEY .env
```

**Verificar cookies:**
- HTTPS habilitado?
- `SESSION_COOKIE_SECURE = True` ?

---

## 📊 Monitoramento

### Healthcheck

Criar endpoint `/health`:

```python
@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200
```

### Uptime Monitoring

Usar serviços como:
- UptimeRobot
- Pingdom
- StatusCake

### Performance Monitoring

Instalar New Relic ou Sentry:

```bash
pip install newrelic
pip install sentry-sdk[flask]
```

---

## 🔒 Segurança

### Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Fail2Ban

```bash
sudo apt-get install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Atualizações de Segurança

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
```

---

## 📞 Suporte

Para problemas ou dúvidas:
1. Verificar logs
2. Consultar documentação
3. Abrir issue no GitHub

---

## 📝 Checklist de Deploy

- [ ] Servidor configurado e atualizado
- [ ] Banco de dados criado
- [ ] Usuário do sistema criado
- [ ] Repositório clonado
- [ ] .env configurado com SECRET_KEY forte
- [ ] Dependências instaladas
- [ ] Migrações executadas
- [ ] Gunicorn configurado e testado
- [ ] Supervisor configurado
- [ ] Nginx configurado
- [ ] SSL/HTTPS configurado
- [ ] Firewall configurado
- [ ] Backup automático configurado
- [ ] Logs rotacionados
- [ ] Monitoramento configurado
- [ ] Testes de funcionalidade realizados

---

**Versão:** 3.0  
**Última atualização:** Janeiro 2026  
**Autor:** Mesa Literária Team
