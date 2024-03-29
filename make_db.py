from sheepyart.sheepyart import app
from sheepyart.sheepyart import db_file
from sheepyart.sheepyart import conf
from sheepyart.sheepyart import db
from sheepyart.app.models import User, Category
from flask_bcrypt import Bcrypt
from datetime import date

# ------------------------- Run application -------------------------
if __name__ == "__main__":
    # XXX: init: figure out how to do this automatically.

    # create database if it doesn't exist
    from os import path

    exists = path.isfile(path.join('sheepyart', db_file))

    db.create_all()
    print('Database automatically created.')

    # XXX: database: figure out making the migration stuff work
    listing = conf["categories"]

    # add parent categories
    parent_ids = {}
    for category in listing:
        category_add = Category(title=category)
        db.session.add(category_add)
        db.session.flush() # assign ids to categories
        parent_ids[category] = category_add.id

    # add subcategories
    for category in listing:
        for subcats in listing[category]:
            parent_cat_id = parent_ids[category]
            db.session.add(Category(title=subcats, parent_id=parent_cat_id))

    db.session.commit()
    print('Defaults added to database.')
