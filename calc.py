import math
import os
import sys

# Кастомные цвета для Linux терминала
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def fast_cacl():
    print(eval(input("Введите пример ")))

def clear_screen():
    """Очистка экрана с проверкой ОС"""
    os.system('clear')

def display_header():
    """Отображение заголовка с цветами"""
    clear_screen()
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*50}")
    print(" "*20 + "КАЛЬКУЛЯТОР")
    print(f"{'='*50}{Colors.RESET}")
    print(f"{Colors.YELLOW}Доступные операции:{Colors.RESET}")

def display_operations():
    """Отображение списка операций с цветами"""
    ops = [
        ("1. Сложение (+) ", Colors.GREEN),
        ("2. Вычитание (-) ", Colors.GREEN),
        ("3. Умножение (*) ", Colors.GREEN),
        ("4. Деление (/) ", Colors.GREEN),
        ("5. Возведение в степень (^) ", Colors.BLUE),
        ("6. Квадратный корень (sqrt) ", Colors.BLUE),
        ("7. Синус (sin) ", Colors.MAGENTA),
        ("8. Косинус (cos) ", Colors.MAGENTA),
        ("9. Тангенс (tan) ", Colors.MAGENTA),
        ("10. Арксинус (asin) ", Colors.MAGENTA),
        ("11. Арккосинус (acos) ", Colors.MAGENTA),
        ("12. Арктангенс (atan) ", Colors.MAGENTA),
        ("13. Логарифм по основанию 10 (log) ", Colors.CYAN),
        ("14. Натуральный логарифм (ln) ", Colors.CYAN),
        ("15. Факториал (!) ", Colors.CYAN),
        ("16. Быстрый подсчет ", Colors.CYAN),
        ("17. Выход (q) ", Colors.RED)
    ]
    
    for op, color in ops:
        print(f"{color}{op}{Colors.RESET}")

