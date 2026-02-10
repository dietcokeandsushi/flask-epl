#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///epl.sqlite'
#app.secret_key = b'MisecretKey'

#db = SQLAlchemy(app)
#migrate = Migrate(app, db)

#from epl import models, routes

from flask import Flask
from epl.extensions import db, migrate
from epl.core.routes import core_bp
from epl.clubs.routes import clubs_bp
from epl.players.routes import players_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/epl_s02'
    app.secret_key = b'MisecretKey'

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(core_bp, url_prefix='/')
    app.register_blueprint(clubs_bp, url_prefix='/clubs')
    app.register_blueprint(players_bp, url_prefix='/players')

    return app