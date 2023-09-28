# Запуск на сервера
---
Создаем папку на сервере
`mkdir foodgram`

Копируем файлы в папку foodgram
`1. docker-compose.production.yml`
`2. data/`
`3. .env`

Запускаем контейнеры
`sudo docker compose -f docker-compose.production.yml up -d`

Переносим frontend в nginx контейнер
`sudo docker exec  foodgram-nginx-1 cp -rT /static_frontend/build/ /usr/share/nginx/html/`

Для первоначальной настройки
###### Создает админа, и добавляет ингридиенты 
`sudo docker exec foodgram-backend-1 python manage.py data`
###### Создает тестовые рецепты, для диплома
`sudo docker exec foodgram-backend-1 python manage.py recipes_diplom`




# Локальный запуск backend 
---
Создаем виртульное окружение
`python3 -m venv venv`

Устанавливаем переменные из requirements.txt
`pip install -r requirements.txt`

Запуск виртуального окружения
`source venv\bin\activate`

Запуск backend 
`python manage.py runserver`


# API
---
Документация по API находится в папке `docs`




































