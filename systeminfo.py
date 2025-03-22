import logging
import psutil
import datetime
from pyrogram import Client, types, enums
from .. import loader, utils

class SysInfo(loader.Module):  # Убрал декоратор
    """Модуль для отображения информации о системе с помощью psutil."""

    strings = {
        "wait": "⏳ <b>Сбор информации...</b>",
        "info": "💻 <b>Системная информация:</b>\n\n{}",
    }

    async def sysinfo(self, app: Client, message: types.Message):
        """Отображает системную информацию"""
        msg_ = await message.answer(self.strings["wait"])

        try:
            info = {
                "CPU Использование": f"{psutil.cpu_percent()}%",
                "Оперативная память": f"{psutil.virtual_memory().percent}%",
                "Общий объем памяти": f"{psutil.virtual_memory().total / (1024**3):.2f} ГБ",
                "Использовано памяти": f"{psutil.virtual_memory().used / (1024**3):.2f} ГБ",
                "Свободно памяти": f"{psutil.virtual_memory().available / (1024**3):.2f} ГБ",
                "Время работы системы": str(datetime.timedelta(seconds=int(psutil.boot_time())))
            }

            output = "\n".join([f"<b>{key}:</b> {value}" for key, value in info.items()])
            await msg_.edit(self.strings["info"].format(output))
        except Exception as e:
            logging.error(f"Ошибка получения системной информации: {e}")
            await msg_.edit("❌ Не удалось получить информацию о системе.")
