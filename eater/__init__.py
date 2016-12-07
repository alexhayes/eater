# -*- coding: utf-8 -*-
"""Consume APIs and hold them to account."""
# :copyright: (c) 2016 Alex Hayes,
#                 All rights reserved.
# :license:   MIT License, see LICENSE for more details.
from __future__ import absolute_import, print_function, unicode_literals
from collections import namedtuple

VersionInfo = namedtuple(
    'VersionInfo', ('major', 'minor', 'micro', 'releaselevel', 'serial'),
)

VERSION = VersionInfo(0, 3, 1, '', '')
__version__ = '{0.major}.{0.minor}.{0.micro}{0.releaselevel}'.format(VERSION)
__author__ = 'Alex Hayes'
__contact__ = 'alex@alution.com'
__homepage__ = 'http://github.com/alexhayes/eater'
__docformat__ = 'restructuredtext'

# -eof meta-

from eater.api.base import BaseEater  # pylint: disable=wrong-import-position
from eater.api.http import HTTPEater  # pylint: disable=wrong-import-position
from eater.errors import *  # pylint: disable=wrong-import-position,wildcard-import
