# ❓ Perguntas Frequentes (FAQ)

## Instalação

### P: Qual versão do Python preciso?
**R:** Python 3.8 ou superior. Você pode verificar com `python --version`

### P: Qual banco de dados usar?
**R:** MySQL 5.7+. Você pode baixar em: https://dev.mysql.com/downloads/mysql/

### P: Preciso de algum software adicional?
**R:** Não obrigatoriamente. Mas é recomendado:
- **MySQL Workbench** (para gerenciar o banco)
- **Git** (para versionamento)
- **VS Code** (para editar código)

### P: O arquivo `install.bat` deu erro
**R:** Tente:
```bash
python -m pip install --upgrade pip
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### P: Como criar o banco de dados?
**R:** Duas formas:

**Opção 1 - Command Line:**
```bash
mysql -u root -p
CREATE DATABASE meta_leitura;
EXIT;
```

**Opção 2 - MySQL Workbench:**
1. Abra o Workbench
2. Clique em "+" para nova conexão
3. Execute: `CREATE DATABASE meta_leitura;`

---

## Configuração

### P: Onde edito o arquivo `.env`?
**R:** 
1. Abra o arquivo `.env` em um editor de texto
2. Procure por `DB_USER`, `DB_PASSWORD`, etc
3. Altere com suas credenciais
4. Salve

### P: Qual deve ser meu `SECRET_KEY`?
**R:** Pode ser qualquer string. Sugestão:
```bash
python -c "import secrets; print(secrets.token_hex(16))"
```

### P: Tenho MySQL rodando, mas não consegui conectar
**R:** Verifique:
1. Username e password corretos no `.env`
2. Porta MySQL (padrão: 3306)
3. MySQL está rodando: `mysql --version`
4. Teste a conexão: `mysql -u seu_usuario -p`

---

## Execução

### P: Como começo o aplicativo?
**R:** 
- **Windows:** Clique 2x em `run.bat`
- **Mac/Linux:** Execute `python run.py`

### P: Qual URL acessar?
**R:** Abra no navegador: `http://localhost:5000`

### P: Deu erro "ModuleNotFoundError"
**R:** Instale as dependências:
```bash
pip install -r requirements.txt
```

### P: Porta 5000 já está em uso
**R:** Altere em `run.py`:
```python
app.run(debug=True, host='localhost', port=5001)
```

### P: Como parar a execução?
**R:** No terminal, pressione: `Ctrl + C`

---

## Banco de Dados

### P: Como limpar todos os dados?
**R:** 
```bash
mysql -u root -p
USE meta_leitura;
DELETE FROM books;
EXIT;
```

### P: Posso fazer backup dos dados?
**R:** Sim:
```bash
mysqldump -u root -p meta_leitura > backup.sql
```

E restaurar:
```bash
mysql -u root -p meta_leitura < backup.sql
```

### P: Posso usar SQLite em vez de MySQL?
**R:** Sim, mas precisa alterar `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///meta_leitura.db'
```

---

## Uso da Aplicação

### P: Como cadastrar um livro?
**R:**
1. Clique em "+ Novo Livro"
2. Preencha os campos
3. Clique "Cadastrar Livro"

### P: Como atualizar meu progresso?
**R:**
1. Na página inicial, clique em "Editar"
2. Altere as "Páginas Lidas Atualmente"
3. Clique "Salvar Alterações"

### P: O sistema calcula automaticamente as páginas/dia?
**R:** Sim! Acesse "Detalhes" do livro para ver:
- Páginas por dia necessárias
- Dias restantes
- Tempo médio por página

### P: Posso editar a data limite?
**R:** Sim, clique em "Editar" e altere a "Data Limite para Conclusão"

### P: Posso deletar um livro?
**R:** Sim, clique em "Deletar" (cuidado, não há volta!)

### P: Como marcar um livro como concluído?
**R:** Quando você atualiza para a página final, o sistema marca automaticamente

---

## Interface

### P: O sistema funciona em celular?
**R:** Sim! A interface é responsiva e se adapta a qualquer tela

### P: Onde vejo as estatísticas?
**R:** Na página de detalhes de cada livro (clique em "Detalhes")

### P: Posso customizar as cores?
**R:** Sim, edite `static/css/style.css` e altere as variáveis CSS

### P: Como mudar o idioma?
**R:** Os templates usam português por padrão. Você pode editar os arquivos HTML

---

## Performance

### P: O sistema fica lento com muitos livros?
**R:** Banco de dados tem índices para performance. Se mesmo assim ficar lento:
1. Considere arquivar livros antigos
2. Use paginação
3. Otimize o MySQL

### P: Quanto de espaço em disco usa?
**R:** Muito pouco! Menos de 10MB (incluindo código)

---

## Segurança

### P: Meus dados estão seguros?
**R:** 
- Dados armazenados no seu computador
- Sem conexão com internet
- Protegido com validação de entrada

### P: Posso compartilhar o código?
**R:** Sim! Mas remova o `.env` antes

### P: Como fazer backup seguro?
**R:** 
```bash
# Exportar dados
mysqldump -u root -p meta_leitura > backup_$(date +%Y%m%d).sql
```

---

## Troubleshooting Avançado

### P: Erro "Connection refused" no banco
**R:** Verifique se MySQL está rodando:
- **Windows:** Services > MySQL
- **Mac:** System Preferences > MySQL
- **Linux:** `sudo systemctl start mysql`

### P: Erro "Access denied" no MySQL
**R:** Verifique credenciais em `.env`:
- Username correto
- Password correta
- Host correto (localhost)

### P: Erro "No such table: books"
**R:** Execute este código Python:
```python
python
from app import create_app
app = create_app()
```

### P: Como ver os logs de erro?
**R:** Os erros aparecem no terminal onde você rodou `python run.py`

### P: Posso usar em produção?
**R:** Não recomendado. Para produção:
- Use Gunicorn em vez de Flask dev server
- Configure HTTPS
- Use variáveis de ambiente seguras
- Implemente autenticação

---

## Desenvolvimento

### P: Como adicionar um novo campo ao livro?
**R:** Edite `app/models.py` e adicione a coluna. Exemplo:
```python
isbn = db.Column(db.String(20))
```

### P: Posso adicionar novos idiomas?
**R:** Sim, criando templates separados para cada idioma

### P: Como fazer um fork/contribuir?
**R:** 
1. Faça uma cópia do projeto
2. Crie uma branch nova
3. Faça suas alterações
4. Teste tudo
5. Compartilhe as melhorias

---

## Contato e Suporte

### P: Encontrei um bug, o que faço?
**R:** 
1. Anote os passos para reproduzir
2. Verifique a versão do Python/MySQL
3. Tente reproduzir o erro
4. Reporte os detalhes

### P: Tenho uma sugestão de funcionalidade
**R:** Ótimo! Você pode:
- Implementar você mesmo
- Reportar a ideia
- Colaborar no desenvolvimento

---

## Links Úteis

- **Python:** https://www.python.org/
- **Flask:** https://flask.palletsprojects.com/
- **MySQL:** https://www.mysql.com/
- **SQLAlchemy:** https://www.sqlalchemy.org/
- **VS Code:** https://code.visualstudio.com/

---

**Ainda com dúvidas?** Consulte o README.md ou tente:
```bash
python check_setup.py
```

**Não encontrou sua pergunta?** Sugira no projeto! 💡
