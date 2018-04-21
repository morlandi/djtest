from unittest import TestCase

import djtest

class TestJoke(TestCase):

    def test_is_string(self):
        s = djtest.joke()
        self.assertTrue(isinstance(s, str))
