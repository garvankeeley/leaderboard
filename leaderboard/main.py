import falcon
import json
import requests
from leaderboard.util.gz_compress import gzip_decompress
from leaderboard.route_endpoints import get_leaders
from leaderboard import route_endpoints
from leaderboard.fxa import FxaProfileServer
from leaderboard import middleware
from leaderboard.db import (
    session_factory,
    init_sessions
)

# This needs to be run before *any* TLS connections are made
import urllib3.contrib.pyopenssl

urllib3.contrib.pyopenssl.inject_into_urllib3()

BEARER_TOKEN_HEADER = 'Authorization'
FXA_SECRET = "3015f44423df9a5f08d0b5cd43e0cbb6f82c56e37f09a3909db293e17a9e64af"


def crossdomain(req, resp):
    # review this
    resp.set_header('Access-Control-Allow-Origin', '*')


class FetchLeaders(object):
    def on_get(self, req, resp):
        resp.content_type = "application/json"
        country_id = int(req.query_string)
        json_obj = get_leaders.get_leaders_for_country(country_id)
        resp.body = json.dumps(json_obj)


class FxAResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""

        payload = {"client_id": "d0f6d2ed3c5fcc3b",
                   "client_secret": FXA_SECRET,
                   "code": req.params['code']}

        fxa_resp = requests.post("https://oauth-stable.dev.lcip.org/v1/token",
                                 data=json.dumps(payload))

        resp.content_type = "text/html"
        resp.body = fxa_resp.text


class AddStumblesForContributor(object):
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
            raw_bytes = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)

        try:
            raw_json = gzip_decompress(raw_bytes)
            as_json = json.loads(raw_json, encoding='utf-8')
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect.')
        # resp.status = falcon.HTTP_202 # or 200?
        route_endpoints.add_stumbles_for_contributor(email=email,
                                                     display_name=nick,
                                                     query_json=as_json)


init_sessions()

session_manager = middleware.SQLAlchemySessionManager(session_factory)
app = falcon.API(middleware=[session_manager],
                 after=[crossdomain])

app.add_route('/fxa/callback', FxAResource())
app.add_route('/backend/leaders', FetchLeaders())
app.add_route('/backend/add_stumbles', AddStumblesForContributor())

if __name__ == '__main__':
    from wsgiref import simple_server

    httpd = simple_server.make_server('127.0.0.1', 8050, app)
    httpd.serve_forever()
