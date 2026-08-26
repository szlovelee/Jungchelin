from flask import Flask


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "개발용-비밀키"


from . import db, routes, services, utils


app.register_blueprint(db.bp)
app.register_blueprint(routes.bp)
app.register_blueprint(services.bp)
app.register_blueprint(utils.bp)