from flask import Flask

app = Flask(__name__)


from . import db, routes, services, utils 

app.register_blueprint(db.bp)
app.register_blueprint(routes.bp)
app.register_blueprint(services.bp)
app.register_blueprint(utils.bp)
