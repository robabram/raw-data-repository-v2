#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from rdr_server.config import ConfigSection

#
# Database Configuration Section
#
db = ConfigSection('MySQL configuration')

#
# Google Service Configuration
#
service = ConfigSection('Google Service Configuration')

service.ALLOW_NONPROD_REQUESTS = True
# service.METRICS_SHARDS = 10

#
# Google Storage Bucket Configuration Section
#
buckets = ConfigSection('Google Storage Configuration')


#
# Survey Configuration Section
#
survey = ConfigSection('Survey configuration')

survey.BASELINE_PPI_QUESTIONNAIRE_FIELDS = [
    "questionnaireOnTheBasics",
    "questionnaireOnOverallHealth",
    "questionnaireOnLifestyle"
]

survey.PPI_QUESTIONNAIRE_FIELDS = [
    "questionnaireOnTheBasics",
    "questionnaireOnOverallHealth",
    "questionnaireOnLifestyle",
    "questionnaireOnFamilyHealth",
    "questionnaireOnHealthcareAccess",
    "questionnaireOnMedicalHistory",
    "questionnaireOnMedications"
]

#
# Biobank Configuration Section
#
biobank = ConfigSection('Biobank configuration')

# biobank.SAMPLES_SHARDS = 2

biobank.BASELINE_SAMPLE_TEST_CODES = [
    "1ED04",
    "1ED10",
    "1HEP4",
    "1PST8",
    "2PST8",
    "1SST8",
    "2SST8",
    "1PS08",
    "1SS08",
    "1UR10",
    "1CFD9",
    "1PXR2",
    "1UR90",
    "2ED10"
]

biobank.DNA_SAMPLE_TEST_CODES = [
    "1ED10",
    "2ED10",
    "1ED04",
    "1SAL",
    "1SAL2"
]

#
# Email Configuration Section
#
email = ConfigSection('Email Configuration')

email.INTERNAL_STATUS_SENDER = [
    "pmi-drc-alerts@googlegroups.com"
]

email.INTERNAL_STATUS_RECIPIENTS = [
    "pmi-drc-alerts+nonprod@googlegroups.com"
]

#
# Key Management Configuration Section
#
keys = ConfigSection('Key Management Configuration')

keys.DAYS_TO_DELETE_KEYS = 3
keys.AES_KEY = "digit-16-aes-key"