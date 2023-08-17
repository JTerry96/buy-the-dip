import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import psycopg2

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

# the values of those depend on your setup
POSTGRES_URL=get_env_variable("POSTGRES_URL")
POSTGRES_USER=get_env_variable("POSTGRES_USER")
POSTGRES_PW=get_env_variable("POSTGRES_PW")
POSTGRES_DB=get_env_variable("POSTGRES_DB")

app = Flask(__name__)

app.app_context().push()

app.config['SECRET_KEY'] = 'mysecretkey'

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=POSTGRES_USER,
    pw=POSTGRES_PW,
    url=POSTGRES_URL,
    db=POSTGRES_DB
)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

from service.schemas import stock

from service.views.stock import stock_blueprint

app.register_blueprint(stock_blueprint, url_prefix='')
