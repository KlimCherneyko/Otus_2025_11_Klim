import pytest
import pymysql
from pymysql.cursors import DictCursor


def pytest_addoption(parser):
    parser.addoption("--host", default="127.0.0.1", help="MariaDB host")
    parser.addoption("--port", default="3306", help="MariaDB port")
    parser.addoption("--database", default="bitnami_opencart", help="Database name")
    parser.addoption("--user", default="bn_opencart", help="Database user")
    parser.addoption("--password", default="", help="Database password")


@pytest.fixture(scope="session")
def connection(request):
    conn = pymysql.connect(
        host=request.config.getoption("--host"),
        port=int(request.config.getoption("--port")),
        user=request.config.getoption("--user"),
        password=request.config.getoption("--password"),
        database=request.config.getoption("--database"),
        cursorclass=DictCursor,
        autocommit=True,
    )
    yield conn
    conn.close()
