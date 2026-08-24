# Frontend-тестирование Sauce Demo и Backend-тестирование Restful Booker

Курсовая работа: автоматизированные UI-тесты веб-приложения [Sauce Demo](https://www.saucedemo.com/) и API-тесты [Restful Booker](https://restful-booker.herokuapp.com/).

Стек: Python, pytest, Selenium, requests, Allure, Jenkins.

## Тема

Frontend-тестирование на основе веб-приложения Sauce Demo и Backend-тестирование на основе API Restful Booker

## Ресурсы

| Слой | Ресурс | Почему |
|---|---|---|
| UI | https://www.saucedemo.com/ | Публичное демо-приложение, стабильные `data-test` локаторы, полный e-commerce сценарий |
| API | https://restful-booker.herokuapp.com/ | Публичный CRUD API с авторизацией, документация: https://restful-booker.herokuapp.com/apidoc/index.html |

Проекты работодателей не используются.

Учётные данные Sauce Demo (публичные): пользователь `standard_user`, пароль `secret_sauce`.  
Restful Booker: `admin` / `password123`. Данные API сбрасываются примерно каждые 10 минут, поэтому тесты создают свои бронирования.

## Критерии и как они закрыты

| Критерий | Реализация |
|---|---|
| Page Object | `ui/pages/` — все действия UI только через page-классы |
| Allure title / steps / attach | `@allure.title`, `@allure.step`, attach request/response и скриншот |
| Минимум 10 UI и 20–30 API | 19 UI-тестов, 29 API-тестов (параметризация считается отдельно) |
| Скриншот при падении | хук `pytest_runtest_makereport` в `conftest.py` |
| Jenkins + отчёт там же | `jenkins/docker-compose.yml`, Pipeline, Allure plugin |

## Структура

```text
coursework/
  ui/pages/          Page Object для Sauce Demo
  ui/tests/          UI-тесты
  api/client/        HTTP-клиент Restful Booker
  api/tests/         API-тесты
  jenkins/           Jenkins в Docker
  Jenkinsfile        Pipeline
  conftest.py        драйвер, URL, скриншот при падении
```

## Локальный запуск

```bash
cd coursework
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
chmod +x run_tests.sh
./run_tests.sh
```

Отдельно:

```bash
pytest -m ui
pytest -m api
```

Отчёт Allure:

```bash
allure serve allure-results
```

Headed-режим браузера: `pytest -m ui --selenium-headed`.

## Jenkins

```bash
cd coursework/jenkins
docker compose up -d --build
```

После старта:

1. Открыть http://localhost:8080
2. Войти: `admin` / `admin`
3. Job `saucedemo-booker-tests` создаётся автоматически и запускается каждые ~30 минут
4. Build Now → в билде открыть **Allure Report**

Каталог `coursework/` монтируется в контейнер как `/coursework`. Образ Jenkins уже содержит Python, Chromium, Allure CLI и плагины.

## Объём тестов

**UI (19):** логин, locked out, валидация логина (3), logout, сортировка (4), карточка товара, корзина (add 1 / add 2 / remove inventory / remove cart), checkout happy path, валидация checkout (3).

**API (29):** ping, auth success, auth invalid (3), update без токена, список id, get по id, 404, фильтры имени (2), фильтр checkin, типы полей, create, schema, цены (4), depositpaid (2), без additionalneeds, без firstname, PUT, PATCH, PUT + Basic auth, DELETE, GET после DELETE, DELETE без токена.
