Noterc
======

Synopsis
--------

Pynote is configured with a ressource file in your home directory.
The location of this file is ``~/.noterc``. The synthax of this file
is quite easy. It is formatted as a line-separated list of ``KEY=VALUE``
pairs, blank lines, and lines starting with ``#``, are ignored.
The whole documatation of this synthax is located in the official
`Python Documentation`_.

.. _`Python Documentation`: http://docs.python.org/3.3/library/configparser.html#quick-start

Please ensure you have a ``[DEFAULT]`` section on top of your file.
Support for additional sections may come in future releases...


Settings
--------

data
    Specifies the place where your stored notes live. ``~`` is to be
    expanded to your homedir. You can set this location e.g. to your
    Dropbox directory to ensure automatic syncing of your notes.
    **Default**: ``~/.note``

dateformat
    Set the default dateformat for all dates shown in pynote.
    It must be a string like e.g. ``YYYY-MM-dd HH:mm``, see `babel docs`_.
    The values "full", "long", "medium", or "short" are allowed as well,
    but you may have to set *locale*.
    **Default**: ``YYYY-MM-dd HH:mm``

.. _`babel docs`: http://babel.pocoo.org/docs/dates/#date-fields

locale
    Set the locale for datetime formatting. **Default: en_US**

reldates
    Use relative dates in your notes table. **Values: yes, no;
    Default: no**

ignore_suffixes
    Ignore files in the notes folder with a specific suffic, e.g. '.pdf'.
    It may be useful if you store other files, such as pdfs, in your
    notes directory. This configuration value must be a valid JSON string.
    **Default: []**

editor
    The command line editor which is used to create and edit notes.
    If it is not present pynote takes the environment variable ``$EDITOR``.

pygments_theme
    Choose the pygments theme for synthax highlighting things. If it is
    not present it takes the value ``default``. The following values are
    supported:

    * vs
    * trac
    * fruity
    * borland
    * pastie
    * bw
    * native
    * emacs
    * murphy
    * manni
    * monokai
    * perldoc
    * vim
    * tango
    * friendly
    * autumn
    * rrt
    * colorful
    * default


Example Noterc File
-------------------

::

    [DEFAULT]
    data = ~/Dropbox/.note/
    dateformat = medium
    reldates = yes
    ignore_suffixes = [".pdf", ".odt"]
    locale = de_DE
    editor = vim
    pygments_theme = monokai


Bugs
----

Bugs? You must be kidding; there are no bugs in this software. But if
this crazy thing happens write an email to stefan@sevenbyte.org or checkout
the bugtracker on github https://github.com/rumpelsepp/pynote
