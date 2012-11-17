'''Posthook SMTPd server'''

from contextlib import contextmanager
import re
import sys

import smtpd
import asyncore

from posthook import response


class SMTPServer(smtpd.SMTPServer, object):

    def __init__(self, address='0.0.0.0', port=6054, workers=1000):
        super(SMTPServer, self).__init__((address, port), None)
        # Disregard workers, instanciate SMTPServer

    def run(self):
        # TODO catch errors
        asyncore.loop()

    def process_message(self, peer, mailfrom, rcpttos, data):
        '''Convert to a standard format'''
        for rcpt in rcpttos:
            res = self.recv({
                'protocol_name': 'SMTP',
                'sender': mailfrom,
                'recipient': rcpt,
                'client_address': peer,
                'data': data
            })
            action = '450'
            if isinstance(res, response.Dunno):
                action = '450'
            elif isinstance(res, response.Okay):
                action = '250'
            elif isinstance(res, response.Defer):
                action = '450'
            elif isinstance(res, response.Reject):
                action = '550'
            elif isinstance(res, response.Discard):
                action = '250'
            elif isinstance(res, resopnse.Hold):
                action = '250'
            elif isinstance(res, response.Response):
                res.msg = 'Command not implemented'
                action = '502'
            else:
                raise BadAction()

            # Add msg?
            if hasattr(res, 'msg') and res.msg is not None:
                return '{action} {msg}'.format(
                    action=action,
                    msg=res.msg
                )
            else:
                return '{action}'.format(action)

    def recv(self, params):
        '''Received connection, process SMTP parameters'''
        return response.Dunno()

class BadAction(Exception):
    '''Raised on missing or invalid action response'''
    pass
