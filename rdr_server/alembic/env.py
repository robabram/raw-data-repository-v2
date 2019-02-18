from __future__ import with_statement

import logging
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from rdr_server.model.base_model import BaseModel, BaseMetricsModel

# Importing this is what gets our model available for Alembic.
import rdr_server.model.database  # pylint: disable=unused-import

logger = logging.getLogger('alembic')

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = {
    'rdrv2': BaseModel.metadata,
    'metricsv2': BaseMetricsModel.metadata
}

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

db_schemas = [x.strip() for x in str(config.get_main_option('sqlalchemy.schemas')).split(',')]

db_engine = config.get_main_option("sqlalchemy.engine")
db_host = config.get_main_option("sqlalchemy.host")
uri_proto = config.get_main_option("sqlalchemy.url").replace('%host%', db_host)

autogen_blacklist = ["aggregate_metrics_ibfk_1", ]


def include_object_fn(schema):
    def f(obj, name, type_, reflected, compare_to):
        # pylint: disable=unused-argument
        # Workaround what appears to be an alembic bug for multi-schema foreign
        # keys. This should still generate the initial foreign key contraint, but
        # stops repeated create/destroys of the constraint on subsequent runs.
        # TODO(calbach): File an issue against alembic.
        if type_ == "foreign_key_constraint" and obj.table.schema == "metrics":
            return False
        if name in autogen_blacklist:
            logger.info("skipping blacklisted %s", name)
            return False
        if type_ == "table" and reflected:
            # This normally wouldn't be necessary, except that our RDR models do not
            # specify a schema, so we would otherwise attempt to apply their tables
            # to the metrics DB. See option 1c on
            # https://docs.google.com/document/d/1FTmH-DDVlyY7BNsBzj0FV9m_kWQpCjKM__zK0GmIiCc
            return obj.schema == schema
        return True

    return f


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    for schema in db_schemas:
        url = uri_proto.replace('%engine%', db_engine)
        url = url.replace('%db%', schema)
        logger.info('database uri: {0}'.format(url))
        url = url.replace('%user%', 'root').replace('%passwd%', 'root')

        with open('{0}.sql'.format(schema), 'w') as handle:
            context.configure(
                url=url,
                target_metadata=target_metadata[schema],
                output_buffer=handle,
                literal_binds=True,
                include_schemas=True,
                include_object=include_object_fn(schema)
            )

            with context.begin_transaction():
                context.run_migrations(schema=schema)


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    for schema in db_schemas:
        url = uri_proto.replace('%engine%', db_engine)
        url = url.replace('%db%', schema)
        logger.info('database uri: {0}'.format(url))
        url = url.replace('%user%', 'root').replace('%passwd%', 'root')

        connectable = engine_from_config(
            # config.get_section(config.config_ini_section),
            # prefix="sqlalchemy.",
            {'url': url},
            prefix='',
            poolclass=pool.NullPool,
        )

        logger.info('migrating schema: {0}'.format(schema))

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata[schema],
                upgrade_token="{0}_upgrades".format(schema),
                downgrade_token="{0}_downgrades".format(schema),
                include_schemas=True,
                include_object=include_object_fn(schema)
            )

            with context.begin_transaction():
                context.run_migrations(schema=schema)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
