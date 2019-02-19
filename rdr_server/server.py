#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from flask import Flask
from flask_restplus import Api, Resource

# import api namespaces
from rdr_server.apis.hello_world import api as ns1
from rdr_server.apis.internal import api as ns2

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
api = Api(app)

# Add name spaces
api.add_namespace(ns1)
api.add_namespace(ns2)


@api.route('/_ah/warmup')
class HelloWorld(Resource):
    def get(self):
        return '{ "success": "true" }'

