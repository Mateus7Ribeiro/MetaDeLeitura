# 🔄 Guia de Migração v1.0 → v2.0

## ⚠️ Problema

Se você tem um banco de dados da **v1.0**, ao usar a **v2.0** você receberá:

```
sqlalchemy.exc.OperationalError: 
(pymysql.err.OperationalError) (1054, "Unknown column 'books.user_id' in 'field list'")
```

Isso acontece porque o novo sistema requer:
- ✅ Tabela `users` (não existia antes)
- ✅ Coluna `user_id` em `books` (não existia antes)

## ✅ Solução

Você tem **2 opções**:

---

## Opção 1: Script Python (RECOMENDADO) ⭐

### Passo 1: Execute o script
```bash
python migrate_db.py
```

### Passo 2: Veja o resultado
```
1️⃣  Verificando se tabelas existem...
   ✓ Tabelas criadas/verificadas

2️⃣  Verificando usuário admin...
   ✓ Usuário admin criado

3️⃣  Verificando livros sem proprietário...
   ✓ 5 livro(s) associado(s)

4️⃣  Estatísticas finais:
   📊 Total de usuários: 1
   📚 Total de livros: 5
   📋 Livros por usuário:
      - admin: 5 livro(s)

✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!
```

### Passo 3: Use normalmente
```bash
python run.py
```

---

## Opção 2: Script SQL (MANUAL)

### Passo 1: Abra MySQL
```bash
mysql -u root -p
```

### Passo 2: Use o banco
```sql
USE meta_leitura;
```

### Passo 3: Execute o script
```sql
-- Copie e cole o conteúdo de migrate_v1_to_v2.sql
```

Ou execute direto:
```bash
mysql -u root -p meta_leitura < migrate_v1_to_v2.sql
```

---

## 📝 O que Acontece Durante a Migração

### 1. Cria tabela `users`
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(255),
    reading_speed FLOAT DEFAULT 2.5,
    created_at DATETIME,
    updated_at DATETIME
);
```

### 2. Adiciona coluna `user_id` a `books`
```sql
ALTER TABLE books ADD COLUMN user_id INT NOT NULL;
```

### 3. Cria usuário `admin`
- **Username**: admin
- **Senha**: admin123
- **Email**: admin@local.com
- **Velocidade**: 2.5 min/página (padrão)

### 4. Associa todos os livros antigos ao admin
```sql
UPDATE books SET user_id = 1 WHERE user_id IS NULL;
```

### 5. Adiciona relacionamento
```sql
ALTER TABLE books ADD FOREIGN KEY (user_id) REFERENCES users(id);
```

---

## 🎯 Próximos Passos

Após a migração:

### 1. Execute a aplicação
```bash
python run.py
```

### 2. Faça login como admin
- Username: `admin`
- Senha: `admin123`

### 3. Veja seus livros antigos
- Todos estarão lá! 📚
- Associados ao usuário `admin`

### 4. Configure sua velocidade
- Vá em ⚙️ Configurações
- Altere "Tempo Médio por Página"
- Padrão é 2.5 (você pode usar o que preferir)

### 5. Crie novo usuário (Opcional)
- Clique em "Sair"
- Clique em "Registre-se"
- Crie sua conta pessoal
- Novos livros ficarão nesta conta

---

## 🔑 Credenciais Padrão

Após a migração, você tem:

```
Usuário admin (criado automaticamente)
├─ Username: admin
├─ Senha: admin123
├─ Email: admin@local.com
├─ Velocidade: 2.5 min/página
└─ Livros: Todos os seus livros antigos ✓
```

**Recomendação**: Depois de migrar, mude a senha de admin!

---

## ⚡ Migração Completa

| Arquivo | Conteúdo |
|---------|----------|
| `migrate_v1_to_v2.sql` | Script SQL puro (execute no MySQL) |
| `migrate_db.py` | Script Python (execute com `python migrate_db.py`) |

---

## ✨ Exemplo de Execução

### Terminal
```powershell
PS C:\PROJETOS\Python\MetaDeLeitura> python migrate_db.py
============================================================
MIGRAÇÃO DE BANCO DE DADOS v1.0 → v2.0
============================================================

1️⃣  Verificando se tabelas existem...
   ✓ Tabelas criadas/verificadas

2️⃣  Verificando usuário admin...
   ⚠ Usuário admin não encontrado, criando...
   ✓ Usuário admin criado
   📝 Credenciais:
      - Username: admin
      - Senha: admin123
      - Email: admin@local.com

3️⃣  Verificando livros sem proprietário...
   ⚠ 3 livro(s) sem proprietário encontrado(s)
   Associando ao usuário admin...
   ✓ 3 livro(s) associado(s)

4️⃣  Estatísticas finais:
   📊 Total de usuários: 1
   📚 Total de livros: 3
   📋 Livros por usuário:
      - admin: 3 livro(s)

============================================================
✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!
============================================================

Próximos passos:
1. Execute: python run.py
2. Acesse: http://localhost:5000
3. Faça login com admin/admin123
4. Vá em Configurações e altere a velocidade de leitura
5. Seus livros antigos continuam lá! 📚

PS C:\PROJETOS\Python\MetaDeLeitura>
```

---

## 🆘 Troubleshooting

### Erro: "Unknown column 'books.user_id'"
**Causa**: Migração não foi executada
**Solução**: Execute `python migrate_db.py` ou o script SQL

### Erro: "Duplicate entry 'admin'"
**Causa**: User admin já existe
**Solução**: Deletar e recriar:
```sql
DELETE FROM users WHERE username='admin';
```

### Erro de conexão MySQL
**Causa**: MySQL não está rodando
**Solução**: 
- Windows: Abra Services e inicie MySQL
- macOS: `brew services start mysql`
- Linux: `sudo systemctl start mysql`

### Livros sumiram
**Causa**: Algo deu errado na migração
**Solução**: 
1. Faça backup
2. Recrie o banco
3. Execute novamente

---

## 📊 Antes e Depois

### Antes (v1.0)
```
Banco: meta_leitura
├─ Tabela: books
│  ├─ id
│  ├─ name
│  ├─ total_pages
│  ├─ current_page
│  ├─ current_percentage
│  ├─ target_date
│  ├─ created_at
│  ├─ updated_at
│  └─ is_completed
```

### Depois (v2.0)
```
Banco: meta_leitura
├─ Tabela: users
│  ├─ id
│  ├─ username
│  ├─ email
│  ├─ password_hash
│  ├─ reading_speed ← NOVO!
│  ├─ created_at
│  └─ updated_at
│
├─ Tabela: books
│  ├─ id
│  ├─ user_id ← NOVO!
│  ├─ name
│  ├─ total_pages
│  ├─ current_page
│  ├─ current_percentage
│  ├─ target_date
│  ├─ created_at
│  ├─ updated_at
│  └─ is_completed
```

---

## ✅ Checklist

Antes de começar a usar v2.0:

- [ ] Executi `python migrate_db.py` (ou SQL script)
- [ ] Verifiquei que a migração completou com sucesso
- [ ] Executei `python run.py`
- [ ] Fiz login com admin/admin123
- [ ] Vi meus livros antigos no dashboard
- [ ] Alterei a velocidade de leitura
- [ ] Criei um novo usuário (opcional)

---

**Pronto! Sua migração está completa!** 🚀

Para dúvidas, consulte `FAQ.md` ou `TESTING.md`.
