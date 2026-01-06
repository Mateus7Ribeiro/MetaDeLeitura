#!/bin/bash
# Script de backup para Meta de Leitura v3.0

set -e

# Configurações
BACKUP_DIR="/var/www/MetaDeLeitura/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "🔄 Backup - Meta de Leitura v3.0"
echo "=========================================="
echo ""

# Carregar variáveis de ambiente
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

# 1. Backup do banco de dados
echo -e "${YELLOW}1️⃣  Fazendo backup do banco de dados...${NC}"
BACKUP_DB="$BACKUP_DIR/db_$DATE.sql.gz"

if mysqldump -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME | gzip > $BACKUP_DB; then
    echo -e "${GREEN}✓ Backup do banco salvo: $BACKUP_DB${NC}"
    echo "   Tamanho: $(du -h $BACKUP_DB | cut -f1)"
else
    echo "✗ Erro ao fazer backup do banco!"
    exit 1
fi

# 2. Backup de uploads
echo ""
echo -e "${YELLOW}2️⃣  Fazendo backup de uploads...${NC}"
BACKUP_UPLOADS="$BACKUP_DIR/uploads_$DATE.tar.gz"

if tar -czf $BACKUP_UPLOADS static/uploads/; then
    echo -e "${GREEN}✓ Backup de uploads salvo: $BACKUP_UPLOADS${NC}"
    echo "   Tamanho: $(du -h $BACKUP_UPLOADS | cut -f1)"
else
    echo "✗ Erro ao fazer backup de uploads!"
    exit 1
fi

# 3. Backup de configuração
echo ""
echo -e "${YELLOW}3️⃣  Fazendo backup de configuração...${NC}"
BACKUP_CONFIG="$BACKUP_DIR/config_$DATE.tar.gz"

if tar -czf $BACKUP_CONFIG .env app/config.py; then
    echo -e "${GREEN}✓ Backup de configuração salvo: $BACKUP_CONFIG${NC}"
else
    echo "⚠ Aviso: Erro ao fazer backup de configuração"
fi

# 4. Limpeza de backups antigos
echo ""
echo -e "${YELLOW}4️⃣  Limpando backups antigos (>${RETENTION_DAYS} dias)...${NC}"
DELETED=$(find $BACKUP_DIR -name "*.gz" -mtime +$RETENTION_DAYS -delete -print | wc -l)
echo -e "${GREEN}✓ Removidos $DELETED arquivo(s) antigo(s)${NC}"

# 5. Resumo
echo ""
echo "=========================================="
echo "✅ Backup concluído com sucesso!"
echo "=========================================="
echo ""
echo "📊 Resumo:"
echo "  Data: $(date '+%d/%m/%Y %H:%M:%S')"
echo "  Localização: $BACKUP_DIR"
echo "  Arquivos:"
ls -lh $BACKUP_DIR/*$DATE* | awk '{print "    - " $9 " (" $5 ")"}'
echo ""
echo "💾 Espaço em disco:"
df -h $BACKUP_DIR | tail -1 | awk '{print "  Usado: " $3 " / " $2 " (" $5 ")"}'
echo ""
