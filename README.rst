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

In Arch Linux you can use the PKGBUILDs in the AUR. There is a git_ and a
stable_ version. Otherwise use::

    $ pip install pynote

.. _git: https://aur.archlinux.org/pkgbase/pynote-git/
.. _stable: https://aur.archlinux.org/pkgbase/pynote/


Install from source
-------------------

Clone the project with::

    $ git clone https://github.com/rumpelsepp/pynote.git

Install pynote with::

    $ python setup.py install

As mentioned before pynote is written in python 3. As I use the pathlib module
there is **at least python 3.4 required**. Maybe there are backports of pathlib
to python 3.3 or below but I have not tested them. If you did so please let me
know.


Quickstart
----------

For initialization just run any command and pynote will tell you what to do::

    $ note new "spam"
    Error: The directory /home/stefan/.note does not exist!
    You can create it with "mkdir /home/stefan/.note".

    $ mkdir /home/stefan/.note

    $ note new "spam"
    Error: The directory /home/stefan/.note/.trash does not exist!
    You can create it with "mkdir /home/stefan/.note/.trash".

    $ mkdir /home/stefan/.note/.trash

    $ note new "spam"
    Info: New note 'spam' created!


Create a new note::

    $ note new "spam"
    Info: New note 'spam' created!


List notes in a table::

    $ note list
    ID  Title         Age
    --  -----------   ---------
    0   spam          3 seconds
    1   lovely spam   1 day


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

    $ note edit 0
    $ note edit --title 0
    $ note edit --tags 0


Move a note to trash::

    $ note delete 0
    Info: Note 'spam' moved to trash!


Show trash::

    $ note list --trash
    ID  Title  Age
    --  -----  ----------
    0   spam   15 seconds


Restore a note from trash (remember to use the ID from trash)::

    $ note restore 0
    Info: Note 'spam' restored!


For help just pass ``--help`` to any command!
