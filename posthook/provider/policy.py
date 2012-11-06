'''Posthook policy server'''

import gevent
from gevent.server import StreamServer
from gevent.socket import wait_read
from gevent.pool import Pool

from contextlib import contextmanager
import re
import sys

from posthook import response


class PolicyServer(object):

    def __init__(self, address='0.0.0.0', port=6054, workers=1000):
        self.port = port
        self.address = address
        self.pool = Pool(workers)

    def run(self):
        self.daemon = StreamServer(
            (self.address, self.port),
            self.handle,
            spawn=self.pool
        )
        self.daemon.serve_forever()

    def handle(self, socket, address):
        print 'Connection from {0}'.format(address)
        h = socket.makefile()

        while True:
            try:
                with self.params(h) as param:
                    if param is None:
                        break
                    action = self.response_action(param)
                    print 'Sent action: {}'.format(action.rstrip())
                    h.write(action)
                    h.flush()
            except ClientDisconnected:
                print 'Disconnected'
                break

    @contextmanager
    def params(self, h):
        param_list = dict(pair for pair in self._sess_params(h))
        if param_list == dict():
            yield None
        else:
            yield param_list

    def _sess_params(self, h):
        while True:
            line = h.readline()
            if not line:
                raise ClientDisconnected()
            if line == "\r" or line == "\r\n" or line == "\n":
                break
            m = re.search(r'^([\w\_]+)=(.*)$', line)
            if m is not None:
                yield (m.group(1), m.group(2))

    def recv(self, params):
        return response.Dunno()

    def response_action(self, params):
        '''Translate response to policy action'''
        res = self.recv(params)
        action = 'dunno'
        if isinstance(res, response.Okay):
            action = 'ok'
        elif isinstance(res, response.Defer):
            action = 'defer'
        elif isinstance(res, response.Reject):
            if hasattr(res, 'code') and res.code is not None:
                action = str(res.code)
            else:
                action = 'reject'
        elif isinstance(res, response.DeferIfReject):
            action = 'defer_if_reject'
        elif isinstance(res, response.DeferIfPermit):
            action = 'defer_if_permit'
        elif isinstance(res, response.BCC):
            action = 'bcc'
        elif isinstance(res, response.Discard):
            action = 'discard'
        elif isinstance(res, response.Dunno):
            action = 'dunno'
        elif isinstance(res, response.Hold):
            action = 'hold'
        elif isinstance(res, response.Warn):
            action = 'warn'
        elif isinstance(res, response.Response):
            return 'dunno'
        else:
            raise BadAction()

        # Return msg as well, if available
        if res.msg is not None:
            return 'action={action} {msg}\n\n'.format(
                action=action,
                msg=res.msg
            )
        else:
            return 'action={action}\n\n'.format(action=action)


class ClientDisconnected(Exception):
    '''Raised on disconnection'''
    pass

class BadAction(Exception):
    '''Raised on missing or invalid action response'''
    pass

