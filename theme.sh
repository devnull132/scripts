#!/bin/bash

WALLPAPER_DIR="/home/daniil/Walp/"

# Функция для установки обоев в GNOME
set_wallpaper() {
    local wallpaper="$1"
    
    if [ -n "$wallpaper" ]; then
        # Устанавливаем обои для GNOME
        gsettings set org.gnome.desktop.background picture-uri "file://$wallpaper"
        gsettings set org.gnome.desktop.background picture-uri-dark "file://$wallpaper"
        gsettings set org.gnome.desktop.screensaver picture-uri "file://$wallpaper"
        
        # Опционально: для динамических обоев (GNOME 42+)
        # gsettings set org.gnome.desktop.background picture-options 'zoom'
        
        # Если установлен wal, генерируем цветовую схему
        if command -v wal >/dev/null; then
            wal -i "$wallpaper" -n
            
            # Применяем цвета к GNOME терминалу (если используется)
            if [ -f ~/.cache/wal/colors.sh ] && [ -f ~/.cache/wal/sequences ]; then
                . ~/.cache/wal/colors.sh
                # Можно добавить применение цветов к другим GNOME компонентам
            fi
        fi
    fi
}

# Проверяем существование директории
if [ -d "$WALLPAPER_DIR" ]; then
    # Если передан аргумент
    if [ $# -gt 0 ]; then
        # Проверяем каждый аргумент
        for arg in "$@"; do
            # Убираем возможный дефис в начале
            filename="${arg#-}"
            wallpaper_path="$WALLPAPER_DIR$filename"
            
            if [ -f "$wallpaper_path" ]; then
                set_wallpaper "$wallpaper_path"
                echo "Обои установлены: $filename"
                exit 0
            else
                echo "Файл не найден: $wallpaper_path"
                exit 1
            fi
        done
    else
        # Если аргументов нет - случайный выбор
        RANDOM_WALLPAPER=$(find "$WALLPAPER_DIR" -type f \( -name '*.jpg' -o -name '*.png' -o -name '*.jpeg' -o -name '*.webp' \) | shuf -n 1)
        
        if [ -n "$RANDOM_WALLPAPER" ]; then
            set_wallpaper "$RANDOM_WALLPAPER"
            echo "Случайные обои установлены: $(basename "$RANDOM_WALLPAPER")"
        else
            echo "Не найдено файлов обоев в директории: $WALLPAPER_DIR"
            exit 1
        fi
    fi
else
    echo "Директория с обоями не найдена: $WALLPAPER_DIR"
    exit 1
fi
