from sheepyart.sheepyart import app, db, db_file

from logging.handlers import RotatingFileHandler

# ------------------------- Run application -------------------------
if __name__ == "__main__":
    # set up logger
    # FIXME: logger: add dates to the logs config
    handler = RotatingFileHandler('sheepyart.log', maxBytes=10000, backupCount=1)
    app.logger.addHandler(handler)

    # create database if it doesn't exist
    from os import path
    if path.isfile(path.join('sheepyart', db_file)):
        pass
    else:
        db.create_all()
        app.logger.info('Database automatically created.')

    app.run(port='8000', host='0.0.0.0', debug=True)
