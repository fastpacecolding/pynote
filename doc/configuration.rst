Noterc
======

Synopsis
--------

Pynote is configured with a local ressource file in your home directory
(``~/.noterc``) and a global one in ``/etc/noterc``. The local ressource file
overwrites the global one. Their synthax is quite easy. It is formatted as a
line-separated list of ``KEY=VALUE`` pairs, blank lines, and lines starting
with ``#``, are ignored.  Please ensure you have a ``[DEFAULT]`` section on top
of your file. The whole documatation of the synthax is located here:
http://docs.python.org/3.4/library/configparser.html#quick-start



Settings
--------

data
    Specifies the place where your stored notes live. ``~`` is to be
    expanded to your homedir. You can set this location e.g. to your
    Dropbox directory to ensure automatic syncing of your notes.

    **Default**: ``~/.note``

colors
    Activate colorized output. Pynote automatically detects whether the output
    supports colors. If you redirect pynote's output into a file ANSI color
    codes will be stripped. You may have to add ``export PAGER=less -R`` to
    your .bashrc or .zshrc for color support in the pager.

    **Default**: no

dateformat
    Set the default dateformat for all dates shown in pynote.
    It must be a string like e.g. ``YYYY-MM-dd HH:mm``, see
    http://babel.pocoo.org/docs/dates/#date-fields.
    The values "full", "long", "medium", or "short" are allowed as well,
    but you may have to set *locale*.

    **Default**: ``YYYY-MM-dd HH:mm``

locale
    Set the locale for datetime formatting. This will affect the formatting in
    the age column if you use reldates.

    **Default**: en_US

reldates
    Use relative dates in your notes table. This option accepts 'yes' or 'no'.

    **Default**: no

extension
    Specifiy a extension which should be added to the filename of each note.
    This might be useful for using markup languages (such as rst, asciidoc,
    markdown...) and synthax highlighting in your editor. You have to include
    the dot.

    **Default**: None

ignore_extension
    Ignore files in the notes folder with a specific extension, e.g. '.pdf'.
    It may be useful if you store other files, such as pdfs, in your
    notes directory. This configuration value must be a valid JSON string.

    **Default**: ``[]``

editor
    The command line editor which is used to create and edit notes.
    You can pass additional arguments to the editor as well, e.g.
    ``vim -c "set ft=asciidoc"``. If it is not present pynote will take
    the environment variable ``$EDITOR``. If ``$EDITOR`` is not set this
    value will fall back to ``'nano'``.

pygments_theme
    Choose the pygments theme for synthax highlighting things. You'll find
    instructions to get all supported values on the pygments webpage here:
    http://pygments.org/docs/styles/#getting-a-list-of-available-styles

    **Default**: default


Example Noterc File
-------------------

::

    [DEFAULT]
    data = ~/Dropbox/.note/
    editor = vim
    pygments_theme = monokai

    # Dateformat settings
    dateformat = medium
    reldates = yes
    locale = de_DE

    # File extension settings
    extension = .rst
    ignore_extensions = [".pdf", ".odt"]


Bugs
----

Bugs? You must be kidding; there are no bugs in this software. But if
this crazy thing happens write an email to stefan@sevenbyte.org or checkout
the bugtracker on github https://github.com/rumpelsepp/pynote.
