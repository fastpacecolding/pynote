pynote
======

pynote is a project to manage your notes on the commandline. It is
entirely written in Python 3 and provides a very handy cmd-interface.
You can browse the source code in `cgit`_. A `github mirror`_ is also
available. Checkout the `news`_ section in redmine and the `CHANGES`_ file
before updating!

Please do not use any of these cool github pull requests because
they will mess up the git history (see `CONTRIBUTING`_ file)!


features
--------

* create, delete, update, list and read notes
* compare revisions of a note by creating a (colored) unified diff
* list and restore deleted notes in trash
* everything is stored in human readable JSON files
* nice meta data for every note including creation time, updating time,
  deletion time, uuid, tags
* syntax highlighting using pygments for managing code snippets


planned
-------

* version control (diff revisions, revert revisions)
* export module
* tags and filters


basic usage
-----------

At first you have to create the configfile ``noterc`` and the data
directory ``~/.note``. There is a command included to do this.::

    $ note init


create a new note
`````````````````

::

    $ note new "spam"

Your editor (e.g. nano) will open and you can type in your content.


list notes
``````````

::

    $ note list
    +----+-------+------------------+
    | id | title | updated          |
    +----+-------+------------------+
    | 1  | spam  | 2013-12-09 10:59 |
    +----+-------+------------------+


edit note
`````````

::

    $ note edit 1

Your editor opens with the content of the note. After saving your
modifications she revision number is incremented.


delete note
```````````

::

    $ note delete 1


read a note
```````````

::

    $ note show 1
    +-------------------------------------------------+
    | title:    spam
    | created:  2013-12-09 10:59
    | updated:  2013-12-09 10:59
    | revision: 1
    | uuid:     188fcae5-86cf-4e5a-b955-35b38694bb43
    +-------------------------------------------------+

    Spam, Spam, Spam, lovely Spam
    Wonderful Spam, Lovely Spam.
    Spam, Spam, Spam, magnificent Spam,
    Superlative Spam.
    Spam, Spam, Spam, wonderous Spam,
    Surgical Spam, splendiferous Spam.
    Spam, Spam, Spam, Spaaam!


compare the revisions of a note
```````````````````````````````

::

    $ note compare 1 2 1
    --- spam, revision: 1   2013-12-18 18:22
    +++ spam, revision: 2   2013-12-18 18:23
    @@ -1,7 +1,6 @@
     Spam, Spam, Spam, lovely Spam
     Wonderful Spam, Lovely Spam.
    -Spam, Spam, Spam, magnificent Spam,
     Superlative Spam.
     Spam, Spam, Spam, wonderous Spam,
    -Surgical Spam, splendiferous Spam.
     Spam, Spam, Spam, Spaaam!
    +This is a change!


show trash
``````````

::

    $ note trash
    +----+--------+------------------+
    | id | title  | deleted          |
    +----+--------+------------------+
    | 1  | spam   | 2013-12-09 13:05 |
    | 0  | spam2  | 2013-12-09 13:04 |
    +----+--------+------------------+


restore a note from trash
`````````````````````````

::

    $ note restore 1


getting help
````````````

::

    $ note --help
    $ note show --help
    $ note compare --help
    $ man noterc
    and so on...


install
-------

In Arch Linux you can use the PKGBUILD in AUR_. Otherwise use::

    $ pip install pynote


.. Links:
.. _cgit: http://cgit.sevenbyte.org/pynote/
.. _`github mirror`: https://github.com/statschner/pynote
.. _`news`: http://redmine.sevenbyte.org/projects/pynote/news
.. _`CHANGES`: http://cgit.sevenbyte.org/pynote/tree/CHANGES
.. _`CONTRIBUTING`: http://cgit.sevenbyte.org/pynote/tree/CONTRIBUTING?h=develop
.. _AUR: https://aur.archlinux.org/packages/pynote/
