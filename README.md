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
2. Установите зависимости
```bash
poetry install
poetry update
```
3. Примените миграции
```bash
python manage.py migrate
```

4. Создайте суперпользователя
```commandline
python manage.py createsuperuser
```

5. Запустите сервер
```commandline
python manage.py runserver
```

6. Откройте http://127.0.0.1:8000

**Админка**
http://127.0.0.1:8000/admin/





The project includes the layout and client-side logic for the following pages and components:

-   **Homepage (`home.html`):** a product catalog with interactive filters.
-   **Product Pages:** 12 unique pages for each product, complete with descriptions, specifications, and user reviews.
-   **Shopping Cart (`cart.html`):** an interactive cart with features to change item quantities and remove items, with automatic total recalculation.
-   **Checkout (`checkout.html`):** a form for entering shipping information and selecting a payment method.
-   **Authentication:**
    -   Login (`login.html`), registration (`register.html`), and password recovery (`forgot_password.html`) pages.
    -   **Login/Logout Simulation:** the header dynamically changes based on the user's authentication status (using `localStorage`).
-   **User Account (`account.html`):** a tabbed page for viewing order history and editing user information.
-   **Custom Admin Panel:**
    -   A page to view the product list (`admin/products.html`).
    -   A form to add/edit products (`admin/add.html`) with an image upload simulation.


