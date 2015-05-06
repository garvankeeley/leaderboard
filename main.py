import falcon
import json
from leaders import fetch_leaders

def crossdomain(req, resp):
    resp.set_header('Access-Control-Allow-Origin', '*')

class MainResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        #lon1 = float(req.get_param('lon1', '0'))
        resp.content_type = "application/json"
        resp.body = json.dumps(fetch_leaders(int(req.query_string)))

app = falcon.API(after=[crossdomain])
main = MainResource()
app.add_route('/leaders', main)
