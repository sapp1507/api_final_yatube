# API проекта YaTube

##Установка и запуск
Клонировать репозиторий и перейти в его каталог в командной строке:
```
git clone git@github.com:sapp1507/api_final_yatube.git
cd api_final_yatube
```
Создать и активировать виртуальное окружение:
```
python3 -m venv venv
source venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции:
```
cd yatube_api
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
Для создания суперпользователя:
```
python3 manage.py createsuperuser
```
##Возможности API
Документация по API доступна по адресу [redoc/](http://127.0.0.1:8000/redoc)

Получение публикаций:
```
GET api/v1/posts/
```
Создание публикации:
```
POST api/v1/posts/
```
Получение публикации:
```
GET api/v1/posts/(id)
```
Обновление публикации:
```
PUT api/v1/posts/(id)
```
Частичное обновление публикации:
```
PATH api/v1/posts/(id)
```
Удаление публикации:
```
DELETE api/v1/posts/(id)
```
Получение комментариев:
```
GET api/v1/posts/(post_id)/comments/
```
Добавление комментария:
```
POST api/v1/posts/(post_id)/comments/
```
Получение комментария:
```
GET api/v1/posts/(post_id)/comments/(id)
```
Обновление комментария:
```
PUT api/v1/posts/(post_id)/comments/(id)
```
Частичное обновление комментария:
```
PATH api/v1/posts/(post_id)/comments/(id)
```
Удаление комментария:
```
DELETE api/v1/posts/(post_id)/comments/(id)
```
Список сообществ:
```
GET api/v1/groups/
```
Информация о сообществе:
```
GET api/v1/groups/(id)
```
Подписки:
```
GET api/v1/follow/
```
Подписка:
```
POST api/v1/follow/
```
Получить JWT-токен:
```
POST api/v1/jwt/create/
```
Обновить JWT-токен:
```
POST api/v1/jwt/refresh/
```
Проверить JWT-токен:
```
POST api/v1/jwt/verify/
```