=====
Usage
=====

Quickstart
----------

Let's get started with a trivial example, this usage assumes you are familiar
with schematics_ (v2.x) and somewhat familiar with requests_.

Firstly, define models that represent the API you have the fortunate pleasure
of communicating with.

.. code-block:: python

    from schematics import Model
    from schematics.types import ListType, ModelType, StringType

    class Book(Model):
        title = StringType(required=True, min_length=3)


    class BookListResponse(Model):
        """
        Represents, as a Python object, the JSON response returned by the API.
        """
        books = ListType(ModelType(Book))

Once you've defined models that represent the APIs input/output you then create
a class that inherits ``eater.HTTPEater``. Your class must define a ``url``,
``request_cls`` and ``response_cls``.

.. code-block:: python

    import eater

    class BookListAPI(eater.HTTPEater):
        url = 'http://example.com/books/'
        response_cls = BookListResponse

You can then consume the API;

.. code-block:: python

    api = BookListAPI()

    response = api()

    for book in response.books:
        print(book.title)

Note that you *call* the actual instance of your API class.


Holding the API to account
--------------------------

That's right, we were concerned our API wasn't going to do what it said it
would. That would be hard to imagine for the trivial example we have above
however accidents do happen, developers are only human right?!

Remember our definition of a book?

.. code-block:: python

    class Book(Model):
        title = StringType(required=True, min_length=3)

If for some reason the endpoint at https://example.com/books/ returned a book
that contained a title less than three characters in length schematics would
kindly raise a ``DataError`` for us.

For example;

.. code-block:: python

    from schematics.exceptions import DataError

    try:
        response = api()
    except DataError as e:
        # Oh no, our API provider didn't give us back what they said they would
        # e would now contain something like:
        # schematics.exceptions.DataError: {'title': ValidationError("String value is too short.")}


HTTP request type
-----------------

By default ``HTTPEater`` performs a HTTP ``GET`` request however you can change
this by setting ``method`` on your API class;

.. code-block:: python

    class BookCreateAPI(eater.HTTPEater):
        method = 'post'
        ...

Any request method supported by requests_ is supported, ie... ``get, post, put,
delete, head, options``.


Post Data
---------

You can send a JSON object over the wire by defining a ``request_cls`` on your API
class, as follows;

.. code-block:: python

    class BookCreateAPI(eater.HTTPEater):
        url = 'http://example.com/books/'
        method = 'post'
        request_cls = Book
        response_cls = Book

You can then call your API as follows;

.. code-block:: python

    api = BookCreateAPI()
    response = api(name='Awesome Book')

Which would result in the following JSON payload being sent to the server;

.. code-block:: json

    {
        name: "Awesome Book"
    }

It's also possible to pass in an instance of your ``request_cls`` as the first
(and only) parameter.

.. code-block:: python

    book = Book({'name': 'Awesome Book'})
    response = api(book)

Dynamic URL
-----------

The ``url`` can contain string formatting that refers the request model, like so;

.. code-block:: python

    class GetBookRequest(Model):
        id = IntType(required=True, min_value=1)


    class GetBookAPI(eater.HTTPEater):
        url = 'http://path.to.awesome/{request_model.id}'
        request_cls = GetBookRequest
        response_cls = Book

For more control you can also override the ``get_url`` method;

.. code-block:: python

    class GetBookAPI(eater.HTTPEater):
        url = 'http://path.to.awesome/'
        request_cls = GetBookRequest
        response_cls = Book

        def get_url(self, request_model: Model) -> str:
            if request_model.id < 100:
                return 'http://path.to.less.awesome/'
            else:
                return self.url


More Control
------------

You can control any kwarg supplied to requests_ by defining a
``get_request_kwargs`` method in your API class.

For instance, if you want to `pass some parameters in the URL <http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls>`_;

.. code-block:: python

    class BookListAPI(eater.HTTPEater):

        def get_request_kwargs(self, request_model: BookListRequest, **kwargs) -> dict:
            """
            Returns a dict of kwargs to supply to requests.
            """
            kwargs['params'] = {
                'in_print': request_model.in_print
            }
            return kwargs

However, a better way of setting ``kwargs['params']`` above would be;

.. code-block:: python

    kwargs['params'] = request_model.to_primitive()

Calling ``to_primitive()`` on your model returns a dict of native python types
suitable for sending over the wire. See the `schematics docs <http://schematics.readthedocs.io/en/latest/usage/exporting.html#primitive-types>`_
for more information.


Auth, Headers & Sessions
------------------------

Under the covers ``HTTPEater`` automatically creates a ``requests.Session`` for
you.

When you create an instance of your API class that inherits ``HTTPEater`` you can
pass through kwargs that will be applied to this generated session, or optionally
you can pass in a session object of your creation.

.. code-block:: python

    api = BookListAPI(auth=('john', 's3cr3t'))

Need to set a custom header?

.. code-block:: python

    api = BookListAPI(headers={'EGGS': 'Sausage'})

Or need to do something really special with your own custom session?

.. code-block:: python

    session = requests.Session()
    api = BookListAPI(session=session)

Alternatively you can override the ``create_session`` method on your ``BookListAPI``
class;

.. code-block:: python

    class BookListAPI(eater.HTTPEater):
        url = 'https://example.com/books/'
        request_cls = BookListRequest
        response_cls = Response

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


Control everything!
-------------------

You can break into all aspects of eater's lifecycle by overriding methods on your
API class;

- :py:meth:`.HTTPEater.get_url` - Modify the URL
- :py:meth:`.HTTPEater.create_request_model` - Modify the creation of your ``request_model``
- :py:meth:`.HTTPEater.get_request_kwargs` - Modify the kwargs supplied to requests_
- :py:meth:`.HTTPEater.create_response_model` - Modify the creation of the ``response_model`` from the requests response.
- :py:meth:`.HTTPEater.create_session` - Modify the creation of the session.

See the :doc:`internals/reference/index` for more details.


.. _schematics: http://github.com/schematics/schematics/
.. _requests: https://github.com/kennethreitz/requests/
