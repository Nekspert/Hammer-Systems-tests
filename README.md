# Hammer-Systems-tests

## Referral System API

Простой сервис авторизации по номеру телефона с реферальной системой на Django + DRF.

## Возможности

* Запрос и проверка 4-значного кода авторизации
* Авторизация/регистрация пользователя по номеру телефона
* Генерация случайного 6-значного инвайт-кода при первой авторизации
* Активация чужого инвайт-кода (только один раз)
* Просмотр своего профиля с текущим инвайт-кодом и списком рефералов

## Требования

* Python 3.8+
* PostgreSQL
* pip

## Установка и запуск

1. Клонируем репозиторий и переходим в папку проекта:

   ```bash
   git clone https://github.com/Nekspert/Hammer-Systems-tests.git
   cd referral_system
   ```

2. Создаем и активируем виртуальное окружение:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .\.venv\Scripts\activate     # Windows
   ```

3. Устанавливаем зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Создаем файл `.env` в корне проекта и заполняем переменные:

   ```dotenv
   DB_NAME=<имя_бд>
   DB_USER=<пользователь>
   DB_PASSWORD=<пароль>
   DB_HOST=<хост>
   DB_PORT=<порт>
   ```

5. Применяем миграции и создаем суперпользователя:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Запускаем сервер:

   ```bash
   python manage.py runserver
   ```

Теперь API доступно по адресу `http://127.0.0.1:8000/api/`.

## Аутентификация

Используется токен DRF. Для получения токена:

1. Запрос кода: `POST /api/auth/request_code/` с JSON `{ "phone_number": "+71234567890" }`.
2. Верификация кода: `POST /api/auth/verify_code/` с `{ "phone_number": "+71234567890", "code": "1234" }`.

В ответе придет токен:

```json
{
  "token": "<ваш_токен>"
}
```

Для последующих запросов добавляйте заголовок:

```
Authorization: Token <ваш_токен>
```

## Эндпоинты

Ниже описание API:

| Метод | URL                        | Пояснение                                                        |
|-------|----------------------------|------------------------------------------------------------------|
| POST  | `/api/auth/request_code/`  | Запрос SMS-кода по `phone_number`                                |
| POST  | `/api/auth/verify_code/`   | Проверка кода, создание/авторизация пользователя, возврат токена |
| GET   | `/api/profile/`            | Получение профиля (токен в заголовке)                            |
| POST  | `/api/profile/use_invite/` | Активация чужого `invite_code` (токен в заголовке)               |

## 📋 Postman Collection

В корне репозитория лежит `postman_collection.json` с готовыми запросами:

* Request Code
* Verify Code
* Get Profile
* Use Invite