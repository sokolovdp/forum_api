from forum import app


def test_index_returns_200():
    request, response = app.test_client.get('/topic/0')
    assert response.status == 200


def test_index_patch_not_allowed():
    request, response = app.test_client.patch('/topic/0')
    assert response.status == 405


test_index_returns_200()
test_index_patch_not_allowed()
