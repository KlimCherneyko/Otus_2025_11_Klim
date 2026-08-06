# Анализ access-лога веб-сервера

Скрипт `analyze_log.py` парсит access-логи в формате:

```text
%h - - %t "%r" %s %b "%{Referer}" "%{User-Agent}" %d
```

и собирает статистику за один проход по файлу.

## Зависимости

Только стандартная библиотека Python 3 (`argparse`, `json`, `os`, `re`, `collections`).

## Подготовка

Распаковать архив с логом:

```shell
tar -xzvf access.tar.gz
```

## Запуск

Анализ конкретного файла:

```shell
python3 analyze_log.py access.log
```

Анализ всех `.log` файлов в директории:

```shell
python3 analyze_log.py .
```

## Результат

Для каждого лог-файла скрипт:

1. печатает JSON-статистику в терминал;
2. сохраняет её в файл рядом с рабочей директорией запуска (`access.log` → `access.json`).

Поля JSON:

| Поле | Описание |
|------|----------|
| `total_requests` | общее число запросов |
| `total_stat` | число запросов по HTTP-методам |
| `top_ips` | топ-3 IP по числу запросов |
| `top_longest` | топ-3 самых долгих запросов (`ip`, `date`, `method`, `url`, `duration`) |
