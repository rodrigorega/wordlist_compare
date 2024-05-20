import unittest
from collections import Counter

from wordlist_compare import _normalize, _get_leaked_mails


class TestWordlistCompare(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(['foobar@email.com'], _normalize(['fOo.bAr@email.com\n']))

    def test_normalize_malformed_mails(self):
        mails = ['foobar@email.com', 'bobnomail.com', 'alice@email.com', 'foo.bar@email.com']
        self.assertEqual(Counter(['foobar@email.com', 'alice@email.com']), Counter(_normalize(mails)))

    def test_get_leaked_mails_empty(self):
        leaked_mails = _get_leaked_mails([], [])
        self.assertEqual([], leaked_mails)

    def test_get_leaked_mails(self):
        leaks = [
            'john_doe@email.com',
            'alice@email.net',
            'bob@email.org',
            'foo_bar@condemor.com',
            'chunkylover53@aol.com'
        ]
        mails = [
            'aLiCe@email.net',
            'BoB@email.org',
            'b.O.b@email.org'
        ]

        leaked_mails = _get_leaked_mails(mails, leaks)
        self.assertEqual(Counter(['alice@email.net', 'bob@email.org']), Counter(leaked_mails))
