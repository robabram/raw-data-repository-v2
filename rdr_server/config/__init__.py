#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
# https://stackoverflow.com/questions/6198372/most-pythonic-way-to-provide-global-configuration-variables-in-config-py

import importlib
import os


class ConfigSection(object):
    """
    Configuration Section
    """

    def __init__(self, *args):
        self.__header__ = str(args[0]) if args else None

    def __repr__(self):
        if self.__header__ is None:
            return super(ConfigSection, self).__repr__()
        return self.__header__

    def next(self):
        """ Fake iteration functionality.
        """
        raise StopIteration

    def __iter__(self):
        """ Fake iteration functionality.
        We skip magic attributes and Structs, and return the rest.
        """
        ks = self.__dict__.keys()
        for k in ks:
            if not k.startswith('__') and not isinstance(k, ConfigSection):
                yield getattr(self, k)

    def __len__(self):
        """ Don't count magic attributes or Structs.
        """
        ks = self.__dict__.keys()
        return len([k for k in ks if not k.startswith('__') and not isinstance(k, ConfigSection)])


if 'GCP_PROJECT' not in os.environ:
    raise KeyError('GCP_PROJECT environment variable not set to a valid project.')

config = importlib.import_module('.{0}'.format(os.environ['GCP_PROJECT']), 'config')
config.__dict__.pop('ConfigSection', None)
config.__dict__['GCP_PROJECT'] = os.environ['GCP_PROJECT']
