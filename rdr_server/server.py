#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

# TODO: Drop flask_restplus and switch to flask views
# TODO: http://flask.pocoo.org/docs/1.0/views/

# TODO: documentation https://dev.to/djiit/documenting-your-flask-powered-api-like-a-boss-9eo

from flask import Flask
from flask_restplus import Api, Resource

# import api namespaces
from rdr_server.api.hello_world import api as ns1
from rdr_server.api.internal import api as ns2
from rdr_server.api.calendar import api as ns3

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
api = Api(app, version='0.1', title='A good test', description='A simple API test')

# Add name spaces
api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)



@api.route('/_ah/warmup')
class HelloWorld(Resource):
    def get(self):
        return '{ "success": "true" }'

