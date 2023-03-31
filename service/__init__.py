import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.app_context().push()

app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# created database
db = SQLAlchemy(app)
# abilities to migrate that db
Migrate(app,db)

db.create_all()
db.session.commit()

from service.views.views import relationship_blueprint

app.register_blueprint(relationship_blueprint, url_prefix='')
