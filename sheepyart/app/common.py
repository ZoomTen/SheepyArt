"""SheepyArt Common Functions"""

from sheepyart.app.models import Art, Category, User
from flask import escape, url_for

def make_user_gallery(user, num_entries=0, sort_new=False):
    """Makes a user gallery.

    This is a processor for `make_gallery` which takes a User
    and finds all the art pieces created by that User, then
    passes it through the generic `make_gallery` function.

    Args:
        user(User): A User object from which to extract art entries.
                    This *cannot* be None or other types.
        num_entries(Int): The number of entries to generate. This defaults
                        to 0, for showing all entries from the user. A value
                        of 1 will show the oldest/newest entries, depending
                        on the `sort_new` value.
                        Any value lower than 0 will result in an
                        AssertionError.
        sort_new(Bool): Whether or not to sort by the newest art
                        in the collection.

    """
    art = Art.query.filter_by(by=user)

    return make_gallery(art=art, num_entries=num_entries,
                        sort_new=sort_new)


def make_category_gallery(category, num_entries=0, sort_new=False):
    """Makes a category gallery.

    This is a processor for `make_gallery` which takes a Category
    and finds all the art pieces placed on that Category, then
    passes it through the generic `make_gallery` function.

    Args:
        category(Category): A Category object from which to extract art entries.
                    This can be None, if you wish to extract art from all
                    categories.
        num_entries(Int): The number of entries to generate. This defaults
                        to 0, for showing all entries from the user. A value
                        of 1 will show the oldest/newest entries, depending
                        on the `sort_new` value.
                        Any value lower than 0 will result in an
                        AssertionError.
        sort_new(Bool): Whether or not to sort by the newest art
                        in the collection.

    """
    if category is None:
        # NOTE: common: what is this
        art = Art.query.filter_by()
    else:
        art = Art.query.filter_by(category=category.id)

    return make_gallery(art=art, num_entries=num_entries,
                        sort_new=sort_new)


def make_gallery(art, num_entries=0, sort_new=False):
    """Makes gallery entries, sorted by oldest or newest.

    This fetches n art entries (n=num_entries) from
    a BaseQuery of the Art object. They may be sorted by new or otherwise.

    Args:
        query(BaseQuery): An SQLAlchemy BaseQuery object of the Art column which
                    is already filtered by the `make_*_gallery` functions.
        num_entries(Int): The number of entries to generate. This defaults
                        to 0, for showing all entries from the user. A value
                        of 1 will show the oldest/newest entries, depending
                        on the `sort_new` value.
                        Any value lower than 0 will result in an
                        AssertionError.
        sort_new(Bool): Whether or not to sort by the newest art
                        in the collection.

    Returns:
        A List, containing Dict mappings with the following format:

        {
            "title": "Mage Reference Sheet",
            "id": 10,
            "link": "/art/10",
            "thumb": "/static/thumbnail/INSERTHASHHERE_thumb.jpg",
            "catid": 35,
            "catname": "Refsheet/DnD",
            "catlink": "/browse/35?page=0",
            "byname": "dndgreg",
            "bylink": "/user/dndgreg",
            "byid": 256
        }
    """
    assert num_entries >= 0, "num_entries cannot be negative!"

    # NOTE: common: ticky tacky I'm on the keyboard
    if sort_new:
        if num_entries > 0:
            entries = art.order_by(Art.pubdate.desc()).limit(num_entries).all()
        else:
            entries = art.order_by(Art.pubdate.desc()).all()
    else:
        if num_entries > 0:
            entries = art.limit(num_entries).all()
        else:
            entries = art.all()

    gallery = []
    for entry in entries:
        catname = ""
        cat = Category.query.get(entry.category)
        if cat.parent_id is not None:
            par_cat = Category.query.get(cat.parent_id)
            catname = f"{par_cat.title}/{cat.title}"
        else:
            catname = f"{cat.title}"

        # FIXME: common: catlink is supposed to be the link to category. needs implementing.
        gallery.append(
                        {
                            "title": escape(entry.title),
                            "id": entry.id,
                            "link": url_for('art.view_art', art_id=entry.id),
                            "thumb": url_for('static',
                                             filename='thumbnail/'
                                             + entry.thumbnail),
                            "catid": cat.id,
                            "catname": catname,
                            "catlink": "#",
                            "byname": escape(entry.by.username),
                            "bylink": url_for('userpage.view_userpage',
                                               username=escape(entry.by.username)
                                               ),
                            "byid": entry.by.id
                            }
                        )
    return gallery