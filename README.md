# Hop & Barley — Интернет-магазин для пивоварения

## Что это?
Учебный проект интернет-магазина товаров для домашнего пивоварения.

## Функционал
- Каталог товаров с категориями
- Корзина (для авторизованных и гостей)
- Оформление заказа с валидацией
- Отзывы к товарам
- Уведомления об ошибках/успехе
- Email подтверждение заказа

## Технологии
- Docker
- Django 4.x
- Python 3.10+
- PostgreSQL
- HTML/CSS/JavaScript (vanilla)

## Как запустить

1. Клонируйте репозиторий
```bash
git clone https://github.com/BorisovAndreyS/M3Project
cd M3Project 
```
2. Настройте окружение
```bash
cp .env.example .env
```
# Отредактируйте переменные при необходимости

3. Соберите и запустите контейнеры
```bash
docker-compose up --build
```

4. В новом терминале примените миграции
```commandline
docker-compose exec backend python manage.py migrate
```

5. Создайте суперпользователя
```commandline
docker-compose exec backend python manage.py createsuperuser
```

6. Откройте http://127.0.0.1:8000

**Админка**
http://127.0.0.1:8000/admin/


