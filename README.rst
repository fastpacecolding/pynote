pynote
======

pynote is a project to manage your notes on the commandline. It is written in
Python 3 and provides a very handy cmd-interface. You can browse the source
code in cgit_ or in github_. If something does not behave as expected please
file a bug in github, write an email_ or check out the `support thread`_ in the
arch linux forums.

Documentation is hosted on `Read the Docs`_.

.. _`cgit`: http://cgit.sevenbyte.org/pynote/
.. _`github`: https://github.com/statschner/pynote
.. _`email`: stefan@sevenbyte.org
.. _`support thread`: https://bbs.archlinux.org/viewtopic.php?pid=1362268
.. _`Read the Docs`: https://pynote.readthedocs.org


Install
-------

In Arch Linux you can use the PKGBUILDs in AUR_. Otherwise use::

    $ pip install pynote

.. _AUR: https://aur.archlinux.org/packages/?K=pynote


Install from source
-------------------

Clone the project with::

    $ git clone https://github.com/rumpelsepp/pynote.git

Install pynote with::

    $ python setup.py install


Quickstart
----------

Create a new note::

    $ note new "spam"

List notes in a table::

    $ note list
    ID  Title  Updated
    --  -----  ---------
    0   spam   3 seconds

Read a note (use the numeric ID from the table)::

    $ note show 0
    spam @ 2014-05-31 17:19, 48 seconds ago

    Spam, Spam, Spam, lovely Spam
    Wonderful Spam, Lovely Spam.
    Spam, Spam, Spam, magnificent Spam,
    Superlative Spam.
    Spam, Spam, Spam, wonderous Spam,
    Surgical Spam, splendiferous Spam.
    Spam, Spam, Spam, Spaaam!

Edit a note::

    $ note edit 1

Move a note to trash::

    $ note delete 1

Show trash::

    $ note trash

Restore a note from trash::

    $ note restore 1

For help just pass ``--help`` to any command!
