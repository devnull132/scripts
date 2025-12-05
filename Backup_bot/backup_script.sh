
#!/bin/bash

# =============================================
# КОНФИГУРАЦИЯ
# =============================================
USER="daniil"
BACKUP_DIR="/home/$USER/backups"
LOG_DIR="/home/$USER/backups/logs"
LOG_FILE="$LOG_DIR/backup_$(date +%Y-%m-%d_%H-%M-%S).log"

# Директории и файлы для бэкапа
SOURCE_DIRS=(
    "/home/$USER/Minecraft Server"
    "/home/$USER/Projects"
    "/home/$USER/.hmcl.json"
    "/home/$USER/.minecraft"
    "/home/$USER/HMCL-3.7.3.jar"
    "/home/daniil/.local/share/hmcl"
)

# Исключения
EXCLUDE_PATTERNS=(
    "--exclude=*.tmp"
    "--exclude=*.log"
    "--exclude=*/cache/*"
    "--exclude=*/logs/*"
    "--exclude=*/temp/*"
    "--exclude=*.lock"
    "--exclude=*/session.lock"
    "--exclude=*/world/session.lock"
    "--exclude=*/crash-reports/*"
    "--exclude=*/debug/*"
)

TG_BOT_SCRIPT="/home/$USER/Backup_bot/main.py"
MAX_RETRIES=3  # Количество повторных попыток отправки
RETRY_DELAY=10  # Задержка между повторными попытками (секунды)

# Настройки архивации
MAX_SPLIT_SIZE="45M"  # Размер частей архива
BACKUPS_TO_KEEP=5  # Сколько наборов бэкапов хранить

# =============================================
# ФУНКЦИИ
# =============================================

log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" | tee -a "$LOG_FILE"
}

check_error() {
    if [ $? -ne 0 ]; then
        log "ОШИБКА: $1"
        exit 1
    fi
}

send_file_with_retry() {
    local files=("$@")
    local attempt=1
    
    while [ $attempt -le $MAX_RETRIES ]; do
        log "Попытка $attempt/$MAX_RETRIES отправки ${#files[@]} файлов..."
        
        # Отправляем все файлы одним вызовом Python-скрипта
        if python3 "$TG_BOT_SCRIPT" "${files[@]}"; then
            log "✅ Все файлы успешно отправлены"
            return 0
        else
            log "❌ Ошибка отправки файлов (попытка $attempt)"
            
            if [ $attempt -lt $MAX_RETRIES ]; then
                log "⏳ Ожидание $RETRY_DELAY секунд перед следующей попыткой..."
                sleep $RETRY_DELAY
            fi
            attempt=$((attempt + 1))
        fi
    done
    
    log "⚠️ Не удалось отправить файлы после $MAX_RETRIES попыток"
    return 1
}

# =============================================
# ОСНОВНОЙ СКРИПТ
# =============================================

# Настройка логгирования
mkdir -p "$BACKUP_DIR" "$LOG_DIR"
touch "$LOG_FILE"

log "🚀 Запуск процесса бэкапа $(date '+%Y-%m-%d %H:%M:%S')"

# Проверка скрипта бота
if [ ! -f "$TG_BOT_SCRIPT" ]; then
    check_error "Скрипт бота не найден: $TG_BOT_SCRIPT"
fi

# Создание архива
DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_PREFIX="$BACKUP_DIR/backup_$DATE.tar.gz.part_"

log "📦 Создание архива..."

# Создание временного файла списка
TMP_LIST=$(mktemp)
for source in "${SOURCE_DIRS[@]}"; do
    if [ -e "$source" ]; then
        echo "$source"
    fi
done > "$TMP_LIST"

# Создание многотомного архива
tar -cz "${EXCLUDE_PATTERNS[@]}" \
    --files-from="$TMP_LIST" \
    --ignore-failed-read \
    2>/dev/null | \
split -b "$MAX_SPLIT_SIZE" - "$BACKUP_PREFIX"

TAR_EXIT_CODE=${PIPESTATUS[0]}
rm "$TMP_LIST"

if [ $TAR_EXIT_CODE -ne 0 ] && [ $TAR_EXIT_CODE -ne 1 ]; then
    check_error "Создание архива завершилось с ошибкой (код: $TAR_EXIT_CODE)"
fi

# Проверка созданных частей
parts=($(ls ${BACKUP_PREFIX}* 2>/dev/null | sort -V))
if [ ${#parts[@]} -eq 0 ]; then
    check_error "Не удалось создать части архива!"
fi

log "✅ Архив создан. Частей: ${#parts[@]}"

# Отправка ВСЕХ частей одним вызовом
log "📤 Отправка всех частей в Telegram..."
if send_file_with_retry "${parts[@]}"; then
    log "✅ Все части успешно отправлены!"
    
    # Удаление отправленных частей
    log "🗑️ Удаление отправленных частей с диска..."
    rm -f "${parts[@]}"
else
    log "❌ Не удалось отправить все части"
    # Можно сохранить список неудачных частей для повторной попытки
    FAILED_PARTS_FILE="$BACKUP_DIR/failed_parts_$DATE.txt"
    printf "%s\n" "${parts[@]}" > "$FAILED_PARTS_FILE"
    log "Список частей сохранен в: $FAILED_PARTS_FILE"
fi

# Очистка старых бэкапов
log "🧹 Очистка старых бэкапов..."
cd "$BACKUP_DIR" || exit

backup_prefixes=$(ls backup_*.part_* 2>/dev/null | grep -Po 'backup_.*(?=\.part_)' | sort -u | head -n -$BACKUPS_TO_KEEP)

if [ -n "$backup_prefixes" ]; then
    echo "$backup_prefixes" | while read -r prefix; do
        log "Удаление: $prefix*"
        rm -f "${prefix}".part_*
    done
fi

log "========================================"
log "📊 Бэкап завершен: ${#parts[@]} частей"
log "Логи сохранены в: $LOG_FILE"

