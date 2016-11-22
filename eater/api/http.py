# -*- coding: utf-8 -*-
"""
    eater.api
    ~~~~~~~~~

    Eater API classes and utilities.
"""

from abc import abstractmethod

import requests
from schematics import Model

from eater.api.base import BaseEater
from eater.errors import EaterTimeoutError, EaterConnectError, EaterUnexpectedError


class HTTPEater(BaseEater):
    """
    Eat JSON HTTP APIs for breakfast.
    """

    #: An instance of requests Session
    session = None

    #: The HTTP method to use to make the API call.
    method = 'get'

    def __init__(self, *,
                 session: requests.Session=None,
                 auth: tuple=None,
                 headers: requests.structures.CaseInsensitiveDict=None):

        if session is None:
            self.create_session(auth, headers)

    def __call__(self, *args, **kwargs):
        return self.request(*args, **kwargs)

    @property
    @abstractmethod
    def url(self) -> str:
        """
        Returns the URL to the endpoint.
        """

    def request(self, *, request_model: Model=None, **kwargs) -> Model:
        """
        Make a HTTP request of of type method.
        """
        request_model = self.create_request_model(request_model=request_model, **kwargs)
        kwargs = self.get_request_kwargs(request_model=request_model)

        try:
            response = getattr(self.session, self.method)(self.url, **kwargs)
            return self.create_response_model(response, request_model)

        except requests.Timeout:
            raise EaterTimeoutError("%s.%s for URL '%s' timed out." % (
                type(self).__name__,
                self.method,
                self.url
            ))

        except requests.RequestException as exc_info:
            raise EaterConnectError("Exception raised for URL '%s'." % self.url) from exc_info

    def create_response_model(self, response: requests.Response, request_model: Model) -> Model:  # pylint: disable=unused-argument
        """
        Given a requests Response object, return the response model.

        :param response: A requests.Response object representing the response from the API.
        :param request_model: The model used to generate the request.
        """
        if response.status_code >= 400:
            raise EaterUnexpectedError("Received unexpected HTTP response '%s %s' for URL '%s'." % (
                response.status_code,
                response.reason,
                response.url,
            ))

        if response.headers['content-type'] == 'application/json':
            raw_data = response.json()
            return self.response_cls(raw_data=raw_data, validate=True)

        raise NotImplementedError(
            "Content type '%s' is not implemented. Class %s should implement a handle_response method." % (
                response.headers['content-type'],
                type(self),
            )
        )

    def create_request_model(self, request_model: Model=None, **kwargs) -> Model:
        """
        Create the request model either from kwargs or request_model.
        """
        if request_model is None:
            request_model = self.request_cls(raw_data=kwargs)
        return request_model

    def get_request_kwargs(self, request_model: Model, **kwargs) -> dict:  # pylint: disable=no-self-use
        """
        Retrieve a dict of kwargs to supply to requests.
        """
        kwargs['json'] = request_model.to_primitive()
        return kwargs

    def create_session(self, auth: tuple=None, headers: requests.structures.CaseInsensitiveDict=None) -> requests.Session:
        """
        Create an instance of a requests Session.
        """
        if self.session is None:
            self.session = requests.Session()
            if auth:
                self.session.auth = auth
            if headers:
                self.session.headers.update(headers)
        return self.session
