=====
eater
=====

Consume APIs and hold them to account.

.. image:: https://travis-ci.org/alexhayes/eater.png?branch=master
    :target: https://travis-ci.org/alexhayes/eater
    :alt: Build Status

.. image:: https://landscape.io/github/alexhayes/eater/master/landscape.png
    :target: https://landscape.io/github/alexhayes/eater/
    :alt: Code Health

.. image:: https://codecov.io/github/alexhayes/eater/coverage.svg?branch=master
    :target: https://codecov.io/github/alexhayes/eater?branch=master
    :alt: Code Coverage

.. image:: https://readthedocs.org/projects/eater/badge/
    :target: http://eater.readthedocs.org/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/eater.svg
    :target: https://pypi.python.org/pypi/eater
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/eater.svg
    :target: https://pypi.python.org/pypi/eater/
    :alt: Supported Python versions


Not every API provider has an API as nice as Stripe_ and often their
documentation is incorrect or (arguably better) non-existent.

Not every API provider can manage their release cycle, like inform customers,
conform to semantic version numbers etc..

Chances are, if you're reading this, you're trying to talk to an API just like
this.

You want to be sure, when you send them something, they give you the right
thing back. That is, it contains the write shape of data and the correct data
types and if you're really persnickety, that it validates against defined rules.

Well, this Python library, with the help of schematics_, will allow you to do
just that.

Install
-------

.. code-block:: bash

    pip install eater


Usage
-----

Not that this has ever happened to anyone, ever... but let's say you are
dealing with an API that you don't necessarily trust. Perhaps the API is in
flux because it's alpha/beta or perhaps it's not versioned and changes get made
without notifying users. In any case, you want to be sure that what it says it
does, it definitely does.

Using eater, first you define the API to be consumed, in part using schematics_
models.

.. code-block:: python

    import eater
    from schematics import Model, IntegerType, StringType, BooleanType, ListType, ModelType

    class Book(Model):
        title = StringType(required=True, min_length=3)


    class Request(Model):
        """
        Represents, as a Python object, the JSON data required by the API.
        """
        in_print = BooleanType()


    class Response(Model):
        """
        Represents, as a Python object, the JSON response returned by the API.
        """
        books = ListType(ModelType(Book))

    class BooksAPI(eater.HTTPEater):
        url = 'https://example.com/books/'
        request_cls = Request
        response_cls = Response


You can then consume the API;

.. code-block:: python

    api = BooksAPI()
    response = api(in_print=True)

    for book in response.books:
        print(book.title)

See the full documentation at https://readthedocs.org/projects/eater

Author
------

Alex Hayes <alex@alution.com>


.. _schematics: http://github.com/schematics/schematics/
.. _Stripe: https://stripe.com/docs/api
