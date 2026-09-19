# ShopEasy

Учебный интернет-магазин на Django с каталогом товаров, пользователями и оформлением заказов.

## Что это

ShopEasy — серверное web-приложение интернет-магазина, в котором выделены основные доменные части:

- каталог и управление товарами;
- аккаунты пользователей;
- работа с корзиной и заказами;
- HTML-шаблоны магазина;
- административное управление данными через Django.

## Зачем

Проект создан для практики разработки e-commerce backend: моделирования сущностей магазина, построения пользовательского сценария от каталога до заказа и работы с Django ORM, шаблонами и миграциями.

## Стек

- **Python 3.9+**
- **Django 5.2.5**
- **SQLite** — локальное хранилище
- **Pillow** — изображения товаров
- **python-decouple** — настройки через окружение
- **Django Templates** — server-side UI

## Быстрый старт

```bash
git clone https://github.com/Temurlan01/ShopEasy.git
cd ShopEasy
python -m venv .venv

# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .\.venv\Scripts\Activate.ps1

pip install -r requrements.txt
python manage.py migrate
python manage.py runserver
```

Приложение будет доступно по адресу http://127.0.0.1:8000.

> Файл зависимостей в репозитории называется `requrements.txt`.

## Скриншоты и демо

Публичный demo URL пока не настроен. Для портфолио добавьте в `docs/screenshots/` скриншоты каталога, карточки товара, корзины и оформления заказа:

```md
![Каталог](docs/screenshots/catalog.png)
![Карточка товара](docs/screenshots/product.png)
![Корзина](docs/screenshots/cart.png)
```

## Структура

```text
market/                 # каталог и товары
orders/                 # заказы
users/                  # пользователи
internet_market_project/ # настройки Django
templates/              # HTML-шаблоны
manage.py               # CLI Django
```

## Дальнейшее развитие

- подключить PostgreSQL и Redis;
- добавить оплату и уведомления;
- покрыть checkout тестами;
- добавить Docker и CI;
- опубликовать staging/demo-версию.

## Лицензия

Лицензия пока не указана.
