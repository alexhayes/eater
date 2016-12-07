# -*- coding: utf-8 -*-
"""

    eater.tests.api.http
    ~~~~~~~~~~~~~~~~~~~~

    Tests on :py:mod:`eater.api.http`
"""

import pytest
import requests
from requests.structures import CaseInsensitiveDict
import requests_mock
from schematics import Model
from schematics.exceptions import DataError
from schematics.types import StringType, IntType, ModelType

from eater import HTTPEater, EaterTimeoutError, EaterConnectError, EaterUnexpectedError


def test_can_subclass():
    class PersonAPI(HTTPEater):
        request_cls = Model
        response_cls = Model
        url = 'http://example.com'
    PersonAPI()


def test_request_cls_defaults_none():
    class PersonAPI(HTTPEater):  # pylint: disable=abstract-method
        response_cls = Model
        url = 'http://example.com'

    api = PersonAPI()
    assert api.request_cls is None


def test_get_url_with_request_cls_none():  # pylint: disable=invalid-name
    class PersonAPI(HTTPEater):  # pylint: disable=abstract-method
        response_cls = Model
        url = 'http://example.com'

    api = PersonAPI(None)
    assert api.url == 'http://example.com'


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

    expected_person = Person(dict(name='John'))
    api = PersonAPI(name=expected_person.name)

    with requests_mock.Mocker() as mock:
        mock.get(
            api.url,
            json=expected_person.to_primitive(),
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json'
            })
        )

        actual_person = api()
        assert actual_person == expected_person

        # Now check that api can take a model as the first parameter
        api = PersonAPI(expected_person)
        actual_person = api()
        assert actual_person == expected_person


def test_post_request():
    class Person(Model):
        pk = IntType()  # pylint: disable=invalid-name
        name = StringType()

    class UpdatePersonResponse(Model):
        status = StringType()
        person = ModelType(Person)

    class UpdatePersonAPI(HTTPEater):
        request_cls = Person
        response_cls = UpdatePersonResponse
        method = 'post'
        url = 'http://example.com/person/{request_model.pk}/'

    expected_request = Person(dict(pk=1, name='John'))
    expected_response = UpdatePersonResponse(dict(status='success', person=expected_request))
    api = UpdatePersonAPI(expected_request)

    with requests_mock.Mocker() as mock:
        mock.post(
            api.url,
            json=expected_response.to_primitive(),
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json'
            })
        )

        actual_response = api()
        assert actual_response == expected_response

        # Assert we sent the correct request
        assert mock.called is True
        assert mock.call_count == 1
        request = mock.request_history[0]
        actual_request = api.request_cls(request.json())
        assert actual_request.to_primitive() == expected_request.to_primitive()
        requests_mock.request_history = None


def test_request_cls_none():
    class Person(Model):
        name = StringType()

    class PersonAPI(HTTPEater):
        request_cls = None
        response_cls = Person
        url = 'http://example.com/person'

    expected_person = Person(dict(name='John'))
    api = PersonAPI(name=expected_person.name)

    with requests_mock.Mocker() as mock:
        mock.get(
            api.url,
            json=expected_person.to_primitive(),
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json'
            })
        )

        actual_person = api()
        assert actual_person == expected_person


def test_data_error_raised():
    class Person(Model):
        name = StringType(required=True, min_length=4)

    class PersonAPI(HTTPEater):
        request_cls = Person
        response_cls = Person
        url = 'http://example.com/person'

    api = PersonAPI(name='John')

    with pytest.raises(DataError):
        with requests_mock.Mocker() as mock:
            mock.get(
                api.url,
                json={'name': 'Joh'},
                headers=CaseInsensitiveDict({
                    'Content-Type': 'application/json'
                })
            )
            api()


def test_url_formatting():
    class Person(Model):
        name = StringType()

    class GetPersonAPI(HTTPEater):
        request_cls = Person
        response_cls = Person
        url = 'http://example.com/person/{request_model.name}/'

    expected_url = 'http://example.com/person/John/'

    api = GetPersonAPI(name='John')
    assert api.url == expected_url

    with requests_mock.Mocker() as mock:
        mock.get(
            expected_url,
            json={'name': 'John'},
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json'
            })
        )
        response = api()
        assert response.name == 'John'


def test_get_url():
    class Person(Model):
        name = StringType()

    class GetPersonAPI(HTTPEater):
        request_cls = Person
        response_cls = Person
        url = 'http://example.com/person/'

        def get_url(self) -> str:
            return '%s%s/' % (type(self).url, self.request_model.name)

    expected_url = 'http://example.com/person/John/'

    api = GetPersonAPI(name='John')
    assert api.url == expected_url

    with requests_mock.Mocker() as mock:
        mock.get(
            'http://example.com/person/John/',
            json={'name': 'John'},
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/json'
            })
        )
        response = api()
        assert response.name == 'John'


def test_requests_parameter():
    class GetPersonAPI(HTTPEater):
        request_cls = Model
        response_cls = Model
        url = 'http://example.com/person/'

    api = GetPersonAPI(_requests={
        'auth': ('john', 's3cr3t'),
        'headers': {
            'EGGS': 'Sausage'
        }
    })
    assert api.session.auth == ('john', 's3cr3t')
    assert api.session.headers['EGGS'] == 'Sausage'


def test_create_session():
    class GetPersonAPI(HTTPEater):
        request_cls = Model
        response_cls = Model
        url = 'http://example.com/person/'

        def create_session(self, session: requests.Session=None, **kwargs):  # pylint: disable=unused-argument
            session = requests.Session()
            session.auth = ('john', 's3cr3t')
            return session

    api = GetPersonAPI()
    assert api.session.auth == ('john', 's3cr3t')


def test_requests_timeout():
    class GetPersonAPI(HTTPEater):
        request_cls = Model
        response_cls = Model
        url = 'http://example.com/'

    def timeout(*args, **kwargs):  # pylint: disable=unused-argument
        raise requests.Timeout()

    api = GetPersonAPI()

    with requests_mock.Mocker() as mock:
        mock.get(
            'http://example.com/',
            text=timeout
        )
        with pytest.raises(EaterTimeoutError):
            api()


def test_requests_connecterror():
    class GetPersonAPI(HTTPEater):
        request_cls = Model
        response_cls = Model
        url = 'http://example.com/'

    def connect(*args, **kwargs):  # pylint: disable=unused-argument
        raise requests.ConnectionError()

    api = GetPersonAPI()

    with requests_mock.Mocker() as mock:
        mock.get(
            'http://example.com/',
            text=connect
        )
        with pytest.raises(EaterConnectError):
            api()


def test_status_code_gte_400():
    class GetPersonAPI(HTTPEater):
        request_cls = Model
        response_cls = Model
        url = 'http://example.com/'

    api = GetPersonAPI()

    with requests_mock.Mocker() as mock:
        mock.get(
            'http://example.com/',
            status_code=400,
        )
        with pytest.raises(EaterUnexpectedError):
            api()


def test_non_json_content_response():
    class GetPersonAPI(HTTPEater):
        request_cls = Model
        response_cls = Model
        url = 'http://example.com/'

    api = GetPersonAPI()

    with requests_mock.Mocker() as mock:
        mock.get(
            'http://example.com/',
            text='Hello world',
            headers=CaseInsensitiveDict({
                'Content-Type': 'text/plain'
            })
        )
        with pytest.raises(NotImplementedError):
            api()
