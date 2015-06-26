import falcon
import json
from leaderboard.route_endpoints import get_leaders
from leaderboard import middleware
from leaderboard.db import (
    session_factory,
    init_sessions
)


def crossdomain(req, resp):
    # review this
    resp.set_header('Access-Control-Allow-Origin', '*')


class FetchLeaders:
    def on_get(self, req, resp):
        resp.content_type = "application/json"
        resp.body = json.dumps(get_leaders.get_leaders_for_country(int(req.query_string)))


class AddStumblesForUser:
    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        req.get_header('bearer_token')
        # resp.body = json.dumps(
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
app.add_route('/add_leaderboard_stumbles_for_user', AddStumblesForUser())
