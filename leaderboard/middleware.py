import sqlalchemy.orm.scoping as scoping


class SQLAlchemySessionManager(object):
    def __init__(self, session_factory, auto_commit=False):
        self._session_factory = session_factory
        self._scoped = isinstance(session_factory, scoping.ScopedSession)
        self._auto_commit = auto_commit

    def process_request(self, req, resp, params):
        req.context['session'] = self._session_factory()

    def process_response(self, req, resp):
        session = req.context['session']

        if self._auto_commit:
            session.commit()

        if self._scoped:
            session.remove()
        else:
            session.close()
