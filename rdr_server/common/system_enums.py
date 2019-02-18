import json
from enum import IntEnum

from dateutil.relativedelta import relativedelta

from rdr_server.common.code_constants import (
    # Internal Use Codes
    UNSET,
    # PMI Codes
    PMI_SKIP_CODE, PMI_UNANSWERED_CODE, PMI_FREE_TEXT_CODE, PMI_OTHER_CODE,
    PMI_PREFER_NOT_TO_ANSWER_CODE,
    # Race Codes
    RACE_AIAN_CODE, RACE_ASIAN_CODE, RACE_BLACK_CODE, RACE_MENA_CODE, RACE_NHDPI_CODE,
    RACE_WHITE_CODE, RACE_HISPANIC_CODE, RACE_FREETEXT_CODE, RACE_NONE_OF_THESE_CODE
)

# These are handled specially in code; others will be inserted into the database and handled
# dynamically.
UNSET_HPO_ID = 0

# A pattern for test participant email addresses.
TEST_EMAIL_PATTERN = '%@example.com'
# The name of the 'test' HPO that test participants are normally affiliated with.
TEST_HPO_NAME = 'TEST'
TEST_HPO_ID = 19
# Test login phone number prefix
TEST_LOGIN_PHONE_NUMBER_PREFIX = '444'


class Operator(IntEnum):
    EQUALS = 0  # Case insensitive comparison for strings, exact comparison otherwise
    LESS_THAN = 1
    GREATER_THAN = 2
    LESS_THAN_OR_EQUALS = 3
    GREATER_THAN_OR_EQUALS = 4
    NOT_EQUALS = 5
    # Note: we don't support contains or exact string comparison at this stage


class PropertyType(IntEnum):
    STRING = 0
    DATE = 1
    DATETIME = 2
    ENUM = 3
    INTEGER = 4
    CODE = 5


class SiteStatus(IntEnum):
    """ The active scheduling status of a site. """
    UNSET = 0
    ACTIVE = 1
    INACTIVE = 2


class EnrollingStatus(IntEnum):
    """ The actively enrolling status of a site. """
    UNSET = 0
    ACTIVE = 1
    INACTIVE = 2


class DigitalSchedulingStatus(IntEnum):
    """ The status of a sites digital scheduling capability. """
    UNSET = 0
    ACTIVE = 1
    INACTIVE = 2


class ObsoleteStatus(IntEnum):
    """ If an organization is obsolete but referenced in other tables. """
    ACTIVE = 0
    OBSOLETE = 1


class CodeType(IntEnum):
    """A type of code"""
    MODULE = 1
    TOPIC = 2
    QUESTION = 3
    ANSWER = 4


class PhysicalMeasurementsStatus(IntEnum):
    """The state of the participant's physical measurements."""
    UNSET = 0
    COMPLETED = 1
    CANCELLED = 2


class QuestionnaireStatus(IntEnum):
    """The status of a given questionnaire for this participant"""
    UNSET = 0
    SUBMITTED = 1
    SUBMITTED_NO_CONSENT = 2
    SUBMITTED_NOT_SURE = 3
    SUBMITTED_INVALID = 4


class QuestionnaireDefinitionStatus(IntEnum):
    """ If a questionnaire has been determined to be invalid"""
    VALID = 0
    INVALID = 1


class EnrollmentStatus(IntEnum):
    """A status reflecting how fully enrolled a participant is"""
    INTERESTED = 1
    MEMBER = 2
    FULL_PARTICIPANT = 3


class SampleStatus(IntEnum):
    """Status of biobank samples"""
    UNSET = 0
    RECEIVED = 1
    # DA-814 - sample disposal statuses for a good outcome.
    DISPOSED = 10
    CONSUMED = 11
    UNKNOWN = 12
    # DA-814 - sample disposal statuses for a bad outcome.
    SAMPLE_NOT_RECEIVED = 13
    SAMPLE_NOT_PROCESSED = 14
    ACCESSINGING_ERROR = 15
    LAB_ACCIDENT = 16
    QNS_FOR_PROCESSING = 17
    QUALITY_ISSUE = 18


