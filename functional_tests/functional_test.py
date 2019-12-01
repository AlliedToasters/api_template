import os
import pytest
import requests


@pytest.fixture
def base_url():
    key='BASE_URL'
    assert os.environ[key], 'Set the %s environment variable'.format(key)
    return os.environ[key]


def test_basic_response(base_url):
    resp = requests.post(base_url + '/somepath', json={"someKey": "someValue"})
    assert True
