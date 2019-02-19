#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
import json
import requests
from flask_restplus import Namespace, Resource

_CODEBOOK_URL_BASE = 'https://raw.githubusercontent.com/all-of-us-terminology/codebook-to-fhir/'
_CODEBOOK_ERRORS_URL = _CODEBOOK_URL_BASE + 'gh-pages/CodeSystem/ppi.issues.json'
_CODEBOOK_URL = _CODEBOOK_URL_BASE + 'gh-pages/CodeSystem/ppi.json'

api = Namespace('internal', description='Internal related operations')


@api.route('/ImportCodeBook')
class CodeBook(Resource):
    def post(self):

        resp = {}

        try:
            req = requests.get(_CODEBOOK_URL)
        except Exception as e:
            return {'error_messages': [{'error': e}]}

        if req.status_code == 200:
            cb = req.json()
            resp['published_version'] = cb['version']
            resp['active_version'] = 'unknown'
            return resp
        else:
            return {'error_messages': [{'error': 'failed to retrieve current codebook.'}]}
