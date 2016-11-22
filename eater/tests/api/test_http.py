# -*- coding: utf-8 -*-
"""

    eater.tests.api.http
    ~~~~~~~~~~~~~~~~~~~~

    Tests on :py:mod:`eater.api.http`
"""

import pytest
import requests_mock
from requests.structures import CaseInsensitiveDict
from schematics import Model
from schematics.exceptions import DataError
from schematics.types import StringType

from eater import HTTPEater


def test_can_subclass():
    class PersonAPI(HTTPEater):
        request_cls = Model
        response_cls = Model
        url = 'http://example.com'
    PersonAPI()


def test_must_define_request_cls():
    class PersonAPI(HTTPEater):  # pylint: disable=abstract-method
        response_cls = Model
        url = 'http://example.com'

    with pytest.raises(TypeError):
        PersonAPI()  # pylint: disable=abstract-class-instantiated


def test_must_define_response_cls():
    class PersonAPI(HTTPEater):  # pylint: disable=abstract-method
        request_cls = Model
        url = 'http://example.com'

    with pytest.raises(TypeError):
        PersonAPI()  # pylint: disable=abstract-class-instantiated


def test_must_define_url():
    class PersonAPI(HTTPEater):  # pylint: disable=abstract-method
        request_cls = Model
        response_cls = Model

    with pytest.raises(TypeError):
        PersonAPI()  # pylint: disable=abstract-class-instantiated


def test_get_request():
    class Person(Model):
        name = StringType()

    class PersonAPI(HTTPEater):
        request_cls = Person
        response_cls = Person
        url = 'http://example.com/person'

    api = PersonAPI()
    expected_person = Person(dict(name='John'))

    with requests_mock.Mocker() as mock:
        mock.get(
            api.url,
            json=expected_person.to_primitive(),
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json'
            })
        )

        actual_person = api(name=expected_person.name)

        assert actual_person == expected_person


def test_data_error_raised():
    class Person(Model):
        name = StringType(required=True, min_length=4)

    class PersonAPI(HTTPEater):
        request_cls = Person
        response_cls = Person
        url = 'http://example.com/person'

    api = PersonAPI()

    with pytest.raises(DataError):
        with requests_mock.Mocker() as mock:
            mock.get(
                api.url,
                json={'name': 'Joh'},
                headers=CaseInsensitiveDict({
                    'Content-Type': 'application/json'
                })
            )
            api(name='John')