def get_sample_status_enum_value(status):
    """
    Return the SampleStatus enum value for the given status from Mayo
    :param status: a sample status value
    :return: SampleStatus enum value
    """
    if status is None:
        return SampleStatus.UNSET

    # Set Received if we have an empty status value, the sample has not been disposed of yet.
    if not status:
        return SampleStatus.RECEIVED

    status = status.lower()

    if status == 'disposed':
        return SampleStatus.DISPOSED
    elif status == 'consumed':
        return SampleStatus.CONSUMED
    elif status == 'sample not received':
        return SampleStatus.SAMPLE_NOT_RECEIVED
    elif status == 'sample not processed':
        return SampleStatus.SAMPLE_NOT_PROCESSED
    elif status == 'accessioning error':
        return SampleStatus.ACCESSINGING_ERROR
    elif status == 'lab accident':
        return SampleStatus.LAB_ACCIDENT
    elif status == 'qns for processing':
        return SampleStatus.QNS_FOR_PROCESSING
    elif status == 'quality issue':
        return SampleStatus.QUALITY_ISSUE

    # Set unknown for any new status values.
    return SampleStatus.UNKNOWN


class OrderStatus(IntEnum):
    """Status of biobank orders and samples"""
    UNSET = 0
    CREATED = 1
    COLLECTED = 2
    PROCESSED = 3
    FINALIZED = 4


class BiobankOrderStatus(IntEnum):
    """ The status of a biobank order: amended/cancelled """
    UNSET = 0
    AMENDED = 1
    CANCELLED = 2


class MetricSetType(IntEnum):
    """Type determining the schema for a metric set."""
    PUBLIC_PARTICIPANT_AGGREGATIONS = 1


class MetricsKey(IntEnum):
    """Key for a metrics set metric aggregation."""
    GENDER = 1
    RACE = 2
    STATE = 3
    AGE_RANGE = 4
    PHYSICAL_MEASUREMENTS = 5
    BIOSPECIMEN_SAMPLES = 6
    QUESTIONNAIRE_ON_OVERALL_HEALTH = 7
    QUESTIONNAIRE_ON_PERSONAL_HABITS = 8
    QUESTIONNAIRE_ON_SOCIODEMOGRAPHICS = 9
    ENROLLMENT_STATUS = 10


class Stratifications(IntEnum):
    """Variables by which participant counts can be stacked"""
    TOTAL = 1
    ENROLLMENT_STATUS = 2
    GENDER_IDENTITY = 3
    RACE = 4
    AGE_RANGE = 5
    EHR_CONSENT = 6
    EHR_RATIO = 7


METRIC_SET_KEYS = {
    MetricSetType.PUBLIC_PARTICIPANT_AGGREGATIONS: set([
        MetricsKey.GENDER,
        MetricsKey.RACE,
        MetricsKey.STATE,
        MetricsKey.AGE_RANGE,
        MetricsKey.PHYSICAL_MEASUREMENTS,
        MetricsKey.BIOSPECIMEN_SAMPLES,
        MetricsKey.QUESTIONNAIRE_ON_OVERALL_HEALTH,
        MetricsKey.QUESTIONNAIRE_ON_PERSONAL_HABITS,
        MetricsKey.QUESTIONNAIRE_ON_SOCIODEMOGRAPHICS,
        MetricsKey.ENROLLMENT_STATUS
    ])
}


# These race values are derived from one or more answers to the race/ethnicity question
# in questionnaire responses.
class Race(IntEnum):
    UNSET = 0
    PMI_Skip = 1
    # UNMAPPED = 2 -- Not actually in use.
    AMERICAN_INDIAN_OR_ALASKA_NATIVE = 3
    BLACK_OR_AFRICAN_AMERICAN = 4
    ASIAN = 5
    NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER = 6
    WHITE = 7
    HISPANIC_LATINO_OR_SPANISH = 8
    MIDDLE_EASTERN_OR_NORTH_AFRICAN = 9
    HLS_AND_WHITE = 10
    HLS_AND_BLACK = 11
    HLS_AND_ONE_OTHER_RACE = 12
    HLS_AND_MORE_THAN_ONE_OTHER_RACE = 13
    MORE_THAN_ONE_RACE = 14
    OTHER_RACE = 15
    PREFER_NOT_TO_SAY = 16


# A type of organization responsible for signing up participants.
class OrganizationType(IntEnum):
    UNSET = 0
    # Healthcare Provider Organization
    HPO = 1
    # Federally Qualified Health Center
    FQHC = 2
    # Direct Volunteer Recruitment Center
    DV = 3
    # Veterans Administration
    VA = 4


