import pytest
from sqlalchemy.orm import Session
from sqlalchemy import select
from pytest import fixture
from app import create_app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine





@pytest.fixture(autouse=True)
@pytest.mark.run(order=100010)
def test_connect_testing_DB(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/read_order/11')
    if response.status_code == 200:
        pytest.exit("Test is not allowed to run with a real database")
    assert response.status_code == 400
    # engine = app_fixture.extensions['sqlalchemy'].engine
    # with Session(engine) as session:
    with app_fixture.app_context():
        stmt = (
            select(DB_client.id_client, DB_client.second_name)
            .where(DB_client.id_client == 1))
        client = session.execute(stmt).first()
        print(client)
        # session.execute(DB_client.__table__.delete())
        # session.commit()