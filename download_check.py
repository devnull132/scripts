import os 
def check_files():
    files_tg = os.listdir(path="/home/daniil/Downloads/Telegram Desktop")
    for file in files_tg:
        if ".png" in file or ".jpg" in file or ".avif" in file or ".jpeg" in file:
            os.system(f"mv '/home/daniil/Downloads/Telegram Desktop/{file}' '/home/daniil/Imgs/{file}'")
        elif ".mp4" in file:
            os.system(f"mv '/home/daniil/Downloads/Telegram Desktop/{file}' '/home/daniil/Video/{file}'")
        elif ".pdf" in file or ".txt" in file or ".md" in file:
            os.system(f"mv '/home/daniil/Downloads/Telegram Desktop/{file}' '/home/daniil/Docs/{file}'")
    files_download = os.listdir(path="/home/daniil/Downloads")
    for file in files_download:
        if ".png" in file or ".jpg" in file or ".avif" in file or ".jpeg" in file:
            os.system(f"mv '/home/daniil/Downloads/{file}' '/home/daniil/Imgs/{file}'")
        elif ".mp4" in file:
            os.system(f"mv '/home/daniil/Downloads/{file}' '/home/daniil/Video/{file}'")
        elif ".pdf" in file or ".txt" in file or ".md" in file:
            os.system(f"mv '/home/daniil/Downloads/{file}' '/home/daniil/Docs/{file}'")
    files_home = os.listdir(path="/home/daniil")
    for file in files_home:
        if ".png" in file or ".jpg" in file or ".avif" in file or ".jpeg" in file or ".webp" in file:
            os.system(f"mv '/home/daniil/{file}' '/home/daniil/Imgs/{file}'")
        elif ".mp4" in file:
            os.system(f"mv '/home/daniil/{file}' '/home/daniil/Video/{file}'")
        elif ".pdf" in file or ".txt" in file or ".md" in file:
            os.system(f"mv '/home/daniil/{file}' '/home/daniil/Docs/{file}'")
check_files()
