#!/bin/bash

WALLPAPER_DIR="/home/daniil/Walp/"
# Функция для установки обоев
set_wallpaper() {
    local wallpaper="$1"
    
    if [ -n "$wallpaper" ]; then
        feh --bg-fill "$wallpaper"
        
        if command -v wal >/dev/null; then
            wal -i "$wallpaper" -n
        fi
        
        if [ -f ~/.cache/wal/colors.sh ]; then
            . ~/.cache/wal/colors.sh
            bspc config normal_border_color "$color0"
            bspc config active_border_color "$color1"
            bspc config focused_border_color "$color2"
            bspc config presel_feedback_color "$color3"
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
                exit 0
            else
                echo "Файл не найден: $wallpaper_path"
                exit 1
            fi
        done
    else
        # Если аргументов нет - случайный выбор
        RANDOM_WALLPAPER=$(find "$WALLPAPER_DIR" -type f \( -name '*.jpg' -o -name '*.png' -o -name '*.jpeg' \) | shuf -n 1)
        
        if [ -n "$RANDOM_WALLPAPER" ]; then
            set_wallpaper "$RANDOM_WALLPAPER"
        fi
    fi
else
    echo "Директория с обоями не найдена: $WALLPAPER_DIR"
    exit 1
fi
