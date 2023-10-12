class TestConfig(object):
    TESTING=True
    DEBUG=True
    SECRET_KEY='secret'
    ACCESS_EXP_MINUTES=1
    REFRESH_EXP_DAYS=1
    SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'