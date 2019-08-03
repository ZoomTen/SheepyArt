from sheepyart.sheepyart import app


# ------------------------- Run application -------------------------
if __name__ == "__main__":
    from logging.handlers import RotatingFileHandler

    # set up logger
    # TODO: logger: add dates to the logs config
    handler = RotatingFileHandler('sheepyart.log', maxBytes=10000, backupCount=1)
    app.logger.addHandler(handler)

    app.run(port='8000', host='0.0.0.0', debug=True)
