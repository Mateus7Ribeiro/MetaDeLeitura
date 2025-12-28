# GUIA COMPLETO DE DEPLOY - Meta de Leitura

## 🚀 Opções de Hosting Recomendadas

### 1. **PythonAnywhere** ⭐ (MAIS FÁCIL - Recomendado para iniciantes)
- **Custo**: Grátis até ~100k hits/mês
- **Vantagens**: Hosting Python completo, setup automático, MySQL incluído
- **Desvantagens**: Limitado em recursos
- **Tempo de setup**: 5-10 minutos

### 2. **Heroku** (DEPRECATED 2022, não recomendado)
- Parou de oferecer plano grátis

### 3. **Railway.app** 🚀 (Excelente)
- **Custo**: $5/mês ou pay-as-you-go
- **Vantagens**: Git deploy automático, PostgreSQL/MySQL incluído
- **Desvantagens**: Precisa cartão de crédito
- **Tempo de setup**: 10-15 minutos

### 4. **Render.com** (Ótima alternativa)
- **Custo**: $7-12/mês
- **Vantagens**: Deploy automático, banco grátis
- **Desvantagens**: Mais lento que Railway
- **Tempo de setup**: 10-15 minutos

### 5. **AWS / DigitalOcean / Linode** (Profissional)
- **Custo**: $3-20/mês
- **Vantagens**: Controle total, escalável
- **Desvantagens**: Setup mais complexo
- **Tempo de setup**: 30-60 minutos

---

## 🔧 PREPARAÇÃO DO PROJETO

### Passo 1: Criar arquivo `.env` para produção

Crie `.env.production`:
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=seu-chave-secreta-super-longa-e-segura-aqui-32-caracteres-min
DB_USER=seu_usuario_mysql
DB_PASSWORD=sua_senha_mysql
DB_HOST=seu_host_mysql (ex: mysql.pythonanywhere.com)
DB_PORT=3306
DB_NAME=seu_usuario_mysql$meta_leitura
```

### Passo 2: Gerar SECRET_KEY segura

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Passo 3: Atualizar requirements.txt para produção

Adicione:
```
Gunicorn==21.2.0
```

Gunicorn é um servidor WSGI profissional (melhor que o desenvolvimento).

### Passo 4: Criar arquivo Procfile (para Heroku/Railway)

```
web: gunicorn "app:create_app()"
```

### Passo 5: Criar arquivo runtime.txt

```
python-3.11.5
```

### Passo 6: Atualizar app/config.py para produção

Adicione ao começo:
```python
# Produção
SESSION_COOKIE_SECURE = True  # HTTPS apenas
SESSION_COOKIE_SAMESITE = 'Lax'
```

---

## 📋 COMPARAÇÃO DE PLATAFORMAS

| Plataforma     | Custo    | Facilidade | MySQL Nativo | Deploy   |
|---|---|---|---|---|
| PythonAnywhere | Grátis   | ⭐⭐⭐⭐⭐  | ✅           | Manual   |
| Railway        | $5+      | ⭐⭐⭐⭐   | ✅           | Git      |
| Render         | $7+      | ⭐⭐⭐⭐   | ✅           | Git      |
| DigitalOcean   | $3+      | ⭐⭐⭐    | ✅           | Variado  |
| AWS            | Variável | ⭐⭐     | ✅           | Variado  |

---

## ✅ PASSO A PASSO: PYTHONANYWHERE (Recomendado)

### 1. Registre-se
- Acesse: https://www.pythonanywhere.com
- Crie conta gratuita

### 2. Setup do Banco de Dados
- Vá para "Databases"
- Clique em "Add a database"
- MySQL (escolha seu nome de usuário)
- Anote as credenciais

### 3. Crie um Web App
- "Web" → "Add a new web app"
- Escolha "Python 3.11"
- Escolha "Flask"

### 4. Configure o Código
- Vá para "Web" → seu app
- Na seção "Code" clique em "Go to directory"
- Clone seu repositório:
```bash
git clone https://github.com/seu_usuario/MetaDeLeitura.git
cd MetaDeLeitura
```

### 5. Instale Dependências
```bash
pip install --user -r requirements.txt
```

### 6. Configure o arquivo WSGI
- PythonAnywhere cria um arquivo `/var/www/seu_usuario_pythonanywhere_com_wsgi.py`
- Substitua pelo código abaixo:

```python
import sys
import os
path = '/home/seu_usuario/MetaDeLeitura'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)
os.environ['FLASK_ENV'] = 'production'

