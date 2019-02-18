"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}
from rdr_server.model.base_model import UTCDateTime

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade(schema):
    globals()["upgrade_{0}".format(schema)]()


def downgrade(schema):
    globals()["downgrade_{0}".format(schema)]()

##
## generate an "upgrade_<xyz>() / downgrade_<xyz>()" function
## for each database name in the ini file.
##
% for schema in [x.strip() for x in str(config.get_main_option('sqlalchemy.schemas')).split(',')]:

def upgrade_${schema}():
    ${context.get("{0}_upgrades".format(schema), "pass").replace('rdr_server.model.base_model.', '')}


def downgrade_${schema}():
    ${context.get("{0}_downgrades".format(schema).replace('rdr_server.model.base_model.', ''), "pass")}

% endfor