# Описание
---

Дипломный проект Яндекс Практиум
Веб приложение по размещению рецептов
## Задача 
---

Написать backend под frontend по документации api



# API
---
Документация по API находится в папке `docs`


# Команды
---
Файлы с командами находятся `backend\basic_setuo\managment\cammands\`

- `data` - Выполняет миграцию, создает стакику и перемещает ее на диск для контейнера nginx, заполняет таблицу Ingridient, заполняет таблицу Tag, создает администратора.
- `data_test` - Создает администратора, создает тестовых пользователей, заполняет таблицу Tag, заполняет таблицу Ingridient, заполняет таблицу Receipt тестовыми данными, добавляет в бд TagReceipt, добавляет тестовые данные в IngridientReceipt.
- `recipes_diplom` - создает тестовых пользователей, создает рецепты с тегами и ингридиентами


# Запуск на сервера
---

### На рабочем сервере
---
__Создаем папку на сервере__
    `mkdir foodgram`
    
__Копируем файлы в папку foodgram__
- `docker-compose.production.yml`
- `data/`
- `.env`
    
__Запускаем контейнеры__
`sudo docker compose -f docker-compose.production.yml up -d`
    
__Переносим frontend в nginx контейнер__
`sudo docker exec  foodgram-nginx-1 cp -rT /static_frontend/build/ /usr/share/nginx/html/`
    
### Для первоначальной настройки
__Создает админа, и добавляет ингридиенты__
`sudo docker exec foodgram-backend-1 python manage.py data`
__Создает тестовые рецепты, для диплома__
`sudo docker exec foodgram-backend-1 python manage.py recipes_diplom`
    

### Локальный запуск backend 
---
__Создаем виртульное окружение__
    `python3 -m venv venv`
    
__Устанавливаем переменные из requirements.txt__
`pip install -r requirements.txt`
    
__Запуск виртуального окружения__
`source venv\bin\activate`
    
__Запуск backend__
`python manage.py runserver`