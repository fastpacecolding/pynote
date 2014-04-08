pynote
======

pynote is a project to manage your notes on the commandline. It is
entirely written in Python 3 and provides a very handy cmd-interface.
You can browse the source code in `cgit`_ or in `github`_.
If something does not behave as expected please file a bug in github,
write an `email`_ or check out the `support thread`_ in the arch linux
forums.


features
--------

* create, delete, update, list and read notes
* compare revisions of a note by creating a unified diff
* list and restore deleted notes in trash
* everything is stored in human readable JSON files
* meta data for every note including creation time, updating time,
  deletion time, uuid, tags
* filter notes depending on its tags
* syntax highlighting using pygments for managing code snippets


planned
-------

* version control (diff revisions, revert revisions)
* export module


install
-------

In Arch Linux you can use the PKGBUILD in AUR_. Otherwise use::

    $ pip install pynote


.. Links:
.. _`cgit`: http://cgit.sevenbyte.org/pynote/
.. _`github`: https://github.com/statschner/pynote
.. _`release notes`: http://redmine.sevenbyte.org/projects/pynote/wiki/Releases
.. _`changelog`: http://cgit.sevenbyte.org/pynote/plain/CHANGES
.. _`bugtracker`: http://redmine.sevenbyte.org/projects/pynote
.. _`email`: stefan@sevenbyte.org
.. _`support thread`: https://bbs.archlinux.org/viewtopic.php?pid=1362268
.. _`via pypi`: http://pythonhosted.org//pynote/
.. _`contributing`: http://cgit.sevenbyte.org/pynote/plain/CONTRIBUTING
.. _`AUR`: https://aur.archlinux.org/packages/pynote/
