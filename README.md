# 📚 Mesa Literária

Sistema web para controlar suas metas de leitura. Cadastre seus livros, defina datas de conclusão e o sistema calculará quantas páginas você precisa ler por dia para atingir sua meta.

## 🎯 Funcionalidades

- ✅ Cadastrar livros com total de páginas
- ✅ Registrar progresso de leitura (páginas ou percentual)
- ✅ Definir data limite para conclusão
- ✅ Calcular automaticamente páginas/dia necessárias
- ✅ Visualizar progresso com barras de progresso
- ✅ Editar e deletar livros
- ✅ Interface web responsiva
- ✅ Persistência em banco de dados MySQL

## 🛠️ Pré-requisitos

- Python 3.8+
- MySQL 5.7+
- pip (gerenciador de pacotes Python)

## 📦 Instalação

### 1. Clone ou extraia o projeto

```bash
cd c:\PROJETOS\Python\MetaDeLeitura
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
# No Windows
venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

#### 4.1 Crie o banco de dados no MySQL

```sql
CREATE DATABASE meta_leitura;
```

#### 4.2 Configure as variáveis de ambiente

Edite o arquivo `.env` na raiz do projeto:

```env
# Configuração do Banco de Dados
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_HOST=localhost
DB_PORT=3306
DB_NAME=meta_leitura

# Configuração do Flask
SECRET_KEY=sua_chave_secreta_aqui
FLASK_ENV=development
FLASK_DEBUG=True
```

## 🚀 Como executar

```bash
python run.py
```

O aplicativo estará disponível em: `http://localhost:5000`

## 📖 Como usar

1. **Cadastrar um Livro**
   - Clique em "+ Novo Livro"
   - Preencha o nome do livro, total de páginas, páginas atuais (opcional) e data limite
   - Clique em "Cadastrar Livro"

2. **Acompanhar Progresso**
   - Na página inicial, visualize todos os seus livros
   - Veja a barra de progresso e o percentual lido
   - Observe quantas páginas precisa ler por dia

3. **Editar Progresso**
   - Clique em "Editar" no livro desejado
   - Atualize as páginas lidas atualmente
   - Salve as alterações

4. **Visualizar Detalhes**
   - Clique em "Detalhes" para ver informações completas
   - Veja a meta diária de páginas
   - Acompanhe dias restantes até a data limite

## 📊 Estrutura do Projeto

```
MetaDeLeitura/
├── app/
│   ├── __init__.py           # Inicialização da aplicação Flask
│   ├── config.py              # Configurações da aplicação
│   ├── models.py              # Modelos do banco de dados
│   └── routes.py              # Rotas e views
├── templates/
│   ├── base.html              # Template base
│   ├── index.html             # Página inicial
│   ├── add_book.html          # Cadastro de livro
│   ├── edit_book.html         # Edição de livro
│   └── book_detail.html       # Detalhes do livro
├── static/
│   ├── css/
│   │   └── style.css          # Estilos CSS
│   └── js/
│       └── script.js          # Scripts JavaScript
├── .env                       # Variáveis de ambiente
├── requirements.txt           # Dependências Python
├── run.py                     # Arquivo principal
└── README.md                  # Este arquivo
```

## 🗄️ Banco de Dados

### Tabela: books

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT | ID do livro (PK) |
| name | VARCHAR(255) | Nome do livro |
| total_pages | INT | Total de páginas |
| current_page | INT | Páginas lidas atualmente |
| current_percentage | FLOAT | Percentual lido |
| target_date | DATETIME | Data limite |
| created_at | DATETIME | Data de criação |
| updated_at | DATETIME | Data da última atualização |
| is_completed | BOOLEAN | Livro concluído? |

## 🧮 Cálculos

### Páginas por Dia
```
Páginas por Dia = Páginas Restantes / Dias Restantes
```

### Percentual de Leitura
```
Percentual = (Páginas Lidas / Total de Páginas) × 100
```

## 🔧 API Endpoints

- `GET /` - Página inicial
- `GET /add` - Formulário de novo livro
- `POST /add` - Criar novo livro
- `GET /book/<id>` - Visualizar detalhes do livro
- `GET /book/<id>/edit` - Formulário de edição
- `POST /book/<id>/edit` - Atualizar livro
- `POST /book/<id>/delete` - Deletar livro
- `GET /api/books` - Lista de livros (JSON)
- `GET /api/book/<id>` - Dados do livro (JSON)
- `POST /api/book/<id>/update-progress` - Atualizar progresso (JSON)

## 🛡️ Segurança

- Proteção CSRF em formulários
- Validação de entrada
- Tratamento de exceções
- Variáveis sensíveis em arquivo `.env`

## 🐛 Troubleshooting

### Erro de conexão com banco de dados
- Verifique se o MySQL está rodando
- Confirme as credenciais em `.env`
- Verifique se o banco de dados foi criado

### Porta 5000 já está em uso
- Altere a porta em `run.py` ou use:
```bash
python run.py --port 5001
```

### Módulos não encontrados
- Ative o ambiente virtual
- Execute `pip install -r requirements.txt` novamente

## 📝 Notas

- O sistema calcula automaticamente o progresso em percentual baseado nas páginas
- Datas passadas não são permitidas no cadastro
- Livros completados ficam marcados visualmente como "Concluído"

## 📄 Licença

Este projeto é de uso livre.

## 👤 Autor

Sistema desenvolvido para controle de metas de leitura pessoais.

---

**Dúvidas ou sugestões?** Sinta-se livre para expandir o projeto com novas funcionalidades!
