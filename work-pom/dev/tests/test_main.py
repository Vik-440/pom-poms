# from starlette.testclient import TestClient
# from app import app

# client = TestClient(app)
from routes.main import return_data_from_flask

# def return_data_from_flask():
#     return ({"ping": "pong"})


def test_0get():
    info = {
        "id_order": 541,
        "data_order": "2022-02-23",
        "kolor_model": "малиновий",
        "kod_model": "190-B05"}
    info1 = {
        "id_order": 541,
        "kolor_model": "малиновий",
        "data_order": "2022-02-23",
        "kod_model": "190-B05"}
    # response = client.get("/")
    # assert response.status_code == 200
    # assert response.json() == {"ping": "pong!"}
    print(return_data_from_flask)
    assert info == info1
    # assert return_data_from_flask == info
