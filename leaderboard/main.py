import falcon
import json
from leaderboard.route_endpoints import get_leaders
from leaderboard import route_endpoints
from leaderboard import middleware
from leaderboard.db import (
    session_factory,
    init_sessions
)


BEARER_TOKEN_HEADER = 'Authorization'

def crossdomain(req, resp):
    # review this
    resp.set_header('Access-Control-Allow-Origin', '*')


class FetchLeaders:
    def on_get(self, req, resp):
        resp.content_type = "application/json"
        resp.body = json.dumps(get_leaders.get_leaders_for_country(int(req.query_string)))


def token_ok(req):
    token = req.get_header(BEARER_TOKEN_HEADER, '')
    if token.startswith('Bearer'):
        token = token.replace('Bearer ', '')
        # TODO: check the validity of the token against the
        # profile server
        return True
    else:
        return False

class AddStumblesForUser:
    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        
        if not token_ok(req):
            token = req.get_header(BEARER_TOKEN_HEADER, '')
            msg = 'Unauthorized submission [%s]' % token
            raise falcon.HTTPError(falcon.HTTP_403, msg)

        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)

        try:
            as_json = json.loads(raw_json, encoding='utf-8')
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect.')
        # resp.status = falcon.HTTP_202 # or 200?
        route_endpoints.add_stumbles_for_user(email=None, login_token=None, query_json=as_json)
        # resp.body = json.dumps(add_stumbles_for_user(result_json), encoding='utf-8')

init_sessions()

session_manager = middleware.SQLAlchemySessionManager(session_factory)
app = falcon.API(middleware=[session_manager],
                 after=[crossdomain])
app.add_route('/leaders', FetchLeaders())
app.add_route('/add_stumbles', AddStumblesForUser())
