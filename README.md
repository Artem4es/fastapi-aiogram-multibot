### FastApi-Aiogram-multibot
FastApi-Aiogram-multibot - Chat GPT бот с возможностью создания новых ботов налету через API.

### Как запустить? 👾
Проект можно запустить, используя Docker-compose для этого:


- Клонировать репозиторий:

```
git clone git@github.com:Artem4es/fastapi-aiogram-multibot.git
```

Создать файл .env в корневой директории (той же где .env.template) на основе .env.template 


- Запустить проект через docker-compose:

```
docker-compose up --build
```

ТГ боты реализованы через Webhook, поэтому нужен адрес хоста, где запущен проект в сети или Ngrok.
   - Если есть хост:
     - Его адрес нужно указать в переменной BASE_WEBHOOK_URL в файле .env


   - Ecли хоста нет:
      - Если проект запускается локально можно использовать Ngrok. https://ngrok.com/download
      - Запустите сервер Ngrok на 80 порту.
         ```
         ngrok http 80
         ```
      - Скопируйте адрес из поля Forwarding в переменную BASE_WEBHOOK_URL .env файла




   - После запуска проекта cразу будет активирован Main bot, токен которого вы указали в .env (MAIN_BOT_TOKEN)
   - Логи прокинуты через mount и доступны локально в src/app/logs/app.log

### Исчерпывающая документация проекта 📘
После запуска проекта доступная документация Swagger и Redoc по адресам: http://localhost:8000/docs/ или тут http://localhost:8000/redoc/
