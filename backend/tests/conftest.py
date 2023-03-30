from pytest import fixture
from app import create_app
from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.clients.models import DB_client
from app.orders.models import DB_orders
from app.materials.models import DB_materials
from app.products.models import DB_product
from app.payments.models import DB_payment
from app.outlay.models import DB_outlay


@fixture(scope="session")
def app_fixture():
    app_fixture = create_app('testing') # production development testing
    # engine = app_fixture.extensions['sqlalchemy'].engine
    # Session.configure(bind=engine)
    yield app_fixture


def pytest_collection_modifyitems(items):
    # items.sort(key=lambda x: x.get_closest_marker("run").kwargs.get("order", 0))
    items.sort(key=lambda x: x.get_closest_marker("run").kwargs.get("order", 0) if x.get_closest_marker("run") else 0)


@fixture(scope="session")
def db_session_fixture(app_fixture):
    engine = create_engine(app_fixture.config['DATABASE_URI'], echo=True)
    Session = sessionmaker(bind=engine)

    session = Session()
    print(f"name of testing DB - {app_fixture.config['DATABASE_URI']}")
    # DB_client.metadata.drop_all(engine)
    # DB_orders.metadata.drop_all(engine)
    # DB_payment.metadata.drop_all(engine)
    # DB_product.metadata.drop_all(engine)
    # session.commit()

    # DB_client.metadata.create_all(engine)
    # DB_orders.metadata.create_all(engine)
    # DB_payment.metadata.create_all(engine)
    # DB_product.metadata.create_all(engine)
    # session.commit()
    # session.close()
    return

    # yield session

    
    