import os
import unittest
from datetime import datetime

from pynote import container
from pynote import helper


class TestNote(unittest.TestCase):

    def setUp(self):
        self.now = datetime.now()
        self.note_dict = {'title': 'Test Note',
                          'created': self.now.timestamp(),
                          'updated': self.now.timestamp(),
                          'deleted': None,
                          'revision': 1,
                          'uuid': '1b442f70-2320-4122-8567-612d0e90eafd',
                          'tags': [],
                          'content': 'This is the content for the Unit Test!!'}
        self.note = container.Note(title='Test Note', created=self.now,
                                   updated=self.now, deleted=None, revision=1,
                                   uuid='1b442f70-2320-4122-8567-612d0e90eafd',
                                   tags=[],
                                   content='This is the content for the Unit Test!!')

    def test_from_dict(self):
        self.assertIsInstance(self.note, container.Note)
        self.assertEqual(container.Note.from_dict(self.note_dict), self.note)

    def test_to_dict(self):
        self.assertIsInstance(self.note.to_dict(), dict)
        self.assertDictEqual(self.note.to_dict(), self.note_dict)


class TestContainer(unittest.TestCase):

    def setUp(self):
        self.data_file = helper.create_tempfile()
        self.trash_file = helper.create_tempfile()
        self.revisions_file = helper.create_tempfile()

        with open(self.data_file, 'w') as f:
            f.write('[]')
        with open(self.trash_file, 'w') as f:
            f.write('[]')
        with open(self.revisions_file, 'w') as f:
            f.write('[]')

        self.data = container.Data(self.data_file)
        self.trash = container.Data(self.trash_file)
        self.revisions = container.Data(self.revisions_file)

    def tearDown(self):
        os.remove(self.data_file)
        os.remove(self.trash_file)
        os.remove(self.revisions_file)

    def test_data_container(self):
        note = container.Note.create('A Testnote!')
        self.assertIsInstance(self.data, container.Data)
        self.data.append(note)

        self.assertTrue(self.data[0])
        self.assertEqual(self.data[0], note)
        self.assertEqual(len(self.data), 1)
        self.assertTrue(self.data.dumps())
        self.assertRaises(IndexError, self.data.__getitem__, 1)
        self.assertRaises(IndexError, self.data.__setitem__, 1, 1)
        self.assertRaises(IndexError, self.data.__delitem__, 1)

    def test_trash_container(self):
        note = container.Note.create('A Testnote!')
        self.assertIsInstance(self.trash, container.Data)
        self.trash.append(note)

        self.assertTrue(self.trash[0])
        self.assertEqual(self.trash[0], note)
        self.assertEqual(len(self.trash), 1)
        self.assertTrue(self.trash.dumps())
        self.assertRaises(IndexError, self.trash.__getitem__, 1)
        self.assertRaises(IndexError, self.trash.__setitem__, 1, 1)
        self.assertRaises(IndexError, self.trash.__delitem__, 1)

    def test_revisions_container(self):
        note = container.Note.create('A Testnote!')
        self.assertIsInstance(self.revisions, container.Data)
        self.revisions.append(note)

        self.assertTrue(self.revisions[0])
        self.assertEqual(self.revisions[0], note)
        self.assertEqual(len(self.revisions), 1)
        self.assertTrue(self.revisions.dumps())
        self.assertRaises(IndexError, self.revisions.__getitem__, 1)
        self.assertRaises(IndexError, self.revisions.__setitem__, 1, 1)
        self.assertRaises(IndexError, self.revisions.__delitem__, 1)


if __name__ == '__main__':
    unittest.main()
