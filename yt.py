import yt_dlp
import os

def download_youtube_video(url, output_path="/home/daniil/downloads_yt"):
    """
    Скачивает видео с YouTube используя yt-dlp
    """
    try:
        # Создаем папку для загрузок
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Настройки для загрузки
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Получаем информацию о видео
            info = ydl.extract_info(url, download=False)
            print(f"Название: {info.get('title', 'Неизвестно')}")
            print(f"Автор: {info.get('uploader', 'Неизвестно')}")
            print(f"Длительность: {info.get('duration', 0)} секунд")
            print(f"Просмотров: {info.get('view_count', 0)}")
            
            # Скачиваем видео
            print("Начинаем загрузку...")
            ydl.download([url])
            
        print(f"Видео успешно скачано в папку: {output_path}")
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пример использования
if __name__ == "__main__":
    video_url = input("Введите ссылку на YouTube видео: ")
    download_youtube_video(video_url)
