pynote
======

pynote is a project to manage your notes on the commandline. It is
entirely written in Python 3 and provides a very handy cmd-interface.
You can browse the source code in `cgit`_ or in `github`_.
If something does not behave as expected please file a bug in github,
write an `email`_ or check out the `support thread`_ in the arch linux
forums.

Documentation is hosted on `Read the Docs`_.

.. _`cgit`: http://cgit.sevenbyte.org/pynote/
.. _`github`: https://github.com/statschner/pynote
.. _`email`: stefan@sevenbyte.org
.. _`support thread`: https://bbs.archlinux.org/viewtopic.php?pid=1362268
.. _`Read the Docs`: https://pynote.readthedocs.org


features
--------

- create, delete, update, list and read notes
- compare revisions of a note by creating a unified diff
- list and restore deleted notes in trash
- everything is stored in human readable JSON files
- meta data for every note including creation time, updating time,
  deletion time, uuid, tags
- filter notes depending on its tags
- syntax highlighting using pygments for managing code snippets


planned
-------

- more version control (diff revisions, revert revisions)
- export module


install
-------

In Arch Linux you can use the PKGBUILD in AUR_. Otherwise use::

    $ pip install pynote

.. _AUR: https://aur.archlinux.org/packages/pynote/


install from source
-------------------

- Make sure you have installed babel_ and sphinx_.
- Clone the project with ``git clone https://github.com/rumpelsepp/pynote.git``
- Create docs and locales with ``make docs`` and ``make compile-locales``.
- Now you are ready to fire ``python setup.py install``.

.. _babel: http://babel.pocoo.org/
.. _sphinx: http://sphinx-doc.org/index.html
