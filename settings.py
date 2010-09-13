DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql://<user>:<password>@<host>:<port>/<db>'

SECRET_KEY = ',-Xx,[grC(o&@Lxftz:i&*I`ZCHL+hPE'

## Celery
BROKER_HOST = 'localhost'
BROKER_PORT = 5672
BROKER_USER = 'freddo'
BROKER_PASSWORD = 'freddo'
BROKER_VHOST = 'freddo'
BROKER_CONNECTION_TIMEOUT = 0.1
CELERY_RESULT_BACKEND = 'amqp'
CELERY_IGNORE_RESULT = True
