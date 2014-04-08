Commands
========

.. note::
    Every command is to be used like ``$ note cmd``, e.g. ``$ note list``.
    Every command supports the ``-h, --help`` option.


list
----

``usage: note list [-h]``

This prints out a table with all stores notes. This is the default
command if you pass nothing to ``$ note``. The columns are sorted by
the updated time.

::

    $ note list
    +----+-------+------------------+
    | id | title | updated          |
    +----+-------+------------------+
    | 0  | spam  | 2013-12-09 10:59 |
    +----+-------+------------------+


show
----

``usage: usage: note show [-h] [-a] [-n] [-l LANG] [key]``

Shows a specific note including a header with some metadata. You have
to pass the numeric id of the note to show, e.g. ``$ note show 0``.

::

    $ note show 1
    +-------------------------------------------------+
    | title:    spam
    | created:  2013-12-09 10:59
    | updated:  2013-12-09 10:59
    | revision: 1
    | tags:     foo, bar
    | uuid:     188fcae5-86cf-4e5a-b955-35b38694bb43
    +-------------------------------------------------+

    Spam, Spam, Spam, lovely Spam
    Wonderful Spam, Lovely Spam.
    Spam, Spam, Spam, magnificent Spam,
    Superlative Spam.
    Spam, Spam, Spam, wonderous Spam,
    Surgical Spam, splendiferous Spam.
    Spam, Spam, Spam, Spaaam!


**Accepted options**

``-n, --no-header``
    Supresses the header.

``-a, --all``
    Print out every active note. Supressing the header is supported
    as well. Passing a numeric id is not mandatory.

``-l LANG, --lang LANG``
    Use pygments for synthax-highlighting. It is nice for storing
    code snippets into pynote. You have to pass the programming
    language, e.g. ``$ note show 5 -l python``.


new
---

``usage: usage: note new [-h] title``

Your editor (e.g. nano) opens and you can type in your content.


edit
----

``usage: usage: note edit [-h] [-t] key``

Your editor opens with the content of the note. After saving your
modifications the revision number is incremented.


**Accepted options**

``-t, --title``
    Edit the title instead of the content.


delete
------

``usage: note delete [-h] key``

Move a note to trash.


trash
-----

``usage: note trash [-h]``

Prints out all delete notes in a table.

::

    $ note trash
    +----+--------+------------------+
    | id | title  | deleted          |
    +----+--------+------------------+
    | 1  | spam   | 2013-12-09 13:05 |
    | 0  | spam2  | 2013-12-09 13:04 |
    +----+--------+------------------+


restore
-------

``usage: note restore [-h] key``

Restore a delete note from trash. You have to use the numeric id
from ``$ note trash``.


revisions
---------

``usage: note revisions [-h] key``

Shows all available revisions of a note as a table.

::

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

``usage: note compare [-h] [-n] key to_rev from_rev``

Create a unified diff of two notes. Pass the numeric id of a note
and the two revision numbers which you want to compare. This command
uses colors by default.

.. note::
    I think i will change the behaviour. I think it's better to make
    colors optional with ``-c, --colors``.

::

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


**Accepted options**

``-n, --no-color``
    Supress colors!


init
----

``usage: note init [-h] [--config | --force]``

Create an inital ``~/.noterc`` and a data directory. This command
is interactive and asks you what it should do.


**Accepted options**

``--config``
    Only create a new ``~/.noterc``. Useful when you have messed up
    your previous ``~/.noterc`` or when you want to check out the
    defaults.

``--force``
    Overwrite an existing ``~/.noterc``.


tags
----

``usage: note tags [-h] [-a ADD [ADD ...] | -d DELETE [DELETE ...]] [key]``

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


**Accepted options**

``-a ADD, --add ADD``
    Add one or more tags to a note. ``$ note tags 1 --add "foo"``

``-d DELETE, --delete DELETE``
    Remove one or more tags from a note, ``$ note tags 1 --delete "foo"``
