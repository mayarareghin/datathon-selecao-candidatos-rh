from http import HTTPStatus

# TESTES DA RAIZ
def test_root_deve_retornar_ok(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
