from pytest import fixture
from app import create_app
from app.base_model import Base
from sqlalchemy import create_engine




@fixture(scope="session")
def app_fixture():
    app_fixture = create_app('testing') # production development testing

    engine = create_engine(app_fixture.config['SQLALCHEMY_DATABASE_URI'], future=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    yield app_fixture


def pytest_collection_modifyitems(items):
    items.sort(key=lambda x: x.get_closest_marker("run").kwargs.get("order", 0) if x.get_closest_marker("run") else 0)
