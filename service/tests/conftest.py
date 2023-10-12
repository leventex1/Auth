import pytest
from service import create_app
from service.config.testconfig import TestConfig

@pytest.fixture()
def app():
    app = create_app(config=TestConfig)

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()