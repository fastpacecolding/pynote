Reference Guide
===============

.. note::
    * Every command is to be used like ``$ note cmd``, e.g. ``$ note list``.
    * Every command can be shortened like ``$ note list`` -> ``$ note li``.
      Pynote detects the matching command automatically.
    * Every command supports the ``-h, --help`` option.


note
----

This is the root command of pynote. It supports a few options as well.

.. cmdoption:: --no-pager

    Supress paging.

.. cmdoption:: --no-header

    Supress the header.

.. cmdoption:: --version

    Show the version and exit.


list
----

This prints out a table with all stores notes. This is the default
command if you pass nothing to ``$ note``. The columns are sorted by
the updated time::

    $ note list
    ID  Title         Age
    --  -----------   ---------
    0   spam          3 seconds
    1   lovely spam   1 day


.. cmdoption:: --tags TAGS

    Filter appropriate tags. You can pass several tags just like this: ``note
    list --tags "tag1 tag2"``

.. cmdoption:: -e, --extended

    Add a tags column to the table.

.. cmdoption:: --trash

    List the content of trash instead.


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

.. cmdoption:: -w, --wrap-text

    Wrap output at 70 signs. This may be useful if you want to read
    a badly formatted note on the terminal.


all
---

Just prints out all notes.


new
---

Your configured editor (e.g. nano) opens and you can type in your content.
You have to pass the title of the note like this::

    $ note new "wonderful spam"


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

Move a note to trash. The note will be moved to ``trash_path`` which
can be configured explicitly and which defaults to ``data_path/.trash``.


restore
-------

Restore a delete note from trash. You have to use the numeric id
from ``$ note list --trash``.


conf
----

Show all configuration values for debugging reasons::

    $ note conf
    global_config      /etc/noterc
    local_config       /home/stefan/.noterc
    data_path          /home/stefan/.note
    trash_path         /home/stefan/.note/.trash
    editor             vim
    colors             False
    dateformat         YYYY-MM-dd HH:mm
    reldates           False
    locale             en_US
    extension
    ignore_extensions  []
    pygments_theme     default
