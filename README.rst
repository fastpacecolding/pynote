pynote is a project to manage your notes on the commandline. It is
entirely written in Python 3 and provides a very handy cmd-interface.

**The project is not stable yet! So be careful!**


features
========

* create, delete, update and read notes
* everything is stored in human readable JSON files
* nice meta data for every note including creation time, updating time,
  deletion time, uuid, tags


planned
=======

* version control (diff revisions, revert revisions)
* trash to ensure you do not loose any data
* export module
* syntax highlighting using pygments for managing code snippets
* tags and filters


basic usage
===========

create a new note
-----------------

::

    $ note new "blub"

Your editor (e.g. nano) will open and you can type in your content.


list notes
----------

::

    $ note list
    +----+-------+------------------+
    | id | title | updated          |
    +----+-------+------------------+
    | 1  | blub  | 2013-12-09 10:59 |
    +----+-------+------------------+


edit note
---------

::

    $ note edit 1


delete note
-----------

::

    $ note delete 1


read a note
-----------

::

    $ note show 1
    +-------------------------------------------------+
    | title:    blub
    | created:  2013-12-09 10:59
    | updated:  2013-12-09 10:59
    | revision: 1
    | uuid:     188fcae5-86cf-4e5a-b955-35b38694bb43
    +-------------------------------------------------+

    foo is bar



install
=======

In Arch Linux you can use the attached PKGBUILD in ``dist``.
Otherwise use:

::

    $ pip install pynote


You can also browse the source code in cgit: http://cgit.sevenbyte.org/pynote/
