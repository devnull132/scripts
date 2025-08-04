import os
import random
import pygame
import time
from pygame import mixer
import sys
import select
from mutagen import File
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.easyid3 import EasyID3

def setup_colors():
    try:
        import colorama
        colorama.init()
        return True
    except:
        return False

COLOR_SUPPORT = setup_colors()

def color_text(text, rgb):
    if not COLOR_SUPPORT:
        return text
    r, g, b = [int(x * 255) for x in rgb]
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_audio_files(directory):
    extensions = ('.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac')
    return [f for f in os.listdir(directory) if f.lower().endswith(extensions)]

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02d}"

def draw_progress_bar(current, total, width=30):
    progress = min(1.0, current / total)
    filled = int(width * progress)
    bar = "[" + "=" * filled + " " * (width - filled) + "]"
    return bar
def get_metadata(file_path):
    try:
        # Сначала пробуем прочитать как UTF-8
        try:
            audio = File(file_path)
            if file_path.lower().endswith('.mp3'):
                audio = EasyID3(file_path)
            
            artist = audio.get('artist', [None])[0]
            title = audio.get('title', [None])[0]
            
            if artist and title:
                return f"{artist} - {title}"
            elif title:
                return title
        except:
            pass
        
        # Если не получилось, пробуем Windows-1251 (для русских тегов)
        try:
            audio = File(file_path)
            if file_path.lower().endswith('.mp3'):
                audio = EasyID3(file_path)
                # Принудительно перекодируем из cp1251
                artist = audio.get('artist', [None])[0]
                title = audio.get('title', [None])[0]
                
                if artist:
                    artist = artist.encode('cp1251', errors='replace').decode('utf-8', errors='replace')
                if title:
                    title = title.encode('cp1251', errors='replace').decode('utf-8', errors='replace')
                
                if artist and title:
                    return f"{artist} - {title}"
                elif title:
                    return title
            return os.path.splitext(os.path.basename(file_path))[0]
        except:
            return os.path.splitext(os.path.basename(file_path))[0]
    except:
        return os.path.splitext(os.path.basename(file_path))[0]
def print_player_ui(song_name, current_pos, song_length, current_index, total_songs, volume, loop):
    display_name = song_name if len(song_name) < 40 else song_name[:37] + "..."
    pos_time = format_time(current_pos)
    len_time = format_time(song_length)
    track_count = f"{current_index + 1}/{total_songs}"
    progress_bar = draw_progress_bar(current_pos, song_length)
    
    title = color_text("♪ Сейчас играет:", (0.1, 0.7, 0.9))
    track_info = color_text(f"{display_name} {track_count}", (0.9, 0.6, 0.1))
    time_info = color_text(f"{pos_time}/{len_time}", (0.3, 0.8, 0.3))
    vol_info = color_text(f"🔊 {int(volume * 100)}%", (0.8, 0.8, 0.8))
    
    ui = [
        f"\n{title} {track_info}{' 🔁' if loop else ''}",
        f"{progress_bar} {time_info} {vol_info}"
    ]
    print("\n".join(ui))

def print_controls():
    controls = [
        ("n", "следующая"),
        ("p", "предыдущая"),
        ("s", "пауза"),
        ("+/-", "громкость"),
        ("l", "повтор"),
        ("r", "перемешать"),
        ("q", "выход")
    ]
    
    print(color_text("\nУправление:", (0.7, 0.7, 0.7)))
    for cmd, desc in controls:
        cmd_colored = color_text(cmd.ljust(6), (0.4, 0.8, 0.4))
        print(f" {cmd_colored} → {desc}")

def play_music(directory):
    pygame.init()
    mixer.init()
    audio_files = get_audio_files(directory)
    
    if not audio_files:
        print(color_text("🚫 Нет аудиофайлов в директории!", (1.0, 0.3, 0.3)))
        return
    
    random.shuffle(audio_files)
    current_index = 0
    playing = True
    paused = False
    volume = 0.7
    mixer.music.set_volume(volume)
    loop_current = False
    
    # Функция для воспроизведения текущего трека
    def play_current_track():
        nonlocal current_index
        current_file = os.path.join(directory, audio_files[current_index])
        try:
            sound = pygame.mixer.Sound(current_file)
            length = sound.get_length()
            mixer.music.load(current_file)
            mixer.music.play(loops=-1 if loop_current else 0)
            return length, get_metadata(current_file)
        except pygame.error as e:
            print(color_text(f"⚠ Ошибка: {e}", (1.0, 0.3, 0.3)))
            current_index = (current_index + 1) % len(audio_files)
            return 0, audio_files[current_index]
    
    song_length, song_name = play_current_track()
    last_update = 0
    
    while playing:
        current_time = time.time()
        if current_time - last_update >= 0.3:
            current_pos = mixer.music.get_pos() / 1000
            if current_pos < 0:
                current_pos = 0
            
            clear_screen()
            print_player_ui(
                song_name, current_pos, song_length,
                current_index, len(audio_files), volume, loop_current
            )
            print_controls()
            last_update = current_time
        
        # Проверка завершения трека
        if not loop_current and not paused and current_pos >= song_length - 0.5:
            current_index = (current_index + 1) % len(audio_files)
            song_length, song_name = play_current_track()
            continue
        
        # Обработка ввода
        cmd = None
        if os.name == 'posix':
            if select.select([sys.stdin], [], [], 0)[0]:
                cmd = sys.stdin.readline().strip().lower()
        else:
            import msvcrt
            if msvcrt.kbhit():
                cmd = msvcrt.getch().decode().lower()
        
        if cmd:
            if cmd == 'n':
                current_index = (current_index + 1) % len(audio_files)
                song_length, song_name = play_current_track()
            elif cmd == 'p':
                current_index = (current_index - 1) % len(audio_files)
                song_length, song_name = play_current_track()
            elif cmd == 's':
                paused = not paused
                if paused:
                    mixer.music.pause()
                else:
                    mixer.music.unpause()
            elif cmd == '+':
                volume = min(1.0, volume + 0.1)
                mixer.music.set_volume(volume)
            elif cmd == '-':
                volume = max(0.0, volume - 0.1)
                mixer.music.set_volume(volume)
            elif cmd == 'l':
                loop_current = not loop_current
                mixer.music.play(loops=-1 if loop_current else 0)
            elif cmd == 'r':
                random.shuffle(audio_files)
                current_index = 0
                song_length, song_name = play_current_track()
            elif cmd == 'q':
                playing = False
        
        time.sleep(0.05)
    
    mixer.music.stop()
    mixer.quit()
    pygame.quit()

if __name__ == "__main__":
    clear_screen()
    print(color_text("=== Музыкальный Плеер ===", (0.1, 0.7, 0.9)))
    
    default_dir = "/home/daniil/music"
    directory = input(f"Путь к музыке [по умолчанию: {default_dir}]: ").strip()
    directory = directory or default_dir
    
    if not os.path.isdir(directory):
        print(color_text(f"🚫 Директория '{directory}' не найдена!", (1.0, 0.3, 0.3)))
    else:
        play_music(directory)
