
#!/usr/bin/env python3
import asyncio
import sys
import time
from datetime import datetime
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter, TelegramServerError

TOKEN = ""
ADMIN_CHAT_ID = ""

# Настройки повторных попыток
MAX_RETRIES = 10  # Максимальное количество попыток
INITIAL_DELAY = 5  # Начальная задержка в секундах
MAX_DELAY = 300  # Максимальная задержка в секундах (5 минут)
BACKOFF_FACTOR = 2  # Множитель для экспоненциальной задержки

# Глобальная сессия бота
bot = None

async def init_bot():
    """Инициализация бота один раз для всех отправок"""
    global bot
    if bot is None:
        bot = Bot(
            token=TOKEN,
            default=DefaultBotProperties(parse_mode="HTML")
        )
    return bot

async def send_part_with_retry(file_path: str):
    """Отправка файла с повторными попытками при ошибках"""
    await init_bot()
    
    # Парсим номер части из имени файла
    if '.part_' in file_path:
        part_num = file_path.split('.part_')[-1]
    else:
        # Если формат другой, пробуем другой способ
        import re
        match = re.search(r'\.part_?(\d+)$', file_path)
        if match:
            part_num = match.group(1)
        else:
            # Или берем последний элемент после точки
            part_num = file_path.split('.')[-1]
    
    file = FSInputFile(file_path)
    
    # Пробуем определить общее количество частей
    total_parts = None
    try:
        import glob
        import os
        # Ищем все файлы с тем же префиксом
        dir_path = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        
        if '.part_' in base_name:
            prefix = base_name.split('.part_')[0] + '.part_'
            all_parts = glob.glob(os.path.join(dir_path, prefix + '*'))
            total_parts = len(all_parts)
    except:
        pass
    
    caption = (
        f"📦 Backup part {part_num}\n"
        f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    
    if total_parts:
        caption += f"🔢 Part {part_num} of {total_parts}"
    else:
        caption += f"🔢 Part {part_num}"
    
    delay = INITIAL_DELAY
    
    for attempt in range(MAX_RETRIES):
        try:
            print(f"Attempt {attempt + 1}/{MAX_RETRIES} sending part {part_num}...")
            
            await bot.send_document(
                chat_id=ADMIN_CHAT_ID,
                document=file,
                caption=caption
            )
            
            print(f"✅ Part {part_num} successfully sent!")
            return True
            
        except TelegramRetryAfter as e:
            # Telegram просит подождать
            wait_time = e.retry_after
            print(f"⚠️ Rate limit: waiting {wait_time} seconds...")
            await asyncio.sleep(wait_time)
            continue
            
        except TelegramNetworkError as e:
            # Проблемы с сетью
            error_msg = str(e)
            print(f"🌐 Network error on attempt {attempt + 1} for part {part_num}: {error_msg}")
            
        except TelegramServerError as e:
            # Проблемы сервера Telegram
            error_msg = str(e)
            print(f"🔄 Telegram server error on attempt {attempt + 1} for part {part_num}: {error_msg}")
            
        except Exception as e:
            # Другие ошибки
            error_msg = str(e)
            print(f"❌ Error on attempt {attempt + 1} for part {part_num}: {error_msg}")
        
        # Если это последняя попытка, завершаем с ошибкой
        if attempt == MAX_RETRIES - 1:
            print(f"⚠️ Max attempts ({MAX_RETRIES}) exceeded for part {part_num}")
            return False
        
        # Вычисляем задержку для следующей попытки с экспоненциальным откатом
        if delay < MAX_DELAY:
            delay *= BACKOFF_FACTOR
            if delay > MAX_DELAY:
                delay = MAX_DELAY
        
        # Добавляем немного случайности к задержке
        jitter = delay * 0.1
        actual_delay = delay + (jitter * (0.5 - time.time() % 1))
        
        print(f"⏳ Waiting {actual_delay:.1f} seconds before next attempt...")
        await asyncio.sleep(actual_delay)
    
    return False


async def send_part(file_path: str):
    """Основная функция отправки файла"""
    try:
        success = await send_part_with_retry(file_path)
        return success
            
    except Exception as e:
        print(f"💥 Critical error sending file {file_path}: {e}")
        return False


async def close_bot():
    """Закрытие сессии бота"""
    global bot
    if bot:
        try:
            await bot.session.close()
        except:
            pass
        bot = None


async def main(file_paths: list):
    """Основная асинхронная функция для отправки нескольких файлов"""
    try:
        # Инициализируем бота
        await init_bot()
        
        results = []
        total = len(file_paths)
        
        for i, file_path in enumerate(file_paths, 1):
            print(f"\n📤 Sending file {i}/{total}: {file_path}")
            success = await send_part(file_path)
            results.append((file_path, success))
            
            # Небольшая пауза между файлами, но не после последнего
            if i < total:
                await asyncio.sleep(1)
        
        # Выводим сводку
        print("\n" + "="*50)
        print("📊 SENDING SUMMARY:")
        successful = sum(1 for _, success in results if success)
        print(f"✅ Successfully sent: {successful}/{total}")
        
        if successful < total:
            print("❌ Failed files:")
            for file_path, success in results:
                if not success:
                    print(f"  - {file_path}")
            return False
        else:
            print("🎉 All files sent successfully!")
            return True
            
    finally:
        # Закрываем бота в конце
        await close_bot()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Send single file: python3 backup_bot.py <file_path>")
        print("  Send multiple files: python3 backup_bot.py <file1> <file2> ...")
        sys.exit(1)
    
    try:
        if len(sys.argv) == 2:
            # Одиночная отправка (для совместимости)
            asyncio.run(main([sys.argv[1]]))
        else:
            # Множественная отправка
            asyncio.run(main(sys.argv[1:]))
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
        asyncio.run(close_bot())
        sys.exit(0)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        asyncio.run(close_bot())
        sys.exit(1)

