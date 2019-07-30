'''
    SheepArt global object
'''

from os import path

# Base app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Haml + Sass support
from werkzeug import ImmutableDict
from flask_scss import Scss

# For the definition file
import json

# ------------------------- Definitions -------------------------

with open(path.join("sheepart", "app", "definitions.json"),"r") as def_files:
    # Load our JSON definition file as a dictionary that
    # we can use
    conf = json.load(def_files)

db_file = conf["db_file"]

# ------------------------- Control -------------------------
class Hamlisk(Flask):
    "Flask, but with HAMLish"
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
app.config['SECRET_KEY'] = conf["secret"]

# Make db
db = SQLAlchemy(app)

# Compile SCSS
Scss(app)
