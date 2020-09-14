# =============================================================================
# Minet Argparse Helpers
# =============================================================================
#
# Miscellaneous helpers related to CLI argument parsing.
#
from argparse import Action, ArgumentTypeError

from minet.crowdtangle.constants import CROWDTANGLE_PARTITION_STRATEGIES
from minet.utils import nested_get


class BooleanAction(Action):
    """
    Custom argparse action to handle --no-* flags.
    Taken from: https://thisdataguy.com/2017/07/03/no-options-with-argparse-and-python/
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(BooleanAction, self).__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, False if option_string.startswith('--no') else True)


class CrowdtanglePartitionStrategyType(object):
    def __call__(self, string):
        if string in CROWDTANGLE_PARTITION_STRATEGIES:
            return string

        try:
            return int(string)
        except ValueError:
            choices = ' or '.join(CROWDTANGLE_PARTITION_STRATEGIES)

            raise ArgumentTypeError('partition strategy should either be %s, or an number of posts.' % choices)


class SplitterType(object):
    def __init__(self, splitchar=','):
        self.splitchar = splitchar

    def __call__(self, string):
        return string.split(self.splitchar)


class WrappedConfigValue(object):
    def __init__(self, key, value=None):
        self.key = key
        self.value = value

    def resolve(self, config):
        if self.value is not None:
            return self.value

        return nested_get(self.key, config)


class ConfigAction(Action):
    def __init__(self, option_strings, dest, rc_key, **kwargs):
        super(ConfigAction, self).__init__(option_strings, dest, default=WrappedConfigValue(rc_key), **kwargs)
        self.rc_key = rc_key

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, WrappedConfigValue(self.rc_key, values))
