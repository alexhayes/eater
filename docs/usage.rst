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


Once you've defined models that represent the APIs input/output you then create
a class that inherits ``eater.HTTPEater``. Your class must define a ``url``,
``request_cls`` and ``response_cls``.

.. code-block:: python

    import eater
    
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

Note that you *call* the actual instance and can pass in ``kwargs`` that are
used to create an instance of your ``Request`` model.

It's also possible to pass in an instance of your request model;

.. code-block:: python

    request_model = Request({'in_print': True})
    response = api(request_model=request_model)


Holding the API to account
--------------------------

That's right, we were concerned our API wasn't going to do what it said it
would. That would be hard to imagine for the trivial example we have above
however accidents do happen, developers are only human.

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
        response = api(in_print=True)
    except DataError as e:
        # Oh no, our API provider didn't give us back what they said they would
        # e would now contain something like:
        # schematics.exceptions.DataError: {'title': ValidationError("String value is too short.")}


HTTP request type
-----------------

By default ``HTTPEater`` performs a HTTP ``GET`` request, you can change this
by setting ``method`` on your API class;

.. code-block:: python

    class BooksAPI(eater.HTTPEater):
        method = 'post'
        ...

Or alternatively at runtime;

.. code-block:: python

    api = BooksAPI()
    api.method = 'post'

Any request method supported by requests_ is supported, ie... ``PUT, DELETE,
HEAD, OPTIONS``.

Dynamic URL
-----------

The ``url`` is just a property, thus you can define it dynamically;

.. code-block:: python

    class BooksAPI(eater.HTTPEater):

        @property
        def url(self):
            return 'http://path.to.awesome/'


Control Request Parameters
--------------------------

You can control the params, or any kwarg supplied to requests_ by defining a
``get_request_kwargs`` method in your class.

.. code-block:: python

    class BooksAPI(eater.HTTPEater):

        def get_request_kwargs(self, request_model: Request, **kwargs) -> dict:
            """
            Retrieve a dict of kwargs to supply to requests.
            """
            kwargs['params'] = {
                'in_print': request_model
            }
            return kwargs

However, a better way of settings ``kwargs['params']`` above would be;

.. code-block:: python

    kwargs['params'] = request_model.to_primitive()


Auth, Headers & Sessions
------------------------

Under the covers HTTPEater automatically creates a requests.Session for you.

When you create an instance of HTTPEater you can pass through kwargs that will
be applied to this generated session, or optionally you can pass in a session
object of your creation.

.. code-block:: python

    api = BooksAPI(auth=('john', 's3cr3t'))

Need to set a custom header?

.. code-block:: python

    api = BooksAPI(headers={'EGGS': 'Sausage'})

Or do something really special with your own custom session?

.. code-block:: python

    session = requests.Session()
    api = BooksAPI(session=session)

Alternatively you can override the ``create_session`` method on your ``BooksAPI``
class;

.. code-block:: python

    class BooksAPI(eater.HTTPEater):
        url = 'https://example.com/books/'
        request_cls = Request
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


More Control
------------

You can break into all aspects of eater's lifecycle, simply by overriding any
one of the methods it uses to call and parse the response from your friendly
API.

See the :doc:`internals/reference/index` for more details.


.. _schematics: http://github.com/schematics/schematics/
.. _requests: https://github.com/kennethreitz/requests/
