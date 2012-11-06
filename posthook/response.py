'''Posthook response action classes'''


class Response(object):
    '''Action response representation'''

    msg = None

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return '<{}Response>'.format(
            self.__class__.__name__
        )

class Okay(Response):
    pass

class Reject(Response):
    def __init__(self, msg=None, code=None):
        super(Reject, self).__init__(msg)
        self.code = code

class Defer(Response):
    pass

class DeferIfReject(Response):
    pass

class DeferIfPermit(Response):
    pass

class BCC(Response):
    pass

class Discard(Response):
    pass

class Dunno(Response):
    def __init__(self):
        super(Dunno, self).__init__()

class Hold(Response):
    pass

class Warn(Response):
    pass
