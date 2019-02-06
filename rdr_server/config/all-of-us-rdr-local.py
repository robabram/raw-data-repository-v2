#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from rdr_server.config.defaults import *

db.connection = 'blaszer'

biobank.ID_PREFIX = 'Z'

service.USERS = {
    'example@example.com': {
        'roles': ['ptc', 'healthpro', 'exporter', 'storefront'],
        'whitelisted_ip_ranges': {
            'ip6': ['::1/64'],
            'ip4': ['127.0.0.1/32']
        }
    },
    'awardee-pitt@pmi-drc-api-test.iam.gserviceaccount.com': {
        'roles': ['awardee_sa'],
        'awardee': 'PITT',
        'whitelisted_ip_ranges': {
            'ip4': ['136.142.28.15', '136.142.28.122', '136.142.28.123', '136.142.28.76', '136.142.202.70',
                    '136.142.202.71', '136.142.202.72', '136.142.202.73', '136.142.202.74', '136.142.202.75',
                    '136.142.202.76', '136.142.202.77', '136.142.202.78']
        }
    }
}

buckets.BIOBANK_SAMPLES_BUCKET_NAME = 'app_default_bucket'
buckets.GHOST_ID_BUCKET = 'all-of-us-rdr-test-ghost-accounts'
buckets.CONSENT_PDF_BUCKET = 'app_default_bucket'

