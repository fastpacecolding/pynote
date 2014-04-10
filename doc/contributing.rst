Contributing
============

Hacking
-------

Please stick to PEP8_ and PEP257_. If you are a Sublime Text 3 User you
can use the ``pynote.sublime-project`` file with the required settings.

.. _PEP8: http://www.python.org/dev/peps/pep-0008/
.. _PEP257: http://www.python.org/dev/peps/pep-0257/


Commit Messages
---------------

Checkout git's `Commit Guidelines`_!

.. _`Commit Guidelines`: http://git-scm.com/book/en/Distributed-Git-Contributing-to-a-Project#Commit-Guidelines


Pull Request
------------

Feel free to send me any request! I don't care about the pull request format
any more but please keep an eye on PEP8_... :-)


How to create a translation
---------------------------

* Make sure you have installed babel_.
* Clone the project with ``git clone https://github.com/rumpelsepp/pynote.git``
* At first you have to create a translation catalogue. There is a make target
  included for doing this. For creating a polish message catolgue you can use
  ``make init-locale LOCALE=pl``.
* You will find the new translation files in the ``locale`` directory.
* Finish your translation e.g. with poedit_ and send a pullrequest! It
  may be included in the next release.

.. _babel: http://babel.pocoo.org/
.. _poedit: http://www.poedit.net/



GPG Key
-------

My GPG public key is available at `pgp.mit.edu`_::


    pub   2048R/A655F324 2013-05-02 [expires: 2015-05-02]
          Key fingerprint = 4398 1A32 9497 6B9F 334B  ACBA 6D07 7CDE A655 F324
    uid                  Stefan Tatschner <stefan@sevenbyte.org>
    uid                  Stefan Tatschner <stefan.tatschner@gmail.com>
    uid                  Stefan Tatschner <stefan.tatschner@stud.th-deg.de>
    sub   2048R/2B359DD3 2013-05-02 [expires: 2015-05-02]

.. _`pgp.mit.edu`: http://pgp.mit.edu:11371/pks/lookup?op=vindex&search=0x6D077CDEA655F324
