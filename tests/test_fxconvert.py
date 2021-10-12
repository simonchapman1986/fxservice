import json
import pytest
from unittest import mock
from app import app
from decimal import Decimal
from app.utils import convert, extract
from app.utils.response import response_builder
from app.utils.errors import UnprocessableEntity, ServiceUnavailable, NotFound


@pytest.fixture
def client():
    app.app.config["TESTING"] = True
    with app.app.test_client() as client:
        yield client


def test_healthcheck(client):
    response = client.get("/healthcheck")
    if response.status_code != 200:
        assert "wrong response code given {} != 200".format(response.status_code)


def test_missing_url_params(client):
    response = client.get("/convert?from=GBP&to=USD")
    data = json.loads(response.get_data(as_text=True))
    if response.status_code != 422:
        assert "wrong response code given {} != 422".format(response.status_code)


def test_client_param(client):
    response = client.get("/convert?from=GBP&to=USD&amount=1&client=test")
    data = json.loads(response.get_data(as_text=True))
    if response.status_code != 200:
        assert "wrong response code given {} != 422".format(response.status_code)
    elif data['client'] != "test":
        assert "wrong client given {} != test".format(response.client)


def test_monthly_url(client):
    response = client.get("/convert?from=GBP&to=USD&amount=1&client=test&method=avg")
    if response.status_code != 200:
        assert "wrong response code given {} != 422".format(response.status_code)


def test_client_param_default(client):
    response = client.get("/convert?from=GBP&to=USD&amount=1")
    data = json.loads(response.get_data(as_text=True))
    if response.status_code != 200:
        assert "wrong response code given {} != 422".format(response.status_code)
    elif data['client'] != "default":
        assert "wrong client given {} != default".format(response.client)


def test_date_bug(client):
    # same query from example 
    response = client.get("/convert?from=GBP&to=USD&amount=1&date=2021-03-09")
    if response.status_code == 500:
        assert "wdate big has returned ??".format(response.status_code)

def test_convert():
    result = convert.calculate_fx("1", "1.2")
    if result != Decimal("1.20"):
        assert 0


def test_response_builder():
    resp = response_builder(
        response_builder(
            success=True,
            from_="USD",
            to="GBP",
            amount="1",
            rate="1.20",
            date="2021-03-01",
            result="1.20",
        )
    )
    if resp.result != True:
        assert "wrong succ code given {} != True".format(resp.success)
