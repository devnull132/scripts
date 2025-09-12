#!/usr/bin/env python3
import asyncio
import sys
from datetime import datetime
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile

TOKEN = ""
ADMIN_CHAT_ID = ""

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

async def send_part(file_path: str):
    try:
        part_num = file_path.split('.part_')[-1]
        file = FSInputFile(file_path)
        caption = (
            f"📦 Backup part {part_num}\n"
            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"🔢 Part {part_num} of {file_path.split('.part_')[0]}"
        )
        
        await bot.send_document(
            chat_id=ADMIN_CHAT_ID,
            document=file,
            caption=caption
        )
        return True
    except Exception as e:
        print(f"Error sending part: {e}")
        return False
    finally:
        await bot.session.close()

async def main(file_path: str):
    await send_part(file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 backup_bot.py <file_path>")
        sys.exit(1)
    
    asyncio.run(main(sys.argv[1]))
