Developer Documentation
=======================

Contributions
-------------

Contributions are more than welcome!

To get setup do the following;

.. code-block:: bash

    mkvirtualenv --python=/usr/bin/python3.5 eater
    git clone https://github.com/alexhayes/eater.git
    cd eater
    pip install -r requirements/dev.txt


Running Tests
-------------

Once you've checked out you should be able to run the tests;

.. code-block:: bash

    tox

Or run all environments at once using detox;

.. code-block:: bash

    detox

Or simply run with py.test;

.. code-block:: bash

    py.test


Linting
-------

Running pylint is easy and is part of the CI;

.. code-block:: pylint

    pylint eater


Creating Documentation
----------------------

.. code-block:: bash

    cd docs
    make apidoc clean html

