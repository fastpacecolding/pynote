Roadmap
=======


pynote X.X
----------

- Drop prettytable and create an own library.
- Fix tests...


pynote 0.3
----------

- Create your own reports in ``~/.noterc``.

  ::

      [long]
      fields = description, updated, tags
      order_by = updated
      ascending = yes

- Import/Export module
- ``note edit``: Edit header as well. I have to write a little parser
  for this.
- Add hash to notes metadata. It may be useful for detecting changes.
- Switch to SHA512; MD5 is out ;)
