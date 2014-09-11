Frequently Asked Questions
==========================


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
