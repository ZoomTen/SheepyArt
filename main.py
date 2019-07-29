from flask import Flask, g

# database
from flask_sqlalchemy import SQLAlchemy

# haml support
from werkzeug import ImmutableDict

# scss support
from flask_scss import Scss

# to parse definitions
import json

# App definitions
from app.browse import browse
from app.search import search

# db filename
db_file = 'base.db'

from datetime import datetime

# ------------------------- Control -------------------------
class Hamlisk(Flask):
    "Flask, but with HAML"
    jinja_options = ImmutableDict(
        extensions=['jinja2.ext.autoescape',
                    'jinja2.ext.with_',
                    'hamlish_jinja.HamlishExtension']
    )

    def __init__(self):
        Flask.__init__(self, __name__)

app = Hamlisk()

# HAMLish settings
app.jinja_env.hamlish_mode = 'indented'
app.jinja_env.hamlish_enable_div_shortcut = True

# App stuff
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file
app.config['SECRET_KEY'] = 'b1613a965683af63ca3f8673'

# Compile SCSS
Scss(app)

# ------------------------- Definitions -------------------------

with open("app/definitions.json","r") as def_files:
    conf = json.load(def_files)

# ------------------------- Model -------------------------
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    # avatar is a static image link
    avatar = db.Column(db.String(128), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    art = db.relationship('Art', backref='by', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.avatar}')"

class Art(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    # image is a static image link
    image = db.Column(db.String(128), nullable=False, default='art.jpg')
    # thumbnail is a static image link, default='default.jpg'
    thumbnail = db.Column(db.String(128), nullable=False, default='thumb.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    favorites = db.Column(db.Integer, nullable=False, default=0)
    views = db.Column(db.Integer, nullable=False, default=0)
    pubdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False, default='')
    tags = db.Column(db.String(256), nullable=False, default='')
    category = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Art('{self.title}', '{self.image}', '{self.category}', '{self.favorites}', '{self.views}', '{self.pubdate}')"

# ------------------------- View: register endpoints -------------------------


# Register all search categories
@app.context_processor
def quack_all():
    return dict(
    search_categories=conf["search_categories"]
    )

# Register all routes
app.register_blueprint(browse)
app.register_blueprint(search)

# ------------------------- Run application -------------------------
if __name__ == "__main__":
    # create database if it doesn't exist
    from os import path
    if path.isfile(db_file):
        pass
    else:
        db.create_all()

    app.run(port='8000', host='0.0.0.0', debug=True)
