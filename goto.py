import sys
import webbrowser

def main():
    if len(sys.argv) < 2:
        print("Использование: script.py <слово_или_домен>")
        return
    
    input_str = sys.argv[1].strip().lower()
    tlds = ['.com', '.ru', '.net', '.org', '.info', '.biz', '.de', '.uk', '.br', '.pl', '.in', '.it', '.fr', '.au', '.us', '.co', '.io', '.me']
    
    # Проверяем доменные окончания (включая двухуровневые)
    is_domain = False
    for tld in sorted(tlds, key=len, reverse=True):
        if input_str.endswith(tld):
            is_domain = True
            break
    
    if is_domain:
        # Добавляем протокол если отсутствует
        url = input_str if '://' in input_str else 'http://' + input_str
    else:
        # Формируем поисковый URL
        url = f"https://duckduckgo.com/?q={input_str}"
    
    webbrowser.open(url)

if __name__ == "__main__":
    main()

