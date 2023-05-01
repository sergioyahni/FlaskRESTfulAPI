from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return '<User %r>' % self.name


class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World!'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    db.create_all()  # sny
    app.run(debug=True)
