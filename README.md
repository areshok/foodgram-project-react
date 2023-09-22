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
Ссылки для API даны для локальной проверки, для проверки на сервере заменить `127.0.0.1:8000` на `доменное имя` 

#### Пользователи
список пользователей
`get` `http://127.0.0.1:8000/api/users/`
регистрация пользователя
`post` `http://127.0.0.1:8000/api/users/`
профиль пользователя
`get` `http://127.0.0.1:8000/api/users/1/`
текущий пользователь
`get` `http://127.0.0.1:8000/api/users/me/`
смена пароля
`post` `http://127.0.0.1:8000/api/users/set_password/`
получение токена
`post` `http://127.0.0.1:8000/api/auth/token/login/`
удаление токена
`post` `http://127.0.0.1:8000/api/auth/token/logout/`

#### Теги
Список тегов
`get` `http://127.0.0.1:8000/api/tags/`
Получение тега
`get` `http://127.0.0.1:8000/api/tags/1/`

#### Рецепты




































