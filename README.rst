Django Copywriting
============

Copywriting is the act of writing copy (text) for the purpose of advertising or marketing a product, business, person, opinion or idea. The addressee (reader, listener, etc.) of the copy is meant to be persuaded to buy the product advertised for, or subscribe to the viewpoint the text shares.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-copywriting

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/arteria/django-copywriting.git#egg=copywriting

TODO: Describe further installation steps (edit / remove the examples below):

Add ``copywriting`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'copywriting',
    )

Add the ``copywriting`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^blog/', include('copywriting.urls')),
    )

Before your tags/filters are available in your templates, load them by using

.. code-block:: html

	{% load copywriting_tags %}


Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate copywriting


Usage
-----

TODO:

- Describe usage or point to docs. Also describe available settings and templatetags.
- Add dependencies
- Better Installation Guide

Set the FEED_SETTINGS in your projects settings.py file, here is an example:

.. code-block:: python

    FEED_SETTINGS = {
        'title': "My awesome Blog",
        'link': "/blog/",
        'description': "Don't miss any of my new posts",
        'author_email': "me@domain.ch",
        'author_name': "Scrooge McDuck",
        'author_link': "https://www.domain.ch/",
        'feed_url': "https://www.domain.ch/blog/feed/",
        'categories': [
            'DuckTales',
            'Daisy Duck',
            ]
    }


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-copywriting
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch

.. image:: https://d2weczhvl823v0.cloudfront.net/philippeowagner/django-history/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free