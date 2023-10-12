from werkzeug.test import Client

def test_auth_user_post_200(client: Client):

    response = client.post('/auth/user', json={
        'email': 'test1',
        'password': 'test1'
    })
    assert response.status_code == 200




def test_auth_user_post_409(client: Client):

    response = client.post('/auth/user', json={
        'email': 'test1',
        'password': 'test1'
    })
    assert response.status_code == 200

    response = client.post('/auth/user', json={
        'email': 'test1',
        'password': 'test1'
    })
    assert response.status_code == 409




def test_auth_user_post_400(client: Client):
    response = client.post('/auth/user', json={
    })
    assert response.status_code == 400

    response = client.post('/auth/user', json={
        'password': 'test1'
    })
    assert response.status_code == 400

    response = client.post('/auth/user', json={
        'email': 'test1',
    })
    assert response.status_code == 400

    response = client.post('/auth/user', json={
        'email': [1, 2],
        'password': 5
    })
    assert response.status_code == 400

    response = client.post('/auth/user', json={
        'email': 'test',
        'password': 5
    })
    assert response.status_code == 400

    response = client.post('/auth/user', json={
        'email': 5,
        'password': 'test'
    })
    assert response.status_code == 400
