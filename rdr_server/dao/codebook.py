#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from rdr_server.dao.base_dao import BaseDao
from rdr_server.model.code import Code, CodeBook


class CodeBookDao(BaseDao):

    model = None  # type: CodeBook

    def __init__(self):
        super(CodeBookDao, self).__init__(CodeBook)
