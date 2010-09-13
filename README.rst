Freddo is a web app for automating deployment/IT tasks.  It's inspired by
Etsy's deployinator.  But it's open source.  And a work in progress.

::

    git clone --recursive git://github.com/jbalogh/freddo.git
    cd freddo

    # Customize your settings_local.py:
    from settings import *
    SQLALCHEMY_DATABASE_URI = 'mysql://<user>:<password>@<host>:<port>/<db>'
    DEBUG = False

    # Set up Rabbit:
    rabbitmqctl add_user freddo freddo
    rabbitmqctl add_vhost freddo
    rabbitmqctl set_permissions -p freddo freddo '.*' '.*' '.*'

    # Set up MySQL:
    CREATE DATABASE freddo;

    # gogogo
    ./manage.py runserver
    ./manage.py celeryd -d
