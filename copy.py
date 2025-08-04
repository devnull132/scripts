import sys
import subprocess

def copy_to_clipboard(text):
    process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
    process.communicate(input=text.encode('utf-8'))

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: ./copy_file_to_clipboard.py <путь_к_файлу>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    file_content = read_file(file_path)
    copy_to_clipboard(file_content)
    print(f"Содержимое файла '{file_path}' скопировано в буфер обмена")
