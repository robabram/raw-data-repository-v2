#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

import unittest
from rdr_server.config import config


class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_gcp_project(self):
        self.assertEquals('all-of-us-rdr-local', config.GCP_PROJECT)
