#!/bin/bash

# Параметры
USER="daniil"
BACKUP_DIR="/home/$USER/backups"
SOURCE_DIRS=(
    "/home/$USER/Minecraft Server"
    "/home/$USER/Projects"
    "/home/$USER/.hmcl.json"
    "/home/$USER/.minecraft"
    "/home/$USER/HMCL-3.6.12.jar"
    "/home/daniil/.local/share/hmcl"
    "/home/daniil/.config"
    "/home/daniil/Walp"
)
TG_BOT_SCRIPT="/home/$USER/Backup_bot/main.py"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_PREFIX="$BACKUP_DIR/backup_$DATE.tar.gz.part_"

# Исключаем временные файлы
EXCLUDE_PATTERNS=(
    "--exclude=*.tmp"
    "--exclude=*.log"
    "--exclude=*/cache/*"
    "--exclude=*/logs/*"
    "--exclude=*/temp/*"
)

# Создаем директорию для бэкапов
mkdir -p "$BACKUP_DIR" || { echo "Failed to create backup directory"; exit 1; }

# Создаем многотомный архив
echo "Creating split backup..."
tar -cz "${EXCLUDE_PATTERNS[@]}" "${SOURCE_DIRS[@]}" 2>/dev/null | \
split -b 45M - "$BACKUP_PREFIX"

# Проверяем созданные части
parts=($(ls ${BACKUP_PREFIX}*))
if [ ${#parts[@]} -eq 0 ]; then
    echo "Backup creation failed!"
    exit 1
fi

# Отправляем каждую часть
for part in "${parts[@]}"; do
    echo "Sending part: $part"
    if ! python3 "$TG_BOT_SCRIPT" "$part"; then
        echo "Failed to send part: $part"
        # Можно добавить повторную попытку
        sleep 5
        python3 "$TG_BOT_SCRIPT" "$part" || echo "Failed again: $part"
    fi
done

# Удаляем старые бэкапы (сохраняем последние 5 комплектов)
echo "Cleaning old backups..."
cd "$BACKUP_DIR" || exit
# Удаляем все, кроме 5 последних наборов частей
ls | grep -Po 'backup_.*(?=\.part_)' | sort -u | head -n -5 | while read -r prefix; do
    rm -f "${prefix}".part_*
done
