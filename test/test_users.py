import pytest

from jose import jwt

from app import schemas
from app.config import settings
from test.conftest import test_user

#def test_root(client):
#    res = client.get("/")
#    print(res.json().get('message'))
#    assert res.json().get('message') == 'Hello World'
#    assert res.status_code == 200

def test_create_user(client):
    res=client.post(
        "/users/", json={"email": "test123@mail.com",
                         "password": "abc123"}
    )
    #print(res.json())
    new_user=schemas.UserResponse(**res.json())

    assert new_user.email == 'test123@mail.com'
    assert res.status_code == 201


def test_login_user(client, test_user):
    res=client.post(
        "/login", data={"username": test_user['email'],
                        "password": test_user['password']}
    )

    login_res=schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key,
                         algorithms=[settings.algorithm])
    id=payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type=="bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code",[
    ('wrongEmail@mail.com', 'abc123', 403),
    ('test123@mail.com', 'wrongPassword', 403),
    ('wrongEmail@mail.com', 'wrongPassword', 403),

    (None, 'abc123', 422),
    ('test123@mail.com', None, 422)
])

def test_incorrect_login(client, email, password, status_code):
    res=client.post(
        "/login", data={"username": email,
                        "password": password}
    )

    assert res.status_code == status_code
    #assert res.json().get('detail') == "Invalid Credentials"