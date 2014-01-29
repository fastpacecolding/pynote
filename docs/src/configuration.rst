Configuration
=============

Pynote is configured with a ressource file in your home directory.
The location of this file is ``~/.noterc``. The synthax of this file
is quite easy. It is formatted as a line-separated list of KEY=VALUE
pairs, blank lines, and lines starting with ``#``, are ignored.
The whole documatation of this file is located in the official python
`documentation`_.

.. _`documentation`: http://docs.python.org/3.3/library/configparser.html#quick-start

The default ``~/.noterc`` can be created with the ``init`` command of
pynote. If you just want to create you can use the `--config` option,
see :doc:`commands`. Please ensure you have a ``[DEFAULT]`` section on top
of your file. Support for additional sections may come in future releases...

The folowing keywords are supported. You also find this list in the
shipped manpage with ``$ man noterc``.

`data`
    Specifies the place where your stored notes live. ``~`` is to be
    expanded to your homedir. You can set this location e.g. to your
    Dropbox directory to ensure automatic syncing of your notes.

`dateformat`
    Set the default dateformat for all dates shown in pynote.
    It must be a string like e.g. ``d.m.Y H:M``.

`editor`
    The command line editor which is used to create and edit notes.
    If it is not present pynote takes the environment variable ``$EDITOR``.

`pygments_theme`
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
