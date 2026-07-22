# Skill: Otus DZ — Selenium + Docker Compose + Selenoid

Выводы из работы над ДЗ 10 (проект `DZv2`, папка `dz/`).

## Структура проекта

- Тесты и инфраструктура лежат в **`dz/`** (раньше `dz9` / `dz10`).
- Ветка для сдачи: **`dz-10`**.
- Не удалять старые папки без нужды — git видит rename как delete+add и раздувает diff.

## ДЗ 10 — что должно быть

1. **`dz/docker-compose.yml`** — OpenCart (phpMyAdmin + MariaDB + OpenCart) + сервис **`tests`**.
2. Сеть **`selenoid`** (external) — OpenCart и тесты в одной сети с Selenoid.
3. Тесты ждут healthcheck OpenCart (`depends_on: condition: service_healthy`), запускаются на **Selenoid**, проходят успешно.

## Selenoid (поднимается отдельно, до compose)

```bash
mkdir -p ~/selenoid
# browsers.json с chrome 120.0 → selenoid/chrome:120.0

docker network create selenoid   # если ещё нет

docker run -d --name selenoid \
  --network selenoid -p 4444:4444 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/selenoid/browsers.json:/etc/selenoid/browsers.json:ro \
  aerokube/selenoid:latest-release \
  -container-network selenoid

docker run -d --name selenoid-ui \
  --network selenoid -p 8090:8080 \
  aerokube/selenoid-ui:1.10.11 \
  --selenoid-uri http://selenoid:4444
```

UI: http://localhost:8090

## Запуск окружения и тестов

```bash
cd dz
PHPADMIN_PORT=8081 OPENCART_PORT=8080 LOCAL_IP=<ТВОЙ_IP> docker compose up --build
```

- **`LOCAL_IP`** — реальный IP (например `192.168.2.143`), не плейсхолдер `<ТВОЙ_IP>`.
- URL для тестов: **`http://${LOCAL_IP}:${OPENCART_PORT}`** (как в задании).
- Admin по умолчанию (Bitnami): **`user` / `bitnami`** (`OPENCART_USERNAME` / `OPENCART_PASSWORD` в compose).

## Известные проблемы и фиксы

| Проблема | Решение |
|----------|---------|
| `Failed to resolve 'selenoid'` | Selenoid не запущен или не в сети `selenoid` |
| `bitnami/mariadb:11.2: not found` | Образ **`bitnamilegacy/mariadb:11.2`** |
| Тесты падали на локаторах | Адаптация под OpenCart 4: `administration/`, `#header-cart`, валюта через `<a>`, регистрация без telephone |
| ~3M токенов в чате | Длинные логи compose, повторные прогоны агентом, огромные terminal dumps |

## conftest.py — Selenoid

Опции: `--executor selenoid`, `--browser_version`, `--selenoid-url` (по умолчанию `http://selenoid:4444/wd/hub`). При `executor=selenoid` — `webdriver.Remote`.

---

## Правило: тесты запускает пользователь

> Источник: `.cursor/rules/user-runs-tests.mdc` (alwaysApply: true)

- **Не** запускать Selenium / docker-compose / длинные `pytest` сессии, если пользователь явно не попросил.
- Давать **точную команду**; ждать **короткий вывод** (summary / FAILED), не перечитывать огромные логи без нужды.
- Перед правкой **многих файлов** — спросить; diff **минимальный**.
- Диагностика по **20–40 строкам** из терминала, не по полному дампу.

### Экономия токенов

1. Новый чат на новую задачу.
2. Тесты и логи — на стороне пользователя.
3. В чат — только ошибка + short test summary.
4. Ask/Plan для обсуждения, Agent — для точечных правок кода.
5. Не прикреплять лишние большие файлы и полный терминал.
