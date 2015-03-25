Django Copywriting
============

Copywriting is the act of writing copy (text) for the purpose of advertising or marketing a product, business, person, 
opinion or idea. The addressee (reader, listener, etc.) of the copy is meant to be persuaded to buy the product advertised 
for, or subscribe to the viewpoint the text shares.

Features
--------

* Generic Author Model support
* Articles
* Automatically generated Feed 
* Tags / search by tags
* Ping Google on publish
* Workflow (Draft -> Review -> Ready to Publish -> Published)
* Automatically register Articles for search if https://github.com/etianen/django-watson is installed
* Get next/prev published article 
* Comments powered by https://disqus.com/ 

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-copywriting (not pushed yet! use latest commit from GitHub)

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

	{% load blogtags %}


Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate copywriting


Usage
-----


Sitemaps
--------

Add the following lines to your ``urls.py``

	
.. code-block:: python

	from copywriting.sitemaps import BlogSitemap
	sitemaps = {
	    'blog': BlogSitemap,
	}
	
	# in patterns... 
	
	url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),


Make sure that ``'django.contrib.sitemaps'`` is in your ``INSTALLED_APPS``.

Comments
--------

To use comments add a shortname and a context_processor to your settings:

.. code-block:: python

	DISQUS_SHORTNAME = 'example'
	
	TEMPLATE_CONTEXT_PROCESSORS = (
		# ...
		'copywriting.context_processors.disqus_shortname',
		# ...
	)


The comments will render where the div with the id="disqus_thread" is located:

.. code-block:: html

    	<div id="disqus_thread"></div>

The comments are controlled with the comments_enabled boolean in the article entity.

Signals
-------

You can catch a signal when a article changes to "ready to review" or "ready to publish". Here is an example:

.. code-block:: python

	from django.dispatch import receiver
	from copywriting.signals import ready_to_review
	from copywriting.signals import ready_to_publish
	
	@receiver(ready_to_publish)
	def notify_publisher(sender, **kwargs):
	    print "New article with ID=%s" % kwargs['articleID']
		
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

Known issues, TODOs and planned features
----------------------------------------

* ImageBucketObject is missing! Issue #5
* ImageCropping dependencies
* Translation added for ``desc`` so manual migrations of the DB are required. Add the new rows and rename ``desc`` to your primary language. This would be ``desc_de`` in case you start with German.




Contribute
----------

If you want to contribute to this project, just send us your pull requests. Thanks.
