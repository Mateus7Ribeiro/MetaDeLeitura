# 🚀 Deploy PythonAnywhere - Mesa Literária v3.0

## 📋 Pré-requisitos

- Conta PythonAnywhere (Free, Hacker ou Web Developer)
- Versão 1.0 rodando com dados
- Acesso ao console bash
- Acesso ao MySQL database

---

## ⚠️ IMPORTANTE - Backup da v1.0

**ANTES DE QUALQUER COISA, faça backup completo da v1.0!**

```bash
# 1. Conectar ao MySQL via console PythonAnywhere
mysql -u YOUR_USERNAME -h YOUR_USERNAME.mysql.pythonanywhere-services.com -p

# 2. Fazer dump do banco de dados
mysqldump -u YOUR_USERNAME -h YOUR_USERNAME.mysql.pythonanywhere-services.com -p YOUR_USERNAME\$meta_leitura > backup_v1_$(date +%Y%m%d_%H%M%S).sql

# 3. Backup dos uploads (fotos, etc)
cd ~
tar -czf backup_v1_uploads_$(date +%Y%m%d_%H%M%S).tar.gz MetaDeLeitura/static/uploads/

# 4. Backup do código
tar -czf backup_v1_code_$(date +%Y%m%d_%H%M%S).tar.gz MetaDeLeitura/

# 5. Verificar backups criados
ls -lh backup_v1_*
```

---

## 📦 Passo 1: Preparar Novo Diretório

```bash
# 1. Abrir console Bash no PythonAnywhere

# 2. Renomear versão antiga (não deletar!)
cd ~
mv MetaDeLeitura MetaDeLeitura_v1_backup

# 3. Clonar nova versão
git clone https://github.com/SEU_USUARIO/MetaDeLeitura.git
cd MetaDeLeitura
git checkout prod_V3  # ou main, dependendo da branch

# 4. Verificar estrutura
ls -la
```

---

## 🐍 Passo 2: Configurar Virtual Environment

```bash
# 1. Criar virtualenv (Python 3.10 recomendado)
mkvirtualenv --python=/usr/bin/python3.10 metaleitura_v3

# 2. Ativar virtualenv
workon metaleitura_v3

# 3. Atualizar pip
pip install --upgrade pip

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Verificar instalação
pip list | grep -E "Flask|SQLAlchemy|pymysql"
```

---

## 🗄️ Passo 3: Configurar Variáveis de Ambiente

**⚠️ IMPORTANTE: Configure ANTES de executar migrações!**

```bash
cd ~/MetaDeLeitura

# Copiar template
cp .env.pythonanywhere .env

# Editar arquivo .env
nano .env
```

**Configure os valores:**

```bash
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-generated-with-secrets-token-hex-32

DB_HOST=YOUR_USERNAME.mysql.pythonanywhere-services.com
DB_PORT=3306
DB_NAME=YOUR_USERNAME$meta_leitura
DB_USER=YOUR_USERNAME
DB_PASSWORD=your_mysql_password

LOG_LEVEL=INFO
```

**Gerar SECRET_KEY:**
```bash
workon metaleitura_v3
python -c "import secrets; print(secrets.token_hex(32))"
```

**Salvar e sair:** Ctrl+O, Enter, Ctrl+X

---

## 🗄️ Passo 4: Configurar Banco de Dados

### 4.1 Backup Adicional (via interface web)

1. Acesse **Databases** tab
2. Clique em **Download** ao lado do database `YOUR_USERNAME$meta_leitura`
3. Salve o arquivo `.sql.gz` localmente

### 4.2 Preparar para Migração

```bash
# Conectar ao MySQL
mysql -u YOUR_USERNAME -h YOUR_USERNAME.mysql.pythonanywhere-services.com -p

# Verificar tabelas existentes
USE YOUR_USERNAME$meta_leitura;
SHOW TABLES;
DESCRIBE users;
DESCRIBE books;

# Sair do MySQL
exit;
```

### 4.3 Executar Migrações

```bash
cd ~/MetaDeLeitura

# Ativar virtualenv
workon metaleitura_v3

# Executar migração completa para v3.0 (RECOMENDADO)
# Este script adiciona: name, profile_picture, user_hash e tabela user_followers
python migrate_to_v3.py

# OU executar migrações individualmente:
# python migrate_add_user_fields.py  # Adiciona name e profile_picture
# python migrate_user_hash.py        # Adiciona user_hash e user_followers

# Verificar resultado
python -c "
from app import create_app, db
from app.models import User
app = create_app(create_tables=False)
with app.app_context():
    print('Usuários encontrados:', User.query.count())
    user = User.query.first()
    if user:
        print('Campos do usuário:', [c.name for c in User.__table__.columns])
        print('User hash:', user.user_hash)
"
```

---

##  Passo 5: Restaurar Uploads da v1.0

