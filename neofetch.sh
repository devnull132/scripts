#!/bin/bash

# Путь к папке с конфигами neofetch
CONFIG_DIR="/home/daniil/.config/neofetch"

# Проверяем, существует ли папка
if [ ! -d "$CONFIG_DIR" ]; then
    echo "Ошибка: папка $CONFIG_DIR не существует"
    exit 1
fi

# Ищем все файлы .conf в папке
CONFIG_FILES=("$CONFIG_DIR"/*.conf)

# Проверяем, есть ли файлы .conf
if [ ${#CONFIG_FILES[@]} -eq 0 ]; then
    echo "Ошибка: в папке $CONFIG_DIR нет файлов .conf"
    exit 1
fi

# Выбираем случайный файл
RANDOM_CONFIG="${CONFIG_FILES[RANDOM % ${#CONFIG_FILES[@]}]}"

# Запускаем neofetch с выбранным конфигом
neofetch --config "$RANDOM_CONFIG"
