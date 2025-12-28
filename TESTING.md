# 🧪 Guia de Teste - Sistema de Usuários

## ✅ Checklist de Testes

### 1. Autenticação Básica

#### Teste: Criar Conta
- [ ] Acesse http://localhost:5000
- [ ] Clique em "Registrar"
- [ ] Preencha: username, email, senha
- [ ] Clique em "Criar Conta"
- [ ] Sistema redireciona para login

#### Teste: Login
- [ ] Na página de login, insira credenciais
- [ ] Clique em "Login"
- [ ] Você é redirecionado para dashboard
- [ ] Navbar mostra seu nome de usuário

#### Teste: Logout
- [ ] Clique em "Sair" na navbar
- [ ] Você é redirecionado para login
- [ ] Sessão é limpada

### 2. Proteção de Rotas

#### Teste: Acesso sem Login
- [ ] Limpe cookies (ou use navegação privada)
- [ ] Tente acessar http://localhost:5000/
- [ ] Sistema redireciona para login

#### Teste: Acesso Protegido
- [ ] Faça login
- [ ] Tente direto: /add, /book/1, /settings
- [ ] Todas funcionam (se existem)
- [ ] Sem login, todas redirecionam para login

### 3. Isolamento de Dados

#### Setup:
Crie dois usuários: `alice` e `bob`

#### Teste: Alice não vê livros de Bob
1. Faça login como **Alice**
2. Cadastre um livro: "Harry Potter"
3. Veja na dashboard (aparece)
4. Faça logout
5. Faça login como **Bob**
6. Na dashboard, não vê "Harry Potter" ✓
7. Tente acessar direto: http://localhost:5000/book/1
8. Erro 403: "Acesso negado" ✓

#### Teste: Bob não pode editar livro de Alice
1. Continue como **Bob**
2. Tente: http://localhost:5000/book/1/edit
3. Erro 403 ✓

#### Teste: Bob não pode deletar livro de Alice
1. Continue como **Bob**
2. Tente: POST /book/1/delete
3. Erro 403 ✓

### 4. Velocidade de Leitura

#### Teste: Configurar Velocidade
1. Faça login
2. Clique em "⚙️ Configurações"
3. Mude "Tempo Médio por Página" para **2.0**
4. Clique "Salvar Configurações"
5. Mensagem "Configurações salvas com sucesso!" ✓

#### Teste: Aplicar em Cálculos
1. Crie um livro:
   - Nome: "Teste"
   - Total de páginas: 100
   - Páginas atuais: 0
   - Data: 10 dias de agora

2. Clique em "Detalhes"
3. Observe:
   - Páginas por dia: ~10
   - Tempo diário de leitura: ~20 minutos ✓

#### Teste: Recalcular com Mudança
1. Volte para "Configurações"
2. Mude velocidade para **3.0**
3. Volte para "Detalhes" do livro
4. Tempo diário agora deve ser: ~30 minutos ✓

#### Teste: Cada usuário tem velocidade diferente
1. Alice: Configure 2.0
2. Bob: Configure 4.0
3. Ambos criam livro igual (10 páginas/dia)
4. Alice: 20 minutos
5. Bob: 40 minutos ✓

### 5. Formulários e Validações

#### Teste: Registro - Campos Obrigatórios
- [ ] Tente deixar campo em branco
- [ ] Mensagem de erro aparece

#### Teste: Registro - Email Duplicado
- [ ] Registre: `teste@email.com`
- [ ] Tente registrar novamente
- [ ] Erro: "Email já está registrado" ✓

#### Teste: Registro - Username Duplicado
- [ ] Registre: `usuario1`
- [ ] Tente registrar novamente
- [ ] Erro: "Nome de usuário já existe" ✓

#### Teste: Login - Credenciais Inválidas
- [ ] Username correto, senha errada
- [ ] Erro: "Username ou senha incorretos" ✓

#### Teste: Configurações - Velocidade Inválida
- [ ] Tente inserir número negativo
- [ ] Erro: "Velocidade deve ser maior que 0" ✓