```bash
# Copiar fotos de perfil e uploads da v1.0
mkdir -p ~/MetaDeLeitura/static/uploads/profiles
cp -r ~/MetaDeLeitura_v1_backup/static/uploads/* ~/MetaDeLeitura/static/uploads/

# Verificar
ls -la ~/MetaDeLeitura/static/uploads/profiles/
```

---

## 🌐 Passo 6: Configurar Web App

### 6.1 Acessar Web Tab

1. Vá para **Web** tab no PythonAnywhere
2. Se tiver app existente, clique em **Reload** (não delete ainda)

### 6.2 Atualizar Configuração

**Source code:**
```
/home/YOUR_USERNAME/MetaDeLeitura
```

**Working directory:**
```
/home/YOUR_USERNAME/MetaDeLeitura
```

**WSGI configuration file:**
- Clique em **WSGI configuration file** link
- Substitua TODO o conteúdo por:

```python
import sys
import os

# Adicionar projeto ao path
project_home = '/home/YOUR_USERNAME/MetaDeLeitura'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Carregar variáveis de ambiente
from dotenv import load_dotenv
dotenv_path = os.path.join(project_home, '.env')
load_dotenv(dotenv_path)

# Criar aplicação
from app import create_app
application = create_app()
```

### 6.3 Configurar Virtualenv

Na seção **Virtualenv:**
```
/home/YOUR_USERNAME/.virtualenvs/metaleitura_v3
```

### 6.4 Configurar Static Files

Adicionar mapeamentos:

| URL                  | Directory                                          |
|----------------------|----------------------------------------------------|
| /static/             | /home/YOUR_USERNAME/MetaDeLeitura/static           |
| /static/uploads/     | /home/YOUR_USERNAME/MetaDeLeitura/static/uploads   |

---

## 🧪 Passo 7: Testar Aplicação

```bash
# 1. Testar conexão com banco
cd ~/MetaDeLeitura
workon metaleitura_v3

python -c "
from app import create_app, db
app = create_app(create_tables=False)
with app.app_context():
    try:
        db.engine.connect()
        print('✅ Conexão com banco OK')
    except Exception as e:
        print('❌ Erro:', e)
"

# 2. Testar carregamento da aplicação
python -c "
from app import create_app
app = create_app(create_tables=False)
print('✅ Aplicação carregada com sucesso')
print('Blueprints:', [bp.name for bp in app.blueprints.values()])
"
```

### 7.1 Reload Web App

1. Volte para **Web** tab
2. Clique em **Reload YOUR_USERNAME.pythonanywhere.com**
3. Aguarde 10-15 segundos

### 7.2 Verificar Error Log

1. Clique em **Error log** link
2. Verifique se há erros
3. Corrija e recarregue se necessário

---

## ✅ Passo 8: Validação

### 8.1 Testar Funcionalidades Básicas

- [ ] Página inicial carrega
- [ ] Login funciona com usuários da v1.0
- [ ] "Minhas Leituras" mostra livros antigos
- [ ] Adicionar novo livro funciona
- [ ] Editar livro funciona
- [ ] Atualizar progresso funciona

### 8.2 Testar Novas Funcionalidades v3.0

- [ ] **Perfil:** Foto de perfil (sem foto ainda)
- [ ] **Perfil:** Editar nome em Configurações
- [ ] **Perfil:** Upload de foto funciona
- [ ] **Perfil:** Visualizar seguidores funciona
- [ ] **Perfil:** Visualizar seguindo funciona
- [ ] **Configurações:** Alterar senha funciona
- [ ] **Configurações:** Validação de senha forte funciona
- [ ] **Leitura Coletiva:** Gráfico de progresso proporcional correto

### 8.3 Verificar Dados Migrados

```bash
mysql -u YOUR_USERNAME -h YOUR_USERNAME.mysql.pythonanywhere-services.com -p

USE YOUR_USERNAME$meta_leitura;

-- Verificar novos campos
DESCRIBE users;
-- Deve ter: name, profile_picture

-- Verificar dados
SELECT id, username, name, email, profile_picture FROM users LIMIT 5;

-- Verificar se name foi populado
SELECT COUNT(*) as total, 
       COUNT(name) as com_name, 
       COUNT(profile_picture) as com_foto 
FROM users;

exit;
```

---

## 🔄 Passo 9: Migração de Dados Específica

### Se usuários não têm o campo 'name' populado:

```bash
cd ~/MetaDeLeitura
workon metaleitura_v3

python -c "
from app import create_app, db
from app.models import User

app = create_app(create_tables=False)
with app.app_context():
    users = User.query.filter(User.name == None).all()
    for user in users:
        user.name = user.username
    db.session.commit()
    print(f'✅ {len(users)} usuários atualizados com nome')
"
```

---

## 🚨 Solução de Problemas

### Error: "No module named 'app'"

```bash
# Verificar estrutura
ls -la ~/MetaDeLeitura/app/

# Verificar WSGI path
grep "project_home" /var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py

# Verificar __init__.py
cat ~/MetaDeLeitura/app/__init__.py
```

