import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_apscheduler import APScheduler

def get_env_variable(name):
    try:
        print(os.getenv('THING'))
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

app = Flask(__name__)

load_dotenv()

app.app_context().push()

app.config['SECRET_KEY'] = 'mysecretkey'

POSTGRES_URL=get_env_variable("POSTGRES_URL")
POSTGRES_USER=get_env_variable("POSTGRES_USER")
POSTGRES_PW=get_env_variable("POSTGRES_PW")
POSTGRES_DB=get_env_variable("POSTGRES_DB")

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

from service.views.stock import update_tickers

scheduler = APScheduler()
scheduler.add_job(
    id = 'Scheduled task',
    func = update_tickers,
    trigger = 'cron',
    hour='13',
    minute='0'
)

scheduler.start()
