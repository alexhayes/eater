# -*- coding: utf-8 -*-
"""
    eater.tests.api.base
    ~~~~~~~~~~~~~~~~~~~~

    Tests on :py:mod:`eater.api.base`
"""
import pytest
from schematics import Model

from eater import BaseEater


def test_can_subclass():
    class Person(BaseEater):
        request_cls = Model
        response_cls = Model
    Person()


def test_must_define_request_cls():
    class Person(BaseEater):  # pylint: disable=abstract-method
        response_cls = Model

    with pytest.raises(TypeError):
        Person()  # pylint: disable=abstract-class-instantiated


def test_must_define_response_cls():
    class Person(BaseEater):  # pylint: disable=abstract-method
        request_cls = Model

    with pytest.raises(TypeError):
        Person()  # pylint: disable=abstract-class-instantiated
