pynote
======

pynote is a project to manage your notes on the commandline. It is
entirely written in Python 3 and provides a very handy cmd-interface.
You can browse the source code in `cgit`_. A `github mirror`_ is also
available. **Checkout the `news`_ section in redmine and the CHANGES file
before updating!**

Please do not use any of these cool github pull requests because
they will mess up the git history (see CONTRIBUTING file)!

**The project is not stable yet! So be careful there might be large changes!**


features
--------

* create, delete, update, list and read notes
* list deleted notes in 'trash'
* everything is stored in human readable JSON files
* nice meta data for every note including creation time, updating time,
  deletion time, uuid, tags


planned
-------

* version control (diff revisions, revert revisions)
* trash to ensure you do not loose any data
* export module
* syntax highlighting using pygments for managing code snippets
* tags and filters


basic usage
-----------

At first you have to create the configfile ``noterc`` and the data
directory ``~/.note``. There is a script included to do this.::

    $ note-init


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


install
-------

In Arch Linux you can use the PKGBUILD in AUR_. Otherwise use
(add ``--pre`` for dev releases)::

    $ pip install pynote


.. Links:
.. _cgit: http://cgit.sevenbyte.org/pynote/
.. _`github mirror`: https://github.com/statschner/pynote
.. _`news`: http://redmine.sevenbyte.org/projects/pynote/news
.. _AUR: https://aur.archlinux.org/packages/pynote/
