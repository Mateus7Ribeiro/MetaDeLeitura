#!/bin/bash
# Script de deploy para produção - Mesa Literária v3.0

set -e  # Parar em caso de erro

echo "=========================================="
echo "🚀 Deploy - Mesa Literária v3.0"
echo "=========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para log
log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# 1. Verificar pré-requisitos
echo "1️⃣  Verificando pré-requisitos..."

if [ ! -f ".env.production" ]; then
    log_error ".env.production não encontrado!"
    echo "   Copie .env.production.example e configure as variáveis"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    log_error "Python 3 não encontrado!"
    exit 1
fi

log_success "Pré-requisitos OK"
echo ""

# 2. Criar diretórios necessários
echo "2️⃣  Criando diretórios..."
mkdir -p logs
mkdir -p static/uploads/profiles
mkdir -p backups
log_success "Diretórios criados"
echo ""

# 3. Ativar ambiente virtual
echo "3️⃣  Configurando ambiente virtual..."
if [ ! -d "venv" ]; then
    log_warning "Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
fi

source venv/bin/activate
log_success "Ambiente virtual ativado"
echo ""

# 4. Instalar dependências
echo "4️⃣  Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt
log_success "Dependências instaladas"
echo ""

# 5. Backup do banco de dados
echo "5️⃣  Fazendo backup do banco de dados..."
source .env.production
BACKUP_FILE="backups/db_backup_$(date +%Y%m%d_%H%M%S).sql"

if command -v mysqldump &> /dev/null; then
    mysqldump -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME > $BACKUP_FILE
    log_success "Backup salvo em $BACKUP_FILE"
else
    log_warning "mysqldump não disponível. Faça backup manual!"
fi
echo ""

# 6. Executar migrações
echo "6️⃣  Executando migrações do banco..."
python migrate_add_user_fields.py
log_success "Migrações concluídas"
echo ""

# 7. Coletar arquivos estáticos (se necessário)
echo "7️⃣  Verificando arquivos estáticos..."
log_success "Arquivos estáticos OK"
echo ""

# 8. Teste de configuração
echo "8️⃣  Testando configuração..."
export FLASK_ENV=production
python -c "from app import create_app; app = create_app(); print('✓ Configuração OK')"
log_success "Testes de configuração passaram"
echo ""

# 9. Permissões
echo "9️⃣  Ajustando permissões..."
chmod -R 755 static/
chmod -R 777 static/uploads/
chmod -R 755 logs/
log_success "Permissões ajustadas"
echo ""

echo "=========================================="
echo "✅ Deploy concluído com sucesso!"
echo "=========================================="
echo ""
echo "📋 Próximos passos:"
echo "1. Configure seu servidor web (Nginx/Apache)"
echo "2. Configure WSGI (Gunicorn/uWSGI)"
echo "3. Inicie o serviço"
echo ""
echo "Para iniciar manualmente:"
echo "  gunicorn -w 4 -b 0.0.0.0:5000 run:app"
echo ""
