#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from flask_restplus import Namespace, Resource, fields
from rdr_server.dao.codebook import CodeBookDao

api = Namespace('cats', description='Cats related operations')

cat = api.model('Cat', {
    'id': fields.String(required=True, description='The cat identifier'),
    'name': fields.String(required=True, description='The cat name'),
})

CATS = [
    {'id': 'felix', 'name': 'Felix'},

]


@api.route('/')
class CatList(Resource):
    @api.doc('list_cats')
    @api.marshal_list_with(cat)
    def get(self):
        """List all cats"""
        return CATS


@api.route('/count')
class CatCount(Resource):
    def get(self):
        dao = CodeBookDao()
        count = dao.count()
        return {'count': count}


@api.route('/<id>')
@api.param('id', 'The cat identifier')
@api.response(404, 'Cat not found')
class Cat(Resource):
    # @api.doc('get_cat')
    @api.marshal_with(cat)
    def get(self, id):
        """Fetch a cat given its identifier"""
        for cat in CATS:
            if cat['id'] == id:
                return cat
        api.abort(404)
