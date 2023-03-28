from pytest import fixture
from app import create_app


@fixture(scope="session")
def app_fixture():
    app_fixture = create_app('testing') # production development testing
    yield app_fixture


