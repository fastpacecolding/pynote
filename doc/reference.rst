Reference Guide
===============

.. note::
    Every command is to be used like ``$ note cmd``, e.g. ``$ note list``.
    Every command supports the ``-h, --help`` option.

.. note::
    This page has to be cleaned up for pynote 1.0


note
----

This is the root command of pynote. It supports a few options as well.

.. cmdoption:: --no-pager

    Supress paging.

.. cmdoption:: --no-header

    Supress the header.


list
----

This prints out a table with all stores notes. This is the default
command if you pass nothing to ``$ note``. The columns are sorted by
the updated time::

    $ note list
    ID  Title   Age
    --  ------  ---------
    0   spam    3 seconds


.. cmdoption:: --tags TAGS

    Filter appropriate tags. You can pass several tags just like this: ``note
    list --tags "tag1 tag2"``

.. cmdoption:: -e, --extended

    Add a tags column to the table.


show
----

Shows a specific note including a header with some metadata. You have
to pass the numeric id of the note to show, e.g. ``$ note show 0``::

    $ note show 0
    spam @ 2014-05-31 17:19, 48 seconds ago

    Spam, Spam, Spam, lovely Spam
    Wonderful Spam, Lovely Spam.
    Spam, Spam, Spam, magnificent Spam,
    Superlative Spam.
    Spam, Spam, Spam, wonderous Spam,
    Surgical Spam, splendiferous Spam.
    Spam, Spam, Spam, Spaaam!


.. cmdoption:: -l LANG, --lang LANG

    Use pygments for synthax-highlighting. It is nice for storing
    code snippets into pynote. You have to pass the programming
    language, e.g. ``$ note show 5 -l python``.


new
---

Your editor (e.g. nano) opens and you can type in your content.


edit
----

Your editor opens with the content of the note. After saving the note will
be updated. You choose between editing the content, title and tags.


.. cmdoption:: --title

    Edit the title instead of the content.

.. cmdoption:: --tags

    Edit attached tags. Every line in the editor indicates one tag.


delete
------

Move a note to trash.


trash
-----

Prints out all delete notes in a table::

    $ note trash
    +----+--------+------------------+
    | id | title  | deleted          |
    +----+--------+------------------+
    | 1  | spam   | 2013-12-09 13:05 |
    | 0  | spam2  | 2013-12-09 13:04 |
    +----+--------+------------------+


restore
-------

Restore a delete note from trash. You have to use the numeric id
from ``$ note trash``.


revisions
---------

Shows all available revisions of a note as a table::

    $ note revisions 8
    There are 2 revisions of 'spam':

    +----------+---------------+------------------+
    | revision | title         | updated          |
    +----------+---------------+------------------+
    | 2        | spam          | 2014-01-12 13:04 |
    | 1        | my silly spam | 2014-01-06 22:31 |
    +----------+---------------+------------------+


compare
-------

Create a unified diff of two notes. Pass the numeric id of a note
and the two revision numbers which you want to compare. This command
supports colors::

    $ note compare 1 2 1
    --- my silly spam, revision: 1   2014-01-06 22:31
    +++ spam, revision: 2   2014-01-12 13:04
    @@ -1,7 +1,6 @@
     Spam, Spam, Spam, lovely Spam
     Wonderful Spam, Lovely Spam.
    -Spam, Spam, Spam, magnificent Spam,
     Superlative Spam.
     Spam, Spam, Spam, wonderous Spam,
    -Surgical Spam, splendiferous Spam.
     Spam, Spam, Spam, Spaaam!
    +This is a change!


.. cmdoption:: -c, --color

    Use colors!


tags
----

View, delete or add tags. This command is quite new and maybe some features
are missing. A tag is just an arbitrary string. A note can contain multiple
tags. If no arguments are passed to this commands it prints out all tags
which are used in the database::

    $ note tags
    The following tags exist:
    foo
    bar

If a numeric id of a note is passed to this command it prints out the tags
of this note::

    $ note tags 1
    Note 1, spam, is tagged with:
    foo
    bar

For deleting and adding tags checkout out the accepted options!


.. cmdoption:: -a ADD, --add ADD

    Add one or more tags to a note. ``$ note tags 1 --add "foo"``

.. cmdoption:: -d DELETE, --delete DELETE

    Remove one or more tags from a note, ``$ note tags 1 --delete "foo"``
