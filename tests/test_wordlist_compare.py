import unittest

from wordlist_compare import _normalize, _get_leaked_mails


class TestWordlistCompare(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual('foobar@email.com', _normalize('fOo.bAr@email.com'))

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
        self.assertEqual(['alice@email.net', 'bob@email.org'], leaked_mails)
