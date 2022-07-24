from sheepyart.sheepyart import app
import sys

# ------------------------- Run application -------------------------
if __name__ == "__main__":
    from logging.handlers import RotatingFileHandler

    # set up logger
    # TODO: logger: add dates to the logs config
    handler = RotatingFileHandler('sheepyart.log', maxBytes=10000, backupCount=1)
    app.logger.addHandler(handler)

    PORT=8000

    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])

    app.run(port=PORT, host='0.0.0.0', debug=True)
