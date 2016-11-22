=====
eater
=====

Python library to consume APIs and hold them to account.


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

Contents
--------

.. toctree::
 :maxdepth: 1

 installation
 usage
 developer
 internals/reference/index


License
-------

This software is licensed under the `MIT License`. See the `LICENSE`_.


Author
------

Alex Hayes <alex@alution.com>

.. _LICENSE: https://github.com/alexhayes/eater/blob/master/LICENSE
.. _schematics: http://github.com/schematics/schematics/
.. _Stripe: https://stripe.com/docs/api
