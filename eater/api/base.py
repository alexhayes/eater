# -*- coding: utf-8 -*-
"""
    eater.api.base
    ~~~~~~~~~~~~~~

    Base Eater API classes and utilities.
"""
from abc import ABC, abstractmethod
from typing import Union, Callable

from schematics import Model


class BaseEater(ABC):
    """
    Base Eater class.
    """

    @property
    @abstractmethod
    def request_cls(self) -> Callable[..., Union[Model, None]]:
        """
        A schematics model that represents the API request.
        """

    @property
    @abstractmethod
    def response_cls(self) -> Callable[..., Model]:
        """
        A schematics model that represents the API response.
        """