from app import create_app
application = create_app()
```

### 7. Configurar Variáveis de Ambiente
- Web → Seu app → "WSGI configuration file"
- Adicione no topo antes de `from app import create_app`:
```python
os.environ['DB_HOST'] = 'seu_usuario.mysql.pythonanywhere-services.com'
os.environ['DB_USER'] = 'seu_usuario'
os.environ['DB_PASSWORD'] = 'sua_senha'
os.environ['DB_NAME'] = 'seu_usuario$meta_leitura'
os.environ['SECRET_KEY'] = 'sua-chave-segura-aqui'
```

### 8. Reload da aplicação
- Clique em "Reload" em verde na página do Web app

### 9. Acesse seu app
- `https://seu_usuario.pythonanywhere.com`

---

## ✅ PASSO A PASSO: RAILWAY.APP

### 1. Registre-se
- Acesse: https://railway.app
- Login com GitHub

### 2. Crie novo projeto
- "New Project" → "Deploy from GitHub"
- Selecione seu repositório

### 3. Adicione banco MySQL
- Clique em "Add" → "Database" → "MySQL"

### 4. Configure Variáveis
- Vá para "Variables"
- Copie todas da seção DATABASE_URL e configure:
```
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta
DB_HOST=seu_mysql_host
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=seu_banco
```

### 5. Configure Deployment
- Crie `railway.json`:
```json
{
  "build": {
    "builder": "nixpacks"
  },
  "deploy": {
    "startCommand": "gunicorn 'app:create_app()' --bind 0.0.0.0:$PORT"
  }
}
```

### 6. Deploy automático
- Cada push para seu repo faz deploy automático

---

## 🔒 CHECKLIST PRÉ-DEPLOY

- [ ] `SECRET_KEY` alterada para valor seguro (32+ caracteres)
- [ ] `SESSION_COOKIE_SECURE = True` em produção
- [ ] Banco de dados configurado (MySQL no servidor)
- [ ] Arquivo `.env.production` criado com credenciais
- [ ] `requirements.txt` atualizado com Gunicorn
- [ ] `run.py` configurado para `debug=False` em produção
- [ ] Testado localmente com `gunicorn "app:create_app()"`
- [ ] `.gitignore` inclui `.env`, `.env.production`, `__pycache__`

---

## ⚠️ PROBLEMAS COMUNS E SOLUÇÕES

### Erro: "No module named 'app'"
**Solução**: Certifique-se de que `__init__.py` existe em `app/`

### Erro: "Can't connect to MySQL"
**Solução**: Verifique credenciais de banco no `.env`

### Erro: "ModuleNotFoundError: No module named 'flask'"
**Solução**: Rode `pip install -r requirements.txt`

### App lento em PythonAnywhere
**Solução**: Upgrade para conta paga ou use Railway/Render

### CSS/JS não carregam
**Solução**: Certifique-se da pasta `static/` no servidor

---

## 🎯 PRÓXIMOS PASSOS

1. Escolha uma plataforma (PythonAnywhere é mais fácil)
2. Siga o passo a passo acima
3. Teste a URL pública
4. Configure domínio customizado (opcional)

---

## 📞 SUPORTE

Dúvidas? Consulte:
- PythonAnywhere: https://help.pythonanywhere.com
- Railway: https://docs.railway.app
- Render: https://render.com/docs

Sucesso no deploy! 🚀
