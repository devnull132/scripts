WALLPAPER_DIR="/home/daniil/Walp/"
if [ -d "$WALLPAPER_DIR" ]; then
    # Выбираем случайные обои
    RANDOM_WALLPAPER=$(find "$WALLPAPER_DIR" -type f \( -name '*.jpg' -o -name '*.png' -o -name '*.jpeg' \) | shuf -n 1)
    
    if [ -n "$RANDOM_WALLPAPER" ]; then
        feh --bg-fill "$RANDOM_WALLPAPER"
        
        if command -v wal >/dev/null; then
            wal -i "$RANDOM_WALLPAPER" -n
        fi
        
        if [ -f ~/.cache/wal/colors.sh ]; then
            . ~/.cache/wal/colors.sh
            bspc config normal_border_color "$color0"
            bspc config active_border_color "$color1"
            bspc config focused_border_color "$color2"
            bspc config presel_feedback_color "$color3"
        fi
    fi
fi
