import pytest
import warnings

from app import main, data, app
from app.data import RedisWrapper
import redis
from redis.exceptions import ConnectionError

from fastapi import FastAPI
from starlette.testclient import TestClient

@pytest.fixture
def client():
    #app.config['TESTING'] = True
    client = TestClient(app)
    yield client

def redis_wrapper_suite(r):
    """runs suite of tests on RedisWrapper"""
    starting_length =  len(r)
    r.set('__test', '10')
    out = r.get('__test', None)
    assert out == '10'
    out2 = r.get('__null_test', None)
    assert out2 is None
    out3 = r.get('__null_test', '[]')
    assert out3 == '[]'
    assert len(r) == starting_length + 1
    r.delete('__test')
    assert len(r) == starting_length

def test_redis_wrapper_dict():
    """test using dictionary as datastore"""
    r = RedisWrapper(use_dict=True)
    redis_wrapper_suite(r)

def test_redis_wrapper_redis():
    """test using reddis client as datastore"""
    r = RedisWrapper()
    try:
        assert r.type == 'dict'
        run_test=True
    except AssertionError:
        msg = 'WARNING-- redis server not found. Skipping redis test...'
        with pytest.warns(UserWarning):
            warnings.warn(msg, UserWarning)
        run_test=False
    if run_test:
        redis_wrapper_suite(r)

def test_healthcheck(client):
    resp = client.get('/healthcheck')
    assert resp.status_code == 200
    assert resp.json()['status'] == 'ok'

def test_request(client):
    request_json = {
      "someKey": "someValue"
    }
    resp = client.post("/some_path", json=request_json)
    assert resp.status_code == 200
    assert True

def test_400_on_missing_search_arg(client):
    resp = client.post("/some_path", json={
      "invalid__key": "value!"
    })
    assert resp.status_code == 400

def test_400_on_bad_json(client):
    resp = client.post("/some_path", data={
      "someKey": "someValue"
    })
    assert resp.status_code == 400
