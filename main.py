from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'your_database_name.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable a warning

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Create a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

# Create a UserSchema for serialization/deserialization
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/user", methods=["POST"])
def add_user():
    username = request.json["username"]
    email = request.json["email"]
    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

#endpoint update a user
@app.route("/user/<id>",methods=["put"])
def update_user(id):
  user = User.query.get(id)
  name  = request.json['username']
  email = request.json['email']
  user.username  = name
  user.email = email
  db.session.commit()
  return user_schema.jsonify(user)   
@app.route("/user/<id>", methods=["delete"])
def delete_user(id):
   user =User.query.get(id)
   db.session.delete(user)
   db.session.commit()
   return user_schema.jsonify(user)
     
#endpoint get one user
@app.route("/user/<id>",methods=["GET"])
def get_oneuser(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0", debug=True)

