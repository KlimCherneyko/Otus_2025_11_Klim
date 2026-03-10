def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://ya.ru",
        help="URL для проверки статус-кода"
    )
    parser.addoption(
        "--status_code",
        action="store",
        default="200",
        help="Ожидаемый статус-код"
    )
