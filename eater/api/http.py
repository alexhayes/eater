# -*- coding: utf-8 -*-
"""
    eater.api
    ~~~~~~~~~

    Eater HTTP API classes.
"""

from abc import abstractmethod
from typing import Union

import requests
from schematics import Model

from eater.api.base import BaseEater
from eater.errors import EaterTimeoutError, EaterConnectError, EaterUnexpectedError


class HTTPEater(BaseEater):
    """
    Eat JSON HTTP APIs for breakfast.

    Instances of this class can't be created directly, you must subclass this class and set ``url`` and
    ``response_cls``.

    See :doc:`/usage` for more details.
    """

    #: Default request_cls to None
    request_cls = None

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
        Returns the URL to the endpoint - property must be defined by a subclass.
        """

    def get_url(self, request_model: Union[Model, None]) -> str:
        """
        Retrieve the URL to be used for the request.

        :param request_model: An instance of the ``request_cls`` or ``None``.
        :type request_model: Model|None
        :return: The URL to the API endpoint.
        :rtype: str
        """
        return self.url.format(request_model=request_model)

    def request(self, request_model: Model=None, **kwargs) -> Model:
        """
        Make a HTTP request of of type method.

        You should generally leave this method alone. If you need to customise the behaviour use the methods that
        this method uses.
        """
        request_model = self.create_request_model(request_model=request_model, **kwargs)
        url = self.get_url(request_model)
        kwargs = self.get_request_kwargs(request_model=request_model)

        try:
            response = getattr(self.session, self.method)(url, **kwargs)
            return self.create_response_model(response, request_model)

        except requests.Timeout:
            raise EaterTimeoutError("%s.%s for URL '%s' timed out." % (
                type(self).__name__,
                self.method,
                url
            ))

        except requests.RequestException as exc_info:
            raise EaterConnectError("Exception raised for URL '%s'." % url) from exc_info

    def create_response_model(self, response: requests.Response, request_model: Model) -> Model:  # pylint: disable=unused-argument
        """
        Given a requests Response object, return the response model.

        :param response: A requests.Response object representing the response from the API.
        :type response: requests.Response
        :param request_model: The model used to generate the request - an instance of ``request_cls``.
        :type request_model: schematics.Model
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

        :param request_model: An instance of ``request_cls`` or None.
        :type request_model: Model|None
        :param kwargs: kwargs to be supplied as the ``raw_data`` parameter when instantiating ``request_cls``.
        :type kwargs: dict
        :return: An instance of ``request_cls``.
        :rtype: schematics.Model
        """
        if request_model is None and self.request_cls is not None:
            request_model = self.request_cls(raw_data=kwargs)  # pylint: disable=not-callable
        return request_model

    def get_request_kwargs(self, request_model: Union[Model, None], **kwargs) -> dict:  # pylint: disable=no-self-use
        """
        Retrieve a dict of kwargs to supply to requests.

        :param request_model: An instance of ``request_cls`` or None.
        :type request_model: Model|None
        :param kwargs: kwargs to be supplied as the ``raw_data`` parameter when instantiating ``request_cls``.
        :type kwargs: dict
        :return: A dict of kwargs to be supplied to requests when making a HTTP call.
        :rtype: dict
        """
        if request_model is not None:
            kwargs['json'] = request_model.to_primitive()
        return kwargs

    def create_session(self, auth: tuple=None, headers: requests.structures.CaseInsensitiveDict=None) -> requests.Session:
        """
        Create an instance of a requests Session.

        :param auth: The ``auth`` kwarg when to supply when instantiating ``requests.Session``.
        :type auth: tupel|None
        :param headers: A dict of headers to be supplied as the ``headers`` kwarg when instantiating ``requests.Session``.
        :type headers: requests.structures.CaseInsensitiveDict
        :return: An instance of ``requests.Session``
        :rtype: requests.Session
        """
        if self.session is None:
            self.session = requests.Session()
            if auth:
                self.session.auth = auth
            if headers:
                self.session.headers.update(headers)
        return self.session