### Error: "Access denied for user"

```bash
# Verificar .env
cat ~/MetaDeLeitura/.env | grep DB_

# Testar conexão manualmente
mysql -u YOUR_USERNAME -h YOUR_USERNAME.mysql.pythonanywhere-services.com -p
```

### Error: "Unknown column 'users.user_hash' in 'field list'"

```bash
# Executar migração completa
cd ~/MetaDeLeitura
workon metaleitura_v3
python migrate_to_v3.py
```

### Error: "Table 'users' doesn't have column 'name'"

```bash
# Re-executar migração completa
cd ~/MetaDeLeitura
workon metaleitura_v3
python migrate_to_v3.py
```

### Static files não carregam

1. Verificar mapeamentos no Web tab
2. Verificar permissões: `ls -la ~/MetaDeLeitura/static/`
3. Reload web app

### 500 Internal Server Error

1. Verificar Error Log no Web tab
2. Verificar se virtualenv está configurado
3. Verificar WSGI file
4. Testar localmente: `python -c "from app import create_app; create_app()"`

---

## 📊 Monitoramento

### Verificar Logs

```bash
# Error log (via Web tab)
# Acesse: Web > Error log

# Ou via console
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log
```

### Verificar Uso de Disco

```bash
du -sh ~/MetaDeLeitura
du -sh ~/MetaDeLeitura/static/uploads/
```

---

## 🎯 Checklist Final

- [ ] Backup v1.0 realizado (código, banco, uploads)
- [ ] Banco de dados migrado com sucesso
- [ ] Campos `name` e `profile_picture` existem na tabela users
- [ ] Virtualenv configurado e ativo
- [ ] Arquivo .env criado com credenciais corretas
- [ ] WSGI file atualizado
- [ ] Static files mapeados
- [ ] Uploads da v1.0 copiados
- [ ] Web app recarregado sem erros
- [ ] Login funciona com usuários existentes
- [ ] Livros da v1.0 visíveis
- [ ] Novas funcionalidades testadas
- [ ] Error log sem erros críticos

---

## 📝 Diferenças v1.0 → v3.0

### Banco de Dados
- ✅ Compatível: Estrutura antiga preservada
- 🆕 Novos campos: `users.name`, `users.profile_picture`
- 🆕 Novas tabelas: Nenhuma (evolução incremental)

### Funcionalidades Novas
1. **Perfis de Usuário:**
   - Nome editável (separado de username)
   - Upload de foto de perfil
   - Visualização de seguidores/seguindo
   - Estatísticas detalhadas

2. **Segurança:**
   - Política de senha forte
   - Troca de senha com validação
   - Validação de senha antiga

3. **Leitura Coletiva:**
   - Gráfico de progresso proporcional corrigido
   - Melhor visualização de múltiplos livros

4. **Interface:**
   - Botão "Novo Livro" contextual
   - Username clicável na navbar
   - Design modernizado

### Arquivos Novos
- `wsgi.py` - Configuração PythonAnywhere
- `migrate_add_user_fields.py` - Migração de campos
- `app/config.py` - Sistema multi-ambiente
- Templates atualizados

---

## 🔙 Rollback (Se necessário)

```bash
# 1. Parar web app (via Web tab > Disable)

# 2. Restaurar código v1.0
cd ~
rm -rf MetaDeLeitura
mv MetaDeLeitura_v1_backup MetaDeLeitura

# 3. Restaurar banco de dados
gunzip < backup_v1_YYYYMMDD_HHMMSS.sql.gz | mysql -u YOUR_USERNAME -h YOUR_USERNAME.mysql.pythonanywhere-services.com -p YOUR_USERNAME\$meta_leitura

# 4. Atualizar WSGI para v1.0 (se necessário)

# 5. Reload web app
```

---

## 📞 Suporte

### Logs Úteis
- Error log: Web tab > Error log
- Server log: Web tab > Server log
- Access log: /var/log/

### Comandos de Diagnóstico

```bash
# Verificar Python
python --version

# Verificar pip packages
pip list | grep -E "Flask|SQLAlchemy|pymysql"

# Testar importações
python -c "import flask; import sqlalchemy; import pymysql; print('✅ OK')"

# Verificar banco
mysql -u YOUR_USERNAME -h YOUR_USERNAME.mysql.pythonanywhere-services.com -p -e "SHOW DATABASES;"
```

---

## 🎉 Sucesso!

Após seguir todos os passos, sua aplicação v3.0 estará rodando no PythonAnywhere com:

✅ Todos os dados da v1.0 preservados  
✅ Novas funcionalidades de perfil  
✅ Sistema de upload de fotos  
✅ Segurança aprimorada  
✅ Interface modernizada  

**URL:** https://YOUR_USERNAME.pythonanywhere.com

---

**Versão:** 3.0  
**Plataforma:** PythonAnywhere  
**Data:** Janeiro 2026