### 6. Interface

#### Teste: Navbar com Usuário
- [ ] Faça login
- [ ] Navbar mostra: 👤 username | ⚙️ Configurações | Meus Livros | + Novo Livro | Sair ✓

#### Teste: Navbar sem Usuário
- [ ] Faça logout
- [ ] Navbar mostra: Login | Registrar ✓

#### Teste: Página de Erro
- [ ] Tente acessar /book/999 (não existe)
- [ ] Erro 404 com link para voltar ✓

#### Teste: Página de Acesso Negado
- [ ] Create livro como Alice
- [ ] Login como Bob
- [ ] Tente acessar livro de Alice
- [ ] Página com mensagem "Acesso negado" ✓

### 7. API

#### Teste: GET /api/books
1. Faça login
2. Acesse: http://localhost:5000/api/books
3. Retorna JSON com SEUS livros
4. Se muda usuário, lista é diferente ✓

#### Teste: GET /api/book/<id>
1. Seu livro: Funciona
2. Livro de outro: Erro 403 JSON ✓

#### Teste: POST /api/book/<id>/update-progress
1. Seu livro: Funciona
2. Livro de outro: Erro 403 JSON ✓

---

## 🧪 Teste de Carga

### Múltiplos Usuários
Crie 5 usuários diferentes com velocidades diferentes:

```
Ana: 1.5 min/página
João: 2.5 min/página
Maria: 3.5 min/página
Pedro: 4.0 min/página
Lucas: 2.0 min/página
```

Crie 3 livros iguais para todos:
- 300 páginas
- 0 páginas lidas
- 30 dias

Verifique que tempo diário é diferente para cada um.

---

## 🐛 Teste de Edge Cases

### Teste: Zero Dias Restantes
1. Crie livro com data de conclusão = hoje
2. Veja os cálculos (deve dividir por 1 ou 0)
3. Tempo deve ser realista

### Teste: Data no Passado
1. Tente criar livro com data no passado
2. Sistema rejeita (validação) ✓

### Teste: Múltiplas Abas
1. Abra 2 abas
2. Faça login em uma
3. A outra deve reconhecer a sessão
4. Faça logout em uma
5. Ambas ficam deslogadas ✓

### Teste: Cookies Expirados
1. Espere até a sessão expirar (7 dias)
2. Tente usar a app
3. Redireciona para login ✓

---

## 📊 Teste de Performance

### Teste: Velocidade de Página
- [ ] Login: < 1 segundo
- [ ] Dashboard: < 2 segundos
- [ ] Configurações: < 1 segundo
- [ ] Criar livro: < 2 segundos

### Teste: Banco de Dados
- Com 100 livros, dashboard carrega normalmente?
- API retorna em < 500ms?

---

## ✨ Testes Visuais

- [ ] Login page parece profissional
- [ ] Register page é clara
- [ ] Settings page é intuitiva
- [ ] Navbar é responsivo (mobile/desktop)
- [ ] Cores estão consistentes
- [ ] Textos são legíveis

---

## 🎯 Checklist Final

Marque como ✅ quando passar:

- [ ] Registro funciona
- [ ] Login funciona
- [ ] Logout funciona
- [ ] Isolamento de dados funciona
- [ ] Velocidade de leitura funciona
- [ ] Cálculos usam velocidade correta
- [ ] Rótulo está correto ("Tempo Diário de Leitura")
- [ ] Todas as validações funcionam
- [ ] API funciona com isolamento
- [ ] Interface é responsiva
- [ ] Não há erros no console
- [ ] Não há erros no Flask log

---

## 📝 Relatório de Testes

Ao encontrar um bug, documente:

```
Bug #1: [Descrição]
- Passos para reproduzir:
  1. ...
  2. ...
  3. ...
- Resultado esperado: ...
- Resultado obtido: ...
- Browser/OS: ...
- Severidade: [ ] Crítica [ ] Alta [ ] Média [ ] Baixa
```

---

**Boa sorte com os testes!** 🚀
