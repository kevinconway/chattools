=========
chattools
=========

*Demo tools for extracting metadata from chat lines.*

Example Usage
=============

Emoticons
---------

.. code-block:: python

    from chattools import emoticon
    print(tuple(emoticon.emoticons('Some message with (emoticons) here.')))

HREFs
-----

.. code-block:: python

    from chattools import href
    urls = tuple(href.hrefs('Some message with https://sites.com in it.'))
    titles = tuple(href.titles(urls))
    print(zip(urls, titles))

@Mentions
---------

.. code-block:: python

    from chattools import mention
    print(tuple(mention.mentions('Some message with @mentions in it.')))

Metadata
--------

.. code-block:: python

    from chattools import metadata
    meta = metadata.Metadata('Some message.')
    print(tuple(meta.mentions))
    print(tuple(meta.hrefs))
    print(tuple(meta.emoticons))
    print(meta.json)

Testing
=======

All tests are organized in the 'tests' subdirectory. The layout of the test
modules is paired one-to-one with the modules they test. For example, the tests
for chattools.mentions are found in tests/test_mentions.py. Attempt to
maintain this organization when adding new tests.

This repository comes with a tox.ini file which is configured to run a fairly
exhaustive set of tests. All the current unit tests run, and pass, under Python
2.6, 2.7, 3.2, 3.3, and 3.4 interpreters. Running the default tox command will
attempt to run the tests in all these environments. In addition, tox is also
configured to run PEP8, PyFlakes, and PyLint checks. The PyLint checks will
make use of the .pylintrc file also included in this repository.

License
=======

::

    (MIT License)

    Copyright (C) 2015 Kevin Conway

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.


Contributing
============

All contributions to this project are protected under the agreement found in
the `CONTRIBUTING` file. All contributors should read the agreement but, as
a summary::

    You give us the rights to maintain and distribute your code and we promise
    to maintain an open source distribution of anything you contribute.
