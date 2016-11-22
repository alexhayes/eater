# -*- coding: utf-8 -*-
"""
    eater.errors
    ~~~~~~~~~~~~

    A place for errors that are raised by Eater.
"""

__all__ = [
    'EaterError',
    'EaterTimeoutError',
    'EaterConnectError',
    'EaterUnexpectedError',
    'EaterUnexpectedResponseError'
]


class EaterError(Exception):
    """
    Base Eater error.
    """


class EaterTimeoutError(EaterError):
    """
    Raised if something times out.
    """


class EaterConnectError(EaterError):
    """
    Raised if there is a connection error.
    """


class EaterUnexpectedError(EaterError):
    """
    Raised when something unexpected happens.
    """


class EaterUnexpectedResponseError(EaterUnexpectedError):
    """
    Raised when a response from an API is unexpected.
    """