ANSWER_CODE_TO_RACE = {
    RACE_AIAN_CODE: Race.AMERICAN_INDIAN_OR_ALASKA_NATIVE,
    RACE_ASIAN_CODE: Race.ASIAN,
    RACE_BLACK_CODE: Race.BLACK_OR_AFRICAN_AMERICAN,
    RACE_MENA_CODE: Race.MIDDLE_EASTERN_OR_NORTH_AFRICAN,
    RACE_NHDPI_CODE: Race.NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER,
    RACE_WHITE_CODE: Race.WHITE,
    RACE_HISPANIC_CODE: Race.HISPANIC_LATINO_OR_SPANISH,
    RACE_FREETEXT_CODE: Race.OTHER_RACE,
    PMI_PREFER_NOT_TO_ANSWER_CODE: Race.PREFER_NOT_TO_SAY,
    RACE_NONE_OF_THESE_CODE: Race.OTHER_RACE,
    PMI_OTHER_CODE: Race.OTHER_RACE,
    PMI_FREE_TEXT_CODE: Race.OTHER_RACE,
    PMI_UNANSWERED_CODE: Race.UNSET,
    PMI_SKIP_CODE: Race.PMI_Skip,
}


class WithdrawalStatus(IntEnum):
    """Whether a participant has withdrawn from the study."""
    NOT_WITHDRAWN = 1
    NO_USE = 2


class WithdrawalReason(IntEnum):
    """Whether a participant has been administratively withdrawn from the study.
       If value is UNSET it mean that a participant went through the normal withdrawal process."""
    UNSET = 0
    FRAUDULENT = 1
    DUPLICATE = 2
    TEST = 3


class SuspensionStatus(IntEnum):
    """Whether a participant has been suspended from the study."""
    NOT_SUSPENDED = 1
    NO_CONTACT = 2


# The lower bounds of the age buckets.
_AGE_LB = [0, 18, 26, 36, 46, 56, 66, 76, 86]
AGE_BUCKETS = ['{}-{}'.format(b, e) for b, e in zip(_AGE_LB, [a - 1 for a in _AGE_LB[1:]] + [''])]


def get_bucketed_age(date_of_birth, today):
    if not date_of_birth:
        return UNSET
    age = relativedelta(today, date_of_birth).years
    for begin, end in zip(_AGE_LB, [age_lb - 1 for age_lb in _AGE_LB[1:]] + ['']):
        if (age >= begin) and (not end or age <= end):
            return str(begin) + '-' + str(end)


def _map_single_race(code):
    if code is None:
        return Race.UNSET
    race_value = ANSWER_CODE_TO_RACE.get(code.value)
    if race_value:
        return race_value
    return ANSWER_CODE_TO_RACE.get(code.parent)


def get_race(race_codes):
    '''Transforms one or more race codes from questionnaire response answers about race
    into a single race enum; the enum includes values for multiple races.
    See: https://docs.google.com/document/d/1Z1rGULWVlmSIAO38ACjMnz0aMuua3sKqFZXjGqw3gqQ'''
    if not race_codes:
        return None
    if len(race_codes) == 1:
        return _map_single_race(race_codes[0])
    else:
        all_races = set([_map_single_race(race_code) for race_code in race_codes])
        if Race.HISPANIC_LATINO_OR_SPANISH in all_races:
            if len(all_races) > 2:
                return Race.HLS_AND_MORE_THAN_ONE_OTHER_RACE
            if Race.WHITE in all_races:
                return Race.HLS_AND_WHITE
            if Race.BLACK_OR_AFRICAN_AMERICAN in all_races:
                return Race.HLS_AND_BLACK
            return Race.HLS_AND_ONE_OTHER_RACE
        else:
            return Race.MORE_THAN_ONE_RACE


# TODO: Fix this function, try to relocate it to hpo_dao.py.
# def make_primary_provider_link_for_id(hpo_id):
#     from dao.hpo_dao import HPODao
#    return make_primary_provider_link_for_hpo(HPODao().get(hpo_id))


def make_primary_provider_link_for_hpo(hpo):
    return make_primary_provider_link_for_name(hpo.name)


def make_primary_provider_link_for_name(hpo_name):
    """Returns serialized FHIR JSON for a provider link based on HPO information.

    The returned JSON represents a list containing the one primary provider.
    """
    return json.dumps([{
        'primary': True,
        'organization': {
            'reference': 'Organization/%s' % hpo_name
        }
    }], sort_keys=True)
