import falcon
import json
from leaderboard.route_endpoints import get_leaders
from leaderboard import route_endpoints
from leaderboard.fxa import FxaProfileServer
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
        country_id = int(req.query_string)
        json_obj = get_leaders.get_leaders_for_country(country_id)
        resp.body = json.dumps(json_obj)


class AddStumblesForUser:
    def token_ok(self, req):
        token = req.get_header(BEARER_TOKEN_HEADER, '')
        if token.startswith('Bearer'):
            token = token.replace('Bearer ', '')
            fxa_serv = FxaProfileServer()
            (email, nick) = fxa_serv.fetch_profile(token)
            if (email == ''):
                return None
            return (token, email, nick)
        else:
            return None

    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        token_resp = self.token_ok(req)
        if token_resp is None:
            token = req.get_header(BEARER_TOKEN_HEADER, '')
            msg = 'Unauthorized submission [%s]' % token
            raise falcon.HTTPError(falcon.HTTP_403, msg)

        token, email, nick = token_resp

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
        route_endpoints.add_stumbles_for_user(email=email,
                                              displayName=nick,
                                              login_token=token,
                                              query_json=as_json)

init_sessions()

session_manager = middleware.SQLAlchemySessionManager(session_factory)
app = falcon.API(middleware=[session_manager],
                 after=[crossdomain])
app.add_route('/leaders', FetchLeaders())
app.add_route('/add_stumbles', AddStumblesForUser())
