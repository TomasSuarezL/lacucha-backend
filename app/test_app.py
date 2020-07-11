

def test_root_route_connection(client):
    rv = client.get('/health')
    assert b'Ok' in rv.data