def linux_calculator():
    """Основная функция калькулятора с кастомным интерфейсом для Linux"""
    while True:
        display_header()
        display_operations()
        
        operation = input(f"\n{Colors.BOLD}{Colors.WHITE}Введите операцию (или номер): {Colors.RESET}").lower()
        
        if operation in ['q', '17', 'выход']:
            print(f"{Colors.YELLOW}\nДо свидания!{Colors.RESET}")
            break
        
        try:
            if operation in ['+', '1', 'сложение']:
                a = float(input(f"{Colors.GREEN}Введите первое число: {Colors.RESET}"))
                b = float(input(f"{Colors.GREEN}Введите второе число: {Colors.RESET}"))
                print(f"{Colors.BOLD}Результат: {Colors.GREEN}{a + b}{Colors.RESET}")
                
            elif operation in ['-', '2', 'вычитание']:
                a = float(input(f"{Colors.GREEN}Введите первое число: {Colors.RESET}"))
                b = float(input(f"{Colors.GREEN}Введите второе число: {Colors.RESET}"))
                print(f"{Colors.BOLD}Результат: {Colors.GREEN}{a - b}{Colors.RESET}")
                
            elif operation in ['*', '3', 'умножение']:
                a = float(input(f"{Colors.GREEN}Введите первое число: {Colors.RESET}"))
                b = float(input(f"{Colors.GREEN}Введите второе число: {Colors.RESET}"))
                print(f"{Colors.BOLD}Результат: {Colors.GREEN}{a * b}{Colors.RESET}")
                
            elif operation in ['/', '4', 'деление']:
                a = float(input(f"{Colors.GREEN}Введите первое число: {Colors.RESET}"))
                b = float(input(f"{Colors.GREEN}Введите второе число: {Colors.RESET}"))
                if b == 0:
                    print(f"{Colors.RED}Ошибка: деление на ноль!{Colors.RESET}")
                else:
                    print(f"{Colors.BOLD}Результат: {Colors.GREEN}{a / b}{Colors.RESET}")
                    
            elif operation in ['^', '5', 'степень']:
                a = float(input(f"{Colors.BLUE}Введите основание: {Colors.RESET}"))
                b = float(input(f"{Colors.BLUE}Введите степень: {Colors.RESET}"))
                print(f"{Colors.BOLD}Результат: {Colors.BLUE}{a ** b}{Colors.RESET}")
                
            elif operation in ['sqrt', '6', 'корень']:
                a = float(input(f"{Colors.BLUE}Введите число: {Colors.RESET}"))
                if a < 0:
                    print(f"{Colors.RED}Ошибка: корень из отрицательного числа!{Colors.RESET}")
                else:
                    print(f"{Colors.BOLD}Результат: {Colors.BLUE}{math.sqrt(a)}{Colors.RESET}")
                    
            elif operation in ['sin', '7']:
                a = float(input(f"{Colors.MAGENTA}Введите угол в градусах: {Colors.RESET}"))
                print(f"{Colors.BOLD}Результат: {Colors.MAGENTA}{math.sin(math.radians(a))}{Colors.RESET}")
                
            elif operation in ['cos', '8']:
                a = float(input(f"{Colors.MAGENTA}Введите угол в градусах: {Colors.RESET}"))
                print(f"{Colors.BOLD}Результат: {Colors.MAGENTA}{math.cos(math.radians(a))}{Colors.RESET}")
                
            elif operation in ['tan', '9']:
                a = float(input(f"{Colors.MAGENTA}Введите угол в градусах: {Colors.RESET}"))
                print(f"{Colors.BOLD}Результат: {Colors.MAGENTA}{math.tan(math.radians(a))}{Colors.RESET}")
                
            elif operation in ['asin', '10']:
                a = float(input(f"{Colors.MAGENTA}Введите значение (-1 до 1): {Colors.RESET}"))
                if -1 <= a <= 1:
                    print(f"{Colors.BOLD}Результат: {Colors.MAGENTA}{math.degrees(math.asin(a))}°{Colors.RESET}")
                else:
                    print(f"{Colors.RED}Ошибка: значение должно быть между -1 и 1{Colors.RESET}")
                    
            elif operation in ['acos', '11']:
                a = float(input(f"{Colors.MAGENTA}Введите значение (-1 до 1): {Colors.RESET}"))
                if -1 <= a <= 1:
                    print(f"{Colors.BOLD}Результат: {Colors.MAGENTA}{math.degrees(math.acos(a))}°{Colors.RESET}")
                else:
                    print(f"{Colors.RED}Ошибка: значение должно быть между -1 и 1{Colors.RESET}")
                    
            elif operation in ['atan', '12']:
                a = float(input(f"{Colors.MAGENTA}Введите значение: {Colors.RESET}"))
                print(f"{Colors.BOLD}Результат: {Colors.MAGENTA}{math.degrees(math.atan(a))}°{Colors.RESET}")
                
            elif operation in ['log', '13']:
                a = float(input(f"{Colors.CYAN}Введите число: {Colors.RESET}"))
                if a <= 0:
                    print(f"{Colors.RED}Ошибка: число должно быть положительным{Colors.RESET}")
                else:
                    print(f"{Colors.BOLD}Результат: {Colors.CYAN}{math.log10(a)}{Colors.RESET}")
                    
            elif operation in ['ln', '14']:
                a = float(input(f"{Colors.CYAN}Введите число: {Colors.RESET}"))
                if a <= 0:
                    print(f"{Colors.RED}Ошибка: число должно быть положительным{Colors.RESET}")
                else:
                    print(f"{Colors.BOLD}Результат: {Colors.CYAN}{math.log(a)}{Colors.RESET}")
                    
            elif operation in ['!', '15', 'факториал']:
                a = int(input(f"{Colors.CYAN}Введите целое число: {Colors.RESET}"))
                if a < 0:
                    print(f"{Colors.RED}Ошибка: факториал отрицательного числа не определен{Colors.RESET}")
                else:
                    print(f"{Colors.BOLD}Результат: {Colors.CYAN}{math.factorial(a)}{Colors.RESET}")
            elif operation == "16":
                fast_cacl()
            else:
                print(f"{Colors.RED}Неизвестная операция. Попробуйте снова.{Colors.RESET}")
                
            input(f"\n{Colors.YELLOW}Нажмите Enter чтобы продолжить...{Colors.RESET}")
                
        except ValueError:
            print(f"{Colors.RED}Ошибка: введите корректное число{Colors.RESET}")
            input(f"\n{Colors.YELLOW}Нажмите Enter чтобы продолжить...{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Произошла ошибка: {e}{Colors.RESET}")
            input(f"\n{Colors.YELLOW}Нажмите Enter чтобы продолжить...{Colors.RESET}")

if __name__ == "__main__":
    # Проверяем, работает ли в Linux терминале
    if os.name == 'posix' and sys.stdout.isatty():
        linux_calculator()
