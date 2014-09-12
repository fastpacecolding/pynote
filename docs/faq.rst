Frequently Asked Questions
==========================


Upgrading from 0.2 to 1.0
-------------------------

In pynote 1.0 there are huge changes in managing the storage backend. I changed
from *.json files to managing plain text files. There are several advantages:

* A note's metadata could be extracted from the filesystem such as the
  modification time and the title.
* We do not have to load the whole data for creating a note list. We just can
  do a list dir to get all of the titles and every modification time. It should
  be quite faster for large note lists.
* You can manage your notes without pynote as well. All you need is a text
  editor and a filebrowser as there are just plain text files.

You have to convert the json files to plain text files. I have created a gist_
to do that. You can run the script after updating to pynote 1.0 or before; it
does not matter. You only have to make sure that there is this section in your
~/.noterc::

    [DEFAULT]
    data = path/to/my/notes

The easiest way is to use curl to get the code and just pipe it into python::

    curl -L https://gist.githubusercontent.com/rumpelsepp/9b17cda631af5cdbb412/raw/note_migrate.py | python

Make sure that is has worked and you have plaintext files in your data path.
You can now remove ``data.json``, ``trash.json`` and ``revision.json`` and
convert your ~/.noterc to the new format, see :doc:`configuration`. The
conversion should not be that difficult!

.. _gist: https://gist.github.com/rumpelsepp/9b17cda631af5cdbb412


How can I change the extension of my notes?
-------------------------------------------

In pynote 1.0 there is a new configuration option called ``extension``. Every
new note will get this extension. This might be useful for setting the correct
synthax in your editor automatically. The extension option only affects new
notes; it will not alter any existing notes because it might mess up things.
You can add your prefered extension with this bash script very easily.
Consider adjusting the NOTE_PATH and EXTENSION variable to your needs.

.. code-block:: bash

    #!/usr/bin/env bash

    NOTE_PATH="$HOME/.note"
    EXTENSION=".txt"

    # see: http://stackoverflow.com/a/1108608/2587286
    find $NOTE_PATH -type f -not -name "*.*" -exec mv "{}" "{}"$EXTENSION \;
