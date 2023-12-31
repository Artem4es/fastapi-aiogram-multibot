from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from src.config import Settings

settings = Settings()
scheduler = AsyncIOScheduler()

phrase_list = list()
phrase_list.append('С новым годом, братишка! Пусть в новом году у тебя будет бабло как у олигарха, машина как у бандита, а девчонки падают к твоим ногам, как подкова к фотоаппарату!')
phrase_list.append('С новым годом, братишка! Пусть в новом году у тебя будет бабло как у олигарха, машина как у бандита, а девчонки падают к твоим ногам, как подкова к фотоаппарату!')
phrase_list.append('Новый год наступает, и ты, сука, все еще такой же дерзкий и крутой! Пусть в этом году тебе не попадаются мудаки на пути и все твои планы сбываются, как дешевая водка на дне бутылки!')
phrase_list.append('Наступает новый год, бро! Давай забудем все плохое и встретим его с чистой душой и полным баком отжига! Пусть наша жопа будет держаться крепче, чем корка насосной дубинки, и мы не опускаемся ни на миллиметр!')
phrase_list.append('С новым годом, чувак! Пусть наша банда будет сильнее, чем семья Кардашьян, и мы шныряем по улицам как настоящие короли. Желаю, чтобы в новом году мы дрались редко, но всегда побеждали!')
phrase_list.append('С новым годом, кент! Пусть у тебя всегда будет карман нарезной и достаточно пива в холодильнике, чтобы снимать жажду после боевого выхода. А чтобы удача тебя не обманула, носи свои пупырышки с гордостью!')

async def my_job():
    bot = Bot(settings.gop_token)
    IDS = settings.ids.split(',')
    i = 0
    for id in IDS:
        await bot.send_message(id, phrase_list[i])
        i += 1


scheduled_time = datetime(year=2024, month=1, day=1, hour=0, minute=0, second=0)
scheduler.add_job(my_job, 'date', run_date=scheduled_time)