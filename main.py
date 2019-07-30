from sheepart.sheepart import app, db, db_file


# ------------------------- Run application -------------------------
if __name__ == "__main__":
    # create database if it doesn't exist
    from os import path
    if path.isfile(db_file):
        pass
    else:
        db.create_all()

    app.run(port='8000', host='0.0.0.0', debug=True)
