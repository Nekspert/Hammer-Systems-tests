# Hammer-Systems-tests

## Referral System API

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