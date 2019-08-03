"""SheepyArt Common Functions"""

from sheepyart.app.models import Art, Category, User
from flask import escape, url_for

# Sanitizing
from sheepyart.sheepyart import scrub

# Markdown parsing
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension


def parse_markdown(input):
    """Parses a Markdown input.

    This wraps around Python Markdown, converting the Markdown string
    to HTML and sanitizes it. The Markdown flavor used in this app is
    GFM (GitHub's markdown), and the sanitization depends on the settings
    specified in sheepyart.py.

    Args:
        input(String): A Markdown-formatted string

    Returns:
        An HTML-formatted String that has already been sanitized.
    """
    convert = markdown.markdown(input,
                                extensions=[GithubFlavoredMarkdownExtension()]
                                )
    return scrub.clean(convert)


def make_user_gallery(user, num_entries=0, sort_new=False, offset=0):
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
        offset(Integer): Offset entries by x entries.

    Returns:
        A List, see make_gallery.
    """
    art = Art.query.filter_by(by=user)

    return make_gallery(art=art, num_entries=num_entries,
                        sort_new=sort_new, offset=offset)


def make_category_gallery(category, user=None, num_entries=0, sort_new=False, offset=0):
    """Makes a category gallery.

    This is a processor for `make_gallery` which takes a Category
    and finds all the art pieces placed on that Category, then
    passes it through the generic `make_gallery` function.

    Args:
        category(Category): A Category object from which to extract art entries.
                    This can be None, if you wish to extract art from all
                    categories.
        user(User): If specified, this will return art entries of a specific
                    category from a specific user.
        num_entries(Int): The number of entries to generate. This defaults
                        to 0, for showing all entries from the user. A value
                        of 1 will show the oldest/newest entries, depending
                        on the `sort_new` value.
                        Any value lower than 0 will result in an
                        AssertionError.
        sort_new(Bool): Whether or not to sort by the newest art
                        in the collection.
        offset(Integer): Offset entries by x entries.

    Returns:
        A List, see make_gallery.
    """
    # XXX: common: this probably isn't good
    if category:
        if category.parent_id is None:
            catlist = Category.query.filter_by(parent_id=category.id).all()
            if user:
                art = Art.query.filter_by(category=category.id, by=user)
                for cat in catlist:
                    art = art.union(Art.query.filter_by(category=cat.id,
                                                        by=user))
            else:
                art = Art.query.filter_by(category=category.id)
                for cat in catlist:
                    art = art.union(Art.query.filter_by(category=cat.id))
        else:
            if user:
                art = Art.query.filter_by(category=category.id, by=user)
            else:
                art = Art.query.filter_by(category=category.id)
    else:
        art = Art.query.filter_by()

    return make_gallery(art=art, num_entries=num_entries,
                        sort_new=sort_new, offset=offset)


def make_gallery(art, num_entries=0, sort_new=False, offset=0):
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
        offset(Integer): Offset entries by x entries.

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
            entries = art.order_by(Art.pubdate.desc()).limit(num_entries).offset(offset).all()
        else:
            entries = art.order_by(Art.pubdate.desc()).offset(offset).all()
    else:
        if num_entries > 0:
            entries = art.limit(num_entries).offset(offset).all()
        else:
            entries = art.offset(offset).all()

    gallery = []
    for entry in entries:
        catname = ""
        cat = Category.query.get(entry.category)
        if cat.parent_id is not None:
            par_cat = Category.query.get(cat.parent_id)
            catname = f"{par_cat.title}/{cat.title}"
        else:
            catname = f"{cat.title}"

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
                            "catlink": url_for('browse.do_browse') + f"?cat={entry.category}",
                            "byname": escape(entry.by.username),
                            "bylink": url_for('userpage.view_userpage',
                                               username=escape(entry.by.username)
                                               ),
                            "byid": entry.by.id
                            }
                        )
    return gallery
