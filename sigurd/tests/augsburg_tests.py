"""

"""

import unittest

from sigurd.nib_augsburg.nib_reader import read_txt
from sigurd.nib_augsburg.nib_retrieval import MAIN_LINKS


class AugsburgTest(unittest.TestCase):

    def test_read(self):
        with self.assertRaises(FileExistsError):
            read_txt(MAIN_LINKS[0])
