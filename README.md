# SheepyArt

Flask practice app, basically a classic DeviantArt ripoff
(The VidLii of DeviantArt?)

It's supposed to look like the 2008 layout, but even I don't remember
what that looked like. It might end up looking like an amalgamation of
2008 and 2010 dA. The VidLii of DeviantArt? nah.

Currently watching a dozen or so Flask tutorials,
including Corey Schafer's series - you'll see once you go into
my commit history >_<

## Features
  * Basic user authentication (login/logout)
  * Basic file upload
  * Database
  * Basic configuration through `definitions.json`

## Todo
  * Collections support

## Oddities
  * Importing global objects need to be done from `sheepyart.sheepyart`
  * Database located at `sheepyart/base.db`, definitions file located at `sheepyart/app/definitions.json`
  * Logs located at rootdir/`sheepyart.log`


## What to install first
Core dependencies
  * Python 3.7 (3.5 if using the `py35` branch)
  * Pipenv (make sure it's the Python 3 pipenv!)

PIL dependencies
  * libjpeg (`libjpeg-dev` in Debian and descendants)
  * zlib (`zlib1g-dev` in Debian and descendants)
  * ffi (`libffi-dev` in Debian and descendants)

## Run
  * Run `pipenv install`
  * Then `pipenv run python make_db.py`.
  * Then `pipenv run python main.py`.
