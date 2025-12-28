# 🚀 Guia Rápido de Início

## Opção 1: Windows (Recomendado)

### Passo 1: Instalar dependências
Clique duas vezes no arquivo `install.bat`

### Passo 2: Configurar o banco de dados
1. Abra o MySQL Workbench ou linha de comando do MySQL
2. Execute:
```sql
CREATE DATABASE meta_leitura;
```

### Passo 3: Configurar credenciais
1. Abra o arquivo `.env` em um editor de texto
2. Preencha suas credenciais do MySQL:
```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
DB_NAME=meta_leitura
```

### Passo 4: Executar
Clique duas vezes no arquivo `run.bat`

O sistema abrirá em: **http://localhost:5000**

---

## Opção 2: macOS/Linux

### Passo 1: Abrir terminal

### Passo 2: Instalar dependências
```bash
chmod +x install.sh
./install.sh
```

### Passo 3: Configurar o banco de dados
```bash
mysql -u root -p
```
Na linha do MySQL:
```sql
CREATE DATABASE meta_leitura;
EXIT;
```

### Passo 4: Configurar credenciais
Edite o arquivo `.env` com suas credenciais

### Passo 5: Ativar ambiente virtual
```bash
source venv/bin/activate
```

### Passo 6: Executar
```bash
python run.py
```

---

## Opção 3: Criação manual da tabela (Opcional)

Se preferir criar a tabela manualmente, execute o arquivo `database.sql` no MySQL:

1. Abra MySQL Workbench
2. Abra o arquivo `database.sql`
3. Clique em "Execute"

---

## Primeira Execução

1. Acesse: **http://localhost:5000**
2. Clique em "+ Novo Livro"
3. Preencha os dados:
   - **Nome**: O nome do livro
   - **Total de Páginas**: Quantas páginas tem o livro
   - **Páginas Atuais**: Quantas páginas já leu (opcional)
   - **Data Limite**: Até quando quer terminar

4. Clique em "Cadastrar Livro"

---

## Calculadora de Meta

O sistema **calcula automaticamente**:

- **Páginas por dia**: Quantas páginas precisa ler por dia
- **Dias restantes**: Quantos dias faltam
- **Progresso**: Porcentagem lida
- **Páginas restantes**: Quantas páginas faltam

---

## Troubleshooting

### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Erro: "Connection refused" (Banco de dados)
- Verifique se o MySQL está rodando
- Confirme as credenciais em `.env`

### Erro: "Porta 5000 em uso"
Edite `run.py`:
```python
app.run(debug=True, host='localhost', port=5001)
```

### Problema: Não consegue acessar o site
- Espere 2-3 segundos após iniciar
- Tente: http://127.0.0.1:5000
- Verifique se há erro no terminal

---

## Dicas

✅ Defina metas realistas
✅ Atualize o progresso regularmente
✅ Use "Editar" para corrigir dados
✅ Não deletar livros sem fazer backup

---

**Pronto! Comece a controlar suas metas de leitura!** 📚
