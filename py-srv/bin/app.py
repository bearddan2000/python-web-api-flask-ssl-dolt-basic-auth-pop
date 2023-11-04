from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@db/beverage"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class PopModel(db.Model):
    __tablename__ = 'pop'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    color = db.Column(db.String())

    def __init__(self, name, color):
        self.name = name
        self.color = color

users = {
    'user': 'pass'
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return True
    return False

@app.route('/pop')
@auth.login_required
def handle_beverage():
        pops = PopModel.query.all()
        results = [
            {
                "name": pop.name,
                "color": pop.color
            } for pop in pops]

        return {"count": len(results), "pop": results, "message": "success"}


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5000, debug = True, ssl_context='adhoc')
