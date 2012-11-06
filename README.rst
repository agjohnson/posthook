Posthook
========

Asynchronous SMTP server and Postfix policy service base for writing service
hooks for processing and testing mail.

Synopsis
--------

A simple policy daemon that rejects all mail except for a single address would
look like:

::

    from posthook.provider.policy import PolicyServer
    from posthook import response

    class RejectAllTheMail(PolicyServer):

        def recv(self, params):
            if params['recipient'] == 'test@foo.tld':
                return response.Discard(msg='Discarded')
            return response.Reject(msg='Nope')

    app = RejectAllTheMail()
    app.run()

Replacing ``policy.PolicyServer`` with ``smtp.SMTPServer`` will provide a
similar interface serving SMTP directly. This is useful for building local
testing services without Postfix. Some responses specific to queue management,
not the SMTP transaction, are not recognized by the SMTP server.

Author
------

Anthony Johnson ``<aj@ohess.org>``
