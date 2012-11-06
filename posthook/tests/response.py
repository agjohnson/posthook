'''Posthook response action classes'''

import unittest
from mock import patch, Mock

from posthook import response

class ResponseTests(unittest.TestCase):

    def test_response_base(self):
        o = response.Response(msg='test')
        self.assertEquals('action=dunno test\n\n', o.response())

    def test_response_ok(self):
        o = response.Okay(msg='test')
        self.assertEquals('action=ok test\n\n', o.response())

    def test_response_reject(self):
        o = response.Reject(msg='test')
        self.assertEquals('action=reject test\n\n', o.response())

    def test_response_reject_4xx(self):
        o = response.Reject(msg='test', code=413)
        self.assertEquals('action=413 test\n\n', o.response())

    def test_response_reject_5xx(self):
        o = response.Reject(msg='test', code=500)
        self.assertEquals('action=500 test\n\n', o.response())

    def test_response_reject_bad(self):
        o = response.Reject(msg='test', code=600)
        self.assertEquals('action=reject test\n\n', o.response())

